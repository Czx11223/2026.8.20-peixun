"""成绩分析与报告聚合。"""
from typing import List, Dict


def grade_from_score(score: int) -> str:
    if score >= 85: return "A"
    if score >= 75: return "B"
    if score >= 65: return "C"
    return "D"


def build_summary(avg: int, weak_count: int, dimensions: List[Dict]) -> str:
    weakest = min(dimensions, key=lambda d: d["score"]) if dimensions else None
    if avg >= 80:
        base = "整体表现优秀，结构清晰、表达流畅，已具备较强的校招竞争力。"
    elif avg >= 70:
        base = "整体表现良好，基础扎实；在表达精炼度与量化成果上仍有提升空间。"
    else:
        base = "基础尚可，但回答结构与表达需要系统训练，建议结合模板多做专项练习。"
    if weakest:
        base += f"相对薄弱的维度是「{weakest['name']}」({weakest['score']} 分)，建议优先加强。"
    if weak_count:
        base += f"本次有 {weak_count} 道薄弱题目，可在错题回看中针对性复练。"
    return base
