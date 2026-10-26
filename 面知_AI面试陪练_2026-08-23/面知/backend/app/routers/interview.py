import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Interview, Question, Answer
from ..services.data import get_job, SEED_QUESTIONS
from ..services.analysis import grade_from_score
from ..schemas import QuestionOut, StartInterviewOut, InterviewFinishIn

router = APIRouter(prefix="/api/interview", tags=["interview"])


@router.post("/start", response_model=StartInterviewOut)
def start_interview(
    # Query alias：前端传 jobId（camelCase），query 参数不做别名转换，必须显式声明
    job_id: str = Query("", alias="jobId"),
    db: Session = Depends(get_db),
):
    job = get_job(job_id) or get_job("java-dev")
    interview = Interview(
        id=str(uuid.uuid4()),
        job_name=job["name"],
        mode=job["mode"],
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)

    qs = db.query(Question).all()
    if not qs:
        qs = [Question(**s) for s in SEED_QUESTIONS]
    # 优先匹配岗位所属行业题库；不足时用全量补齐；统一截断到目标题量（落实「意向岗位题库匹配」）
    # 抽题：企业优先 → 行业 → 全量（落实「意向岗位/企业题库匹配」）
    company = job.get("company", "")
    industry = job.get("industry", "")
    target = job["total_questions"]
    picked = [q for q in qs if q.company and q.company == company]
    if len(picked) < target:
        picked += [q for q in qs if q.company != company and q.industry == industry]
    if len(picked) < target:
        picked += [q for q in qs if q.company != company and q.industry != industry]
    # 自我介绍题强制置顶第一题（面试惯例开场；若未被抽中则替换末位补齐题，保证总量不变）
    intro = next((x for x in qs if "自我介绍" in x.title or "introduce" in x.title.lower()), None)
    if intro and intro not in picked:
        if picked:
            picked[-1] = intro
        else:
            picked = [intro]
    picked.sort(key=lambda q: 0 if ("自我介绍" in q.title or "introduce" in q.title.lower()) else 1)
    qs = picked[:target]
    questions = [QuestionOut(**{
        "id": q.id, "title": q.title, "type": q.type, "difficulty": q.difficulty,
        "industry": q.industry, "company": q.company,
        "reference_answer": q.reference_answer, "template": q.template,
    }) for q in qs]
    return StartInterviewOut(
        interview_id=interview.id, job_name=job["name"], mode=job["mode"], questions=questions,
    )


@router.post("/{interview_id}/finish")
def finish_interview(interview_id: str, payload: InterviewFinishIn, db: Session = Depends(get_db)):
    """结束面试：上报实际练习时长（秒），并结算总分与评级（基于已保存作答），
    保证报告「用时/得分」与看板「练习总时长/记录」数据一致。"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(404, "面试会话不存在")
    interview.duration_sec = max(0, payload.duration_sec)
    answers = db.query(Answer).filter(Answer.interview_id == interview_id).all()
    if answers:
        avg = round(sum(a.score for a in answers) / len(answers))
        interview.total_score = avg
        interview.grade = grade_from_score(avg)
    db.commit()
    return {"ok": True, "durationSec": interview.duration_sec, "totalScore": interview.total_score}


@router.delete("/{interview_id}")
def cancel_interview(interview_id: str, db: Session = Depends(get_db)):
    """取消/退出面试：删除会话及其全部作答记录（不产生历史记录）。"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(404, "面试会话不存在")
    db.delete(interview)  # Interview.answers 配置了 cascade，连带删除
    db.commit()
    return {"ok": True}
