import os
import argparse
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('scores_dir', help='full path to a directory containing all pairs synonymy scores', type=str)
parser.add_argument('labels_dir', help='full path to a directory containing labels for all pairs synonymy scores', type=str)
parser.add_argument('clustering_dir', help='full path to a directory where clustering output will be written', type=str)

# Read in lists of scores and labels, converting scores to a distance array and labels to a label array.
def make_arrays(scores_path, labels_path):
    """Read scores and labels in from files. Convert them to ndarrays for clustering."""
    pairs_scores = pd.read_csv(score_path, header=None)
    labels = pd.read_csv(label_path, header=None)
    # Transform similarity (proximity) scores to distances.
    pairs_distances = 1 - pairs_scores
    distances_array = np.array(pairs_distances[0][:])
    labels_array = np.array(labels[0][:])
    return distances_array, labels_array


if __name__=='__main__':
    if args.scores_dir is not None and args.labels_dir is not None:
        # We are reading from one or more files containing word pair lists, and writing
        # pairwise relatedness scores to an output file.
        if os.path.isdir(args.source_dir):
            for subdir, dirs, files in os.walk(args.source_dir):
                for file in files:
