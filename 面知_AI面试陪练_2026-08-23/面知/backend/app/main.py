from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db, SessionLocal
from .seed import seed_questions
from .routers import questions, interview, answers, report, growth, qa, asr, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_questions(db)
    finally:
        db.close()
    yield


app = FastAPI(title="面知 API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (questions.router, interview.router, answers.router, report.router,
          growth.router, qa.router, asr.router, user.router):
    app.include_router(r)


@app.get("/api/health")
def health():
    return {"status": "ok"}
