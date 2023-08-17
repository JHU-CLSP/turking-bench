import csv
import argparse
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import date
import string
import os
import time
from rouge_score import rouge_scorer
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
from time import sleep
from PIL import Image, ImageDraw
import io
from io import BytesIO
import math
import pandas as pd
import random
import configparser
import json
from transformers import AutoTokenizer

TURKLE_URL = "http://localhost:8001"


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
        print(" - - - inside rouge  - - - ")
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
    def retrieve_gold_labels(project_name, instance_index, input_name):
        df = pd.read_csv(f'../tasks/{project_name}/batch.csv')
        # Keep the columns that are not answers and then combine the rows that are the same to find the distinct inputs
        cols = [col for col in df.columns if not col.startswith("Answer.")]
        distinct_rows = df[cols].drop_duplicates()
        if instance_index <= len(distinct_rows):
            # select the row
            ith_row = distinct_rows.iloc[[instance_index - 1]]
            result = df[df[cols].isin(ith_row.to_dict('list')).all(axis=1)]
            return result[f'Answer.{input_name}'].tolist()
        else:
            return []

    def calculate_rouge(self, project_name, index, input_type, input_name, baseline_answer):
        baseline_answer = str(baseline_answer)
        answers = Evaluation.retrieve_gold_labels(project_name, index, input_name)
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
        elif input_type in ['radio']:
            # if the field type is radio button, then compute the majority vote among the options
            print("Computing the majority vote")
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
                    self.rouge,
                    prediction=majority_answer_str,
                    ground_truths=[majority_answer_str],
                    xlingual=False
                )

                return scores
            else:
                return 0.0
        else:
            raise Exception("to be implemented")


class Input:
    def __init__(self, url, input_name):
        self.url = url
        self.input_name = input_name

    def get_html(self):
        response = requests.get(self.url)
        html = response.text
        return html

    @staticmethod
    def extract_input_values_from_url(url, input_names=None):
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
            input_names = set()
            inputs = soup.find_all(['input', 'textarea', 'select'])

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

            input_fields.append({'input_type': input_type, 'input_name': input_name})

        # before returning them, sort the input values based on their position in the HTML
        return sorted(
            input_fields,
            key=lambda x: str(soup).index(str(soup.find(attrs={'name': x['input_name']})))
        )


