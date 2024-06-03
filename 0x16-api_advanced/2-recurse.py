#!/usr/bin/python3
"""
Queries the Reddit API and returns a list containing the
titles of all hot articles for a given subreddit.
"""
import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursive function that queries the Reddit API and returns a list
    containing the titles of all hot articles for a given subreddit.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'custom'}
    params = {'limit': 100, 'after': after}
    response = requests.get(
            url, headers=headers, params=params, allow_redirects=False
            )

    if response.status_code != 200:
        return None
    data = response.json().get("data")
    after = data.get("after")
    children = data.get("children")
    for child in children:
        hot_list.append(child.get("data").get("title"))
    if after is not None:
        return recurse(subreddit, hot_list, after)
    return hot_list

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
