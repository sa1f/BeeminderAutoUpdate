# Credit: https://gist.github.com/pztrick/9203100

from rauth.service import OAuth1Service
from rauth.service import OAuth1Session

api_url = 'http://platform.fatsecret.com/rest/server.api'

fatsecret = OAuth1Service(
        consumer_key = 'CONSUMER_KEY_HERE',
        consumer_secret = 'CONSUMER_SECRET_HERE',
        name = 'Beeminder',
        request_token_url = 'http://www.fatsecret.com/oauth/request_token',
        access_token_url = 'http://www.fatsecret.com/oauth/access_token',
        authorize_url = 'http://www.fatsecret.com/oauth/authorize')

if __name__ == "__main__":
    request_token, request_token_secret = fatsecret.get_request_token(
                            method = 'GET',
                            params = {'oauth_callback':'oob'})
    authorize_url = fatsecret.get_authorize_url(request_token)

    print 'Visit this URL in your browser: ' + authorize_url
    code = raw_input('Enter the code from the browser: ')

    session = fatsecret.get_auth_session(
                request_token,
                request_token_secret,
                params={'oauth_verifier': code})

    REST_params = {'method': 'food_entries.get_month', 'format':'json'}
    result = session.get(api_url, params=REST_params)

    print result.json()
    print result.content

