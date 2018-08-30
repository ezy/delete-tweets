#!/bin/python3
# Largely copied from http://www.mathewinkson.com/2015/03/delete-old-tweets-selectively-using-python-and-tweepy
# However, Mathew's script cannot delete tweets older than something like a year (these tweets are not available from the twitter API)
# This script is a complement on first use, to delete old tweets. It uses your twitter archive to find tweets' ids to delete
# How to use it :
#     - download and extract your twitter archive (tweet.js will contain all your tweets with dates and ids)
#     - put this script in the extracted directory
#     - complete the secrets to access twitter's API on your behalf and, possibly, modify days_to_keep
#     - delete the few junk characters at the beginning of tweet.js, until the first '['   (it crashed my json parser)
#     - review the script !!!! It has not been thoroughly tested, it may have some unexpected behaviors...
#     - run this script
#     - forget this script, you can now use Mathew's script for your future deletions
#
#  License : Unlicense http://unlicense.org/

import tweepy

import json
from datetime import datetime, timedelta, timezone

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
days_to_keep = 30

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)

print(cutoff_date)

fp = open("tweet.js","r")
myjson = json.load(fp)

for tweet in myjson:
    d = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
    if d < cutoff_date:
        print(tweet['created_at'] + " " + tweet['id_str'])
        try:
            api.destroy_status(tweet['id_str'])
        except:
            pass
