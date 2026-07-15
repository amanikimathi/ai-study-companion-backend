from search import search_chunks
from test_gemini import ask_gemini

def rag_chat(question: str) -> str:
    """Answers a question using only the content of the uploaded lecture,
    by retrieving relevant chunks and asking Gemini to answer using them."""

    # Step 1: Retrieve the most relevant chunks for this question
    relevant_chunks = search_chunks(question, n_results=3)

    # Step 2: Combine the chunks into one block of context text
    context = "\n\n".join(relevant_chunks)

    # Step 3: Build a prompt that instructs Gemini to answer ONLY using this context
    prompt = f"""You are a helpful study assistant. Answer the student's question
using ONLY the context below. If the answer isn't in the context, say
"I don't see that in the lecture notes" instead of guessing.

Context:
{context}

Question: {question}

Answer:"""

    # Step 4: Send it to Gemini and return the answer
    answer = ask_gemini(prompt)
    return answer

if __name__ == "__main__":
    question = "What is the capital city of Nairobi"
    answer = rag_chat(question)

    print(f"Question: {question}\n")
    print(f"Answer: {answer}")
    