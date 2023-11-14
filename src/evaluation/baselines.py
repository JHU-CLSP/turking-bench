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
from evaluation.input import Input
import logging
from typing import List

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

    def get_action_list(self):
        """
        This function returns the list of actions that can be performed on a HTML page as implemented in the Actions class.
        This list is particularly useful for designing "tool" (actin)-augmented web-browsing agents.
        """
        # get the list of methods in the Actions class
        action_list = [method for method in dir(MyActions) if not method.startswith('_')]
        # include their docstrings as well
        action_list = [(method, getattr(MyActions, method).__doc__) for method in action_list]
        return action_list

    def get_encoded_input_prompt(self, input: Input):
        actions = self.get_action_list()
        # encode the actions as a string
        actions = '\n\n'.join([f"{action[0]}: {action[1]}" for action in actions])
        return f"""
        Given a web-based task, we'd like to solve it by executing actions. Below is a list of actions that
        can be performed on a HTML page. \n\n{actions} \n\n

        Now, given the following input `{input}`, decide what set of actions need to be executed.
        """



class NewBaseline(Baseline):

    def solve_task(self, input: Input, **kwargs):
        # list of ations that can be performed on a HTML page
        dummy_input = Input(
            url="https://www.google.com",
            input_name="dummy",
            input_type="textarea",
            task_name="dummy")
        encoded_actions_prompt = self.get_encoded_input_prompt(dummy_input)
        print("encoded actions: ", encoded_actions_prompt)

        # Add your code here to process the HTML data and generate a summary

        # Youc can either make direct calls to the actions
        # for example, you can access the HTML code
        html_result = self.actions.get_html()

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
        print("Called solve, input:", input)
        # get the index of the input
        answers = kwargs['answers']
        print("kwargs", kwargs) # answers should not be empty since you rely on answers to do things
        print("answers", answers)
        actions_per_input = ""  # no action by default
        for answer in answers:
            if answer and answer != '{}':
                # self.actions.execute_command(input, answer)

                print(f" --> Input name: {input.name}")
                print(f" --> Input value: {answer}")

                r1 = self.actions.wait_for_element(input)

                # wait 0.1 sec for the page to fully load
                sleep(0.1)
                self.actions.maximize_window()
                response = self.actions.scroll_to_element(input)
                input_element = response.outcome

                action_sequence = []

                if input.type in ['text', 'textarea', 'password', 'email', 'number', 'tel', 'url']:
                    action_sequence.append(self.actions.modify_text(input.name, answer))
                elif input.type in ['checkbox']:
                    if not input_element.is_selected():
                        action_sequence.append(self.actions.modify_checkbox(input.name, answer))
                elif input.type in ['radio']:
                    if not input_element.is_selected():
                        action_sequence.append(self.actions.modify_radio(input.name, answer))
                elif input.type == 'select':
                    action_sequence.append(self.actions.modify_select(input.name, answer))
                elif input.type == 'range':
                    action_sequence.append(self.actions.modify_range(input.name, answer))
                elif input.type in ['button', 'color', 'date', 'datetime-local', 'file', 'hidden', 'image',
                                    'month', 'reset', 'search', 'submit', 'time']:
                    raise Exception(
                        f"{Fore.RED} ** Warning **: We don't know how to handle this input type `{input.type}`")

                action_sequence = "\n\n".join([r.action for r in action_sequence])
                actions_per_input = {
                    "input_name": input.name,
                    "action_sequence": action_sequence,
                }
                break

        return actions_per_input


class RandomBaseline(Baseline):
    """
    This baseline randomly selects an action from the list of actions that can be performed on a HTML page.
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

class ModelBaseline(Baseline):
    """
    This baseline is used to execute the outputs of our ML models
    """

    def solve(self, inputs: List[Input], outputs, **kwargs) -> bool:
        """
        Executes the outputs of our ML models from outputs of string code and returns the score
        """

        error_flag = False
        for idx, output in enumerate(outputs):
            input = inputs[idx]
            print("input:", input)
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
