import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Answer, Interview, Question
from ..schemas import AnswerIn, AnswerOut
from ..services.llm import comment as llm_comment
from ..services.data import SEED_QUESTIONS

router = APIRouter(prefix="/api", tags=["answer"])


@router.post("/answer", response_model=AnswerOut)
def submit_answer(payload: AnswerIn, db: Session = Depends(get_db)):
    if not payload.answer.strip():
        raise HTTPException(422, "作答内容不能为空")
    # 关联面试会话：
    # 1) 优先使用前端传入的 interviewId（主链路），精确归属当前会话
    # 2) 未传时回退到最近创建的会话（按 date 倒序，而非 UUID 字典序——UUID 排序不等于创建顺序，会把答案挂到错误会话导致报告为空）
    # 3) 传了但找不到 → 明确 404，避免静默挂错会话
    interview = None
    if payload.interview_id:
        interview = db.query(Interview).filter(Interview.id == payload.interview_id).first()
        if not interview:
            raise HTTPException(404, "面试会话不存在，请重新开始面试")
    if interview is None:
        interview = (
            db.query(Interview)
            .order_by(Interview.date.desc(), Interview.id.desc())
            .first()
        )
    if not interview:
        interview = Interview(id=str(uuid.uuid4()), job_name="模拟面试", mode=payload.mode)
        db.add(interview)
        db.commit()
        db.refresh(interview)

    q = db.query(Question).filter(Question.id == payload.question_id).first()
    ref = q.reference_answer if q else next((s["reference_answer"] for s in SEED_QUESTIONS if s["id"] == payload.question_id), "")
    tpl = q.template if q else next((s["template"] for s in SEED_QUESTIONS if s["id"] == payload.question_id), "STAR：情境 → 任务 → 行动 → 结果")

    res = llm_comment(payload.question or (q.title if q else "面试题目"), payload.answer, payload.mode)
    question_text = payload.question or (q.title if q else "")

    # 自动保存模式：同一面试同一题 upsert（更新而非新增），保证每题仅一条记录、可反复修订
    answer = (
        db.query(Answer)
        .filter(Answer.interview_id == interview.id, Answer.question_id == payload.question_id)
        .first()
    )
    if answer is None:
        answer = Answer(id=str(uuid.uuid4()), interview_id=interview.id, question_id=payload.question_id)
        db.add(answer)
    answer.question = question_text
    answer.answer = payload.answer
    answer.score = res["score"]
    answer.grade = res["grade"]
    answer.is_weak = res["score"] < 70
    answer.comment = res["comment"]
    answer.suggestion = res["suggestion"]
    answer.reference_answer = ref
    answer.template = tpl
    db.commit()
    db.refresh(answer)
    return AnswerOut(
        id=answer.id, question_id=payload.question_id, question=answer.question, answer=answer.answer,
        score=answer.score, grade=answer.grade, is_weak=answer.is_weak, comment=answer.comment,
        suggestion=answer.suggestion, reference_answer=answer.reference_answer, template=answer.template,
    )