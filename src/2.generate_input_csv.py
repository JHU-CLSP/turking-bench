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
    # ensure that ../tasks is available
    if not os.path.exists('../tasks'):
        raise Exception("No directory named `tasks` found. Make sure that you run this script in the `src/` directory")

    for root, dirs, files in os.walk('../tasks'):
        # if files is empty then show an error
        if not files or len(files) == 0:
            raise Exception(f"No files in the specified directory: {dirs}")

        for file in files:
            if file.endswith('batch.csv'):
                path = os.path.join(root, file)
                print(' ** Reading: ' + path)
                create_input(path)