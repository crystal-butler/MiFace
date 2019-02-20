#!/usr/bin/python
import os
import argparse
import numpy as np
np.seterr(divide='ignore', invalid='ignore')  # Fix runtime error (when dividing by zeros).

parser = argparse.ArgumentParser()
parser.add_argument('vectors_file', help='a file of word-features vectors', type=str)
parser.add_argument('--vocab_file', help='a file of vocabulary words; if not given, one will be generated \
from vectors_file', default=None, type=str)
parser.add_argument('--source_dir', help="a directory containing lists of word pairs; requires a value for output_dir",
                    default=None, type=str)
parser.add_argument('--output_dir', help="a directory to write relatedness value files to", default=None, type=str)
args = parser.parse_args()


def generate():
    if args.vocab_file is not None:
        # Parse the optionally provided vocabulary file.
        with open(args.vocab_file, 'r') as f:
            words = [x.rstrip().split(' ')[0] for x in f.readlines()]
    # Semantic vectors (or word embeddings) are the result of training a ML model to represent word relatedness.
    with open(args.vectors_file, 'r') as f:
        # The pre-trained semantic vectors will go into a Python dictionary.
        # Dictionaries are key:value indexed; lookup is done via hash function and should be O(1) time complexity.
        # But the dictionary is just an intermediate. Lookups will be done against a numpy ndarray, constructed later.
        vectors = {}
        # The "words" list is an intermediate. The dictionary used in processing is construceted later.
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
                    # On Mac, automatically generated .DS_Store files will cause an error, so ignore hidden files.
                    if not file.startswith('.'):
                        f = open(subdir + '/' + file, 'r')
                        f2 = open(args.output_dir + file, 'w')
                        for line in f:
                            array = []
                            for word in line.split():
                                array.append(word)
                            input_term1 = array[0]
                            input_term2 = array[1]
                            relatedness = distance(W, vocab, input_term1, input_term2)
                            if relatedness == -100:
                                # One of the words wasn't in the vocabulary, so write nothing to the file.
                                continue
                            else:
                                f2.write("%s%s%s\n" % (input_term1.ljust(20), input_term2.ljust(20), relatedness))
                        f2.close()
                        f.close()
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
                    print("From -1 to 1, the simlarity of %s and %s is %f." % (input_term1, input_term2, relatedness))
