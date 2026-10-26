"""岗位配置与种子题库数据。

数据源：app/seed_data/{jobs,questions}.json（由 backend/tools/generate_seed.py 生成，
支持用 tools/import_jobs.py 按 CSV 幂等合并扩充）。
"""
import json
import os
from typing import List, Dict

_SEED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed_data")


def _load(name: str) -> List[Dict]:
    path = os.path.join(_SEED_DIR, name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


JOBS: List[Dict] = _load("jobs.json")
SEED_QUESTIONS: List[Dict] = _load("questions.json")


def get_job(job_id: str) -> Dict | None:
    return next((j for j in JOBS if j["id"] == job_id), None)


def get_jobs_by_company(company: str) -> List[Dict]:
    return [j for j in JOBS if j["company"] == company]
