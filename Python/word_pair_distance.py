#!/usr/bin/python

# Crystal Butler
# 2019/03/01
# Adapted from https://github.com/stanfordnlp/GloVe/blob/master/eval/python/distance.py.
# Requires pretrained word embeddings (semantic vectors) and lists of word pairs as input.
# Words that are misspelled or not in the vocabulary of the embeddings are silently skipped.
# The script outputs four sets of files, one file per label pair, containing:
#   -- a label pair and relatedness score on each line (to args.output_dir)
#   -- words not found in the vocabulary, if any (to args.output_dir/Errors)
#   -- labels successfully processed by the script (to args.output_dir/Label_Lists)
#   -- relatedness scores only (to args.output_dir/Score_Lists)
# The third and fourth files are required for performing clustering in MATLAB.

import os
import shutil
import argparse
import math
import numpy as np
np.seterr(divide='ignore', invalid='ignore')  # fix runtime error when dividing by zero

parser = argparse.ArgumentParser()
parser.add_argument('vectors_file', help='a file of word-features vectors', type=str)
parser.add_argument('--vocab_file', help='a file of vocabulary words; if not given, one will be generated \
from vectors_file', default=None, type=str)
parser.add_argument('--source_dir',
                    help="an optional directory containing lists of word pairs to score;\
                     requires a value for output_dir",
                    default=None, type=str)
parser.add_argument('--output_dir', help="a directory to write relatedness value files to", default=None, type=str)
args = parser.parse_args()

if (args.output_dir is not None):
    # Set up directories for our output files, if need be.
    if not os.path.exists(args.output_dir + "Errors"):
        os.makedirs(args.output_dir + "Errors")
    err = args.output_dir + "Errors/"
    if not os.path.exists(args.output_dir + "Label_Lists"):
        os.makedirs(args.output_dir + "Label_Lists")
    lab = args.output_dir + "Label_Lists/"
    if not os.path.exists(args.output_dir + "Label_and_Score_Lists"):
        os.makedirs(args.output_dir + "Label_and_Score_Lists")
    labscr = args.output_dir + "Label_and_Score_Lists/"
    if not os.path.exists(args.output_dir + "Score_Lists"):
        os.makedirs(args.output_dir + "Score_Lists")
    scr = args.output_dir + "Score_Lists/"


def generate():
    if args.vocab_file is not None:
        # Parse the optionally provided vocabulary file.
        with open(args.vocab_file, 'r', encoding='utf-8') as f:
            words = [x.rstrip().split(' ')[0] for x in f.readlines()]
    # Semantic vectors (or word embeddings) are the result of training a ML model to represent word relatedness.
    with open(args.vectors_file, 'r', encoding='utf-8', errors='ignore') as f:
        # The pre-trained semantic vectors will go into a Python dictionary.
        # Dictionaries are key:value indexed; lookup is done via hash function and should be O(1) time complexity.
        # But the dictionary is just an intermediate. Lookups will be done against a numpy ndarray, constructed later.
        vectors = {}
        # The "words" list is an intermediate. The dictionary used in processing is constructed later.
        words = []
        vals = []
        for line in f:
            # Populate the dictionary with word feature lists, indexed by word.
            vals = line.rstrip().split(' ')
            # The vocabulary file gets created here, if one wasn't provided on script invocation.
            if args.vocab_file is None:
                words.append(vals[0])
            vectors[vals[0]] = [float(x) for x in vals[1:]]
        vector_dim = len(vals) - 1  # Number of features in a semantic vector, minus the vocab word at the beginning.
        vocab_size = len(words)

    # Create word:numbered index dictionary from the "words" list, to be used for vector lookups.
    vocab = {w: idx for idx, w in enumerate(words)}

    # Create a numpy ndarray of semantic vectors. The ndarray is indexed by row number, while we need to index by word.
    # But we'll be using the O(1) lookup time from our vocab dictionary to translate from input word to row number.
    W = np.zeros((vocab_size, vector_dim))
    for word, v in vectors.items():
        if word == '<unk>':
            continue
        W[vocab[word], :] = v

    # Normalize each word vector to unit variance.
    W_norm = np.zeros(W.shape)
    d = (np.sum(W ** 2, 1) ** (0.5))
    W_norm = (W.T / d).T
    return (W_norm, vocab)


