"""
Creating sentiment analysis out of a single youtube videos
"""

import json
import sys
import re
from pprint import pprint
# sys.path.append("C:\\NotBackedUp\\codes\\Pyscript\\MachineLearning\\NLP\\")


#### Outlining steps ####
# 1. Select a popular (2M view counts) youtube videos in English
# 2. Extract the likes/dislikes and comments
# 3. Determine the sentiment whether it is positive or negative from likes and comment

# 1. select a popular video link
## Casey Neistat - Best Airplane seat
# youtube_link = 'https://www.youtube.com/watch?v=k5mF56PO6vE'

## Seiko Baselworld 2018 8 new watches
youtube_link = 'https://www.youtube.com/watch?v=lCStiGKuCw0'

## account to use
google_account = 'vintage.gramophone@gmail.com'

# 2. Defining youtube functions
def youtube_builder(usingproxy=True):
    import httplib2
    from httplib2 import socks
    from apiclient.discovery import build

    p = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_HTTP,
                            proxy_host='10.62.36.14',
                            proxy_port=80)

    # http connection
    theHttp = httplib2.Http(proxy_info=p)

    # https connection (need to disable ssl)
    theHttp = httplib2.Http(proxy_info=p, disable_ssl_certificate_validation=True)


    # Building youtube connection

    DEVELOPER_KEY = "AIzaSyBBHyzwTo0G-F6q3_aL59fYHshiRNS9Sow"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    if usingproxy ==True:
       youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY, http=theHttp)
    else:
       youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Returning youtube object
    return youtube

def youtube_stats(video_id, max_results=5):
    '''
    get the statistics of a youtube video including likes/dislikes,
    view counts, comment counts for single or multiple videos
    '''
    # ensure that keyword is string
    if type(video_id) == list:
        video_id_str = ','.join(video_id)
    elif type(video_id) == str:
        video_id_str = video_id
    else:
        video_id_str = str(video_id)

    res = youtube.videos().list(
        id = video_id_str,
        part='statistics, snippet',
        maxResults=max_results
        ).execute()

    stats = res['items'][0]['statistics']

    return stats

def youtube_comments_multipage(video_id, nextpage_token=None):
    '''
    get the maximum number of comments in a video and return all
    the comments in text format recursively
    '''

    res = youtube.commentThreads().list(
        videoId=video_id,
        part='snippet',
        textFormat='plainText',
        maxResults=50,
        pageToken=nextpage_token
        ).execute()

    commentlist = []
    for item in res['items']:
        comment = item['snippet']['topLevelComment']
        text = comment['snippet']['textDisplay']
        authorName = comment['snippet']['authorDisplayName']
        commentlist.append(text)
        # print('Comment by %s: %s' % (authorName, text))
    
    if 'nextPageToken' not in res:
        # print('no more recurse')
        return commentlist
    else:
        # print('recursion')
        token = res['nextPageToken']
        commentlist.extend(youtube_comments_multipage(video_id=video_id, nextpage_token=token))
        return commentlist

# 3. extract the likes/dislikes and comments

# build youtube object
youtube = youtube_builder(usingproxy=True)

# get video_id from link
video_id = re.search('v=(.*)', youtube_link, re.IGNORECASE).group(1)

# get statistics
video_stat = youtube_stats(video_id)
# pprint(video_stat, depth=3)
print(video_stat)

# get comments
video_comments = youtube_comments_multipage(video_id)
print(len(video_comments))
# print('\n'.join(video_comments))

# write results to file so to stop scraping everytime
filename = 'youtube_comment_video_' + video_id
print(filename)

with open(filename+'.txt', 'w', encoding='utf-8') as f:
    f.write(str(video_comments))

# 4. Determine whether sentiment is positive or negative


print('script success')
