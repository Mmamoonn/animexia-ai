import requests
import json

# Define the URL (Make sure the server is running!)
url = 'http://127.0.0.1:5000/api/chat'

# The data we want to send
payload = {
    'message': 'Hello! Who are you?',
    'session_id': 'test_user_1'
}

print(f"📡 Sending message to {url}...")

try:
    # Send a POST request (simulate hitting 'Enter' in chat)
    response = requests.post(url, json=payload)
    
    # Print the result
    if response.status_code == 200:
        print("\n✅ SUCCESS!")
        print("🤖 Bot Reply:", response.json().get('response'))
    else:
        print(f"\n❌ FAILED: Status Code {response.status_code}")
        print("Error details:", response.text)

except requests.exceptions.ConnectionError:
    print("\n❌ FAILED: Could not connect.")
    print("👉 Is your Flask server running? Run 'python app.py' in a separate terminal.")