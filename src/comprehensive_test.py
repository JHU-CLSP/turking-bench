eval = __import__('4_run_evaluation')
from evaluation.actions import MyActions
from evaluation.baselines import Baseline
from utils.hidden_prints import HiddenPrints

evaluation = eval.Evaluation(solver_type="oracle", tasks="all",
                             do_eval=True, dump_features=True, report_field_stats=True)


def test_evaluation():
    # dictionary mapping {task_name, {num_successes, success_percentage, num_errors, avg_failing_score}}
    results = evaluation.enumerate_comprehensive_tasks(max_instance_count=1000) # dictionary of results

    # Global statistics
    tasks_succeeded = 0
    tasks_with_errors = 0
    tasks_failed = 0 # not counting tasks_with_errors

    for task in results:
        result = results[task]
        if result["success_percentage"] > 0.99:
            tasks_succeeded += 1 
        elif result["num_errors"] > 0:
            tasks_with_errors += 1
        else:
            tasks_failed += 1

        print(f"Task: {task} | Successes: {result['num_successes']} | Success Percentage: {result['success_percentage']} | Errors: {result['num_errors']} | Avg Failing Score: {result['avg_failing_score']}")

if __name__ == "__main__":
    print("Running comprehensive tests")
    test_evaluation()
