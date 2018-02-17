# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 11:02:34 2018

@author: Huiyu Jiang
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
import time

filename = 'train_data.csv'
reviews = pd.read_csv('train_data.csv')
rev_200 = reviews.iloc[0:200,]
sentence = rev_200.loc[ 'text']

import re
sen_let = re.sub('[^a-zA-Z]',' ', sentence)
stops = set(stopwords.words("english"))

sen_new = [w for w in sen_let.lower().split() if not w in stops]  
def noise_remove(review, stops):
    review = re.sub("[^a-zA-Z]", " ", review)
    review = review.lower().split()
    useful_review = [w for w in review if not w in stops]  
    return " ".join(useful_review)

noise_remove(sen_let, stops)
from nltk.stem.wordnet import WordNetLemmatizer 
lem = WordNetLemmatizer()

from nltk.stem.porter import PorterStemmer 
stem = PorterStemmer()
" ".join([stem.stem(w) for w in sen_new])

from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer() 