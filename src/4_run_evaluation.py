import argparse
from colorama import init as colorama_init
from colorama import Fore, Back, Style
import configparser
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
from evaluation.actions import MyActions
from evaluation.input import Input
from evaluation.baselines import Baseline

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
    def __init__(self):
        self.default_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        self.xlingual_tokenizer = GPTTokenizer()
        self.xlingual_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], tokenizer=self.xlingual_tokenizer)
        self.driver = self.create_driver()
        self.actions = MyActions(self.driver)

    # as soon as the code is loaded, we look for alignnent between the task names and their ids
    task_ids = requests.get(f"{TURKLE_URL}/get_tasks/").json()

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

    def load_task_names(setup: str):
        """
        This function returns the list of tasks for a given setup.
        """

        # load all tasks
        all_tasks = os.listdir("../tasks")

        if setup == 'all':
            return all_tasks
        else:
            with open('../data/splits/evaluation_tasks.txt', 'r') as f:
                test = f.read().splitlines()

            with open('../data/splits/subjective_evaluation_tasks.txt', 'r') as f:
                subjective_test = f.read().splitlines()

            # make sure that the splits are exclusive
            assert len(set(test).intersection(set(subjective_test))) == 0, f"{Fore.RED}The test and subjective test " \
                                                                           f"splits are not exclusive\n: test: {test}\nsubjective_test: {subjective_test}"

            if setup == 'test':
                return test
            elif setup == 'subjective_test':
                return subjective_test
            elif setup == 'train':
                # all tasks minue test and subjective test
                return list(set(all_tasks) - set(test) - set(subjective_test))
            else:
                raise Exception(f"{Fore.RED}Invalid setup: {setup}")

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

    @staticmethod
    def retrieve_gold_labels(task_name: str, instance_index: int, input_names: List[str]):
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
            Evaluation.task_ids[task_name]), f"The number of unique tasks {len(distinct_rows)} is " \
                                             f"not the same as the number of tasks in the batch: " \
                                             f"{len(Evaluation.task_ids[task_name])}."

        assert instance_index <= len(
            distinct_rows), f"The instance index {instance_index} is out of range: {len(distinct_rows)}."

        # select the row corresponding to instance_index
        row = distinct_rows.iloc[instance_index]
        # in the original dataframe "df", select all the rows that correspond to the selected "row"
        # and then select the columns that start with "Answer."
        df_subset = df[df[cols].eq(row).all(1)]
        answers_map = {input_name: df_subset[f"Answer.{input_name}"].tolist() for input_name in input_names}

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

    def enumerate_tasks(self, tasks: List[str], batch: bool, maximum: int, mode: str, input_format: str, image_format: str):
        """
        Enumerate the tasks and their instances
        :param tasks: list of tasks
        :param batch: batch size TODO: what is this?
        :param maximum: maximum number of instances per task
        :param mode: train or test
        :param input_format: text or image. This matters for "training" mode, where we need to save the inputs on disk.
        """


        results = {}
        self.driver.get(TURKLE_URL)
        aggregate_field_statistics = {}  # We store the stats related to the field types/frequency here
        task_field_statistics = {}
        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")
            # TODO we gotta drop this after adding gold labels to the sandbox tasks
            if 'sandbox' in task_name:
                continue
            if task_name not in Evaluation.task_ids.keys():
                print(f"{Fore.RED}Task `{task_name}` is not available on Turkle.")
                print("Available tasks are:", Evaluation.task_ids.keys())
                continue
            instance_ids = Evaluation.task_ids[task_name]
            first_instance_id = min(instance_ids)
            print("First instance id:", first_instance_id)

            # if maximum is less than the number of instances, we sample a random subset of instances
            if maximum < len(instance_ids):
                # random sample
                instance_ids = random.sample(instance_ids, maximum)

            # instance_ids = [27809]
            data = []

            # TODO: what is the purpose of this vs. test mode?
            if mode == 'train':
                directory = f'train/{task_name}'
                if not os.path.exists(directory):
                    os.makedirs(directory)

                images_directory = f'{directory}/images'
                if not os.path.exists(images_directory):
                    os.makedirs(images_directory)

                html_directory = f'{directory}/HTML'
                if not os.path.exists(html_directory):
                    os.makedirs(html_directory)

                # Sample random instances of each task
                for instance_id in instance_ids:
                    url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                    driver.get(url)

                    # TODO: check if all the files (images, videos, audio, css, etc.) in the HTML are accessible
                    # TODO: find all the URLS in the HTML and check if they are accessible

                    # evaluation = Evaluation(driver)
                    if batch:
                        df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                        input_names = [col.replace('Answer.', '') for col in df.columns if col.startswith('Answer.')]
                        inputs = Input.extract_input_values_from_url(url, input_names)
                    else:
                        inputs = Input.extract_input_values_from_url(url)

                    for input in inputs:
                        if input['input_type'] != 'hidden':
                            task = Input(url, input['input_name'])

                            if input_format == 'image' or 'both':
                                if image_format == 'full_page':
                                    task_image = Input.get_page_screenshots(driver)
                                elif image_format == 'div':
                                    task_image = Input.get_element_screenshot(driver, input['input_name'],
                                                                              input['input_type'])
                                elif image_format == 'bordered_div':
                                    task_image = Input.get_element_screenshot_with_border(driver, input['input_name'],
                                                                                          input['input_type'])

                                if isinstance(task_image, list):
                                    img_ids = []
                                    for j, image in enumerate(task_image):
                                        image_id = f'{instance_id}_{input["input_name"]}_{j}.png'
                                        image.save(f'{images_directory}/{image_id}')
                                        img_ids.append(image_id)
                                    image_id = img_ids
                                else:
                                    image_id = f'{instance_id}_{input["input_name"]}.png'
                                    task_image.save(f'{images_directory}/{image_id}')
                            else:
                                image_id = None

                            html_id = f'{instance_id}_{input["input_name"]}.html'
                            with open(f'{html_directory}/{html_id}', 'w') as f:
                                f.write(driver.page_source)

                            row_number = instance_id - first_instance_id
                            baseline_answer = Baseline.oracle_baseline(
                                task_name, row_number, input['input_name']
                            )
                            actions.execute_command(input['input_type'], baseline_answer, input['input_name'])

                            data.append({
                                'input': [input['input_type'], input['input_name']],
                                'image_id': image_id,
                                'html_id': html_id,
                                'output': baseline_answer
                            })

                with open(f'{directory}/{task_name}.json', 'w') as f:
                    json.dump(data, f)

            if mode == 'test':
                # Sample random instances of each task
                for instance_id in instance_ids:
                    row_number = instance_id - first_instance_id
                    print(f"instance_id: {instance_id} <-> row_number: {row_number}")

                    url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                    driver.get(url)
                    evaluation = Evaluation()
                    if batch:  # TODO: better name? Batch here means that we use the field names from HTML file. Other names: Oracle, known fields, etc.
                        df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                        input_names = [col.replace('Answer.', '') for col in df.columns if col.startswith('Answer.')]
                        inputs = Input.extract_input_values_from_url(url, input_names)
                    else:
                        inputs = Input.extract_input_values_from_url(url)

                    print(" --> inputs: {}".format(inputs))

                    answers_map = Evaluation.retrieve_gold_labels(
                        task_name, row_number, [i['input_name'] for i in inputs]
                    )

                    print(" --> input labels: {}".format(answers_map))

                    # for counting overall statistics
                    if True:
                        if task_name not in task_field_statistics:
                            task_field_statistics[task_name] = {}

                        for i in inputs:
                            type = i['input_type']

                            if type not in aggregate_field_statistics:
                                aggregate_field_statistics[type] = 0

                            aggregate_field_statistics[type] += 1

                            if type not in task_field_statistics[task_name]:
                                task_field_statistics[task_name][type] = 0
                            task_field_statistics[task_name][type] += 1

                        continue

                    for input in inputs:
                        element = driver.find_element(By.NAME, input['input_name'])
                        # make sure that the element is visible
                        print(
                            f"{Fore.GREEN} - - - - - - - - - - - -  starting a new element: `{input}` - - - - - - - - - - - -  ")
                        if element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0:
                            task = Input(url, input['input_name'])
                            # baseline_answer = Baseline.solve_task(task, driver)
                            # baseline_answer = Baseline.random_baseline(i['input_name'], i['input_type'], driver)

                            baseline_answer = Baseline.oracle_baseline(
                                task_name,
                                row_number,
                                input['input_name']
                            )
                            actions.execute_command(
                                input['input_type'],
                                baseline_answer,
                                input['input_name']
                            )
                            score = evaluation.calculate_rouge(
                                answers_map[input['input_name']],
                                input['input_type'],
                                baseline_answer
                            )
                            if task_name not in results:
                                results[task_name] = {}
                            if input['input_type'] not in results[task_name]:
                                results[task_name][input['input_type']] = []
                            results[task_name][input['input_type']].append(score)
                        else:
                            print(f'{Fore.RED}Skipping element {input["input_name"]} since it is not visible.')

                df = pd.DataFrame()
                for task_name, inputs in results.items():
                    for input_type, scores in inputs.items():
                        print(scores)
                        avg_score = sum(scores) / len(scores)
                        # TODO: check if we can safely change the "projects" in the following lines to tasks
                        df = pd.concat(
                            [df,
                             pd.DataFrame({'project': [task_name], 'input_type': [input_type], 'score': [avg_score]})],
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
        driver.quit()

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
    eval = Evaluation()
    tasks = eval.load_task_names(setup='all')  # TODO: receive setup from input
    config = eval.read_config('config.ini')
    batch = config.getboolean('DEFAULT', 'batch')  # TODO: what is this?
    max_instance_count = config.getint('DEFAULT', 'num')
    mode = config.get('DEFAULT', 'mode')
    input_format = config.get('DEFAULT', 'input_format')
    image_format = config.get('DEFAULT', 'image_format', fallback='full_page')
    eval.enumerate_tasks(tasks, batch, max_instance_count, mode, input_format, image_format)
