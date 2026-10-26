from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Question
from ..services.data import JOBS, SEED_QUESTIONS, get_job
from ..schemas import QuestionOut, JobConfig

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.get("/jobs", response_model=list[JobConfig])
def list_jobs():
    return [JobConfig(**j) for j in JOBS]


@router.get("", response_model=list[QuestionOut])
def list_questions(industry: str = "", db: Session = Depends(get_db)):
    q = db.query(Question)
    if industry:
        q = q.filter(Question.industry == industry)
    items = q.all()
    if not items:  # 数据库为空时回退到种子数据
        items = [Question(**s) for s in SEED_QUESTIONS]
    return [QuestionOut(**_to_dict(i)) for i in items]


def _to_dict(obj):
    if isinstance(obj, Question):
        return {
            "id": obj.id, "title": obj.title, "type": obj.type, "difficulty": obj.difficulty,
            "industry": obj.industry, "company": obj.company,
            "reference_answer": obj.reference_answer, "template": obj.template,
        }
    return obj.__dict__
