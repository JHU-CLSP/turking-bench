import argparse
from bs4 import BeautifulSoup
from colorama import init as colorama_init
from colorama import Fore
import configparser
from evaluation.actions import MyActions
from evaluation.input import Input
from evaluation import baselines
import json
import os
import pandas as pd
import random
import requests
from rouge_score import rouge_scorer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import string
from transformers import AutoTokenizer
from tqdm import tqdm
from typing import List
import numpy as np

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

    def create_driver(self):
        # TODO: make the seleciton of headless (no visual browser for faster processing) a parameter
        options = Options()
        options.headless = True

        import platform
        if platform.system() == 'Linux':
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

    @staticmethod
    def extract_input_values_from_url(url, task_name, input_names=None) -> List[Input]:
        """
        This utility function extracts the list of input fields that could be filled in.
        Then for each input field, it identifies their type (text area, checkbox, etc.)
        :param url: the url to extract the input fields from
        :param input_names: a list of input names to extract
        :return: a list of input names and their types
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        input_fields = []

        # if a list of input names are provided in the input, then extract the input fields with those names
        # otherwise, look for inputs that may look like input fields
        if input_names:
            input_names = set(input_names)
            inputs = []
            for name in input_names:
                input = soup.find(attrs={'name': name})
                if input and input.name in ['input', 'select', 'textarea']:
                    inputs.append(input)
        else:
            inputs = soup.find_all(['input', 'textarea', 'select'])

        # exclude special inputs
        exclude_input_names = [
            'csrfmiddlewaretoken',  # hidden field automatically added external css files
            'worker_ip'  # hidden field for bookkeeping
        ]
        inputs = [input for input in inputs if input.get('name') not in exclude_input_names]

        # make sure "names" are unique. Convert to set and back to list
        inputs = list(set(inputs))

        # now for our list of inputs, indentify their types
        for input in inputs:
            if input.name in ['input']:
                input_type = input.get('type')
                if not input_type:
                    input_type = 'text'
            elif input.name == 'textarea':
                input_type = 'textarea'
            elif input.name == 'select':
                input_type = 'select'
            else:
                continue

            input_name = input.get('name')
            if not input_name:
                continue

            input_fields.append(
                Input(url=url, input_name=input_name, input_type=input_type, task_name=task_name)
            )

        # before returning them, sort the input values based on their position in the HTML
        return sorted(
            input_fields,
            key=lambda x: str(soup).index(str(soup.find(attrs={'name': x.name})))
        )

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
        if xlingual:
            scorer = self.xlingual_rouge_scorer
        else:
            scorer = self.default_rouge_scorer
        scores = scorer.score(prediction=prediction, target=ground_truth)
        return scores["rougeL"].fmeasure

    @staticmethod
    def metric_max_over_ground_truths(metric_fn, prediction, ground_truths, xlingual=False):
        print(" --> inside rouge  ")
        print(f"predictions: {prediction}")
        print(f"ground_truths: {ground_truths}")

        scores_for_ground_truths = []
        for ground_truth in ground_truths:
            score = metric_fn(prediction, ground_truth, xlingual=xlingual)
            scores_for_ground_truths.append(score)
        score = max(scores_for_ground_truths)
        print("scores: ", score)
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
        distinct_rows = df[cols].drop_duplicates()

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
        answers_map = {input_name: df_subset.get(f"Answer.{input_name}", np.array([])).tolist() for input_name in
                       input_names}

        # Note: we explicitly do not exclude "nan" values (empty cells) because sometimes the correct action is to leave
        # the field empty. For example, not selecting a checkbox or leaving a text box empty. Of course there are also
        # scenarios where this is not correct (hence, some "noise" in the evaluation).
        # return [a for a in answers.tolist() if not (type(a) == float and np.isnan(a))]
        return answers_map

    def calculate_rouge(self, answers: List[str], input_type: str, baseline_answer: str):
        baseline_answer = str(baseline_answer)
        print("answers", answers)
        print("baseline_answer", baseline_answer)

        if input_type in ['text', 'textarea']:
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
            scores = Evaluation.metric_max_over_ground_truths(
                self.exact_match,
                prediction=baseline_answer,
                ground_truths=[str(answer) for answer in answers],
                xlingual=False
            )
            return scores
        else:
            raise Exception(f"{Fore.RED}to be implemented")

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

        # TODO: make these parameters
        input_format = "both"
        image_format = "full_page"

        tasks = self.load_task_names()

        results = {}
        self.driver.get(TURKLE_URL)
        aggregate_field_statistics = {}  # We store the stats related to the field types/frequency here
        task_field_statistics = {}
        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")

            # TODO we gotta drop this after adding gold labels to the sandbox tasks
            if 'sandbox' in task_name:
                continue

            if task_name not in self.task_ids.keys():
                print(f"{Fore.RED}Task `{task_name}` is not available on Turkle.")
                print("Available tasks are:", self.task_ids.keys())
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

                input("Press Enter to continue...")

                row_number = instance_id - first_instance_id
                print(f"instance_id: {instance_id} <-> row_number: {row_number}")

                url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                self.driver.get(url)

                # get the name of the fields
                df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                input_names = [col.replace('Answer.', '') for col in df.columns if col.startswith('Answer.')]
                inputs = Evaluation.extract_input_values_from_url(url, input_names)

                print(" --> inputs: {}".format([x.name for x in inputs]))

                answers_map = self.retrieve_gold_labels(
                    task_name, row_number, [x.name for x in inputs]
                )

                print(" --> input labels: {}".format(answers_map))

                # TODO: check if all the files (images, videos, audio, css, etc.) in the HTML are accessible
                # TODO: find all the URLS in the HTML and check if they are accessible

                if self.dump_features:
                    directory = f'features/{task_name}'
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    images_directory = f'{directory}/images'
                    if not os.path.exists(images_directory):
                        os.makedirs(images_directory)

                    html_directory = f'{directory}/HTML'
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
                    data = []

                for i in inputs:
                    element = self.driver.find_element(By.NAME, i.name)
                    # make sure that the element is visible
                    print(f"{Fore.GREEN} - - - - - -  starting a new element: `{i}` - - - - - -  ")

                    if not element.is_displayed() or element.size['width'] <= 0 or element.size['height'] <= 0:
                        print(f'{Fore.RED}Skipping element `{i.name}` since it is not visible.')
                        continue

                    if self.solver_type == 'oracle':
                        kwargs = {'answers': answers_map[i.name]}
                        baseline_answer = self.solver.solve(i, **kwargs)
                    else:
                        baseline_answer = self.solver.solve(i)

                    if self.dump_features:
                        if input_format == 'image' or 'both':
                            if image_format == 'full_page':
                                task_image = self.actions.take_page_screenshots()
                            elif image_format == 'div':
                                task_image = self.actions.take_element_screenshot(i)
                            elif image_format == 'bordered_div':
                                task_image = self.actions.take_element_screenshot_with_border(i)
                            else:
                                raise Exception(f"{Fore.RED}Invalid image format: {image_format}")

                        if i.type != 'hidden':
                            if input_format == 'image' or 'both':
                                if image_format == 'full_page':
                                    task_image = self.actions.take_page_screenshots()
                                elif image_format == 'div':
                                    task_image = self.actions.take_element_screenshot(i)
                                elif image_format == 'bordered_div':
                                    task_image = self.actions.take_element_screenshot_with_border(i)

                                if isinstance(task_image, list):
                                    img_ids = []
                                    for j, image in enumerate(task_image):
                                        image_id = f'{instance_id}_{i.name}_{j}.png'
                                        image.save(f'{images_directory}/{image_id}')
                                        img_ids.append(image_id)
                                    image_id = img_ids
                                else:
                                    image_id = f'{instance_id}_{i.name}.png'
                                    task_image.save(f'{images_directory}/{image_id}')
                            else:
                                image_id = None

                            html_id = f'{instance_id}_{i.name}.html'
                            with open(f'{html_directory}/{html_id}', 'w') as f:
                                f.write(self.driver.page_source)

                            gold_output = "tbd"
                            self.actions.execute_command(i, baseline_answer)

                            data.append({
                                'input_type': i.type,
                                'input_name': i.name,
                                'image_id': image_id,
                                'html_id': html_id,
                                'output': gold_output
                            })


                    # TODO: scoring should be done after all the annotations are done
                    # score = self.calculate_rouge(answers_map[input.name], input.type, baseline_answer)
                    score = 0.0

                    # collecting field statistics
                    if task_name not in results:
                        results[task_name] = {}

                    if i.type not in results[task_name]:
                        results[task_name][i.type] = []
                    results[task_name][i.type].append(score)

                if self.dump_features:
                    with open(f'{directory}/{task_name}.json', 'w') as f:
                        json.dump(data, f)

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
    print(f"{Fore.BLUE}Solver: {args.solver}")
    max_instance_count = int(args.max_instance_count)

    do_eval = args['do_eval']
    dump_features = args['dump_features']
    report_field_stats = args['report_field_stats']
    assert type(do_eval) == bool

    eval = Evaluation(solver_type=args.solver_type, tasks=args.tasks,
                      do_eval=do_eval, dump_features=dump_features, report_field_stats=report_field_stats)

    # input_format = config.get('DEFAULT', 'input_format')
    # image_format = config.get('DEFAULT', 'image_format', fallback='full_page')
    eval.enumerate_tasks(max_instance_count)
