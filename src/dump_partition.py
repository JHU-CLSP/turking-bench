import evaluation_class
from evaluation.actions import MyActions
from evaluation.baselines import Baseline
from utils.hidden_prints import HiddenPrints
import sys

evaluation = evaluation_class.Evaluation(solver_type="oracle", tasks="dmp1",
                             do_eval=True, dump_features=True, report_field_stats=True, headless=True)

def run_dump():
    evaluation.enumerate_tasks(max_instance_count=1, dump_partitions=1)

if __name__ == "__main__":
    print("Running dump features")
    evaluation.tasks = sys.argv[1]
    run_dump()
