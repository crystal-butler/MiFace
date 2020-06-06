# Adapted from https://towardsdatascience.com/fine-tune-glove-embeddings-using-mittens-89b5f3fe4c39

import mittens
import csv
import numpy as np
from spacy.lang.en import English


# Convert GloVe embeddings to a dictionary for use with Mittens.
def embeddings_to_dict(embeddings_path):
    with open(embeddings_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ',quoting=csv.QUOTE_NONE)
        embed = {line[0]: np.array(list(map(float, line[1:])))
                for line in reader}
    return embed


def tokenize_text(text_path):
    nlp = English()
    # Create a Tokenizer with the default settings for English
    # including punctuation rules and exceptions
    tokenizer = nlp.Defaults.create_tokenizer(nlp)
    tokens = []
    with open(text_path, encoding='utf-8') as f:
        for line in f:
            tokens.append(tokenizer(line))
    


if __name__=='__main__':
    embeddings_path = "data/glove.840B.300d.txt"
    text_path = "data/all_dictionaries_synonyms_cleaned_sorted.txt"
    converted_embeddings = embeddings_to_dict(embeddings_path)
    print(f'Length of the embeddings dictionary is {len(converted_embeddings)}.')
    tokens = tokenize_text(text_path)
    print(f'Length of the tokens array is {len(tokens)}.')