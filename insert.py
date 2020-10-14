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
<<<<<<< HEAD
import sqlite3
=======
>>>>>>> 1f10fa92d38b90dc29ae062df0c0c48978b58841

# Mimics the functionality of the Last.FM website by saying how many songs were listened to today.
# All dates are in UTC, so if I want to get it in my timezone, I'll need to make a new column with converted times

##### IMPORTANT ######
# PULL MAX DATE + 1 SO THAT WE DON'T PULL THE SAME SONG THAT WE PULLED LAST TIME
##### IMPORTANT #####

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

<<<<<<< HEAD

=======
>>>>>>> 1f10fa92d38b90dc29ae062df0c0c48978b58841
def readDataFindMax(filename):
        db = pd.read_csv(filename, delimiter = ',') #, usecols=['date']) # read the csv
        print('loaded')

        date_dump = db['date'].dropna() # gets rid of NA values (for currently listening to tracks)
        date_dump = date_dump.apply(string_to_dict) # replaces single quotes and json.loads into dictionaries
        date_dump.to_csv("dewey_data_dump.csv", header=True)

        lst = []
        for i in range(0, date_dump.count()):
            lst.append(int(date_dump.iloc[i]['uts']))

        pullDate = int((max(lst)))
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
<<<<<<< HEAD
            'from': 1598918400 # sept 1 2020 #1546300800 # january 1st 2019
=======
            'from': pullDate
>>>>>>> 1f10fa92d38b90dc29ae062df0c0c48978b58841
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
        #if not getattr(response, 'from_cache', False):
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

<<<<<<< HEAD

=======
>>>>>>> 1f10fa92d38b90dc29ae062df0c0c48978b58841
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

<<<<<<< HEAD

