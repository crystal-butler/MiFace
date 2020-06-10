import csv
import re
import subprocess
import os
import numpy as np
from spacy.lang.en import English
from mittens import GloVe


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


