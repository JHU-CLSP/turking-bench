import csv
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

class Evaluation:
    def __init__(self, rouge):
        self.rouge = Rouge()
    
    def calculate_rouge(self, n, input_name, baseline_answer):
        # TBD
        df = pd.read_csv('batch.csv')
        start_index = (n * 3) - 1       
        answers = []
        for i in range(3):
            answer = self.df.iloc[start_index+i][f'Answer.{input_name}']
            answers.append(answer)
        
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
                option = driver.find_element_by_xpath(f"//input[@type='{input_type}'][@value='{input_value}']")
                option.click()
        except NoSuchElementException:
            print(f"Element with name '{input_name}' not found")

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
    def extract_input_values_from_url(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        inputs = soup.find_all(['input', 'textarea'])
        input_values = []
        input_names = set()
        for input in inputs:
            input_type = input.get('type')
            if not input_type:
                input_type = 'text'
            input_name = input.get('name')
            if not input_name or input_name in input_names:
                continue
            input_values.append({'input_type': input_type, 'input_name': input_name})
            input_names.add(input_name)
        return input_values

class Baseline:
    @staticmethod
    def solve_task(task):
        html = task.get_html()

        # Add your code here to process the HTML data and generate a summary

        result = None
        return result

def main(url):
    driver = webdriver.Firefox()
    driver.get(url)
    evaluation = Evaluation(driver)
    inputs = Input.extract_input_values_from_url(url)
    screenshot= Input.take_screenshot(driver)
    full_screenshot= Input.take_full_screenshot(driver)
    print(inputs)
    for i in inputs:
        if i['input_type'] != 'hidden':
            task = Input(url, i['input_name'])
            summary = Baseline.solve_task(task)
            Input.enter_input(i['input_type'], summary, i['input_name'], driver)
    
    scores = evaluation.enumerate(task)
    print(scores)

main(url)