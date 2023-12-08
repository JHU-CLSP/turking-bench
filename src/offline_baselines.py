# This code is for v1 of the openai package: pypi.org/project/openai
import os
import json
from evaluation.prompts import get_encoded_input_prompt
from evaluation.actions import ActionUtils


DIR = "../model_output"
def evaluate():
    # list the directories
    dirs = os.listdir(f"{DIR}")
    for dir in dirs:
        # read the json file
        with open(f"{DIR}/{dir}/{dir}.json", "r") as f:
            json_data = json.load(f)

        for instance in json_data:

            for field in instance["fields"]:
                # get the prompt
                html_file_name = field["html_id"]

                # read the html file
                with open(f"{DIR}/{dir}/HTML/{html_file_name}", "r") as f:
                    html = f.read()

                input_name = field["input_name"]

                text_prompt = get_encoded_input_prompt(input_name, html)

                # call the open the api
                response = ActionUtils.open_ai_call(text_prompt)

                gold_action = field["output"]["action_sequence"]

                print("gold_action", gold_action)
                print("response", response)
                print(" - - - - ")

# execution entry point
if __name__ == "__main__":
    evaluate()
