# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 17:35:24 2016

@author: hengyliu
"""

import gensim
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
import numpy
from random import shuffle
import nltk
import sys

input_filename = sys.argv[1]
output_filename = sys.argv[2]
query_field = int(sys.argv[3])
passage_field = int(sys.argv[4])

train_data = []
lines = []

def TrainDataGenerate(input_filename, query_field, passage_filed):
    global train_data
    global lines
    fr = open(input_filename, 'r', encoding='utf-8')
    start_index = 0
    max_field = max(query_field, passage_field)
    for line in fr:
        arr = line.strip().split('\t')
        if(len(arr) - 1 < max_field):
            continue
        query = arr[query_field]
        passage = arr[passage_field]
        
        train_data.append(LabeledSentence(utils.to_unicode(query).split(), ["query_{0}".format(start_index)]))
        train_data.append(LabeledSentence(utils.to_unicode(passage).split(), ["passage_{0}".format(start_index)]))
        lines.append(line.strip())
        start_index += 1        
    fr.close()

#TrainDataGenerate(input_filename, query_field, passage_field)

model = Doc2Vec(min_count=5, window=5, size=100, sample=1e-4, negative=5, workers=8)
def ModelTrain():
    global model
    model.build_vocab(train_data)
    for i in range(10):
        shuffle(train_data)
        model.train(train_data)
           
#ModelTrain()

def Predict(output_filename):
    global model
    fw = open(output_filename, 'w', encoding='utf-8')
    for i in range(len(lines)):
        score = model.docvecs.similarity("query_%d"%i, "passage_%d"%i)
        fw.write("{0}\t{1}\n".format(lines[i], score))    
    fw.close()
    
#Predict(output_filename)

if __name__ == "__main__":
    TrainDataGenerate(input_filename, query_field, passage_field)
    ModelTrain()
    Predict(output_filename)