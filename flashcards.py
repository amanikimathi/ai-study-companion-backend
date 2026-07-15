import json
from read_pdf import extract_text_from_pdf
from test_gemini import ask_gemini

def generate_flashcards(pdf_path: str, num_cards: int = 8) -> list[dict]:
    """Reads a PDF and asks Gemini to produce flashcards as structured data
    (a list of question/answer pairs), not just plain text."""

    text = extract_text_from_pdf(pdf_path)

    prompt = f"""Create {num_cards} flashcards from the following lecture notes.
Each flashcard should have a "question" and an "answer".

Respond with ONLY valid JSON, in exactly this format, and nothing else
(no markdown, no explanation, no code fences):

[
  {{"question": "...", "answer": "..."}},
  {{"question": "...", "answer": "..."}}
]

Lecture notes:
{text}"""

    response_text = ask_gemini(prompt)

    # Gemini sometimes wraps JSON in ```json ... ``` even when told not to.
    # This strips that out just in case, so json.loads() doesn't break.
    cleaned = response_text.replace("```json", "").replace("```", "").strip()

    flashcards = json.loads(cleaned)
    return flashcards

if __name__ == "__main__":
    cards = generate_flashcards("my_lecture.pdf")

    print(f"Generated {len(cards)} flashcards:\n")
    for i, card in enumerate(cards):
        print(f"Card {i+1}")
        print(f"  Q: {card['question']}")
        print(f"  A: {card['answer']}")
        print()