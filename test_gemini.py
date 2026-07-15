import os
from dotenv import load_dotenv
from google import genai

# Toggle this to True if you want to test other code without using real API quota
USE_MOCK = False

load_dotenv()

def ask_gemini(prompt: str) -> str:
    """Sends a prompt to Gemini and returns the text response.
    When USE_MOCK is True, returns a fake response instead of
    making a real network call."""
    if USE_MOCK:
        return f"[MOCK RESPONSE] This is a fake AI answer standing in for: '{prompt}'"

    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    result = ask_gemini("Explain what RAG means in one sentence.")
    print(result)