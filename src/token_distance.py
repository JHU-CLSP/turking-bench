import csv
import os
import re
import chardet
from transformers import GPT2Tokenizer 
import Levenshtein


def token_distance(text1, text2):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokens1 = tokenizer.tokenize(text1)
    tokens2 = tokenizer.tokenize(text2)
    distance = Levenshtein.distance("".join(tokens1), "".join(tokens2))
    return distance


def main():
    root_folder = "tasks"
    csv_file = "token_distance.csv"
    folders = os.listdir(root_folder)
    distances = [[0 for _ in folders] for _ in folders]
    for folder1 in folders:
        path1 = os.path.join(root_folder, folder1, "htmltext.txt")
        encoding = chardet.detect(open(path1, "rb").read())["encoding"]
        with open(path1, "r", encoding=encoding) as file:
            text1 = file.read()

        for folder2 in folders:
            path2 = os.path.join(root_folder, folder2, "htmltext.txt")
            encoding = chardet.detect(open(path2, "rb").read())["encoding"]
            with open(path2, "r", encoding=encoding) as file:
                text2 = file.read()
                distance = token_distance(text1, text2)
                distances[folders.index(folder1)][folders.index(folder2)] = distance

    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["-"] + folders)
        for folder1 in folders:
            row = [folder1]
            for folder2 in folders:
                row.append(distances[folders.index(folder1)][folders.index(folder2)])
            writer.writerow(row)

if __name__ == "__main__":
    main()
