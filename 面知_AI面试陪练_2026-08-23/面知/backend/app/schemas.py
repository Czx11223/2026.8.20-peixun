from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional, List


class ApiModel(BaseModel):
    """统一契约基类：输出 camelCase（对齐前端 TS 类型），同时兼容 snake_case 入参。

    - 响应序列化：FastAPI 默认 response_model_by_alias=True，字段将按别名(camelCase)输出
    - 请求解析：populate_by_name=True，前端 camelCase 与后端 snake_case 均可接收
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class QuestionOut(ApiModel):
    id: str
    title: str
    type: str = "行为面试 STAR"
    difficulty: str = "中等"
    industry: str = "互联网"
    company: str = ""  # 题目来源企业，校招通用题为空
    reference_answer: str = ""
    template: str = ""


class StartInterviewOut(ApiModel):
    """开始面试返回：interviewId / jobName / mode / questions（统一 camelCase 契约）"""

    interview_id: str
    job_name: str
    mode: str
    questions: List[QuestionOut]


class JobConfig(ApiModel):
    id: str
    name: str
    company: str = ""  # 所属企业（如 腾讯/华为），用于企业岗位与抽题企业优先匹配
    industry: str
    duration: int
    question_types: List[str]
    answer_mode: str = "text"  # text | voice
    mode: str = "normal"       # normal | pressure
    total_questions: int = 8


class AnswerIn(ApiModel):
    interview_id: str = ""  # 当前面试会话 id（修复：精确关联答案所属会话，避免按 UUID 字典序误挂其他会话）
    question_id: str
    question: str = ""
    answer: str
    mode: str = "text"


class AnswerOut(ApiModel):
    id: str
    question_id: str
    question: str
    answer: str
    score: int
    grade: str
    is_weak: bool
    comment: str
    suggestion: str
    reference_answer: str
    template: str


class Dimension(ApiModel):
    name: str
    score: int


class ReportOut(ApiModel):
    id: str
    job_name: str
    mode: str
    date: str
    total_score: int
    grade: str
    duration_sec: int
    summary: str
    dimensions: List[Dimension]
    answers: List[AnswerOut]


class GrowthPoint(ApiModel):
    date: str
    total: int
    expression: int
    logic: int


class InterviewHistory(ApiModel):
    id: str
    date: str
    job_name: str
    mode: str
    score: int
    grade: str
    duration_sec: int


class DashboardOut(ApiModel):
    total_sessions: int
    avg_score: int
    weak_dimension: str
    total_practice_min: int
    trend: List[GrowthPoint]
    dimensions: List[Dimension]
    history: List[InterviewHistory]


class ModelSettings(ApiModel):
    model_name: str = "deepseek-chat"
    api_key: str = ""
    base_url: str = "https://api.deepseek.com/v1"
    temperature: float = 0.7
    max_tokens: int = 2048


class QAIn(ApiModel):
    question: str


class InterviewFinishIn(ApiModel):
    """结束面试：上报实际练习时长（秒）"""

    duration_sec: int = 0
