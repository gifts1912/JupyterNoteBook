# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 11:46:55 2016

@author: hengyliu
"""
import nltk
import string
import re
from nltk.stem.porter import *


stopwords = nltk.corpus.stopwords.words('english')
def stopWordsFilter(passage):
    use_words = [word for word in passage.strip().split() if word not in stopwords]
    return ' '.join(use_words)
    

def punctuationFilter(line):
    cleanline = re.sub('[' + string.punctuation + ']', '', line)
    return cleanline
        

stemmer = PorterStemmer()
def wordStemmer(passage):
    result = []
    for word in passage.strip().split():
        try:
            wordStemmer = stemmer.stem(word)
            result.append(wordStemmer)
        except:
            continue
    
    return ' '.join(result)
    

def cleanLines(passage):
    #print("original\t{0}".format(passage))
    pus = punctuationFilter(passage)
  #  print("punctuation\t{0}".format(pus))
    
    sw = stopWordsFilter(pus)
   # print ("stopwordfilter\t{0}".format(sw))
    
    ws = wordStemmer(sw)   
    #print("wordStemp\t{0}".format(ws))
    
    return ws
    
    