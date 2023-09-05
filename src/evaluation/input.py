import requests


class Input:
    def __init__(self, url, input_name, input_type, task_name):
        self.url = url
        self.name = input_name
        self.task = task_name
        self.type = input_type

    def get_html(self):
        response = requests.get(self.url)
        html = response.text
        return html
