# LectureLens

**Turn a single lecture PDF into a complete study kit — summary, flashcards, quiz questions, essay prompts, and an AI chat grounded in your own notes.**

**Live demo:** https://ai-study-companion-smoky.vercel.app
**Frontend repo:** https://github.com/amanithomas12/ai-study-companion-frontend

---

## What it does

Studying for one lecture usually means switching between several different AI tools — one for summaries, another for flashcards, another for practice questions. LectureLens consolidates all of that into one upload:

-**Summary** — a concise overview of the lecture
- **Flashcards** — interactive, flippable question/answer cards
- **Multiple choice questions** — with instant right/wrong feedback
- **Essay questions** — with key points a strong answer should cover
- **AI chat (RAG)** — ask questions about your own uploaded lecture. The AI only answers from content actually retrieved from your document — if the answer isn't in your notes, it says so honestly instead of guessing.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| AI | Google Gemini API (text generation + embeddings) |
| Vector search | ChromaDB (for RAG) |
| Database | PostgreSQL, SQLAlchemy |
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Auth | Clerk |
| Deployment | Render (backend + database), Vercel (frontend) |

## How it works

1. **Upload** — user uploads a lecture PDF through the web app
2. **Extraction** — `pypdf` pulls the readable text out of the PDF
3. **Chunking** — text is split into ~500-character overlapping chunks, so context isn't lost at chunk boundaries
4. **Embedding** — each chunk is converted into a 3072-dimension vector using Gemini's embedding model, batched into a single API call for speed
5. **Storage** — embeddings are stored in ChromaDB, a vector database, enabling meaning-based search
6. **Generation** — the full lecture text is sent to Gemini four times in parallel (via `asyncio`) to generate the summary, flashcards, MCQs, and essay questions as structured JSON
7. **Persistence** — the document and generated study pack are saved to PostgreSQL
8. **RAG chat** — when a user asks a question, it's embedded and compared against stored chunks; the closest matches are retrieved and passed to Gemini alongside the question, with an explicit instruction to answer *only* from that retrieved context

## Running locally

```bash
git clone https://github.com/amanithomas12/ai-study-companion-backend.git
cd ai-study-companion-backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/study_companion
```

Create the database tables:
```bash
python models.py
```

Run the server:
```bash
uvicorn main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`.

## Key API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/generate-full-pack` | POST | Upload a PDF, generate all study materials, save to database and ChromaDB |
| `/study-pack/{document_id}` | GET | Retrieve a previously generated study pack |
| `/chat` | POST | Ask a question, answered via RAG against stored documents |

## Challenges & how I solved them

- **Gemini free-tier rate limits** — original implementation made ~40+ separate embedding calls per document (one per chunk). Rewrote to batch all chunks into a single API call, and parallelized the four content-generation calls using `asyncio.gather`, cutting both API usage and response time significantly.
- **CORS** between the deployed frontend (Vercel) and backend (Render) — resolved with FastAPI's `CORSMiddleware`, explicitly allowlisting the live frontend origin.
- **A mid-project laptop reset** forced a full environment rebuild — recovered cleanly since the codebase was already version-controlled on GitHub, reinforcing why committing early and often matters.

## Known limitations / what's next

- Backend API endpoints don't yet verify Clerk auth tokens server-side (auth is currently enforced at the frontend UI level only)
- RAG chat currently searches across all stored documents rather than being scoped per-document
- PDF-only for now; Word/PowerPoint support is a planned addition
- Hosted on free-tier services — expect ~30-60s cold-start delay on the first request after inactivity

## Author

Built solo by Amani Thomas, a second-year software engineering student, as a portfolio project and hackathon submission.
