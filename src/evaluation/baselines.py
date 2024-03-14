import numpy as np
from colorama import Fore
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import date
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from evaluation.actions import MyActions
from evaluation.actions import ActionUtils
from evaluation.input import Input
from evaluation.prompts import get_encoded_input_prompt
from evaluation.vision import GPT4VModel, OLlamaVisionModel
from evaluation.text import GPT4Model, OLlamaTextModel, ClaudeTextModel
import logging
from typing import List
from utils.cleaning import clean_values
import os
import base64


class Baseline:
    """
    This is the base class for all baselines.
    """

    def __init__(self, actions: MyActions, driver):
        self.driver = driver
        self.actions = actions

    def solve(self, input: Input, **kwargs):
        """
        This function solves the task given the input name and type.
        """
        # TODO decide what the output of this function should be
        raise NotImplementedError("This method should be implemented by the subclass.")


class NewBaseline(Baseline):

    def solve_task(self, input: Input, **kwargs):
        # list of ations that can be performed on a HTML page
        dummy_input = Input(
            url="https://www.google.com",
            input_name="dummy",
            input_type="textarea",
            task_name="dummy")
        encoded_actions_prompt = get_encoded_input_prompt(dummy_input, "")
        print("encoded actions: ", encoded_actions_prompt)

        # Add your code here to process the HTML data and generate a summary

        # You can either make direct calls to the actions
        # for example, you can access the HTML code
        url = kwargs['url']
        html_result = self.actions.get_html(url)

        # or you can take screenshots of the page
        screenshot_result = self.actions.take_full_screenshot()

        # Or you can build a neural model that returns a bunch of commands in string format
        commands = "self.actions.scroll_to_element(input)"

        exec(commands)

        return


class OracleBaseline(Baseline):
    """
    This baseline uses the gold labels to solve the task.
    """

    def solve(self, input: Input, **kwargs):
        self.actions.wait_for_element(input.name)

        # wait 0.1 sec for the page to fully load
        sleep(0.1)
        self.actions.maximize_window()
        _, input_element = self.actions.scroll_to_element(input.name)

        # get the index of the input
        answers = kwargs['answers']
        print(f"{Fore.CYAN}--> Oracle baseline: Input name: {input.name}")
        print(f"{Fore.CYAN}--> Oracle baseline: answers", answers)
        answers = [answer for answer in answers if answer is not None and answer != '{}']
        print(f"{Fore.CYAN}--> Oracle baseline: filtered answers", answers)

        action = ""  # no action by default
        if len(answers) == 0:
            # do nothing
            pass
        elif input.type in ['text', 'textarea', 'password', 'email', 'number', 'tel', 'url']:
            # select an answer randomly
            for idx in range(len(answers)):
                a = answers[idx]
                if a in ["nan", "{}", "'{}'"] or (type(a) == float and np.isnan(a)):
                    answers[idx] = ""

            print(f"answers after mapping: `{answers}`")

            answers = clean_values(answers)
            answers = list(set(answers))

            answers_without_empty = [answer for answer in answers if answer != ""]
            if len(answers_without_empty) > 0:
                answer = random.choice(answers_without_empty)
            else:
                answer = random.choice(answers)
            action = self.actions.modify_text(input.name, answer)
        elif input.type in ['checkbox']:
            answer = random.choice(answers)
            if not input_element.is_selected():
                action = self.actions.modify_checkbox(input.name, answer)
        elif input.type in ['radio']:
            # do a majority vote and then select the majority answer
            votes = {}
            for answer in answers:
                if answer in votes:
                    votes[answer] += 1
                else:
                    votes[answer] = 1

            majority_answer = max(votes, key=votes.get)
            majority_answer_str = str(majority_answer)

            # commenting out this condition since looking up the input element does not take into account
            # the value of the input we want to select
            # if not input_element.is_selected():

            action = self.actions.modify_radio(input.name, majority_answer_str)

        elif input.type == 'select':
            votes = {}
            for answer in answers:
                if answer in votes:
                    votes[answer] += 1
                else:
                    votes[answer] = 1

            majority_answer = max(votes, key=votes.get)
            majority_answer_str = str(majority_answer)
            action = self.actions.modify_select(input.name, majority_answer_str)
        elif input.type == 'range':
            # average multiple answers
            answers = [float(answer) for answer in answers]
            avg_answer = sum(answers) / len(answers)
            action = self.actions.modify_range(input.name, avg_answer)
        elif input.type in ['button', 'color', 'date', 'datetime-local', 'file', 'hidden', 'image',
                            'month', 'reset', 'search', 'submit', 'time']:
            raise Exception(f"{Fore.RED} ** Warning **: We don't know how to handle this input type `{input.type}`")

        actions_per_input = {
            "input_name": input.name,
            "action_sequence": action,
        }

        return actions_per_input


