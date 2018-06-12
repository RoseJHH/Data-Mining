from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import matplotlib.pyplot as plt


DEVELOPER_KEY = "AIzaSyB7bDd1kP5wWi-Mjo8LlapgzJn5m_UnZQA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(q, max_results=20):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=q + " Official Trailer",
        type="video",
        # pageToken=token,
        # order = order,
        part="id,snippet",
        maxResults=max_results,
        # location=location

    ).execute()

    title = []
    channelId = []
    channelTitle = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    tags = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title.append(search_result['snippet']['title'])

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            viewCount.append(response['items'][0]['statistics']['viewCount'])
            likeCount.append(response['items'][0]['statistics']['likeCount'])
            dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])

            print (likeCount)

        if 'commentCount' in response['items'][0]['statistics'].keys():
            commentCount.append(response['items'][0]['statistics']['commentCount'])
        else:
            commentCount.append([])

        if 'tags' in response['items'][0]['snippet'].keys():
            tags.append(response['items'][0]['snippet']['tags'])
        else:
            tags.append([])

    youtube_dict = {'tags': tags, 'channelId': channelId, 'channelTitle': channelTitle,
                    'title': title, 'videoId': videoId,'likeCount':likeCount ,'dislikeCount':dislikeCount,'viewCount': viewCount,'commentCount': commentCount}

    return youtube_dict

read = pd.read_csv('/Users/rosejh/PycharmProjects/ProjectSummer/venv/bom_scraper_master/Movie/Dataset2014.csv' )
print(len(read['name'].index))
# for i in range(low,len(read['name'].index),1):
test=[]
df=[]
index = 0
# for index in range(0,5):#, row in read.iterrows():
test=(youtube_search('Iron Man 3'))
test.keys()
df=pd.DataFrame(data=test)
#     test.append((youtube_search(read['name'].at[index])))
# # test.keys()
#     df.append(pd.DataFrame(data=test[index]))
df1 = df[['title','viewCount','channelTitle','commentCount','likeCount','dislikeCount','tags','videoId','channelId']]
df1.columns = ['Title','viewCount','channelTitle','commentCount','likeCount','dislikeCount','tags','videoId','channelId']
#save file
df1.to_csv('/Users/rosejh/PycharmProjects/ProjectSummer/venv/bom_scraper_master/outYoutube/test.csv')

# import lxml
# import requests
# import time
# import sys
# import progress_bar as PB
# import pandas as pd
# from textblob import TextBlob
# import plotly as py
# import plotly.graph_objs as go
#
#
# YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}'
# YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}'
# key = "AIzaSyB7bDd1kP5wWi-Mjo8LlapgzJn5m_UnZQA"
#
#
# def commentExtract(videoId, count=-1):
#     print ("Comments downloading")
#     page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))
#     while page_info.status_code != 200:
#         if page_info.status_code != 429:
#             print ("Comments disabled")
#             sys.exit()
#
#         time.sleep(20)
#         page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))
#
#     page_info = page_info.json()
#     # print (page_info)
#
#     authorDisplayName = []
#     likeCount = []
#     publishedAt = []
#     comments = []
#     sentiment_value = []
#     sentiments = []
#     co = 0;
#     sentiment = 0
#     positive = 0
#     negative = 0
#
#     for i in range(len(page_info['items'])):
#         comments.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
#         authorDisplayName.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'])
#         likeCount.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'])
#         publishedAt.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'])
#
#         wiki = TextBlob(comments[i])
#         print(wiki)
#         sentiment += wiki.sentiment.polarity
#         if sentiment >= 0:
#             positive += 1
#         else:
#             negative += 1
#
#         sentiment = sentiment / len(page_info['items'])
#         print('\nAverage sentiment: ' + str(sentiment)+'\n')
#         sentiment_value.append(sentiment)
#         if(sentiment >= 0):
#             sentiments.append("Positive")
#         else:
#             sentiments.append("Negative")
#
#         labels = ['Positive', 'Negative']
#         values = [positive, negative]
#         #colors = ['#00E64D', '#B72222']
#
#         trace = go.Pie(labels=labels, values=values)
#
#         py.offline.plot([trace], filename='yt.html')
#
#         co += 1
#
#         if co == count:
#             dict = {'videoId': videoId, 'authorDisplayName': authorDisplayName, 'comments': comments, 'likeCount': likeCount,
#                     'publishedAt': publishedAt, 'sentiment_value': sentiment_value, 'sentiment':sentiments}
#             return dict
#
#
# data_comment = commentExtract("7N3ERfi6WHM",20)
# print (data_comment.keys())
# df_comment = pd.DataFrame(data=data_comment)
# print (df_comment.head())
# df1_comment = df_comment[['videoId','authorDisplayName','comments','likeCount','publishedAt','sentiment_value','sentiment']]
# df1_comment.columns = ['videoId','authorDisplayName','comments','likeCount','publishedAt','sentiment_value','sentiment']
# df1_comment.to_csv('/Users/rosejh/PycharmProjects/ProjectSummer/venv/bom_scraper_master/YT_comment/test.csv')