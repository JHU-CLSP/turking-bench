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
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                data['new_key'] = 'new_value'

                with open(os.path.join(root, file), 'w') as f:
                    json.dump(data, f)