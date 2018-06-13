"""
UCI SPAM classification using knn
"""

# #Library
import os
import pandas as pd
pd.set_option('display.max_colwidth', -1)

scriptdir = os.path.dirname(os.path.abspath(__file__))

# os.chdir("C:\\NotBackedUp\\datafiles\\uci\\")
os.chdir(scriptdir)

# Read in Data
with open('SMSSpamCollection', 'r') as f:
    lines = f.readlines()

# print(lines[0:2])
text_class = [l.split('\t')[0] for l in lines]
text_msg = [l.split('\t')[1] for l in lines]
text_msg = [t.replace('\n', '') for t in text_msg]

# Create DataFrame
df = pd.DataFrame({'textclass': text_class,
                  'textmessage':  text_msg})


# Subset dataframe for spam
spamdf = df[df['textclass'] == 'spam']
print(spamdf.textmessage.tolist()[0:10])

# Subset dataframe for ham
hamdf = df[df['textclass'] == 'ham']
#print(hamdf.head())

# Checking what is the most common word in spam
spamwordlist = [word for line in spamdf.textmessage.tolist() for word in line.split()]
print(spamwordlist[0:2])

# lowercase
spamwordlist = [word.lower() for word in spamwordlist]

# excluding stop words
stopwords = ['i', 'you', 'he',' she', 'it', 'they', 'we', 'a', 'the', 'is', 'am', 'are', 'was', 'were', 'for', 'to', 'or', 'your']
spamwordlist = [word for word in spamwordlist if word not in stopwords]

setspam = set(spamwordlist)
spamcounter = [spamwordlist.count(word) for word in setspam]
spamdict = dict(zip(list(setspam), spamcounter))

import operator

sortedspam = sorted(spamdict.items(), key=operator.itemgetter(1), reverse=True)
print((sortedspam[0:20]))

# Checking what is the most common word in ham
hamwordlist = [word for line in hamdf.textmessage.tolist() for word in line.split()]
print(hamwordlist[0:2])

# lowercase
hamwordlist = [word.lower() for word in hamwordlist]

# excluding stop words
stopwords2 = ['i', 'you', 'he',' she', 'it', 'they', 'we', 'a', 'the',
              'is', 'am', 'are', 'was', 'were', 'for', 'to', 'or', 'your',
              ':-):):-):-)']
hamwordlist = [word for word in hamwordlist if word not in stopwords2]

setham = set(hamwordlist)
hamcounter = [hamwordlist.count(word) for word in setspam]
hamdict = dict(zip(list(setham), hamcounter))

import operator

sortedham = sorted(hamdict.items(), key=operator.itemgetter(1), reverse=True)
print((sortedham[0:20]))




# A lot of call (342) and free (180) in spam word list


