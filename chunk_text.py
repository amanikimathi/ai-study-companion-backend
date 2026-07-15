from read_pdf import extract_text_from_pdf

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Splits a long string of text into smaller overlapping chunks.
    
    chunk_size: how many characters per chunk
    overlap: how many characters repeat between consecutive chunks,
             so we don't lose context at the boundary
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # move forward, but re-include the overlap

    return chunks

if __name__ == "__main__":
    text = extract_text_from_pdf("my_lecture.pdf")
    chunks = chunk_text(text)

    print(f"Total chunks created: {len(chunks)}\n")
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ({len(chunk)} chars) ---")
        print(chunk)
        print()
