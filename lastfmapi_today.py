#!/usr/bin/python
import requests
import json
from datetime import datetime
import requests_cache
import time
#from IPython.core.display import clear_output
import pandas as pd
import math
#import csv
import os.path
from os import path

# Mimics the functionality of the Last.FM website by saying how many songs were listened to today.
# All dates are in UTC, so if I want to get it in my timezone, I'll need to make a new column with converted times

# Only set the API to pull data from the max date in the csv file

# API Response Codes
#200: Everything went okay, and the result has been returned (if any).
#301: The server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint name is changed.
#400: The server thinks you made a bad request. This can happen when you don’t send along the right data, among other things.
#401: The server thinks you’re not authenticated. Many APIs require login credentials, so this happens when you don’t send the right credentials to access an API.
#403: The resource you’re trying to access is forbidden: you don’t have the right permissions to see it.
#404: The resource you tried to access wasn’t found on the server.
#503: The server is not ready to handle the request.

#apikey = 6a76bb9ed119dd4394c3f3bb5c0dcbd3
#shared_secret = a571d9b0049be7880a5da881da7df6d7

# ONLY GRAB DATA THAT WE HAVE NOT GRABBED YET
#requests_cache.install_cache('lastfm_cache')

# create another .csv with a sum for each day of songs played that can be an easy reference. That will be added to each time
# Make another csv file to log the max dates from every api call so that there is less to cull through when getting max date


# Load up the most recent date added to the .csv db
#try: # if we have a spreadsheet with data, NICE
if path.exists('lastfm_db.csv') == True:     # check to see if spreadsheet exists
    print('File exists! Wonderful! You are a pro!')
    print('loading')

    time.sleep(1)
    db = pd.read_csv('lastfm_db.csv', delimiter = ',') #, usecols=['date']) # read the csv
    time.sleep(1)
    print('loaded')

    dates = db.iloc[:,3] #['uts'] # grab all dates
    print(dates)
    time.sleep(3)
    #pullDate = str(max(dates))        # set max date
    pullDate = max(dates)
    print('Pull Date: ' + pullDate)
    time.sleep(3)

elif path.exists('lastfm_db.csv') == False: # throw an error if the file doesn't exist, carry on to except
    print("File does not exist!")
    print("First time running! Welcome to the SCROBBLE :)")
    time.sleep(3)
    f = open("lastfm_db.csv", "w")
    header = pd.DataFrame(columns = ["album", "artist", "date", "image", "loved", "mbid", "name", "streamable", "url"])
    header.to_csv(f, header=True)
    pullDate = '1582866560'  #"1572584400"    # set max date as a date before when I started scrobbling
    print("BACK IN BUSINESS")
    f.close()
        #raise Exception("File does not exist!")

#except: # if this is the first time we are ever calling this and we don't have a spreadsheet, make one
#    print("WE HAVE AN ERROR")

#requests_cache.install_cache('lastfm_cache')


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'noahwlibby'}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = '6a76bb9ed119dd4394c3f3bb5c0dcbd3'
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # Create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def get_tracks():
    page = 1
    total_pages = 999999
    responses =  []
    today = datetime.today()

    while page <= total_pages:
        payload = {
            'method': 'user.getrecenttracks',
            'user': 'noahwlibby',
            'extended': 1,
            'limit': 200,
            'page': page,
            'from': pullDate
        }

        # print some of the output so we can see the status
        print("Requesting page {}/{}".format(page, total_pages))
        # clear the output to make things neater
        #clear_output(wait = True)

        # make the API call
        response = lastfm_get(payload)

        # if we get an error, print the response and halt the loop
        if response.status_code != 200:
            print(response.text)
            break

        # extract pagination info
        page = int(response.json()['recenttracks']['@attr']['page'])
        total_pages = int(response.json()['recenttracks']['@attr']['totalPages'])

        # append response
        responses.append(response)

        # open file - outside of while loop
        # does this data already exist in the file?
        # if no, append it to the end of the file
        # at the end, close the file - outside of while loop

        # if it's not a cached result, sleep
        if not getattr(response, 'from_cache', False):
            time.sleep(0.25)

        # increment the page number
        page += 1
    return responses

responses = get_tracks()
# bring the list of lists into a list of dataframes and then to a single df
frames = [pd.DataFrame(r.json()['recenttracks']['track']) for r in responses]
alltracks = pd.concat(frames, sort=True)
alltracks.info()
#alltracks.head()



# Also figure out why the api isn't actually pulling in new data. Probably somethin to do with the way that the cache is set up

def playing_now(df):
    pos = 0
    try:
        for i in df['@attr']:
            if isinstance(i,dict): # there should only ever be one dictionary, with value 'true' - everything else is NaN
                trackname   = df.iloc[pos,7]
                artistname  = df.iloc[pos,2]
                date        = df.iloc[pos,3]
                album       = df.iloc[pos,2]
                return trackname
                break
            else:
                pos += 1
    except:
        print("not currently listening")
        return

def totalsongstoday(df):
    today = date.today()



#a = playing_now(alltracks)
#print(a)

with open('lastfm_db.csv', 'w') as f:
    alltracks.to_csv(f, mode="a", header=True)
#print(alltracks.iloc[1,6])
#print(a)
#print(alltracks['artist'][1])

#playing = playing_now(responses)
#print(playing)

#recenttracks_dump = jprint(r.json()['recenttracks']['track'])


#jprint(r.json()[recenttracks_dump])


# Need a solution to access the attributes of a nested JSON object.
# I.e.: [recenttracks][track][@attr] returns an error
def nested_jprint(obj):
    # Convert your input dictionary to a string using json.dumps()
    data = json.dumps(obj, sort_keys = True, indent = 4)
    # Write the string to a file
    with open("test.json", 'w') as test:
        test.write(data)

    # Read it back
    with open("test.json") as test:
        data = test.read()

    # decoding the JSON to dictionary
    d = json.loads(data)

#a = nested_jprint(alltracks)


"""
# get track counts
track_count = [len(r.json()['recenttracks']['track']) for r in responses]
pd.Series(track_count).value_counts()
print(track_count)
"""



#if __name__ == "__main__":
# user = input("Username: ")















    #
