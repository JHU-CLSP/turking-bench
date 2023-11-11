import os
import json

scratch4 = "/scratch4/danielk/kxu39/turk_data"
task_name = "task1"
os.makedirs(f"{scratch4}/{task_name}", exist_ok=True)

with open(f'{scratch4}/{task_name}/{task_name}.json', 'w') as fp:
    fp.write("hello world")