import csv
import os
import re
import chardet
import pandas as pd
from transformers import GPT2Tokenizer 


def main():
    root_folder = "tasks"
    input_type_stats = []
    folders = os.listdir(root_folder)
    for folder in folders:
        path = os.path.join(root_folder, folder, "htmltext.txt")
        encoding = chardet.detect(open(path, "rb").read())["encoding"]
        with open(path, "r", encoding=encoding) as file:
            text = file.read()
            tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            tokens1 = tokenizer.tokenize(text)

            input_type_stats.append({
                'Directory': folder,
                'Number of Tokens': len(tokens1),
            })
    print(input_type_stats)
    stats_df = pd.DataFrame(input_type_stats)
    stats_df.to_csv('token_size.csv', index=False)

if __name__ == "__main__":
    main()