import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import extract_timeline as et

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

#create an app
app = Flask(__name__)

#create app routes
@app.route("/")
def welcome():
    # Landing Page
    pass

@app.route("/api/all_tweets")
def example():
    '''
    Testing: This route pulls all tweets from the timeline table
    Current set to personal tweet list
    '''
    alltweets = session.query(timeline.tweet, timeline.date).all()
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
    tweets = session.query(timeline.tweet, timeline.date).filter(timeline.tweet.like(f'%{query}%')).all()
    formatted_data = [{
            "tweet": x[0],
            "date": x[1],
        } for x in tweets]
    return jsonify(formatted_data)


#run the python script
if __name__ == "__main__":
    app.run(debug=True)
