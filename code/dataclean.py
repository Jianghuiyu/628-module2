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
        if (np.std(count/max(count)) > 0.15) & (sum(count) > 0.01):
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

hpos_word = []
pos_word = []
neutral = []
neg_word = []
hneg_word = []
extension = []

## Make useful word and symbol table
for word in useful:
    weightstar = sum(useful_word[word]*useful_word['star'])/sum(useful_word[word])
    if weightstar <= 2.2:
        hneg_word += [word]
    elif (weightstar > 2.2) & (weightstar <2.6):
        neg_word += [word]
    elif (weightstar > 3.25) & (weightstar <3.65):
        pos_word += [word]
    elif weightstar >= 3.65:
        hpos_word += [word]
    elif useful_word[word][2] < sum(useful_word[word])/6.5:
        extension += [word]
    else:
        neutral += [word]

for syms in usesym:
    weightstar = sum(useful_sym[syms]*useful_sym['star'])/sum(useful_sym[syms])
    if weightstar <= 2.2:
        hneg_word += [syms]
    elif (weightstar > 2.2) & (weightstar <2.6):
        neg_word += [syms]
    elif (weightstar > 3.25) & (weightstar <3.65):
        pos_word += [syms]
    elif weightstar >= 3.65:
        hpos_word += [syms]
    elif useful_sym[syms][2] < sum(useful_sym[syms])/6.5:
        extension += [syms]
    else:
        neutral += [syms]

reviews = reviews[['stars','name','text','date']]
reviews['words'] = 0
reviews['upper'] = 0
reviews['exclaim'] = 0
reviews['dquote'] = 0
reviews['quest'] = 0
reviews['price'] = 0
reviews['highneg'] = 0
reviews['neg'] = 0
reviews['neutral'] = 0
reviews['pos'] = 0
reviews['highpos'] = 0
reviews['extension'] = 0

## apply useful features to process raw reviews
rank = range(900000,1000000)
for rowid in rank:
    name = reviews.loc[rowid,'name']
    reviews.loc[rowid,'name'] = re.sub("[^a-zA-Z]", "", name).lower()
    review = reviews.loc[rowid,'text']
    review = re.sub("n't",'not',review)
    upper = [w for w in review.split() if (w.isupper()) & (w!='I')]
    reviews.loc[rowid,'upper'] = len(upper)
    symbols = re.sub("[a-zA-Z]", " ", review).split()
    exclaim = 0
    quest = 0
    dquote = 0
    price = 0
    hpos = 0
    pos = 0
    neg = 0
    hneg = 0
    neu = 0
    extens = 0
    
    for e in symbols:
        if '?' in e:
            quest += 1
        elif '!' in e:
            exclaim += 1
        elif '"' in e:
            dquote += 1
        elif '$' in e:
            price += 1
        elif e in hpos_word:
            hpos += 1
        elif e in pos_word:
            pos += 1
        elif e in neg_word:
            neg += 1
        elif e in hneg_word:
            hneg += 1
        elif e in neutral:
            neu += 1
        elif e in extension:
            extens += 1
    
    review = re.sub("[^a-zA-Z]", " ", review)
    review = review.lower().split() 
    reviews.loc[rowid,'words'] = len(review)
    
    for w in review:
        clean = stem.stem(w)
        if clean in hpos_word:
            hpos += 1
        elif clean in pos_word:
            pos += 1
        elif clean in neg_word:
            neg += 1
        elif clean in hneg_word:
            hneg += 1
        elif clean in neutral:
            neu += 1
        elif clean in extension:
            extens += 1
            
    if rowid % 500 == 0:
        print(rowid)
    reviews.loc[rowid, 'exclaim'] = exclaim
    reviews.loc[rowid, 'dquote'] = dquote
    reviews.loc[rowid, 'quest'] = quest
    reviews.loc[rowid, 'price'] = price
    reviews.loc[rowid, 'highpos'] = hpos
    reviews.loc[rowid, 'pos'] = pos
    reviews.loc[rowid, 'neutral'] = neu
    reviews.loc[rowid, 'neg'] = neg
    reviews.loc[rowid, 'highneg'] = hneg
    reviews.loc[rowid, 'extension'] = extens
    







            
