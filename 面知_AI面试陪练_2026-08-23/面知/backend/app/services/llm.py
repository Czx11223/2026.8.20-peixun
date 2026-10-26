"""大模型服务：默认 DeepSeek；无 API Key 时自动降级为本地 mock 点评，保证可运行。"""
import re
import uuid
from typing import Dict, List

from ..config import settings


def _grade_from_score(score: int) -> str:
    if score >= 85: return "A"
    if score >= 75: return "B"
    if score >= 65: return "C"
    return "D"


def _mock_comment(question: str, answer: str, mode: str) -> Dict:
    chars = len(re.sub(r"\s", "", answer))
    fillers = len(re.findall(r"然后|那个|就是说|嗯|其实", answer))
    score = max(40, min(95, 55 + chars // 10 - fillers * 3))
    grade = _grade_from_score(score)
    if grade in ("S", "A"):
        comment = "回答结构清晰，要点完整，与岗位匹配度高。"
    elif grade == "B":
        comment = "整体尚可，但部分要点展开不足，建议补充量化结果。"
    else:
        comment = "回答偏简略，缺少结构化组织，建议用 STAR 法重新梳理。"
    return {
        "score": score,
        "grade": grade,
        "comment": comment,
        "suggestion": "使用 STAR 结构，先给结论再展开，并补充可量化的成果数据。",
        "dimensions": [
            {"name": "内容完整度", "score": min(100, score + 4)},
            {"name": "逻辑结构", "score": min(100, score + 2)},
            {"name": "表达流畅度", "score": max(40, score - 7)},
            {"name": "岗位匹配度", "score": min(100, score + 1)},
            {"name": "抗压表现", "score": max(40, score - 4) if mode == "pressure" else min(100, score)},
        ],
    }


def comment(question: str, answer: str, mode: str = "normal") -> Dict:
    """返回 AI 点评结果。生产环境调用 DeepSeek，演示环境走 mock。"""
    if not settings.api_key:
        return _mock_comment(question, answer, mode)

    try:
        import requests
        prompt = (
            "你是一位严格的校招面试考官。请对候选人的回答评分(0-100)并给出点评与优化建议，"
            "以及五个维度(内容完整度/逻辑结构/表达流畅度/岗位匹配度/抗压表现)的分值。\n"
            f"面试题目：{question}\n候选人回答：{answer}\n"
            "请严格以 JSON 返回：{score, grade, comment, suggestion, dimensions:[{name,score}]}"
        )
        resp = requests.post(
            f"{settings.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {settings.api_key}", "Content-Type": "application/json"},
            json={
                "model": settings.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": settings.temperature,
                "max_tokens": settings.max_tokens,
            },
            timeout=8,
        )
        content = resp.json()["choices"][0]["message"]["content"]
        import json
        data = json.loads(content)
        data["grade"] = data.get("grade") or _grade_from_score(data.get("score", 60))
        return data
    except Exception:
        # 调用失败兜底，不影响主流程
        return _mock_comment(question, answer, mode)


def answer_question(question: str) -> str:
    """AI 答疑（面试疑问辅导）。"""
    if not settings.api_key:
        return (
            f"关于「{question}」：建议使用 STAR 结构（情境-任务-行动-结果）组织回答，"
            "先抛结论再展开细节，并保持与岗位 JD 的强关联。可在模拟面试中针对性练习。"
        )
    try:
        import requests
        resp = requests.post(
            f"{settings.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {settings.api_key}", "Content-Type": "application/json"},
            json={
                "model": settings.model_name,
                "messages": [{"role": "user", "content": f"作为面试教练，简洁回答：{question}"}],
                "temperature": settings.temperature,
                "max_tokens": 800,
            },
            timeout=8,
        )
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return f"关于「{question}」：建议使用 STAR 结构组织回答，先给结论再展开细节。"
