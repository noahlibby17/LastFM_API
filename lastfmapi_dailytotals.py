#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date

# Have a row for every day since I started scrobbling
# Grab data from db csv for each day. Must first convert time from UTC to Central
#

# For now: just grab data from current day. Grab data from db csv for today
#

secondsPerHour = 3600 # number of seconds in
hoursOffUTC = 6 # set to hours off UTC
secondsOffUTC = secondsPerHour * hoursOffUTC

if path.exists('lastfm_db.csv') == True:     # check to see if spreadsheet exists

    db = pd.read_csv('lastfm_db.csv', delimiter = ',') #, usecols=['date']) # read the csv
    today = datetime.today()


elif path.exists('lastfm_db.csv') == False: # throw an error if the file doesn't exist, carry on to except
    pass










#
