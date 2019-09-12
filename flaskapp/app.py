import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    request,
    render_template,
    jsonify)

import numpy as np
import pandas as pd
import datetime as dt

import extract_timeline as et
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
    return render_template("layout.html")


@app.route("/", methods=["POST"])
def pull_timeline():
    user = request.form["username"]
    data = et.get_timeline(user)
    et.loadzone(data)
    return render_template("search.html")


@app.route("/search")
def searchpg():
    return render_template("search.html")
    # pass

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


#run the python script
if __name__ == "__main__":
    app.run(debug=True)
