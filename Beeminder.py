#!/usr/bin/python

from FatSecret import *

# Check for beeminder_info.json, else get auth_token

if not os.path.isfile('beeminder_info.json'):
    print "Sign into beeminder and visit: https://www.beeminder.com/api/v1/auth_token.json"
    info['username'] = raw_input("Enter your username: ")
    info['auth_token'] = raw_input("Enter your auth_token code: ")
    info['weight_goal_name'] = raw_input("Enter your weight goal name: ")
    info['calorie_goal_name'] = raw_input("Enter your calorie goal name: ")
    with open('beeminder_info.json', 'w') as outfile:
        json.dump(info, outfile)


with open('beeminder_info.json', 'r') as infile:
    info = json.load(infile)

params = {'value':weight, 'auth_token': info['auth_token']}
baseUrl = "https://www.beeminder.com/api/v1/" + "users/" + info['username']
r = requests.post(baseUrl + "/goals/" + info['weight_goal_name'] + "/datapoints.json", params=params)

params = {'value':calories, 'auth_token': info['auth_token']}
baseUrl = "https://www.beeminder.com/api/v1/" + "users/" + info['username']
r = requests.post(baseUrl + "/goals/" + info['calorie_goal_name'] + "/datapoints.json", params=params)

