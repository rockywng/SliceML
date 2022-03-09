import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('wordnet')
#nltk.download('omw-1.4')
pd.set_option('display.max_columns',None)
US_comments = pd.read_csv("C:\\Users\\wangx\\Downloads\\UScomments.csv\\UScomments.csv", error_bad_lines=False, dtype={'video_id':str, 'comment_text':str, 'likes':int, 'replies':int}, encoding='latin-1')
#print(US_comments.head())
US_comments.dropna(inplace=True)
US_comments.drop(41587, inplace=True)
US_comments = US_comments.reset_index().drop('index',axis=1)
US_comments.likes = US_comments.likes.astype(int)
US_comments.replies = US_comments.replies.astype(int)
print("hello")
#US_comments = US_comments.head(90000)
#print(US_comments.head())
#US_comments = US_comments.replace('[^a-zA-Z0-9 ]', '', regex=True)
US_comments['comment_text'] = US_comments['comment_text'].str.replace("[^a-zA-Z#]", " ", regex=True)
print("hi1")
US_comments['comment_text'] = US_comments['comment_text'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
print("hi2")
US_comments['comment_text'] = US_comments['comment_text'].apply(lambda x:x.lower())
print("hi3")
tokenized_tweet = US_comments['comment_text'].apply(lambda x: x.split())
print("hi4")
#tokenized_tweet.head()
wnl = WordNetLemmatizer()
tokenized_tweet.apply(lambda x: [wnl.lemmatize(i) for i in x if i not in set(stopwords.words('english'))]) 
print(tokenized_tweet.head())
#wnl = WordNetLemmatizer()
#tokenized_tweet.apply(lambda x: [wnl.lemmatize(i) for i in x if i not in set(stopwords.words('english'))]) 
#print(tokenized_tweet.head())
for i in range(len(tokenized_tweet)):
    tokenized_tweet[i] = ' '.join(tokenized_tweet[i])
US_comments['comment_text'] = tokenized_tweet
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
US_comments['Sentiment Scores'] = US_comments['comment_text'].apply(lambda x:sia.polarity_scores(x)['compound'])
print(US_comments.head())
US_comments['Sentiment'] = US_comments['Sentiment Scores'].apply(lambda s : 'Positive' if s > 0 else ('Neutral' if s == 0 else 'Negative'))
print(US_comments.head())
US_comments.to_csv('betternlp.csv',  index=False)