import evaluation_class
import argparse

if __name__ == "__main__":
    # user argparser to recive he input parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver_type", help="random or oracle", default="random")
    parser.add_argument("--tasks", help="train, test, or subjective_test", default="test")
    parser.add_argument("--max_instance_count", help="maximum number of instances per task", default=1)
    parser.add_argument("--do_eval", help="whether to compute the quality aginst the gold data", default=True)
    parser.add_argument("--dump_features", help="whether to dump the features", default=False)
    parser.add_argument("--report_field_stats", help="whether to collect statistics for the HTML fields", default=True)

    args = parser.parse_args()
    args.solver_type = "model"

    # call a helper function to go ahead and run evaluation_class evaluate model with appropriate inputs
    # def score_model(self, task_name: str, row_num: int, model_outputs: List[str]):
    # remember to test invalid model outputs that dont compile