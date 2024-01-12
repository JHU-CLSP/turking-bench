import pandas as pd
import os
"""
Script for removing unnecessary data from csv files before releasing them. 
"""

# remove these columns from csv file: HITId, HITTypeId, Reward, CreationTime, MaxAssignments, RequesterAnnotation, AssignmentDurationInSeconds, AutoApprovalDelayInSeconds, Expiration, NumberOfSimilarHITs, LifetimeInSeconds, AssignmentId, WorkerId, AssignmentStatus, AcceptTime, SubmitTime, AutoApprovalTime, ApprovalTime, RejectionTime, RequesterFeedback, WorkTimeInSeconds, LifetimeApprovalRate, Last30DaysApprovalRate, Last7DaysApprovalRate
def remove_columns(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    drop_list = ['HITId', 'HITTypeId', 'Reward', 'CreationTime', 'MaxAssignments', 'RequesterAnnotation', 'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds', 'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds', 'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime', 'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime', 'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate', 'Last30DaysApprovalRate', 'Last7DaysApprovalRate']
    thisFilter = df.filter(drop_list)
    df.drop(thisFilter, inplace=True, axis=1)
    df.to_csv(csv_file , encoding='utf-8-sig', index=False)

def clean_checkboxes(csv_file):
    true = [True]
    false = [False]
    df = pd.read_csv(csv_file, low_memory=False)
    for i, row in df.iterrows():
        for col in df.columns:
            if col.startswith('Answer'):
                if row[col] in true:
                    df.loc[i, col] = "on"
                elif row[col] in false:
                    df.loc[i, col] = ""
    df.to_csv(csv_file, index=False)

# cleaning cases where the checkbox solutions are like q1.1 q1.2 q1.3 where these are question 1 answer 1 answer 2 answer 3 etc.
# and there is False in all the ones except a True in the right answer, like True in answer 2
# Replace with q1 value of 2
# This was used to get the answers (last few columns) for the wikiHow Step Membership Task
def clean_checkboxes_true(csv_file):
    true = [True, "True"]
    df = pd.read_csv(csv_file, low_memory=False)
    answers_df = pd.DataFrame()
    # new answer column names
    column_names = ['Answer.candidate' + str(i) for i in range(1, 16)]

    # Add the columns to the answers DataFrame
    for col_name in column_names:
        answers_df[col_name] = ""

    for i, row in df.iterrows():
        for col in df.columns:
            if col.startswith('Answer.candidate'):
                if row[col] in true:
                    answers_df.at[i, col[:-2]] = col[-1]

    # Append the new DataFrame to the original DataFrame
    df = pd.concat([df, answers_df], axis=1)
    df.to_csv(csv_file, index=False)

# This is to solve cases when answer is like Answer.candidate_3.1 Answer.candidate_3.2 has True/False when answer should just be
# in Answer.candidate_3 and the value like 1 or 2
def clean_split_up_radio(csv_file):
    true = [True, "True"]
    df = pd.read_csv(csv_file, low_memory=False)
    answers_df = pd.DataFrame()
    column_names = []
    for col in df.columns:
        if col.startswith('Answer'):
            # Split the column name at the last period
            beginning, value = col.rsplit(".", 1)
            column_names.append(beginning) # substring off last answer bit after the last period

    # Add the columns to the answers DataFrame
    for col_name in column_names:
        answers_df[col_name] = ""

    for i, row in df.iterrows():
        for col in df.columns:
            if col.startswith('Answer'):
                if row[col] in true:
                    # Split the column name at the last period
                    beginning, value = col.rsplit(".", 1)
                    column_names.append(beginning) # substring off last answer bit after the last period
                    answers_df.at[i, beginning] = value

    # Append the new DataFrame to the original DataFrame
    df = pd.concat([df, answers_df], axis=1)
    df.to_csv(csv_file, index=False)

def convert_on_to_yes(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    for i, row in df.iterrows():
        for col in df.columns:
            if col.startswith('Answer.optradio'):
                if row[col] == "on":
                    df.loc[i, col] = "yes"
    df.to_csv(csv_file , encoding='utf-8-sig', index=False)

# Clean an empty cell with certain properties (in certain col) into a specified value
def clean_empty(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    for i, row in df.iterrows():
        for col in df.columns:
            if col.startswith("Answer."):
                continue
            if pd.isnull(row[col]) or row[col] == "":
                df.loc[i, col] = " "
    df.to_csv(csv_file , encoding='utf-8-sig', index=False)

# Make certain columns empty if not specific values
def make_empty(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    for i, row in df.iterrows():
        for col in df.columns:
            if not (col.startswith("Answer.") and col.endswith("box")):
                continue
            if pd.isnull(row[col]) or row[col] == "" or row[col] == "no":
                continue

            df.loc[i, col] = ""
    df.to_csv(csv_file , encoding='utf-8-sig', index=False)

# Clean an "Empty" cell with certain properties (in certain col) into an actually empty cell, reversing clean_empty 
def clean_unempty(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    for i, row in df.iterrows():
        for col in df.columns:
            if not col.startswith("Answer."):
                continue
            if row[col] == "Empty":
                df.loc[i, col] = ""
    df.to_csv(csv_file , encoding='utf-8-sig', index=False)

if __name__ == '__main__':
    files_to_edit = ["winogrande validation (grammar) additional_ph", "atomic_event2event-effects 4"]
    for root, dirs, files in os.walk('tasks'):
        for file in files:
            if file.endswith('.csv') and file.startswith('batch'):
                if root.split("/")[1] in files_to_edit:
                    print('Cleaning ' + os.path.join(root, file))
                    clean_empty(os.path.join(root, file))