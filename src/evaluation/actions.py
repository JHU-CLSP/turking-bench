from colorama import Fore
import io
from io import BytesIO
from openai import OpenAI
import os
import numpy as np
from PIL import Image, ImageDraw
import re
import requests
import platform
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
import math
from evaluation.input import Input


class ActionUtils:
    """
    This class contains utility functions for actions.
    """

    @staticmethod
    def xpath_string_escape(input_str):
        """ creates a concatenation of alternately-quoted strings that is always a valid XPath expression """
        parts = input_str.split("'")
        return "concat('" + "', \"'\" , '".join(parts) + "', '')"

    @staticmethod
    def is_float(element: any) -> bool:
        # If you expect None to be passed:
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    @staticmethod
    def clear_text(action: ActionChains):
        key = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

        # Perform Ctrl+A (select all)
        action.key_down(key).send_keys('a').key_up(key)
        # Perform Delete
        action.send_keys(Keys.BACKSPACE)

    client = None

    @staticmethod
    def openai_call(prompt):

        if not ActionUtils.client:
            # read it from environment variable
            key = os.environ.get('OPENAI_API_KEY')
            client = OpenAI(api_key=key)

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content


class MyActions:
    """
    This class contains the actions that can be performed on an HTML page
    """

    def __init__(self, driver):
        """
        :param driver: selenium driver
        """
        self.driver = driver

        # scrolss to the element but keeps it in the center of the screen
        self.scroll_to_command = "arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });"

    def execute_js_command(self, command, *args) -> str:
        """
        Executes the javascript command and returns the result.
        """
        outcome = self.driver.execute_script(command, *args)

        return f"self.actions.execute_js_command('{command}')"

    def maximize_window(self) -> str:
        """
        This function maximizes the browser window to make sure we can see all the elements on the page.
        """
        self.driver.maximize_window()

        return "self.maximize_window()"

    def scroll_to_element(self, input_name: str):
        """
        This function scrolls to a given element on the page, after the page is fully loaded.
        It then returns the element.
        """
        _, input_element = self.wait_for_element(input_name)
        self.execute_js_command(self.scroll_to_command, input_element)
        return f"self.actions.scroll_to_element('{input_name}')", input_element

    def wait_for_element(self, input_name: str):
        """
        This function waits for a given element to be loaded on the page, and then returns the element.
        """
        input_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, input_name))
        )
        return f"self.actions.wait_for_element('{input_name}')", input_element

    def modify_text(self, input_name: str, input_value) -> str:
        """
        For a given editable input field such as text box or text area, this function enters the input value into
        the input field.
        :param input_name: name of the input field
        :param input_value: value to be entered into the input field

        For example, if the input name is `name` and the input value is `John`, then we would need to run the following to enter `John` inside this input:
        > self.modify_text("name", "John")
        """
        if not input_value or input_value == 'nan' or (
                type(input_value) == float and np.isnan(input_value)):
            print(
                f"{Fore.RED}Since the input value is `{input_value}`, we are not going to modify the text."
            )
            return f"self.actions.modify_text('{input_name}', '{input_value}')"

        _, input_element = self.scroll_to_element(input_name)
        print(f"{Fore.YELLOW}Add text `{input_value}` to this text input: {input_element.get_attribute('outerHTML')}")

        action = ActionChains(self.driver).move_to_element(input_element).click()
        # now modify the text
        ActionUtils.clear_text(action)
        for i, text in enumerate(re.split(r'[\n\r]', str(input_value))):
            if i:
                action = action.send_keys(Keys.ENTER)
            action = action.send_keys(text)
        action.perform()

        if input_element.tag_name == 'textarea':
            self.execute_js_command(
                'arguments[0].innerHTML = arguments[1]',
                input_element, input_value
            )
        elif input_element.tag_name == 'input':
            self.execute_js_command(
                'arguments[0].setAttribute("value", arguments[1])',
                input_element, input_value
            )

        return f"self.actions.modify_text('{input_name}', '{input_value}')"

    def modify_checkbox(self, input_name: str, input_value) -> str:
        """
        For a given checkbox, this function clicks on the all the correct values.
        :param input_name: name of the input field
        :param input_value: value to be entered into the input field, if we have more than one value, we separate them with `|`

        Example1: if the input name is `colors` and possible input values are `red` and `blue`, then we would need to run the following to click on the `red` and `blue` inside this input:
        > self.modify_checkbox("colors", "red|blue")
        Example2: if the input name is `visited` and the input value is `USA|Europe`, then we would click the following checkboxes USA and Europe by running the following:
        > self.modify_checkbox("visited", "USA|Europe")
        """

        original_input_value = input_value

        # if input value is not string, turn it into a string
        if not isinstance(input_value, str):
            input_value = str(input_value)

        if "|" in input_value:
            input_value = input_value.split("|")
            print(f"{Fore.YELLOW} There are multiple values. Splitting them! {input_value}")

        if type(input_value) == str:
            input_value = [input_value]

        if input_value == 'nan':
            print(
                f"{Fore.RED} ** Warning **: input value is 'nan'. So, we're terminating the function"
            )
            return f"self.actions.modify_checkbox('{input_name}', '{original_input_value}')"
        elif 'nan' in input_value:
            print(
                f"{Fore.YELLOW} ** Warning **: Found input value is 'nan' and filtered it out"
            )
            input_value = [v for v in input_value if v != 'nan']
            if len(input_value) == 0:
                print(
                    f"{Fore.RED} ** Warning **: Since the list of values `{input_value}` is empty, "
                    f"and so, we're terminating the function")
                return f"self.actions.modify_checkbox('{input_name}', '{original_input_value}')"

        self.wait_for_element(input_name)
        self.scroll_to_element(input_name)

        print(f"{Fore.YELLOW}Looking for checkboxes with `name`: `{input_name}` the values: `{input_value}`")

        assert type(input_value) == list, f"Input value `{input_value}` is not a list"

        # now we have to check the checkboxes that have the values we want
        # TODO: need to escape the following parameters
        checkboxes = self.driver.find_elements(
            By.XPATH, f"//input[@type='checkbox' and @name='{input_name}']")

        # TODO: if this is not useful, let's drop it.
        # for single-checkbox inputs, we need to apply "on" or "off" to the checkbox
        # if len(checkboxes) == 1 and input_value[0] in ['on', 'off']:
        #     print(f"{Fore.YELLOW}About to check this checkbox: {checkboxes[0].get_attribute('outerHTML')}")
        #     if input_value[0] == 'on':
        #         checkboxes[0].click()
        #         self.execute_js_command(
        #             'arguments[0].setAttribute("checked", "");', checkboxes[0]
        #         )
        # else:
        for checkbox in checkboxes:
            if checkbox.get_attribute("value") in input_value:
                print(
                    f"{Fore.YELLOW}About to check this checkbox: {checkbox.get_attribute('outerHTML')}"
                )
                checkbox.click()
                self.execute_js_command(
                    'arguments[0].setAttribute("checked", "");', checkbox)

        return f"self.actions.modify_checkbox('{input_name}', '{original_input_value}')"

    def modify_radio(self, input_name: str, input_value) -> str:
        """
        For a given radio button, this function clicks on the correct radio button.
        :param input_name: name of the input field
        :param input_value: which radio button based on the value of the radio button
        
        Example1: if the input name is `reasonability` and the desired input value is `yes`, then we would need to run the following to click on the `yes` radio button:
        > self.modify_radio("reasonability", "yes")
        Example2: if the input name is `year` and the input value is `2025`, then we select the radio button with value `2025` by running the following:
        > self.modify_radio("year", "2025")
        """
        # if input value is double/float, turn it into an integer
        if isinstance(input_value, float):
            if np.isnan(input_value):
                print(
                    f"{Fore.RED} ** Warning **: input value is {input_value}. "
                    f"So, we're not going to modify the radio button.")
                return f"self.actions.modify_radio('{input_name}', '{input_value}')"
            else:
                input_value = int(input_value)

        # if input value is not string, turn it into a string
        if not isinstance(input_value, str):
            input_value = str(input_value)

        if input_value in ['nan', 'None']:
            print(f"{Fore.RED} ** Warning **: input value is {input_value}. "
                  f"So, we're not going to modify the radio button.")
            return f"self.actions.modify_radio('{input_name}', '{input_value}')"

        self.scroll_to_element(input_name)
        value = f"@value='{input_value}'"
        if "'" in input_value and '"' in input_value:
            value = f'@value=`{input_value}`'
        elif "'" in input_value:
            value = f'@value="{input_value}"'

        element = None
        try:
            element = self.driver.find_element(
                By.XPATH,
                f"//input[@type='radio' and @name='{input_name}' and {value}]")
        except:
            # if the value is double/float, turn it into an integer and retry
            print(f"The input value (`{input_value}`, {type(input_value)}) not found. ")
            # if isinstance(input_value, float):
            if input_value == "":
                print(f"{Fore.RED} ** Warning **: input value is {input_value}. "
                    f"So, we're not going to modify the radio button.")
                return f"self.actions.modify_radio('{input_name}', '{input_value}')"

            elif type(input_value) == str and re.match("^[-+]?[0-9]*\.?[0-9]+$", input_value) is not None:
                input_value = int(float(input_value))
                value = f"@value='{input_value}'"
                element = self.driver.find_element(
                    By.XPATH,
                    f"//input[@type='radio' and @name='{input_name}' and {value}]"
                )

        # print element in HTML format
        print(f"{Fore.YELLOW}We are going to select this radio button: {element.get_attribute('outerHTML')}")

        # is this element visible?
        if element.is_displayed():
            action = ActionChains(self.driver).move_to_element(element).click()
            action.perform()
        else:
            print(f"{Fore.RED} ** Warning **: element is not visible. "
                  f"So, we're not going to modify the radio button.")

        self.execute_js_command('arguments[0].setAttribute("checked", "");', element)

        return f"self.actions.modify_radio('{input_name}', '{input_value}')"

    def modify_select(self, input_name: str, input_value) -> str:
        """
        For a given select field (dropdown menu), this function selects the specified option.
        :param input_name: name of the input field
        :param input_value: which select option to choose based on the value of the select

        Example1: if the input name is `question1` and the desired input value is `option2`, then we would need to run the following to select the `option2`:
        > self.modify_select("question1", "option2")        
        Example2: if the input name is `cars` and the input value is `Audi`, then we select the option with value `Audi` by running the following:
        > self.modify_select("cars", "Audi")
        """
        # input_element = self.scroll_to_element(input_name)
        select_element = self.driver.find_element(By.NAME, input_name)
        select = Select(select_element)

        assert len(select.options) > 0, f"Select field {input_name} has no options"

        # get the values of the options
        option_values = [
            option.get_attribute('value') for option in select.options
        ]
        if input_value in option_values:
            # great ... continue!
            pass
        elif ActionUtils.is_float(input_value) and not math.isnan(
                float(input_value)) and str(int(float(input_value))) in option_values:
            # input value is a float, but the option values are integers
            input_value = str(int(float(input_value)))
        else:
            raise Exception(
                f"Input value `{input_value}` is not among the available option values `{option_values}`"
            )

        # select by value
        print(f"{Fore.YELLOW}We are going to select this select `{input_name}` with value `{input_value}`")
        select.select_by_value(input_value)
        self.execute_js_command('arguments[0].setAttribute("selected", "");',
                                select.first_selected_option)

        return f"self.actions.modify_select('{input_name}', '{input_value}')"

    def modify_range(self, input_name: str, input_value) -> str:
        """
        For a given "range" input, this function clicks on the specified range value.
        :param input_name: name of the input field
        :param input_value: which range value to end up on 

        Example1: if the input name is `satisfactory` and the desired input value is `12`, then we would need to run the following to click on the `12`:
        > self.modify_range("satisfactory", "12")
        Example2: if the input name is `volume` and the input value is `20`, then we get the range to `20` by running the following:
        > self.modify_range("volume", "20")
        """
        # if input value is double/float, turn it into an integer
        # if isinstance(input_value, float):
        #     input_value = int(input_value)

        # if input value is not string, turn it into a string
        # if not isinstance(input_value, str):
        #     input_value = str(input_value)

        if input_value in ['nan', 'None']:
            print(f"{Fore.RED} ** Warning **: input value is {input_value}. "
                  f"So, we're not going to modify the range.")
            return f"self.actions.modify_range('{input_name}', '{input_value}')"

        self.scroll_to_element(input_name)
        # value = f"@value='{input_value}'"
        # if "'" in input_value and '"' in input_value:
        #     value = f'@value=`{input_value}`'
        # elif "'" in input_value:
        #     value = f'@value="{input_value}"'

        element = self.driver.find_element(
            By.XPATH, f"//input[@type='range' and @name='{input_name}']")

        # print element in HTML format
        print(
            f"{Fore.YELLOW}We are going to set the value of {element.get_attribute('outerHTML')} to {input_value}"
        )

        # set the value to the input value
        self.driver.execute_script(
            f"""
            arguments[0].value = {input_value};
            arguments[0].setAttribute('value', {input_value});""", element)

        return f"self.actions.modify_range('{input_name}', '{input_value}')"

    def take_screenshot(self) -> str:
        """
        This function takes a screenshot of the entire page that is currently visible. It then saves the screenshot.
        # TODO figure out how this function is different than other screenshot functions
        """
        # Get scroll height
        last_height = self.execute_js_command(
            "return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(0.2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Take screenshot
        self.driver.save_screenshot('screenshot.png')
        return "self.take_screenshot()"

    def take_element_screenshot(self, input_name: str) -> str:
        """
        This function takes a screenshot of a given element on the page.
        """

        # find the element based on input name
        element = self.driver.find_element(By.NAME, input_name)

        # get the location and size of the element
        location = element.location
        size = element.size

        # take a screenshot of the entire page
        screenshot = self.driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        # crop the image to the size of the element
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        cropped_image = image.crop((left, top, right, bottom))
        return f"self.actions.take_element_screenshot('{input_name}')"

    def take_element_screenshot_with_border(self, input_name: str) -> str:
        """
        This function takes a screenshot of the entire page and draws a red border around the specified element.
        """

        # find the element based on input name
        element = self.driver.find_element(By.NAME, input_name)

        # get the location and size of the element
        location = element.location
        size = element.size

        # scroll to the element and wait for it to be visible
        self.driver.execute_script(self.scroll_to_command, element)
        sleep(0.2)

        # take a screenshot of the entire page
        screenshot = self.driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        # draw a red border around the element
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (location['x'], location['y'], location['x'] + size['width'],
             location['y'] + size['height']),
            outline='red')

        return f"self.actions.take_element_screenshot_with_border('{input_name}')"

    def take_page_screenshots(self) -> str:
        """
        This function takes a screenshot of the entire page by scrolling down the page and taking a screenshot of each
        """
        screenshots = []

        # get the size of the window
        window_size = self.driver.execute_script(
            "return [window.innerWidth, window.innerHeight];")

        # get the height of the entire page
        page_height = self.driver.execute_script(
            "return document.documentElement.scrollHeight")

        # set the initial scroll position to the top
        scroll_position = 0

        while scroll_position < page_height:
            # take a screenshot of the current view
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            screenshots.append(image)

            # scroll down to the next view
            scroll_position += window_size[1]
            self.driver.execute_script(
                f"window.scrollTo(0, {scroll_position});")

        return "self.take_page_screenshots()"

    def take_full_screenshot(self) -> str:
        """
        This function takes a screenshot of the entire page by stitching together screenshots of each view.
        """
        # Get dimensions of webpage
        total_width = self.driver.execute_script(
            "return document.body.offsetWidth")
        total_height = self.driver.execute_script(
            "return document.body.parentNode.scrollHeight")
        viewport_width = self.driver.execute_script(
            "return document.body.clientWidth")
        viewport_height = self.driver.execute_script(
            "return window.innerHeight")
        # Calculate number of rows and columns needed to capture entire webpage
        rows = math.ceil(total_height / viewport_height)
        cols = math.ceil(total_width / viewport_width)
        # Initialize stitched image
        stitched_image = Image.new('RGB', (total_width, total_height))
        for row in range(rows):
            for col in range(cols):
                # Scroll to current row and column
                self.driver.execute_script(
                    f"window.scrollTo({col * viewport_width}, {row * viewport_height})"
                )
                # Get screenshot as PIL image
                screenshot = Image.open(
                    BytesIO(self.driver.get_screenshot_as_png()))
                # Calculate position to paste screenshot in stitched image
                x = col * viewport_width
                y = row * viewport_height
                # Paste screenshot into stitched image
                stitched_image.paste(screenshot, (x, y))
        # Save stitched image
        stitched_image.save('full_screenshot.png')
        return "self.take_full_screenshot()"

    def load_jquery(self) -> str:
        """
        This function loads jQuery into the current page.
        """
        self.driver.execute_script("""
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js';
            document.head.appendChild(script);
            """)
        return "self.load_jquery()"

    def get_html(self, url):
        response = requests.get(url)
        html = response.text
        return html
