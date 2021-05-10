from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import requests
import bs4
import pandas as pd
import os
import snscrape.modules.twitter as sntwitter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import pycountry as pc
# Create your views here.


def home(request):
    return render(request, 'home.html')


def fetchData(request):
    movie = Movie()
    searchedValue = request.POST['searchValue']

    url = "https://www.reelgood.com/movie/" + searchedValue
    html_code = requests.get(url)
    bs_code = bs4.BeautifulSoup(html_code.text, 'lxml')

    rel_date = ""
    new_search = ""
    for i in searchedValue:
        if i == '-':
            new_search += " "
        else:
            if ord(i) >= 48 and ord(i) <= 57:
                rel_date += i
            else:
                new_search += i
    movie_name = new_search
    release_date = rel_date + "-01-01"
    title = movie_name
    movie.title = title

    images = bs_code.find_all("img", {"class": "css-1sz776d e1181ybh1"})
    image = images[2]['src']
    with open('static/images/pic1.jpg', 'wb') as handle:
        response = requests.get(image, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    imdb_rating = bs_code.find_all(
        "span", {"class": "css-xmin1q ey4ir3j3"})[0].getText()
    movie.imdb = imdb_rating

    if float(imdb_rating) > 0 and float(imdb_rating) <= 5:
        movie.won = "Hell No!"
    elif float(imdb_rating) > 5 and float(imdb_rating) <= 8:
        movie.won = "May be ¯\_(ツ)_/¯"
    else:
        movie.won = "Definitely recommended!"

    description = bs_code.find_all(
        "p", {"itemprop": "description"})[0].getText()
    movie.desc = description

    genre = bs_code.find_all("a", {"class": "css-10wrqt0"})[0].getText()
    movie.genre = genre

    cnc = bs_code.find_all("h3", {"class": "css-i6ptp9 egg5eqo2"})
    lis = []
    for i in cnc:
        lis.append(i.getText())
    movie.cnc = lis

    wtw = bs_code.find_all("title")[0].getText()
    if "Where to Watch It" in wtw:
        movie.wtw = "NA"
    else:
        start = wtw.index("Watch on")
        end = wtw.index("|")
        movie.wtw = wtw[start:end]

    trailer = bs_code.find_all("a", {"class": "css-zniopz e14injhv8"})
    if len(trailer) > 0:
        movie.trailer = trailer[0]['href']
    else:
        movie.trailer = "NA"

    tweets = []
    tweets_list2 = []
    sentiment = []
    sentiments = []
    top5locs = []
    top5locs1 = []
    top5vals = []
    countries = []
    count_ver = 0
    count_norm = 0
    year_count = 0
    yearly_tweets = []
    new_yearly_list = []

    nltk.download('vader_lexicon')
    analyzer = SentimentIntensityAnalyzer()
    params = movie_name + " lang:en since:" + release_date
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(params).get_items()):
        if i > 100000:
            break
        tweets_list2.append([tweet.date, tweet.content, tweet.id, tweet.likeCount, tweet.user.displayname, tweet.user.verified, tweet.user.followersCount,
                            tweet.user.friendsCount, tweet.user.favouritesCount, tweet.user.statusesCount, tweet.user.location])
    tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet', 'ID', 'likes_count', 'Username', 'verified', 'followers',
                                                     'friends', 'favourites', 'statuses', 'location'])
    tweets_df2.sort_values(by=["likes_count"], axis=0,
                           ascending=False, inplace=True)
    top10 = tweets_df2.head(10)
    ids_list = top10['ID'].tolist()
    tweets_list = top10['Tweet'].tolist()
    for i in tweets_list:
        sentiment.append(analyzer.polarity_scores(i))
    for i in sentiment:
        sentiments.append(i['compound'])
    movie.sentiments = sentiments

    for i in ids_list:
        tweets.append('https://twitter.com/jack/status/'+str(i))
    movie.tweets = tweets
    sent_val1 = sum(sentiments)/10
    movie.sent_val = round(((sent_val1+1)/2)*100)

    if movie.sent_val < 40:
        movie.review = "Negative"
    elif movie.sent_val >= 40 and movie.sent_val < 70:
        movie.review = "Neutral"
    else:
        movie.review = "Positive"
    
    for i in range(len(list(pc.countries))):
        countries.append(list(pc.countries)[i].name)
    for j in tweets_df2['location']:
        if j in countries:
            top5locs1.append(j)
    Conter = Counter(top5locs1)
    top5locs1 = Conter.most_common(5)
    for k in range(len(top5locs1)):
        top5locs.append(top5locs1[k][0])
        top5vals.append(top5locs1[k][1])
    movie.con1 = top5locs[0]
    movie.con2 = top5locs[1]
    movie.con3 = top5locs[2]
    movie.con4 = top5locs[3]
    movie.con5 = top5locs[4]
    movie.val1 = top5vals[0]
    movie.val2 = top5vals[1]
    movie.val3 = top5vals[2]
    movie.val4 = top5vals[3]
    movie.val5 = top5vals[4]

    for i in tweets_df2['verified']:
        if i==True:
            count_ver += 1
        else:
            count_norm += 1
    movie.verif = count_ver
    movie.normal = count_norm

    for i in range(int(rel_date),2022):
        for j in tweets_df2['Datetime']:
            if i == j.year:
                year_count += 1
        yearly_tweets.append(year_count)
        year_count = 0
    if len(yearly_tweets)>=5:
        new_yearly_list = yearly_tweets[-5:]
        movie.year1 = new_yearly_list[0]
        movie.year2 = new_yearly_list[1]
        movie.year3 = new_yearly_list[2]
        movie.year4 = new_yearly_list[3]
        movie.year5 = new_yearly_list[4]
    elif len(yearly_tweets)==4:
        movie.year1 = 0
        movie.year2 = yearly_tweets[0]
        movie.year3 = yearly_tweets[1]
        movie.year4 = yearly_tweets[2]
        movie.year5 = yearly_tweets[3]
    elif len(yearly_tweets)==3:
        movie.year1 = 0
        movie.year2 = 0
        movie.year3 = yearly_tweets[0]
        movie.year4 = yearly_tweets[1]
        movie.year5 = yearly_tweets[2]
    elif len(yearly_tweets)==2:
        movie.year1 = 0
        movie.year2 = 0
        movie.year3 = 0
        movie.year4 = yearly_tweets[0]
        movie.year5 = yearly_tweets[1]
    else:
        movie.year1 = 0
        movie.year2 = 0
        movie.year3 = 0
        movie.year4 = 0
        movie.year5 = yearly_tweets[0]
    return render(request, 'info.html', {'movie': movie})
