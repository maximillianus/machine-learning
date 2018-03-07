# Library
import pandas as pd
import os
import sys
import csv
import chardet
import codecs

scriptloc = os.path.dirname(os.path.abspath(__file__))

print(sys.executable)

os.chdir(scriptloc)
print(os.getcwd())

## Read in Data
youtube = pd.read_csv('USvideos.csv', encoding='utf-8')
#print(youtube.head())

## Understanding data
#print(youtube.shape)
#print(youtube.info())

# video id & title
# these 2 should correlate but apparently more title than video id
# this means some title is changed along the way.
# So stick with video_id as key

# trending_date
# 88 unique date


# Data cleaning
# trending date needs cleaning
youtube['trending_date'] = pd.to_datetime(youtube.trending_date, format='%y.%d.%m')


# there will be duplicates video_id in the data because this data is grabbed weekly
# we need to find the latest and drop dupes
# method1
# yt = youtube.sort_values('trending_date', ascending=False).drop_duplicates('video_id')

# method2
id_latest = youtube.groupby('video_id')['trending_date'].idxmax()
yt = youtube.loc[id_latest]

## Exploring statistics
# most likes & dislikes
print(yt[yt.likes == yt.likes.max()].title)
print(yt[yt.dislikes == yt.dislikes.max()].title)

# most views & comments
print(yt[yt.comment_count == yt.comment_count.max()].title)
print(yt[yt.views == yt.views.max()].title)

# top 10 channel that keeps on trending
print(yt.channel_title.value_counts().head(10))







