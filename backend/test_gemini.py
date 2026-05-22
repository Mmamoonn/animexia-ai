import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
else:
    # Configure the SDK
    genai.configure(api_key=api_key)

    # Initialize the Gemini 3 Flash model
    model = genai.GenerativeModel('gemini-3-flash-preview')

    try:
        # Generate a simple response
        response = model.generate_content("Hello! If you can read this, the API key is working. Give me a 1-sentence fun fact about space.")
        print("--- Connection Successful ---")
        print(f"Model Response: {response.text}")
    except Exception as e:
        print("--- Connection Failed ---")
        print(f"Error details: {e}")