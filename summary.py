from read_pdf import extract_text_from_pdf
from test_gemini import ask_gemini

def generate_summary(pdf_path: str) -> str:
    """Reads a PDF and asks Gemini to produce a concise summary of it."""

    text = extract_text_from_pdf(pdf_path)

    prompt = f"""Summarize the following lecture notes for a student studying for an exam.
Keep it concise (around 150-200 words), and focus on the key concepts,
not minor details. Write in plain text only, with no markdown formatting
(no asterisks, no bold, no bullet point symbols like * or -).

Lecture notes:
{text}

Summary:"""

    summary = ask_gemini(prompt)
    return summary

if __name__ == "__main__":
    summary = generate_summary("my_lecture.pdf")
    print(summary)