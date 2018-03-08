# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 14:30:25 2018

@author: Huiyu Jiang
"""

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

useful_word = pd.read_csv('useful.csv')
useful = list(useful_word)
useful_sym = {"'.": [ 0.00588235,  0.00479445,  0.0046729 ,  0.00276611,  0.0020249 ], 
 '),': [ 0.03870968,  0.06161379,  0.06693238,  0.06659664,  0.04509509],
 ').': [ 0.09165085,  0.13761094,  0.15083837,  0.13746499,  0.08663292],
 ')...': [ 0.00189753,  0.00285627,  0.00233645,  0.00192577,  0.00136818],
 '**': [ 0.00379507,  0.00469244,  0.00364211,  0.00318627,  0.00240799],
 '--': [ 0.02912713,  0.05161685,  0.05284497,  0.04639356,  0.03551785],
 '---': [ 0.00388994,  0.00408038,  0.00487905,  0.0035014 ,  0.00257217],
 '.)': [ 0.01166983,  0.01754565,  0.01601154,  0.01418067,  0.00897524],
 '..': [ 0.10996205,  0.09731715,  0.08761682,  0.06778711,  0.05757286],
 '...': [ 0.34278937,  0.37692543,  0.33088235,  0.25045518,  0.19852237],
 '....': [ 0.09003795,  0.08181169,  0.06425234,  0.0462535 ,  0.04359009],
 '.....': [ 0.02447818,  0.02438029,  0.01394997,  0.01015406,  0.01135586],
 '......': [ 0.00787476,  0.00734469,  0.00426058,  0.00360644,  0.00328362],
 '.......': [ 0.00256167,  0.00357034,  0.00185542,  0.00098039,  0.00117663],
 ':(': [ 0.00768501,  0.0127512 ,  0.00804013,  0.00416667,  0.00150499],
 ':)': [ 0.0028463 ,  0.00591656,  0.01614898,  0.03452381,  0.0342865 ],
 ':-)': [ 0.00028463,  0.00081608,  0.00206157,  0.00406162,  0.00339308],
 '://': [ 0.00332068,  0.00357034,  0.00618472,  0.00528711,  0.00300999],
 ';)': [ 0.00037951,  0.00122412,  0.00453546,  0.0067577 ,  0.00582843]}
 
useful_sym = pd.DataFrame(useful_sym)
usesym = list(useful_sym)

reviews = reviews[['stars','name','text','date']]
reviews['words'] = 0
reviews['upper'] = 0
reviews['exclaim'] = 0
reviews['dquote'] = 0
reviews['quest'] = 0
reviews['price'] = 0

## apply useful features to process raw reviews
rank = range(20)
reviews = reviews.loc[rank,]
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
    cleantext = ""
    
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
            cleantext += e + " "
 
    review = re.sub("[^a-zA-Z]", " ", review)
    review = review.lower().split() 
    reviews.loc[rowid,'words'] = len(review)
    
    for w in review:
        clean = stem.stem(w)
        if clean in useful:
            cleantext += clean + " "
            
    if rowid % 500 == 0:
        print(rowid)
    reviews.loc[rowid, 'exclaim'] = exclaim
    reviews.loc[rowid, 'dquote'] = dquote
    reviews.loc[rowid, 'quest'] = quest
    reviews.loc[rowid, 'price'] = price
    reviews.loc[rowid, 'text'] = cleantext
    
reviews.to_csv('test3.csv')
























