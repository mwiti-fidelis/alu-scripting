#!/usr/bin/python3
"""
Contains the top_ten function
"""
import requests


def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    listed for a given subreddit.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        'User-Agent': 'linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)'
    }
    params = {
        'limit': 10
    }

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
        if response.status_code == 200:
            data = response.json().get('data')
            children = data.get('children')
            for post in children:
                print(post.get('data').get('title'))
        else:
            print("None")
    except Exception:
        print("None")