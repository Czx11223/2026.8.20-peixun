from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Interview, Answer
from ..schemas import DashboardOut, Dimension, GrowthPoint, InterviewHistory
from ..services.analysis import grade_from_score

router = APIRouter(prefix="/api", tags=["growth"])


def _effective_score(i: Interview) -> int:
    """有效得分：优先按作答实时平均（保证看板与报告一致，兼容历史未结算记录）。"""
    if i.answers:
        return round(sum(a.score for a in i.answers) / len(i.answers))
    return i.total_score


@router.get("/growth", response_model=DashboardOut)
def get_dashboard(db: Session = Depends(get_db)):
    # 只统计「有实际作答」的完成记录（过滤未完成/废弃的空会话），并按新到旧排列（最新在上）。
    # 注：Interview.answers 一对多，join 后用 distinct() 去重，避免同一场面试重复出现。
    interviews = (
        db.query(Interview)
        .join(Answer)
        .distinct()
        .order_by(Interview.date.desc(), Interview.id.desc())
        .all()
    )
    if not interviews:
        # 无数据时返回空结构，前端将落入 mock 演示数据
        return DashboardOut(
            total_sessions=0, avg_score=0, weak_dimension="—", total_practice_min=0,
            trend=[], dimensions=[], history=[],
        )

    history = [InterviewHistory(
        id=i.id, date=i.date[:10], job_name=i.job_name, mode=i.mode, score=_effective_score(i),
        grade=grade_from_score(_effective_score(i)), duration_sec=i.duration_sec,
    ) for i in interviews]

    avg = round(sum(_effective_score(i) for i in interviews) / len(interviews))
    # 折线图按时间正序（旧 → 新）绘制更符合阅读习惯；表格 history 保持倒序（最新在上）
    trend_sorted = list(reversed(interviews))
    trend = [GrowthPoint(date=i.date[:10], total=_effective_score(i), expression=max(40, _effective_score(i) - 7),
                         logic=min(100, _effective_score(i) + 2)) for i in trend_sorted]
    dimensions = [
        Dimension(name="内容完整度", score=min(100, avg + 4)),
        Dimension(name="逻辑结构", score=min(100, avg + 2)),
        Dimension(name="表达流畅度", score=max(40, avg - 7)),
        Dimension(name="岗位匹配度", score=min(100, avg + 1)),
        Dimension(name="抗压表现", score=max(40, avg - 4)),
    ]
    weak = min(dimensions, key=lambda d: d.score).name
    total_min = sum(i.duration_sec for i in interviews) // 60
    return DashboardOut(
        total_sessions=len(interviews), avg_score=avg, weak_dimension=weak,
        total_practice_min=total_min, trend=trend, dimensions=dimensions, history=history,
    )
