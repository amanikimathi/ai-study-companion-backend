import os
from dotenv import load_dotenv
from google import genai
from read_pdf import extract_text_from_pdf
from chunk_text import chunk_text

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_embedding(text: str) -> list[float]:
    """Converts a piece of text into a list of numbers (a vector)
    representing its meaning, using Gemini's embedding model."""
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

if __name__ == "__main__":
    # Step 1: Get the real PDF text and split it into chunks
    text = extract_text_from_pdf("my_lecture.pdf")
    chunks = chunk_text(text)

    # Step 2: Embed every chunk, one at a time
    embeddings = []
    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk)
        embeddings.append(vector)
        print(f"Chunk {i+1}/{len(chunks)} embedded — length: {len(vector)}")

    print(f"\nDone. Total embeddings created: {len(embeddings)}")