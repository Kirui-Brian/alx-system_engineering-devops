#!/usr/bin/python3
"""
Module: export_to_CSV

This module retrieves data from a REST API and exports the TODO list progress
for a given employee ID to a CSV file.
"""

import csv
import requests
import sys


def main():
    """
    Main function to fetch user information and TODO list data,
    process it, and export it to a CSV file.
    """
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)

    # Fetch user information
    user_url = (
        "https://jsonplaceholder.typicode.com/"
        f"users/{employee_id}"
    )
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print("User not found")
        sys.exit(1)
    user_data = user_response.json()

    # Fetch TODO list
    todos_url = (
        "https://jsonplaceholder.typicode.com/users/"
        f"{employee_id}/todos"
    )
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print("Error fetching TODO list")
        sys.exit(1)
    todos_data = todos_response.json()

    # Process data
    employee_username = user_data.get("username")

    # CSV file name
    csv_filename = f"{employee_id}.csv"

    # Write to CSV file
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for task in todos_data:
            writer.writerow([
                employee_id,
                employee_username,
                task.get("completed"),
                task.get("title")
            ])


if __name__ == "__main__":
    main()
