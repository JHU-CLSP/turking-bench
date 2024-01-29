import re
import ast

def clean_log():
    """
    Clean the turk_logs.txt file to only contain the relevant information 
    """
    with open("turk_logs.txt", "r") as read_file, open("turk_logs_clean.txt", "w") as write_file:
        latest_task = ""
        for line in read_file:
            # Figure out which lines to write back to the cleaned txt file
            if line.startswith("instance_id:") or line.startswith(" --> inputs:") \
                or line.startswith(" --> Per-instance overall score:") \
                or line.startswith(" --> Per-instance per-field breakdown:"):
                # or line.startswith(" --> scores:") or line.startswith("----> per-field score:") \
                # or line.startswith("--> Computing the majority vote") \
                write_file.write(line)

            if line.startswith(" ------- evaluating input:"):
                extracted_task = extract_task_info(line)
                if extracted_task != latest_task:
                    write_file.write(line)
                    latest_task = extracted_task

def extract_task_info(line: str) -> str:
    # Define the regex pattern
    pattern = r"task=`([^`]*)`"

    # Search for the pattern in the string
    match = re.search(pattern, line)

    # If a match is found, return the captured group
    if match:
        return match.group(1)

    return None

def extract_overall_score(line: str) -> float:
    # Split the line into parts based on spaces
    parts = line.split()

    # The score should be the last element in the parts list
    score_str = parts[-1]
    # Strip unwanted characters (keeping only digits and the decimal point)
    score_str_cleaned = ''.join(filter(lambda x: x.isdigit() or x == '.', score_str))

    # Convert the score to a float and return
    try:
        return float(score_str_cleaned)
    except ValueError:
        return None

def extract_dict(line: str) -> dict:
    # Find the start of the dictionary
    dict_start = line.find("{")
    # Find the end of the dictionary
    dict_end = line.rfind("}") + 1

    # Extract the dictionary string
    dict_str = line[dict_start:dict_end]

    # Convert the string to a dictionary
    try:
        extracted_dict = ast.literal_eval(dict_str)
        return extracted_dict
    except (ValueError, SyntaxError):
        # Handle the exception if the string is not a valid Python literal
        print(f"Error: The string {dict_str} is not a valid Python literal dictionary to extract {ValueError} {SyntaxError}")
        return None

def group_log():
    """
    Group the scores based on inputs
    """

    data = {}

    with open("turk_logs_clean.txt", "r") as read_file:
        latest_task = ""
        for line in read_file:
            if line.startswith(" ------- evaluating input:"):
                extracted_task = extract_task_info(line)
                if extracted_task != latest_task:
                    # Skip this task since it only half finished in the logged run
                    skipped_task = ""
                    if extracted_task == skipped_task:
                        break

                    data[extracted_task] = {"all": [], "breakdown": []}
                    latest_task = extracted_task
            
            if line.startswith(" --> Per-instance overall score:"):
                score = extract_overall_score(line)
                data[latest_task]["all"].append(score)

            
            if line.startswith(" --> Per-instance per-field breakdown:"):
                breakdown = extract_dict(line)
                data[latest_task]["breakdown"].append(breakdown)

    ret = {}

    for key in data:
        ret[key] = {}
        ret[key]["all"] = sum(data[key]["all"]) / len(data[key]["all"])

        temp = {}
        for breakdown in data[key]["breakdown"]:
            for field in breakdown:
                if field not in ret:
                    temp[field] = {}
                    temp[field]["sum"] = 0 
                    temp[field]["len"] = 0 

                for score in breakdown[field]:
                    temp[field]["sum"] += score
                    temp[field]["len"] += 1

        for field in temp:
            ret[key][field] = temp[field]["sum"] / temp[field]["len"]

    return ret


if __name__ == '__main__':
    clean_log()
    res = group_log()

    with open("turk_logs_result.txt", "w") as write_file:
        for key in sorted(res.keys()):
            print(f"{key}: {res[key]}")
            write_file.write(f"{key}: {res[key]}\n")