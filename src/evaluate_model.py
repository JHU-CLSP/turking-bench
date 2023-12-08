import json
import os
import evaluation_class
import argparse
from typing import List
import copy

def call_score_model(eval: evaluation_class.Evaluation, task_name: str, **kwargs):
    # print("call_score_model", task_name, row_num, model_outputs)
    scores = []
    eval.enumerate_tasks(1, task=task_name, scores=scores, params=kwargs)
    return scores

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
    scores = []
    folders = []
    for folder in os.listdir(dir):
        print(f"folder name: {folder}")
        folders.append(folder)
        file = f"{dir}/{folder}/{folder}.json"

        fp = open(f"model_output/{folder}/{folder}.json", "r")
        json_data = json.load(fp)

        evaluated_tasks = []

        kwargs = {}
        for task in json_data:
            row_num = task["row_num"]
            print(f"row_num {row_num}")
            model_outputs = [field["output"] for field in task["fields"]]
            kwargs[str(row_num)] = model_outputs

        scores.append(call_score_model(eval, folder, **kwargs))
    
    # Close the driver
    eval.driver.quit()
    print(f"Tasks: {folders}")
    print(f"Model Scores: {scores}")
