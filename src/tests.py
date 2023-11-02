import evaluation_class
from evaluation.actions import MyActions
from evaluation.baselines import Baseline
from evaluation.input import Input
from utils.hidden_prints import HiddenPrints

evaluation = evaluation_class.Evaluation(solver_type="oracle", tasks="all",
                             do_eval=True, dump_features=True, report_field_stats=True, headless=True)


def test_actions():
    baseline = Baseline(driver=evaluation.driver, actions=evaluation.actions)
    action_list = baseline.get_action_list()
    print(action_list)
    assert len(action_list) > 0, f"The action list should not be empty: {action_list}"

    # Dummy input
    dummy_input = Input(
        url="https://www.google.com",
        input_name="dummy",
        input_type="text",
        task_name="dummy")
    encoded_actions_prompt = baseline.get_encoded_input_prompt(dummy_input)
    print(encoded_actions_prompt)
    assert len(encoded_actions_prompt) > 0, f"The encoded actions prompt should not be empty: {encoded_actions_prompt}"


def test_evaluation():
    evaluation.enumerate_tasks(max_instance_count=1)


if __name__ == "__main__":
    print("Running initial pass on tests without logs")
    try:
        with HiddenPrints():
            test_evaluation()
            test_actions()
    except Exception as error:
        print("An error occurred:", error)
        print("Rerunning tests with logs now")
        test_evaluation()
        test_actions()

    # TODO: test that we can apply the gold labels on the tasks

    # TODO: test the actions

    # TODO: test the evaluation
