# coding: utf-8

import numpy as np
from collections import defaultdict
from Queue import PriorityQueue
import sys
from scipy import spatial
from scipy import stats

def load_benchmark(filename, all_words):
    scores = {}
    for line in open(filename):
        w1, w2, score = line.strip().split()
        w1 = w1.lower()
        w2 = w2.lower()
        all_words.add(w1)
        all_words.add(w2)
        scores[(w1,w2)]=float(score)
    return scores

def extract_vectors(corpus_path, all_words):
    vectors = {}
    for line in open(corpus_path):
        first_space = line.find(' ')
        word = line[:first_space]
        if word in all_words:
            data = line.strip().split()
            vectors[word] = np.array(map(float, data[1:]))
            vectors[word] /= np.linalg.norm(vectors[word])
    return vectors

def get(vectors, word):
    if word in vectors:
        return vectors[word]
    else:
        return np.zeros(300)


all_words = set()





benches = ["MC-pairs-EN-30.txt", "MEN-pairs-EN-3000.txt", 
           "RG-pairs-EN-65.txt", "RW-pairs-EN-2034.txt", "SCWS-pairs-EN-2023.txt",
           "SimLex-pairs-EN.txt", "WS-pairs-EN-353.txt"]

for bench in benches:
    load_benchmark("sim_benchs/" + bench, all_words)

#change the vector filename here
#vectors = extract_vectors("vectors.my", all_words)


def evaluate(vectors):
    for bench in benches:
        #change the folder with benchmarks here
        bench1 = load_benchmark("sim_benchs/" + bench, all_words)
        gold_val = []
        my_val = []
        for (w1,w2), sc in bench1.iteritems():
            #if w1 in vectors and w2 in vectors:
                gold_val.append(sc)
                scor =  get(vectors, w1).dot(get(vectors, w2))
                my_val.append(scor)
        print bench, stats.spearmanr(gold_val, my_val)[0]


#change vectors file
evaluate(extract_vectors(sys.argv[1], all_words))

