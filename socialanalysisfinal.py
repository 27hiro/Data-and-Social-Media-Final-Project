# -*- coding: utf-8 -*-
"""Socialanalysisfinal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vyn8_dGJkNOP6nEjOx766RbKNq3b9b4s
"""

!pip install -qq whatthelang

!pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

# Import Library
#import twint

pip install nest_asyncio

import nest_asyncio
nest_asyncio.apply()

"""
# Configuration of the twint
c = twint.Config()
c.Store_csv = True
c.Output = "Arcanesample.csv"
c.Search = "#Arcane"
c.Limit = 10000
c.Lang = 'en'
"""

# Run search
#twint.run.Search(c)

import pandas as pd

tweet_df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/data/Arcanesample.csv')

tweet_df = tweet_df[tweet_df['language'] == 'en']

tweet_df.tail()



import nltk
from nltk import word_tokenize

nltk.download('punkt')

nltk.download('wordnet')

with open("/content/drive/MyDrive/Colab Notebooks/data/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt","r") as f:
  lexicontext = f.readlines()
wordline = []
for line in lexicontext:
  wordline.append(line.split("\t"))

newlex = {}
for entry in wordline:
  if entry[1] == "positive":
    if int(entry[2][0]) > 0:
      newlex[entry[0]] = 1
  elif entry[1] == "negative":
    if int(entry[2][0]) > 0:
      newlex[entry[0]] = -1
f.close()

def NRCscore(wordlist):
  word = []
  score = 0.0 
  for lemma in wordlist:
    if lemma.lower() in newlex:
      score += newlex[lemma.lower()]
      word.append(lemma.lower())
  return score, word

del newlex['riot'] #Because name of company that makes arcane is called riot

#simple binary lexicon based analysis
score_list = []
words_list = []
sent_list = []
for sents in tweet_df['tweet']:
  sent_list.append(sents)
  tokens = word_tokenize(sents)
  wnl = nltk.WordNetLemmatizer()
  lemmalist = [wnl.lemmatize(t) for t in tokens]
  NRC_score, NRCwords = NRCscore(lemmalist)
  score_list.append(NRC_score)
  if NRCwords != '':
    words_list.append(NRCwords)

#Cheking if all lists have same length
print(len(sent_list))
print(len(words_list))
print(len(score_list))

avrscore = sum(score_list) / len(score_list)
count = 0
total = 0
for i in score_list:
  if i != 0:
    total+=i
    count+=1
zerolessavr = total/count

print(f'Average is {avrscore : .2f}') #calculates avearge here

print(f'Average with out neutral is {zerolessavr : .2f}')

print(len(words_list))
print(len(score_list))



# utilities
import re
import pickle
import numpy as np
import pandas as pd

# plotting
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# nltk
from nltk.stem import WordNetLemmatizer

# sklearn
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report

binarylex_df = pd.DataFrame({'Words': words_list, 'Score': score_list, 'Sentence' : sent_list})

binarylex_df.head()

import matplotlib.pyplot as plt

print(max(binarylex_df['Score']))
print(min(binarylex_df['Score']))

countscore = []
for i in range(-7, 8):
  count=0
  for score in binarylex_df['Score']:
    if score == i:
      count+=1
  countscore.append(count)

data1 = pd.Series(countscore, index=list(range(-7,8)))
data1.head()

plt.xlabel('Frequency')
plt.ylabel('Score')
plt.title('Frequency of Scores with neutral values')
data1.plot.bar()

plt.xlabel('Frequency')
plt.ylabel('Score')
plt.title('Frequency of Scores without neutral values')
data1.drop(0).plot.bar()

emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad', 
          ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
          ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed', 
          ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
          '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
          '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink', 
          ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}

stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
             'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
             'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',
             'does', 'doing', 'down', 'during', 'each','few', 'for', 'from', 
             'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
             'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
             'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
             'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',
             'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're',
             's', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such',
             't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
             'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 
             'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
             'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
             'why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre",
             "youve", 'your', 'yours', 'yourself', 'yourselves']

def preprocess(textdata):
    processedText = []
    
    # Create Lemmatizer and Stemmer.
    wordLemm = WordNetLemmatizer()
    
    # Defining regex patterns.
    userPattern      = '@[^\s]+'
    hashtagPattern   = r"#[^\s]+"
    urlPattern       = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
        
    # Replace all emojis.
    for emoji in emojis.keys():
        textdata = textdata.replace(emoji, "EMOJI" + emojis[emoji])      
    # Replace @USERNAME to 'USER'.
    textdata = re.sub(userPattern,' USER', textdata)        
    # Replace #hashtag to tag.
    textdata = re.sub(hashtagPattern,' tag', textdata) 
    #Replace url with URL
    textdata = re.sub(urlPattern,' URL',textdata)
    for word in textdata.split():
      # Checking if the word is a stopword.
      #if word not in stopwordlist:
      if len(word)>1:
      # Lemmatizing the word.
        word = wordLemm.lemmatize(word)
        processedText.append(word)
            
    
        
    return processedText

text = ''
processed = []
for i in tweet_df['tweet']:
  processed.append(preprocess(i))

corpus = sum(processed, [])

