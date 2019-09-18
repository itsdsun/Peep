import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    request,
    render_template,
    json,
    jsonify)

# to analyze tweets
import numpy as np
import pandas as pd
import datetime as dt

# to extract and load timeline into sqlite
import extract_timeline as et

# for filtering words
from collections import Counter
import nltk
'''

#set up database
#create engine to connect
engine = create_engine("sqlite:///peep.sqlite", connect_args={'check_same_thread': False})

#reflect databases and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

#reference to each table
timeline = Base.classes.timeline


#create session
session = Session(engine)
'''


from flask_sqlalchemy import SQLAlchemy

#create an app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///peep.sqlite"

sesh = SQLAlchemy(app)


class timeline(sesh.Model):
    __tablename__ = 'timeline'

    index = sesh.Column(sesh.Integer, primary_key=True)
    tweet = sesh.Column(sesh.String)
    date = sesh.Column(sesh.String)

    def __repr__(self):
        return '<timeline %r>' % (self.name)



@app.route("/", methods=["GET"])
def welcome():
    # Landing Page
    return render_template("testindex.html")


@app.route("/", methods=["POST"])
def pull_timeline():
    user = request.form["username"]
    data = et.get_timeline(user)
    et.loadzone(data)
    return render_template("search.html")


@app.route("/api/all_tweets")
def example():
    '''
    Testing: This route pulls all tweets from the timeline table
    Current set to personal tweet list
    '''
    alltweets = sesh.session.query(timeline.tweet, timeline.date).all()
    formatted_data = [{
            "tweet": x[0],
            "date": x[1],
        } for x in alltweets]
    return jsonify(formatted_data)

@app.route("/api/search/<query>")
def search(query):
    """
    Testing: This route queries from one timeline table

    Other way of querying:
    # q = f"SELECT * FROM timeline WHERE tweet LIKE '%{query}%'"
    # tweets = engine.execute(q).fetchall()
    """
    tweets = sesh.session.query(timeline.tweet, timeline.date).filter(timeline.tweet.like(f'%{query}%')).all()
    formatted_data = [{
            "tweet": x[0],
            "date": x[1],
        } for x in tweets]
    return jsonify(formatted_data)

@app.route("/api/stats")
def nani():
    try:
        alltweets = sesh.session.query(timeline.tweet, timeline.date).all()
        df = pd.DataFrame([(d.tweet, d.date) for d in alltweets], columns=['tweet', 'date'])
        all_rt = df[df['tweet'].str.match('RT')]
        total_rt = int(all_rt['tweet'].count())
        all_replies = df[df['tweet'].str.contains('@')]
        total_replies = int(all_replies['tweet'].count())

        # Top 3 RT person
        rt_dict = {}
        for x in all_rt['tweet']:
            tt = x.split()
            if tt[1] not in rt_dict:
                rt_dict[tt[1]] = 1
            else:
                rt_dict[tt[1]] += 1

        rt_df = pd.DataFrame(list(rt_dict.items()), columns=['username', 'count'])
        rd_df2 = rt_df.sort_values(by='count', ascending=False).head(3)


        uncleanwords = " ".join(df["tweet"]).split()
        words = []
        for x in uncleanwords:
            if '@' not in x:
                words.append(x)


        stopwords1 = nltk.corpus.stopwords.words('english')

        # add an exclude filter
        stopwords2 = ['u', 'I', 'RT', 'ur', 'da', 'im', 'r', 'like', 'dis','ya','rn','got','n','the','The']

        stopwords = stopwords1.extend(stopwords2)

        words_except_stop_dist = nltk.FreqDist(w for w in words if w not in stopwords1)

        topwords = pd.DataFrame(words_except_stop_dist.most_common(10),
                            columns=['Word', 'Frequency'])

        hashtags = []
        for x in uncleanwords:
            if '#' in x:
                hashtags.append(x)

        hashtagfreq = nltk.FreqDist(w for w in hashtags)

        tophashtags = pd.DataFrame(hashtagfreq.most_common(10),
                            columns=['Word', 'Frequency'])

        # Average word length of tweets
        allthetweets = list(df['tweet'])
        noRT= [x for x in allthetweets if "RT" not in x]
        noRTlen = [len(x.split()) for x in noRT]
        avgword = round((sum(noRTlen) / len(noRTlen)),2)

        # Average character length of tweets
        noRTlenbychar = [len(list(x)) for x in noRT]
        avgchar = round((sum(noRTlenbychar) / len(noRTlenbychar)),2)


        statsdata = {
        "retweets": total_rt,
        "replies": total_replies,
        "top_RT": [{"count": int(rd_df2['count'].values[0]),
                    "username": str(rd_df2['username'].values[0])},
                    {"count": int(rd_df2['count'].values[1]),
                                "username": str(rd_df2['username'].values[1])},
                    {"count": int(rd_df2['count'].values[2]),
                                "username": str(rd_df2['username'].values[2])}
                    ],
        "top_words": [{"tweet": str(topwords['Word'].values[x]),
                                "frequency": int(topwords['Frequency'].values[x])
                                } for x in range(10)],
        # "top_hashtags": [{"tweet": str(tophashtags['Word'].values[x]),
        #                         "frequency": int(tophashtags['Frequency'].values[x])
        #                         } for x in range(9)]
        "average_words_per_tweet": float(avgword),
        "average_char_per_tweet": float(avgchar)

        }


    except Exception as e:
        print(e)

    return jsonify(statsdata)

#run the python script
if __name__ == "__main__":
    app.run(debug=True)
