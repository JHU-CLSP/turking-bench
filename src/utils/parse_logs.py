import re

def clean_log():
    """
    Clean the turk_logs.txt file to only contain the relevant information 
    """
    with open("turk_logs.txt", "r") as read_file, open("turk_logs_clean.txt", "w") as write_file:
        for line in read_file:
            # Figure out which lines to write back to the cleaned txt file
            if line.startswith("instance_id:") or line.startswith(" --> inputs:") \
                or line.startswith(" ------- evaluating input:") \
                or line.startswith("--> Computing the majority vote") \
                or line.startswith(" --> scores:") or line.startswith("----> per-field score:") \
                or line.startswith(" --> Per-instance overall score:") \
                or line.startswith(" --> Per-instance per-field breakdown:"):
                write_file.write(line)

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


def group_log():
    """
    Group the scores based on inputs
    """

    ret = {}

    with open("turk_logs_clean.txt", "r") as read_file:
        latest_task = ""
        for line in read_file:
            if line.startswith(" ------- evaluating input:"):
                extracted_task = extract_task_info(line)
                if extracted_task != latest_task:
                    # Skip this task since it only half finished in the logged run
                    if extracted_task == "Scalar Adjectives Identification":
                        break

                    ret[extracted_task] = []
                    latest_task = extracted_task
            
            if line.startswith(" --> Per-instance overall score:"):
                print(f"found a score line = {line}")
                score = extract_overall_score(line)
                print(f"score = {score}")
                ret[latest_task].append(score)

    return ret


if __name__ == '__main__':
    clean_log()
    res = group_log()
    print(res)