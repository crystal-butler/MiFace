import sys
import os
import gzip
import re

with open('/home/jupyter/Notebooks/crystal/NLP/Vocab_Files/vocab_checked.txt', 'r') as v:
    n = 1
    l1 = 1
    l2 = 1
    vocab = v.read().splitlines()
    for word in vocab:
        path = '/home/jupyter/Notebooks/crystal/NLP/CC_Text/'
        for filename in sorted(os.listdir(path)):
            f = os.path.join(path, filename)
            out = os.path.join('/home/jupyter/Notebooks/crystal/NLP/Vocab_Files/Vocab_Output', word + '_context.txt')
            print(f'Looking for word {n}: {word} in file {f}, which is line {l1}')
            with gzip.open(f, 'rt', encoding='utf-8') as cc, open(out, 'a+'):
                for cc_line in cc:
                    if re.search(word, str(cc)):
                        print(cc_line)
                        out.write(cc_line)
            l1 += 1
        path = '/home/jupyter/Notebooks/crystal/NLP/CC_Text_125'
        for filename in sorted(os.listdir(path)):
            f = os.path.join(path, filename)
            out = os.path.join('/home/jupyter/Notebooks/crystal/NLP/Vocab_Files/Vocab_Output', word + '_context.txt')
            print(f'Looking for word {n}: {word} in file {f}, which is line {l2}')
            with gzip.open(f, 'rt', encoding='utf-8') as cc, open(out, 'a+'):
                for cc_line in cc:
                    if re.search(word, str(cc)):
                        print(cc_line)
                        out.write(cc_line)
            l2 += 1
        n += 1