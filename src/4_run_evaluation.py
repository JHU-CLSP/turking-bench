import argparse
from colorama import Fore
import evaluation_class

if __name__ == "__main__":
    # user argparser to recive he input parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver_type",
                        help="donothing, random, oracle, offline_predictions, gpt4-text, gpt4-text-vision, text-vision",
                        default="oracle")
    parser.add_argument("--ollama_model",
                        help="llava",
                        default="llava")
    parser.add_argument("--num_demonstrations",
                        help="number of demonstrations for few shot example per input",
                        type=int,
                        default=0)
    parser.add_argument("--use_relevant_html",
                        help="whether to give only relevant HTML as context to the model",
                        action=argparse.BooleanOptionalAction)
    parser.parse_args(['--no-use_relevant_html'])
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
    parser.add_argument("--server",
                        help="whether we are running on a virtual server with xvfb and xserver-xephyr installed",
                        action=argparse.BooleanOptionalAction)
    parser.parse_args(['--no-server'])
    parser.add_argument("--screenshot_path",
                        help="file name where screenshots are saved",
                        default="screenshot.png")

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
        headless=args.headless,
        on_server=args.server,
        ollama_model=args.ollama_model,
        screenshot_path=args.screenshot_path,
        num_demonstrations=args.num_demonstrations,
        use_relevant_html=args.use_relevant_html
    )

    # eval.enumerate_tasks(max_instance_count)
    # Debugging mode
    eval.enumerate_tasks(max_instance_count, task="ethics_sbic dialogue 2nd 0", first_instance_only=True)
    # Collecting example code: python 4_run_evaluation.py --no-do_eval --headless > extract.txt
    # eval.enumerate_tasks(max_instance_count, task="ethics_sbic dialogue 2nd 0", first_instance_only=True, input_name="norm")
