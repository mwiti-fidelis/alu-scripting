#!/usr/bin/python3
"""
Query the Reddit API recursively, parse titles, and count keywords.
"""

import requests
import re


def count_words(subreddit, word_list, hot_list=[], after=None):
    # Reddit API endpoint
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    
    headers = {
        'User-Agent': 'python:alx_api_advanced:v1.0.0 (by /u/your_username)'
    }

    params = {
        'limit': 100
    }
    
    if after:
        params['after'] = after
    
    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        
        # Check if the request was successful
        if response.status_code != 200:
            return None

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        
        if not posts:
            return None if not hot_list else hot_list
        
        # Add titles to hot_list
        for post in posts:
            title = post.get('data', {}).get('title', '')
            hot_list.append(title)
        
        # Get the 'after' value for pagination
        after = data.get('data', {}).get('after')
        
        if after:
            return count_words(subreddit, word_list, hot_list, after)
        else:
            return process_titles(hot_list, word_list)
    
    except Exception:
        return None


def process_titles(titles, word_list):
    word_list = [word.lower() for word in word_list]
    word_counts = {}
    for title in titles:
        title_lower = title.lower()
        
        for word in word_list:
            # Use regex to find whole word matches
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, title_lower, re.IGNORECASE)
            
            if word in word_counts:
                word_counts[word] += len(matches)
            else:
                word_counts[word] = len(matches)
    
    return word_counts


def print_results(word_counts):
    if not word_counts:
        return

    filtered_counts = {k: v for k, v in word_counts.items() if v > 0}
    
    if not filtered_counts:
        return
    
    # Sort by count (descending), then alphabetically (ascending)
    sorted_counts = sorted(filtered_counts.items(), key=lambda x: (-x[1], x[0]))

    for word, count in sorted_counts:
        print(f"{word}: {count}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = [x for x in sys.argv[2].split()]
        result = count_words(subreddit, word_list)
        if result:
            print_results(result)