# -*- coding: utf-8 -*-
"""面知 岗位/题库批量导入工具（CSV → seed_data JSON 幂等合并）。

用法（先创建 CSV，UTF-8 编码）：
  python tools/import_jobs.py jobs.csv            # 导入岗位
  python tools/import_jobs.py questions.csv --type question
  python tools/import_jobs.py both.csv            # 根据表头自动识别

岗位 CSV 表头（id, name, company, industry, duration, question_types, answer_mode, mode, total_questions）
  示例行：bytedance-99, AI产品经理, 字节跳动, 互联网, 20, "产品分析,行为面试 STAR", text, normal, 8
题目 CSV 表头（id, title, type, difficulty, industry, company, reference_answer, template）
  示例行：q99, （字节跳动）如何设计AIGC产品？, 产品分析, 中等, 互联网, 字节跳动, 参考要点…, 模板…

导入后运行 python tools/generate_seed.py 重新生成前端 TS 数据。
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_DIR = os.path.join(ROOT, "app", "seed_data")


def load(name):
    path = os.path.join(SEED_DIR, name)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []


def save(name, data):
    path = os.path.join(SEED_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"已写入 {path}（{len(data)} 条）")


def parse_types(s):
    return [x.strip() for x in s.split(",") if x.strip()]


def import_file(csv_path, kind):
    with open(csv_path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("CSV 为空")
        return
    # 自动识别类型
    if kind is None:
        headers = set(rows[0].keys())
        kind = "job" if "name" in headers and "question_types" in headers else "question"

    if kind == "job":
        key = "id"
        data = load("jobs.json")
        seen = {d["id"] for d in data}
        n = 0
        for r in rows:
            rid = r["id"].strip()
            if not rid or rid in seen:
                continue
            data.append({
                "id": rid,
                "name": r["name"].strip(),
                "company": r.get("company", "").strip(),
                "industry": r.get("industry", "互联网").strip(),
                "duration": int(r.get("duration", 15)),
                "question_types": parse_types(r.get("question_types", "行为面试 STAR")),
                "answer_mode": r.get("answer_mode", "text").strip(),
                "mode": r.get("mode", "normal").strip(),
                "total_questions": int(r.get("total_questions", 8)),
            })
            seen.add(rid)
            n += 1
        save("jobs.json", data)
        print(f"导入岗位 {n} 条，跳过已存在 {len(rows) - n} 条")
    else:
        data = load("questions.json")
        seen = {d["id"] for d in data}
        n = 0
        for r in rows:
            rid = r["id"].strip()
            if not rid or rid in seen:
                continue
            data.append({
                "id": rid,
                "title": r["title"].strip(),
                "type": r.get("type", "行为面试 STAR").strip(),
                "difficulty": r.get("difficulty", "中等").strip(),
                "industry": r.get("industry", "互联网").strip(),
                "company": r.get("company", "").strip(),
                "reference_answer": r.get("reference_answer", "").strip(),
                "template": r.get("template", "").strip(),
            })
            seen.add(rid)
            n += 1
        save("questions.json", data)
        print(f"导入题目 {n} 条，跳过已存在 {len(rows) - n} 条")

    print("提示：再运行 python tools/generate_seed.py 同步前端数据。")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    kind = None
    if "--type" in sys.argv:
        kind = sys.argv[sys.argv.index("--type") + 1]
    import_file(sys.argv[1], kind)
