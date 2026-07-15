from fastapi import FastAPI, UploadFile
from summary import generate_summary
from flashcards import generate_flashcards
from mcqs import generate_mcqs
from essay_questions import generate_essay_questions
from rag_chat import rag_chat
from store_in_chroma import store_document as store_in_chroma_db
from models import SessionLocal, Document, StudyPack

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Study Companion backend is running"}


async def save_upload(file: UploadFile) -> str:
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    return temp_path


@app.post("/generate-full-pack")
async def generate_full_pack(file: UploadFile):
    """Uploads a PDF, generates ALL study materials, stores it for RAG chat,
    and saves everything permanently to the database."""

    temp_path = await save_upload(file)

    # Step 1: Store chunks in ChromaDB for future RAG chat
    store_in_chroma_db(temp_path)

    # Step 2: Generate all content using our existing functions
    summary = generate_summary(temp_path)
    flashcards = generate_flashcards(temp_path)
    mcqs = generate_mcqs(temp_path)
    essay_qs = generate_essay_questions(temp_path)

    # Step 3: Open a database session (a temporary connection for these queries)
    db = SessionLocal()

    # Step 4: Create a Document row
    new_document = Document(filename=file.filename)
    db.add(new_document)
    db.commit()       # actually writes it to the database
    db.refresh(new_document)  # reloads it so we get its auto-generated id

    # Step 5: Create a StudyPack row, linked to that document
    new_study_pack = StudyPack(
        document_id=new_document.id,
        summary=summary,
        flashcards=flashcards,
        mcqs=mcqs,
        essay_questions=essay_qs
    )
    db.add(new_study_pack)
    db.commit()

    # Grab the id we need WHILE the session is still open
    document_id = new_document.id

    db.close()

    return {
        "document_id": document_id,
        "summary": summary,
        "flashcards": flashcards,
        "mcqs": mcqs,
        "essay_questions": essay_qs
    }


@app.get("/study-pack/{document_id}")
def get_study_pack(document_id: int):
    """Retrieves a previously generated study pack by document ID,
    instead of regenerating it from scratch."""

    db = SessionLocal()
    study_pack = db.query(StudyPack).filter(StudyPack.document_id == document_id).first()
    db.close()

    if study_pack is None:
        return {"error": "No study pack found for that document ID"}

    return {
        "summary": study_pack.summary,
        "flashcards": study_pack.flashcards,
        "mcqs": study_pack.mcqs,
        "essay_questions": study_pack.essay_questions
    }


@app.post("/chat")
async def chat_endpoint(question: str):
    answer = rag_chat(question)
    return {"answer": answer}

