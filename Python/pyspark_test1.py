import sys
import os
import gzip
import re
import timeit
from timeit import default_timer as timer

def read_text_file_into_memory(file_path):
    with open(file_path, 'rt', encoding='utf-8') as f:
        lines = f.read().splitlines()
    return lines

def filter_on_vocab(word, line):
    results = []
    if word in line:
        results.append(line)
    return results


if __name__ == "__main__":
    start = timer()
    vocab_file_path = '/scratch/cb2610/MiFace/Python/vocab_files/vocab_checked.txt'
    vocab = read_text_file_into_memory(vocab_file_path)
    WET_file_path = '/scratch/cb2610/Common_Crawl/WET_Files_Test0/CC-MAIN-20200117152059-20200117180059-00138.warc.wet'
    cc_lines = read_text_file_into_memory(WET_file_path)
    end = timer()
    run_time = end - start
    print(f'There are {len(vocab)} words in the vocabulary.\n')
    print(f'It took {run_time} seconds to read the vocabulary file and text file into memory.')
    print(f'There are {len(cc_lines)} lines in the text file.')
    start = timer()
    vocab_lines = []
    printed = []
    for line in cc_lines:
        for i in range(101):
            if vocab[i] not in printed:
                print(f'Searching for {vocab[i]}...')
                printed.append(vocab[i])
            match = filter_on_vocab(vocab[i], line)
            if match:
                assert len(match) == 1
                vocab_lines.append(match[0])

    end = timer()
    run_time = end - start
    print(f'Found {len(vocab_lines)} lines matching the vocabulary in {run_time} seconds.')
