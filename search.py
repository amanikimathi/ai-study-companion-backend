import chromadb
from embed import get_embedding

# Connect to the same ChromaDB folder and collection we stored chunks in
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="lecture_chunks")

def search_chunks(question: str, n_results: int = 3) -> list[str]:
    """Takes a question, embeds it, and returns the most relevant
    stored chunks from ChromaDB based on meaning similarity."""
    
    # Step 1: Turn the question into a vector, same way we did for chunks
    question_vector = get_embedding(question)

    # Step 2: Ask ChromaDB for the closest matching stored vectors
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=n_results
    )

    # Step 3: Extract just the text of the matched chunks
    matched_chunks = results["documents"][0]
    return matched_chunks

if __name__ == "__main__":
    question = "What personality traits do entrepreneurs have?"
    matches = search_chunks(question)

    print(f"Question: {question}\n")
    for i, chunk in enumerate(matches):
        print(f"--- Match {i+1} ---")
        print(chunk)
        print()