plt.figure(figsize = (20,20))
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800, collocations=False).generate(" ".join(corpus))
plt.imshow(wc)

for i in range(len(corpus)):
  if corpus[i] == 'tag' or corpus[i] == 'URL' or corpus[i] == 'USER':
    corpus[i] = ''

plt.figure(figsize = (20,20))
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800, collocations=False).generate(" ".join(corpus))
plt.imshow(wc)

corpus = sum(list(binarylex_df['Words']), [])
plt.figure(figsize = (20,20))
wc = WordCloud(max_words = 1000 , width = 1600 , height = 800, collocations=False).generate(" ".join(corpus))
plt.imshow(wc)

#changing score so its has binary of 1 or 0
biscore_list = []
for i in score_list:
  if i > 0:
    biscore_list.append(1)
  elif i < 0:
    biscore_list.append(-1)
  else:
    biscore_list.append(0)
print(biscore_list)

len(biscore_list)

binarylex_df['Binary score'] = biscore_list

binarylex_df.head()

sentiment = binarylex_df['Binary score']

new_corpus = []
for i in processed:
  z = ''
  for x in i:
    z += ' ' + x
  new_corpus.append(z)

print(len(new_corpus))
print(len(sentiment))

test_data = []
test_sentiment = []
for index, score in enumerate(sentiment):
  if score != 0:
    test_data.append(new_corpus[index])
    test_sentiment.append(sentiment[index])



print(len(test_sentiment))
print(len(test_data))

X_train, X_test, y_train, y_test = train_test_split(test_data, test_sentiment, test_size = 0.05, random_state = 0)
print(f'Data Split done.')

vectoriser = TfidfVectorizer(ngram_range=(1,2), max_features=4000)
vectoriser.fit(X_train)
print(f'Vectoriser fitted.')
print('No. of feature_words: ', len(vectoriser.get_feature_names()))

X_train = vectoriser.transform(X_train)
X_test  = vectoriser.transform(X_test)
print(f'Data Transformed.')

def model_Evaluate(model):
    
    # Predict values for Test dataset
    y_pred = model.predict(X_test)

    # Print the evaluation metrics for the dataset.
    print(classification_report(y_test, y_pred))
    
    # Compute and plot the Confusion matrix
    cf_matrix = confusion_matrix(y_test, y_pred)

    categories  = ['Negative','Positive']
    group_names = ['True Neg','False Pos', 'False Neg','True Pos']
    group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)]

    labels = [f'{v1}\n{v2}' for v1, v2 in zip(group_names,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)

    sns.heatmap(cf_matrix, annot = labels, cmap = 'Blues',fmt = '',
                xticklabels = categories, yticklabels = categories)

    plt.xlabel("Predicted values", fontdict = {'size':14}, labelpad = 10)
    plt.ylabel("Actual values"   , fontdict = {'size':14}, labelpad = 10)
    plt.title ("Confusion Matrix", fontdict = {'size':18}, pad = 20)

BNBmodel = BernoulliNB(alpha = 2)
BNBmodel.fit(X_train, y_train)

model_Evaluate(BNBmodel)

SVCmodel = LinearSVC()
SVCmodel.fit(X_train, y_train)
model_Evaluate(SVCmodel)

LRmodel = LogisticRegression(C = 2, max_iter = 5000, n_jobs=-1)
LRmodel.fit(X_train, y_train)
model_Evaluate(LRmodel)

#as data are skewed into positive can also make balanced data by removing random positives
import random as rand
pos = 0
neg = 0
pos_list = []
neg_list = []
for index, score in enumerate(test_sentiment):
  if score > 0:
    pos+=1
    pos_list.append(test_data[index])
  else:
    neg+=1
    neg_list.append(test_data[index])
print(pos, neg)
print(len(pos_list), len(neg_list))

#lets make 600 of each
pos_random = rand.sample(range(1353), 600)
neg_random = rand.sample(range(612), 600)
unskewed_data = []
for i in pos_random:
  unskewed_data.append(pos_list[i])
for i in neg_random:
  unskewed_data.append(neg_list[i])
print(len(unskewed_data))

unskewed_score = [1 if x < 600 else -1 for x in range(1200)]
len(unskewed_score)



X_train, X_test, y_train, y_test = train_test_split(unskewed_data, unskewed_score, test_size = 0.1, random_state = 0)
print(f'Data Split done.')

vectoriser = TfidfVectorizer(ngram_range=(1,2), max_features=3000)
vectoriser.fit(X_train)
print(f'Vectoriser fitted.')
print('No. of feature_words: ', len(vectoriser.get_feature_names()))

X_train = vectoriser.transform(X_train)
X_test  = vectoriser.transform(X_test)
print(f'Data Transformed.')

BNBmodel = BernoulliNB(alpha = 2)
BNBmodel.fit(X_train, y_train)

model_Evaluate(BNBmodel)

SVCmodel = LinearSVC()
SVCmodel.fit(X_train, y_train)
model_Evaluate(SVCmodel)

LRmodel = LogisticRegression(C = 2, max_iter = 3000, n_jobs=-1)
LRmodel.fit(X_train, y_train)
model_Evaluate(LRmodel)