def create_user_table(conn,user): # creates a table for the user if one does not exist
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param lastfm_user: a CREATE TABLE statement
    :return:
    """
    sql_create_user_table = f""" CREATE TABLE IF NOT EXISTS {user}_music (
                                              album text
                                            , artist text
                                            , date text
                                            , image text
                                            , loved integer
                                            , mbid text
                                            , name text
                                            , streamable integer
                                            , url text
                                            , unixdate integer
                                        ); """
    try:
        c = conn.cursor()
        c.execute(sql_create_user_table)
    except Error as e:
        print(e)


def add_song(conn, user, entry):
    """
    Add new songs
    :param conn:
    :param last_fm user:
    :param song entry:
    :return:
    """

    sql = f''' INSERT INTO {user}_music(album,artist,date,image,loved,mbid,name,streamable,url,unixdate)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql,entry)
=======
def add_song(conn, song):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO songs(album,artist,date,image,loved,mbid,name,streamable,url,unixdate)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
>>>>>>> 1f10fa92d38b90dc29ae062df0c0c48978b58841
    conn.commit()

    return cur.lastrowid

<<<<<<< HEAD

def main(): # add param for username
    #########################
    ### Grab all the data ###
    #########################

    # call get_tracks, bring the list of lists into a list of dataframes and then to a single df, then reverse the order to get most recent at bottom
    responses = get_tracks()
    frames = [pd.DataFrame(r.json()['recenttracks']['track']) for r in responses]
    alltracks = pd.concat(frames, sort=True)
    alltracks = alltracks.iloc[::-1] # flip the df so most recent songs are at the bottom. Makes appending easier
    alltracks['unixdate'] = ''

    alltracks.info() # prints info about the df

    # remove rows for tracks that are currently being played from dataset; they will be added in the next api call once the song is over
    if playing_now_check(alltracks) == True:
        print('Currently listening!')
        alltracks = alltracks[alltracks['@attr'].isna()] # gets rid of rows that have currently playing track
        alltracks = alltracks.drop(['@attr'], axis=1) # drops @attr column
        alltracks.info()
        print('DROPPED')

        ### Add column with just unix time dates
        for i in range(0, alltracks['date'].count()):
            unix = alltracks['date'].iloc[i]['uts']
            alltracks['unixdate'].iloc[i] = unix

        ######################
        ### Database calls ###
        ######################

        #Create connection to database file
        database = r"/Users/noahlibby/Documents/code/LastFM_API/lastfm.sqlite"
        conn = create_connection(database)
        # create tables
        if conn is not None:
            # create projects table
            create_user_table(conn, 'noah')
            print('table exists!')
        else:
            print("Error! Cannot create the database connection.")
        alltracks.to_sql(name='noah_music', con=conn, if_exists='replace')
        print('ADDED TO DB')
        conn.close()

    elif playing_now_check(alltracks) == False:
        print('Not currently listening. Makes the code easier...')
        ### Add column with just unix time dates
        for i in range(0, alltracks['date'].count()):
            unix = alltracks['date'].iloc[i]['uts']
            alltracks['unixdate'].iloc[i] = unix

        time.sleep(1)

        ######################
        ### Database calls ###
        ######################

        #Create connection to database file
        database = r"/Users/noahlibby/Documents/code/LastFM_API/lastfm.sqlite"
        conn = create_connection(database)
        # create tables
        if conn is not None:
            # create projects table
            create_user_table(conn, 'noah')
            print('table exists!')
        else:
            print("Error! Cannot create the database connection.")
        alltracks.to_sql(name='noah_music', con=conn, if_exists='replace')
        print('ADDED TO DB')
        conn.close()

#######################
#### CALL MAIN FUNC ###
#######################
if __name__ == '__main__':
    # add command line param or call function to get lastfm username
    main()
=======
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
    header = pd.DataFrame(columns = ["album", "artist", "date", "image", "loved", "mbid", "name", "streamable", "url", "unixdate"]) # don't add a column for currently listening
    header.to_csv(f, header=True)
    pullDate = 1    # set max date as 1970
    f.close()

    g = open("maxDateRepo.csv", "w") # creates a file to store all of the max dates so we don't have to cull through every date every time
    header = pd.DataFrame(columns = ['MaxDate']) # don't add a column for currently listening
    header.to_csv(g, header=True)
    g.close()
    print("BACK IN BUSINESS")

# call get tracks, bring the list of lists into a list of dataframes and then to a single df, then reverse the order
responses = get_tracks()
frames = [pd.DataFrame(r.json()['recenttracks']['track']) for r in responses]
alltracks = pd.concat(frames, sort=True)
alltracks = alltracks.iloc[::-1] # flip the df so most recent songs are at the bottom. Makes appending easier
alltracks['unixdate'] = ''

alltracks.info() # prints info about the df

#Create connection to database file
database = r"/Users/noahlibby/Documents/code/LastFM_API/noah_lastfm.db"
conn = create_connection(database)

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

    ### Add column with just unix time dates
    for i in range(0, alltracks['date'].count()):
        unix = alltracks['date'].iloc[i]['uts']
        alltracks['unixdate'].iloc[i] = unix

    ### APPEND ALLTRACKS TO THE .CSV DB FILE
    alltracks.to_csv('lastfm_db.csv', mode="a", header=False)

    ### SAVE THE MAX DATE FOR REF
    date_dump2 = alltracks.iloc[1:,:]['date'].dropna() # gets rid of NA values (for currently listening to tracks)
    lst2 = []
    for i in range(0, date_dump2.count()):
        lst2.append(int(date_dump2.iloc[i]['uts'])) # remember that every 201 row is missing because of dropna()

    # Get max date from this pull and add it to maxDateRepo.csv file for easy reference
    maxDate = (max(lst2))+1 # plus 1 so it doesn't pull the same song
    g = open('maxDateRepo.csv', 'a+')
    csv_writer = csv.writer(g)
    csv_writer.writerow([datetime.fromtimestamp(pullDate),maxDate]) # Add contents of list as last row in the csv file
    g.close() # close the file

    # Add data to database
    with conn:
        for i in range(0, alltracks['date'].count()):
                entry = alltracks[i,:]
                song_entry = add_song(conn,entry)


elif playing_now_check(alltracks) == False:
    print('Not currently listening. Makes the code easier...')
    ### Add column with just unix time dates
    for i in range(0, alltracks['date'].count()):
        unix = alltracks['date'].iloc[i]['uts']
        alltracks['unixdate'].iloc[i] = unix

    time.sleep(1)
    alltracks.to_csv('lastfm_db.csv', mode="a", header=False)

    ### SAVE THE MAX DATE FOR REF
    date_dump2 = alltracks.iloc[1:,:]['date'].dropna() # gets rid of NA values (for currently listening to tracks)
    lst2 = []
    for i in range(0, date_dump2.count()):
        lst2.append(int(date_dump2.iloc[i]['uts'])) # remember that every 201 row is missing because of dropna()

    # Get max date from this pull and add it to maxDateRepo.csv file for easy reference
    maxDate = (max(lst2))+1 # plus 1 so it doesn't pull the same song
    g = open('maxDateRepo.csv', 'a+')
    csv_writer = csv.writer(g)
    csv_writer.writerow([datetime.fromtimestamp(pullDate),maxDate]) # Add contents of list as last row in the csv file
    g.close() # close the file

    # Add data to database
    with conn:
        for i in range(0, alltracks['date'].count()):
                entry = alltracks[i,:]
                song_entry = add_song(conn,entry)
>>>>>>> 1f10fa92d38b90dc29ae062df0c0c48978b58841
