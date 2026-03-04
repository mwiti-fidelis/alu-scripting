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
    # Construct URL and use .format() for Python 3.4.3 compatibility
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    # Custom User-Agent to avoid 'Too Many Requests' errors
    headers = {
        'User-Agent': 'linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)'
    }

    # Set limit to 10 as per requirements
    params = {
        'limit': 10
    }

    try:
        # allow_redirects=False is mandatory to catch invalid subreddits
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)

        # Only a 200 status code is a valid subreddit response
        if response.status_code == 200:
            data = response.json().get('data', {})
            children = data.get('children', [])
            for post in children:
                print(post.get('data', {}).get('title'))
        else:
            print("None")
    except Exception:
        print("None")
