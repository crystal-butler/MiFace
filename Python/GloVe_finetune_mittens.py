# Adapted from https://towardsdatascience.com/fine-tune-glove-embeddings-using-mittens-89b5f3fe4c39

from mittens import Mittens
from sklearn.feature_extraction.text import CountVectorizer
import csv
import re
import subprocess
import os
import numpy as np
from spacy.lang.en import English


# Convert GloVe embeddings to a dictionary for use with Mittens.
def embeddings_to_dict(embeddings_path):
    with open(embeddings_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ',quoting=csv.QUOTE_NONE)
        embed = {line[0]: np.array(list(map(float, line[1:])))
                for line in reader}
    return embed


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
    embeddings_path = "data/glove.840B.300d.txt"
    text_path = "data/all_dicts_syns_filtered.txt"
    tokenized_text_path = "data/all_dicts_syns_filtered_tokenized.txt"
    embeddings_path_output = "data/embeddings_word/dicts_syns_filtered_embeddings.txt"
    
    converted_embeddings = embeddings_to_dict(embeddings_path)
    print(f'Length of the embeddings dictionary is {len(converted_embeddings)}.')
    
    tokenize_text(text_path, tokenized_text_path)
    print(f'Tokenized text saved to {tokenized_text_path}.')
    
    corpus_vocab = make_vocab("data/vocab_files/vocab_checked.txt")
    print(corpus_vocab[0:10])
   
    text = []
    with open(tokenized_text_path, 'r', encoding='utf-8') as f:
        text.append(f.read())
    cooccurrence_array = build_cooccurrence_array(corpus_vocab, text)

    mittens_model = Mittens(n=300, max_iter=10)
    dicts_syns_filtered_embeddings = mittens_model.fit(
        cooccurrence_array,
        vocab = corpus_vocab,
        initial_embedding_dict = converted_embeddings
    )
    print(f'\nThe first five embeddings are:\n')
    for n in range(0, 5):
        print(dicts_syns_filtered_embeddings[n])
    print(f'Length of dicts_syns_filtered_embeddings is {len(dicts_syns_filtered_embeddings)}')
    print(f'Length of corpus_vocab is {len(corpus_vocab)}')
    with open(embeddings_path_output, 'w', encoding='utf-8') as f:
        for word, embedding in zip(corpus_vocab, dicts_syns_filtered_embeddings):
            f.write(word + ' ' + embedding + '\n')
