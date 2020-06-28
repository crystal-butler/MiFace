import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('scores_dir', help='full path to a directory containing all pairs synonymy scores', type=str)
parser.add_argument('histogram_dir', help='full path to a directory where the histogram plot will be written', type=str)
parser.add_argument('bin_count', help='the number of bins used in the histogram', type=float)
args = parser.parse_args()


def concatenate_scores():
    all_scores = []
    for entry in sorted(os.listdir(args.scores_dir)):
        if os.path.isfile(os.path.join(args.scores_dir, entry)):
            if not entry.startswith('.'):
                with open(os.path.join(args.scores_dir, entry), 'r') as f:
                    for line in f:
                        score = line.strip()
                        all_scores.append(score)
    print(len(all_scores))
    return all_scores


def sort_scores(all_scores):



if __name__ == '__main__':
    all_scores = concatenate_scores()
