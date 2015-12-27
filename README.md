# FatSecret API

My first project working with REST and Oauth. Just want to get my calorie and weight data from FatSecret into Beeminder


**Requires:** 
* rauth 
* requests 

**Instructions:**

1. Install required modules using pip
2. Get [FatSecret keys](http://platform.fatsecret.com)
3. If you want to get 750words.com details too, then you'll need casperjs, run 'casperjs 750words.js' to get auth
3. Run Beeminder.py
4. For the Beeminder username and goal names, here's the format from one of the goal urls:
    https://www.beeminder.com/{username}/goals/{goalName}
5. Go ahead and automate the script using crontab

# Beeminder AutoRetroratchet (TODO)

Automatically trim safety buffer using casper.js
