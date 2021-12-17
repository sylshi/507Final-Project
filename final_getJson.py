from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= 'hpEqwcgDgmqWBGugejF3GmU5tw72kiaEmBB3H1AbcJL7rt29kNKvjLg1vvXROQ3s8t8WanMr34GQGyQs1D4ynuCvgcpN-rsvjCpwNZD02Xl' \
         '_GhCrjgbOxCBlZeKyYXYx'


# API constants, you shouldn't have to change these.

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
REVIEWS_PATH = f'/v3/businesses/{id}/reviews'


# Search for the restaurants in Chicago(Default)
DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'chicago'
SEARCH_LIMIT = 50


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {'Authorization': 'Bearer %s' % api_key}

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, offset):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': offset
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_reviews(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: yelp will return 3 user reviews
    """
    #business_path = BUSINESS_PATH + business_id
    headers = {'Authorization': 'Bearer %s' % api_key}
    review_path = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
    req = requests.get(review_path, headers=headers)
    result = req.text
    reviews = json.loads(result)
    return reviews


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    result=[]
    for i in range(1,902,50):
        response = search(API_KEY, term, location,offset=i)

        business_detail = response.get('businesses')

        if not business_detail:
            print(u'No businesses for {0} in {1} found.'.format(term, location))
            return
        for j in range(0, len(business_detail)):
            business_id = business_detail[j]['id']
            reviews = get_reviews(API_KEY, business_id)
            a = reviews.get('reviews')
            dict = {}
            business_detail[j]["reviews"] = []
            for k in range(0,len(a)):
                dict["review_content"] = a[k]["text"]
                dict["individual_rating"] = a[k]["rating"]
                #didn't use copy at the first time, almost made a mistake to append a same review 3 times.
                temp = dict.copy()
                business_detail[j]["reviews"].append(temp)
                # print(business_detail)
        print(business_detail)
        result = result+business_detail
        with open('restaurants.json','w') as fp:
            json.dump(result,fp)

    # print(u'{0} businesses found, querying business info ' \
    #     'for the top result "{1}" ...'.format(
    #         len(businesses), business_id))
    # response = get_business(API_KEY, business_id)

    # print(u'Result for business "{0}" found:'.format(business_id))
    # pprint.pprint(response, indent=2)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()