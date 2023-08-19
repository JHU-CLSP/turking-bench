"""
We used this file to compute the distances between pairs of tasks.
"""

import csv
import os
import chardet
from transformers import GPT2Tokenizer
from tqdm import tqdm
from rouge_score import rouge_scorer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

default_rouge_scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)


def token_distance(text1, text2):
    # compute rouge distance between the two texts
    scores = default_rouge_scorer.score(prediction=text1, target=text2)
    return scores["rougeL"].fmeasure


def main():
    root_folder = "tasks"
    folders = os.listdir(root_folder)
    # exclude hidden folders
    folders = [folder for folder in folders if not folder.startswith(".")]
    distances = [[0 for _ in folders] for _ in folders]

    for folder1 in tqdm(folders):
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

    with open("../token_distance.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["-"] + folders)
        for folder1 in folders:
            row = [folder1]
            for folder2 in folders:
                row.append(distances[folders.index(folder1)][folders.index(folder2)])
            writer.writerow(row)


if __name__ == "__main__":
    main()
