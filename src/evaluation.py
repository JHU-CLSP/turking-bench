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

    def calculate_rouge(self, task, index, input_name, baseline_answer):
        df = pd.read_csv(f'../tasks/{task}/batch.csv')
        cols = [col for col in df.columns if not col.startswith("Answer.")]
        distinct_rows = df[cols].drop_duplicates()
        if index <= len(distinct_rows):
            ith_row = distinct_rows.iloc[[index-1]]            
            result = df[df[cols].isin(ith_row.to_dict('list')).all(axis=1)]            
            answers = result[input_name].tolist()
        else:
            answers = []
        scores = []
        for answer in answers:
            score = self.rouge.get_scores(answer, baseline_answer)[0]['rouge-1']['f']
            scores.append(score)
        avg_score = sum(scores) / len(scores)
        return avg_score


class Input:
    def __init__(self, url, input_id):
        self.task = url
        self.input_id = input_id

    def get_html(self):
        response = requests.get(self.task)
        html = response.text
        return html

    @staticmethod
    def enter_input(input_type, input_value, input_name, driver):
        try:
            if input_type == 'text' or input_type == 'textarea':
                # Wait for element to become visible
                text_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, input_name)))
                # Scroll element into view
                driver.execute_script("arguments[0].scrollIntoView();", text_box)
                action = ActionChains(driver)
                action.move_to_element(text_box)
                action.click()
                action.send_keys(input_value)
                action.perform()
                text_box.submit()
            elif input_type == 'radio' or input_type == 'checkbox':
                option = driver.find_element(f"//input[@type='{input_type}'][@value='{input_value}']")
                option.click()
            elif input_type == 'button':
                button = driver.find_element(By.NAME, input_name)
                button.click()
            elif input_type == 'color':
                color_picker = driver.find_element(By.NAME, input_name)
                color_picker.click()
                color_picker.send_keys(input_value)
            elif input_type == 'date':
                date_picker = driver.find_element(By.NAME, input_name)
                date_picker.click()
                date_picker.send_keys(input_value)
            elif input_type == 'datetime-local':
                datetime_picker = driver.find_element(By.NAME, input_name)
                datetime_picker.click()
                datetime_picker.send_keys(input_value)
            elif input_type == 'email':
                email_input = driver.find_element(By.NAME, input_name)
                email_input.click()
                email_input.send_keys(input_value)
            elif input_type == 'file':
                file_input = driver.find_element(By.NAME, input_name)
                file_input.send_keys(input_value)
            elif input_type == 'hidden':
                hidden_input = driver.find_element(By.NAME, input_name)
                hidden_input.send_keys(input_value)
            elif input_type == 'image':
                image_input = driver.find_element(By.NAME, input_name)
                image_input.click()
            elif input_type == 'month':
                month_picker = driver.find_element(By.NAME, input_name)
                month_picker.click()
                month_picker.send_keys(input_value)
            elif input_type == 'number':
                number_input = driver.find_element(By.NAME, input_name)
                number_input.click()
                number_input.send_keys(input_value)
            elif input_type == 'password':
                password_input = driver.find_element(By.NAME, input_name)
                password_input.click()
                password_input.send_keys(input_value)
            elif input_type == 'range':
                range_slider = driver.find_element(By.NAME, input_name)
                range_slider.click()
            elif input_type == 'reset':
                reset_button = driver.find_element(By.NAME, input_name)
                reset_button.click()
            elif input_type == 'search':
                search_box = driver.find_element(By.NAME, input_name)
                search_box.click()
                search_box.send_keys(input_value)
            elif input_type == 'submit':
                submit_button = driver.find_element(By.NAME, input_name)
                submit_button.click()
            elif input_type == 'tel':
                tel_input = driver.find_element(By.NAME, input_name)
                tel_input.click()
                tel_input.send_keys(input_value) 
            elif input_type == 'time':
                time_picker = driver.find_element(By.NAME, input_name) 
                time_picker.click() 
                time_picker.send_keys(input_value) 
            elif input_type == 'url': 
                url_input = driver.find_element(By.NAME, input_name) 
                url_input.click() 
                url_input.send_keys(input_value) 
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
                inputs += soup.find_all(name)
        else:
            input_names = set()
            inputs = soup.find_all(['input', 'textarea'])
        for input in inputs:
            input_type = input.get('type', 'text')
            input_name = input.get('name')
            if not input_name:
                continue
            input_values.append({'input_type': input_type, 'input_name': input_name})
        return input_values

class Baseline:
    @staticmethod
    def solve_task(task):
        screenshot = Input.take_screenshot(driver)
        full_screenshot = Input.take_full_screenshot(driver)
        html = task.get_html()

        # Add your code here to process the HTML data and generate a summary

        result = None
        return result


def find_frame_url(project_name, driver):
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
    driver = webdriver.Firefox()
    for task in tasks:
        driver.get(base_url)
        offset, instances = find_frame_url(task, driver)
        random_numbers = [random.randint(1, instances) for _ in range(min(instances, maximum))]
        for num in random_numbers:
            url = f'http://localhost:8000/task/{num+offset}/iframe/'
            driver.get(url)
            evaluation = Evaluation(driver)
            if batch:
                df = pd.read_csv(f'../tasks/{task}/batch.csv', nrows=0)
                input_names = [col.replace('Answer.', '') for col in df.columns if col.startswith('Answer.')]
                inputs = Input.extract_input_values_from_url(url,input_names)
            else:
                inputs = Input.extract_input_values_from_url(url)
            for i in inputs:
                if i['input_type'] != 'hidden':
                    task = Input(url, i['input_name'])
                    summary = Baseline.solve_task(task)
                    Input.enter_input(i['input_type'], summary, i['input_name'], driver)
                score = evaluation.calculate_rouge(task, num, i['input_name'], baseline_answer)
                print(score)

if __name__ == "__main__":
    # receive input arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--tasks', type=str,
                    help='names of the tasks (Project column of the website); separate multiple tasks with semicolons', required=True)
    parser.add_argument('--batch', type=bool, default=True, help='determine if this task has a batch or not')
    parser.add_argument('--num', type=int, default=1, help='Maximum number of instances from each task')
    args = parser.parse_args()
    tasks = args.tasks.split(';')
    batch = args.batch
    maximum = int(args.num)
    enumerate_tasks(tasks, batch, maximum)