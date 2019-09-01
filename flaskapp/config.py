from configparser import ConfigParser

config = ConfigParser()

config['twitterapi'] = {
    'CONSUMER_KEY' : "ax4mZCclRsJ7zrsxujdSSnnhY",
    'CONSUMER_SECRET' : "t0ytgg2eSdnkjobCT0aJxTXzMhbryAeGo69ZYv2sZ8kYJzSn4r",
    'ACCESS_KEY' : "1118664863536914432-hhGBGqWkXwBW8ZyOdZUZmy2sUFM1Tu",
    'ACCESS_SECRET' : "QNQZ4DSrZ7rOIDugsNNDphI77XEBk2Uzz44pCFSuujPAQ",
}


with open('./dev.ini', 'w') as f:
    config.write(f)
