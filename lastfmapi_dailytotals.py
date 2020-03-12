#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import time
import pandas as pd
import math
import csv
import os.path
from os import path

# Have a row for every day since I started scrobbling
# Grab data from db csv for each day. Must first convert time from UTC to Central
#

# For now: just grab data from current day. Grab data from db csv for today

def string_to_dict(dict_string):
    # Convert to proper json format
    dict_string = dict_string.replace("\'", "\"")
    return json.loads(dict_string)

def readDateData(filename, date):

        # read the file using only select date and the date right before and the date right after to account for timezone differences
        db = pd.read_csv(filename, delimiter = ',')

        # convert dates timezone I want
        # count the number of rows with that date
        # add this number to another spreadsheet called lastfmapi_today.csv which has a row for day and a row for total.
        # for now, just update the value in the row  with that date. Can append it at another point


        print('loaded')

        date_dump = db['date'].dropna() # gets rid of NA values (for currently listening to tracks)
        date_dump = date_dump.apply(string_to_dict) # replaces single quotes and json.loads into dictionaries
        date_dump.to_csv("data_dump.csv", header=True)

        lst = []
        for i in range(1, date_dump.count()):
            lst.append(int(date_dump.iloc[i]['uts']))

        pullDate = int((max(lst)))
        del lst
        return pullDate


secondsPerHour = 3600 # number of seconds in
hoursOffUTC = 6 # set to hours off UTC
secondsOffUTC = secondsPerHour * hoursOffUTC # negative = west, positive = east

if path.exists('lastfm_db.csv') == True:     # check to see if spreadsheet exists

    db = pd.read_csv('lastfm_db.csv', delimiter = ',')
    now = datetime.now()
    print(now)
    timestamp = datetime.timestamp(now) # convert to unix time




elif path.exists('lastfm_db.csv') == False:
    pass










#
