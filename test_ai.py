import os
from dotenv import load_dotenv
from groq import Groq

# Load hidden keys from .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: GROQ_API_KEY not found in your .env file!")
else:
    print("🔹 Found API Key, attempting connection...")
    try:
        # Initialize the free Groq client
        client = Groq(api_key=api_key)
        
        # Test a simple fast completion call using the 8B model
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say 'System Online!'"}]
        )
        print(f"✅ Success! AI Response: {completion.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")