from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import date
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from evaluation.actions import MyActions
from evaluation.input import Input
# from 4.run_evaluation import Evaluation
evaluation = __import__('4_run_evaluation')

class Baseline:
    """
    This is the base class for all baselines.
    """
    def solve(self, input: Input, driver, **kwargs):
        """
        This function solves the task given the input name and type.
        """
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

    def get_encoded_action_list(self):
        actions = self.get_action_list()
        # encode the actions as a string
        actions = '\n'.join([f"{action[0]}: {action[1]}" for action in actions])
        return f"""
        Our job is to solve a bunch of web-based tasks. 
        Below is a list of actions that can be performed on a HTML page.
        {actions}
        """

class NewBaseline(Baseline):

    def solve_task(self, input: Input, driver, **kwargs):
        screenshot = Input.take_screenshot(driver)
        full_screenshot = Input.take_full_screenshot(driver)
        html = input.get_html()

        # Add your code here to process the HTML data and generate a summary

        result = None
        return result

class OracleBaseline(Baseline):
    """
    This baseline uses the gold labels to solve the task.
    """

    def solve(self, input: Input, driver, **kwargs):
        # get the index of the input
        index = kwargs['index']
        answers_map = evaluation.Evaluation.retrieve_gold_labels(input.task, index, [input.name])
        answers = answers_map[input.name]
        for answer in answers:
            if answer and answer != '{}':
                return answer
        return None

class RandomBaseline(Baseline):
    """
    This baseline randomly selects an action from the list of actions that can be performed on a HTML page.
    """
    def solve(self, input: Input, driver, **kwargs):
        input_element = driver.find_element(By.NAME, input.name)
        input_type = input.type
        input_name = input.name
        if input_type == 'text':
            messages = ["Hello!", "How are you?", "What's up?", "Nice to meet you!"]
            return random.choice(messages)
        else:
            options = []
            if input_type == 'radio' or input_type == 'checkbox':
                options = [option.get_attribute('value') for option in driver.find_elements(By.NAME, input_name)]
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
            return random.choice(options)
