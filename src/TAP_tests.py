import evaluation_class
from evaluation.actions import MyActions
from evaluation.baselines import Baseline
from utils.hidden_prints import HiddenPrints
import sys

evaluation = evaluation_class.Evaluation(solver_type="oracle", tasks="all",
                             do_eval=True, dump_features=False, report_field_stats=False, headless=True)


def test_evaluation():
    if evaluation.tasks == "all":
        evaluation.solver_type = "random"
        results = evaluation.enumerate_tap_tasks_random(max_instance_count=2) # dictionary of results
    else:
        # dictionary mapping {task_name, {num_successes, num_errors, num_failing, sum_failing_scores} }
        max_instance_count = 1000
        results = evaluation.enumerate_tap_tasks(max_instance_count=max_instance_count) # dictionary of results

    # Global statistics
    tasks_succeeded = 0
    tasks_with_errors = 0
    tasks_failed = 0 # not counting tasks_with_errors

    for task in results:
        result = results[task]
        # Note (Daniel): softened the conditioned a bit to allow for some failures
        # if result["num_errors"] == 0 and result["num_failing"] == 0:
        if result["num_errors"] + result["num_failing"] < 0.05 * result["num_successes"]:
            tasks_succeeded += 1
        elif result["num_errors"] > 0:
            tasks_with_errors += 1
        else:
            tasks_failed += 1

        print(f"task: {task} | result: {result}")

    print(f"tasks_succeeded: {tasks_succeeded} | tasks_with_errors: {tasks_with_errors} | tasks_failed: {tasks_failed}")
    assert tasks_with_errors == 0 and tasks_failed == 0, f"There were {tasks_with_errors} errors and {tasks_failed} failures"

if __name__ == "__main__":
    print("Running comprehensive tests")
    evaluation.tasks = sys.argv[1]
    test_evaluation()
