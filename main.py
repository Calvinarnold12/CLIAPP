import os
import requests
from dotenv import load_dotenv

# 1. Load configuration
load_dotenv()
TOKEN = os.getenv("CANVAS_API_TOKEN")
BASE_URL = "https://boisestatecanvas.instructure.com/api/v1"

if not TOKEN:
    print("Error: CANVAS_API_TOKEN not found in .env file.")
    exit()

headers = {"Authorization": f"Bearer {TOKEN}"}

def fetch_paginated_data(url):
    """Helper to handle Canvas pagination by following the 'next' link."""
    results = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
        
        results.extend(response.json())
        
        # Check 'Link' header for the 'next' relation
        url = response.links.get('next', {}).get('url')
    return results

def get_courses():
    """Endpoint 1: Fetch and display courses."""
    print("\n--- Fetching your courses ---")
    url = f"{BASE_URL}/courses?enrollment_state=active"
    courses = fetch_paginated_data(url)
    
    valid_courses = []
    for c in courses:
        if 'name' in c:
            print(f"[{c['id']}] {c['name']}")
            valid_courses.append(str(c['id']))
    return valid_courses

def get_assignments(course_id):
    """Endpoint 2: Fetch assignments for a specific course ID."""
    print(f"\n--- Fetching assignments for course {course_id} ---")
    url = f"{BASE_URL}/courses/{course_id}/assignments"
    assignments = fetch_paginated_data(url)
    
    if not assignments:
        print("No assignments found or access denied.")
        return

    print(f"{'Assignment Name':<50} | {'Due Date'}")
    print("-" * 75)
    for a in assignments:
        name = a.get('name', 'N/A')
        due = a.get('due_at', 'No Due Date')
        # Simple string slicing to make the date readable
        clean_date = due.replace('T', ' ').replace('Z', '') if due else "None"
        print(f"{name[:48]:<50} | {clean_date}")

def main():
    # List courses first
    available_ids = get_courses()
    
    # Requirement: Accept user input
    user_choice = input("\nEnter a Course ID to see assignments (or 'q' to quit): ").strip()
    
    if user_choice.lower() == 'q':
        return
    elif user_choice in available_ids:
        get_assignments(user_choice)
    else:
        print("Invalid ID. Please run the script again and pick an ID from the list.")

if __name__ == "__main__":
    main()