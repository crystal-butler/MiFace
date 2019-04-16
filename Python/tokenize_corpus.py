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

# Don't include common words or part-of-speech designations in training files.
stoplist = ["adj", "adjective", "adv", "all", "an", "and", "are", "as", "at", "be", "been", "but", "by", "can",
            "for", "had", "has", "have", "he", "her", "hers", "his", "if", "in", "is", "it",
            "nor", "noun", "of", "on", "or", "our", "ours", "phrasal", "she", "so", "some",
            "than", "that", "the", "them", "they", "their", "theirs", "this", "to", "us",
            "verb", "was", "we", "what", "who", "with", "you"]


# Read in the corpus file, and split tokens to the output file.
def create_token_list(corpus_file, token_file):
    with open(args.corpus_file, 'r', encoding="utf8", errors='ignore') as infile, open(args.token_file, 'w') as outfile:
        for line in infile:
            # Find all words comprising two or more alphabetic characters,
            # including contractions and hyphenated words.
            temp = (re.findall(r'[a-zA-Z]+[\_\-\']?[a-zA-Z]+', line))
            cleaned = []
            for t in temp:
                # Don't write out single letters or stoplist words.l
                # Transform all to lowercase for standardization.
                if (t.lower() not in stoplist):
                    cleaned.append(t.lower())
            for c in cleaned:
                outfile.write("{} ".format(c))


if __name__ == "__main__":
    create_token_list(args.corpus_file, args.token_file)
