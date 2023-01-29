import tweepy
from tweepy import OAuthHandler
from tweepy import API
import pycountry as pyc

# don't steal my token pls <3
BEARER_TOKEN='AAAAAAAAAAAAAAAAAAAAAAQelQEAAAAAMokcw4TlgVwCmVlMdWDxTbAagOs%3DvIsC1frxjuFVZ9sktHxUYEp9ktTVVFIBCsaXWCDX0hD2x7jR7V'

# get tweets
client = tweepy.Client(bearer_token=BEARER_TOKEN)
# TAKE USER INPUT
countryQuery = input("Find recent tweets about travel in a certain country (input country name): ")

keyword = str(countryQuery)+' women safe'  # gets tweets containing women and safe and that country (safe will catch safety)

# get country code to plug in as param in search_recent_tweets
country_code = str(pyc.countries.search_fuzzy(countryQuery)[0].alpha_2)

# get 100 recent tweets containing keywords and from location = countryQuery
query = str(keyword+' -is:retweet')  # search for keyword and no retweets
posts = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['id', 'text', 'entities', 'author_id'])
# filter posts to remove retweets

# export tweets to json
import json
with open('twitter.json', 'w') as fp:
    for tweet in posts.data:
        json.dump(tweet.data, fp)
        fp.write('\n')
        print("* " + str(tweet.text))
        '''
        #if not tweet['retweeted']:
        if 'RT @' not in tweet.text:  # REMOVES RETWEETS
            json.dump(tweet.data, fp)
            fp.write('\n')
            print("* " + str(tweet.text))
        '''