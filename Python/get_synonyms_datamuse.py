# Crystal Butler
# 2019/05/05
# Get synonyms for a list of newline-separated tokens from
# https://api.datamuse.com/.

import argparse
import requests
import time
import json

BASE_URL = "https://api.datamuse.com/words?rel_syn="


parser = argparse.ArgumentParser()
parser.add_argument('vocab_file', help="an input list of newline-separated tokens", type=str)
parser.add_argument('words_file', help="output file of tokens and their synonym texts", type=str)
args = parser.parse_args()


def get_synonym_words(token):
    lookup_url = "".join([BASE_URL, token])
    syn_words = []
    error_count = 0
    try:
        response = requests.get(lookup_url)
    except OSError:
        print("Can't connect; retrying in one minute...")
        time.sleep(60)
        response = requests.get(lookup_url)  # if network is busy, wait a minute and try again
    while not (response.status_code == 200):  # if we didn't get a positive response
        time.sleep(60)
        response = requests.get(lookup_url)
        error_count += 1
        if (error_count > 60):
            return None
    try:
        data = json.loads(response.content)
    except SyntaxError:  # occurs if response.content is "b'Results not found'"
        return syn_words
    for dict in data:
        syn_words.append(dict['word'])
    return syn_words


if __name__ == "__main__":
    with open(args.vocab_file, 'r') as f, open(args.words_file, 'w') as o:
        line = f.readline()  # the input file must be only one token per line
        token = line.strip()
        while token:
            syn_words = get_synonym_words(token)
            if (syn_words is None):  # we failed to get a valid response for an hour
                print("Program failed while looking up {}".format(token))
                break
            if syn_words:
                o.write("{} ".format(token))
                for n in syn_words:
                    o.write("{} ".format(n))
                o.write("\n")  # newline separate each vocabulary word
            line = f.readline()
            token = line.strip()
            # time.sleep(1)  # avoid exceeding the daily request limit
