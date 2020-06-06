# Adapted from https://towardsdatascience.com/fine-tune-glove-embeddings-using-mittens-89b5f3fe4c39

import mittens
import csv
import numpy as np

# Convert GloVe embeddings to a dictionary for use with Mittens.
def embeddings_to_dict(embeddings_path):
    with open(embeddings_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=' ',quoting=csv.QUOTE_NONE)
        embed = {line[0]: np.array(list(map(float, line[1:])))
                for line in reader}
    return embed

if __name__=='__main__':
    embeddings_path = "data/glove.840B.300d.txt"
    converted_embeddings = embeddings_to_dict(embeddings_path)
    print(f'Length of the embeddings dictionary is {len(converted_embeddings)}.')