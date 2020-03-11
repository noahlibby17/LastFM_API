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
import csv
import os.path
from os import path
from operator import attrgetter
import config

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

# ONLY GRAB DATA THAT WE HAVE NOT GRABBED YET
#requests_cache.install_cache('lastfm_cache')

## TO DO:
# • Move the storage from .csv to sqlite database
# • Copy/move code to get max value from the top to inside/before API call
# • Store the max values in a separate .csv file for easier parsing and call that file when trying to find max value

# create another .csv with a sum for each day of songs played that can be an easy reference. That will be added to each time the API is called and there is new data
# Make another csv file to log the max dates from every api call so that there is less to cull through when getting max date

API_KEY = config.api_key
API_SECRET = config.api_secret

#################################
##### FUNCTION DEFINITIONS ######
#################################

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

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'noahwlibby'}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
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


##########################
##### FUNCTION CALLS #####
##########################

# Load up the most recent date added to the .csv db
if path.exists('lastfm_db.csv') == True:     # check to see if spreadsheet exists
    print('File exists! Wonderful! You are a pro!')
    print('loading')

    #if path.exists('maxDateRepo.csv') == True:
        #dates = db['date'] # gets just the data column into a series
    print('We have a max date file! Reading from max date file...')
    db = pd.read_csv('maxDateRepo.csv', delimiter = ',') #, usecols=['date']) # read the csv
    pullDate = db[['MaxDate']].max()
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
    pullDate = "1"    # set max date as 1970
    f.close()

    g = open("maxDateRepo.csv", "w") # creates a file to store all of the max dates so we don't have to cull through every date every time
    header = pd.DataFrame(columns = ['MaxDate']) # don't add a column for currently listening
    header.to_csv(g, header=True)
    g.close()
    print("BACK IN BUSINESS")

# bring the list of lists into a list of dataframes and then to a single df
responses = get_tracks()
frames = [pd.DataFrame(r.json()['recenttracks']['track']) for r in responses]
alltracks = pd.concat(frames, sort=True)
alltracks.info() # prints info about the df

# remove rows for tracks that are currently being played from dataset; they will be added in the next api call once the song is over
if playing_now_check(alltracks) == True:
    print('Currently listening!')
    #alltracks[alltracks['@attr'] != '{\'nowplaying\': \'true\'}']
    # Get names of indexes for which column Age has value 30
    #indexNames = alltracks.loc[alltracks['@attr'].notnull()].index
    #print(alltracks.loc[alltracks['@attr']])

    alltracks = alltracks[alltracks['@attr'].isna()] # gets rid of rows that have currently playing track
    alltracks = alltracks.drop(['@attr'], axis=1) # drops @attr column
    alltracks.info()

    print('DROPPED')

    ### APPEND ALLTRACKS TO THE .CSV DB FILE
    alltracks.to_csv('lastfm_db_full.csv', mode="a", header=False)
    alltracks.iloc[2:,:].to_csv('lastfm_db.csv', mode="a", header=False)
    alltracks.iloc[2:,:].to_csv('lastfm_db_iloc.csv', mode="a", header=False)


    ### SAVE THE MAX DATE FOR REF
    date_dump2 = alltracks.iloc[2:,:]['date'].dropna() # gets rid of NA values (for currently listening to tracks)
    lst2 = []
    for i in range(1, date_dump2.count()):
        lst2.append(int(date_dump2.iloc[i]['uts'])) # remember that every 201 row is missing because of dropna()

    # Get max date from this pull and add it to maxDateRepo.csv file for easy reference
    maxDate = (max(lst2))
    g = open('maxDateRepo.csv', 'a+')
    csv_writer = csv.writer(g)
    csv_writer.writerow([datetime.now(),maxDate]) # Add contents of list as last row in the csv file
    g.close() # close the file


###### LEFT OFF: Trying to get maxdate to pull properly from maxdaterepo, trying to delete rows with currently listenign tracks and writing only columns that I want



elif playing_now_check == False:
    print('Not currently listening. Makes the code easier...')
    alltracks.to_csv('lastfm_db.csv', mode="a", header=False)
    ### SAVE THE MAX DATE FOR REF
    date_dump2 = alltracks['date'].iloc[1:,:].dropna() # gets rid of NA values (for currently listening to tracks)
    lst2 = []
    for i in range(1, date_dump2.count()):
        lst2.append(int(date_dump2.iloc[i]['uts'])) # remember that every 201 row is missing because of dropna()

    # Get max date from this pull and add it to maxDateRepo.csv file for easy reference
    maxDate = (max(lst2))
    g = open('maxDateRepo.csv', 'a+')
    csv_writer = csv.writer(g)
    csv_writer.writerow([datetime.now(),maxDate]) # Add contents of list as last row in the csv file
    g.close() # close the file



def totalsongstoday(df):
    today = date.today()


"""
# get track counts
track_count = [len(r.json()['recenttracks']['track']) for r in responses]
pd.Series(track_count).value_counts()
print(track_count)
"""


#if __name__ == "__main__":
# user = input("Username: ")
