#!/usr/bin/python3

"""
Module: export_user_todos

This module fetches user and todo data from the JSONPlaceholder API,
processes the data, and exports it to a JSON file in a structured format.

Functions:
    fetch_data(url)
        Fetch data from the given URL and return the JSON response.

    main()
        The main function that orchestrates the fetching, processing,
        and exporting of data.

Execution:
    When run as a script, this module will fetch data from the
    JSONPlaceholder API for users and todos, process it to associate
    each user's todos with their username, and export the data to a JSON file.
"""

import json
import logging
import requests

# Define the API endpoints as constants
USERS_URL = "https://jsonplaceholder.typicode.com/users"
TODOS_URL = "https://jsonplaceholder.typicode.com/todos"
OUTPUT_FILE = 'todo_all_employees.json'

# Configure logging
logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_data(url):
    """
    Fetch data from the given URL and return the JSON response.

    Parameters:
        url (str): The URL to fetch data from.

    Returns:
        list or dict: The JSON response data parsed into a Python object.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from {url}: {e}")
        return None


def main():
    """
    The main function that orchestrates the fetching, processing,
    and exporting of data.

    Fetches data from the JSONPlaceholder API for users and todos,
    processes it to associate each user's todos with their username,
    and exports the data to a JSON file in the required format.
    """
    # Fetch data from the API endpoints
    logging.info("Fetching users data...")
    users = fetch_data(USERS_URL)
    
    logging.info("Fetching todos data...")
    todos = fetch_data(TODOS_URL)

    # Check if data fetching was successful
    if users is None or todos is None:
        logging.error("Data fetching failed. Exiting the script.")
        return

    # Create a dictionary to hold the data in the required format
    all_data = {}

    # Process the data
    logging.info("Processing data...")
    for user in users:
        user_id = user['id']
        username = user['username']
        all_data[user_id] = []

        # Find todos for this user
        user_todos = [todo for todo in todos if todo['userId'] == user_id]

        # Add each todo to the user's list in the required format
        for todo in user_todos:
            all_data[user_id].append({
                "username": username,
                "task": todo['title'],
                "completed": todo['completed']
            })

    # Write the data to a JSON file
    logging.info(f"Writing data to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, 'w') as json_file:
            json.dump(all_data, json_file, indent=4)
        logging.info("Data has been successfully exported.")
    except IOError as e:
        logging.error(f"Failed to write data to {OUTPUT_FILE}: {e}")


if __name__ == "__main__":
    main()
