import pandas as pd
import os
"""
Script for removing unnecessary data from csv files
"""

# remove these columns from csv file: HITId, HITTypeId, Reward, CreationTime, MaxAssignments, RequesterAnnotation, AssignmentDurationInSeconds, AutoApprovalDelayInSeconds, Expiration, NumberOfSimilarHITs, LifetimeInSeconds, AssignmentId, WorkerId, AssignmentStatus, AcceptTime, SubmitTime, AutoApprovalTime, ApprovalTime, RejectionTime, RequesterFeedback, WorkTimeInSeconds, LifetimeApprovalRate, Last30DaysApprovalRate, Last7DaysApprovalRate
def remove_columns(csv_file):
    df = pd.read_csv(csv_file, low_memory=False)
    drop_list = ['HITId', 'HITTypeId', 'Reward', 'CreationTime', 'MaxAssignments', 'RequesterAnnotation', 'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds', 'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds', 'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime', 'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime', 'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate', 'Last30DaysApprovalRate', 'Last7DaysApprovalRate']
    thisFilter = df.filter(drop_list)
    df.drop(thisFilter, inplace=True, axis=1)
    df.to_csv(csv_file , encoding='utf-8-sig', index=False)

if __name__ == '__main__':
    for root, dirs, files in os.walk('tasks'):
        for file in files:
            if file.endswith('.csv'):
                print('Cleaning ' + file)
                remove_columns(os.path.join(root, file))