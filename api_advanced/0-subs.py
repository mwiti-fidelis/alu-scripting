#!/usr/bin/python3
"""
Query the Reddit API and return the number of subscribers for a given subreddit.
"""

import requests
import sys


def number_of_subscribers(subreddit):
    """Return the number of subscribers for a given subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    
    headers = {
        'User-Agent': 'python:alx_api_advanced:v1.0.0 (by /u/your_username)'
    }
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('subscribers', 0)
        else:
            return 0
            
    except Exception:
        return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        print("{:d}".format(number_of_subscribers(sys.argv[1])))