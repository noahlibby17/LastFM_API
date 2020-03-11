#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import config

# Grab songs that are currently playing to send out to IFTTT

# API Response Codes
#200: Everything went okay, and the result has been returned (if any).
#301: The server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint name is changed.
#400: The server thinks you made a bad request. This can happen when you don’t send along the right data, among other things.
#401: The server thinks you’re not authenticated. Many APIs require login credentials, so this happens when you don’t send the right credentials to access an API.
#403: The resource you’re trying to access is forbidden: you don’t have the right permissions to see it.
#404: The resource you tried to access wasn’t found on the server.
#503: The server is not ready to handle the request.

API_KEY = config.api_key
API_SECRET = config.api_secret

def string_to_dict(dict_string):
    # Convert to proper json format
    dict_string = dict_string.replace("\'", "\"")
    return json.loads(dict_string)

def readDataFindMax(filename):
        db = pd.read_csv(filename, delimiter = ',') #, usecols=['date']) # read the csv
        print('loaded')

        date_dump = db['date'].dropna() # gets rid of NA values (for currently listening to tracks)
        date_dump = date_dump.apply(string_to_dict) # replaces single quotes and json.loads into dictionaries
        date_dump.to_csv("data_dump.csv", header=True)

        lst = []
        for i in range(1, date_dump.count()):
            lst.append(int(date_dump.iloc[i]['uts']))

        pullDate = (max(lst))
        del lst
        return pullDate
        # SAVE THIS: print(date_dump.iloc[1]['uts']) # this might be a much simpler solution if the .csv is ordered by timestamp

# Load up the most recent date added to the .csv db
if path.exists('lastfm_db.csv') == True:     # check to see if spreadsheet exists
    print('File exists! Wonderful! You are a pro!')
    print('loading')

    #if path.exists('maxDateRepo.csv') == True:
        #dates = db['date'] # gets just the data column into a series
    print('We have a max date file! Reading from max date file...')
    db = pd.read_csv('maxDateRepo.csv', delimiter = ',') #, usecols=['date']) # read the csv
    pullDate = db[['MaxDate']].idxmax()
    print(pullDate)

    """
    # Just to catch some extra errors for now... will probably deprecate this catch
    elif path.exists('maxDateRepo.csv') == False:
        #dates = db['date'] # gets just the data column into a series
        print('We DO NOT have a max date file! Reading from overall database...')
        readDataFindMax('lastfm_db.csv')
    """

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

# bring the list of lists into a list of dataframes and then to a single df
responses = get_tracks()
frames = [pd.DataFrame(r.json()['recenttracks']['track']) for r in responses]
alltracks = pd.concat(frames, sort=True)

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

def playing_now_check(df):
    pos = 0
    try:
        for i in df['@attr']:
            if isinstance(i,dict): # there should only ever be one dictionary, with value 'true' - everything else is NaN
                return True
                break
            else:
                pos += 1
    except:
        return False

def totalsongstoday(df):
    today = date.today()

print(playing_now(alltracks))
