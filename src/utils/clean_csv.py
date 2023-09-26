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

def clean_empty(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    df.fillna(value="None", inplace=True)
    df.replace("", "None", inplace=True) # undo the previous line
    df.to_csv(csv_file , encoding='utf-8-sig', index=False)

if __name__ == '__main__':
    files_to_edit = ["HTER - longer sentences -27 Sep 1129"]
    for root, dirs, files in os.walk('tasks'):
        for file in files:
            if file.endswith('.csv') and root.split("/")[1] in files_to_edit and file.startswith('batch'):
                print('Cleaning ' + file)
                # remove_columns(os.path.join(root, file))
                clean_empty(os.path.join(root, file))