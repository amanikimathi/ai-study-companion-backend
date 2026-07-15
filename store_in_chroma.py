import chromadb
from read_pdf import extract_text_from_pdf
from chunk_text import chunk_text
from embed import get_embedding

# Step 1: Create a ChromaDB client that saves data to a local folder
# (so it persists even after the script ends, unlike a normal Python variable)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Step 2: Create (or open, if it already exists) a collection to store our chunks
collection = chroma_client.get_or_create_collection(name="lecture_chunks")

def store_document(pdf_path: str):
    """Reads a PDF, chunks it, embeds each chunk, and stores everything in ChromaDB."""
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        vector = get_embedding(chunk)
        chunk_id = f"chunk_{i}"

        collection.add(
            ids=[chunk_id],
            embeddings=[vector],
            documents=[chunk]
        )
        print(f"Stored chunk {i+1}/{len(chunks)}")

    print(f"\nAll chunks stored. Collection now has {collection.count()} items.")

if __name__ == "__main__":
    store_document("my_lecture.pdf")
    