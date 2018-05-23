'''
This script is to test and play around with youtube API
using Python to scrape comments.

'''

# Libraries
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import httplib2
from httplib2 import socks
import os
import sys

# Setup a proxy
## ANZ proxy is used below
p = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_HTTP,
                        proxy_host='10.62.36.14',
                        proxy_port=80)

# http connection
# theHttp = httplib2.Http(proxy_info=p)

# https connection (need to disable ssl)
theHttp = httplib2.Http(proxy_info=p, disable_ssl_certificate_validation=True)


# Building youtube connection

DEVELOPER_KEY = "AIzaSyBBHyzwTo0G-F6q3_aL59fYHshiRNS9Sow"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY, http=theHttp)
# youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)



# 3. Getting all comments from a single video
def youtube_comments(video_id):
    '''
    get the maximum number of comments in a video and return all
    the comments in text format
    '''

    res = youtube.commentThreads().list(
        videoId=video_id,
        part='snippet,replies',
        textFormat='plainText',
        maxResults=None
        ).execute()


    for item in res['items']:
        comment = item['snippet']['topLevelComment']
        authorName = comment['snippet']['authorDisplayName']
        text = comment['snippet']['textOriginal']
        print('Comment by %s: %s' % (authorName, text))
        if 'replies' in item:
            replies = item['replies']['comments']
            for reply in replies:
                reply_text = reply['snippet']['textOriginal']
                reply_author = reply['snippet']['authorDisplayName']
                print('  -->Reply by %s: %s' % (reply_author, reply_text))
                

    return res

# 3.b. getting all comments for multiple comment page
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
        print('no more recurse')
        return commentlist
    else:
        print('recursion')
        token = res['nextPageToken']
        commentlist.extend(youtube_comments_multipage(video_id=video_id, nextpage_token=token))
        return commentlist

# 3.c. getting all comments AND replies for multiple comment page
def youtube_comments_replies_multi(video_id, nextpage_token=None):
    '''
    get the maximum number of comments in a video and return all
    the comments in text format recursively
    '''

    res = youtube.commentThreads().list(
        videoId=video_id,
        part='snippet,replies',
        textFormat='plainText',
        maxResults=100,
        pageToken=nextpage_token
        ).execute()

    commentlist = []
    for item in res['items']:
        comment = item['snippet']['topLevelComment']
        text = comment['snippet']['textDisplay']
        authorName = comment['snippet']['authorDisplayName']
        commentID = comment['id']
        totalreplycount = item['snippet']['totalReplyCount']
        print('**total reply count:', totalreplycount)
        print('**CommentID:', commentID)
        print('Comment by %s: %s' % (authorName, text))
        commentlist.append(text)
        if 'replies' in item:
            if totalreplycount < 6:
                replies = item['replies']['comments']
                print('Number of Replies:', len(replies))
                for reply in replies:
                    reply_text = reply['snippet']['textOriginal']
                    reply_author = reply['snippet']['authorDisplayName']
                    commentlist.append(reply_text)
                    print('  Reply by %s: %s' % (reply_author, reply_text))
            elif totalreplycount > 5:
                reply_res = youtube.comments().list(parentId=commentID, part='snippet').execute()
                # print('Number of Replies:', len(reply_res['items']))
                for item2 in reply_res['items']:
                    commentText = item2['snippet']['textOriginal']
                    commentAuthor = item2['snippet']['authorDisplayName']
                    commentlist.append(commentText)
                    # print('Reply by %s: %s' % (commentAuthor, commentText))
        print('-------------------------')
    
    if 'nextPageToken' not in res:
        print('\n**** no more recurse ****\n')
        return commentlist
    else:
        print('\n**** recursion ****\n')
        token = res['nextPageToken']
        commentlist.extend(youtube_comments_replies_multi(video_id=video_id, nextpage_token=token))
        return commentlist

video_id_seiko = 'lCStiGKuCw0'
video_id_me = '5i3cuBygFU8'
# youtube_comment_replies_multi(video_id_me)
# comments = youtube_comment_replies_multi(video_id_seiko)
comments = youtube_comments_multipage(video_id_seiko)
# print(comments)
print(len(comments))

# sample comment ID for replies more than 5
sample_commentID = 'UgyhS9GFtk84qRQR8C14AaABAg'



# End script
print('youtube script success')
