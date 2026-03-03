#!/usr/bin/python3
"""
Query the Reddit API that return s list of titles for all hot articles for a given subreddit
"""


import requests
import sys

def recurse(subreddit, hot_list=[]):
    # Reddit API endpoint for hot posts
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    headers = {
        'User-Agent': 'python:alx_api_advanced:v1.0.0 (by /u/your_username)'
    }

    # Get up to 100 posts per request
    params = {
        'limit': 100  
    }

    # After parameter when paginating
    if after:
        params['after'] = after

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            return None
        
        data = response.json()
        # Acess the posts
        posts = data.get('data', {}).get('children', [])

        if not posts:
            return None if not hot_list else hot_list
        
        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                hot_list.append(title)
        # get the after value for pagination
        after = data.get('data', {}).get('after')

        if after:
            return recurse(subreddit, hot_list, after)
        else:
            return hot_list
        
    except Exception:
        return None


if __name__ == '__main__':
    recurse = __import__('2-recurse').recurse
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")