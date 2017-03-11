## need this API https://github.com/bear/python-twitter
## this is the API https://pypi.python.org/pypi/twitter


import twitter
import json 
 
   
   # XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
   # for these credentials, which you'll need to provide in place of these
   # empty string values that are defined as placeholders.
   # See https://dev.twitter.com/docs/auth/oauth for more information 
   # on Twitter's OAuth implementation.
   
   
   #Put these values in an external python file and import them using the import statement#
   #CONSUMER_KEY = ''
   #CONSUMER_SECRET=''
   #TOKEN='-'
   #TOKEN_SECRET=''
   
import ConfigParser
config=ConfigParser.RawConfigParser()
config.read('tokenstwitter.properties')

CONSUMER_KEY=config.get('twitter','CONSUMER_KEY') 
CONSUMER_SECRET=config.get('twitter','CONSUMER_SECRET') 
TOKEN=config.get('twitter','TOKEN') 
TOKEN_SECRET=config.get('twitter','TOKEN_SECRET') 
   
# auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)

# twitter_api = twitter.Twitter(auth=auth)
#print CONSUMER_KEY

# Authorize Twitter information
auth=twitter.oauth.OAuth(TOKEN,TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
t = twitter.Twitter(auth=auth)

# Retrieve the 10 most recent statuses from the user's screen name
recent_tweets = t.statuses.user_timeline(screen_name='DeschainRo',count=10)

# Dump the information into a newly created JSON file
tweets_in_json= json.dumps(recent_tweets, indent=4, sort_keys=True)
tweets_filename='tweets.json'
f=open(tweets_filename,'w')
f.write(tweets_in_json)
f.close()

# Parse the JSON file and convert the data to a GeoJSON
with open(tweets_filename) as data_file:
   alldata = json.loads (data_file.read())
   geo_data = {
		"type": "FeatureCollection",
		"features": []
	}
   for tweet in alldata:
		geo_json_feature = {
				"type": "Feature",
				"properties": {
					"twitter_handle": tweet['user']['screen_name'],
					"name": tweet['user']['name'],
					"text": tweet['text']
				},
				"geometry": {
					"type": tweet['coordinates']['type'],
					"coordinates": tweet['coordinates']['coordinates']
				}
			}
		geo_data['features'].append(geo_json_feature)
with open('twitter_geodata.json', 'w') as fout:
	fout.write(json.dumps(geo_data, indent=4))



