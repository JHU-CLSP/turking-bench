import csv
import argparse
import os
from rouge import Rouge
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from time import sleep
from PIL import Image
from io import BytesIO
import math
import pandas as pd
import random


class Evaluation:
    def __init__(self, rouge):
        self.rouge = Rouge()

    def calculate_rouge(self, project_name, index, input_name, baseline_answer):
        df = pd.read_csv(f'../tasks/{project_name}/batch.csv')
        cols = [col for col in df.columns if not col.startswith("Answer.")]
        distinct_rows = df[cols].drop_duplicates()
        if index <= len(distinct_rows):
            ith_row = distinct_rows.iloc[[index-1]]            
            result = df[df[cols].isin(ith_row.to_dict('list')).all(axis=1)]            
            answers = result[f'Answer.{input_name}'].tolist()
        else:
            answers = []
        scores = []
        for answer in answers:
            score = self.rouge.get_scores(answer, baseline_answer)[0]['rouge-1']['f']
            scores.append(score)
        avg_score = sum(scores) / len(scores)
        return avg_score


class Input:
    def __init__(self, url, input_name):
        self.url = url
        self.input_name = input_name

    def get_html(self):
        response = requests.get(self.url)
        html = response.text
        return html

    @staticmethod
    def enter_input(input_type, input_value, input_name, driver):
        try:
            driver.maximize_window()            
            if input_type in ['text', 'textarea']:
                text_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, input_name)))
                driver.execute_script("arguments[0].scrollIntoView();", text_box)
                action = ActionChains(driver)
                action.move_to_element(text_box)
                action.click()
                action.send_keys(input_value)
                action.perform()
                text_box.submit()
            elif input_type in ['button', 'checkbox', 'color', 'date', 'datetime-local', 'email', 'file', 'hidden', 'image', 'month', 'number', 'password', 'radio', 'range', 'reset', 'search', 'submit', 'tel', 'time', 'url']:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, input_name)))
                input_element = driver.find_element(By.NAME, input_name)
                action = ActionChains(driver)
                if input_type in ['button', 'checkbox', 'color', 'date', 'datetime-local', 'email', 'image', 'month', 'number', 'password', 'radio', 'range', 'reset', 'search', 'submit', 'tel', 'time']:
                    action.move_to_element(input_element)
                    action.click()
                if input_type in ['color', 'date', 'datetime-local', 'email', 'file', 'hidden', 'month', 'number', 'password', 'search', 'tel']:
                    action.send_keys(input_value)
                action.perform()
        except:
            print(f"We have a problem with '{input_name}'")

    def take_screenshot(driver):
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # Take screenshot
        driver.save_screenshot('screenshot.png')

    def take_full_screenshot(driver):
        # Get dimensions of webpage
        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        # Calculate number of rows and columns needed to capture entire webpage
        rows = math.ceil(total_height / viewport_height)
        cols = math.ceil(total_width / viewport_width)
        # Initialize stitched image
        stitched_image = Image.new('RGB', (total_width, total_height))
        for row in range(rows):
            for col in range(cols):
                # Scroll to current row and column
                driver.execute_script(f"window.scrollTo({col * viewport_width}, {row * viewport_height})")
                # Get screenshot as PIL image
                screenshot = Image.open(BytesIO(driver.get_screenshot_as_png()))
                # Calculate position to paste screenshot in stitched image
                x = col * viewport_width
                y = row * viewport_height
                # Paste screenshot into stitched image
                stitched_image.paste(screenshot, (x, y))
        # Save stitched image
        stitched_image.save('full_screenshot.png')

    @staticmethod
    def extract_input_values_from_url(url, input_names=None):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        input_values = []
        if input_names:
            input_names = set(input_names)
            inputs=[]
            for name in input_names:
                inputs.append(soup.find(attrs={'name': name}))
        else:
            input_names = set()
            inputs = soup.find_all(['input', 'textarea'])
        for input in inputs:
            input_type = input.get('type')
            if not input_type:
                input_type = 'text'
            input_name = input.get('name')
            if not input_name:
                continue
            input_values.append({'input_type': input_type, 'input_name': input_name})
        return input_values

class Baseline:
    @staticmethod
    def solve_task(task, driver):
        screenshot = Input.take_screenshot(driver)
        full_screenshot = Input.take_full_screenshot(driver)
        html = task.get_html()

        # Add your code here to process the HTML data and generate a summary

        result = None
        return result

    def oracle_baseline(project_name, index, input_name):
        df = pd.read_csv(f'../tasks/{project_name}/batch.csv')
        cols = [col for col in df.columns if not col.startswith("Answer.")]
        distinct_rows = df[cols].drop_duplicates()
        if index <= len(distinct_rows):
            ith_row = distinct_rows.iloc[[index-1]]            
            result = df[df[cols].isin(ith_row.to_dict('list')).all(axis=1)]            
            answers = result[f'Answer.{input_name}'].tolist()
            for answer in answers:
                if answer and answer != {}:
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
                options = [(start_datetime + timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M') for i in range(int(minutes_diff) + 1)]
            return random.choice(options)


def find_task_id(project_name, driver):
    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    sum_of_tasks = 0
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) > 0:
            if cells[0].text == project_name:
                instances = int(cells[3].text)
                break
            sum_of_tasks += int(cells[3].text)
    return sum_of_tasks, instances

def enumerate_tasks(tasks, batch, maximum):
    base_url = "http://localhost:8000"
    #driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    for project_name in tasks:
        driver.get(base_url)
        offset, instances = find_task_id(project_name, driver)
        random_numbers = [random.randint(1, instances) for _ in range(min(instances, maximum))]
        for num in random_numbers:
            url = f'http://localhost:8000/task/{num+offset}/iframe/'
            driver.get(url)
            evaluation = Evaluation(driver)
            if batch:
                df = pd.read_csv(f'../tasks/{project_name}/batch.csv', nrows=0)
                input_names = [col.replace('Answer.', '') for col in df.columns if col.startswith('Answer.')]
                inputs = Input.extract_input_values_from_url(url,input_names)
            else:
                inputs = Input.extract_input_values_from_url(url)
            for i in inputs:
                if i['input_type'] != 'hidden':
                    task = Input(url, i['input_name'])
                    baseline_answer = Baseline.solve_task(task, driver)
                    #baseline_answer = Baseline.oracle_baseline(project_name, num, i['input_name'])
                    #baseline_answer = Baseline.random_baseline(i['input_name'], i['input_type'], driver)
                    Input.enter_input(i['input_type'], baseline_answer, i['input_name'], driver)
                score = evaluation.calculate_rouge(project_name, num, i['input_name'], baseline_answer)
                print(score)
            

if __name__ == "__main__":
    with open('../test.txt', 'r') as f:
        tasks = f.read().splitlines()
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=bool, default=True, help='determine if this task has a batch or not')
    parser.add_argument('--num', type=int, default=1, help='Maximum number of instances from each task')
    args = parser.parse_args()
    batch = args.batch
    maximum = int(args.num)
    enumerate_tasks(tasks, batch, maximum)