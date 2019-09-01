import tweepy
import requests
import pandas as pd

from configparser import ConfigParser

config = ConfigParser()

config.read('dev.ini')

CONSUMER_KEY = config.get('twitterapi', 'CONSUMER_KEY')
CONSUMER_SECRET = config.get('twitterapi', 'CONSUMER_SECRET')
ACCESS_KEY = config.get('twitterapi', 'ACCESS_KEY')
ACCESS_SECRET = config.get('twitterapi', 'ACCESS_SECRET')

# authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# variables
api = tweepy.API(auth)
mentions = api.mentions_timeline()
user = api.me()



def get_timeline(username):
    '''
        Pulls all time tweets for username
    '''
    all_tweets = []
    datetimes = []
    for status in tweepy.Cursor(api.user_timeline, screen_name='@'+username, tweet_mode="extended").items():
        # print(status.full_text)
        all_tweets.append(status.full_text)
        datetimes.append(status.created_at)
    # print(datetimes[0])
    tl = pd.DataFrame({'tweet':all_tweets,
                        'date':datetimes})
    return tl

def tocsv(dataframe):
    '''
        Puts tweets into csv
    '''
    try:
        dataframe.to_csv("timeline.csv",encoding='utf-8')
    except:
        print("This shiet dint werk")

import pandas as pd
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()


def loadzone(data):
    '''
    Loads timeline into sqlite db

    '''
    try:

        engine = create_engine("sqlite:///peep.sqlite")
        conn = engine.connect()

        data.to_sql(name='timeline', con= engine, if_exists='replace', index=True)
        print("All loaded into database")

    except:
        print("This shiet failed")

# if __name__ == '__main__':
    # tl = get_timeline("laurasun")
#     tocsv(tl)
#     print("Extracted timeline and converted to csv")
