#!/usr/bin/python
import requests
import json
from datetime import datetime
#import requests_cache
import time
#from IPython.core.display import clear_output
import pandas as pd
import math
#import csv
import os.path
from os import path
from operator import attrgetter

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

## TO DO:
# • Move the storage from .csv to sqlite database
# • Copy/move code to get max value from the top to inside/before API call
# • Store the max values in a separate .csv file for easier parsing and call that file when trying to find max value

# create another .csv with a sum for each day of songs played that can be an easy reference. That will be added to each time the API is called and there is new data
# Make another csv file to log the max dates from every api call so that there is less to cull through when getting max date

def string_to_dict(dict_string):
    # Convert to proper json format
    dict_string = dict_string.replace("\'", "\"")
    return json.loads(dict_string)

def stringKey_to_int(df, keyname):
    pass
    #print(max(date_dump, key=attrgetter('uts')))
    #d = {k:int(v) for k,v in df.items()


# Load up the most recent date added to the .csv db
if path.exists('lastfm_db.csv') == True:     # check to see if spreadsheet exists
    print('File exists! Wonderful! You are a pro!')
    print('loading')

    time.sleep(1)
    db = pd.read_csv('lastfm_db.csv', delimiter = ',') #, usecols=['date']) # read the csv
    time.sleep(1)
    print('loaded')

    #dates = db['date'] # gets just the data column into a series
    date_dump = db['date'].dropna() # gets rid of NA values (for currently listening to tracks)
    date_dump = date_dump.apply(string_to_dict) # replaces single quotes and json.loads into dictionaries
    date_dump.to_csv("data_dump.csv", header=True)

    lst = []
    for i in range(1, date_dump.count()):
        lst.append(int(date_dump.iloc[i]['uts'])) # remember that every 201 row is missing because of dropna()

    pullDate = (max(lst))
    del lst # clear this from memory
    # SAVE THIS: print(date_dump.iloc[1]['uts']) # this might be a much simpler solution if the .csv is ordered by timestamp


elif path.exists('lastfm_db.csv') == False: # throw an error if the file doesn't exist, carry on to except
    print("File does not exist!")
    print("First time running! Welcome to the SCROBBLE :)")
    time.sleep(3)
    f = open("lastfm_db.csv", "w")
    header = pd.DataFrame(columns = ["album", "artist", "date", "image", "loved", "mbid", "name", "streamable", "url"]) # don't add a column for currently listening
    header.to_csv(f, header=True)
    pullDate = "1572584400"    # set max date as a date before when I started scrobbling
    f.close()

    g = open("maxDateRepo.csv", "w") # creates a file to store all of the max dates so we don't have to cull through every date every time
    header = pd.DataFrame(columns = ["MaxDate"]) # don't add a column for currently listening
    header.to_csv(g, header=True)
    g.close()
    print("BACK IN BUSINESS")


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


date_dump2 = alltracks['date'].dropna() # gets rid of NA values (for currently listening to tracks)
date_dump2 = date_dump2.apply(string_to_dict) # replaces single quotes and json.loads into dictionaries

lst2 = []
for i in range(1, date_dump2.count()):
    lst.append(int(date_dump2.iloc[i]['uts'])) # remember that every 201 row is missing because of dropna()

maxDate = (max(lst2))
g = open("maxDateRepo.csv", "w")
g.write(maxDate)
g.close() # close the file


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
