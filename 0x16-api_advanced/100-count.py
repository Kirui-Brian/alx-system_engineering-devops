#!/usr/bin/python3
"""
Queries the Reddit API,
parses the title of all hot articles,
and prints a sorted count of given keywords.
"""
import requests
from collections import Counter
import re

def count_words(subreddit, word_list, after=None, word_count=Counter()):
    """
    Recursive function that queries the Reddit API,
    parses the title of all hot articles,
    and prints a sorted count of given keywords.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'custom'}
    params = {'limit': 100, 'after': after}
    response = requests.get(
            url, headers=headers, params=params, allow_redirects=False
            )

    if response.status_code != 200:
        return
    data = response.json().get("data")
    after = data.get("after")
    children = data.get("children")
    for child in children:
        title = child.get("data").get("title").lower()
        words = re.split(r'\W', title)
        for word in words:
            if word in word_list:
                word_count[word] += 1
    if after is not None:
        return count_words(subreddit, word_list, after, word_count)
    else:
        word_list = [[
            word, word_count[word]
            ] for word in word_list if word_count[word] > 0]
        word_list.sort(key=lambda x: (-x[1], x[0]))
        for word in word_list:
            print("{}: {}".format(word[0], word[1]))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(
            sys.argv[0])
            )
    else:
        word_list = [x.lower() for x in sys.argv[2].split()]
        count_words(sys.argv[1], word_list)
