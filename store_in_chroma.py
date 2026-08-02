import chromadb
from read_pdf import extract_text_from_pdf
from chunk_text import chunk_text
from embed import get_embeddings_batch

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="lecture_chunks")

def store_document(pdf_path: str):
    """Reads a PDF, chunks it, embeds all chunks in one batch call,
    and stores everything in ChromaDB."""
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    # One API call for ALL chunks instead of one call per chunk
    embeddings = get_embeddings_batch(chunks)

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks
    )

    print(f"All {len(chunks)} chunks stored in one batch. Collection now has {collection.count()} items.")

if __name__ == "__main__":
    store_document("my_lecture.pdf")
    