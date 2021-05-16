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
    movie = Movie()  # Movie object
    searchedValue = request.POST['searchValue']  # user's search query

    # search query appended to reelgood url
    url = "https://www.reelgood.com/movie/" + searchedValue
    html_code = requests.get(url)  # url's html code
    bs_code = bs4.BeautifulSoup(html_code.text, 'lxml')  # beatified html code
    
    rel_date = ""
    new_search = ""
    # seperates movie name and year from search query
    for i in searchedValue:
        if i == '-':
            new_search += " "
        else:
            if ord(i) >= 48 and ord(i) <= 57:
                rel_date += i
            else:
                new_search += i
    movie_name = new_search  # seperated movie name
    release_date = rel_date + "-01-01"  # year appended with jan 1st for future use
    title = movie_name
    movie.title = title  # Movie model title initialised

    # finds img tag in html code with given class name
    images = bs_code.find_all("img", {"class": "css-1sz776d e1181ybh1"})
    image = images[2]['src']  # fetched movie poster
    # Download the image at the given location
    with open('static/images/pic1.jpg', 'wb') as handle:
        response = requests.get(image, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    imdb_rating = bs_code.find_all(
        "span", {"class": "css-xmin1q ey4ir3j3"})[0].getText() #fetched imdb rating using particular tag and its class
    movie.imdb = imdb_rating #Movie model imdb initialised

    #initialise "watch or not?" string of movie model based on the range of imdb rating
    if float(imdb_rating) > 0 and float(imdb_rating) <= 5:
        movie.won = "Hell No!"
    elif float(imdb_rating) > 5 and float(imdb_rating) <= 8:
        movie.won = "May be ¯\_(ツ)_/¯"
    else:
        movie.won = "Definitely recommended!"

    description = bs_code.find_all(
        "p", {"itemprop": "description"})[0].getText() #fetched description using particular tag and its class
    movie.desc = description #Movie model description initialised

    genre = bs_code.find_all("a", {"class": "css-10wrqt0"})[0].getText() #fetched genre using particular tag and its class
    movie.genre = genre #Movie model genre initialised

    cnc = bs_code.find_all("h3", {"class": "css-i6ptp9 egg5eqo2"}) #fetched "cast and crew" using particular tag and its class
    lis = []
    for i in cnc:
        lis.append(i.getText()) #storing each value in cast and crew in a list
    movie.cnc = lis #Movei model cast and crew initialised

    wtw = bs_code.find_all("title")[0].getText() #fetched "where to watch?" using particular tag and its class
    #handled null value error
    if "Where to Watch It" in wtw:
        movie.wtw = "NA"
    else:
        start = wtw.index("Watch on")
        end = wtw.index("|")
        movie.wtw = wtw[start:end]

    trailer = bs_code.find_all("a", {"class": "css-zniopz e14injhv8"}) #fetched trailer link using particular tag and its class
    #handled null value error
    if len(trailer) > 0:
        movie.trailer = trailer[0]['href']
    else:
        movie.trailer = "NA"

    #All the required initialisations for below code to function properly
    #follwoing two lists are used to initialise tweets list in movie model
    tweets = []
    tweets_list2 = []
    #follwoing two lists are used to initialise sentiments list in movie model
    sentiment = []
    sentiments = []
    #follwoing initialisations are used to initialise cons and vals in movie model
    top5locs = []
    top5locs1 = []
    top5vals = []
    countries = []
    count_ver = 0 #No of verified users count
    count_norm = 0 #No of non-verified users count
    #follwoing initialisations are used to initialise years in movie model
    year_count = 0
    yearly_tweets = []
    new_yearly_list = []

    nltk.download('vader_lexicon') #downloads vader lexicon
    analyzer = SentimentIntensityAnalyzer() #create SentimentIntensityAnalyzer object
    #following code generates dataframe containing the columns specified in line number 130 and stored in tweets_df2
    params = movie_name + " lang:en since:" + release_date
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(params).get_items()):
        if i > 100000:
            break
        tweets_list2.append([tweet.date, tweet.content, tweet.id, tweet.likeCount, tweet.user.displayname, tweet.user.verified, tweet.user.followersCount,
                            tweet.user.friendsCount, tweet.user.favouritesCount, tweet.user.statusesCount, tweet.user.location])
    tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet', 'ID', 'likes_count', 'Username', 'verified', 'followers',
                                                     'friends', 'favourites', 'statuses', 'location'])
    tweets_df2.sort_values(by=["likes_count"], axis=0,
                           ascending=False, inplace=True) #sort dataframe based on likes_count
    top10 = tweets_df2.head(10) #pick frist 10 tweets from sorted dataframe
    ids_list = top10['ID'].tolist() #select tweet ID column of those 10 tweets to display on webpage
    tweets_list = tweets_df2['Tweet'].tolist() #select tweet column of all tweets
    for i in tweets_list:
        sentiment.append(analyzer.polarity_scores(i)) #find polarity score of each tweet
    for i in sentiment:
        sentiments.append(i['compound']) #select compoud key from the dictionary generted by above code for each tweet
    movie.sentiments = sentiments #store all compounds of all tweets

    for i in ids_list:
        tweets.append('https://twitter.com/x/status/'+str(i)) #store tweet urls of top 10 to display on webpage
    movie.tweets = tweets #initialise tweets list in movie model
    #calculate mean of all the compounds of all tweets
    sent_val1 = sum(sentiments)/100000
    movie.sent_val = round(((sent_val1+1)/2)*100)

    #Classify movie revie as negative or neutral or positive based in mean value
    if movie.sent_val < 40:
        movie.review = "Negative"
    elif movie.sent_val >= 40 and movie.sent_val < 70:
        movie.review = "Neutral"
    else:
        movie.review = "Positive"

    for i in range(len(list(pc.countries))):
        countries.append(list(pc.countries)[i].name) #store on country names in a list using pycountry library
    #store all the valid country locations in a new list by checking location column of tweets with previously stored country names
    for j in tweets_df2['location']:
        if j in countries:
            top5locs1.append(j)
    #count the total of each country in the new list and pick top 5 countries based on count
    Conter = Counter(top5locs1)
    top5locs1 = Conter.most_common(5)
    #iterate over the top 5 countries and initialise cons and vals of movie model
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

    #count the no of verified and non-verfied user by iterating over verified column of dataframe
    for i in tweets_df2['verified']:
        if i == True:
            count_ver += 1
        else:
            count_norm += 1
    #initialise those counts to corresponding movie model variables
    movie.verif = count_ver
    movie.normal = count_norm

    #fetch the no of tweets per year for past 5 years
    for i in range(int(rel_date), 2022):
        for j in tweets_df2['Datetime']:
            if i == j.year:
                year_count += 1
        yearly_tweets.append(year_count)
        year_count = 0
    #if movie is released 5 or greater than 5 years ago
    if len(yearly_tweets) >= 5:
        new_yearly_list = yearly_tweets[-5:]
        movie.year1 = new_yearly_list[0]
        movie.year2 = new_yearly_list[1]
        movie.year3 = new_yearly_list[2]
        movie.year4 = new_yearly_list[3]
        movie.year5 = new_yearly_list[4]
    #if the movie is released 4 years ago
    elif len(yearly_tweets) == 4:
        movie.year1 = 0
        movie.year2 = yearly_tweets[0]
        movie.year3 = yearly_tweets[1]
        movie.year4 = yearly_tweets[2]
        movie.year5 = yearly_tweets[3]
    #if the movie is released 3 years ago
    elif len(yearly_tweets) == 3:
        movie.year1 = 0
        movie.year2 = 0
        movie.year3 = yearly_tweets[0]
        movie.year4 = yearly_tweets[1]
        movie.year5 = yearly_tweets[2]
    #if the movie is released 2 years ago
    elif len(yearly_tweets) == 2:
        movie.year1 = 0
        movie.year2 = 0
        movie.year3 = 0
        movie.year4 = yearly_tweets[0]
        movie.year5 = yearly_tweets[1]
    #if the movie is released 1 years ago
    else:
        movie.year1 = 0
        movie.year2 = 0
        movie.year3 = 0
        movie.year4 = 0
        movie.year5 = yearly_tweets[0]
    return render(request, 'info.html', {'movie': movie})
