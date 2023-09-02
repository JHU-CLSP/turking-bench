"""
This script creates MTurk sandbox tasks
We use sandbox for human evaluation
"""
import os
import json
import re
from tqdm import tqdm
import amt
from amt import mturk
from amt import create
from amt import expire

from colorama import Fore

MAX_ATTEMPTS = 25
"""The number of retries to perform for requests."""

ENVS = {
    'live': {
        'region_name': 'us-east-1',
        'endpoint_url': 'https://mturk-requester.us-east-1.amazonaws.com',
        'worker_url': 'https://www.mturk.com/',
        'requester_url': 'https://requester.mturk.com/'
    },
    'sandbox': {
        'region_name': 'us-east-1',
        'endpoint_url': 'https://mturk-requester-sandbox.us-east-1.amazonaws.com',
        'worker_url': 'https://workersandbox.mturk.com/',
        'requester_url': 'https://requestersandbox.mturk.com/'
    }
}

# set environmental variable for "AWS_PROFILE"
os.environ["AWS_PROFILE"] = "danyal.khashabi@gmail.com"

env = 'sandbox'
print(f"{Fore.BLUE} Using the following profile: {os.getenv('AWS_PROFILE')}")
client = amt.mturk.get_mturk_client(env)
region_name = ENVS[env]['region_name']
endpoint_url = ENVS[env]['endpoint_url']
worker_url = ENVS[env]['worker_url']

print(f'Creating mturk client in region {region_name} with endpoint {endpoint_url}.')


def turn_csv_to_jsonl(csf_file_name, jsonl_file_name, max_num_rows):
    import csv
    import jsonlines
    with open(csf_file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # make sure the titles (first row) does not have any dash in their names
        titles_with_dash = [x for x in csv_reader.fieldnames if "-" in x]
        assert len(titles_with_dash) == 0, f"Titles with dash: {titles_with_dash}"
        with jsonlines.open(jsonl_file_name, mode='w') as writer:
            for i, row in enumerate(csv_reader):
                # replace all "﻿" with ""
                row = {k.replace("﻿", ""): v for k, v in row.items()}
                if i >= max_num_rows:
                    break
                writer.write(row)


def launch_amt_experiments(max_num_rows=10):
    # create a directory called "definition"
    default_directory = "default_definition"
    if not os.path.exists(default_directory):
        raise Exception("Directory %s does not exist" % default_directory)

    # load tasks from ../data/splits/evaluation_tasks.txt
    tasks = []
    with open("../data/splits/evaluation_tasks.txt", "r") as f:
        for line in f:
            tasks.append(line.strip())

    prefix = "human-eval-Aug26-"
    for task in tqdm(tasks):

        print(" - - - - - - - - - - - - - - - \n * processing task: %s" % task)

        task_dir = f"../tasks/{task}/"
        definition_dir = "default_definition"

        # create jsonl version of the data
        turn_csv_to_jsonl(task_dir + "input.csv", task_dir + "input.jsonl", max_num_rows)

        # read "hittypeproperties.json" json file
        with open(os.path.join(definition_dir, "hittypeproperties_copy.json"), "r") as f:
            hittypeproperties = f.read()
            # parse the json file
            hittypeproperties = json.loads(hittypeproperties)
            # change the title, keywords, and description
            hittypeproperties["Title"] = prefix + task
            hittypeproperties["Keywords"] = prefix + task
            hittypeproperties["Description"] = prefix + task
            # convert the json back to string
            hittypeproperties = json.dumps(hittypeproperties)

        with open(os.path.join(definition_dir, "hittypeproperties.json"), "w+") as f:
            f.write(hittypeproperties)

        # copy HTML file to the "task_dir"
        template_tail = """
            ]]>
            </HTMLContent>
            <FrameHeight>450</FrameHeight>
        </HTMLQuestion>
        """
        template_head = """
        <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
            <HTMLContent>
            <![CDATA[
        """
        with open(os.path.join(definition_dir, "question.xml.j2"), "w+") as f:
            # read the oroginal template
            question = open(os.path.join(task_dir, "template.html"), "r").read()

            # use regex convert mturk variables ${variable} to jinja2 variables {{variable}}
            question = re.sub(r"\$\{(.+?)\}", r"{{\1}}", question)
            f.write(template_head + question + template_tail)

        batch_dir = create.create_batch(
            client=client,
            definition_dir=default_directory,
            data_path=task_dir + "/input.jsonl",
            save_dir=task_dir)

        print(
            f'Finished creating batch directory: {batch_dir}.'
            f'\n'
            f'\n    Preview HITs: {worker_url}'
            f'\n')

        # remove hittypeproperties.json
        os.system(f"rm {definition_dir}/hittypeproperties.json")
        os.system(f"rm {definition_dir}/question.xml.j2")
        print(f"{Fore.YELLOW}Done with the releasing this task")


def expire_sandbox_tasks(delete):
    # set environmental variable for "AWS_PROFILE"
    # load tasks from ../data/splits/evaluation_tasks.txt
    tasks = []
    with open("../data/splits/evaluation_tasks.txt", "r") as f:
        for line in f:
            tasks.append(line.strip())

    if False:
        batch_dirs = []
        for task in tasks:
            # list all the directories that start with "batch-"
            batch_dirs.extend(
                [
                    os.path.join("../tasks", task, d) for d in os.listdir(os.path.join("../tasks", task)) if
                    d.startswith("batch-")
                ]
            )

    else:
        batch_dirs = [
            "../tasks/winogrande validation (grammar) additional_ph/batch-41f00859-6f7a-4709-bb8f-5594337a9874",
            "../tasks/wikiHow step-goal linking pilot cleanse-url/batch-0b3ac568-ef1b-4c1a-98d2-0ab8cf821c4b",
            "../tasks/Spanish Word Alignment/batch-3a3f6343-d6ee-4afe-af24-308889e93977",
            "../tasks/Sherlock IMG 2 TXT Eval 15/batch-ba0a49eb-6333-4cb5-a21c-c9425377da2a",
            "../tasks/Sherlock IMG 2 TXT Eval 15/batch-c359ce9a-7f20-4896-b74b-5b5a61e49efc",
        ]
    for batch_dir in batch_dirs:
        print(f"{Fore.CYAN} -> expiring the following batch: {batch_dir}")
        try:
            expire.expire_batch(client, batch_dir)
        except Exception as e:
            print(f"{Fore.RED} -> failed to expire the following batch: {batch_dir}")
            print(e)

        if delete:
            # delete the directory after escaping the spaces in the directory name
            batch_dir_nospace = batch_dir.replace(' ', '\ ')
            print(f"{Fore.GREEN} -> deleting the following batch: {batch_dir}")
            try:
                os.system(f"rm -rf {batch_dir_nospace}")
            except Exception as e:
                print(f"{Fore.RED} -> failed to delete the following batch: {batch_dir_nospace}")
                print(e)


if __name__ == "__main__":
    launch_amt_experiments(max_num_rows=10)
    # expire_sandbox_tasks(delete=True)
