#!/usr/bin/python3
"""
Query the Reddit API and return the number of subscribers
for a given subreddit.
"""
import requests


def number_of_subscribers(subreddit):
    """Return the number of subscribers for a given subreddit."""
    if not subreddit or not isinstance(subreddit, str):
        return 0

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "CustomUserAgent/1.0"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("subscribers", 0)
        else:
            # Invalid subreddit or redirect
            return 0
    except Exception:
        return 0