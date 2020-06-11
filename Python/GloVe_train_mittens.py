import csv
import re
import subprocess
import os
import numpy as np
from spacy.lang.en import English
from mittens import GloVe
from sklearn.feature_extraction.text import CountVectorizer


def tokenize_text(text_path, tokenized_text_path):
    nlp = English()
    # Create a Tokenizer with the default settings for English
    # including punctuation rules and exceptions
    tokenizer = nlp.Defaults.create_tokenizer(nlp)
    with open(text_path, encoding='utf-8') as f_in, open(tokenized_text_path, 'a', encoding='utf-8') as f_out:
        for line in f_in:
            tokens = tokenizer(line)
            for token in tokens:
                if (re.match(r"(\w+)", token.text)) or (re.match(r"(\n)", token.text)):
                    f_out.write(token.text.lower() + " ")


def make_vocab(vocab_file):
    vocab_list = []
    with open(vocab_file, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            vocab_list.append(values[0])
            # print(f'Appended {values[0]} to vocab_list.')
    return vocab_list


def build_cooccurrence_array(vocab, tokenized_text):
    vectorized_count = CountVectorizer(ngram_range=(1,1), vocabulary=vocab)
    count_fit = vectorized_count.fit_transform(text)
    count_matrix = (count_fit.T * count_fit)
    count_matrix.setdiag(0)
    cooccurrence_array = count_matrix.toarray()
    return cooccurrence_array


if __name__=='__main__':
    text_path = "data/all_dictionaries_synonyms_cleaned_sorted.txt"
    tokenized_text_path = "data/all_dicts_syns_tokenized.txt"
    embeddings_path_output = "data/embeddings_word/embeddings_dicts_syns-300-20000.txt"
    
    tokenize_text(text_path, tokenized_text_path)
    print(f'Tokenized text saved to {tokenized_text_path}.')
    
    corpus_vocab = make_vocab("data/vocab_files/vocab_checked.txt")
    print(corpus_vocab[0:10])
   
    text = []
    with open(tokenized_text_path, 'r', encoding='utf-8') as f:
        text.append(f.read())
    cooccurrence_array = build_cooccurrence_array(corpus_vocab, text)

    glove_model = GloVe(n=300, max_iter=20000)
    dicts_syns_filtered_embeddings = glove_model.fit(cooccurrence_array)
    print(f'\nThe first five embeddings are:\n')
    for n in range(0, 5):
        print(dicts_syns_filtered_embeddings[n])
    print(f'\n\nLength of dicts_syns_filtered_embeddings is {len(dicts_syns_filtered_embeddings)}')
    print(f'Length of corpus_vocab is {len(corpus_vocab)}')
    with open(embeddings_path_output, 'w', encoding='utf-8') as f:
        for word, embedding in zip(corpus_vocab, dicts_syns_filtered_embeddings):
            f.write(word)
            for value in embedding:
                f.write(' ' + str(value))
            f.write('\n')
    