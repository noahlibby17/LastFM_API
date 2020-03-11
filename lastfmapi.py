import requests
import json
from datetime import datetime
import requests_cache
import time
from IPython.core.display import clear_output
import pandas as pd
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

requests_cache.install_cache()

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'noahwlibby'}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

r = lastfm_get({
    'method': 'user.getrecenttracks',
    'user': 'noahwlibby'
})
#print(r.status_code)



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

        # if it's not a cached result, sleep
        if not getattr(response, 'from_cache', False):
            time.sleep(0.25)

        # increment the page number
        page += 1
    return responses

"""
r0 = responses[0]
r0_json = r0.json()
r0_recenttracks = r0_json['recenttracks']['track']
r0_df = pd.DataFrame(r0_recenttracks)
print(r0_df.head())
"""
responses = get_tracks()
# bring the list of lists into a list of dataframes and then to a single df
frames = [pd.DataFrame(r.json()['recenttracks']['track']) for r in responses]
alltracks = pd.concat(frames, sort=True)
alltracks.info()

def playing_now(responses):
    for r in responses: # can i sort this by most recently added date?
        if pd.DataFrame(r.json()['recenttracks']['track']['@attr']['nowplaying']) == True:
            return pd.DataFrame(r.json()['recenttracks']['track'])
            break

playing = playing_now(responses)
print(playing)

"""
# get track counts
track_count = [len(r.json()['recenttracks']['track']) for r in responses]
pd.Series(track_count).value_counts()
print(track_count)
"""



#if __name__ == "__main__":
# user = input("Username: ")















    #
