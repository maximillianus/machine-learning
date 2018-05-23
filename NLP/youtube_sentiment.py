# Libraries
import os, sys
import re

## Seiko Baselworld 2018 8 new watches
youtube_link = 'https://www.youtube.com/watch?v=lCStiGKuCw0'

## account to use
google_account = 'vintage.gramophone@gmail.com'

video_id = re.search('v=(.*)', youtube_link, re.IGNORECASE).group(1)

filename = 'youtube_comment_video_' + video_id + '.txt'

# read from file
with open(filename, 'r', encoding='utf8') as f:
    video_comments = eval(f.readline())

print(video_comments)

