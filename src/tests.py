from src.evaluation import Evaluation
from src.evaluation import Actions

def test_actions():
    pass

def test_evaluation():
    tasks = Evaluation.load_task_names(setup='all')  # TODO: receive setup from input
    config = Evaluation.read_config('config.ini')
    batch = config.getboolean('DEFAULT', 'batch')  # TODO: what is this?
    max_instance_count = config.getint('DEFAULT', 'num')
    mode = config.get('DEFAULT', 'mode')
    input_format = config.get('DEFAULT', 'input_format')
    image_format = config.get('DEFAULT', 'image_format', fallback='full_page')

    # test that we can enumerate the tasks
    Evaluation.enumerate_tasks(tasks, batch, max_instance_count, mode, input_format, image_format)

if __name__ == "__main__":

    pass

    # test that we can apply the gold labels on the tasks

    # test the actions

    # test the evaluation
