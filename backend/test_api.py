import requests
import json

print("\n🎌 Testing Animexia AI Backend...")
print("=" * 60)

# API endpoint
url = "http://localhost:5000/api/chat"

# Test message
test_message = {
    "message": "Recommend me a good action anime!"
}

try:
    # Send request
    print("📤 Sending request to backend...")
    response = requests.post(url, json=test_message)
    
    # Check if request was successful
    if response.status_code == 200:
        result = response.json()
        
        print("\n✅ Backend is working!")
        print("\n🤖 Animexia AI Response:")
        print("-" * 60)
        print(result['response'])
        print("-" * 60)
        print(f"\n📊 Status: {result['status']}")
    else:
        print(f"\n❌ Error: Status code {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("\n❌ Error: Cannot connect to backend!")
    print("Make sure app.py is running in another terminal.")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 60)