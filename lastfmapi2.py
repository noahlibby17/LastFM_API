import requests
import json
from datetime import datetime
import requests_cache
import time
from IPython.core.display import clear_output

# Get the number of tracks that a user has scrobbled today


# API Response Codes
#200: Everything went okay, and the result has been returned (if any).
#301: The server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint name is changed.
#400: The server thinks you made a bad request. This can happen when you don’t send along the right data, among other things.
#401: The server thinks you’re not authenticated. Many APIs require login credentials, so this happens when you don’t send the right credentials to access an API.
#403: The resource you’re trying to access is forbidden: you don’t have the right permissions to see it.
#404: The resource you tried to access wasn’t found on the server.
#503: The server is not ready to handle the request.

#apikey = 6a76bb9ed119dd4394c3f3bb5c0dcbd3
#shared_secret = a571d9b0049be7880a5da881da7df6d7


requests_cache.install_cache()

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': 'noahwlibby'}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = '6a76bb9ed119dd4394c3f3bb5c0dcbd3'
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


#jprint(r.json())

# Get all of the pages of data
responses_list = []
page = 1
total_pages = 99999

while page <= total_pages:
    payload = {
        'method': 'user.getrecenttracks',
        'user': 'noahwlibby',
        'limit': 500,
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
    page = int(response.json())






















    #
