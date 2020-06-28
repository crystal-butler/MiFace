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
    scores_array = scores_array.round(decimals=6)
    return(scores_array)


def trim_scores(scores_array):
    trimmed_scores = scores_array[scores_array < 1]
    return trimmed_scores


def calculate_statistics(scores_array):
    mu = np.mean(scores_array)
    sigma = np.std(scores_array)
    a_min = np.min(scores_array)
    a_max = scores_array.max()
    return mu, sigma, a_min, a_max


if __name__ == '__main__':
    scores_all = concatenate_scores()
    print(f'Read in {len(scores_all)} scores.')
    scores_sorted = sort_scores(scores_all)
    assert len(scores_all) == len(scores_sorted)
    scores_array = make_array(scores_sorted)
    assert (scores_array.shape)[0] == len(scores_sorted)
    scores_trimmed = trim_scores(scores_array)
    print(f'After removing scores = 1, there are {scores_trimmed.shape[0]} scores.')
    
    # Calculate statistics of the distribution.
    mu, sigma, a_min, a_max = calculate_statistics(scores_trimmed)
    print(f'Mean of {scores_trimmed.shape[0]} scores is {mu}, with standard deviation {sigma}.')
    print(f'The minimum is {a_min} and the maximum non-1 value is {a_max}.')

    # Build the histogram figure.
    fig, ax = plt.subplots()
    # Plot the histogram of the data.
    n, bins, patches = ax.hist(scores_trimmed, args.bin_count, density=1)
    plt.rc('ytick',labelsize=16)
    # Add a 'best fit' line.
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
        np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    ax.plot(bins, y, '--')
    # Format the figure.
    ax.set_xlabel('Scores', fontsize=16)
    ax.set_ylabel('Probability density', fontsize=16)
    ax.set_title('Histogram of Synonymy Scores', fontsize=18)

    plt.show()
    plt.close()