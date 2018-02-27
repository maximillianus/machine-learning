# ====================================== #
#            Youtube Kaggle              #
# ====================================== #

## ******************************************************** ##
## Script to play around with data science for Kaggle       ##
## This script analyzes youtube trend analytics             ##
##                                                          ##
##                                                          ##
## ******************************************************** ##

rm(list=ls())

## Set directory
maindir <- "C:/NotBackedUp/"
workingdir <- "C:/NotBackedUp/datafiles/kaggle/youtube/"
setwd(workingdir)

## Read data
# CSV
#filename <- 'USvideos_subset.csv'
filename <- 'USvideos.csv'
df <- read.csv(filename, stringsAsFactors = F, encoding='UTF-8')

# JSON
require(jsonlite)
jsonfile <- 'US_category_id.json'
json_data <- fromJSON(jsonfile, flatten = TRUE)
json_df <- json_data$items

# Getting category id
category_df <- json_df[,c('id', 'snippet.title')]
category_df$id <- as.numeric(category_df$id)
category_df <- category_df[order(category_df$id),]
rm(json_data, json_df)
names(category_df) <- c('category_id', 'category')


## Subsetting and write data
#partial_df <- df[c(1:20, 8000:8020, 17550:17578),]
#write.csv(x=partial_df, file="USvideos_subset.csv")

## Counting unique values for each column
as.data.frame(apply(df, 2, function(x) length(unique(x))))



## Data Cleaning

# Trending Date
trend_date <- df$trending_date
trend_date <- as.Date(trend_date, "%y.%d.%m")
df$trending_date <- trend_date
rm(trend_date)

# Publish date & time
names(df)[names(df) == 'publish_time'] <- 'publish_datetime'
pub_datetime <- strptime(df$publish_datetime, "%Y-%m-%dT%H:%M:%OSZ", tz='UTC')
pub_datetime <- as.character(pub_datetime)
pub_date <- sapply(strsplit(pub_datetime,split=" "), `[`, 1)
pub_time <- sapply(strsplit(pub_datetime,split=" "), `[`, 2)
df$publish_date <- pub_date
df$publish_time <- pub_time
rm(pub_date, pub_time, pub_datetime)

# Thumbnails (discard)
df$thumbnail_link <- NULL

# Category ID
categoryid <- df$category_id
df$category_id <- NULL
df$category_id <- categoryid
df2 <- df %>% inner_join(category_df)
names(df2)[18] <- 'category'
df <- df2
rm(df2, categoryid)

#

#

## Data Description

# `df` is divided into multiple video_id over a period of time
# there are 88 days with ~200 video_ids/day so total = 88 * 200 = 17600 rows
# Actual row count is 17578

## Variables / Column
# video_id : chr : unique id referring to individual video
# trending_date : Date : 88 trending days
# title : chr : video title
# channel_title : chr : channel of video owner
# publish_datetime : chr : when video is published
# tags : chr : list of tags 
# views : int : number of views
# likes : int : number of likes
# dislikes : int : number of dislikes
# comment_count : int : number of comments
# thumbnail_link : chr : link to thumbnail
# comments_disabled : chr : whether commenting is disabled
# ratings_disabled : chr : wheter ratings is disabled
# video_error_or_removed : chr : whether video error or removed
# description : chr : video description

## Business questions to answer
require(ggplot2)

## 1. Which video have most likes, dislikes, comment_count, views?

# *Need to get the last index for each duplicate rows of video
df_uniquevid <- df[!rev(duplicated(rev(df$video_id))),]

# Top 10 Videos with most views
df_uniquevid %>% ungroup() %>% 
  select(video_id, views, channel_title, title) %>% 
  arrange(-views) %>% 
  top_n(10, views) %>% 
  ggplot(aes(x=reorder(video_id, -views), y=views, fill=title)) + geom_bar(stat='identity') +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Top 10 Videos with most likes
df_uniquevid %>% ungroup() %>% 
  select(video_id, likes, channel_title, title) %>% 
  arrange(-likes) %>% 
  top_n(10, likes) %>%
  ggplot(aes(x=reorder(video_id, -likes), y=likes, fill=title)) + geom_bar(stat='identity')

# Top 10 Videos with most dislikes
df_uniquevid %>% ungroup() %>% 
  select(video_id, dislikes, channel_title, title) %>% 
  arrange(-dislikes) %>% 
  top_n(10, dislikes) %>%
  ggplot(aes(x=reorder(video_id, -dislikes), y=dislikes, fill=title)) + geom_bar(stat='identity')


# Top 10 Videos with most comment
df_uniquevid %>% ungroup() %>% 
  select(video_id, comment_count, channel_title, title) %>% 
  arrange(-comment_count) %>% 
  top_n(10, comment_count) %>%
  ggplot(aes(x=reorder(video_id, -comment_count), y=comment_count, fill=title)) + 
  geom_bar(stat='identity') +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.text=element_text(size=7),
        legend.position = c(0.75,0.7))

# likes:dislikes ratio for most liked videos

# likes:dislikes ratio for most disliked videos



  
