import json
from read_pdf import extract_text_from_pdf
from test_gemini import ask_gemini

def generate_mcqs(pdf_path: str, num_questions: int = 5) -> list[dict]:
    """Reads a PDF and asks Gemini to produce multiple-choice questions
    as structured data: a question, 4 options, and the correct answer."""

    text = extract_text_from_pdf(pdf_path)

    prompt = f"""Create {num_questions} multiple-choice questions from the following
lecture notes, for a student studying for an exam.

Each question should have exactly 4 options, with only one correct answer.

Respond with ONLY valid JSON, in exactly this format, and nothing else
(no markdown, no explanation, no code fences):

[
  {{
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "..."
  }}
]

The "correct_answer" must exactly match one of the strings in "options".

Lecture notes:
{text}"""

    response_text = ask_gemini(prompt)
    cleaned = response_text.replace("```json", "").replace("```", "").strip()

    mcqs = json.loads(cleaned)
    return mcqs

if __name__ == "__main__":
    questions = generate_mcqs("my_lecture.pdf")

    print(f"Generated {len(questions)} MCQs:\n")
    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q['question']}")
        for opt in q['options']:
            marker = "✓" if opt == q['correct_answer'] else " "
            print(f"  [{marker}] {opt}")
        print()
        