def distance(W, vocab, input_term1, input_term2):
    if input_term1 not in vocab or input_term2 not in vocab:
        # Magic number to indicate that some word wasn't in the vocabulary.
        return -100

    # Cosine similarity is calculated as (vector1 • vector2) / (\\vector1\\ * \\vector2\\). But the magnitudes of
    # our vectors have all been normalized to 1, so this reduces to a vector dot product.
    distance = np.dot(W[vocab[input_term1]], W[vocab[input_term2]])
    return distance


if __name__ == "__main__":
    W, vocab = generate()
    if args.source_dir is not None and args.output_dir is not None:
        # We are reading from one or more files containing word pair lists, and writing
        # pairwise relatedness scores to an output file.
        if os.path.isdir(args.source_dir):
            for subdir, dirs, files in os.walk(args.source_dir):
                for file in files:
                    # Check to see whether the ID list generated in create_all_pairs.py is in the input directory.
                    # If it is, move it.
                    if (file == "ID_list.txt"):
                        shutil.copyfile((subdir + "/" + file), (args.output_dir + file))
                        os.remove(subdir + "/" + file)

                    ID = file.rstrip().split("_")[0]  # relies on file name beginning with ID_

                    # On Mac, automatically generated .DS_Store files will cause an error, so ignore hidden files.
                    if not ((file.startswith('.')) or (file == "ID_list.txt")):
                        # Get all our needed files open for business.
                        f_in = open(subdir + '/' + file, 'r')
                        f_err = open(err + ID + "_errors.txt", 'w')
                        f_lab = open(lab + ID + "_labels.txt", 'w')
                        f_scr = open(scr + ID + "_scores.txt", 'w')
                        f_labscr = open(labscr + ID + ".txt", 'w')

                        # Calculate n-1 for original number of labels used to generate the all-pairs list.
                        cnt = 0
                        for cnt, l in enumerate(f_in):
                            pass
                        n_minus = math.floor(math.sqrt(cnt * 2))
                        f_in.seek(0)

                        # Calculate relatedness scores.
                        linecnt = n_minus
                        for line in f_in:
                            # Keeping track of when to write to the labels file.
                            if (linecnt == 0):
                                n_minus -= 1
                                linecnt = n_minus
                            array = []
                            # Get the relatedness score, and write to the appropriate file(s).
                            for word in line.split():
                                array.append(word)
                            input_term1 = array[0]
                            input_term2 = array[1]
                            relatedness = distance(W, vocab, input_term1, input_term2)
                            if relatedness == -100:
                                # One of the words wasn't in the vocabulary, so write to the error file.
                                f_err.write("%s%s%s\n" % (input_term1.ljust(20), input_term2.ljust(20), relatedness))
                            else:
                                f_labscr.write("%s%s%s\n" % (input_term1.ljust(20), input_term2.ljust(20), relatedness))
                                f_scr.write("%s\n" % (relatedness))
                                if (linecnt == 1):
                                    f_lab.write("%s\n" % (array[0]))
                                if ((linecnt == 1) and (n_minus == 1)):
                                    f_lab.write("%s\n" % (array[1]))
                            linecnt -= 1

                        # Close up shop for this round of processing.
                        f_labscr.close()
                        f_scr.close()
                        f_lab.close()
                        f_err.close()
                        f_in.close()
        else:
            print("The source directory is empty, or you input a file name rather than a directory name: exiting.")
    else:
        # Get pairs of words from the command line and print relatedness scores to standard out.
        while True:
            input_term1 = input("\nEnter the first of two words (type EXIT to quit): ")
            if input_term1 == 'EXIT':
                break
            input_term2 = input("Enter the second of two words (type EXIT to quit): ")
            if input_term2 == 'EXIT':
                break
            else:
                relatedness = distance(W, vocab, input_term1, input_term2)
                if relatedness == -100:
                    print("Oops! One of your words wasn't in the vocabulary.")
                else:
                    print("From -1 to 1, the similarity of %s and %s is %f." % (input_term1, input_term2, relatedness))
