import argparse
import numpy as np
import sys
import subprocess as sp

def generate():
    # SM - READING AND PARSING THE VOCAB AND VECTOR FILES / SAVING THEM TO WORD AND VECTOR VARIABLES
    parser = argparse.ArgumentParser()
    parser.add_argument('--vocab_file', default='glove.6B.vocab.txt', type=str)     # CB 03/28/2016 changed from default
    parser.add_argument('--vectors_file', default='glove.6B.300d.txt', type=str)    # CB 03/28/2016 changed from default
    args = parser.parse_args()

    with open(args.vocab_file, 'r') as f:
        words = [x.rstrip().split(' ')[0] for x in f.readlines()]
    with open(args.vectors_file, 'r') as f:
        vectors = {}
        for line in f:
            vals = line.rstrip().split(' ')
            vectors[vals[0]] = [float(x) for x in vals[1:]]

#SM possible vector WORD X WORD MATRIX (iterating through dictionaries.... word: index then index:word)
    vocab_size = len(words)
    vocab = {w: idx for idx, w in enumerate(words)}
    ivocab = {idx: w for idx, w in enumerate(words)}

    vector_dim = len(vectors[ivocab[0]])
    W = np.zeros((vocab_size, vector_dim))
    for word, v in vectors.items():
        if word == '<unk>':
            continue
        W[vocab[word], :] = v

    # normalize each word vector to unit variance
    W_norm = np.zeros(W.shape)
    d = (np.sum(W ** 2, 1) ** (0.5))
    W_norm = (W.T / d).T
    return (W_norm, vocab, ivocab)

def distance(W, vocab, ivocab, input_term1, input_term2):
    #for idx, term in enumerate(input_term.split(' ')):
    if input_term1 in vocab:
        print('Word 1: %s  Position in vocabulary: %i' % (input_term1, vocab[input_term1]))
       # if idx == 0:
       #     vec_result = W[vocab[input_term1], :] 
        #else:
        vec_result1 = W[vocab[input_term1], :] 
    else:
        print('Word 1: %s  Out of dictionary!\n' % input_term1)

    if input_term2 in vocab:
        print('Word 2: %s  Position in vocabulary: %i' % (input_term2, vocab[input_term2]))
       # if idx == 0:
       #     vec_result = W[vocab[input_term1], :] 
        #else:
        vec_result2 = W[vocab[input_term2], :] 
    else:
        print('Word 2: %s  Out of dictionary!\n' % input_term2)
      
    
    vec_norm = np.zeros(vec_result1.shape)
    d = (np.sum(vec_result1 ** 2,) ** (0.5))
    vec_norm = (vec_result1.T / d).T

    dist = np.dot(W, vec_norm.T)

    #for term in input_term.split(' '):
    index = vocab[input_term1]
    dist[index] = -np.Inf

    a = np.argsort(-dist)[:N]



    print("\n                               Word       Cosine distance\n")
    print("---------------------------------------------------------\n")
    for x in a: #changes number of items that print - prints only first/ highest scored word in the list
        if ivocab[x] == input_term2: 
            print("%35s\t\t%f\n" % (ivocab[x], dist[x]))
            break
         


if __name__ == "__main__":
    N = 798033          # number of closest words that will be shown
    W, vocab, ivocab = generate()
    while True:
        raw_input('Press enter to continue: ')      # CB 03/28/2016: added to clear terminal window properly
        tmp = sp.call('clear',shell=True)           # CB 03/28/2016: added to clear terminal window properly
        input_term1 = raw_input("\nEnter word 1: ") #SM 4/10/16)
        input_term2 = raw_input("\nEnter word 2: ")
        #if input_term == 'EXIT':
         #  break
        #else:
        distance(W, vocab, ivocab, input_term1, input_term2)


