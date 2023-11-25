import json
import os
import evaluation_class
import argparse
from typing import List
import copy

def call_score_model(eval: evaluation_class.Evaluation, task_name: str, row_num: int, model_outputs: List[str]):
    # print("call_score_model", task_name, row_num, model_outputs)
    score = []
    eval.enumerate_tasks(1, task=task_name, row_num=row_num, model_outputs=model_outputs, score=score)
    return score

if __name__ == "__main__":
    # user argparser to recive he input parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver_type", help="random or oracle", default="model")
    parser.add_argument("--tasks", help="train, test, or subjective_test", default="test_easy")
    parser.add_argument("--max_instance_count", help="maximum number of instances per task", default=1)
    parser.add_argument("--do_eval", help="whether to compute the quality aginst the gold data", default=True)
    parser.add_argument("--dump_features", help="whether to dump the features", default=False)
    parser.add_argument("--report_field_stats", help="whether to collect statistics for the HTML fields", default=True)
    parser.add_argument("--headless", help="whether to run the browser `headless` (no visual interface).", default=False)

    args = parser.parse_args()
    eval = evaluation_class.Evaluation(
        solver_type=args.solver_type,
        tasks=args.tasks,
        do_eval=args.do_eval,
        dump_features=args.dump_features,
        report_field_stats=args.report_field_stats,
        headless=args.headless
    )

    dir = "model_output"
    ex_dir = "Question Typing 4" # example dir
    for folder in os.listdir(dir):
        print(f"folder name: {folder}")
        file = f"{dir}/{folder}/{folder}.json"

    fp = open(f"model_output/{ex_dir}/{ex_dir}.json", "r")
    json_data = json.load(fp)

    evaluated_tasks = []

    curr_task = {}
    for block in json_data:
        if "task_name" in block:
            evaluated_tasks.append(copy.deepcopy(curr_task))
            curr_task["task_name"] = block["task_name"]
            curr_task["row_num"] = block["row_num"]
            curr_task["model_outputs"] = []
        else:
            curr_task["model_outputs"].append(block["output"])

    evaluated_tasks.append(copy.deepcopy(curr_task)) # add the last block 
    evaluated_tasks.pop(0) # pop out the first empty {} curr_task

    for task in evaluated_tasks:
        task_name = task["task_name"]
        row_num = task["row_num"]
        model_outputs = task["model_outputs"]
        print(f"Task Name: {task_name} Row Num: {row_num}")
        score = call_score_model(eval, task_name, row_num, model_outputs)
        print(f"Model Score: {score}")
        break