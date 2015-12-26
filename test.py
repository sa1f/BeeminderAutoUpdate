# Credit: https://gist.github.com/pztrick/9203100

from rauth.service import OAuth1Service
from rauth.service import OAuth1Session
import os.path
import json

api_url = 'http://platform.fatsecret.com/rest/server.api'

if not os.path.isfile('info.json'):
    consumer_key = raw_input('Enter your consumer key:  ')
    consumer_secret = raw_input('Enter your consumer secret key:  ')

    info = {'key': consumer_key, 'secret': consumer_secret}
    with open('info.json', 'w') as outfile:
        json.dump(info, outfile)
else:
    with open('info.json', 'r') as infile:
        info = json.load(infile)


fatsecret = OAuth1Service(
        consumer_key = info['key'],
        consumer_secret = info['secret'],
        name = 'Beeminder',
        request_token_url = 'http://www.fatsecret.com/oauth/request_token',
        access_token_url = 'http://www.fatsecret.com/oauth/access_token',
        authorize_url = 'http://www.fatsecret.com/oauth/authorize')

if __name__ == "__main__":
    if not 'code' in info:
        info['request_token'], info['request_token_secret'] = fatsecret.get_request_token(
                                method = 'GET',
                                params = {'oauth_callback':'oob'})
        authorize_url = fatsecret.get_authorize_url(info['request_token'])

        print 'Visit this URL in your browser: ' + authorize_url
        info['code'] = raw_input('Enter the code from the browser: ')

        with open('info.json', 'w') as outfile:
            json.dump(info, outfile)


    session = fatsecret.get_auth_session(
                info['request_token'],
                info['request_token_secret'],
                params={'oauth_verifier': info['code']})

    params = {'method': 'food_entries.get_month', 'format':'json'}
    result = session.get(api_url, params=params)

    print result.json()
    print result.content

