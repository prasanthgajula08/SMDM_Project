import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data to
tweets_list2 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
params="AvengersEndgame lang:en since:2019-04-26"
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(params).get_items()):
    tweets_list2.append([tweet.date,tweet.content,tweet.id,tweet.likeCount,tweet.user.displayname, tweet.user.verified, tweet.user.followersCount, 
    tweet.user.friendsCount, tweet.user.favouritesCount, tweet.user.statusesCount, tweet.user.location])
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime','Tweet','ID','likes_count','Username','verified','followers',
'friends','favourites','statuses','location'])
tweets_df2.to_csv('Ave_endGame.csv')