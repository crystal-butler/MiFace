# Crystal Butler
# 2019/04/25
# Get synonyms for a list of newline-separated tokens from
# https://words.bighugelabs.com/.

import argparse
import requests

BASE_URL = "http://words.bighugelabs.com/api/2/"
RESPONSE_TYPE = "json"  # other response formats are text, xml, php
NEAR = ["syn", "rel", "sim"]  # get synonyms, related words, and similar words


parser = argparse.ArgumentParser()
parser.add_argument('vocab_file', help="an input list of newline-separated tokens", type=str)
parser.add_argument('syn_file', help="output file of tokens and their synonyms", type=str)
parser.add_argument('api_key', help="the API request key")
args = parser.parse_args()


def get_synonyms(token):
    lookup_url = "".join([BASE_URL, args.api_key, "/", token, "/", RESPONSE_TYPE])
    response = requests.get(lookup_url)
    if not response:
        near_token = []
        return near_token
    response_dict = response.json()
    near_token = get_nested(response_dict)
    return near_token


# The Big Huge Thesaurus API returns a JSON object with nested dictionaries.
# The code below relies on synonyms, related words, and similar words being
# nested one level deep.
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
