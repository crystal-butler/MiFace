import sys
import os
import gzip
import re

with open('/home/jupyter/Notebooks/crystal/NLP/Vocab_Files/vocab_checked.txt', 'r') as v:
    vocab = v.read().splitlines()
    for word in vocab:
        path = '/home/jupyter/Notebooks/crystal/NLP/CC_Text/'
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            out = os.path.join('/home/jupyter/Notebooks/crystal/NLP/Vocab_Files/Vocab_Output', word + '_context.txt')
            with gzip.open(f, 'rt', encoding='utf-8') as cc, open(out, 'a+'):
                for cc_line in cc:
                    if re.search(word, str(cc)):
                        print(cc_line)
                        out.write(cc_line)
        path = '/home/jupyter/Notebooks/crystal/NLP/CC_Text_125'
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            out = os.path.join('/home/jupyter/Notebooks/crystal/NLP/Vocab_Files/Vocab_Output', word + '_context.txt')
            print(out)
            with gzip.open(f, 'rt', encoding='utf-8') as cc, open(out, 'a+'):
                for cc_line in cc:
                    if re.search(word, str(cc)):
                        print(cc_line)
                        out.write(cc_line)