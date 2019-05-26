# Crystal Butler
# 2019/05/26
# Generate and save a vocabulary file for a given list of word-feature vectors.
# Vectors must contain the vocabulary word as the first element, followed by
# any number of space-separated feature values.

import argparse

# Read in options.
parser = argparse.ArgumentParser()
parser.add_argument('vectors_file', help="a file of word-feature vectors", type=str)
parser.add_argument('output_file', help="a file path for writing the vocabulary", type=str)
args = parser.parse_args()

# Constant, used to format output file name.
SUFFIX = ".txt"


def make_vocab():
    vals = []
    with open(args.vectors_file, 'r') as f, open(args.output_file, 'w') as o:
        for line in f:
            vals = line.rstrip().split(' ')
            o.write("{}\n".format(vals[0]))
        return 0


if __name__ == "__main__":
    vocab = make_vocab()
