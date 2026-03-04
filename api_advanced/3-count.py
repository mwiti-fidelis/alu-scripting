#!/usr/bin/python3
"""
Query the Reddit API recursively, parse titles, and count keywords.
"""

import requests
import re


def count_words(subreddit, word_list, hot_list=None, after=None):
    """Recursively fetch hot posts from Reddit API."""
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
            if not hot_list:
                return None
            return process_titles_recursive(hot_list, word_list, 0, {})
        
        # Add titles to hot_list
        for post in posts:
            title = post.get('data', {}).get('title', '')
            hot_list.append(title)
        
        # Get the 'after' value for pagination
        after = data.get('data', {}).get('after')
        
        if after:
            return count_words(subreddit, word_list, hot_list, after)
        else:
            return process_titles_recursive(hot_list, word_list, 0, {})
    
    except Exception:
        return None


def process_titles_recursive(titles, word_list, title_index, word_counts):
    """Recursively process titles and count words."""
    # Base case: all titles processed
    if title_index >= len(titles):
        return word_counts
    
    # Process current title
    current_title = titles[title_index]
    word_counts = count_words_in_title_recursive(current_title, word_list, 0, word_counts)
    
    # Recursive call for next title
    return process_titles_recursive(titles, word_list, title_index + 1, word_counts)


def count_words_in_title_recursive(title, word_list, word_index, word_counts):
    """Recursively count words from word_list in a title."""
    # Base case: all words processed
    if word_index >= len(word_list):
        return word_counts
    
    # Get current word (lowercase for case-insensitive matching)
    current_word = word_list[word_index].lower()
    
    # Count occurrences using regex for whole word matching
    title_lower = title.lower()
    pattern = r'\b' + re.escape(current_word) + r'\b'
    matches = re.findall(pattern, title_lower)
    count = len(matches)
    
    # Update word_counts
    if current_word in word_counts:
        word_counts[current_word] += count
    else:
        word_counts[current_word] = count
    
    # Recursive call for next word
    return count_words_in_title_recursive(title, word_list, word_index + 1, word_counts)


def print_results(word_counts):
    """Print results sorted by count (desc) then alphabetically (asc)."""
    if not word_counts:
        return

    # Filter out words with 0 count
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