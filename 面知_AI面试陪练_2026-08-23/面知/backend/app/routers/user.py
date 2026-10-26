from fastapi import APIRouter
from ..schemas import ModelSettings
from ..config import settings

router = APIRouter(prefix="/api/user", tags=["user"])

# 演示环境用内存存储；生产环境应持久化到数据库或加密配置
_store = ModelSettings(
    model_name=settings.model_name,
    api_key=settings.api_key,
    base_url=settings.base_url,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
)


@router.get("/settings", response_model=ModelSettings)
def get_settings():
    return _store


@router.put("/settings")
def save_settings(payload: ModelSettings):
    global _store
    _store = payload
    return {"ok": True}
