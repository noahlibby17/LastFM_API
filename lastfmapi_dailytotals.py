#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import time
import pandas as pd
import math
import csv
import os.path
from os import path
import json

# Have a row for every day since I started scrobbling
# Grab data from db csv for each day. Must first convert time from UTC to Central
#

# For now: just grab data from current day. Grab data from db csv for today

secondsPerHour = 3600 # number of seconds in
hoursOffUTC = 6 # set to hours off UTC
secondsOffUTC = secondsPerHour * hoursOffUTC # negative = west, positive = east

def string_to_dict(dict_string):
    # Convert to proper json format
    dict_string = dict_string.replace("\'", "\"")
    return json.loads(dict_string)

def convertTimeZone(unix_date):
    return unix_date + secondsOffUTC


#86400 # day in seconds

def readDateData(filename, targetDate):
        # count the number of rows with that date
        # add this number to another spreadsheet called lastfmapi_today.csv which has a row for day and a row for total.
        # for now, just update the value in the row  with that date. Can append it at another point

        # convert targetDate to unix in a new variable
        unixTargetDate = datetime.timestamp(targetDate)

        # read the file using only select date and the date right before and the date right after to account for timezone differences
        db = pd.read_csv(filename, delimiter = ',', usecols = ['unixdate'])
        # convert dates to timezone I want
        db['timezoneDate'] = db['unixdate'].apply(convertTimeZone)
        # trim down to only two days surrounding target date
        db[db['timezoneDate'] > (unixTargetDate - 86400)]
        db[db['timezoneDate'] < (unixTargetDate + 86400)]
        #db['dayName'] = db['timezoneDate']
        print(db)
        print('loaded')


        #db.to_csv("newdump.csv", header=False)




if path.exists('lastfm_db.csv') == True:     # check to see if spreadsheet exists

    now = datetime.now()
    print(now)
    timestamp = datetime.timestamp(now) # convert to unix time
    readDateData('lastfm_db.csv', now)



elif path.exists('lastfm_db.csv') == False:
    pass










#
