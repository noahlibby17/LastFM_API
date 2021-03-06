import requests
import json
from datetime import datetime
import requests_cache
import time
from IPython.core.display import clear_output
import pandas as pd
import math
import csv
import config

# todo:
# throw all of the json data into a pandas dataframe so that I can see it better


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


#requests_cache.install_cache('lastfm_cache')


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'noahwlibby'}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

"""
r = lastfm_get({
    'method': 'user.getrecenttracks',
    'user': 'noahwlibby'
})
#print(r.status_code)
"""


def jprint(obj):
    # Create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# test
#jprint(r.json())


def get_tracks():
    page = 1
    total_pages = 99999
    responses =  []
    while page <= total_pages:
        payload = {
            'method': 'user.getrecenttracks',
            'user': 'noahwlibby',
            'extended': 1,
            'limit': 200,
            'page': page
        }

        # print some of the output so we can see the status
        print("Requesting page {}/{}".format(page, total_pages))
        # clear the output to make things neater
        clear_output(wait = True)

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
        # does this data already exist in the file? use date.max: if date(entry) > date.max(csv file) ; utcadjust = tzinfo.utcoffset(date)
        # if no, if the date is greater than the current max date, add it to responses
        # at the end:
        # convert responses to a pandas dateframe
        # read the csv file into a variable
        # and append the responses to the csv file
        # save the file
        # close the file - outside of while loop

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



a = playing_now(alltracks)
print(a)


print(alltracks.iloc[1,2]['uts'])
#{'uts': '1582926138', '#text': '28 Feb 2020, 21:42'}
#alltracks.to_csv(r'testcsv.csv')
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
