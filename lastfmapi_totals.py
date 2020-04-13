#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
import time
import pandas as pd
import math
import csv
import os.path
from os import path
import json
import lastfmapi_dailytotals

# Take list as input, outputs total number of songs for each day

secondsPerHour = 3600 # number of seconds in
hoursOffUTC = 6 # set to hours off UTC
secondsOffUTC = secondsPerHour * hoursOffUTC # negative = west, positive = east

### If backfilling, follow this logic:

# 1. Create the file ('lastfm_dailytotals.csv')
# 2. Take in a list of all previous dates
# 3. Loop over all the dates and run the function

### define main function
if __name__ == "__main__":

    if path.exists('lastfm_db.csv') == True:     # check to see if spreadsheet exists

        yesterday = datetime.today() - timedelta(days=1)
        total = lastfmapi_dailytotals.readDateData('lastfm_db.csv', yesterday, secondsOffUTC)
        if path.exists('lastfm_dailytotals.csv'):
            g = open('lastfm_dailytotals.csv', 'a+')
            csv_writer = csv.writer(g)
            dt = datetime(yesterday.year, yesterday.month, yesterday.day)
            csv_writer.writerow([dt, total]) # Add contents of list as last row in the csv file
            g.close() # close the file
        elif path.exists('lastfm_dailytotals.csv') == False:
            pass


    elif path.exists('lastfm_db.csv') == False:
        pass
