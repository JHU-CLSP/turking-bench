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


class Evaluation:
    def __init__(self, rouge):
        self.rouge = Rouge()

    def calculate_rouge(self, project_name, index, input_type, input_name, baseline_answer):
        baseline_answer = str(baseline_answer)
        df = pd.read_csv(f'../tasks/{project_name}/batch.csv')
        cols = [col for col in df.columns if not col.startswith("Answer.")]
        distinct_rows = df[cols].drop_duplicates()
        if index <= len(distinct_rows):
            ith_row = distinct_rows.iloc[[index-1]]            
            result = df[df[cols].isin(ith_row.to_dict('list')).all(axis=1)]            
            answers = result[f'Answer.{input_name}'].tolist()
        else:
            answers = []
        
        if input_type in ['text', 'textarea']:
            scores = self.rouge.get_scores([str(answer) for answer in answers], [baseline_answer] * len(answers))
            if scores:
                max_score = max([score['rouge-1']['f'] for score in scores])
                return max_score
            else:
                return 0.0
        else:
            votes = {}
            for answer in answers:
                if answer in votes:
                    votes[answer] += 1
                else:
                    votes[answer] = 1
            majority_answer = max(votes, key=votes.get)
            majority_answer_str = str(majority_answer)
            scores = self.rouge.get_scores([majority_answer_str], [baseline_answer])
            return scores[0]['rouge-1']['f']

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
            input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, input_name)))
            driver.execute_script("arguments[0].scrollIntoView();", input_element)
            action = ActionChains(driver).move_to_element(input_element).click()
            if input_type in ['text', 'textarea', 'password', 'email', 'number', 'tel', 'url']:
                action.send_keys(input_value)
            elif input_type in ['checkbox', 'radio']:
                if not input_element.is_selected():
                    action.click()
            elif input_type == 'select':
                select = Select(input_element)
                select.select_by_visible_text(input_value)
            elif input_type in ['button', 'color', 'date', 'datetime-local', 'file', 'hidden', 'image', 'month', 'range', 'reset', 'search', 'submit', 'time']:
                pass 
            action.perform()
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"We have a problem with '{input_name}'")
            print(input_value)

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

    def get_element_screenshot(driver, input_name, input_type):
    # find the element based on input name and type
        if input_type in ['select', 'textarea']:
            element = Select(driver.find_element(By.NAME, input_name)).first_selected_option
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

    def get_element_screenshot_with_border(driver, input_name, input_type):
        # find the element based on input name and type
        if input_type in ['select', 'textarea']:
            element = Select(driver.find_element(By.NAME, input_name)).first_selected_option
        else:
            element = driver.find_element(By.NAME, input_name)

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
        draw.rectangle((location['x'], location['y'], location['x']+size['width'], location['y']+size['height']), outline='red')

        return image

    def get_page_screenshots(driver):
        screenshots = []

        # get the size of the window
        window_size = driver.execute_script("return [window.innerWidth, window.innerHeight];")

        # get the height of the entire page
        page_height = driver.execute_script("return document.documentElement.scrollHeight")

        # set the initial scroll position to the top
        scroll_position = 0

        while scroll_position < page_height:
            # take a screenshot of the current view
            screenshot = driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            screenshots.append(image)

            # scroll down to the next view
            scroll_position += window_size[1]
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        return screenshots

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
                input = soup.find(attrs={'name': name})
                if input and input.name in ['input', 'select','textarea']:
                    inputs.append(input)
        else:
            input_names = set()
            inputs = soup.find_all(['input', 'textarea', 'select'])
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
            input_values.append({'input_type': input_type, 'input_name': input_name})
        return sorted(input_values, key=lambda x: str(soup).index(str(soup.find(attrs={'name': x['input_name']}))))

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
                options = [(start_datetime + timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M') for i in range(int(minutes_diff) + 1)]
            return random.choice(options)


def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config

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


def enumerate_tasks(tasks, batch, maximum, mode, html_type, input_format, image_format):
    base_url = "http://localhost:8000"
    driver = webdriver.Firefox()
    #driver = webdriver.Chrome()
    results = {}
    for project_name in tasks:
        print(project_name)
        driver.get(base_url)
        offset, instances = find_task_id(project_name, driver)
        random_numbers = [random.randint(1, instances) for _ in range(min(instances, maximum))]
        data = []
        
        if mode =='train':
            directory = f'train/{project_name}'
            if not os.path.exists(directory):
                os.makedirs(directory)

            images_directory = f'{directory}/images'
            if not os.path.exists(images_directory):
                os.makedirs(images_directory)

            html_directory = f'{directory}/HTML'
            if not os.path.exists(html_directory):
                os.makedirs(html_directory)

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

                        if input_format== 'image' or 'both':
                            if image_format == 'full_page':
                                task_image = Input.get_page_screenshots(driver)
                            elif image_format == 'div':
                                task_image = Input.get_element_screenshot(driver, i['input_name'], i['input_type'])
                            elif image_format == 'bordered_div':
                                task_image = Input.get_element_screenshot_with_border(driver, i['input_name'], i['input_type'])

                            if isinstance(task_image, list):
                                img_ids = []
                                for j, image in enumerate(task_image):
                                    image_id = f'{num}_{i["input_name"]}_{j}.png'
                                    image.save(f'{images_directory}/{image_id}')
                                    img_ids.append(image_id)
                                image_id = img_ids
                            else:
                                image_id = f'{num}_{i["input_name"]}.png'
                                task_image.save(f'{images_directory}/{image_id}')
                        else:
                            image_id = None

                        html_id = f'{num}_{i["input_name"]}.html'
                        with open(f'{html_directory}/{html_id}', 'w') as f:
                            f.write(driver.page_source)

                        baseline_answer = Baseline.oracle_baseline(project_name, num, i['input_name'])
                        Input.enter_input(i['input_type'], baseline_answer, i['input_name'], driver)

                        data.append({
                            'input': [i['input_type'], i['input_name']],
                            'image_id' : image_id,
                            'html_id' : html_id,
                            'output': baseline_answer
                        })

            with open(f'{directory}/{project_name}.json', 'w') as f:
                json.dump(data, f)

        if mode =='test':
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
                    element = driver.find_element(By.NAME, i['input_name'])
                    if element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0:
                        task = Input(url, i['input_name'])
                        #baseline_answer = Baseline.solve_task(task, driver)
                        #baseline_answer = Baseline.random_baseline(i['input_name'], i['input_type'], driver)
                        baseline_answer = Baseline.oracle_baseline(project_name, num, i['input_name'])
                        Input.enter_input(i['input_type'], baseline_answer, i['input_name'], driver)
                        score = evaluation.calculate_rouge(project_name, num, i['input_type'], i['input_name'], baseline_answer)
                        if project_name not in results:
                            results[project_name] = {}
                        if i['input_type'] not in results[project_name]:
                            results[project_name][i['input_type']] = []
                        results[project_name][i['input_type']].append(score)
    if mode =='test':
        df = pd.DataFrame()
        for project_name, inputs in results.items():
            for input_type, scores in inputs.items():
                avg_score = sum(scores) / len(scores)
                df = pd.concat([df, pd.DataFrame({'project': [project_name], 'input_type': [input_type], 'score': [avg_score]})], ignore_index=True)

        if 'project' not in df.columns:
            df.insert(0, 'project', '')
        if 'input_type' not in df.columns:
            df.insert(1, 'input_type', '')
        if 'score' not in df.columns:
            df.insert(1, 'score', '')

        df = df.pivot(index='project', columns='input_type', values='score')
        df.to_csv('baseline_scores.csv', index=True)

if __name__ == "__main__":
    with open('../test.txt', 'r') as f:
        tasks = f.read().splitlines()
    config = read_config('config.ini')
    batch = config.getboolean('DEFAULT', 'batch')
    maximum = config.getint('DEFAULT', 'num')
    mode = config.get('DEFAULT', 'mode')
    html_type = config.get('DEFAULT', 'html_type')
    input_format = config.get('DEFAULT', 'input_format')
    image_format = config.get('DEFAULT', 'image_format', fallback='full_page')
    enumerate_tasks(tasks, batch, maximum, mode, html_type, input_format, image_format)