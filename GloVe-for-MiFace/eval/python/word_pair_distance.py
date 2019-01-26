#!/usr/bin/python
import os
import argparse
import numpy as np
np.seterr(divide='ignore', invalid='ignore')  # fix divide runtime error (when dividing by zeros)

parser = argparse.ArgumentParser()
parser.add_argument('vocab_file', help='a file of vocabulary words', type=str)
parser.add_argument('vectors_file', help='a file of word-feature vectors based on the vocabulary', type=str)
parser.add_argument('--source_dir', help="a directory containing lists of word pairs; requires a value for output_dir \
to be input to work",
                    default=None, type=str)
parser.add_argument('--output_dir', help="a directory to write similarity value files to", default=None, type=str)
args = parser.parse_args()


def generate():
    with open(args.vocab_file, 'r') as f:
        words = [x.rstrip().split(' ')[0] for x in f.readlines()]
    with open(args.vectors_file, 'r') as f:
        vectors = {}
        for line in f:
            # Populate the dictionary with word feature lists, indexed by word.
            vals = line.rstrip().split(' ')
            vectors[vals[0]] = [float(x) for x in vals[1:]]

    # Create word:index and index:word maps.
    vocab = {w: idx for idx, w in enumerate(words)}
    ivocab = {idx: w for idx, w in enumerate(words)}

    # Create a word x feature matrix.
    vocab_size = len(words)
    vector_dim = len(vectors[ivocab[0]])
    W = np.zeros((vocab_size, vector_dim))
    for word, v in vectors.items():
        if word == '<unk>':
            continue
        W[vocab[word], :] = v

    # Normalize each word vector to unit variance.
    W_norm = np.zeros(W.shape)
    d = (np.sum(W ** 2, 1) ** (0.5))
    W_norm = (W.T / d).T
    return (W_norm, vocab, ivocab)


def distance(W, vocab, ivocab, input_term1, input_term2):
    if input_term1 not in vocab or input_term2 not in vocab:
        # Magic number to indicate that some word wasn't in the vocabulary.
        return -1
    else:
        vec_result1 = W[vocab[input_term1], :]

    # Normalize the word vector. The feature matrix has already been normalized.
    vec_norm = np.zeros(vec_result1.shape)
    d = (np.sum(vec_result1 ** 2,) ** (0.5))
    vec_norm = (vec_result1.T / d).T

    # Calculate all distances to our first input word.
    dist = np.dot(W, vec_norm.T)
    index1 = vocab[input_term1]
    index2 = vocab[input_term2]

    # Set the first word's distance to itself to one for a perfect match, then
    # look up the distance to the second word.
    dist[index1] = 1
    return dist[index2]


if __name__ == "__main__":
    W, vocab, ivocab = generate()
    if args.source_dir is not None and args.output_dir is not None:
        # We are reading from one or more files containing word pair lists, and writing
        # pairwise similarity scores to an output file.
        # with open(args.source_dir, 'r') as root_dir:
        for subdir, dirs, files in os.walk(args.source_dir):
            for file in files:
                f = open(subdir + '/' + file, 'r')
                f2 = open(args.output_dir + file, 'w')
                for line in f:
                    array = []
                    for word in line.split():
                        array.append(word)
                    input_term1 = array[0]
                    input_term2 = array[1]
                    similarity = distance(W, vocab, ivocab, input_term1, input_term2)
                    if similarity == -1:
                        # One of the words wasn't in the vocabulary, so write nothing to the file.
                        continue
                    else:
                        f2.write("%s%s%s\n" % (input_term1.ljust(20), input_term2.ljust(20), similarity))
                f2.close()
                f.close()
    else:
        # Get pairs of words from the command line and print similarity scores to standard out.
        while True:
            input_term1 = input("\n Enter the first of two words (type EXIT to quit): ")
            if input_term1 == 'EXIT':
                break
            input_term2 = input("Enter the second of two words (type EXIT to quit): ")
            if input_term2 == 'EXIT':
                break
            else:
                similarity = distance(W, vocab, ivocab, input_term1, input_term2)
                if similarity == -1:
                    print("Oops! One of your words wasn't in the vocabulary.")
                else:
                    print("From -1 to 1, the simlarity of %s and %s is %f." % (input_term1, input_term2, similarity))
