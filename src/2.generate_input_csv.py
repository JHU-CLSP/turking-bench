import pandas as pd
import os

"""
Script for removing unnecessary data from csv files
"""


def create_input(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    df = df.loc[:, ~df.columns.str.startswith('Answer.')]
    df.drop_duplicates(inplace=True)
    df.to_csv(csv_file.replace('batch.csv', 'input.csv'), encoding='utf-8-sig', index=False)


ROOT = '../tasks'

if __name__ == '__main__':
    # ensure that ../tasks is available

    if not os.path.exists(ROOT):
        raise Exception("No directory named `tasks` found. Make sure that you run this script in the `src/` directory")

    items = os.listdir(ROOT)
    # if files is empty then show an error
    if len(items) == 0:
        raise Exception(f"No files in the specified directory `{items}`: {ROOT}")

    for item in items:

        # skip if not a dir
        if not os.path.isdir(os.path.join(ROOT, item)):
            continue

        file = os.path.join(ROOT, item, 'batch.csv')

        # make sure the file exists
        if not os.path.exists(file):
            raise Exception(f"File `{file}` does not exist")

        print(' ** Reading: ' + file)
        create_input(path)
