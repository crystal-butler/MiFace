from sklearn.feature_extraction.text import CountVectorizer
import csv
import re
import subprocess
import os
from spacy.lang.en import English


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
    text_path = "data/all_dicts_syns_filtered.txt"
    tokenized_text_path = "data/all_dicts_syns_filtered_tokenized.txt"
    
    create_vocab_command = ["./GloVe/build/vocab_count < data/all_dicts_syns_filtered_tokenized.txt > data/all_dicts_syns_filtered_vocab.txt"]
    create_cooccurrence_matrix_command = ["./GloVe/build/cooccur -vocab-file data/all_dicts_syns_filtered_vocab.txt < data/all_dicts_syns_filtered_tokenized.txt > data/all_dicts_syns_filtered_cooccurrences.bin"]
    # create_cooccurrence_shuffle_command = ["./GloVe/build/shuffle -memory = 8.0 < data/all_dicts_syns_filtered_cooccurrences.bin > data/all_dicts_syns_filtered_cooccurrences.shuf.bin"]
    create_model_command = ["./GloVe/build/glove -input-file data/all_dicts_syns_filtered_cooccurrences.bin -vocab-file data/all_dicts_syns_filtered_vocab.txt -vector-size 300 -iter 100 -eta .01 -save-file data/embeddings_word/embeddings_all_dicts_syns_filtered-300-100"]

    # tokenize_text(text_path, tokenized_text_path)
    # print(f'Tokenized text saved to {tokenized_text_path}.')
    # execute_C(create_vocab_command)
    # execute_C(create_cooccurrence_matrix_command)
    # execute_C(create_cooccurrence_shuffle_command)  # Executing this command always generates too many temp files, so skipping it.
    execute_C(create_model_command)