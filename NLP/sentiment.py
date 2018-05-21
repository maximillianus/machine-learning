"""
Python sentiment analysis
"""

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
import sys


print(sys.argv)

positive_vocab = ['awesome', 'outstanding', 'fantastic' ,'terrific', 'good', 'nice', 'great']
negative_vocab = ['bad', 'terrible', 'useless', 'hate']
neutral_vocab = ['movie', 'the', 'sound', 'was', 'is', 'actors', 'did', 'know', 'words', 'about']

def word_feats(words):
    return dict([(word, True) for word in words])

positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_voacb]

train_set = negative_features + positive_features + neutral_features
classifier = NaiveBayesClassifier.train(train_set)

# Predict
neg = 0
pos = 0
sentence = sys.argv[1] 
sentence = sentence.lower()
words = sentence.split(' ')
for word in words:
    classResult = classifier.classify(word_feats(word))
    if classResult == 'neg':
        neg += + 1
    if classResult == 'pos':
        pos += 1

print('Positive:' + str(float(pos)/len(words)))
print('Negative:' + str(float(neg)/len(words)))
