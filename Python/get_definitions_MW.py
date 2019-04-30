# Crystal Butler
# 2019/04/29
# Get synonyms for a list of newline-separated tokens from
# https://words.bighugelabs.com/.

import argparse
import requests
import jq

API_KEY = "e071a5dc3c9d18ac7900fe6f98e72706"
BASE_URL = "http://words.bighugelabs.com/api/2/"
NEAR = ["syn", "rel", "sim"]  # get synonyms, related words, and similar words


parser = argparse.ArgumentParser()
parser.add_argument('vocab_file', help="an input list of newline-separated tokens", type=str)
parser.add_argument('syn_file', help="output file of tokens and their synonyms", type=str)
args = parser.parse_args()


def get_synonyms(token):
    lookup_url = "".join([BASE_URL, API_KEY, "/", token, "/json"])  # other response formats are text, xml, php
    response = requests.get(lookup_url)
    if not response:
        near_token = []
        return near_token
    response_dict = response.json()
    near_token = get_nested(response_dict)
    return near_token


def get_nested(response_dict):
    near_token = []
    for k, v in response_dict.items():
        if isinstance(v, dict):
            for subk, subv in v.items():
                if subk in NEAR:
                    for val in subv:
                        near_token.append(val)
    return near_token


if __name__ == "__main__":
    with open(args.vocab_file, 'r') as f, open(args.syn_file, 'w') as o:
        line = f.readline()  # the input file must be only one token per line
        token = line.strip()
        while token:
            near_token = get_synonyms(token)
            if near_token:
                o.write("{} ".format(token))
                for n in near_token:
                    o.write("{} ".format(n))
                o.write("\n")  # newline separate each vocabulary word
            line = f.readline()
            token = line.strip()
