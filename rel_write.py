import os
from pathlib import Path

scratch4 = "/scratch4/danielk/kxu39/turk_data"
task_name = "task1"

Path(f"{scratch4}/{task_name}").mkdir(parents=True, exist_ok=True)

with open(f'{scratch4}/{task_name}/{task_name}.txt', 'w') as fp:
    fp.write("hello world")