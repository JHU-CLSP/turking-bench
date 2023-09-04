from bs4 import BeautifulSoup
import requests


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

        # exclude special inputs
        exclude_input_names = [
            'csrfmiddlewaretoken',  # hidden field automatically added external css files
            'worker_ip'  # hidden field for bookkeeping
        ]
        inputs = [input for input in inputs if input.get('name') not in exclude_input_names]

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
