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

# 1. Watch for any updates to the maxDateRepo sheet (Watchdog or just a CRON job)
# 2. If changes are noticed, grab all new updates
# 3. Connect to the Google Sheets API
# 4. Add the new songs to the Google Sheet
# 5. Close the connection
