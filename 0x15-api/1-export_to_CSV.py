#!/usr/bin/python3
"""
Gather data from a REST API and export TODO list progress for a given employee ID to a CSV file
"""

import csv
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)

    # Fetch user information
    user_url = "https://jsonplaceholder.typicode.com/users/{}".format(employee_id)
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print("User not found")
        sys.exit(1)
    user_data = user_response.json()

    # Fetch TODO list
    todos_url = "https://jsonplaceholder.typicode.com/users/{}/todos".format(employee_id)
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print("Error fetching TODO list")
        sys.exit(1)
    todos_data = todos_response.json()

    # Process data
    employee_username = user_data.get("username")

    # CSV file name
    csv_filename = "{}.csv".format(employee_id)

    # Write to CSV file
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for task in todos_data:
            writer.writerow([employee_id, employee_username, task.get("completed"), task.get("title")])
