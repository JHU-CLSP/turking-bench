"""
This file creates a csv file of the tasks in the repository that is
later used for visualizing the tasks in mturk.html
"""

import os
import pandas as pd


def get_parent_dir(filePath):
    parent_dir = os.path.split(os.path.dirname(filePath))[-1]
    return parent_dir

if __name__ == '__main__':
    # create a dataframe
    df = pd.DataFrame(columns=['Title', 'Action'])
    for root, dirs, files in os.walk('tasks'):
        for file in files:
            if file.endswith('.html'):
                # get the parent directory name
                parent_dir = get_parent_dir(os.path.join(root, file))
                df = df.append({'Title': parent_dir, 'Action': os.path.join(root, file)}, ignore_index=True)
    # save data in a csv file
    df.to_csv('mturk_file_list.csv', index=False)