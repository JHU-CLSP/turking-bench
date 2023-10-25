eval = __import__('4_run_evaluation')
from evaluation.actions import MyActions
from evaluation.baselines import Baseline
from utils.hidden_prints import HiddenPrints
import sys

evaluation = eval.Evaluation(solver_type="random", tasks="all",
                             do_eval=True, dump_features=False, report_field_stats=False, headless=True)


def test_evaluation():
    # dictionary mapping {task_name, {num_successes, num_errors, num_failing, sum_failing_scores} }
    results = evaluation.enumerate_tap_tasks_random(max_instance_count=1000) # dictionary of results

    # Global statistics
    tasks_succeeded = 0
    tasks_with_errors = 0
    tasks_failed = 0 # not counting tasks_with_errors

    for task in results:
        result = results[task]
        if result["num_errors"] == 0 and result["num_failing"] == 0:
            tasks_succeeded += 1 
        elif result["num_errors"] > 0:
            tasks_with_errors += 1
        else:
            tasks_failed += 1

        print(f"task: {task} | result: {result}")

    print(f"tasks_succeeded: {tasks_succeeded} | tasks_with_errors: {tasks_with_errors}")
    assert tasks_with_errors == 0, f"There were {tasks_failed} failures"

if __name__ == "__main__":
    print("Running comprehensive tests for random baseline")
    evaluation.tasks = sys.argv[1]
    test_evaluation()
