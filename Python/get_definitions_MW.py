# Crystal Butler
# 2019/04/25
# Get definitions for a list of newline-separated tokens from
# https://dictionaryapi.com/products/api-collegiate-dictionary.

import argparse
import requests
import re
import time
from lxml import etree

BASE_URL = "https://www.dictionaryapi.com/api/v1/references/collegiate/"
RESPONSE_TYPE = "xml"  # also available as giant mess of deeply nested JSON


parser = argparse.ArgumentParser()
parser.add_argument('vocab_file', help="an input list of newline-separated tokens", type=str)
parser.add_argument('words_file', help="output file of tokens and their definition texts", type=str)
parser.add_argument('api_key', help="the API request key")
args = parser.parse_args()


def get_definition_words(token):
    lookup_url = "".join([BASE_URL, RESPONSE_TYPE, "/", token, "?key=", args.api_key])
    def_words = []
    error_count = 0
    response = requests.get(lookup_url)
    while not (response.status_code == 200):  # if we didn't get a positive response
        time.sleep(60)
        response = requests.get(lookup_url)
        error_count += 1
        if (error_count > 60):
            return None
    try:
        tree = etree.fromstring(response.content)
    except SyntaxError:  # occurs if response.content is "b'Results not found'"
        return def_words
    response_list = tree.xpath("//entry/def/dt//text()")
    for blurb in response_list:
        temp = (re.findall(r'[a-zA-Z]+[\_\-\']?[a-zA-Z]+', blurb))
        for t in temp:
            def_words.append(t)
    return def_words


if __name__ == "__main__":
    with open(args.vocab_file, 'r') as f, open(args.words_file, 'w') as o:
        line = f.readline()  # the input file must be only one token per line
        token = line.strip()
        while token:
            def_words = get_definition_words(token)
            if (def_words is None):  # we failed to get a valid response for an hour
                print("Program failed while looking up {}".format(token))
                break
            if def_words:
                o.write("{} ".format(token))
                for n in def_words:
                    o.write("{} ".format(n))
                o.write("\n")  # newline separate each vocabulary word
            line = f.readline()
            token = line.strip()
