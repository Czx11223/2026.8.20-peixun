from fastapi import APIRouter, UploadFile, File
from ..services.asr import transcribe

router = APIRouter(prefix="/api", tags=["asr"])


@router.post("/asr")
async def speech_to_text(audio: UploadFile = File(...)):
    data = await audio.read()
    text = transcribe(data, fmt=audio.filename.split(".")[-1] if audio.filename else "webm")
    return {"text": text}
