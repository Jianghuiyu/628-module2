# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 12:32:53 2018

@author: Huiyu Jiang
"""

import pandas as pd
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.stem.porter import PorterStemmer 
import re
from sklearn.feature_extraction.text import CountVectorizer

filename = 'train_data.csv'
reviews = pd.read_csv('train_data.csv')

stops = set(stopwords.words("english"))
def noise_remove(review, stops):
    review = re.sub("[^a-zA-Z]", " ", review)
    review = review.lower().split()
    useful_review = [w for w in review if not w in stops]  
    return " ".join(useful_review)

for i in range(5):
    subdata = reviews.loc[reviews['stars']==(i+1)]
    ngroup = round(len(subdata)/200) + 1
    wordtable = Counter()
    for j in range(ngroup):
        if 200*(j+1)>len(subdata):
            rev_200 = subdata.iloc[200*j:len(subdata),] 
        else: 
            rev_200 = subdata.iloc[200*j:200*(j+1),]
        rev_200.index = range(len(rev_200))
        string = " "
        for k in range(len(rev_200)):
            sentence = rev_200.loc[k,'text']
            sen_let = re.sub('[^a-zA-Z]',' ', sentence)
            string += noise_remove(sen_let, stops)
        wordtable += Counter(string.split())
            