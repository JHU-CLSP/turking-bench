#!/usr/bin/env python

import argparse
from Turkle.scripts.client import TurkleClient
import sys
import os
import pandas as pd
from colorama import init as colorama_init
from colorama import Fore, Back, Style

colorama_init(autoreset=True)

parser = argparse.ArgumentParser(
    description="Upload a batch of tasks to Turkle",
    epilog="Requires a template and the batch CSV",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument("-u", help="admin username", default="admin")
parser.add_argument("-p", help="admin password", default="123")
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
for root, dirs, _ in os.walk('../tasks'):
    for dir in dirs:
        temp = ''
        csvpath = ''
        dir_path = os.path.join(root, dir)
        if "batch-" in dir:
            # skip because this is just a directory to store the results of human evaluation
            continue
        for file in os.listdir(dir_path):
            if file.endswith('.html'):
                temp = os.path.join(dir_path, file)
            if file.endswith('input.csv'):
                csvpath = os.path.join(dir_path, file)
                input_encoding = 'utf8'
                output_encoding = 'utf8'
                df = pd.read_csv(csvpath, encoding=input_encoding)
                df.to_csv(csvpath, index=False, encoding=output_encoding)
        print(f"{Fore.BLUE} -> {dir}")
        options = Options(batch_name=dir,
                          project_name=dir,
                          template=temp,
                          csv=csvpath)
        result = client.upload(options)
        if result:
            print(f"{Fore.GREEN}Success")
