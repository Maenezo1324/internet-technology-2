import hashlib
import time
from datetime import datetime

import requests
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, QuestionModel, engine, get_db
from schemas import QuestionRequest

Base.metadata.create_all(bind=engine)

app = FastAPI()


def fetch_unique_question(db_session: Session) -> dict:
    api_url = 'https://the-trivia-api.com/v2/questions?limit=1'
    for _ in range(5):
        try:
            response = requests.get(api_url, timeout=5)
        except requests.RequestException:
            pass
        else:
            if response.status_code == 200:
                payloads = response.json()
                if payloads:
                    question_item = payloads[0]
                    q_text = question_item.get('question', {}).get('text', '')
                    a_text = question_item.get('correctAnswer', '')

                    q_id = int(
                        hashlib.sha256(q_text.encode('utf-8')).hexdigest(),
                        16,
                    ) % (10 ** 8)

                    exists = db_session.query(QuestionModel).filter(
                        QuestionModel.question_id == q_id,
                    ).first()

                    if not exists:
                        return {
                            'id': q_id,
                            'question': q_text,
                            'answer': a_text,
                            'created_at': datetime.now().isoformat(),
                        }
        time.sleep(1)
    return {}


@app.post('/api/questions')
def create_questions(request: QuestionRequest, db: Session = Depends(get_db)):
    last_q = db.query(QuestionModel).order_by(QuestionModel.id.desc()).first()

    saved_count = 0
    while saved_count < request.questions_num:
        new_payload = fetch_unique_question(db)
        if not new_payload:
            return {'error': 'Не удалось получить вопрос от API викторины'}

        new_question = QuestionModel(
            question_id=new_payload['id'],
            question_text=new_payload['question'],
            answer_text=new_payload['answer'],
            created_at=datetime.fromisoformat(new_payload['created_at']),
        )
        db.add(new_question)
        db.commit()
        saved_count += 1

    if last_q:
        return {
            'id': last_q.question_id,
            'question': last_q.question_text,
            'answer': last_q.answer_text,
            'created_at': last_q.created_at.isoformat(),
        }
    return {}