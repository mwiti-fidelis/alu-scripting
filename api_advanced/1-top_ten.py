#!/usr/bin/python3
"""
Query the Reddit API and print the titles of the first 10 hot posts for a given subreddit.
"""

import sys
import requests


def top_ten(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    headers = {
        'User-Agent': 'python:alx_api_advanced:v1.0.0 (by /u/your_username)'
    }

    params = {
        'limit': 10
    }

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)

        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])

            for post in posts:
                title = post.get('data', {}).get('title', '')
                if title:
                    print(title)
        else:
            print("None")

    except Exception:
        print("None")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])