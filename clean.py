# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from nltk.stem.porter import PorterStemmer 
import re

## import data
filename = 'train_data.csv'
reviews = pd.read_csv(filename)
reviews = reviews[['stars','text']]
stem = PorterStemmer()

usefulword = pd.read_csv("useful.csv", header = None)
useful = list(usefulword[0])
usesym = useful[9113:]

def info(text):
    infovec = []
    text = re.sub("n't",'not',text)
    upper = [w for w in text.split() if(w.isupper()) & (w!='I')]
    infovec.append(len(upper))
    exclaim = 0
    dquote = 0
    quest = 0
    price = 0
    usestr = " "
    
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
            usestr += e+ " "
    
    infovec += [quest,exclaim,dquote,price]
    text = re.sub("[^a-zA-Z]"," ",text).lower().split()
    infovec.append(len(text))
    usestr = usestr.join(text)
    for word in useful:
        infovec.append(usestr.count(word))
    return infovec
    

import csv
train1 = reviews.loc[range(100000),]
with open("train1.csv","w", encoding = "utf-8") as final:
    wr = csv.writer(final)
    for id in train1.index.values:
        sparsevec = [train1.loc[id,'stars']]
        text = train1.loc[id,'text']
        sparsevec += info(text)
        wr.writerow(sparsevec)
    















