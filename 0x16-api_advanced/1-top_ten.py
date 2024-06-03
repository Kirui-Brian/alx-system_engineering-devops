#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first
10 hot posts listed for a given subreddit.
"""
import requests

def top_ten(subreddit):
    """
    Function that queries the Reddit API and prints the titles of
    the first 10 hot posts listed for a given subreddit.
    """
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {'User-Agent': 'custom'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        print(None)
        return
    data = response.json().get("data").get("children")
    for post in data:
        print(post.get("data").get("title"))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
