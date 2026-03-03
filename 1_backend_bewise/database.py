from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'postgresql://postgres:postgres@db:5432/quiz_db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class QuestionModel(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, unique=True, index=True)
    question_text = Column(String)
    answer_text = Column(String)
    created_at = Column(DateTime)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()