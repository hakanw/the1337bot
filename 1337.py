#!/usr/local/bin/python2.6
# encoding: utf-8
"""
1337.py
Written October 29, 2011 by Håkan Waara (hwaara@gmail.com)
If you use this for something fun, let me know.
"""
import os
import sys
import datetime
import tweepy
import random

required_env_vars = ("CONSUMER_KEY", "CONSUMER_SECRET", "ACCESS_TOKEN_KEY", "ACCESS_TOKEN_SECRET")
for var in required_env_vars:
    if not var in os.environ:
        print "These variables must be set in your environment, with the authentication info from your registered twitter app, in order for the script to access the API: \n", "\n".join(required_env_vars)
        sys.exit(1)

test = "test" in sys.argv

# only run about once every day
if datetime.datetime.now().strftime("%H%M") != "1337":
    print "The time is not 13.37!"
    if not test:
        sys.exit(1)
else:
    print "13.37 ... let's tweet this!"

# login
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)

followers = dict([(user.id, user) for user in api.followers()])
friends = dict([(user.id, user) for user in api.friends()])

# follow people following us
for (user_id, user) in followers.iteritems():
    if user_id in friends:
        # already followed
        del friends[user_id]
    else:
        print "Following user %s" % user.screen_name
        user.follow()

# unfollow people not following us
for user in friends:
    print "Unfollowing user %s" % user.screen_name
    user.unfollow()

message = random.choice(["13.37", "13.37!", "1337", "13.37", "1337!"])

print "Tweeting"
if not test:
    api.update_status(message)
