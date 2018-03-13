# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 12:32:53 2018

@author: Huiyu Jiang
"""

## import packages we used in python 
import pandas as pd
import numpy as np
from collections import Counter
from nltk.stem.porter import PorterStemmer 
import re
from ggplot import * 
import math

## import data
filename = 'train_data.csv'
reviews = pd.read_csv(filename)
stem = PorterStemmer()

## return cleaned string and corresponding number of words.
def noise_remove(review):
    review = re.sub("n't",'not',review)
    review = re.sub("[^a-zA-Z]", " ", review)
    review = review.lower().split()
    cleaned = [stem.stem(w) for w in review]
    return (" ".join(cleaned))

## count special expressions
def special(review):
    splits = re.sub("[a-zA-Z]", " ", review).split()
    expression = []
    for e in splits:
        if (not bool(re.search(r'\d', e))) & ('!' not in e) & \
           ('?' not in e) & ('"' not in e) & ('$' not in e):
            expression += [e]
    express = Counter(expression)
    return (express)

## use samples to select useful features
featurelist = {} 
symbols = {}
frequency = []
samples = reviews.sample(n=100000)

for i in range(5):
    subdata = samples.loc[samples['stars']==(i+1)]
    length = len(subdata)
    frequency += [length]
    ngroup = math.ceil(length/200)
    wordtable = Counter()
    symtable = Counter()
    
    for j in range(ngroup):
        if 200*(j+1)>len(subdata):
            rev_200 = subdata.iloc[200*j:length,] 
        else: 
            rev_200 = subdata.iloc[200*j:200*(j+1),]
        rev_200.index = range(len(rev_200))
        string = " "
        
        for k in range(len(rev_200)):
            sentence = rev_200.loc[k,'text']
            string += noise_remove(sentence)
            symtable += special(sentence)
        wordtable += Counter(string.split())
    featurelist[str(i+1)+'star'] = dict(wordtable)
    symbols[str(i+1)+'star'] = dict(symtable)
    
## return useful features with given dictionary
def commons(dictionary):
    com_word = {}
    wholedic = list(dictionary['1star'].keys()) +\
               list(dictionary['2star'].keys()) +\
               list(dictionary['3star'].keys()) +\
               list(dictionary['4star'].keys()) +\
               list(dictionary['5star'].keys()) 
    
    for word in wholedic:
        if len(word) == 1:
            continue
        
        count = np.zeros(5)
        for i in range(5):
            if word in dictionary[str(i+1)+'star']:
                index = list(dictionary[str(i+1)+'star'].keys()).index(word)
                value = list(dictionary[str(i+1)+'star'].values())[index]
                count[i] = value/frequency[i]
            else:
                count[i] = 0
        if (np.std(count/max(count)) > 0.1) & (sum(count) > 0.001):
            com_word[word] = count       
    return com_word

## generate a list of useful words and expressions
useful_word = commons(featurelist)
useful = list(useful_word.keys())
useful_sym = commons(symbols)
usesym = list(useful_sym.keys())

## ggplot show four categories' behaviour
com = pd.DataFrame(useful_word)
ggplot(aes(x="stars", weight="float"), com) +\
      geom_bar(width = 0.6) +\
      ggtitle("float") +\
      theme_bw()

ggplot(aes(x="stars", weight="egg"),com ) +\
      geom_bar(width = 0.6) +\
      ggtitle("egg") +\
      theme_bw()
      
ggplot(aes(x="stars", weight="heaven"), com) +\
      geom_bar(width = 0.6) +\
      ggtitle("heaven") +\
      theme_bw()

ggplot(aes(x="stars", weight="trust"),com ) +\
      geom_bar(width = 0.6) +\
      ggtitle("trust") +\
      theme_bw()

def info(text):
    infovec = []
    text = re.sub("n't",'not',text)
    upper = [w for w in text.split() if(w.isupper()) & (w!='I')]
    infovec.append(len(upper))
    exclaim = 0
    dquote = 0
    quest = 0
    price = 0
    usestr = []
    
    symbols = re.sub("[a-zA-Z]"," ",text).split()
    for e in symbols:
        if '?' in e:
            quest += 1
        elif '!' in e:
            exclaim += 1
        elif '"' in e:
            dquote += 1
        elif '$' in e:
            price += 1
        elif e in usesym:
            usestr +=[e]
    
    infovec += [quest,exclaim,dquote,price]
    text = re.sub("[^a-zA-Z]"," ",text).lower().split()
    infovec.append(len(text))
    text += usestr
    for word in useful:
        infovec += [text.count(word)]
    return infovec
    

import csv
with open("train.csv","w", encoding = "utf-8") as final:
    wr = csv.writer(final)
    for id in train.index.values:
        sparsevec = [train.loc[id,'stars']]
        text = train.loc[id,'text']
        sparsevec += info(text)
        wr.writerow(sparsevec)
    
test = pd.read_csv("testval_data.csv")
with open("test.csv","w", encoding = "utf-8") as final:
    wr = csv.writer(final)
    for id in test.index.values:
        text = test.loc[id,'text']
        wr.writerow(info(text))

            
