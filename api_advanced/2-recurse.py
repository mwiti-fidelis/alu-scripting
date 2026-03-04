#!/usr/bin/python3
"""
Contains the recurse function
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Query the Reddit API and return a list containing the titles
    of all hot articles for a given subreddit.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        'User-Agent': 'linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)'
    }
    params = {
        'after': after,
        'limit': 100
    }

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        return None

    data = response.json().get('data')
    after = data.get('after')
    children = data.get('children')

    for post in children:
        hot_list.append(post.get('data').get('title'))

    if after is not None:
        return recurse(subreddit, hot_list, after)

    return hot_list
