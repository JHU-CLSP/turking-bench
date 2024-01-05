import argparse
from colorama import Fore
import random
import pandas as pd
import os
import shutil
from selenium.webdriver.common.by import By
import json
import evaluation_class
from utils.hidden_prints import HiddenPrints
import logging

TURKLE_URL = "http://localhost:8000"
TEST_NAME = "Annotation subj_obj"
SPECIFIED_INDEX = 0
RUN_ALL = False

class Run(evaluation_class.Evaluation):
    def run_task(self, task_name: str, max_instance_count: int, index: int = 0):
        results = {}
        self.driver.get(TURKLE_URL)
        aggregate_field_statistics = {}  # We store the stats related to the field types/frequency here
        task_field_statistics = {}
        print(f"{Fore.BLUE} = = = = = = = = = = = = starting new task: `{task_name}` = = = = = = = = = = = = ")

        instance_ids = self.task_ids[task_name]

        if max_instance_count == 1 and len(instance_ids) - 1 < index:
            raise Exception(f"{Fore.RED}The index {index} is out of bounds for task {task_name} with {len(instance_ids)} instances.")

        first_instance_id = min(instance_ids)

        # if maximum is less than the number of instances, we sample a random subset of instances
        if max_instance_count < len(instance_ids):
            # random sample
            instance_ids = random.sample(instance_ids, max_instance_count)

        # Sample random instances of each task
        for instance_id in instance_ids:
            # remove the randomness of which index we choose
            if max_instance_count == 1:
                instance_id = first_instance_id + index

            row_number = instance_id - first_instance_id
            print(f"instance_id: {instance_id} <-> row_number: {row_number}")

            url = f'{TURKLE_URL}/task/{instance_id}/iframe/'
            self.driver.get(url)

            # get the name of the fields
            df = pd.read_csv(f'../tasks/{task_name}/batch.csv', nrows=0)
            input_names = [col[len('Answer.'):] for col in df.columns if col.startswith('Answer.')]
            inputs = self.extract_input_values_from_url(url=url, task_name=task_name, input_names=input_names)

            print(" --> inputs: {}".format([x.name for x in inputs]))

            answers_map = self.retrieve_gold_labels(
                task_name, row_number, [x.name for x in inputs]
            )

            print(" --> input labels: {}".format(answers_map))

            # TODO: check if all the files (images, videos, audio, css, etc.) in the HTML are accessible
            # TODO: find all the URLS in the HTML and check if they are accessible

            if self.dump_features:
                directory = f'features/{task_name}'
                images_directory = f'{directory}/images'
                html_directory = f'{directory}/HTML'

                if os.path.exists(directory):
                    shutil.rmtree(directory)
                os.makedirs(directory)

                if not os.path.exists(html_directory):
                    os.makedirs(html_directory)

            # for counting overall statistics
            if self.report_field_stats:
                if task_name not in task_field_statistics:
                    task_field_statistics[task_name] = {}

                for i in inputs:
                    if i.type not in aggregate_field_statistics:
                        aggregate_field_statistics[i.type] = 0

                    aggregate_field_statistics[i.type] += 1

                    if i.type not in task_field_statistics[task_name]:
                        task_field_statistics[task_name][i.type] = 0
                    task_field_statistics[task_name][i.type] += 1

            if self.dump_features:
                data_to_be_dumped = []

            for input_idx, i in enumerate(inputs):
                print(f"{Fore.GREEN} - - - - - -  starting a new element: `{i}` - - - - - -  ")

                # make sure that the element is visible
                element = self.driver.find_element(By.NAME, i.name)
                if not element.is_displayed() or element.size['width'] <= 0 or element.size['height'] <= 0:
                    print(f'{Fore.RED}Skipping element `{i.name}` since it is not visible.')
                    continue

                if self.dump_features and i.type != 'hidden':
                    image_format = "bordered_div"  # the most reasonable option
                    # create directory if needed
                    if not os.path.exists(f'{images_directory}_{image_format}'):
                        os.makedirs(f'{images_directory}_{image_format}')
                    if image_format == 'full_page':
                        task_image = self.actions.take_page_screenshots().outcome
                    elif image_format == 'bordered_div':
                        task_image = self.actions.take_element_screenshot_with_border(i).outcome
                    else:
                        raise Exception(f"{Fore.RED}to be implemented for image format `{image_format}`")

                    if isinstance(task_image, list):
                        img_ids = []
                        for j, image in enumerate(task_image):
                            image_id = f'{instance_id}_{input_idx}_{i.name}_{j}.png'
                            image.save(f'{images_directory}_{image_format}/{image_id}')
                            img_ids.append(image_id)
                        image_id = img_ids
                    else:
                        image_id = f'{instance_id}_{input_idx}_{i.name}.png'
                        task_image.save(f'{images_directory}_{image_format}/{image_id}')

                    html_id = f'{instance_id}_{i.name}.html'
                    with open(f'{html_directory}/{html_id}', 'w') as f:
                        # note, we can't use "driver.page_source" since it would return the default source without any changes
                        # TODO: double-check that this HTML code indeed contains the latest changes
                        f.write(self.driver.execute_script("return document.documentElement.outerHTML;"))

                # *after* we dump *input* features, we execute the action
                if self.solver_type == 'oracle':
                    kwargs = {'answers': answers_map[i.name]}
                    print(f"oracle go solve, input: {i}, kwargs: {kwargs}")
                    oracle_action_sequence = self.solver.solve(i, **kwargs)
                else:
                    self.solver.solve(i)

                # *after* we execute the action, we dump the *output* features
                if self.dump_features:
                    data_to_be_dumped.append({
                        'input_type': i.type,
                        'input_name': i.name,
                        'image_id': image_id,
                        'html_id': html_id,
                        'output': oracle_action_sequence
                    })

            # get the input values from the web page
            inputs_with_values = self.extract_values(inputs)

            # collecting field statistics
            if task_name not in results:
                results[task_name] = {}

            # TODO: move this inside a evaluation function to keep here clean
            score = 0.0
            for i in inputs_with_values:
                if i.name in self.excluded_input_names:
                    continue

                if i.values != i.visible_values:
                    if (i.values == [None] and i.visible_values == ['']) or (i.values == [''] and i.visible_values == [None]):
                        pass
                    elif type(i.values[0]) == str and type(i.visible_values[0]) == str:
                        if i.values[0] == i.visible_values[0]:
                            pass
                    else:
                        raise Exception(f"The values `{i.values}` and visible values `{i.visible_values}` should be the same for `{i}`")




                # if checkmarks, sort the values alphabetically
                if i.type == "checkbox":
                    i.values = "|".join(sorted(i.values))
                    for idx in range(len(answers_map[i.name])):
                        x = answers_map[i.name][idx]
                        if type(x) == str and "|" in x:
                            answers_map[i.name][idx] = "|".join(sorted(x.split("|")))
                else:
                    if len(i.values) > 0:
                        i.values = i.values[0]
                    else:
                        i.values = ''
                score_per_field = self.calculate_rouge(answers_map[i.name], i.type, i.values)

                if i.type not in results[task_name]:
                    results[task_name][i.type] = []

                results[task_name][i.type].append(score_per_field)

                print("i", i)
                print("score per field", score_per_field)
                score += score_per_field

            print("length:", len(inputs_with_values), "score: ", score)
            score /= len(inputs_with_values)
            print(f"{Fore.CYAN} --> Overall score: {score}")

            if self.solver_type == 'oracle':
                if score <= 0.99:
                    print(f"input_idx of failure {input_idx}")
                assert score > 0.99, f"{Fore.RED}The oracle baseline should always get a score of 1.0"

            if self.dump_features:
                with open(f'{directory}/{task_name}.json', 'w') as f:
                    json.dump(data_to_be_dumped, f, indent=4)

            df = pd.DataFrame()
            for task_name, inputs in results.items():
                for input_type, scores in inputs.items():
                    # print(scores)
                    avg_score = sum(scores) / len(scores)
                    # TODO: check if we can safely change the "projects" in the following lines to tasks
                    df = pd.concat(
                        [
                            df, pd.DataFrame({
                            'project': [task_name],
                            'input_type': [input_type],
                            'score': [avg_score]
                        })
                        ],
                        ignore_index=True)

            if 'project' not in df.columns:
                df.insert(0, 'project', '')
            if 'input_type' not in df.columns:
                df.insert(1, 'input_type', '')
            if 'score' not in df.columns:
                df.insert(1, 'score', '')

            df = df.pivot(index='project', columns='input_type', values='score')
            df.to_csv('oracle_baseline_scores.csv', index=True)

        # Close the driver
        self.driver.quit()

        print("Now let's print the field statistics")

        # save task_field_statistics (hashmap of hashmaps mapped to integers) as a csv file
        # first turn this hashmap into data frame
        # then save it as a csv file
        results = pd.DataFrame.from_dict(task_field_statistics)
        results.to_csv('task_field_statistics.csv', index=True)

        print("----------------------------------------------")
        print(f'Number of tasks: {len(task_field_statistics.keys())}')
        print("----------------------------------------------")
        print(f'Number of fields: {len(aggregate_field_statistics.keys())}')
        print("----------------------------------------------")
        print(f'Overall field statistics: {aggregate_field_statistics}')
        print("----------------------------------------------")
        print(f'Field statistics per task: {task_field_statistics}')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO
    # user argparser to recive he input parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver_type", help="random or oracle", default="random")
    parser.add_argument("--tasks", help="train, test, or subjective_test", default="test_easy")
    parser.add_argument("--max_instance_count", help="maximum number of instances per task", default=1)
    parser.add_argument("--do_eval", help="whether to compute the quality aginst the gold data", default=True)
    parser.add_argument("--dump_features", help="whether to dump the features", default=False)
    parser.add_argument("--report_field_stats", help="whether to collect statistics for the HTML fields", default=True)

    args = parser.parse_args()
    args.solver_type = "oracle"

    if RUN_ALL:
        args.max_instance_count = 1000
    else:
        args.max_instance_count = 1
    print(f"{Fore.BLUE}Solver: {args.solver_type}")
    max_instance_count = int(args.max_instance_count)

    do_eval = args.do_eval
    dump_features = args.dump_features
    report_field_stats = args.report_field_stats

    if dump_features and args.solver_type != "oracle":
        raise Exception(f"{Fore.RED}dump_features can only be used with oracle solver")

    eval = Run(solver_type=args.solver_type, tasks=args.tasks,
                      do_eval=do_eval, dump_features=dump_features, report_field_stats=report_field_stats, headless = RUN_ALL)

    if RUN_ALL:
        # Note if everything runs smoothly, nothing will be printed since it all succeeds
        with HiddenPrints():
            eval.run_task(TEST_NAME, args.max_instance_count, SPECIFIED_INDEX)
    else:
        eval.run_task(TEST_NAME, args.max_instance_count, SPECIFIED_INDEX)