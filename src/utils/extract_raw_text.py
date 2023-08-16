"""
This file extracts raw text from instructions and saves them to disk.
We used the raw text to compare the tasks and make sure that the eval. vs. train tasks are different from each other.
"""

from bs4 import BeautifulSoup
import re
import os
import chardet


def extract_text_from_html(html_file):
    with open(html_file, 'rb') as f:
        rawdata = f.read()
    encoding = chardet.detect(rawdata)['encoding']
    with open(html_file, 'r', encoding=encoding) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text)
    return text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(text)


for root, dirs, files in os.walk('tasks'):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        for file in os.listdir(dir_path):
            if file.endswith('.html'):
                html_file_path = os.path.join(dir_path, file)
                print(html_file_path)
                extracted_text = extract_text_from_html(html_file_path)
                save_text_to_file(extracted_text, os.path.join(dir_path, "htmltext.txt"))