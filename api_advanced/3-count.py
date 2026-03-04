#!/usr/bin/python3
"""
Module that queries the Reddit API recursively, parses titles
of hot articles, and prints a sorted count of given keywords.
"""
import requests


def count_words(subreddit, word_list, instances={}, after="", count=0):
    """
    Recursively queries the Reddit API and counts keyword occurrences.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        'User-Agent': 'linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)'
    }
    params = {
        'after': after,
        'count': count,
        'limit': 100
    }

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    try:
        if response.status_code != 200:
            return None

        data = response.json().get("data")
        after = data.get("after")
        count += data.get("dist")
        for child in data.get("children"):
            title = child.get("data").get("title").lower().split()
            for word in word_list:
                if word.lower() in title:
                    times = len([t for t in title if t == word.lower()])
                    if instances.get(word.lower()):
                        instances[word.lower()] += times
                    else:
                        instances[word.lower()] = times

        if after is None:
            if len(instances) == 0:
                return
            # Sort by count (descending), then alphabetically (ascending)
            sorted_subs = sorted(
                instances.items(), key=lambda kv: (-kv[1], kv[0]))
            for k, v in sorted_subs:
                print("{}: {}".format(k, v))
        else:
            return count_words(subreddit, word_list, instances, after, count)
    except Exception:
        return None
