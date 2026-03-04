#!/usr/bin/python3
"""
Query the Reddit API and return a list of titles for all hot articles for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively query the Reddit API and return a list of titles for all hot articles.
    """
    # Initialize hot_list on first call to avoid mutable default argument issue
    if hot_list is None:
        hot_list = []
    
    # Fixed URL (removed extra spaces)
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    headers = {
        'User-Agent': 'python:alx_api_advanced:v1.0.0 (by /u/your_username)'
    }

    params = {
        'limit': 100
    }

    # Now 'after' is properly defined as a parameter
    if after:
        params['after'] = after

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        
        # Check for invalid subreddit (status code not 200)
        if response.status_code != 200:
            return None
        
        data = response.json()
        posts = data.get('data', {}).get('children', [])

        # If no posts and hot_list is empty, return None
        if not posts:
            return None if not hot_list else hot_list
        
        # Add titles to hot_list
        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                hot_list.append(title)
        
        # Get the 'after' value for pagination
        after = data.get('data', {}).get('after')

        # Recursive call if there are more posts
        if after:
            return recurse(subreddit, hot_list, after)
        else:
            return hot_list
        
    except Exception:
        return None


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")