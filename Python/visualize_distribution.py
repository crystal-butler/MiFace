import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('scores_dir', help='full path to a directory containing all pairs synonymy scores', type=str)
parser.add_argument('histogram_dir', help='full path to a directory where the histogram plot will be written', type=str)
parser.add_argument('bin_count', help='the number of bins used in the histogram', type=int)
args = parser.parse_args()


def concatenate_scores():
    score_count = 0
    all_scores = []
    for entry in sorted(os.listdir(args.scores_dir)):
        if os.path.isfile(os.path.join(args.scores_dir, entry)):
            if not entry.startswith('.'):
                with open(os.path.join(args.scores_dir, entry), 'r') as f:
                    for line in f:
                        score = line.strip()
                        all_scores.append(score)
                        score_count += 1
    assert len(all_scores) == score_count
    return all_scores


def sort_scores(scores):
    scores.sort()
    return scores


def make_array(scores):
    scores_array = np.array(scores).astype(np.float)
    return(scores_array)


if __name__ == '__main__':
    scores_all = concatenate_scores()
    print(len(scores_all))
    scores_sorted = sort_scores(scores_all)
    assert len(scores_all) == len(scores_sorted)
    scores_array = make_array(scores_sorted)
    assert (scores_array.shape)[0] == len(scores_sorted)

    mu = np.mean(scores_array)
    sigma = np.std(scores_array)
    print(f'Mean of {scores_array.shape[0]} scores is {mu}, with standard deviation {sigma}.')

    # Build the histogram figure.
    fig, ax = plt.subplots()
    # Plot the histogram of the data.
    n, bins, patches = ax.hist(scores_array, args.bin_count, density=1)

    # plt.show()