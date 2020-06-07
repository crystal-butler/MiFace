# Adapted from https://towardsdatascience.com/fine-tune-glove-embeddings-using-mittens-89b5f3fe4c39

import mittens
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


def execute_C(command):
    s = subprocess.run(command, shell = True) 
    print(", return code", s)


if __name__=='__main__':
    embeddings_path = "data/glove.840B.300d.txt"
    text_path = "data/all_dictionaries_synonyms_cleaned_sorted.txt"
    tokenized_text_path = "data/all_dicts_syns_tokenized.txt"
    create_vocab_command = ["./GloVe/build/vocab_count < data/all_dicts_syns_tokenized.txt > data/all_dicts_syns_vocab.txt"]
    create_cooccurrence_matrix_command = ["./GloVe/build/cooccur -vocab-file data/all_dicts_syns_vocab.txt < data/all_dicts_syns_tokenized.txt > data/all_dicts_syns_cooccurrences.bin"]
    create_cooccurrence_shuffle_command = ["./GloVe/build/shuffle -memory = 8.0 < data/all_dicts_syns_cooccurrences.bin > data/all_dicts_syns_cooccurrences.shuf.bin"]
    create_model_command = ["./GloVe/build/glove -input-file data/all_dicts_syns_cooccurrences.bin -vocab-file data/all_dicts_syns_vocab.txt -vector-size 150 -save-file data/embeddings_word/embeddings_all_dicts_syns-150"]
    # converted_embeddings = embeddings_to_dict(embeddings_path)
    # print(f'Length of the embeddings dictionary is {len(converted_embeddings)}.')
    # tokenize_text(text_path, tokenized_text_path)
    # print(f'Tokenized text saved to {tokenized_text_path}.')
    # execute_C(create_vocab_command)
    # execute_C(create_cooccurrence_matrix_command)
    # execute_C(create_cooccurrence_shuffle_command)
    execute_C(create_model_command)