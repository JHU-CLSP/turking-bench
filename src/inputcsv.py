import pandas as pd
import os
"""
Script for removing unnecessary data from csv files
"""

def create_input(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    df = df.loc[:, ~df.columns.str.startswith('Answer.')]
    df.drop_duplicates(inplace=True)
    df.to_csv(csv_file.replace('batch.csv', 'input.csv') , encoding='utf-8-sig', index=False)

if __name__ == '__main__':
    for root, dirs, files in os.walk('tasks'):
        for file in files:
            if file.endswith('batch.csv'):
                print('Reading' + file)
                create_input(os.path.join(root, file))