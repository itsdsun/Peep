import tweepy
import requests
import pandas as pd

# _lsun
CONSUMER_KEY = "ax4mZCclRsJ7zrsxujdSSnnhY"
CONSUMER_SECRET = "t0ytgg2eSdnkjobCT0aJxTXzMhbryAeGo69ZYv2sZ8kYJzSn4r"
ACCESS_KEY ="1118664863536914432-hhGBGqWkXwBW8ZyOdZUZmy2sUFM1Tu"
ACCESS_SECRET = "QNQZ4DSrZ7rOIDugsNNDphI77XEBk2Uzz44pCFSuujPAQ"

# authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# variables
api = tweepy.API(auth)
mentions = api.mentions_timeline()
user = api.me()



def get_timeline(username):
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
    try:
        dataframe.to_csv("timeline.csv",encoding='utf-8')
    except:
        print("This shiet dint werk")


# if __name__ == '__main__':
#     tl = get_timeline("laurasun")
#     tocsv(tl)
#     print("Extracted timeline and converted to csv")
