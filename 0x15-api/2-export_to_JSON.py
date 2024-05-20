#!/usr/bin/python3
"""
Module: todo_exporter.py

This module retrieves data from a REST API and exports the TODO list progress
for a given employee ID to a JSON file.

Usage: python3 todo_exporter.py <employee_id>
"""

import json
import requests
import sys

def fetch_user_data(employee_id):
    """
    Fetch user information from the REST API.

    Parameters:
        employee_id (int): The ID of the employee.

    Returns:
        dict: The user data.
    """
    user_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print("User not found")
        sys.exit(1)
    return user_response.json()

def fetch_todo_list(employee_id):
    """
    Fetch the TODO list for the given employee from the REST API.

    Parameters:
        employee_id (int): The ID of the employee.

    Returns:
        list: The TODO list data.
    """
    todos_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print("Error fetching TODO list")
        sys.exit(1)
    return todos_response.json()

if __name__ == "__main__":
    # Validate command line arguments
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    # Ensure the employee ID is an integer
    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)

    # Fetch user information
    user_data = fetch_user_data(employee_id)

    # Fetch TODO list
    todos_data = fetch_todo_list(employee_id)

    # Process data
    employee_username = user_data.get("username")
    tasks = []
    for task in todos_data:
        tasks.append({
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": employee_username
        })

    # Structure the data as required
    data = {str(employee_id): tasks}

    # JSON file name
    json_filename = f"{employee_id}.json"

    # Write to JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file)
