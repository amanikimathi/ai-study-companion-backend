import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The "engine" is the actual connection to your PostgreSQL database
engine = create_engine(DATABASE_URL)

# Base is a special class that all our table definitions will inherit from
Base = declarative_base()

# SessionLocal lets us create "sessions" - temporary connections used
# to run queries (add, read, update, delete data)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    """Represents a student using the app."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    clerk_id = Column(String, unique=True)  # will link to Clerk auth later
    email = Column(String, unique=True)

    # This lets us access user.documents to get all documents this user uploaded
    documents = relationship("Document", back_populates="owner")


class Document(Base):
    """Represents one uploaded PDF."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="documents")
    study_pack = relationship("StudyPack", back_populates="document", uselist=False)


class StudyPack(Base):
    """Represents the generated AI content for one document."""
    __tablename__ = "study_packs"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))

    summary = Column(Text)
    flashcards = Column(JSON)
    mcqs = Column(JSON)
    essay_questions = Column(JSON)

    document = relationship("Document", back_populates="study_pack")


# This creates all the tables above in your actual PostgreSQL database,
# if they don't already exist
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created successfully.")