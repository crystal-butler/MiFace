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
args = parser.parse_args()

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
    if args.scores_dir is not None and args.labels_dir is not None and args.clustering_dir is not None:
        # We are reading from one or more files containing word pair synonymy scores
        # and their associated labels, clustering the distances between scores,
        # generating a dendrogram and some statistics from the clustering, and writing
        # that output to a file.
        score_files = []
        label_files = []
        for entry in os.listdir(args.scores_dir):
            if os.path.isfile(os.path.join(args.scores_dir, entry)):
                print(entry)
                score_files.append(entry)
        for entry in os.listdir(args.labels_path):
            if os.path.isfile(os.path.join(args.labels_dir, entry)):
                print(entry)
                label_files.append(entry)
    else:
        print("Be sure to include options for scores, labels and output directories when calling this module.")