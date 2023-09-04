import os 
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import chardet

# TODO: this should be merged into evaluation file

def update_input_type_counts(html_file, input_names, input_type_counts):
    with open(html_file, 'rb') as f:
        rawdata = f.read()
    encoding = chardet.detect(rawdata)['encoding']
    with open(html_file, 'r', encoding=encoding) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    inputs=[]
    for name in input_names:
        input = soup.find(attrs={'name': name})
        if input is None:
            continue
        inputs.append(input)
    input_types = []
    for input in inputs:
        if input.name == 'textarea':
            input_type = 'textarea'
        elif input.name == 'select':
            input_type = 'select'
        else:
            input_type = input.get('type') 
            if not input_type:
                input_type = 'text'
        input_types.append(input_type)
    for input_type, count in Counter(input_types).items():
        if input_type in input_type_counts:
            input_type_counts[input_type] += count
        else:
            input_type_counts[input_type] = count


folder_count = sum(os.path.isdir(os.path.join('../tasks', i)) for i in os.listdir('../tasks'))

input_type_counts = {}

for root, dirs, files in os.walk('../tasks'):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        for file in os.listdir(dir_path):
            if file.endswith('batch.csv'):       
                df = pd.read_csv(os.path.join(dir_path, file),low_memory=False)
                input_names = [col.replace('Answer.', '') for col in df.columns if col.startswith('Answer.')]
            if file.endswith('.html'):
                update_input_type_counts(os.path.join(dir_path, file), input_names, input_type_counts)

input_fields = sum(input_type_counts.values())

print("----------------------------------------------")
print(f'Number of Datasets: {folder_count}')
print("----------------------------------------------")
print(f'Number of fields: {input_fields}')
print("----------------------------------------------")
print(f'Number of fields based on the type: {input_type_counts}')