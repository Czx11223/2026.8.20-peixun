from sqlalchemy.orm import Session
from .models import Question
from .services.data import SEED_QUESTIONS


def seed_questions(db: Session):
    """按 id 幂等补齐题库：旧库缺题自动补插，新增题目随升级生效，不覆盖已存在题目。"""
    exist = {q.id for q in db.query(Question).all()}
    added = 0
    for q in SEED_QUESTIONS:
        if q["id"] not in exist:
            db.add(Question(**q))
            added += 1
    if added:
        db.commit()
