'''
This is sentiment analysis from nltk samples and corpora
Twitter samples will be used as data
'''

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize
import random

# Collect data
print(twitter_samples.fileids())


def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words('english')]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

## tweets collection
neg_strings = twitter_samples.strings('negative_tweets.json')
neg_tweets = []
for i,string in enumerate(neg_strings):
    # clean out smileys in strings
    print(i, '-', string)
    clean_str = string.replace(":", "").replace(")", "").replace("(", "")
    words = word_tokenize(clean_str)
    neg_tweets.append((create_word_features(words), 'negative'))

pos_strings = twitter_samples.strings('positive_tweets.json')
pos_tweets = []
for i,string in enumerate(pos_strings):
    # clean out smileys in strings
    print(i, '-', string)
    clean_str = string.replace(":", "").replace(")", "").replace("(", "")
    words = word_tokenize(clean_str)
    pos_tweets.append((create_word_features(words), 'positive'))

random.shuffle(neg_tweets)
random.shuffle(pos_tweets)

train_set = neg_tweets[:4000] + pos_tweets[:4000]
test_set = neg_tweets[4000:] + pos_tweets[4000:]

print(len(train_set), len(test_set))

classifier = NaiveBayesClassifier.train(train_set)

# try classify
testtweet = 'I am sad about what has happened to me'
print('Test Tweet:', testtweet)
res = classifier.classify(create_word_features(word_tokenize(testtweet)))
print('Tweet Sentiment:', res)