class MyActions:
    """
    This class contains the actions that can be performed on an HTML page
    """

    def __init__(self, driver):
        """
        :param driver: selenium driver
        """
        self.driver = driver

    def execute_js_command(self, command, *args):
        """
        Executes the javascript command and returns the result.
        """
        return self.driver.execute_script(command, *args)

    def maximize_window(self):
        """
        This function maximizes the browser window to make sure we can see all the elements on the page.
        """
        self.driver.maximize_window()

    def scroll_to_element(self, element_name):
        """
        This function scrolls to a given element on the page, after the page is fully loaded.
        It then returns the element.
        """
        input_element = self.wait_for_element(element_name)
        self.execute_js_command("arguments[0].scrollIntoView();", input_element)
        return input_element

    def wait_for_element(self, element_name):
        """
        This function waits for a given element to be loaded on the page, and then returns the element.
        """
        input_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, element_name)))
        return input_element

    def modify_text(self, input_name, input_value):
        """
        For a given editable input field such as text box or text area, this function enters the input value into
        the input field.
        :param input_name: name of the input field
        :param input_value: value to be entered into the input field
        :return: None
        """
        input_element = self.scroll_to_element(input_name)
        action = ActionChains(self.driver).move_to_element(input_element).click()
        # now modify the text
        action.send_keys(input_value)
        action.perform()

    def modify_checkbox(self, input_name, input_value):
        """
        For a given checkbox, this function clicks on the specified checks.
        """

        # if input value is not string, turn it into a string
        if not isinstance(input_value, str):
            input_value = str(input_value)

        self.wait_for_element(input_name)
        input_element = self.scroll_to_element(input_name)
        action = ActionChains(self.driver).move_to_element(input_element).click()
        # now modify the text
        action.send_keys(input_value)
        action.perform()

    @staticmethod
    def xpath_string_escape(input_str):
        """ creates a concatenation of alternately-quoted strings that is always a valid XPath expression """
        parts = input_str.split("'")
        return "concat('" + "', \"'\" , '".join(parts) + "', '')"

    def modify_radio(self, input_name, input_value):
        """
        For a given radio button, this function clicks on the specified radio button.
        """
        # if input value is double/float, turn it into an integer
        if isinstance(input_value, float):
            input_value = int(input_value)

        # if input value is not string, turn it into a string
        if not isinstance(input_value, str):
            input_value = str(input_value)

        self.scroll_to_element(input_name)
        value = f"@value='{input_value}'"
        if "'" in input_value:
            value = f'@value="{input_value}"'
        elif "'" in input_name and '"' in input_value:
            value = value = f'@value=`{input_value}`'

        element = self.driver.find_element(
            By.XPATH, f"//input[@type='radio' and @name='{input_name}' and {value}]"
        )

        # print element in HTML format
        print("We are going to select this radio button:")
        print(element.get_attribute('outerHTML'))

        action = ActionChains(self.driver).move_to_element(element).click()
        action.perform()

    def modify_select(self, input_name, input_value):
        """
        For a given select field, this function selects the specified option.
        """
        input_element = self.scroll_to_element(input_name)
        select = Select(input_element)
        select.select_by_visible_text(input_value)

    def execute_command(self, input_type, input_value, input_name):
        """
        For a given input field, this function enters the input value into the input field.
        :param input_type: type of the input field
        :param input_value: value to be entered into the input field
        :param input_name: name of the input field
        :return: None
        """
        print(f" ---> Input name: {input_name}")
        print(f" ---> Input value: {input_value}")
        try:
            self.wait_for_element(input_name)
            self.maximize_window()
            input_element = self.scroll_to_element(input_name)

            if input_type in ['text', 'textarea', 'password', 'email', 'number', 'tel', 'url']:
                self.modify_text(input_name, input_value)

            elif input_type in ['checkbox']:
                if not input_element.is_selected():
                    self.modify_checkbox(input_name, input_value)

            elif input_type in ['radio']:
                if not input_element.is_selected():
                    self.modify_radio(input_name, input_value)

            elif input_type == 'select':
                self.modify_select(input_name, input_value)

            elif input_type in ['button', 'color', 'date', 'datetime-local', 'file', 'hidden', 'image', 'month',
                                'range', 'reset', 'search', 'submit', 'time']:
                pass

        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"We have a problem with '{input_name}'")
            print(input_value)

    def take_screenshot(self):
        """
        This function takes a screenshot of the entire page that is currently visible. It then saves the screenshot.
        """
        # Get scroll height
        last_height = self.execute_js_command("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # Take screenshot
        self.driver.save_screenshot('screenshot.png')

    def take_element_screenshot(self, driver, input_name, input_type):
        """
        This function takes a screenshot of a given element on the page.
        """
        # find the element based on input name and type
        if input_type in ['select', 'textarea']:
            element = Select(self.driver.find_element(By.NAME, input_name)).first_selected_option
        else:
            element = driver.find_element(By.NAME, input_name)
        # get the location and size of the element
        location = element.location
        size = element.size

        # take a screenshot of the entire page
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        # crop the image to the size of the element
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        cropped_image = image.crop((left, top, right, bottom))
        return cropped_image

    def take_element_screenshot_with_border(self, driver, input_name, input_type):
        """
        This function takes a screenshot of the entire page and draws a red border around the specified element.
        """

        # find the element based on input name and type
        if input_type in ['select', 'textarea']:
            element = Select(self.driver.find_element(By.NAME, input_name)).first_selected_option
        else:
            element = self.driver.find_element(By.NAME, input_name)

        # get the location and size of the element
        location = element.location
        size = element.size

        # scroll to the element and wait for it to be visible
        driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(1)

        # take a screenshot of the entire page
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        # draw a red border around the element
        draw = ImageDraw.Draw(image)
        draw.rectangle((location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']),
                       outline='red')

        return image

    def take_page_screenshots(self):
        """
        This function takes a screenshot of the entire page by scrolling down the page and taking a screenshot of each
        """
        screenshots = []

        # get the size of the window
        window_size = self.driver.execute_script("return [window.innerWidth, window.innerHeight];")

        # get the height of the entire page
        page_height = self.driver.execute_script("return document.documentElement.scrollHeight")

        # set the initial scroll position to the top
        scroll_position = 0

        while scroll_position < page_height:
            # take a screenshot of the current view
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            screenshots.append(image)

            # scroll down to the next view
            scroll_position += window_size[1]
            self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        return screenshots

    def take_full_screenshot(self):
        """
        This function takes a screenshot of the entire page by stitching together screenshots of each view.
        """
        # Get dimensions of webpage
        total_width = self.driver.execute_script("return document.body.offsetWidth")
        total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = self.driver.execute_script("return document.body.clientWidth")
        viewport_height = self.driver.execute_script("return window.innerHeight")
        # Calculate number of rows and columns needed to capture entire webpage
        rows = math.ceil(total_height / viewport_height)
        cols = math.ceil(total_width / viewport_width)
        # Initialize stitched image
        stitched_image = Image.new('RGB', (total_width, total_height))
        for row in range(rows):
            for col in range(cols):
                # Scroll to current row and column
                self.driver.execute_script(f"window.scrollTo({col * viewport_width}, {row * viewport_height})")
                # Get screenshot as PIL image
                screenshot = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
                # Calculate position to paste screenshot in stitched image
                x = col * viewport_width
                y = row * viewport_height
                # Paste screenshot into stitched image
                stitched_image.paste(screenshot, (x, y))
        # Save stitched image
        stitched_image.save('full_screenshot.png')

    def load_jquery(self):
        """
        This function loads jQuery into the current page.
        """
        self.driver.execute_script(
            """
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js';
            document.head.appendChild(script);
            """
        )


class Baseline:
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

    @staticmethod
    def solve_task(task, driver):
        screenshot = Input.take_screenshot(driver)
        full_screenshot = Input.take_full_screenshot(driver)
        html = task.get_html()

        # Add your code here to process the HTML data and generate a summary

        result = None
        return result

    # TODO: inconsistent naming: project vs. task
    @staticmethod
    def oracle_baseline(project_name, index, input_name):
        answers = Evaluation.retrieve_gold_labels(project_name, index, input_name)
        for answer in answers:
            if answer and answer != '{}':
                return answer
        return None

    def random_baseline(input_name, input_type, driver):
        input_element = driver.find_element(By.NAME, input_name)
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


def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config

# as soon as the code is loaded, we look for alignnent between the task names and their ids
task_ids = requests.get(f"{TURKLE_URL}/get_tasks/").json()

def enumerate_tasks(tasks, batch, maximum, mode, input_format, image_format):
    """
    Enumerate the tasks and their instances
    :param tasks: list of tasks
    :param batch: batch size TODO: what is this?
    :param maximum: maximum number of instances per task
    :param mode: train or test
    :param input_format: text or image. This matters for "training" mode, where we need to save the inputs on disk.
    """
    driver = webdriver.Firefox()
    # driver = webdriver.Chrome()
    actions = MyActions(driver)
    results = {}
    driver.get(TURKLE_URL)
    for project_name in tasks:
        print(" = = = = = = = = ")
        print(project_name)
        instance_ids = task_ids[project_name]
        first_instance_id = min(instance_ids)

        # if maximum is less than the number of instances, we sample a random subset of instances
        if maximum < len(instance_ids):
            # random sample
            instance_ids = random.sample(instance_ids, maximum)

        data = []

        # TODO: what is the purpose of this vs. test mode?
        if mode == 'train':
            directory = f'train/{project_name}'
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
                # evaluation = Evaluation(driver)
                if batch:
                    df = pd.read_csv(f'../tasks/{project_name}/batch.csv', nrows=0)
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
                            project_name, row_number, input['input_name']
                        )
                        actions.execute_command(input['input_type'], baseline_answer, input['input_name'])

                        data.append({
                            'input': [input['input_type'], input['input_name']],
                            'image_id': image_id,
                            'html_id': html_id,
                            'output': baseline_answer
                        })

            with open(f'{directory}/{project_name}.json', 'w') as f:
                json.dump(data, f)

        if mode == 'test':

            # Sample random instances of each task
            for instance_id in instance_ids:
                url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
                driver.get(url)
                evaluation = Evaluation()
                if batch:  # TODO: better name? Batch here means that we use the field names from HTML file. Other names: Oracle, known fields, etc.
                    df = pd.read_csv(f'../tasks/{project_name}/batch.csv', nrows=0)
                    input_names = [col.replace('Answer.', '') for col in df.columns if col.startswith('Answer.')]
                    inputs = Input.extract_input_values_from_url(url, input_names)
                else:
                    inputs = Input.extract_input_values_from_url(url)

                # TODO: write functionality to count the overall field stats.

                print("inputs: {}".format(inputs))

                for input in inputs:
                    element = driver.find_element(By.NAME, input['input_name'])
                    # make sure that the element is visible
                    print(" - - - - - - ")
                    if element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0:
                        task = Input(url, input['input_name'])
                        # baseline_answer = Baseline.solve_task(task, driver)
                        # baseline_answer = Baseline.random_baseline(i['input_name'], i['input_type'], driver)
                        row_number = instance_id - first_instance_id
                        baseline_answer = Baseline.oracle_baseline(
                            project_name,
                            row_number,
                            input['input_name']
                        )
                        actions.execute_command(
                            input['input_type'],
                            baseline_answer,
                            input['input_name']
                        )
                        score = evaluation.calculate_rouge(
                            project_name,
                            row_number,
                            input['input_type'],
                            input['input_name'],
                            baseline_answer
                        )
                        if project_name not in results:
                            results[project_name] = {}
                        if input['input_type'] not in results[project_name]:
                            results[project_name][input['input_type']] = []
                        results[project_name][input['input_type']].append(score)
                    else:
                        print(f'Skipping element {input["input_name"]} since it is not visible.')

    if mode == 'test':
        df = pd.DataFrame()
        for project_name, inputs in results.items():
            for input_type, scores in inputs.items():
                print(scores)
                avg_score = sum(scores) / len(scores)
                df = pd.concat(
                    [df, pd.DataFrame({'project': [project_name], 'input_type': [input_type], 'score': [avg_score]})],
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


if __name__ == "__main__":
    with open('../data/evaluation_tasks.txt', 'r') as f:
        tasks = f.read().splitlines()
    config = read_config('config.ini')
    batch = config.getboolean('DEFAULT', 'batch')  # TODO: what is this?
    max_instance_count = config.getint('DEFAULT', 'num')
    mode = config.get('DEFAULT', 'mode')
    input_format = config.get('DEFAULT', 'input_format')
    image_format = config.get('DEFAULT', 'image_format', fallback='full_page')
    enumerate_tasks(tasks, batch, max_instance_count, mode, input_format, image_format)
