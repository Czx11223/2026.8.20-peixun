import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

db_dir = os.path.dirname(settings.db_path)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    f"sqlite:///{settings.db_path}",
    connect_args={"check_same_thread": False},
    future=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # 延迟导入避免循环依赖
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    _migrate()


def _migrate():
    """SQLite 轻量迁移：为旧库补列（新库 create_all 已含，此处幂等）。"""
    from sqlalchemy import text
    with engine.begin() as conn:
        q_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(questions)")).fetchall()]
        if "company" not in q_cols:
            conn.execute(text("ALTER TABLE questions ADD COLUMN company VARCHAR(100) DEFAULT ''"))
        a_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(answers)")).fetchall()]
        if "question_id" not in a_cols:
            conn.execute(text("ALTER TABLE answers ADD COLUMN question_id VARCHAR(36) DEFAULT ''"))
