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


def make_output_subdir():
    if not os.path.exists(args.histogram_dir):
        os.makedirs(args.histogram_dir)
    return


def concatenate_scores():
    """Get all the scores from a set of files in a directory,
    and put them into a single list."""
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
    """Turn a list into a numpy array."""
    scores_array = np.array(scores).astype(np.float)
    return(scores_array)


def trim_scores(scores_array):
    """Only consider synonymy scores for pairs of different words.
    Same word pairs have a synonymy score of 1."""
    trimmed_scores = scores_array[scores_array < 1]
    return trimmed_scores


def normalize_array(scores_array):
    scores_norm = (scores_array - np.min(scores_array))/np.ptp(scores_array)
    scores_norm = scores_norm.round(decimals=6)  # clean up floating point errors and reduce significant digits
    return scores_norm


def calculate_statistics(scores_array):
    """Calculate descriptive statistics for the scores distribution."""
    mu = np.mean(scores_array)
    sigma = np.std(scores_array)
    a_min = np.min(scores_array)
    a_max = scores_array.max()
    return mu, sigma, a_min, a_max


def make_output_filenames():
    """Write statistics and histogram figure to the specified directory."""
    hist_file = os.path.join(args.histogram_dir, 'distribution_histogram.png')
    stats_file = os.path.join(args.histogram_dir, 'distribution_stats.txt')
    return hist_file, stats_file


def format_distribution_stats(mu, sigma, a_min, a_max):
    """Pretty print layout for distribution statistics; can be appended to the histogram or saved out as a file."""
    stats_printout = '---------------------------------------------------------------------------------\n'
    stats_printout += 'Synonymy Scores Distribution Statistics\n---------------------------------------------------------------------------------\n'
    stats_printout += ('Mean: ' + str(mu) + '\n')
    stats_printout += ('Standard Deviation: ' + str(sigma) + '\n')
    stats_printout += ('Minimum: ' + str(a_min) + '\n')
    stats_printout += ('Maximum: ' + str(a_max) + '\n')
    return stats_printout


if __name__ == '__main__':
    make_output_subdir()
    scores_all = concatenate_scores()
    print(f'Read in {len(scores_all)} scores.')
    scores_sorted = sort_scores(scores_all)
    assert len(scores_all) == len(scores_sorted)
    scores_array = make_array(scores_sorted)
    assert (scores_array.shape)[0] == len(scores_sorted)
    scores_norm = normalize_array(scores_array)
    assert scores_array.shape[0] == scores_norm.shape[0]
    scores_trimmed = trim_scores(scores_norm)
    print(f'After removing scores = 1, there are {scores_trimmed.shape[0]} scores.')
    
    # Calculate statistics of the distribution.
    mu, sigma, a_min, a_max = calculate_statistics(scores_trimmed)
    stats_printout = format_distribution_stats(mu, sigma, a_min, a_max)

    # Build the histogram figure.
    fig, ax = plt.subplots(figsize=(14, 8.5))  #(width, height) in inches
    # Plot the histogram of the data.
    n, bins, patches = ax.hist(scores_trimmed, args.bin_count, density=1)
    plt.figtext(0.02, 0.12, stats_printout, horizontalalignment='left', verticalalignment='center', fontsize=14)
    plt.subplots_adjust(bottom=0.32, top=0.95, right=0.98, left=0.06)
    # Add a 'best fit' line.
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
        np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    ax.plot(bins, y, '--')
    # Format the figure.
    y_label = 'Probability Density'
    x_label = 'Synonymy Scores: ' + str(args.bin_count) + ' Bins'
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel(y_label, fontsize=16)
    ax.set_title('Histogram of Synonymy Scores', fontsize=18)

    # Save the figure and statistics.
    hist_file, stats_file = make_output_filenames()
    with open(stats_file, 'w') as f_stat:
        f_stat.write(stats_printout)
    plt.savefig(hist_file, format='png')

    # Display the figure.
    plt.show()
    plt.close()