from colorama import init as colorama_init
from colorama import Fore
import configparser
from datetime import datetime
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
from typing import List, Union, Dict
import logging
import bisect
import copy
from utils.cleaning import clean_values
from utils.cleaning import try_numeric
from pyvirtualdisplay import Display

TURKLE_URL = "http://localhost:4000"

colorama_init(autoreset=True)


class GPTTokenizer:
    gpt_tokenizer = AutoTokenizer.from_pretrained("gpt2", max_length=1e5)

    def tokenize(self, s: str):
        tokens = self.gpt_tokenizer.tokenize(s)
        # GPT2 uses Byte-level BPE, which will include space as part of the word.
        # But for the first word of a sentence, there is no space before it.
        # So, we remove all the added spaces ("Ġ").
        tokens = [t.lstrip("Ġ") for t in tokens]
        return tokens


class Evaluation:
    def __init__(self, solver_type: str, tasks: str, do_eval: bool, dump_features: bool, report_field_stats: bool,
                 headless: bool = False, on_server: bool = False, **kwargs):
        """
        on_server flag specifies if we are running this on a server with xvfb and xserver-xephyr
        """
        self.default_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        self.xlingual_tokenizer = GPTTokenizer()
        self.xlingual_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], tokenizer=self.xlingual_tokenizer)

        if on_server:
            print(f"Starting display for the server")
            self.display = Display(visible=0, size=(1920, 1080))
            self.display.start()

        self.driver = self.create_driver(headless=headless, on_server=on_server)
        self.actions = MyActions(self.driver)
        self.solver = None
        self.on_server = on_server
        self.headless = headless
        # as more solvers that we implement, we can add them here:
        self.solver_type = solver_type
        if solver_type == "donothing":
            self.solver = baselines.DoNothingBaseline(driver=self.driver, actions=self.actions)
        elif solver_type == "random":
            self.solver = baselines.RandomBaseline(driver=self.driver, actions=self.actions)
        elif solver_type == "oracle":
            self.solver = baselines.OracleBaseline(driver=self.driver, actions=self.actions)
        elif solver_type == "offline_predictions":
            self.solver = baselines.OfflineModelPredictionsBaseline(driver=self.driver, actions=self.actions)
        elif solver_type == "text" or solver_type == "gpt4-text" or solver_type == "claude" or solver_type == "llama":
            if solver_type == "gpt4-text" or solver_type == "claude" or solver_type == "llama":
                self.solver = baselines.TextBaseline(driver=self.driver, actions=self.actions, model=solver_type, num_demonstrations=kwargs["num_demonstrations"], use_relevant_html=kwargs["use_relevant_html"])
            else:
                self.solver = baselines.TextBaseline(driver=self.driver, actions=self.actions, model="ollama", num_demonstrations=kwargs['num_demonstrations'], use_relevant_html=kwargs['use_relevant_html'], ollama_model=kwargs["ollama_model"])
                self.ollama_model = kwargs["ollama_model"]

            self.num_demonstrations = kwargs["num_demonstrations"]
            self.use_relevant_html = kwargs["use_relevant_html"]
        elif solver_type == "text-vision" or solver_type == "gpt4-text-vision" or solver_type == "llava":
            if solver_type == "gpt4-text-vision":
                self.solver = baselines.VisionTextBaseline(driver=self.driver, actions=self.actions, model=solver_type, screenshot_path=kwargs["screenshot_path"], num_demonstrations=kwargs["num_demonstrations"], use_relevant_html=kwargs["use_relevant_html"])
            if solver_type == "llava":
                self.solver = baselines.VisionTextBaseline(driver=self.driver, actions=self.actions, model=solver_type, screenshot_path=kwargs["screenshot_path"], num_demonstrations=kwargs["num_demonstrations"], use_relevant_html=kwargs["use_relevant_html"])
            else:
                self.solver = baselines.VisionTextBaseline(driver=self.driver, actions=self.actions, model="ollama", screenshot_path=kwargs["screenshot_path"], num_demonstrations=kwargs['num_demonstrations'], use_relevant_html=kwargs['use_relevant_html'], ollama_model=kwargs["ollama_model"])
                self.ollama_model = kwargs["ollama_model"]

            self.num_demonstrations = kwargs["num_demonstrations"]
            self.use_relevant_html = kwargs["use_relevant_html"]
        else:
            raise Exception(f"{Fore.RED}Solver `{solver_type}` not implemented")
        self.tasks = tasks
        assert tasks in ["test_easy", "test_hard", "train", "all", "subjective_test", "CI_tasks"] or tasks.startswith(
            "tap") or tasks.startswith("dmp")

        self.do_eval = do_eval
        self.dump_features = dump_features
        self.report_field_stats = report_field_stats

        # as soon as the code is loaded, we look for alignnent between the task names and their ids
        self.task_ids = requests.get(f"{TURKLE_URL}/get_tasks/").json()

        # exclude special inputs
        self.excluded_input_names = [
            'csrfmiddlewaretoken',  # hidden field automatically added external css files
            'worker_ip',  # hidden field for bookkeeping
            'ee',
            'submit'
        ]

    def __del__(self):
        print(f"Premature destructor being called potentially")
        try:
            if not self.headless and self.on_server:
                self.display.stop()
        except Exception as e:
            print(f"{Fore.RED}Error while stopping the display: {e}")

        self.driver.quit()

    def create_driver(self, headless: bool, on_server: bool = False):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        if on_server:
            options.add_experimental_option("detach", True)
        
        options.page_load_strategy = 'normal'

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

        print("The task names used: ", self.tasks)
        all_tasks = self.load_task_names()
        print("all_tasks len:", len(all_tasks))

        og_partitions = partitions
        split_tasks = []

        # Greedy optimized way to split evenly
        s = set()  # was originally a set, but python sets aren't as robust as C++ std
        sum = 0
        max_instance_count = 1000
        for task in all_tasks:
            df = pd.read_csv(f'../tasks/{task}/batch.csv', nrows=0)
            input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
            val = min(
                max_instance_count,
                len(self.task_ids[task])
            ) * (8 + len(input_names))  # num_tasks * num_inputs_per_task + 8 * num_tasks
            sum += val
            s.add((val, task))  # (val, task name)

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
                        assert len(set(test1).intersection(set(test2))) == 0, \
                            f"{Fore.RED}The tests are not mutually exclusive" \
                            f"splits are not exclusive\n: test1: {test1}\ntest2: {test2}" \
                            f"\nintersection: {set(test1).intersection(set(test2))}"

            if self.tasks == 'test_easy':
                return test
            elif self.tasks == 'test_hard':
                return test_hard
            elif self.tasks == 'subjective_test':
                return subjective_test
            elif self.tasks == 'train':
                # all tasks minus test and subjective test
                return list(set(all_tasks) - set(test) - set(subjective_test) - set(test_hard))
            elif self.tasks == 'CI_tasks' or self.tasks.startswith("tap"):
                # all the tasks that we monitor on in CI (training + test_easy)
                return list(set(all_tasks) - set(subjective_test) - set(test_hard))
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
                    # in HTML (they're created dynamically via JS). An exmaple task is "HTER - longer sentences"
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

            # is it visible?
            i.is_displayed = input.is_displayed()

            # save the position in html source: self.driver.page_source
            i.html_pos = self.driver.page_source.find(input_name)

            input_fields.append(i)

        # sort the input fields based on their y-coordinate, and then their x-coordinate
        input_fields = sorted(input_fields, key=lambda i: (i.y, i.x))

        # sort the input fields so that visible inputs (indicated by `.is_displayed()`) are first
        input_fields = sorted(input_fields, key=lambda i: i.is_displayed, reverse=True)

        # Commented for now; instead changed the code base to just use the order in which the Answer columns are given. We can rearrange it to the order of which inputs to fill in first
        return input_fields

    def extract_values(self, inputs: List[Input]):
        """
        Given a set of values for the input fields, extract the values from the HTML.
        We use this function for evaluation as well as unit testing.
        """

        for input in inputs:
            print("input:", input)
            if input.type in [
                'textarea'
            ]:
                visible_values = self.driver.execute_script(
                    f"return Array.from(document.getElementsByName(`{input.name}`)).filter((element) => element.readOnly == false).map((element) => element.innerHTML);"
                )

                values = visible_values

            elif input.type in [
                'text', 'password', 'email', 'number', 'tel', 'url', 'button', 'color', 'date', 'datetime-local',
                'file', 'image', 'range', 'hidden'
            ]:
                visible_values = self.driver.execute_script(
                    f"return Array.from(document.getElementsByName(`{input.name}`)).map((element) => element.getAttribute('value'));"
                )
                values = visible_values

            elif input.type in ['select']:
                values = self.driver.execute_script(
                    f"return Array.from(document.getElementsByName(`{input.name}`)[0].children).filter((el) => el.selected == true).map((el) => el.value);"
                )
                visible_values = values
                # print(f" visible_values : {visible_values}")
            elif input.type in ['radio']:
                values = self.driver.execute_script(
                    f"return Array.from(document.querySelectorAll(`input[name='{input.name}']:checked`)).map(element => element.value);"
                )
                visible_values = self.driver.execute_script(
                    f"return Array.from(document.getElementsByName(`{input.name}`)).filter(element => element.checked).map(element => element.value);"
                )
                assert len(values) <= 1, f"The number of values should be 1 or 0 but it is `{len(values)}` for {input}"
                assert len(visible_values) <= 1, \
                    f"The number of visible values should be 1 or 0 but it is `{len(visible_values)}` for {input}"

            elif input.type in ['checkbox']:
                if "'" in input.name:
                    command = f"""return Array.from(document.querySelectorAll(`input[name="{input.name}"]:checked`)).map(element => element.value);"""
                else:
                    command = f"""return Array.from(document.querySelectorAll(`input[name='{input.name}']:checked`)).map(element => element.value);"""
                values = self.driver.execute_script(command)

                command = f"""return Array.from(document.getElementsByName(`{input.name}`)).filter(element => element.checked).map(element => element.value);"""
                visible_values = self.driver.execute_script(command)

                # print("input:", input)
                # print("values:", values)
                # print("visible_values:", visible_values)
                # print(" - ")

            elif input.type in ['submit']:
                # do nothing
                values = []
                visible_values = []
            else:
                raise Exception(
                    f"{Fore.RED}To be implemented for type `{input.type}`")

            clean_visible_values = clean_values(visible_values)
            clean_visible_values = [
                html.unescape(v) for v in clean_visible_values
            ]

            input.values = clean_values(values)
            input.visible_values = clean_visible_values

            # TODO: in future, we should consider consolidating visible and visible_values
            print(f" visible : {values}")
            print(f" visible_values : {visible_values}")

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
        print(f"{Fore.BLUE} --> scores: ", score)
        return score

    @staticmethod
    def metric_mean_over_ground_truths(metric_fn, prediction, ground_truths, xlingual=False):
        """
        Returns the max score comparing model predicted output to over the ground truth labels that we have received from the gold labels
        """
        prediction = try_numeric(prediction)
        scores_for_ground_truths = []
        ground_truths = clean_values(ground_truths)
        for ground_truth in ground_truths:
            score = metric_fn(prediction, ground_truth, xlingual=xlingual)
            scores_for_ground_truths.append(score)
        score = float(sum(scores_for_ground_truths)) / len(scores_for_ground_truths)
        print(f"prediction {prediction} ground_truths {ground_truths}")
        print(f"{Fore.BLUE} --> scores: ", score)
        return score

    def retrieve_gold_labels(self, task_name: str, instance_index: int, inputs: List[Input]):
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

        # bringing this back in to check for errors in tap test 18
        assert len(df_subset) > 0, f"Could not find any answers for the instance index {instance_index}."

        # create a map for each Answer (input_name) to its corresponding answers of the instance
        answers_map = {
            input.name: df_subset.get(f"Answer.{input.name}", np.array([])).tolist() for input in inputs
        }

        # If the input type is checkbox, then convert "nan" values to empty strings
        for input in inputs:
            if input.type in ["checkbox", 'radio']:
                answers_map[input.name] = [
                    "" if type(answer) == float and np.isnan(answer) else answer for answer in answers_map[input.name]
                ]

        # Note: Should be careful with nan values since their equality is tricky in Python
        # Note: we explicitly do not exclude "nan" values (empty cells) because sometimes the correct action is to leave
        # the field empty. For example, not selecting a checkbox or leaving a text box empty. Of course there are also
        # scenarios where this is not correct (hence, some "noise" in the evaluation).
        # return [a for a in answers.tolist() if not (type(a) == float and np.isnan(a))]
        return answers_map

    def calculate_metrics(self, answers: List[str], input_type: str, baseline_answer: str):
        baseline_answer = str(baseline_answer)
        print(f"{Fore.YELLOW}----> answers: `{answers}` - type: `{type(answers)}`")
        print(f"{Fore.YELLOW}----> baseline_answer: `{baseline_answer}` - type: `{type(baseline_answer)}`")

        # handle empty
        if answers == [] or answers == [""]:
            if baseline_answer == "" or baseline_answer == [""] or \
                    baseline_answer == [] or baseline_answer == "[]" or baseline_answer == "['']":
                score = 1.0
            else:
                score = 0.0
        elif input_type in ['text', 'textarea', 'hidden']:
            answers = [str(answer) for answer in answers]
            answers = [answer for answer in answers if answer != ""]

            amp = "&amp;"
            answers = [answer.replace(amp, "&") for answer in answers]
            baseline_answer = baseline_answer.replace(amp, "&")

            score = Evaluation.metric_max_over_ground_truths(
                self.rouge,
                prediction=baseline_answer,
                ground_truths=answers,
                xlingual=False
            )
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

                score = Evaluation.metric_max_over_ground_truths(
                    self.exact_match,
                    prediction=baseline_answer,
                    ground_truths=[majority_answer_str],
                    xlingual=False
                )
            else:
                score = 0.0
        elif input_type in ['checkbox']:
            print(f"Model answers: {baseline_answer} \nGold answers: {answers}")
            score = Evaluation.metric_max_over_ground_truths(
                self.exact_match,
                prediction=baseline_answer,
                ground_truths=[str(answer) for answer in answers],
                xlingual=False
            )
        elif input_type in ['range']:
            # if the gold labels are numericals, then we can compute the mean absolute error
            # else, fall back to rouge
            try:
                answers = [float(answer) for answer in answers]
                baseline_answer = float(baseline_answer)
                # average distance to humans
                scores = np.mean(np.abs(np.array(answers) - baseline_answer))

                # max of baseline_answer and answers
                denominator = max(np.max(np.abs(np.array(answers))), np.abs(baseline_answer))

                if denominator > 0:
                    scores /= denominator
                score = 1 - scores
                print(f"{Fore.BLUE} --> using numeric values of the range to compute their error: {scores}")
            except Exception:
                score = Evaluation.metric_mean_over_ground_truths(
                    self.exact_match,
                    prediction=baseline_answer,
                    ground_truths=[str(answer) for answer in answers],
                    xlingual=False
                )
        else:
            raise Exception(f"{Fore.RED}to be implemented for type `{input_type}`")

        print(f"{Fore.YELLOW}----> per-field score: {score}")
        return score

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
        unfiltered_HTML = self.driver.execute_script(
            f"return document.getElementsByName('{input.name}')[0].parentElement.parentElement.outerHTML")
        HTML_arr = unfiltered_HTML.split(">")
        mid_idx = -1
        for idx, i in enumerate(HTML_arr):
            HTML_arr[idx] = i + ">"
            if HTML_arr[idx] == target_element:
                mid_idx = idx

        relevant_html = []
        upper_bound = 15
        lower_bound = 30
        for i in range(max(0, mid_idx - upper_bound), min(len(HTML_arr), mid_idx + lower_bound)):
            relevant_html.append(HTML_arr[i])

        return relevant_html

    def score_outputs(self, inputs: List[Input], answers_map: Dict, task_results: Dict) -> float:
        """
        This function scores the outputs from a model for a given task and instance given the inputs the model should've answered
        """
        # get the input values from the web page
        fail_count=0
        while fail_count < 20:
            try:
                model_outputs = self.extract_values(inputs)
                print(f"MODEL OUTPUTS: {model_outputs}")
                break
            except Exception as e:
                fail_count+=1
                print(f"ERROR: Webdriver Timed Out, Exception - {e}, Trying again x{fail_count}")
        else:
            model_outputs = []

        score = 0.0
        count = 0
        for i in model_outputs:

            print(f"{Fore.GREEN} ------- evaluating input: {i} ------- ")
            if i.name in self.excluded_input_names:
                continue

            if i.type == 'submit':
                continue

            element = self.driver.find_element(By.NAME, i.name)
            if not element.is_displayed():
                # Commenting out this condition since sometimes we have visible inputs with 0 width or height
                # or element.size['width'] <= 0 or element.size['height'] <= 0:
                print(f'{Fore.RED}Skipping element `{i.name}` since it is not visible.')
                continue

            # temp commenting out of this visible values to see what files in TAP tests 18 need to have their ending rows deleted
            # if i.values != i.visible_values:
            #     raise Exception(
            #         f"{Fore.RED}The values `{i.values}` and visible values `{i.visible_values}` should be the same for `{i}`"
            #     )

            # if the answer is already empty for text input, skip it.
            # otherwise, we would be crediting the model for not filling in the input.
            if answers_map[i.name] == [] and i.type in ['text', 'textarea', 'hidden']:
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

            # if the input type is textbox and the gold text is empty, skip it.
            # otherwise, we would be crediting the model for not filling many inputs that are not required.
            if i.type in ['text', 'textarea', 'hidden']:

                answers = answers_map[i.name]
                # normalize responses: turn "nan", or "{}" into empty string
                for idx in range(len(answers)):
                    a = answers[idx]
                    if a in ["nan", "{}", "'{}'"] or (type(a) == float and np.isnan(a)):
                        answers[idx] = ""

                print(f"answers after mapping: `{answers}`")

                answers = clean_values(answers)
                answers = list(set(answers))

                answers_map[i.name] = answers

                if answers == [] or answers == [""]:
                    continue

            # the score for this specific model input/output
            score_per_field = self.calculate_metrics(answers_map[i.name], i.type, i.values)

            if task_results is not None:
                if i.type not in task_results:
                    task_results[i.type] = []

                task_results[i.type].append(score_per_field)

            # if the input type is range, do not count it towards the score
            # we use this score for the automatic checks and we do not have a way to automatically check the range
            if i.type not in ['range']:
                score += score_per_field
                count += 1
            else:
                # instead of ignoring, use perfect score for range otherwise the tests would fail for
                # tasks that have range inputs only
                score += 1.0
                count += 1

        # There are difficult tasks that you need do some movemenets in order for the inputs to appear.
        # Otherwise, nothing would be visible and the score would be 0.
        if count > 0:
            score /= count  # average score for this instance

        return score

    def enumerate_tasks(self, max_instance_count: int, **kwargs):
        """
        Enumerate the tasks and their instances for the main evaluation loop to go through.
        :param max_instance_count: maximum number of instances per task
        """
        if self.tasks.startswith("dmp"):
            # TODO: explain what this is
            tasks = self.load_split_tasks(kwargs.get("dump_partitions"))
        else:
            tasks = self.load_task_names()

        # Override the task of tasks if a specific task is specified
        if "task" in kwargs:
            tasks = [kwargs["task"]]
            print("tasks", tasks)

        results = {}
        aggregate_field_statistics = {}  # We store the stats related to the field types/frequency here
        if self.report_field_stats:
            task_field_statistics = {}
        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")

            # skip, if starting with .
            if task_name.startswith("."):
                continue

            instance_ids = self.task_ids[task_name]
            first_instance_id = min(instance_ids)
            print("First instance id:", first_instance_id)

            per_task_score = 0.0

            # Create a random sample
            instance_ids = random.sample(instance_ids, min(max_instance_count, len(instance_ids)))
            if "first_instance_only" in kwargs and kwargs["first_instance_only"] == True:
                instance_ids = [first_instance_id]

            # collecting field statistics
            if task_name not in results:
                results[task_name] = {}

            if self.dump_features:
                directory = f'/scratch4/danielk/kxu39/turk_data/{task_name}'
                images_directory = f'{directory}/images'
                html_directory = f'{directory}/HTML'

                Path(directory).mkdir(parents=True, exist_ok=True)
                Path(html_directory).mkdir(parents=True, exist_ok=True)

                data_to_be_dumped = []
                curr_data_to_be_dumped = {}

            # Override instance_ids if specified the row_num
            if self.solver_type == "offline_predictions":
                answer_map = {}
                instance_ids = []
                for key, value in kwargs["params"].items():
                    instance_id = first_instance_id + int(key)
                    instance_ids.append(instance_id)
                    answer_map[instance_id] = {}
                    for row in value:
                        answer_map[instance_id][row["input_name"]] = row["action_sequence"]

            # Go through the instances of each task in this random sample
            for instance_id in instance_ids:

                row_number = instance_id - first_instance_id
                print(f"instance_id: {instance_id} <-> row_number: {row_number}")

                url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                self.driver.get(url)

                # get the name of the fields
                df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
                inputs = self.extract_input_values_from_url(url=url, task_name=task_name, input_names=input_names)

                print(" --> inputs: {}".format([x.name for x in inputs]))

                answers_map = self.retrieve_gold_labels(task_name, row_number, inputs)

                print(" --> input labels: {}".format(answers_map))

                # for counting overall statistics
                if self.report_field_stats:
                    if task_name not in task_field_statistics:
                        task_field_statistics[task_name] = {}
                        task_field_statistics[task_name]["instances"] = len(instance_ids)
                        task_field_statistics[task_name]["total_instances"] = len(self.task_ids[task_name])
                        task_field_statistics[task_name]["instantiated_templates"] = 0
                    html = self.actions.get_html(url)
                    task_field_statistics[task_name]["instantiated_templates"] += len(self.xlingual_tokenizer.tokenize(html))

                if self.dump_features:
                    curr_data_to_be_dumped["task_name"] = task_name
                    curr_data_to_be_dumped["instance_id"] = instance_id
                    curr_data_to_be_dumped["row_num"] = row_number
                    curr_data_to_be_dumped["fields"] = []

                for input_idx, i in enumerate(inputs):
                    print(f"{Fore.GREEN} - - - - - -  starting a new element: `{i}` - - - - - -  ")

                    # wait for the element to be visible
                    try:
                        self.actions.wait_for_element(i.name)
                    except:
                        print(f"{Fore.RED}Waited but didn't find input field with name `{i.name}`")

                    if self.report_field_stats: 
                        if i.type not in aggregate_field_statistics:
                            aggregate_field_statistics[i.type] = 0

                        aggregate_field_statistics[i.type] += 1

                        if i.type not in task_field_statistics[task_name]:
                            task_field_statistics[task_name][i.type] = 0
                        task_field_statistics[task_name][i.type] += 1

                    try:
                        # make sure that the element is visible
                        element = self.driver.find_element(By.NAME, i.name)
                    except Exception as e:
                        print(f"{Fore.RED}Could not find input field with name `{i.name}`")
                        continue

                    if not element.is_displayed():
                        # commenting out this condition since sometimes we have visible inputs with 0 width or height
                        # or element.size['width'] <= 0 or element.size['height'] <= 0:
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
                        solver_kwargs = {'answers': answers_map[i.name]}
                        oracle_action_sequence = self.solver.solve(i, **solver_kwargs)
                    elif self.solver_type == 'model':
                        # TODO: the name should be "offline" here?
                        # TODO: check if we really need to pass "answer_map" here?
                        self.solver.solve(i, output=answer_map[instance_id][i.name])
                    else:
                        # random, donothing solvers, or model solvers that don't need to be trained
                        kwargs = {'url': url}
                        self.solver.solve(i, **kwargs)

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

                    if "input_name" in kwargs and i.name == kwargs["input_name"]:
                        print("=" * 20)
                        print("\"" * 3)
                        print(f"Input name: {i.name}")
                        print(f"HTML:\n{self.driver.execute_script('return document.documentElement.outerHTML;')}")
                        print("\"\"\",")
                        print(f"\"{oracle_action_sequence['action_sequence']}\"")
                        print("=" * 20)

                if self.dump_features:
                    data_to_be_dumped.append(copy.deepcopy(curr_data_to_be_dumped))

                if self.do_eval:
                    score = self.score_outputs(inputs, answers_map, results[task_name])
                    print(f"{Fore.CYAN} --> Per-instance overall score: {score}")
                    print(f"{Fore.CYAN} --> Per-instance per-field breakdown: {results[task_name]}")

                    # wait for a keyboard press before continuing
                    # input("Press Enter to continue to the next instance...")

                    per_task_score += score

                    if self.solver_type == 'oracle':
                        assert score > 0.99, f"{Fore.RED}The oracle baseline should always get a score of 1.0. Instead got `{score}`."
                    elif self.solver_type == 'model':
                        kwargs["scores"].append(score)

        if self.do_eval:
            # per-task statistics
            per_task_score = per_task_score / len(instance_ids)
            print(f"{Fore.MAGENTA}Task: {task_name} --> Score: {per_task_score}")
            df = pd.DataFrame()
            for task_name, inputs in results.items():
                all_scores = []
                for input_type, scores in inputs.items():
                    avg_score = sum(scores) / len(scores)
                    all_scores.extend(scores)
                    df = pd.concat(
                        [
                            df, pd.DataFrame({
                            'project': [task_name],
                            'input_type': [input_type],
                            'score': [avg_score]
                        })
                        ],
                        ignore_index=True)


                # add the overall score across all the inputs
                df = pd.concat([
                    df, pd.DataFrame({
                        'project': [task_name],
                        'input_type': ["all"],
                        'score': [sum(all_scores) / len(all_scores)]
                    }
                    )], ignore_index=True
                )

            if 'project' not in df.columns:
                df.insert(0, 'project', '')
            if 'input_type' not in df.columns:
                df.insert(1, 'input_type', '')
            if 'score' not in df.columns:
                df.insert(1, 'score', '')

            df = df.pivot(index='project', columns='input_type', values='score')
            today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            if self.solver_type == "gpt4-text" or self.solver_type == "gpt4-text-vision":
                csv_filename = f'{self.solver_type}_{self.num_demonstrations}_use-relevant-html_{self.use_relevant_html}_{self.tasks}_scores_{today}.csv'
            elif self.solver_type == "text" or self.solver_type == "text-vision":
                csv_filename = f'{self.solver_type}_{self.ollama_model}_{self.num_demonstrations}_use-relevant-html_{self.use_relevant_html}_{self.tasks}_scores_{today}.csv'
            else:
                csv_filename = f'{self.solver_type}_{self.tasks}_scores_{today}.csv'

            df.to_csv(csv_filename, index=True)

            # save results to json
            with open(f'{self.solver_type}_scores_{today}.json', 'w') as f:
                json.dump(results, f, indent=4)

        if self.dump_features:
            with open(f'{directory}/{task_name}.json', 'w') as f:
                json.dump(data_to_be_dumped, f, indent=4)

        if self.report_field_stats:
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

        tasks = self.load_split_tasks(18)

        task_results = {}  # dictionary mapping {task_name, {num_successes, num_errors, num_failing, sum_failing_scores, failing_tasks} }

        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")
            instance_ids = self.task_ids[task_name]
            first_instance_id = min(
                instance_ids)  # TODO: Check if this is also just the first one, might be with how the JSON is formatted

            instance_ids = random.sample(instance_ids, min(max_instance_count, len(instance_ids)))

            num_successes = 0
            num_errors = 0
            sum_failing_scores = 0.0
            task_score = 0.0
            failing_tasks = []
            from utils.hidden_prints import HiddenPrintsHiddenErrors

            with HiddenPrintsHiddenErrors():
                for instance_id in instance_ids:
                    row_num = instance_id - first_instance_id
                    error_flag = False

                    url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                    self.driver.get(url)

                    # get the name of the fields
                    df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
                    input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
                    inputs = self.extract_input_values_from_url(url=url, task_name=task_name, input_names=input_names)

                    # Add stuff from kevin-2 to skip out on these answer_map
                    try:
                        answers_map = self.retrieve_gold_labels(task_name, row_num, inputs)
                    except:
                        error_flag = True

                        if error_flag:
                            num_errors += 1
                            failing_tasks.append(row_num)
                            continue

                    # Same TODO as above, file (images videos audio, css etc. are html accessible and find all URLs)

                    # TODO copy over dump_features
                    # TODO copy over report_field_stats so task_field_statistics

                    # for each input, now go ahead and answer it with oracle
                    for input_idx, i in enumerate(inputs):
                        element = self.driver.find_element(By.NAME, i.name)

                        if not element.is_displayed() or element.size['width'] <= 0 or element.size['height'] <= 0:
                            continue

                        # TODO dump_featuers

                        # assuming solver is oracle
                        kwargs = {'answers': answers_map[i.name]}
                        try:
                            # before would store the action sequence of oracle, not needed here
                            self.solver.solve(i, **kwargs)
                        except Exception as error:
                            error_flag = True
                            continue

                        # TODO dump output features and collect field statistics

                    # get the resulting answers after our model outputs
                    fail_count=0
                    while fail_count < 20:
                        try:
                            model_outputs = self.extract_values(inputs)
                            print(f"MODEL OUTPUTS: {model_outputs}")
                            break
                        except Exception as e:
                            fail_count+=1
                            print(f"ERROR: Webdriver Timed Out, Exception - {e}, Trying again x{fail_count}")
                    else:
                        model_outputs = []

                    # Hack in case model_outputs is zero, treat this as an error so don't divide by zero later
                    if len(model_outputs) == 0:
                        error_flag = True

                    if error_flag:
                        num_errors += 1
                        failing_tasks.append(row_num)
                        continue

                    score = self.score_outputs(inputs, answers_map, task_results=None)

                    if score > 0.95:
                        num_successes += 1
                    else:
                        failing_tasks.append(row_num)
                        sum_failing_scores += score

                    task_score += score

            failing_tasks = failing_tasks[:10]  # only keep the first 10 failing tasks
            task_results[task_name] = {
                "num_successes": num_successes,
                "num_errors": num_errors,
                "num_failing": len(instance_ids) - num_successes - num_errors,
                "sum_failing_scores": sum_failing_scores,
                "failing_tasks": failing_tasks,
                "task_score": task_score / len(instance_ids)
            }
            print(f"{Fore.MAGENTA}Task result", task_name, task_results[task_name])

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

        tasks = self.load_task_names()

        task_results = {}  # dictionary mapping {task_name, {num_successes, num_errors, num_failing, sum_failing_scores, failing_tasks} }

        for task_name in tqdm(tasks):
            print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")
            instance_ids = self.task_ids[task_name]
            first_instance_id = min(
                instance_ids)  # TODO: Check if this is also just the first one, might be with how the JSON is formatted

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

                    answers_map = self.retrieve_gold_labels(task_name, row_num, inputs)

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
                    fail_count=0
                    while fail_count < 20:
                        try:
                            model_outputs = self.extract_values(inputs)
                            print(f"MODEL OUTPUTS: {model_outputs}")
                            break
                        except Exception as e:
                            fail_count+=1
                            print(f"ERROR: Webdriver Timed Out, Exception - {e}, Trying again x{fail_count}")
                    else:
                        model_outputs = []

                    # Hack in case model_outputs is zero, treat this as an error so don't divide by zero later
                    if len(model_outputs) == 0:
                        error_flag = True

                    if error_flag:
                        num_errors += 1
                        failing_tasks.append(row_num)
                        continue

            failing_tasks = failing_tasks[:10]  # only keep the first 10 failing tasks
            task_results[task_name] = {
                "num_successes": num_successes,
                "num_errors": num_errors,
                "num_failing": len(instance_ids) - num_successes - num_errors,
                "sum_failing_scores": sum_failing_scores, "failing_tasks": failing_tasks
            }
            print("task result", task_name, task_results[task_name])

        return task_results
