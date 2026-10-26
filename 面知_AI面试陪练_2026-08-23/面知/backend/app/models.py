from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(String(36), primary_key=True)
    title = Column(String(500), nullable=False)
    type = Column(String(50), default="行为面试 STAR")
    difficulty = Column(String(20), default="中等")
    industry = Column(String(50), default="互联网")
    company = Column(String(100), default="")  # 题目来源企业（如 字节跳动/腾讯/华为），校招通用题为空
    reference_answer = Column(Text, default="")
    template = Column(String(300), default="STAR：情境 → 任务 → 行动 → 结果")


class Interview(Base):
    __tablename__ = "interviews"
    id = Column(String(36), primary_key=True)
    job_name = Column(String(100), nullable=False)
    mode = Column(String(20), default="normal")  # normal | pressure
    date = Column(String(30), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    total_score = Column(Integer, default=0)
    grade = Column(String(2), default="C")
    duration_sec = Column(Integer, default=0)
    summary = Column(Text, default="")
    answers = relationship("Answer", back_populates="interview", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"
    id = Column(String(36), primary_key=True)
    interview_id = Column(String(36), ForeignKey("interviews.id"))
    question_id = Column(String(36), default="")  # 关联题目 id，用于同题自动保存 upsert
    question = Column(Text, default="")
    answer = Column(Text, default="")
    score = Column(Integer, default=0)
    grade = Column(String(2), default="C")
    is_weak = Column(Boolean, default=False)
    comment = Column(Text, default="")
    suggestion = Column(Text, default="")
    reference_answer = Column(Text, default="")
    template = Column(String(300), default="")
    interview = relationship("Interview", back_populates="answers")
