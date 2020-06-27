import os
import sys
import argparse
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('scores_dir', help='full path to a directory containing all pairs synonymy scores', type=str)
parser.add_argument('labels_dir', help='full path to a directory containing labels for all pairs synonymy scores', type=str)
parser.add_argument('clustering_dir', help='full path to a directory where clustering output will be written', type=str)
parser.add_argument('dendro_cutoff', help='the cutoff value for agglomerative hierarchical clustering', type=float)
args = parser.parse_args()


# Read in lists of scores and labels, converting scores to a distance array and labels to a label array.
def make_arrays(scores_path, labels_path):
    """Read scores and labels in from files. Convert them to ndarrays for clustering."""
    pairs_scores = pd.read_csv(scores_path, header=None)
    labels = pd.read_csv(labels_path, header=None)
    # Transform similarity (proximity) scores to distances.
    pairs_distances = 1 - pairs_scores
    distances_array = np.array(pairs_distances[0][:])
    labels_array = np.array(labels[0][:])
    return distances_array, labels_array


def build_linkage_matrix(distances_array):
    # Create the linkage matrix Z (perform hierarchical/agglomerative clustering).
    linkage_matrix = sch.linkage(distances_array, 'average')
    # Fix distances that have become less than 0 due to floating point errors.
    for i in range(len(linkage_matrix)):
        if linkage_matrix[i][2] < 0:
            linkage_matrix[i][2] = 0
    return linkage_matrix


def extract_dendro_name(file_path):
    file_name = os.path.basename(file_path)
    dendro_name = file_name.split('.')[0]
    return dendro_name


if __name__=='__main__':
    if (os.path.isdir(args.scores_dir) and os.path.isdir(args.labels_dir) and os.path.isdir(args.clustering_dir)):
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
        for entry in os.listdir(args.labels_dir):
            if os.path.isfile(os.path.join(args.labels_dir, entry)):
                print(entry)
                label_files.append(entry)
        if (len(score_files) < 1 or len(label_files) < 1):
            print ("Either scores or labels file list is empty: quitting!")
            sys.exit()
        if (len(score_files) != len(label_files)):
            print("The number of scores files doesn't match the number of labels files: quitting!")
            sys.exit()

        for i in range(len(score_files)):
            distances_array, labels_array = make_arrays(os.path.join(args.scores_dir, score_files[i]), \
                os.path.join(args.labels_dir, label_files[i]))
            expected_distances_count = int((len(labels_array) * (len(labels_array) - 1)) / 2)
            # The distances array should be a serialized upper triangular label x label matrix,
            # with entries below the diagonal omitted.
            if (expected_distances_count != len(distances_array)):
                print(f'The number of values in the distances list is {len(distances_array)}, but it should be {expected_distances_count}.')
                print('Skipping...')
                break
            
            linkage_matrix = build_linkage_matrix(distances_array)
            assert linkage_matrix.shape[0] == (len(labels_array) - 1), "The linkage matrix and labels array have mismatched lengths."

            # Title the dendrogram, using the labels file name.
            dendro_name = extract_dendro_name(label_files[i])
            print(dendro_name)
            # Set up the plot.
            plt.figure(figsize=(30, 15))
            title = "Image: " + dendro_name
            plt.title(title, fontsize = 22)
            plt.rc('ytick',labelsize=16)
            plt.ylabel('Cophenetic Coefficient (Distance)', fontsize=18)
            plt.axhline(y=args.dendro_cutoff, color="grey", linestyle="--")
            # Create the dendrogram, with a cutoff specified during module invocation.
            dend = sch.dendrogram(lnk, labels=labels_array, color_threshold=0.8375, leaf_font_size=16, leaf_rotation=70, count_sort='ascending')
            plt.show()

    else:
        print("Be sure to include options for scores, labels and output directories when calling this module.")