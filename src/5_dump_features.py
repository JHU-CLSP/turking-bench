"""
This script is used to dump features for the all the evaluation tasks.
"""
eval = __import__('4_run_evaluation')
from evaluation.baselines import Baseline

evaluation = eval.Evaluation(
    solver_type="oracle", tasks="all",
    do_eval=True, dump_features=True,
    report_field_stats=True,
    headless=True
)
evaluation.enumerate_tasks(max_instance_count=1)
