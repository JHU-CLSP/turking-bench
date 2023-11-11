import os

scratch4 = "/scratch4/danielk/kxu39/turk_data"
task_name = "task1"
os.mkdir(f"{scratch4}/{task_name}", exist_ok=True)

with open(f'{scratch4}/{task_name}/{task_name}.txt', 'w') as fp:
    fp.write("hello world")