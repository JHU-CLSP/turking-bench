import evaluation_class
import argparse
from typing import List

def call_score_model(eval: evaluation_class.Evaluation, task_name: str, row_num: int, model_outputs: List[str]):
    return eval.score_model(task_name, row_num, model_outputs)

if __name__ == "__main__":
    # user argparser to recive he input parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver_type", help="random or oracle", default="model")
    parser.add_argument("--tasks", help="train, test, or subjective_test", default="test")
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

    # TODO: remember to test invalid model outputs that dont compile
    task_name = "ATOMIC Validate gl"
    row_num = 0
    model_outputs = ['pritn(13")', 'self.modify_radio("q1_valid", 1)', 'self.modify_radio("q2_valid", 1)', 'self.modify_radio("q3_valid", 1)',
                     'self.modify_radio("q4_valid", 1)', 'self.modify_radio("q5_valid", 1)']
    score = call_score_model(eval, task_name, row_num, model_outputs)
    print(f"Model Score: {score}")