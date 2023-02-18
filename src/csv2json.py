import os
import csv
import json
import codecs
import pandas

# return the name of parent directory of a file
def get_parent_dir(filePath):
    parent_dir = os.path.split(os.path.dirname(filePath))[-1]
    return parent_dir


if __name__ == '__main__':
    for root, dirs, files in os.walk('tasks'):
        for file in files:
            if file.endswith('.csv'):
                pd = pandas.read_csv(os.path.join(root, file), encoding='utf-8')
                # create a dataframe with the columns starting with 'Answer.' and 'Input.' and 'Approve' and 'Reject'
                pd = pd[[col for col in pd.columns if col.startswith('Answer.') or col.startswith('Input.') or col.startswith('Approve') or col.endswith('Reject')]]
                pd.to_json(os.path.join(root, get_parent_dir(root) + '.json'), orient='records', indent=4 ,force_ascii=False)