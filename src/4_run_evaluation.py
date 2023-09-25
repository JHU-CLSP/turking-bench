import argparse
from colorama import init as colorama_init
from colorama import Fore
import configparser
from evaluation.actions import MyActions
from evaluation.input import Input
from evaluation import baselines
import json
import os
import pandas as pd
import numpy as np
import random
import requests
from rouge_score import rouge_scorer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import shutil
import string
from transformers import AutoTokenizer
from tqdm import tqdm
from typing import List
import logging

TURKLE_URL = "http://localhost:8000"

colorama_init(autoreset=True)


class GPTTokenizer:
    gpt_tokenizer = AutoTokenizer.from_pretrained("gpt2", max_length=1e5)

    def tokenize(self, s):
        tokens = self.gpt_tokenizer.tokenize(s)
        # GPT2 uses Byte-level BPE, which will include space as part of the word.
        # But for the first word of a sentence, there is no space before it.
        # So, we remove all the added spaces ("Ġ").
        tokens = [t.lstrip("Ġ") for t in tokens]
        return tokens


class Evaluation:
    def __init__(self, solver_type: str, tasks: str, do_eval: bool, dump_features: bool, report_field_stats: bool):
        self.default_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        self.xlingual_tokenizer = GPTTokenizer()
        self.xlingual_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], tokenizer=self.xlingual_tokenizer)
        self.driver = self.create_driver()
        self.actions = MyActions(self.driver)
        self.solver = None
        # ass more solvers that we implement, we can add them here:
        self.solver_type = solver_type
        if solver_type == "random":
            self.solver = baselines.RandomBaseline(driver=self.driver, actions=self.actions)
        elif solver_type == "oracle":
            self.solver = baselines.OracleBaseline(driver=self.driver, actions=self.actions)
        else:
            raise Exception(f"{Fore.RED}Solver `{solver_type}` not implemented")
        self.tasks = tasks
        assert tasks in ["test", "train", "all", "subjective_test"]

        self.do_eval = do_eval
        self.dump_features = dump_features
        self.report_field_stats = report_field_stats

        # as soon as the code is loaded, we look for alignnent between the task names and their ids
        self.task_ids = requests.get(f"{TURKLE_URL}/get_tasks/").json()

        # exclude special inputs
        self.excluded_input_names = [
            'csrfmiddlewaretoken',  # hidden field automatically added external css files
            'worker_ip',  # hidden field for bookkeeping
            'ee'
        ]

    def create_driver(self):
        # TODO: make the seleciton of headless (no visual browser for faster processing) a parameter
        options = Options()

        import platform
        if platform.system() == 'Linux':
            options.headless = True
            driver = webdriver.Chrome(options=options)
        elif platform.system() == "Darwin":
            # options.headless = True
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Firefox()

        return driver

    def load_task_names(self):
        """
        This function returns the list of tasks for a given setup.
        """

        # load all tasks
        all_tasks = os.listdir("../tasks")

        if self.tasks == 'all':
            return all_tasks
        else:
            with open('../data/splits/evaluation_tasks.txt', 'r') as f:
                test = f.read().splitlines()

            with open('../data/splits/subjective_evaluation_tasks.txt', 'r') as f:
                subjective_test = f.read().splitlines()

            # make sure that the splits are exclusive
            assert len(set(test).intersection(set(subjective_test))) == 0, f"{Fore.RED}The test and subjective test " \
                                                                           f"splits are not exclusive\n: test: {test}\nsubjective_test: {subjective_test}"

            if self.tasks == 'test':
                return test
            elif self.tasks == 'subjective_test':
                return subjective_test
            elif self.tasks == 'train':
                # all tasks minue test and subjective test
                return list(set(all_tasks) - set(test) - set(subjective_test))
            else:
                raise Exception(f"{Fore.RED}Invalid setup: {self.tasks}")

    def extract_input_values_from_url(self, url, task_name, input_names=None) -> List[Input]:
        """
        This utility function extracts the list of input fields that could be filled in.
        Then for each input field, it identifies their type (text area, checkbox, etc.)
        Note, for doing this we don't use BeautifulSoup because it does not capture the dynamic nature of the page.
        :param url: the url to extract the input fields from
        :param input_names: a list of input names to extract
        :return: a list of input names and their types
        """
        # TODO I think we can drop "url" parameter later.

        # if a list of input names are provided in the input, then extract the input fields with those names
        # otherwise, look for inputs that may look like input fields
        if input_names:
            inputs = []
            for name in input_names:
                # use selenium to find the input field
                try:
                    element = self.driver.find_element(By.NAME, name)
                    # check if the element is of type input, select or textarea
                    if element.tag_name in ['input', 'select', 'textarea']:
                        inputs.append(element)
                except:
                    # the reason that we have try-catch here is becuase elements exists in CSV but they're not created
                    # in HTML (they're created dynamically via JS). An exmaple task is "HTER - longer sentences -27 Sep 1129"
                    print(f"{Fore.RED}Could not find input field with name `{name}`")
        else:
            inputs = self.driver.find_elements(By.XPATH, '//input | //textarea | //select')

        # filter out the elements if their name is in the excluded list
        inputs = [input for input in inputs if input.get_attribute('name') not in self.excluded_input_names]

        # now for our list of inputs, indentify their types
        input_fields = []
        for input in inputs:
            if input.tag_name in ['input']:
                input_type = input.get_attribute('type')
                if not input_type:
                    input_type = 'text'
            elif input.tag_name == 'textarea':
                input_type = 'textarea'
            elif input.tag_name == 'select':
                input_type = 'select'
            else:
                raise Exception(f"{Fore.RED}to be implemented for tag name `{input.tag_name}`")

            input_name = input.get_attribute('name')
            if not input_name:
                raise Exception(f"{Fore.RED}to be implemented for tag name `{input.tag_name}`")

            i = Input(url=url, input_name=input_name, input_type=input_type, task_name=task_name)

            # save the y-coordinate of the input field
            i.y = input.location['y']

            # save the x-coordinate of the input field
            i.x = input.location['x']

            # save the position in html source: self.driver.page_source
            i.html_pos = self.driver.page_source.find(input_name)

            input_fields.append(i)

        # before returning them, sort the input values based on first based on their x-coordinate and then their y-coordinate
        input_fields = sorted(input_fields, key=lambda i: (i.y, i.x))
        return input_fields

    def extract_values(self, inputs: List[Input]):
        """
        Given a set of values for the input fields, extract the values from the HTML.
        We use this function for evaluation as well as unit testing.
        """

        for input in inputs:
            if input.type in ['text', 'textarea', 'select', 'password', 'email', 'number', 'tel', 'url',
                              'button', 'color', 'date', 'datetime-local', 'file', 'image', 'range', 'hidden']:

                values = self.driver.execute_script(
                    f"return Array.from(document.getElementsByName(`{input.name}`)).map((element) => element.value);"
                )

                # commenting out this asssrtion since there could be more than one text input with the same name.
                # an example of this can be seen in "Dialogue safety (socialchemistry) 5" task.
                # assert len(values) == 1, f"The number of values should be 1 but it is `{len(values)}` for {input}"

            elif input.type in ['radio']:
                values = self.driver.execute_script(
                    f"return Array.from(document.getElementsByName(`{input.name}`)).filter(element => element.checked).map(element => element.value);"
                )
                assert len(values) <= 1, f"The number of values should be 1 or 0 but it is `{len(values)}` for {input}"
            elif input.type in ['checkbox']:
                command = f"""return Array.from(document.getElementsByName(`{input.name}`)).filter(element => element.checked).map(element => element.value);"""
                values = self.driver.execute_script(command)
            else:
                raise Exception(f"{Fore.RED}to be implemented for type `{input.type}`")

            input.values = values

        return inputs

    @staticmethod
    # adapted the flowing from Squad v1.1 evaluation, without removing the articles.
    def normalize_answer(s):
        """Lower text and remove punctuation, and extra whitespace."""

        def white_space_fix(text):
            return ' '.join(text.split())

        def remove_punc(text):
            exclude = set(string.punctuation)
            return ''.join(ch for ch in text if ch not in exclude)

        def lower(text):
            return text.lower()

        return white_space_fix(remove_punc(lower(s)))

    def exact_match(self, prediction, references, xlingual=False):
        return (Evaluation.normalize_answer(prediction) == Evaluation.normalize_answer(references))

    def rouge(self, prediction, ground_truth, xlingual=False):
        if prediction == ground_truth:
            return 1.0

        if xlingual:
            scorer = self.xlingual_rouge_scorer
        else:
            scorer = self.default_rouge_scorer
        scores = scorer.score(prediction=prediction, target=ground_truth)
        return scores["rougeL"].fmeasure

    @staticmethod
    def metric_max_over_ground_truths(metric_fn, prediction, ground_truths, xlingual=False):
        scores_for_ground_truths = []
        for ground_truth in ground_truths:
            score = metric_fn(prediction, ground_truth, xlingual=xlingual)
            scores_for_ground_truths.append(score)
        score = float(max(scores_for_ground_truths))
        print(f"{Fore.BLUE} --> scores: ", score)
        return score

    def retrieve_gold_labels(self, task_name: str, instance_index: int, input_names: List[str]):
        """
        Retrieve the gold labels for a given instance index and input names.
        :param task_name: the name of the task
        :param instance_index: the index of the instance in the batch file
        :param input_names: the names of the inputs
        :return: a dictionary of input names and their corresponding gold labels
        """
        print(f" --> Looking up gold labels from row index {instance_index} of `input.csv` (unique inputs). ", )
        df = pd.read_csv(f'../tasks/{task_name}/batch.csv')
        # Keep the columns that are not answers and then combine the rows that are the same to find the distinct inputs
        cols = [col for col in df.columns if not col.startswith("Answer.")]
        # TODO: This is not always good, in HTER - longer sentences case there are many duplicate tasks of same inputs but different outputs
        distinct_rows = df[cols].drop_duplicates()

        # TODO: Turn off this assert while developing since this prohibits non-uniform editing of batch.csv for files that have duplicate inputs but different outputs
        # ensure that the number of unique tasks is exactly the same as the number of tasks in the batch
        assert len(distinct_rows) == len(
            self.task_ids[task_name]), f"The number of unique tasks {len(distinct_rows)} is " \
                                       f"not the same as the number of tasks in the batch: " \
                                       f"{len(self.task_ids[task_name])}."

        assert instance_index <= len(
            distinct_rows), f"The instance index {instance_index} is out of range: {len(distinct_rows)}."

        # select the row corresponding to instance_index
        row = distinct_rows.iloc[instance_index]
        # in the original dataframe "df", select all the rows that correspond to the selected "row"
        # and then select the columns that start with "Answer."
        df_subset = df[df[cols].eq(row).all(1)]
        answers_map = {
            input_name: df_subset.get(f"Answer.{input_name}", np.array([])).tolist() for input_name in input_names
        }

        # Note: we explicitly do not exclude "nan" values (empty cells) because sometimes the correct action is to leave
        # the field empty. For example, not selecting a checkbox or leaving a text box empty. Of course there are also
        # scenarios where this is not correct (hence, some "noise" in the evaluation).
        # return [a for a in answers.tolist() if not (type(a) == float and np.isnan(a))]
        return answers_map

    def calculate_rouge(self, answers: List[str], input_type: str, baseline_answer: str):
        baseline_answer = str(baseline_answer)
        # print(f"answers: `{answers}`")
        print(f"baseline_answer: `{baseline_answer}` - type: `{type(baseline_answer)}`")

        # normalize responses: turn "nan", or "{}" into empty string
        for idx in range(len(answers)):
            a = answers[idx]
            if a == "nan" or a == "{}" or a == "'{}'" or (type(a) == float and np.isnan(a)):
                answers[idx] = ""

        # print(f"answers after mapping: `{answers}`")

        # handle empty
        if answers == []:
            if baseline_answer == "" or baseline_answer == [
                ""] or baseline_answer == [] or baseline_answer == "[]" or baseline_answer == "['']":
                return 1.0
            else:
                return 0.0

        if input_type in ['text', 'textarea', 'hidden']:
            scores = Evaluation.metric_max_over_ground_truths(
                self.rouge,
                prediction=baseline_answer,
                ground_truths=[str(answer) for answer in answers],
                xlingual=False
            )
            return scores
        elif input_type in ['radio', 'select']:
            # if the field type is radio button, then compute the majority vote among the options
            print("--> Computing the majority vote")
            votes = {}
            for answer in answers:
                if answer in votes:
                    votes[answer] += 1
                else:
                    votes[answer] = 1
            if votes:
                majority_answer = max(votes, key=votes.get)
                majority_answer_str = str(majority_answer)

                scores = Evaluation.metric_max_over_ground_truths(
                    self.exact_match,
                    prediction=majority_answer_str,
                    ground_truths=[majority_answer_str],
                    xlingual=False
                )

                return scores
            else:
                return 0.0
        elif input_type in ['checkbox']:
            print("baseline", baseline_answer, "answers:", answers)
            scores = Evaluation.metric_max_over_ground_truths(
                self.exact_match,
                prediction=baseline_answer,
                ground_truths=[str(answer) for answer in answers],
                xlingual=False
            )
            return scores
        elif input_type in ['range']:
            # if the gold labels are numericals, then we can compute the mean absolute error
            # else, fall back to rouge
            try:
                # TODO: range values need to be normalized by their maximum
                # https://github.com/JHU-CLSP/turk-instructions/issues/65
                answers = [float(answer) for answer in answers]
                baseline_answer = float(baseline_answer)
                # "min" since we're happy as long as we're close to one human
                denominator = np.max(answers)
                scores = 1 - np.min(np.abs(np.array(answers) - baseline_answer)) / denominator
                print(f"{Fore.BLUE} --> using numeric values of the range to compute their error: {scores}")
                return scores
            except:
                scores = Evaluation.metric_max_over_ground_truths(
                    self.exact_match,
                    prediction=baseline_answer,
                    ground_truths=[str(answer) for answer in answers],
                    xlingual=False
                )
                return scores
        else:
            raise Exception(f"{Fore.RED}to be implemented for type `{input_type}`")

    @staticmethod
    def read_config(file):
        config = configparser.ConfigParser()
        config.read(file)
        return config

    def enumerate_tasks(self, max_instance_count: int):
        """
        Enumerate the tasks and their instances
        :param max_instance_count: maximum number of instances per task
        """
        input_format = "both"

        tasks = self.load_task_names()
        results = {}
        self.driver.get(TURKLE_URL)
        aggregate_field_statistics = {}  # We store the stats related to the field types/frequency here
        task_field_statistics = {}
        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")

            if task_name in [
                "Style adaptation, pairwise, complex-simple",
                "Spanish Word Alignment",
                "BiSECT Human Evaluation II (2)",
                "NER - Task scruples 26,200 - 30,922",
                "neural-pop (PLAN evaluation) t5-human-test b",
                "Commongen Evals (RLUE) 2",
                "Opinion Mining of Spanish Customer Comments HIT2",
                "ESNLI Rationale Generation 4",
                "COMET2020 ATOMIC Inference Vp 5",
                "Step 2 Verifying Multi-sentence-ness for questions 14",
                "Lattice",
                "wikiHow step-goal linking pilot cleanse-url",
                "mars human eval (a-b testing) 3",
                "Annotation subj_obj",
                "Email Formality Annotation",
                "Photo Collection GVDB",
                "Scalar Adjective Ordering",
                "Rationale Generation 5",
                "ATOMIC - Required Objects 5",
                "Arch - Rel Eval 3",
                "VQA Rationale Generation 5",
                "wikiHow Step Membership",
                "JJ-NN HIT",
                "Commonsense Morality - Text Label Validate-Collect 17",
                "HTER - 27 Sep 1859",
                "Gun violence structured extraction",
                "Summarization (RLUE) 1",
                "Explanation Acceptability (CommonsenseQA)",
                "Sentence Formality Annotation",
                "Congressional Bills 5 point" ,
                "Passive voice Parents 1st-2nd Person Persuasiveness Comparison",
                "BiSECT Multilingual Evaluation",
                "Commonsense Misinformation Tracking Pilot [cancer data setup] 10"
            ]:
                continue


            # TODO we gotta drop this after adding gold labels to the sandbox tasks
            if 'sandbox' in task_name:
                continue

            if "HTER - longer sentences -27 Sep 1129" in task_name:
                # https://github.com/JHU-CLSP/turk-instructions/issues/66
                continue

            if "Simplicity HIT - rank simplicity" in task_name or "Goal Distractor - ATOMIC base events 1" in task_name or "ATOMIC - Required Objects (Sequence) 9" in task_name:
                # flaky only fails in certain tasks like the very first one
                continue

            if "wikiHow Goal Membership" in task_name:
                # the inputs are not loaded properly
                # I think it's becuase the batch file has ".on" in the header
                continue

            if "Human evaluation - quals" in task_name:
                # inputs are not loaded properly
                # I think it's because we don't have the right batch file, though I might be wrong.
                continue

            if task_name not in self.task_ids.keys():
                print(f"{Fore.RED}Task `{task_name}` is not available on Turkle.")
                print("Available tasks are:", self.task_ids.keys())
                continue

            if "Dialogue safety (socialchemistry) 5" in task_name:
                # we're not able to execute some of the text inputs.
                # the page has multiple rationale inputs with the same name so it is not clear how to fill them in.
                # I think the only feasible fix is to merge the 3 text areas with the different names into one.
                continue

            if "Commonsense Morality-Text Label Validate-Collect-Extended" in task_name:
                # one of the text boxes is not filled in properly (it's empty)
                continue

            if "What breaks the flow - no categories 4" in task_name:
                # the oracle is not able to fully solve this task
                continue

            if "ROT Details [m=50] rocstories - 0 - 99" in task_name:
                # the oracle is not able to fully solve this task
                continue

            if "Annotate WaNLI 23" in task_name:
                # the oracle is not able to fully solve this task
                continue

            if "Reddit In-group Analysis Comment annotation 3" in task_name:
                # we don't find the right inputs
                continue

            if "Chatbot Response Quality Evaluation" in task_name:
                # I haven't checked any task after this.
                continue

            instance_ids = self.task_ids[task_name]
            first_instance_id = min(instance_ids)
            print("First instance id:", first_instance_id)

            # if maximum is less than the number of instances, we sample a random subset of instances
            if max_instance_count < len(instance_ids):
                # random sample
                instance_ids = random.sample(instance_ids, max_instance_count)

            # Sample random instances of each task
            for instance_id in instance_ids:

                # wait for a keyboard press before continuing
                # input("Press Enter to continue...")

                row_number = instance_id - first_instance_id
                print(f"instance_id: {instance_id} <-> row_number: {row_number}")

                url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                self.driver.get(url)

                # get the name of the fields
                df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                input_names = [col.replace('Answer.', '') for col in df.columns if col.startswith('Answer.')]
                inputs = self.extract_input_values_from_url(url=url, task_name=task_name, input_names=input_names)

                print(" --> inputs: {}".format([x.name for x in inputs]))

                answers_map = self.retrieve_gold_labels(
                    task_name, row_number, [x.name for x in inputs]
                )

                logging.info(" --> input labels: {}".format(answers_map))

                # TODO: check if all the files (images, videos, audio, css, etc.) in the HTML are accessible
                # TODO: find all the URLS in the HTML and check if they are accessible

                if self.dump_features:
                    directory = f'features/{task_name}'
                    images_directory = f'{directory}/images'
                    html_directory = f'{directory}/HTML'

                    if os.path.exists(directory):
                        shutil.rmtree(directory)
                    os.makedirs(directory)

                    if not os.path.exists(html_directory):
                        os.makedirs(html_directory)

                # for counting overall statistics
                if self.report_field_stats:
                    if task_name not in task_field_statistics:
                        task_field_statistics[task_name] = {}

                    for i in inputs:
                        if i.type not in aggregate_field_statistics:
                            aggregate_field_statistics[i.type] = 0

                        aggregate_field_statistics[i.type] += 1

                        if i.type not in task_field_statistics[task_name]:
                            task_field_statistics[task_name][i.type] = 0
                        task_field_statistics[task_name][i.type] += 1

                if self.dump_features:
                    data_to_be_dumped = []

                for input_idx, i in enumerate(inputs):
                    print(f"{Fore.GREEN} - - - - - -  starting a new element: `{i}` - - - - - -  ")

                    # make sure that the element is visible
                    element = self.driver.find_element(By.NAME, i.name)
                    if not element.is_displayed() or element.size['width'] <= 0 or element.size['height'] <= 0:
                        print(f'{Fore.RED}Skipping element `{i.name}` since it is not visible.')
                        continue

                    if self.dump_features and i.type != 'hidden':
                        image_format = "bordered_div"  # the most reasonable option
                        # create directory if needed
                        if not os.path.exists(f'{images_directory}_{image_format}'):
                            os.makedirs(f'{images_directory}_{image_format}')
                        if image_format == 'full_page':
                            task_image = self.actions.take_page_screenshots().outcome
                        elif image_format == 'bordered_div':
                            task_image = self.actions.take_element_screenshot_with_border(i).outcome
                        else:
                            raise Exception(f"{Fore.RED}to be implemented for image format `{image_format}`")

                        if isinstance(task_image, list):
                            img_ids = []
                            for j, image in enumerate(task_image):
                                image_id = f'{instance_id}_{input_idx}_{i.name}_{j}.png'
                                image.save(f'{images_directory}_{image_format}/{image_id}')
                                img_ids.append(image_id)
                            image_id = img_ids
                        else:
                            image_id = f'{instance_id}_{input_idx}_{i.name}.png'
                            task_image.save(f'{images_directory}_{image_format}/{image_id}')

                        html_id = f'{instance_id}_{i.name}.html'
                        with open(f'{html_directory}/{html_id}', 'w') as f:
                            # note, we can't use "driver.page_source" since it would return the default source without any changes
                            # TODO: double-check that this HTML code indeed contains the latest changes
                            f.write(self.driver.execute_script("return document.documentElement.outerHTML;"))

                    # *after* we dump *input* features, we execute the action
                    if self.solver_type == 'oracle':
                        kwargs = {'answers': answers_map[i.name]}
                        oracle_action_sequence = self.solver.solve(i, **kwargs)
                    else:
                        self.solver.solve(i)

                    # *after* we execute the action, we dump the *output* features
                    if self.dump_features:
                        data_to_be_dumped.append({
                            'input_type': i.type,
                            'input_name': i.name,
                            'image_id': image_id,
                            'html_id': html_id,
                            'output': oracle_action_sequence
                        })

                # get the input values from the web page
                inputs_with_values = self.extract_values(inputs)

                # collecting field statistics
                if task_name not in results:
                    results[task_name] = {}

                # TODO: move this inside a evaluation function to keep here clean
                score = 0.0
                for i in inputs_with_values:
                    if i.name in self.excluded_input_names:
                        continue
                    # if checkmarks, sort the values alphabetically
                    if i.type == "checkbox":
                        i.values = "|".join(sorted(i.values))
                        for idx in range(len(answers_map[i.name])):
                            x = answers_map[i.name][idx]
                            if type(x) == str and "|" in x:
                                answers_map[i.name][idx] = "|".join(sorted(x.split("|")))
                    else:
                        if len(i.values) > 0:
                            i.values = i.values[0]
                        else:
                            i.values = ''
                    score_per_field = self.calculate_rouge(answers_map[i.name], i.type, i.values)

                    if i.type not in results[task_name]:
                        results[task_name][i.type] = []

                    results[task_name][i.type].append(score_per_field)

                    score += score_per_field

                score /= len(inputs_with_values)
                print(f"{Fore.CYAN} --> Overall score: {score}")

                if self.solver_type == 'oracle':
                    assert score > 0.99, f"{Fore.RED}The oracle baseline should always get a score of 1.0"

                if self.dump_features:
                    with open(f'{directory}/{task_name}.json', 'w') as f:
                        json.dump(data_to_be_dumped, f, indent=4)

                df = pd.DataFrame()
                for task_name, inputs in results.items():
                    for input_type, scores in inputs.items():
                        # print(scores)
                        avg_score = sum(scores) / len(scores)
                        # TODO: check if we can safely change the "projects" in the following lines to tasks
                        df = pd.concat(
                            [
                                df, pd.DataFrame({
                                'project': [task_name],
                                'input_type': [input_type],
                                'score': [avg_score]
                            })
                            ],
                            ignore_index=True)

                if 'project' not in df.columns:
                    df.insert(0, 'project', '')
                if 'input_type' not in df.columns:
                    df.insert(1, 'input_type', '')
                if 'score' not in df.columns:
                    df.insert(1, 'score', '')

                df = df.pivot(index='project', columns='input_type', values='score')
                df.to_csv('oracle_baseline_scores.csv', index=True)

        # Close the driver
        self.driver.quit()

        print("Now let's print the field statistics")

        # save task_field_statistics (hashmap of hashmaps mapped to integers) as a csv file
        # first turn this hashmap into data frame
        # then save it as a csv file
        results = pd.DataFrame.from_dict(task_field_statistics)
        results.to_csv('task_field_statistics.csv', index=True)

        print("----------------------------------------------")
        print(f'Number of tasks: {len(task_field_statistics.keys())}')
        print("----------------------------------------------")
        print(f'Number of fields: {len(aggregate_field_statistics.keys())}')
        print("----------------------------------------------")
        print(f'Overall field statistics: {aggregate_field_statistics}')
        print("----------------------------------------------")
        print(f'Field statistics per task: {task_field_statistics}')


