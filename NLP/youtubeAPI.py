'''
This script is to test and play around with youtube API
using Python.

'''

# Libraries
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import httplib2
from httplib2 import socks
import os
import sys
from pprint import pprint

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


# 1. Youtube search by keyword
def youtube_search(keyword, max_results=5):
    '''
    input keyword and this function will search the keyword and returning
    maximum top 5 results
    '''
    res = youtube.search().list(
        q=keyword,
        maxResults=max_results,
        part='id',
        ).execute()

    # will return search result and the video id and also optional snippet
    # snippet is the details information about video results
    return res

# 2. Getting video statistics (single and multiple query)
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

    res = youtube.video().list(
        id = video_id_str,
        part='statistics, snippet',
        maxResults=max_results
        ).execute()

    return res

# 3. Getting all comments from a single video
# refer to youtubeAPI_comments.py
def youtube_comments():
    '''
    get the maximum number of comments in a video and return all
    the comments in text format
    '''

    res = youtube.comment().list(
        ).execute()


    return res

# 4. getting all trending videos from certain countries
def youtube_trending(keyword, max_results=10, region=None, page_token=None):
    '''
    get all the trending videos worldwide or from certain countries
    fill in region to specify trending videos from specific region.
    fill in page token to flip through results pages
    '''

    res = youtube.video().list(
        chart='mostPopular',
        part='id, snippet',
        maxResults=10,
        regionCode=region,
        pageToken=page_token
        ).execute()

    return res

# 5. retrieve top 10 videos by certain sorting category
def youtube_search_sorted(keyword, sort_category, max_results=10, ):
    '''
    search videos and output top 10 based on certain sorting category
    categories include: date, rating, relevance, alphabetical title, viewcount
    default is relevance.
    '''

    accepted_category = ['date', 'rating', 'relevance', 'title', 'viewCount']
    if sort_category not in accepted_category:
        print('Sorting category is wrong. Default to \'relevance\'')
        sort_category = 'relevance'

    res = youtube.search().list(
        q=keyword,
        maxResults=max_results,
        part='id',
        order=sort_category
        ).execute()

    return res

# 6. get all videos from certain channel
def youtube_search_channel(channel_id, max_results=10):
    '''
    search videos and output top 10 based on certain sorting category
    categories include: date, rating, relevance, alphabetical title, viewcount
    default is relevance.
    '''

    res = youtube.search().list(
        channelId=channel_id,
        maxResults=max_results,
        part='id,snippet',
        type='video',
        order='date'
        ).execute()

    return res

# 7. get video by categories
def youtube_search_categories(cat_id, max_results=10):
    '''
    Do a youtube video search by category
    '''
    res = youtube.search().list(
        videoCategoryId=cat_id,
        maxResults=max_results,
        part='id,snippet',
        type='video',
        order='date'
        ).execute()

    return res

# 8. Youtube search video by location
def youtube_search_geoloc(keyword, region='US', max_results=5):
    '''
    input keyword and this function will search the keyword and returning
    maximum top 5 results
    '''
    res = youtube.search().list(
        q=keyword,
        maxResults=max_results,
        part='id, snippet',
        regionCode=region
        ).execute()

    # will return search result and the video id and also optional snippet
    # snippet is the details information about video results
    videos = {}
    for item in res.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            videos[video_id] = video_title
    return videos

# 9. inquire daily quota limit -> can only be done using dashboard tool currently


results = youtube_search_geoloc('seiko', region='ID')
pprint(results)
# End script
print('youtube script success')
