from django.db import models

#Movie model which can be accessed at html page using jinja
class Movie:
    title: str
    imdb: float #imdb rating
    desc: str #description
    genre: str
    cnc: list #cast and crew
    wtw: str #where to watch?
    won: str #should you watch?
    trailer: str 
    tweets: list
    sentiments: list #sentiment list of all tweets
    sent_val: float #mean of compounds of all tweets
    review: str #postive or neutral or negative
    #top 5 countries talking about movie
    con1: str
    con2: str
    con3: str
    con4: str
    con5: str
    #No of tweets from each countries respectively
    val1: int
    val2: int
    val3: int
    val4: int
    val5: int
    verif: int #No of verified users
    normal: int #No of non-verified users
    #No of tweets per year for past 5 years
    year1: int
    year2: int
    year3: int
    year4: int
    year5: int