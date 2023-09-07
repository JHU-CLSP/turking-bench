from colorama import Fore
import io
from io import BytesIO
from PIL import Image, ImageDraw
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import math
from evaluation.input import Input

class Result:
    """
    This class encodes the outcome of each action.
    The result may contain the following fields:
    - success: whether the action was successful
    - message: a message to be displayed to the user
    - action: the action that was performed, including the input
    """
    def __init__(self, success, outcome, action):
        self.success = success
        self.outcome = outcome
        self.action = action

    def __repr__(self):
        return f"Result(success=`{self.success}`, outcome=`{self.outcome}`, action=`{self.action}`)"

class ActionUtils:
    """
    This class contains utility functions for actions.
    """
    @staticmethod
    def xpath_string_escape(input_str):
        """ creates a concatenation of alternately-quoted strings that is always a valid XPath expression """
        parts = input_str.split("'")
        return "concat('" + "', \"'\" , '".join(parts) + "', '')"


class MyActions:
    """
    This class contains the actions that can be performed on an HTML page
    """

    def __init__(self, driver):
        """
        :param driver: selenium driver
        """
        self.driver = driver

    def execute_js_command(self, command, *args) -> Result:
        """
        Executes the javascript command and returns the result.
        """
        self.driver.execute_script(command, *args)

        return Result(success=True, outcome=None, action=f"self.execute_js_command({command})")

    def maximize_window(self) -> Result:
        """
        This function maximizes the browser window to make sure we can see all the elements on the page.
        """
        self.driver.maximize_window()

        return Result(success=True, outcome=None, action="self.maximize_window()")

    def scroll_to_element(self, input: Input) -> Result:
        """
        This function scrolls to a given element on the page, after the page is fully loaded.
        It then returns the element.
        """
        result = self.wait_for_element(input)
        input_element = result.outcome
        self.execute_js_command("arguments[0].scrollIntoView();", input_element)
        return Result(success=True, outcome=input_element, action=f"self.scroll_to_element({input})")

    def wait_for_element(self, input: Input) -> Result:
        """
        This function waits for a given element to be loaded on the page, and then returns the element.
        """
        input_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, input.name)))

        return Result(success=True, outcome=input_element, action=f"self.wait_for_element({input})")

    def modify_text(self, input: Input, input_value) -> Result:
        """
        For a given editable input field such as text box or text area, this function enters the input value into
        the input field.
        :param input_name: name of the input field
        :param input_value: value to be entered into the input field
        :return: None
        """
        if not input_value or input_value == 'nan':
            print(f"{Fore.RED}Since the input value is `{input_value}`, we are not going to modify the text.")
            return Result(success=False, outcome=None, action=f"self.modify_text({input}, {input_value})")

        result = self.scroll_to_element(input)
        input_element = result.outcome
        print(f"{Fore.YELLOW}We are going to add text to this text input: {input_element.get_attribute('outerHTML')}")

        action = ActionChains(self.driver).move_to_element(input_element).click()
        # now modify the text
        action.send_keys(input_value)
        action.perform()
        return Result(success=True, outcome=input_element, action=f"self.modify_text({input}, {input_value})")

    def modify_checkbox(self, input: Input, input_value) -> Result:
        """
        For a given checkbox, this function clicks on the specified checks.
        """

        # if input value is not string, turn it into a string
        if not isinstance(input_value, str):
            input_value = str(input_value)

        if "|" in input_value:
            input_value = input_value.split("|")
            print(f"{Fore.YELLOW} There are multiple values. Splitting them! {input_value}")

        if type(input_value) == str:
            input_value = [input_value]

        if input_value == 'nan':
            print(f"{Fore.RED} ** Warning **: input value is 'nan'. So, we're terminating the function")
            return Result(success=False, outcome=None, action=f"self.modify_checkbox({input}, {input_value})")
        elif 'nan' in input_value:
            print(f"{Fore.YELLOW} ** Warning **: Found input value is 'nan' and filtered it out")
            input_value = [v for v in input_value if v != 'nan']
            if len(input_value) == 0:
                print(f"{Fore.RED} ** Warning **: Since the list of values `{input_value}` is empty, "
                      f"and so, we're terminating the function")
                return Result(success=False, outcome=None, action=f"self.modify_checkbox({input}, {input_value})")

        self.wait_for_element(input)
        self.scroll_to_element(input)

        print(f"{Fore.YELLOW}Looking for checkboxes with `name`: {input}  the following values: {input_value}")

        assert type(input_value) == list, f"Input value `{input_value}` is not a list"

        # now we have to check the checkboxes that have the values we want
        for value in input_value:
            # Find the checkbox that has the given value and click on it
            # TODO: need to escape the following parameters
            checkbox = self.driver.find_element(
                By.XPATH,
                f"//input[@type='checkbox' and @name='{input.name}' and @value='{value}']"
            )
            print(f"{Fore.YELLOW}About to check this checkbox: {checkbox.get_attribute('outerHTML')}")
            checkbox.click()

        return Result(success=True, outcome=None, action=f"self.modify_checkbox({input}, {input_value})")

    def modify_radio(self, input: Input, input_value) -> Result:
        """
        For a given radio button, this function clicks on the specified radio button.
        """
        # if input value is double/float, turn it into an integer
        if isinstance(input_value, float):
            input_value = int(input_value)

        # if input value is not string, turn it into a string
        if not isinstance(input_value, str):
            input_value = str(input_value)

        if input_value in ['nan', 'None']:
            print(f"{Fore.RED} ** Warning **: input value is {input_value}. "
                  f"So, we're not going to modify the radio button.")
            return Result(success=False, outcome=None, action=f"self.modify_radio({input}, {input_value})")

        self.scroll_to_element(input)
        value = f"@value='{input_value}'"
        if "'" in input_value and '"' in input_value:
            value = f'@value=`{input_value}`'
        elif "'" in input_value:
            value = f'@value="{input_value}"'

        element = self.driver.find_element(
            By.XPATH, f"//input[@type='radio' and @name='{input.name}' and {value}]"
        )

        # print element in HTML format
        print(f"{Fore.YELLOW}We are going to select this radio button: {element.get_attribute('outerHTML')}")

        action = ActionChains(self.driver).move_to_element(element).click()
        action.perform()

        return Result(success=True, outcome=None, action=f"self.modify_radio({input.name}, {input_value})")

    def modify_select(self, input: Input, input_value) -> Result:
        """
        For a given select field (dropdown menu), this function selects the specified option.
        """
        # input_element = self.scroll_to_element(input_name)
        select = Select(self.driver.find_element(By.NAME, input.name))

        assert len(select.options) > 0, f"Select field {input.name} has no options"

        # get the values of the options
        option_values = [option.get_attribute('value') for option in select.options]
        assert input_value in option_values, \
            f"Input value `{input_value}` is not among the available option values `{option_values}`"

        # select by value
        select.select_by_value(input_value)

        return Result(success=True, outcome=None, action=f"self.modify_select({input}, {input_value})")

    def execute_command(self, input: Input, input_value) -> Result:
        """
        For a given input field, this function enters the input value into the input field.
        :param input_type: type of the input field
        :param input_value: value to be entered into the input field
        :param input_name: name of the input field
        :return: None
        """
        # TODO: I think this function can be folded inside the oracle baseline class
        print(f" --> Input name: {input.name}")
        print(f" --> Input value: {input_value}")

        self.wait_for_element(input)
        # wait 0.1 sec for the page to fully load
        sleep(0.1)
        self.maximize_window()
        result = self.scroll_to_element(input)
        input_element = result.outcome

        if input.type in ['text', 'textarea', 'password', 'email', 'number', 'tel', 'url']:
            self.modify_text(input, input_value)

        elif input.type in ['checkbox']:
            if not input_element.is_selected():
                return self.modify_checkbox(input, input_value)

        elif input.type in ['radio']:
            if not input_element.is_selected():
                return self.modify_radio(input, input_value)

        elif input.type == 'select':
            return self.modify_select(input, input_value)

        elif input.type in ['button', 'color', 'date', 'datetime-local', 'file', 'hidden', 'image',
                            'month', 'range', 'reset', 'search', 'submit', 'time']:
            print(f"{Fore.RED} ** Warning **: We don't know how to handle this input type `{input.type}`")
            return Result(success=False, outcome=None, action=None)

    def take_screenshot(self) -> Result:
        """
        This function takes a screenshot of the entire page that is currently visible. It then saves the screenshot.
        # TODO figure out how this function is different than other screenshot functions
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
        return Result(success=True, outcome=None, action="self.take_screenshot()")


    def take_element_screenshot(self, input: Input) -> Result:
        """
        This function takes a screenshot of a given element on the page.
        """
        # find the element based on input name and type
        if input.type in ['select', 'textarea']:
            element = Select(self.driver.find_element(By.NAME, input.name)).first_selected_option
        else:
            element = self.driver.find_element(By.NAME, input.name)
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
        return Result(success=True, outcome=cropped_image, action=f"self.take_element_screenshot({input})")

    def take_element_screenshot_with_border(self, input: Input) -> Result:
        """
        This function takes a screenshot of the entire page and draws a red border around the specified element.
        """

        # find the element based on input name and type
        if input.type in ['select', 'textarea']:
            element = Select(self.driver.find_element(By.NAME, input.name)).first_selected_option
        else:
            element = self.driver.find_element(By.NAME, input.name)

        # get the location and size of the element
        location = element.location
        size = element.size

        # scroll to the element and wait for it to be visible
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(1)

        # take a screenshot of the entire page
        screenshot = self.driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        # draw a red border around the element
        draw = ImageDraw.Draw(image)
        draw.rectangle((location['x'], location['y'],
                        location['x'] + size['width'],
                        location['y'] + size['height']), outline='red')

        return Result(success=True, outcome=image, action=f"self.take_element_screenshot_with_border({input})")

    def take_page_screenshots(self) -> Result:
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

        return Result(success=True, outcome=screenshots, action="self.take_page_screenshots()")

    def take_full_screenshot(self) -> Result:
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
        return Result(success=True, outcome=stitched_image, action="self.take_full_screenshot()")

    def load_jquery(self) -> Result:
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
        return Result(success=True, outcome=None, action="self.load_jquery()")

    def get_html(self, url):
        response = requests.get(url)
        html = response.text
        return html

    # TOOD I think we need to create a function that reads strings (Python code) and executes them via Pythin interpretor