class RandomBaseline(Baseline):
    """
    This baseline randomly selects an action from the list of actions that can be performed on a HTML page.
    Because this is somewhat of a complex implementation, we prefer to use the `DoNothingBaseline` instead.
    """

    def solve(self, input: Input, **kwargs):
        input_element = self.driver.find_element(By.NAME, input.name)
        input_type = input.type
        input_name = input.name
        if input.type in ['text', 'textarea', 'password', 'email', 'number', 'tel', 'url']:
            messages = ["Hello!", "How are you?", "What's up?", "Nice to meet you!"]
            return random.choice(messages)
        else:
            options = []
            if input_type == 'radio' or input_type == 'checkbox':
                options = [option.get_attribute('value') for option in self.driver.find_elements(By.NAME, input_name)]
            elif input_type == 'select-one':
                select_element = Select(input_element)
                options = [option.get_attribute('value') for option in select_element.options]
            elif input_type == 'number':
                min_value = int(input_element.get_attribute('min'))
                max_value = int(input_element.get_attribute('max'))
                step_value = int(input_element.get_attribute('step'))
                options = list(range(min_value, max_value + 1, step_value))
            elif input_type == 'range':
                min_value = int(input_element.get_attribute('min'))
                max_value = int(input_element.get_attribute('max'))
                step_value = int(input_element.get_attribute('step'))
                options = list(range(min_value, max_value + 1, step_value))
            elif input_type == 'color':
                colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF']
                options = colors
            elif input_type == 'date':
                start_date = date(2022, 1, 1)
                end_date = date(2023, 12, 31)
                delta = end_date - start_date
                options = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
            elif input_type == 'month':
                start_month = date(2022, 1, 1)
                end_month = date(2023, 12, 1)
                options = [start_month.strftime('%Y-%m')]
                while start_month < end_month:
                    start_month += relativedelta(months=+1)
                    options.append(start_month.strftime('%Y-%m'))
            elif input_type == 'week':
                start_week = date(2022, 1, 3)
                end_week = date(2023, 12, 26)
                options = [start_week.strftime('%Y-W%U')]
                while start_week < end_week:
                    start_week += timedelta(weeks=+1)
                    options.append(start_week.strftime('%Y-W%U'))
            elif input_type == 'time':
                start_time = datetime.strptime('00:00', '%H:%M')
                end_time = datetime.strptime('23:59', '%H:%M')
                delta_time = end_time - start_time
                minutes_diff = delta_time.total_seconds() / 60.0
                options = [(start_time + timedelta(minutes=i)).strftime('%H:%M') for i in range(int(minutes_diff) + 1)]
            elif input_type == 'datetime-local':
                start_datetime = datetime(2022, 1, 1, 0, 0)
                end_datetime = datetime(2023, 12, 31, 23, 59)
                delta_datetime = end_datetime - start_datetime
                minutes_diff = delta_datetime.total_seconds() / 60.0
                options = [(start_datetime + timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M') for i in
                           range(int(minutes_diff) + 1)]
            elif input.type in ['button', 'color', 'date', 'datetime-local', 'file', 'hidden', 'image',
                                'month', 'reset', 'search', 'submit', 'time']:
                raise Exception(
                    f"{Fore.RED} ** Warning **: We don't know how to handle this input type `{input.type}`")

            print("random choices options:", options)
            return random.choice(options)


class DoNothingBaseline(Baseline):
    """
    This baseline randomly does nothing!
    Yet, it provides a baseline for the minimum score that can be achieved.
    """

    def solve(self, input: Input, **kwargs):
        pass

class OfflineModelPredictionsBaseline(Baseline):
    """
    This baseline is used to execute the outputs of our ML models
    """

    def solve(self, input: Input, **kwargs) -> bool:
        """
        Executes the outputs of our ML models from outputs of string code and returns the score
        """

        output = kwargs['output']

        error_flag = False

        print("input:", input, "output:", output)
        self.actions.wait_for_element(input.name)

        # wait 0.1 sec for the page to fully load
        sleep(0.1)
        self.actions.maximize_window()
        self.actions.scroll_to_element(input.name)
        print("about to try executing one action, output:", output)

        try:
            exec(output)
            print("executed one action")
        except Exception as error:
            error_flag = True
            print(f"failed to execute an action {output}, error: {error}")

        return error_flag

class TextBaseline(Baseline):
    """
    Interactive calls to a VLM to solve the task
    """
    def __init__(self, actions: MyActions, driver, model: str, num_demonstrations: int, use_relevant_html: bool, ollama_model: str = "llava"):
        super().__init__(actions, driver)
        if model == "ollama":
            self.ollama_model = ollama_model

        match model:
            case "gpt4-text":
                self.model = GPT4Model()
            case "ollama":
                self.model = OLlamaTextModel(self.ollama_model)
            case "claude":
                self.model = ClaudeTextModel()
            case _:
                raise ValueError(f"Model {self.model} is not supported")

        self.num_demonstrations = num_demonstrations
        self.use_relevant_html = use_relevant_html

    def get_html(self, input: Input, url: str = None) -> str:
        """
        Depending on self.use_relevant_html, if false it is the entire HTML, otherwise:
        This function returns an array of the the relevant HTML lines for a given input field.
        If you want it to be a string of HTML, just to_string this list concatenating one after another
        """

        if not self.use_relevant_html:
            return self.actions.get_html(url)

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
        upper_bound = 5
        lower_bound = 10
        for i in range(max(0, mid_idx - upper_bound), min(len(HTML_arr), mid_idx + lower_bound)):
            relevant_html.append(HTML_arr[i])

        return "\n".join(relevant_html)

    def solve(self, input: Input, **kwargs) -> None:
        """
        Communicate with TextModel to solve the task
        """

        print("input:", input)
        self.actions.wait_for_element(input.name)

        # wait 0.1 sec for the page to fully load
        sleep(0.1)
        self.actions.maximize_window()
        self.actions.scroll_to_element(input.name)
        print("about to try executing one action, on the following input:", input.name)

        # extract HTML
        html = self.get_html(input, kwargs['url'])

        command = self.model.get_text_baseline_action(input.name, html, self.num_demonstrations, self.use_relevant_html)

        # find the index of "self.actions(" and drop anything before it.
        # This is because the GPT4 model sometimes outputs a lot of text before the actual command
        if not command.startswith("self.actions.") and "self.actions." in command:
            command = command[command.find("self.actions."):]
        if "```" in command:
            command = command.replace("```", "")

        try:
            print(f"{Fore.BLUE}Executing one action: {command}")
            exec(command)
        except Exception as error:
            print(f"{Fore.RED}Failed to execute an action {command}, error: {error}")

class VisionTextBaseline(Baseline):
    """
    Interactive calls to a VLM to solve the task
    """
    def __init__(self, actions: MyActions, driver, model: str, screenshot_path: str, num_demonstrations: int, use_relevant_html: bool, ollama_model: str = "llava"):
        super().__init__(actions, driver)
        self.model = model
        if self.model == "ollama":
            self.ollama_model = ollama_model
        self.screenshot_path = os.path.join("screenshots", screenshot_path)

        self.num_demonstrations = num_demonstrations
        self.use_relevant_html = use_relevant_html

    def get_html(self, input: Input, url: str = None) -> str:
        """
        Depending on self.use_relevant_html, if false it is the entire HTML, otherwise:
        This function returns an array of the the relevant HTML lines for a given input field.
        If you want it to be a string of HTML, just to_string this list concatenating one after another
        """

        if not self.use_relevant_html:
            return self.actions.get_html(url)

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
        upper_bound = 5
        lower_bound = 10
        for i in range(max(0, mid_idx - upper_bound), min(len(HTML_arr), mid_idx + lower_bound)):
            relevant_html.append(HTML_arr[i])

        return "\n".join(relevant_html)

    def solve(self, input: Input, **kwargs) -> None:
        """
        Communicate with VLM to solve the task
        """

        print("input:", input)
        self.actions.wait_for_element(input.name)

        # wait 0.1 sec for the page to fully load
        sleep(0.1)
        self.actions.maximize_window()
        self.actions.scroll_to_element(input.name)
        print("about to try executing one action, on the following input:", input.name)

        # extract HTML
        html = self.get_html(input, kwargs['url'])
        self.driver.save_screenshot(self.screenshot_path)
        
        match self.model:
            case "gpt4-text-vision":
                model = GPT4VModel()
            case "ollama":
                model = OLlamaVisionModel(self.ollama_model)
            case _:
                raise ValueError(f"Model {self.model} is not supported")

        command = model.get_vision_text_baseline_action(input.name, html, self.screenshot_path, self.num_demonstrations, self.use_relevant_html)

        # find the index of "self.actions(" and drop anything before it.
        # This is because the GPT4 model sometimes outputs a lot of text before the actual command
        if not command.startswith("self.actions.") and "self.actions." in command:
            command = command[command.find("self.actions."):]
        if "```" in command:
            command = command.replace("```", "")

        try:
            print(f"{Fore.BLUE}Executing one action: {command}")
            exec(command)
        except Exception as error:
            print(f"{Fore.RED}Failed to execute an action {command}, error: {error}")
