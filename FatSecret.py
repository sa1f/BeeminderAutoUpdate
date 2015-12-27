# FatSecret api code credit: https://gist.github.com/pztrick/9203100

from rauth.service import OAuth1Service, OAuth1Session
import os.path
import json
import time
import math
import requests

fatsecret_api_url = 'http://platform.fatsecret.com/rest/server.api'

# Check for fatsecret_info.json, else get access tokens
if not os.path.isfile('fatsecret_info.json'):
    consumer_key = raw_input('Enter your FatSecret consumer key: ')
    consumer_secret = raw_input('Enter your FatSecret consumer secret key: ')

    info = {'key': consumer_key, 'secret': consumer_secret}

    fatsecret = OAuth1Service(
            consumer_key = info['key'],
            consumer_secret = info['secret'],
            name = 'Beeminder',
            request_token_url = 'http://www.fatsecret.com/oauth/request_token',
            access_token_url = 'http://www.fatsecret.com/oauth/access_token',
            authorize_url = 'http://www.fatsecret.com/oauth/authorize')

    # Get request tokens
    request_token, request_token_secret = fatsecret.get_request_token(
                            method = 'GET',
                            params = {'oauth_callback':'oob'})

    authorize_url = fatsecret.get_authorize_url(request_token)

    print 'Visit this URL in your browser: ' + authorize_url
    info['code'] = raw_input('Enter the code from the browser: ')

    # Get access tokens
    info['access_token'], info['access_token_secret'] = fatsecret.get_access_token(
            request_token,
            request_token_secret,
            method = 'POST',
            params={'oauth_verifier': info['code']})

    # Save access tokens for future use
    with open('fatsecret_info.json', 'w') as outfile:
        json.dump(info, outfile)

with open('fatsecret_info.json', 'r') as infile:
    info = json.load(infile)

session = OAuth1Session(info['key'],
                        info['secret'],
                        info['access_token'],
                        info['access_token_secret'])

params = {'method': 'food_entries.get_month', 'format':'json'}
result = session.get(fatsecret_api_url, params=params)
data = result.json()
# timestamp converted into days, oh btw, the 28800 is just converting from utc to pst
date = int(math.floor((time.time() - 28800) / 60 / 60 / 24))

# Get calories for day
for item in data["month"]["day"]:
    if item["date_int"] == str(date):
        calories = item["calories"]
    else:
        calories = 0

params = {'method': 'profile.get', 'format':'json'}
result = session.get(fatsecret_api_url, params=params)
data = result.json()
weight = data["profile"]["last_weight_kg"]