if __name__ == "__main__":
    # user argparser to recive he input parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver_type", help="random or oracle", default="random")
    parser.add_argument("--tasks", help="train, test, or subjective_test", default="test")
    parser.add_argument("--max_instance_count", help="maximum number of instances per task", default=1)
    parser.add_argument("--do_eval", help="whether to compute the quality aginst the gold data", default=True)
    parser.add_argument("--dump_features", help="whether to dump the features", default=False)
    parser.add_argument("--report_field_stats", help="whether to collect statistics for the HTML fields", default=True)

    args = parser.parse_args()
    print(f"{Fore.BLUE}Solver: {args.solver_type}")
    max_instance_count = int(args.max_instance_count)

    do_eval = args.do_eval
    dump_features = args.dump_features
    report_field_stats = args.report_field_stats
    assert type(do_eval) == bool

    if dump_features and not args.solver_type != "oracle":
        raise Exception(f"{Fore.RED}dump_features can only be used with oracle solver")

    eval = Evaluation(solver_type=args.solver_type, tasks=args.tasks,
                      do_eval=do_eval, dump_features=dump_features, report_field_stats=report_field_stats)

    # input_format = config.get('DEFAULT', 'input_format')
    # image_format = config.get('DEFAULT', 'image_format', fallback='full_page')
    eval.enumerate_tasks(max_instance_count)
