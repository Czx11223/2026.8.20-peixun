from fastapi import APIRouter
from ..schemas import QAIn
from ..services.llm import answer_question

router = APIRouter(prefix="/api", tags=["qa"])


@router.post("/qa")
def ai_qa(payload: QAIn):
    return {"answer": answer_question(payload.question)}
