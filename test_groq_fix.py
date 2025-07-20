import os
from dotenv import load_dotenv
import groq

load_dotenv()

def test_groq():
    api_key = os.getenv("GROQ_API_KEY")
    print(f"API Key loaded: {bool(api_key)}")
    
    if api_key:
        try:
            # Test the exact same initialization
            client = groq.Groq(api_key=api_key)
            print("✅ Client created successfully")
            
            # Test API call
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say hello and confirm you're working."}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            print("✅ API call successful!")
            print(f"Response: {response.choices[0].message.content}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_groq()