# Crystal Butler
# 2019/03/05
# Check all label lists in a directory to see whether any labels aren't found in a given vocabulary.
# A vocabulary file can be generated from a set of word embeddings (semantic vectors) if desired.
# This script assumes that files are formatted to be input into create_all_pairs.py.
# It will take a single file of (ID, label) pairs, or multiple files with labels only.
# Files must in a dedicated directory, source_dir.

import os
import argparse

# Read in options.
parser = argparse.ArgumentParser()
parser.add_argument('source_dir', help="a directory containing lists of words to check", type=str)
parser.add_argument('error_dir', help="a directory where vocabulary errors are written", type=str)
parser.add_argument('vocab_out', help="a file where words successfully found in the reference vocabulary are saved", default=None, type=str)
parser.add_argument('--vectors_file', help='a file of word-features vectors', default=None, type=str)
parser.add_argument('--vocab_ref', help='a file of vocabulary words; if not given, one will be generated \
from vectors_file', default=None, type=str)

args = parser.parse_args()

# Constants, used to format output file names.
ZERO_PAD = 4
SUFFIX = ".txt"


def make_vocab():
    vals = []
    vocab = []
    if(args.vocab_ref is None):
        with open(args.vectors_file, 'r') as f:
            for line in f:
                vals = line.rstrip().split(' ')
                vocab.append(vals[0])
            return vocab
    else:
        with open(args.vocab_ref, 'r') as f:
            for line in f:
                for line in f:
                    vals = line.rstrip().split(' ')
                    vocab.append(vals[0])
                return vocab


def get_labels(file):
    vals = []
    labels = []
    with open(file, 'r') as f:
        for line in f:
            vals = line.rstrip().split(' ')
            labels.append(vals[-1])  # gets the last element from the line, discarding ID if present
        return labels


# Check a label list against the vocabulary, and write any errors to error_dir.
def check_vocab(ID, labels, vocab, err_file, write_file):
    with open(err_file, 'w') as e, open(write_file, 'a') as w:
        for label in labels:
            if (label not in vocab):
                e.write("{}\n".format(label))
            else:
                w.write("{}\n".format(label))


if __name__ == "__main__":
    s_dir = os.fsencode(args.source_dir)
    if ((args.vocab_ref is not None) or (args.vectors_file is not None)):
        vocab = make_vocab()
    else:
        print("Sorry, I need either a vocabulary file or a vectors file. Exiting...")
        exit()
    for file in os.listdir(s_dir):
        filename = os.fsdecode(file)
        if filename.startswith('.'):
            continue
        ID = filename.split("_")[0]  # relies on file name beginning with ID_
        ID = ID.zfill(ZERO_PAD)
        in_file = os.path.join(args.source_dir, filename)
        err_file = os.path.join(args.error_dir, ID + "_errors" + SUFFIX)
        labels = get_labels(in_file)
        check_vocab(ID, labels, vocab, err_file, args.vocab_out)
