eval = __import__('4_run_evaluation')
from evaluation.actions import MyActions
from evaluation.baselines import Baseline

eval = eval.Evaluation()

def test_actions():
    baseline = Baseline()
    action_list = baseline.get_action_list()
    print(action_list)
    assert len(action_list) > 0, f"The action list should not be empty: {action_list}"

    encoded_actions_prompt = baseline.get_encoded_action_list()
    print(encoded_actions_prompt)
    assert len(encoded_actions_prompt) > 0, f"The encoded actions prompt should not be empty: {encoded_actions_prompt}"

def test_evaluation():
    tasks = eval.load_task_names(setup='all')  # TODO: receive setup from input
    config = eval.read_config('config.ini')
    batch = config.getboolean('DEFAULT', 'batch')  # TODO: what is this?
    max_instance_count = config.getint('DEFAULT', 'num')
    mode = config.get('DEFAULT', 'mode')
    input_format = config.get('DEFAULT', 'input_format')
    image_format = config.get('DEFAULT', 'image_format', fallback='full_page')
    eval.enumerate_tasks(tasks, batch, max_instance_count, mode, input_format, image_format)

if __name__ == "__main__":

    test_actions()
    test_evaluation()

    # test that we can apply the gold labels on the tasks

    # test the actions

    # test the evaluation
