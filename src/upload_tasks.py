#!/usr/bin/env python

import argparse
from Turkle.scripts.client import TurkleClient
import sys
import os
import pandas as pd

parser = argparse.ArgumentParser(
    description="Upload a batch of tasks to Turkle",
    epilog="Requires a template and the batch CSV",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument("-u", help="admin username", required=True)
parser.add_argument("-p", help="admin password")
parser.add_argument("--server", help="protocol://hostname:port", default="http://localhost:8000")
args = parser.parse_args()

class Options:
    def __init__(self, batch_name, project_name, template, csv):
        self.login = 0
        self.num = 1
        self.batch_name = batch_name    
        self.project_name = project_name
        self.template = template
        self.csv = csv


client = TurkleClient(args.server, args.u, args.p)
for root, dirs, files in os.walk('../tasks'):
    for dir in dirs:
        try:
            temp = ''
            csvpath = ''
            dir_path = os.path.join(root, dir)
            for file in os.listdir(dir_path):
                if file.endswith('.html'):
                    temp = os.path.join(dir_path, file)
                if file.endswith('.csv'):
                    csvpath = os.path.join(dir_path, file)
                    input_encoding = 'utf8'
                    output_encoding = 'utf8'
                    df = pd.read_csv(csvpath, encoding=input_encoding)
                    df.to_csv(csvpath, index=False, encoding=output_encoding)
            print(dir)
            options = Options(batch_name=dir, project_name=dir,
                              template=temp,
                              csv=csvpath)
            result = client.upload(options)
            if result:
                print("Success")
        except:
            continue
