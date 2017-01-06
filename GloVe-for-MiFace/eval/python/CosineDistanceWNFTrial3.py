#!/usr/bin/python
import os
import argparse
import numpy as np
np.seterr(divide='ignore', invalid='ignore') #fix divide runtime error (when dividing by zeros)
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

    #SM - creates WORD x WORD MATRIX 
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
    if input_term1 not in vocab and input_term2 not in vocab:
        f2.write('%s%sWNF%s%s\n' % (input_term1.ljust(20), input_term2.ljust(20), input_term1.rjust(30), input_term2.rjust(20)))
    elif input_term1 not in vocab:
        f2.write('%s%sWNF%s\n' % (input_term1.ljust(20), input_term2.ljust(20), input_term1.rjust(30)))
    elif input_term2 not in vocab:
        f2.write('%s%sWNF%s\n' % (input_term1.ljust(20), input_term2.ljust(20), input_term2.rjust(30)))
    else:
        vec_result1 = W[vocab[input_term1], :] 
    #try catch for vec_norm variable (if the input_term1 is out of dict, vec_result1 won't exist)    
    if 'vec_result1' in locals():  #only computes for vec_result1!!! 
        vec_norm = np.zeros(vec_result1.shape)
        d = (np.sum(vec_result1 ** 2,) ** (0.5))
        vec_norm = (vec_result1.T / d).T
        dist = np.dot(W, vec_norm.T)
        index = vocab[input_term1]
        dist[index] = -np.Inf
        a = np.argsort(-dist)[:N]
        if dist[index] == float('-inf'):  #SM edit = changed -inf to 1 based on same word pair
            dist[index] = 1  
        for x in a: #changes number of items that print - prints only first/ highest scored word in the list
            if ivocab[x] == input_term2: 
                f2.write("%s%s%s\n" % (input_term1.ljust(20), input_term2.ljust(20), dist[x]))
                break
    else:
        pass

    

if __name__ == "__main__":
    N = 798033          # number of closest words that will be shown
    W, vocab, ivocab = generate()
    rootdir = '/data/sam676/TrialThree/allPairs_cleanedCOPY/'
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            f = open(subdir+'/'+ file,'r')
            f2 = open('/data/sam676/TrialThree/cosineScores/'+ file,'w')
            for line in f:
                array = []
                for word in line.split():
                    array.append(word)
                input_term1 = array[0]
                input_term2 = array[1]
                distance(W, vocab, ivocab, input_term1, input_term2)
            f2.close()    
            f.close()








