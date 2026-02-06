import os
import google.generativeai as genai
from dotenv import load_dotenv
import traceback

# Force load .env
load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print(f"Key loaded: {key[:5]}...{key[-5:] if key else 'None'}")

if not key:
    print("CRITICAL: No API Key found in environment variables.")
    exit(1)

genai.configure(api_key=key)

try:
    print("Attempting to list models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Found model: {m.name}")
            
    print("\nAttempting generation with gemini-pro...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello, are you working?")
    print("SUCCESS: Response received!")
    print(response.text)
except Exception as e:
    print("\nFAILURE: An error occurred.")
    traceback.print_exc()
