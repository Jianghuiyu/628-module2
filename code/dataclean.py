# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 12:32:53 2018

@author: Huiyu Jiang
"""

import pandas as pd
import numpy as np
import nltk
from collections import Counter
from nltk.stem.porter import PorterStemmer 
import re
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from ggplot import * 
import math

filename = 'train_data.csv'
reviews = pd.read_csv(filename)
stem = PorterStemmer()
stops = set(stopwords.words("english"))

## return cleaned string and corresponding number of words.
def noise_remove(review):
    review = re.sub("n't",'not',review)
    review = re.sub("[^a-zA-Z]", " ", review)
    review = review.lower().split()
    cleaned = [stem.stem(w) for w in review]
    return (" ".join(cleaned))

featurelist = {} 
frequency = []
samples = reviews.sample(n=100000)
## use noise_remove to select variables
for i in range(5):
    subdata = samples.loc[samples['stars']==(i+1)]
    length = len(subdata)
    frequency += [length]
    ngroup = math.ceil(length/200)
    wordtable = Counter()
    
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
        wordtable += Counter(string.split())
    featurelist[str(i+1)+'star'] = dict(wordtable)
    
def commonword(dictionary):
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

com = commonword(featurelist)
com['stars']=[1,2,3,4,5]
com = pd.DataFrame(com)
useful = list(com.keys())

ggplot(aes(x="stars", weight="disturb"), com) +\
      geom_bar(width = 0.6) +\
      ggtitle("disturb") +\
      theme_bw()

ggplot(aes(x="stars", weight="egg"), com) +\
      geom_bar(width = 0.6) +\
      ggtitle("egg") +\
      theme_bw()
      
ggplot(aes(x="stars", weight="garlic"), com) +\
      geom_bar(width = 0.6) +\
      ggtitle("garlic") +\
      theme_bw()

ggplot(aes(x="stars", weight="bloat"), com) +\
      geom_bar(width = 0.6) +\
      ggtitle("bloat") +\
      theme_bw()

def feature_engineering(review):
    review = re.sub("n't",'not',review)
    review = re.sub("[^a-zA-Z]", " ", review)
    upper = [w for w in review.split() if (w.isupper()) & (w!='I')]
    review = review.lower().split() 
    sen_new = [w for w in review if w in useful]  
    cleaned = [stem.stem(w) for w in sen_new]
    return (" ".join(cleaned),len(review),len(upper))

## Count special symbols like " ? ! Upper word and expression
def emotion(review):
    splits = re.sub("[a-zA-Z]", " ", review).split()
    exclaim = 0
    quest = 0
    dquote = 0
    price = 0
    expression = []
    for e in splits:
        if '!' in e:
            exclaim += 1
        elif '?' in e:
            quest += 1
        elif '"' in e:
            dquote += 1
        elif '$' in e:
            price += 1
        elif (len(e)>1) & (not e.isdigit()):
            expression += [e]
    express = Counter(expression)
    return (exclaim, quest, dquote/2, price, express)

wordlist = {} 
records = []
words = []
uppers = []
exclaims = []
quests = []
dquotes = []
prices = []
expressions = {}

## use sd to select variables
for i in range(5):
    subdata = reviews.loc[reviews['stars']==(i+1)]
    length = len(subdata)
    records += [length]
    ngroup = math.ceil(length/200)
    wordtable = Counter()
    word_count = 0
    up_count = 0
    ex_count = 0
    quest_count = 0
    dquo_count = 0
    price_count = 0
    express_count = Counter()
    
    for j in range(ngroup):
        if 200*(j+1)>len(subdata):
            rev_200 = subdata.iloc[200*j:length,] 
        else: 
            rev_200 = subdata.iloc[200*j:200*(j+1),]
        rev_200.index = range(len(rev_200))
        string = " "
        
        for k in range(len(rev_200)):
            sentence = rev_200.loc[k,'text']
            newsen = feature_engineering(sentence)
            string += newsen[0]
            word_count += newsen[1]
            up_count += newsen[2]
            emotiontable = emotion(sentence)
            ex_count += emotiontable[0]
            quest_count += emotiontable[1]
            dquo_count += emotiontable[2]
            price_count += emotiontable[3]
            express_count += emotiontable[4]
        wordtable += Counter(string.split())
        
    wordlist[str(i+1)+'star'] = dict(wordtable)
    words += [word_count/length]
    uppers += [up_count/length]
    exclaims += [ex_count/length]
    quests += [quest_count/length]
    dquotes += [dquo_count/length]
    prices += [price_count/length]
    expressions[str(i+1)+'star'] = dict(express_count)

summary = {'star': [1,2,3,4,5], 'words': words,'uppers': uppers, 
           'exclaims': exclaims, 'quests': quests,
           'dquotes': dquotes, 'prices': prices}
summary = pd.DataFrame(summary)



    


















            
