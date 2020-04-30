# -*- coding: utf-8 -*-
# Data 477 - Data Capping Project
## Team Young Women
## Allison, Amy, and Kaitlyn


# Commented out IPython magic to ensure Python compatibility.
import seaborn as sns
from matplotlib import colors

!pip install twitterscraper
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import string
from twitterscraper import query_tweets
import datetime as dt

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import keras

### Loading Twitter Data

begin_date = dt.date(2020, 1, 20)
lang = 'english'

tweets = query_tweets("quotepage", begindate=begin_date, lang=lang)
tweets2 = query_tweets("InsipereLifeMe", begindate=begin_date, lang=lang)
tweets3 = query_tweets("MotivationalUi", begindate=begin_date, lang=lang)
tweets4 = query_tweets("1000PlusQuotes", begindate=begin_date, lang=lang)

df1 = pd.DataFrame(t.__dict__ for t in tweets)
dfA = pd.DataFrame(t.__dict__ for t in tweets2)
dfB = pd.DataFrame(t.__dict__ for t in tweets3)
dfC = pd.DataFrame(t.__dict__ for t in tweets4)

###Cleaning Twitter Data

def newTweets(df1):
  screenName = df1[ df1['screen_name'] != 'quotepage' ].index # Saving tweets from this user
  df1.drop(screenName, inplace=True) # Dropping tweets from other users
  df1 = df1[['text']] # Saving tweet column
  df1 = df1.drop_duplicates(subset ="text", keep='first', inplace=False) # Dropping duplicates
  df1 = df1.reset_index(drop=True) # Resetting index
  df1 = df1.rename(columns={'text': 'QUOTE'}) # Renaming Column
  df1['QUOTE'] = df1['QUOTE'].str.split(r'"').str.get(1) # Extracting quote from quotations
  return df1

def newTweetsA(dfA):
  screenName = dfA[ dfA['screen_name'] != 'InsipereLifeMe' ].index # Saving tweets from this user
  dfA.drop(screenName, inplace=True) # Dropping tweets from other users
  dfA = dfA[['text']] # Saving tweet column
  dfA= dfA.drop_duplicates(subset ="text", keep='first', inplace=False) # Dropping duplicates
  dfA = dfA.reset_index(drop=True) # Resetting index
  dfA = dfA.rename(columns={'text': 'QUOTE'}) # Renaming Column
  #dfA['QUOTE'] = dfA['QUOTE'].str.split(r'"').str.get(1) # Extracting quote from quotations
  return dfA

def newTweetsB(df):
  screenName = df[ df['screen_name'] != 'MotivationalUi' ].index # Saving tweets from this user
  df.drop(screenName, inplace=True) # Dropping tweets from other users
  df = df[['text']] # Saving tweet column
  df= df.drop_duplicates(subset ="text", keep='first', inplace=False) # Dropping duplicates
  df = df.reset_index(drop=True) # Resetting index
  df = df.rename(columns={'text': 'QUOTE'}) # Renaming Column
  #df['QUOTE'] = df['QUOTE'].str.split(r'"').str.get(1) # Extracting quote from quotations
  return df

def newTweetsC(df):
  screenName = df[ df['screen_name'] != '1000PlusQuotes' ].index # Saving tweets from this user
  df.drop(screenName, inplace=True) # Dropping tweets from other users
  df = df[['text']] # Saving tweet column
  df= df.drop_duplicates(subset ="text", keep='first', inplace=False) # Dropping duplicates
  df = df.reset_index(drop=True) # Resetting index
  df = df.rename(columns={'text': 'QUOTE'}) # Renaming Column
  df['QUOTE'] = df['QUOTE'].str.split(r'"').str.get(1) # Extracting quote from quotations
  return df

df1 = newTweets(df1)
dfA = newTweetsA(dfA)
dfB = newTweetsB(dfB)
dfC = newTweetsC(dfC)

### Making one database of all the quotes

def appendDF(df1, dfA, dfB, dfC):
  df1 = df1.append(dfA) # Appending tweets to original dataframe
  df1 = df1.append(dfB)
  df1 = df1.append(dfC)
  df1 = df1.reset_index(drop=True) # Resetting index
  return df1

df2 = appendDF(df1, dfA, dfB, dfC)

def cleanTwitter(df2):
  def split(word):
    return len([char for char in word])
  df2['Number of Words'] = df2['QUOTE'].str.split().map(len)
  df2['Number of Characters'] = df2.QUOTE.apply(split)
  df2['Char280'] = (df2['Number of Characters'] <= 280)
  return df2

df2 = cleanTwitter(df2)

### Making the Graphs used on the website

plt.figure(figsize=(10,7))
plt.title('Number of Words in Each Quote of Twitter Data' , fontsize=20)
plt.ylabel('Count', fontsize=15)
sns.distplot(df2['Number of Words'], hist=True, kde=False,
             bins=90, color='#fc94af',
             hist_kws={'edgecolor':'#fc94af'},
             kde_kws={'linewidth': 4})
plt.xlabel('Number of Words', fontsize=15)

plt.savefig('word_with_twitter.png') #saving the figure

plt.figure(figsize=(10,7))
plt.title('Number of Characters in Each Quote of Twitter Data', fontsize=20)
plt.ylabel('Count', fontsize=15)
sns.distplot(df2['Number of Characters'], hist=True, kde=False,
             bins=90, color = '#fc94af',
             hist_kws={'edgecolor':'#fc94af'},
             kde_kws={'linewidth': 4})
plt.xlabel('Number of Character', fontsize=15)

plt.savefig('char_with_twitter.png') #saving the figure
