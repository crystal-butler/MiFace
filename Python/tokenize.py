# Crystal Butler
# 2019/04/11
# Take in a corpus and tokenize it for processing into word vectors by GloVe.
# Tokens must be white space delimited; newlines are reserved to separate documents
# for the final input, if multiple documents are used.
# The output will be a single file of white space delimited tokens, with all numbers
# and punctuation removed, with the exception of the apostrophe, hyphen and underscore
# when they appear as part of a word.

# import os
import argparse
import re

# Read in options.
parser = argparse.ArgumentParser()
parser.add_argument('corpus_file', help='text file, to be broken into individual tokens', type=str)
parser.add_argument('token_file', help='filename to which tokens will be written', type=str)
args = parser.parse_args()


# Read in the corpus file, and split tokens to the output file.
def create_token_list(corpus_file, token_file):
    with open(args.corpus_file, 'r', encoding="utf8", errors='ignore') as infile, open(args.token_file, 'w') as outfile:
        for line in infile:
            # Find all words one alphabetic character or longer, including contractions and hyphenated words.
            temp = (re.findall(r'[a-zA-Z]+[\-\']*[a-zA-Z]*', line))
            print(temp)
            for t in temp:
                outfile.write("{} ".format(t))


if __name__ == "__main__":
    create_token_list(args.corpus_file, args.token_file)
