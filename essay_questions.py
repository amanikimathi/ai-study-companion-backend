import json
from read_pdf import extract_text_from_pdf
from test_gemini import ask_gemini

def generate_essay_questions(pdf_path: str, num_questions: int = 3) -> list[dict]:
    """Reads a PDF and asks Gemini to produce essay/short-answer questions,
    each with a few key points a strong answer should include."""

    text = extract_text_from_pdf(pdf_path)

    prompt = f"""Create {num_questions} essay/short-answer questions from the following
lecture notes, suitable for testing deeper understanding (not just recall).

For each question, also list 3-4 key points a strong answer should cover.

Respond with ONLY valid JSON, in exactly this format, and nothing else
(no markdown, no explanation, no code fences):

[
  {{
    "question": "...",
    "key_points": ["...", "...", "..."]
  }}
]

Lecture notes:
{text}"""

    response_text = ask_gemini(prompt)
    cleaned = response_text.replace("```json", "").replace("```", "").strip()

    essay_questions = json.loads(cleaned)
    return essay_questions

if __name__ == "__main__":
    questions = generate_essay_questions("my_lecture.pdf")

    print(f"Generated {len(questions)} essay questions:\n")
    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q['question']}")
        print("  Key points a strong answer should cover:")
        for point in q['key_points']:
            print(f"    - {point}")
        print()
        