import evaluation_class
from evaluation.actions import MyActions
from evaluation.baselines import Baseline
from utils.hidden_prints import HiddenPrints
import sys

evaluation = evaluation_class.Evaluation(solver_type="oracle", tasks="dmp1",
                             do_eval=True, dump_features=True, report_field_stats=True, headless=True)

def run_dump(total_partitions):
    evaluation.enumerate_tasks(max_instance_count=1, dump_partitions=total_partitions)

if __name__ == "__main__":
    print("Running dump features")
    evaluation.tasks = sys.argv[1]
    total_partitions = sys.argv[2]
    run_dump(total_partitions)
