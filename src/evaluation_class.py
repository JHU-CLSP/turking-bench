from colorama import init as colorama_init
from colorama import Fore
import configparser
from evaluation.actions import MyActions
from evaluation.input import Input
from evaluation import baselines
import html
import json
import os
from pathlib import Path
import pandas as pd
import numpy as np
import platform
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
from typing import List, Union
import logging
import bisect
import copy

TURKLE_URL = "http://localhost:8000"

colorama_init(autoreset=True)

def try_numeric(x: str) -> str:
    """Helper function to convert a string to float representation if possible."""
    try:
        float_value = float(x)
        int_value = int(float_value)
        if int_value == float_value:
            return str(int_value)
        else:
            return str(float_value)
    except:
        return x


def clean_values(values: List[str]) -> List[Union[str, int, float]]:
    """
    This function cleans the values by removing empty strings and "nan" values.
    """

    return [
        try_numeric(value) if value is not None else ''
        for value in values
    ]


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
    def __init__(self, solver_type: str, tasks: str, do_eval: bool, dump_features: bool, report_field_stats: bool, headless: bool = False):
        self.default_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        self.xlingual_tokenizer = GPTTokenizer()
        self.xlingual_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], tokenizer=self.xlingual_tokenizer)
        self.driver = self.create_driver(headless=headless)
        self.actions = MyActions(self.driver)
        self.solver = None
        # ass more solvers that we implement, we can add them here:
        self.solver_type = solver_type
        if solver_type == "random":
            self.solver = baselines.RandomBaseline(driver=self.driver, actions=self.actions)
        elif solver_type == "oracle":
            self.solver = baselines.OracleBaseline(driver=self.driver, actions=self.actions)
        elif solver_type == "model":
            self.solver = baselines.ModelBaseline(driver=self.driver, actions=self.actions)
        else:
            raise Exception(f"{Fore.RED}Solver `{solver_type}` not implemented")
        self.tasks = tasks
        assert tasks in ["test_easy", "test_hard", "train", "all", "subjective_test"] or tasks.startswith("tap") or tasks.startswith("dmp")

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

    def filter_TAP_tasks(self, task_name):
        if "sandbox" in task_name:
            return False

        if "COMET2020 ATOMIC Inference Vp 5" == task_name:
            # input.type submit hasn't been coded for thus self.extract_values is erroring
            return False

        show_questions_tasks = ["Rationale Generation 5", "Gun violence structured extraction", "ESNLI Rationale Generation 4", "JJ-NN HIT", 
                                "neural-pop (PLAN evaluation) t5-human-test b", "VQA Rationale Generation 5", "Lattice"]
        # skip these task since it requires an extra click to show the available questions or next ones
        if task_name in show_questions_tasks:
            return False

        # Has type hidden that we fail certain inputs on
        # But we pass a lot of these cases, lots of answers don't need the hidden input
        if task_name == "What breaks the flow - no categories 4":
            return False

        # Skip since there is a 15 second delay before showing the available questions
        if task_name == "Summarization (RLUE) 1":
            return False
        
        weird_input_formats = ["BiSECT Human Evaluation II (2)", "Spanish Word Alignment"]
        # Skip since these tasks have a weird input format the model cannot interact with
        if task_name in weird_input_formats:
            return False
        
        tasks_should_skip = ["Photo Collection GVDB", "NER - Task scruples 26,200 - 30,922"]
        # tasks I don't think the model is capable of solving
        if task_name in tasks_should_skip:
            return False

        # throwing Email Formality Annotation into the mix, seems like the answers r pretty unusable. questionably empty, floating in the abyss to the right of answers. tried some data processing but then realized it was just oof data. could maybe recover in future by looking at each answer to the right of the answers and sticking them inside Answer. if we want (that could be right, maybe same num of "missing ans" but also some X need answers that are found in Xsrc and junk is filled in X, so lots of work
        # same with Simplicity HIT - rank simplicity, the answers r unusable as well (full text strings for MOST of the responses when they should be numbers between 0 - 5, and weird numbs at the end
        weird_data_in_batch_csv = ["Simplicity HIT - rank simplicity", "Email Formality Annotation"]
        if task_name in weird_data_in_batch_csv:
            return False

        if task_name not in self.task_ids.keys():
            print(f"{Fore.RED}Task `{task_name}` is not available on Turkle.")
            print("Available tasks are:", self.task_ids.keys())
            return False

        return True

    def create_driver(self, headless: bool):
        options = Options()
        if headless:
            options.add_argument("--headless=new")

        import platform
        if platform.system() == 'Linux':
            driver = webdriver.Chrome(options=options)
        elif platform.system() == "Darwin":
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Firefox()

        return driver

    def load_split_tasks(self, partitions: int):
        """
        args: partitions: number of partitions to split the tasks into
        """
        # load all tasks into a list of strings
        all_tasks = os.listdir("../tasks")
        all_tasks = list(filter(self.filter_TAP_tasks, all_tasks))
        print("all_tasks len:", len(all_tasks))

        og_partitions = partitions
        split_tasks = []

        # Greedy optimized way to split evenly
        s = set() # was originally a set, but python sets aren't as robust as C++ std
        sum = 0
        for task in all_tasks:
            df = pd.read_csv(f'../tasks/{task}/batch.csv', nrows=0)
            input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
            val = min(1000, len(self.task_ids[task])) * (8 + len(input_names)) # num_tasks * num_inputs_per_task + 8 * num_tasks
            sum += val
            s.add((val, task)) # (val, task name)

        s = sorted(s)

        # allow for even distribution at end by taking out beginning and re-distributing
        last = len(s) - 1
        while s[last][0] > sum // partitions:
            split_tasks.append([s[last][1]])
            sum -= s[last][0]
            s.remove(s[last])
            partitions -= 1
            last -= 1

        for partition in range(partitions):
            curr = []
            goal = sum // partitions
            while goal > 0 and len(s) > 0:
                ind = min(bisect.bisect_right(s, (goal, "a")), len(s) - 1)
                curr.append(s[ind][1])
                goal -= s[ind][0]
                s.remove(s[ind])
            split_tasks.append(curr)

        split_sums = []
        for i in range(og_partitions):
            temp_sum = 0
            for task in split_tasks[i]:
                df = pd.read_csv(f'../tasks/{task}/batch.csv', nrows=0)
                input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
                val = min(1000, len(self.task_ids[task])) * (8 + len(input_names))
                temp_sum += val
            split_sums.append(temp_sum)

        print("split_sums:", split_sums)

        # Naive way to split up the tasks by evenly number per
        # num_per_partition = -(len(all_tasks) // -partitions) # ceil division
        # split_tasks = [all_tasks[i * num_per_partition : (i + 1) * num_per_partition] for i in range(partitions)]

        # Can optimize this with greedy and DP to minimize difference between largest and smallest partition
        # Start with # of instances * # tasks, then can go # inputs * # instances * # tasks

        ind = int(self.tasks[len("tap"):]) - 1

        if ind == 0:
            for i in range(og_partitions):
                print(f"partition: {i} | {split_tasks[i]}")

        print("this partition's tap tasks", split_tasks[ind])
        return split_tasks[ind]

    def load_task_names(self):
        """
        This function returns the list of tasks for a given setup.
        """

        # load all tasks
        all_tasks = os.listdir("../tasks")

        if self.tasks == 'all':
            return all_tasks
        else:
            with open('../data/splits/evaluation_tasks_easy.txt', 'r') as f:
                test = f.read().splitlines()

            with open('../data/splits/evaluation_tasks_hard.txt', 'r') as f:
                test_hard = f.read().splitlines()

            with open('../data/splits/subjective_evaluation_tasks.txt', 'r') as f:
                subjective_test = f.read().splitlines()

            # make sure that the splits are exclusive
            all_test_splits = [test, test_hard, subjective_test]
            for i, test1 in enumerate(all_test_splits):
                for j, test2 in enumerate(all_test_splits):
                    if i != j:
                        assert len(set(test1).intersection(set(test2))) == 0, f"{Fore.RED}The tests are not mutually exclusive" \
                                                                           f"splits are not exclusive\n: test1: {test1}\ntest2: {test2}" \
                                                                           f"\nintersection: {set(test1).intersection(set(test2))}"

            if self.tasks == 'test_easy':
                return test
            elif self.tasks == 'test_hard':
                return test_hard
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

        inputs = []
        # if a list of input names are provided in the input, then extract the input fields with those names
        # otherwise, look for inputs that may look like input fields
        if input_names:
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

        # instead changed the code base to just use the order in which the Answer columns are given. We can rearrange it to the order of which inputs to fill in first
        return input_fields
    
    def extract_values(self, inputs: List[Input]):
        """
        Given a set of values for the input fields, extract the values from the HTML.
        We use this function for evaluation as well as unit testing.
        """

        for input in inputs:
            if input.type in [
                    'text', 'textarea', 'select', 'password', 'email', 'number',
                    'tel', 'url', 'button', 'color', 'date', 'datetime-local',
                    'file', 'image', 'range', 'hidden'
            ]:

                values = self.driver.execute_script(
                    f"return Array.from(document.getElementsByName(`{input.name}`)).map((element) => element.value);"
                )

                if input.type in ['textarea']:
                    visible_values = self.driver.execute_script(
                        f"return Array.from(document.getElementsByName(`{input.name}`)).map((element) => element.innerHTML);"
                    )
                elif input.type == 'select':
                    visible_values = self.driver.execute_script(
                        f"return Array.from(document.getElementsByName(`{input.name}`)[0].children).filter((el) => el.selected == true).map((el) => el.value);"
                    )
                else:
                    visible_values = self.driver.execute_script(
                        f"return Array.from(document.getElementsByName(`{input.name}`)).map((element) => element.getAttribute('value'));"
                    )

                # commenting out this assertion since there could be more than one text input with the same name.
                # an example of this can be seen in "Dialogue safety (socialchemistry) 5" task.
                # assert len(values) == 1, f"The number of values should be 1 but it is `{len(values)}` for {input}"

            elif input.type in ['radio']:
                values = self.driver.execute_script(
                    f"return Array.from(document.querySelectorAll(`input[name='{input.name}']:checked`)).map(element => element.value);"
                )
                visible_values = self.driver.execute_script(
                    f"return Array.from(document.getElementsByName(`{input.name}`)).filter(element => element.checked).map(element => element.value);"
                )
                assert len(values) <= 1, f"The number of values should be 1 or 0 but it is `{len(values)}` for {input}"
                assert len(visible_values) <= 1, f"The number of visible values should be 1 or 0 but it is `{len(visible_values)}` for {input}"
            elif input.type in ['checkbox']:
                command = f"""return Array.from(document.querySelectorAll(`input[name='{input.name}']:checked`)).map(element => element.value);"""
                values = self.driver.execute_script(command)

                command = f"""return Array.from(document.getElementsByName(`{input.name}`)).filter(element => element.checked).map(element => element.value);"""
                visible_values = self.driver.execute_script(command)
            else:
                raise Exception(
                    f"{Fore.RED}To be implemented for type `{input.type}`")
            clean_visible_values = clean_values(visible_values)
            clean_visible_values = [
                html.unescape(v) for v in clean_visible_values
            ]

            input.values = clean_values(values)
            input.visible_values = clean_visible_values

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
        """
        Returns the max score comparing model predicted output to over the ground truth labels that we have received from the gold labels
        """
        prediction = try_numeric(prediction)
        scores_for_ground_truths = []
        ground_truths = clean_values(ground_truths)
        for ground_truth in ground_truths:
            score = metric_fn(prediction, ground_truth, xlingual=xlingual)
            scores_for_ground_truths.append(score)
        score = float(max(scores_for_ground_truths))
        print(f"prediction {prediction} ground_truths {ground_truths}")
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

        # TODO assert turn off while developing since this prohibits non-uniform editing of batch.csv for files that have duplicate inputs but different outputs
        # ensure that the number of unique tasks is exactly the same as the number of tasks in the batch
        assert len(distinct_rows) == len(
            self.task_ids[task_name]), f"The number of unique tasks {len(distinct_rows)} is " \
                                       f"not the same as the number of tasks in the batch: " \
                                       f"{len(self.task_ids[task_name])}."

        assert instance_index <= len(
            distinct_rows), f"The instance index {instance_index} is out of range: {len(distinct_rows)}."

        # select the row corresponding to instance_index
        row = distinct_rows.iloc[instance_index]
        # in the original df, go choose all the rows that have the same inputs as the selected row instance and return all of the answers
        # this will be a df with multiple rows iff there are multiple answers to the same question instance
        df_subset = df[df[cols].eq(row).all(1)]
        # create a map for each Answer (input_name) to its corresponding answers of the instance
        answers_map = {
            input_name: df_subset.get(f"Answer.{input_name}", np.array([])).tolist() for input_name in input_names
        }

        # Note Note: Should be careful with nan values since their equality is tricky in Python
        # Note: we explicitly do not exclude "nan" values (empty cells) because sometimes the correct action is to leave
        # the field empty. For example, not selecting a checkbox or leaving a text box empty. Of course there are also
        # scenarios where this is not correct (hence, some "noise" in the evaluation).
        # return [a for a in answers.tolist() if not (type(a) == float and np.isnan(a))]
        return answers_map

    def calculate_rouge(self, answers: List[str], input_type: str, baseline_answer: str):
        baseline_answer = str(baseline_answer)
        logging.info(f"answers: `{answers}`")
        logging.info(f"baseline_answer: `{baseline_answer}` - type: `{type(baseline_answer)}`")

        # normalize responses: turn "nan", or "{}" into empty string
        for idx in range(len(answers)):
            a = answers[idx]
            if a == "nan" or a == "{}" or a == "'{}'" or (type(a) == float and np.isnan(a)):
                answers[idx] = ""

        logging.info(f"answers after mapping: `{answers}`")

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
                scores = np.min(np.abs(np.array(answers) - baseline_answer))
                if denominator > 0:
                    scores /= denominator
                scores = 1 - scores
                print(f"{Fore.BLUE} --> using numeric values of the range to compute their error: {scores}")
                return scores
            except Exception:
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

    def get_relevant_html(self, input: Input):
        """
        This function returns an array of the the relevant HTML lines for a given input field.
        If you want it to be a string of HTML, just to_string this list concatenating one after another
        """

        print("input", input)
        target_element = self.driver.execute_script(f"return document.getElementsByName('{input.name}')[0].outerHTML")
        unfiltered_HTML = self.driver.execute_script(f"return document.getElementsByName('{input.name}')[0].parentElement.parentElement.outerHTML")
        HTML_arr = unfiltered_HTML.split(">")
        mid_idx = -1
        for idx, i in enumerate(HTML_arr):
            HTML_arr[idx] = i + ">"
            if HTML_arr[idx] == target_element:
                mid_idx = idx

        relevant_html = []
        upper_bound = 15;
        lower_bound = 30;
        for i in range(max(0, mid_idx - upper_bound), min(len(HTML_arr), mid_idx + lower_bound)):
            relevant_html.append(HTML_arr[i])

        return relevant_html

    def score_outputs(self, inputs: List[Input], task_name: str, row_number: int) -> float:
        """
        This function scores the outputs from a model for a given task and instance given the inputs the model should've answered
        """
        # get the input values from the web page
        model_outputs = self.extract_values(inputs)
        
        # get the right answers
        answers_map = self.retrieve_gold_labels(
            task_name, row_number, [x.name for x in inputs]
        )

        score = 0.0
        for i in model_outputs:
            if i.name in self.excluded_input_names:
                continue

            if i.values != i.visible_values:
                raise Exception(
                    f"The values `{i.values}` and visible values `{i.visible_values}` should be the same for `{i}`"
                )
            
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

            # the score for this specific model input/output
            score_per_field = self.calculate_rouge(answers_map[i.name], i.type, i.values)

            score += score_per_field

        score /= len(model_outputs) # average score for this instance
        print(f"{Fore.CYAN} --> Overall score: {score}")

        return score

    def enumerate_tasks(self, max_instance_count: int, **kwargs):
        """
        Enumerate the tasks and their instances
        :param max_instance_count: maximum number of instances per task
        """
        input_format = "both"

        if self.tasks.startswith("dmp"):
            tasks = self.load_split_tasks(kwargs.get("dump_partitions"))
        else:
            tasks = self.load_task_names()

        # Override the task of tasks if a specific task is specified
        if "task" in kwargs:
            tasks = [kwargs["task"]]
            print("tasks", tasks)
        results = {}
        aggregate_field_statistics = {}  # We store the stats related to the field types/frequency here
        task_field_statistics = {}
        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")

            if self.filter_TAP_tasks(task_name) == False:
                continue

            instance_ids = self.task_ids[task_name]
            first_instance_id = min(instance_ids)
            print("First instance id:", first_instance_id)

            # Create a random sample
            instance_ids = random.sample(instance_ids, min(max_instance_count, len(instance_ids)))

            if self.dump_features:
                directory = f'/scratch4/danielk/kxu39/turk_data/{task_name}'
                images_directory = f'{directory}/images'
                html_directory = f'{directory}/HTML'

                Path(directory).mkdir(parents=True, exist_ok=True)
                Path(html_directory).mkdir(parents=True, exist_ok=True)

                data_to_be_dumped = []
                curr_data_to_be_dumped = {}

            # Override instance_ids if specified the row_num
            if self.solver_type == "model":
                answer_map = {}
                instance_ids = []
                for key, value in kwargs["params"].items():
                    instance_id = first_instance_id + int(key)
                    instance_ids.append(instance_id)
                    answer_map[instance_id] = {}
                    for row in value:
                        print("row", row)
                        answer_map[instance_id][row["input_name"]] = row["action_sequence"]

            # Go through the instances of each task in this random sample
            print(f"len(instance_ids): {len(instance_ids)}")
            for instance_id in instance_ids:
                # wait for a keyboard press before continuing
                # input("Press Enter to continue...")

                row_number = instance_id - first_instance_id
                print(f"instance_id: {instance_id} <-> row_number: {row_number}")

                url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                self.driver.get(url)

                # get the name of the fields
                df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
                inputs = self.extract_input_values_from_url(url=url, task_name=task_name, input_names=input_names)

                print(" --> inputs: {}".format([x.name for x in inputs]))

                answers_map = self.retrieve_gold_labels(
                    task_name, row_number, [x.name for x in inputs]
                )

                logging.info(" --> input labels: {}".format(answers_map))

                # TODO: check if all the files (images, videos, audio, css, etc.) in the HTML are accessible
                # TODO: find all the URLS in the HTML and check if they are accessible

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
                    curr_data_to_be_dumped["task_name"] = task_name
                    curr_data_to_be_dumped["instance_id"] = instance_id
                    curr_data_to_be_dumped["row_num"] = row_number
                    curr_data_to_be_dumped["fields"] = []

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
                        Path(f"{images_directory}_{image_format}").mkdir(parents=True, exist_ok=True)
                        if image_format == 'full_page':
                            task_image = self.actions.take_page_screenshots().outcome
                        elif image_format == 'bordered_div':
                            task_image = self.actions.take_element_screenshot_with_border(i.name).outcome
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
                    elif self.solver_type == 'model':
                        self.solver.solve(i, output = answer_map[instance_id][i.name])
                    else:
                        self.solver.solve(i)

                    # *after* we execute the action, we dump the *output* features
                    if self.dump_features:
                        curr_data_to_be_dumped["fields"].append({
                            'input_type': i.type,
                            'input_name': i.name,
                            'image_id': image_id,
                            'html_id': html_id,
                            'relevant_html': self.get_relevant_html(i),
                            'output': oracle_action_sequence
                        })

                if self.dump_features:
                    data_to_be_dumped.append(copy.deepcopy(curr_data_to_be_dumped))

                # get the input values from the web page
                inputs_with_values = self.extract_values(inputs)

                # collecting field statistics
                if task_name not in results:
                    results[task_name] = {}

                # TODO: use my score_outputs function
                score = 0.0
                for i in inputs_with_values:
                    if i.name in self.excluded_input_names:
                        continue

                    if i.values != i.visible_values:
                        error_flag = True
                        print(
                            f"{Fore.RED}The values `{i.values}` and visible values `{i.visible_values}` should be the same for `{i}`"
                        )

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
                elif self.solver_type == 'model':
                    kwargs["scores"].append(score)

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

        if self.dump_features:
            with open(f'{directory}/{task_name}.json', 'w') as f:
                json.dump(data_to_be_dumped, f, indent=4)

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

    def enumerate_tap_tasks(self, max_instance_count: int):
        """
        Enumerate all the tasks comprehensively, so going upto max_instance_count which should be high
        It will keep going despite failures and errors (and not skip any available tasks)

        :param max_instance_count

        returns:
        a list of tasks tuple (task name, % completed, avg score)
        - % completed will be what percentage of the instances completed with a score of 1
        - avg score is a running mean of their score
        """

        input_format = "both"

        tasks = self.load_split_tasks(18)
        ret = []

        task_results = {} # dictionary mapping {task_name, {num_successes, num_errors, num_failing, sum_failing_scores, failing_tasks} }

        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")
            instance_ids = self.task_ids[task_name]
            first_instance_id = min(instance_ids) # TODO: Check if this is also just the first one, might be with how the JSON is formatted

            instance_ids = random.sample(instance_ids, min(max_instance_count, len(instance_ids)))

            num_successes = 0
            num_errors = 0
            sum_failing_scores = 0.0
            failing_tasks = []
            from utils.hidden_prints import HiddenPrintsHiddenErrors

            with HiddenPrintsHiddenErrors():
                for instance_id in instance_ids:
                    row_num = instance_id - first_instance_id

                    url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                    self.driver.get(url)

                    # get the name of the fields
                    df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                    input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
                    inputs = self.extract_input_values_from_url(url=url, task_name=task_name, input_names=input_names)

                    answers_map = self.retrieve_gold_labels(
                        task_name, row_num, [x.name for x in inputs]
                    )

                    # Same TODO as above, file (images videos audio, css etc. are html accessible and find all URLs)

                    # TODO copy over dump_features
                    # TODO copy over report_field_stats so task_field_statistics

                    error_flag = False
                    # for each input, now go ahead and answer it with oracle
                    for input_idx, i in enumerate(inputs):
                        element = self.driver.find_element(By.NAME, i.name)

                        if not element.is_displayed() or element.size['width'] <= 0 or element.size['height'] <= 0:
                            continue

                        # TODO dump_featuers

                        # assuming solver is oracle
                        kwargs = {'answers': answers_map[i.name]}
                        try:
                            self.solver.solve(i, **kwargs) # before would store the action sequence of oracle, not needed here
                        except Exception as error:
                            error_flag = True
                            continue

                        # TODO dump output features and collect field statistics

                    # get the resulting answers after our model outputs
                    model_outputs = self.extract_values(inputs)

                    # Hack in case model_outputs is zero, treat this as an error so don't divide by zero later
                    if len(model_outputs) == 0:
                        error_flag = True

                    if error_flag:
                        num_errors += 1
                        failing_tasks.append(row_num)
                        continue

                    score = self.score_outputs(inputs, task_name, row_num)

                    if score > 0.99:
                        num_successes += 1
                    else:
                        failing_tasks.append(row_num)
                        sum_failing_scores += score

            failing_tasks = failing_tasks[:10] # only keep the first 10 failing tasks
            task_results[task_name] = {"num_successes": num_successes, "num_errors": num_errors, "num_failing": len(instance_ids) - num_successes - num_errors, "sum_failing_scores": sum_failing_scores, "failing_tasks": failing_tasks}
            print("task result", task_name, task_results[task_name])

        return task_results

    
    def enumerate_tap_tasks_random(self, max_instance_count: int):
        """
        Enumerate all the tasks comprehensively, so going upto max_instance_count which should be high
        It will keep going despite failures and errors (and not skip any available tasks)

        :param max_instance_count

        returns:
        a list of tasks tuple (task name, % completed, avg score)
        - % completed will be what percentage of the instances completed with a score of 1
        - avg score is a running mean of their score
        """

        input_format = "both"

        tasks = self.load_task_names()
        ret = []

        task_results = {} # dictionary mapping {task_name, {num_successes, num_errors, num_failing, sum_failing_scores, failing_tasks} }

        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")
            instance_ids = self.task_ids[task_name]
            first_instance_id = min(instance_ids) # TODO: Check if this is also just the first one, might be with how the JSON is formatted

            instance_ids = random.sample(instance_ids, min(max_instance_count, len(instance_ids)))

            num_successes = 0
            num_errors = 0
            sum_failing_scores = 0.0
            failing_tasks = []
            from utils.hidden_prints import HiddenPrintsHiddenErrors

            with HiddenPrintsHiddenErrors():
                for instance_id in instance_ids:
                    row_num = instance_id - first_instance_id

                    url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                    self.driver.get(url)

                    # get the name of the fields
                    df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                    input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
                    inputs = self.extract_input_values_from_url(url=url, task_name=task_name, input_names=input_names)

                    answers_map = self.retrieve_gold_labels(
                        task_name, row_num, [x.name for x in inputs]
                    )

                    # Same TODO as above, file (images videos audio, css etc. are html accessible and find all URLs)

                    # TODO copy over dump_features
                    # TODO copy over report_field_stats so task_field_statistics

                    error_flag = False
                    # for each input, now go ahead and answer it with oracle
                    for input_idx, i in enumerate(inputs):
                        element = self.driver.find_element(By.NAME, i.name)

                        if not element.is_displayed() or element.size['width'] <= 0 or element.size['height'] <= 0:
                            continue

                        # TODO dump_featuers

                        # assuming solver is oracle
                        kwargs = {'answers': answers_map[i.name]}
                        try:
                            self.solver.solve(i, **kwargs) 
                        except Exception as error:
                            error_flag = True
                            continue

                        # TODO dump output features and collect field statistics

                    # get the resulting answers after our model outputs
                    model_outputs = self.extract_values(inputs)

                    # Hack in case model_outputs is zero, treat this as an error so don't divide by zero later
                    if len(model_outputs) == 0:
                        error_flag = True

                    if error_flag:
                        num_errors += 1
                        failing_tasks.append(row_num)
                        continue

            failing_tasks = failing_tasks[:10] # only keep the first 10 failing tasks
            task_results[task_name] = {"num_successes": num_successes, "num_errors": num_errors, "num_failing": len(instance_ids) - num_successes - num_errors, "sum_failing_scores": sum_failing_scores, "failing_tasks": failing_tasks}
            print("task result", task_name, task_results[task_name])

        return task_results