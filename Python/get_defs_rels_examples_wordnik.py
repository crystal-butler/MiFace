# Crystal Butler
# 2019/05/05
# Get definitions, examples and related words for a list of newline-separated tokens from
# https://www.wordnik.com/.

import argparse
import requests
import json
import re
import time

BASE_URL = "http://api.wordnik.com/v4/word.json/"
RELATED = ["synonym", "hyponym", "variant", "equivalent", "form", "verb-form", "verb-stem", "same-context"]


parser = argparse.ArgumentParser()
parser.add_argument('vocab_file', help="an input list of newline-separated tokens", type=str)
parser.add_argument('words_file', help="output file of tokens and their synonym texts", type=str)
parser.add_argument('api_key', help="the API request key")
args = parser.parse_args()


def get_definition_words(token):
    lookup_url = "".join([BASE_URL, token, "/definitions/?api_key=", args.api_key])
    def_words = []
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
    data = json.loads(response.content)
    if data:
        for dict in data:
            def_text = dict['text']
            temp = (re.findall(r'[a-zA-Z]+[\_\-\']?[a-zA-Z]+', def_text))
            for t in temp:
                def_words.append(t)
    return def_words


def get_related_words(token):
    lookup_url = "".join([BASE_URL, token, "/relatedWords?api_key=", args.api_key])
    rel_words = []
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
    data = json.loads(response.content)
    if data:
        for dict in data:
            if dict['relationshipType'] in RELATED:
                rel_text = dict['words']
                for t in rel_text:
                    rel_words.append(t)
    return rel_words


def get_examples(token):
    lookup_url = "".join([BASE_URL, token, "/examples?api_key=", args.api_key])
    ex_words = []
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
    data = json.loads(response.content)
    if data:
        for dict in data['examples']:
            ex_text = dict['text']
            temp = (re.findall(r'[a-zA-Z]+[\_\-\']?[a-zA-Z]+', ex_text))
            for t in temp:
                ex_words.append(t)
    return ex_words


if __name__ == "__main__":
    with open(args.vocab_file, 'r') as f, open(args.words_file, 'w') as o:
        line = f.readline()  # the input file must be only one token per line
        token = line.strip()
        while token:
            def_words = get_definition_words(token)
            if (def_words is None):  # we failed to get a valid response for an hour
                print("Program failed while looking up definition for {}".format(token))
                break
            if def_words:
                o.write("{} ".format(token))
                for n in def_words:
                    o.write("{} ".format(n))
                o.write("\n")  # newline separate each vocabulary word

            rel_words = get_related_words(token)
            if (rel_words is None):  # we failed to get a valid response for an hour
                print("Program failed while looking up related words for {}".format(token))
                break
            if rel_words:
                o.write("{} ".format(token))
                for n in rel_words:
                    o.write("{} ".format(n))
                o.write("\n")  # newline separate each vocabulary word

            examples = get_examples(token)
            if (examples is None):  # we failed to get a valid response for an hour
                print("Program failed while looking up examples for{}".format(token))
                break
            if examples:
                o.write("{} ".format(token))
                for n in examples:
                    o.write("{} ".format(n))
                o.write("\n")  # newline separate each vocabulary word

            line = f.readline()
            token = line.strip()
            # time.sleep(1)  # avoid exceeding the daily request limit
