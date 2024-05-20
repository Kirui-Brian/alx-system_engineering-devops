import requests
import json

# Define the API endpoints
users_url = "https://jsonplaceholder.typicode.com/users"
todos_url = "https://jsonplaceholder.typicode.com/todos"

# Fetch data from the API endpoints
users_response = requests.get(users_url)
todos_response = requests.get(todos_url)

# Parse the JSON responses
users = users_response.json()
todos = todos_response.json()

# Create a dictionary to hold the data in the required format
all_data = {}

# Process the data
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
with open('todo_all_employees.json', 'w') as json_file:
    json.dump(all_data, json_file, indent=4)

print("Data has been exported to todo_all_employees.json")
