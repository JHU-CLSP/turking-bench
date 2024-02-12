import argparse
from colorama import Fore
import evaluation_class

if __name__ == "__main__":
    # user argparser to recive he input parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver_type",
                        help="donothing, random, oracle, offline_predictions, gpt4-text",
                        default="oracle")
    parser.add_argument("--tasks",
                        help="train, test_easy, test_hard, all, or subjective_test",
                        default="test_easy")
    parser.add_argument("--max_instance_count",
                        help="maximum number of instances per task",
                        type=int,
                        default=1)
    parser.add_argument("--do_eval",
                        help="whether to compute the quality against the gold data",
                        action=argparse.BooleanOptionalAction)
    parser.parse_args(['--no-do_eval'])
    parser.add_argument("--headless",
                        help="whether to run the browser `headless` (no visual interface).",
                        action=argparse.BooleanOptionalAction)
    parser.parse_args(['--no-headless'])
    parser.add_argument("--dump_features",
                        help="whether to dump the input/outputs of the model",
                        action="store_true",
                        default=False)
    parser.add_argument("--report_field_stats",
                        help="whether to collect statistics for the HTML fields",
                        action="store_true",
                        default=False)

    args = parser.parse_args()
    print(f"{Fore.BLUE}Solver: {args.solver_type}")
    max_instance_count = int(args.max_instance_count)

    dump_features = args.dump_features
    report_field_stats = args.report_field_stats
    assert type(args.do_eval) == bool
    assert type(args.headless) == bool

    if dump_features and args.solver_type != "oracle":
        raise Exception(
            f"{Fore.RED}dump_features can only be used with oracle solver")

    eval = evaluation_class.Evaluation(
        solver_type=args.solver_type,
        tasks=args.tasks,
        do_eval=args.do_eval,
        dump_features=dump_features,
        report_field_stats=report_field_stats,
        headless=args.headless
    )

    # eval.enumerate_tasks(max_instance_count)
    # Collecting example code: python 4_run_evaluation.py --no-do_eval --headless > extract.txt
    eval.enumerate_tasks(max_instance_count, task="ethics_sbic dialogue 2nd 0", first_instance_only=True, input_name="norm")
