import os
import json

scratch4 = "/scratch4/danielk/kxu39/turk_data"
task_name = "task1"

with open(f'{scratch4}/{task_name}/{task_name}.json', 'w') as fp:
    fp.write("hello world")