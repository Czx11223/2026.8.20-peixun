# -*- coding: utf-8 -*-
"""面知 后端 API 冒烟测试（Python 版，规避终端中文编码问题）。
用法：先启动 uvicorn app.main:app --port 8000，再运行本脚本。
"""
import json
import sys
import requests

BASE = "http://127.0.0.1:8000/api"
PASS, FAIL = 0, 0


def ck(name, ok, extra=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  ✓ {name} {extra}")
    else:
        FAIL += 1
        print(f"  ✗ {name} {extra}")


def get(path, **kw):
    r = requests.get(BASE + path, timeout=10, **kw)
    return r


def post(path, data=None, **kw):
    r = requests.post(BASE + path, json=data, timeout=10, **kw)
    return r


print("== 1. 健康检查 ==")
r = get("/health")
ck("GET /health", r.status_code == 200, f"({r.status_code}) {r.text}")

print("== 2. 岗位配置（camelCase） ==")
r = get("/questions/jobs")
jobs = r.json()
expect = {"id", "name", "industry", "duration", "questionTypes", "answerMode", "mode", "totalQuestions"}
ck("GET /questions/jobs", r.status_code == 200 and len(jobs) >= 6 and expect.issubset(jobs[0].keys()),
   f"({r.status_code}) {len(jobs)} 岗位，字段={sorted(jobs[0].keys())}")

print("== 3. 题库（行业过滤） ==")
r = get("/questions", params={"industry": "互联网"})
qs = r.json()
ck("GET /questions?industry=互联网", r.status_code == 200 and all(q["industry"] == "互联网" for q in qs),
   f"({r.status_code}) {len(qs)} 题")

print("== 4. 开始面试（企业岗位 + 题量差异：普通面 8 / 压力面 10） ==")
r = post("/interview/start", params={"jobId": "tencent-01"})  # 腾讯 AI 全栈工程师（普通面 8 题）
started = r.json()
iid = started.get("interviewId", "")
n_normal = len(started.get("questions", []))
ck("POST /interview/start?jobId=tencent-01",
   r.status_code == 200 and iid and n_normal == 8 and started.get("jobName") == "AI全栈工程师",
   f"({r.status_code}) jobName={started.get('jobName')} 题目数={n_normal}(期望8)")
r2 = post("/interview/start", params={"jobId": "sgcc-01"})  # 国家电网 电气工程岗（压力面 10 题）
st2 = r2.json()
n_pressure = len(st2.get("questions", []))
ck("POST /interview/start?jobId=sgcc-01(压力面)",
   r2.status_code == 200 and n_pressure == 10 and st2.get("jobName") == "电气工程岗",
   f"({r2.status_code}) jobName={st2.get('jobName')} 题目数={n_pressure}(期望10)")
ck("压力面题量 > 普通面题量", n_pressure > n_normal, f"{n_pressure} > {n_normal}")

print("== 5. 提交作答（带 interviewId 精确归属，答 2 题） ==")
answers_submitted = []
for qi, (qid, qt, txt) in enumerate([
    ("q2", "说说你遇到过最难的技术问题，是如何解决的？",
     "我遇到了一个并发问题，然后我查了日志，就是说定位到了缓存击穿，最后加了锁并压测验证解决了。"),
    ("q1", "请自我介绍，并说明为什么选择我们这个岗位？",
     "我是计算机专业应届生，做过两个Java项目，熟悉Spring全家桶，对这个岗位很感兴趣。"),
], 1):
    r = post("/answer", data={
        "interviewId": iid,  # 关键：精确关联当前会话
        "questionId": qid,
        "question": qt,
        "answer": txt,
        "mode": "text",
    })
    ans = r.json()
    ok = r.status_code == 200 and {"score", "grade", "isWeak", "referenceAnswer", "template"}.issubset(ans.keys())
    ck(f"POST /answer 第{qi}题(interviewId归属)",
       ok, f"({r.status_code}) score={ans.get('score')} grade={ans.get('grade')} isWeak={ans.get('isWeak')}")
    if ok:
        answers_submitted.append(ans["id"])

print("== 6. 生成报告（应聚合本会话全部点评） ==")
r = get(f"/report/{iid}")
rep = r.json()
ck("GET /report/{id} 聚合答案",
   r.status_code == 200 and len(rep.get("answers", [])) == len(answers_submitted) == 2
   and rep.get("totalScore", 0) > 0,
   f"({r.status_code}) totalScore={rep.get('totalScore')} grade={rep.get('grade')} "
   f"answers={len(rep.get('answers', []))}(期望{len(answers_submitted)})")
ck("报告答案 id 与会话一致",
   {a.get("id") for a in rep.get("answers", [])} == set(answers_submitted),
   f"id集合={'一致' if {a.get('id') for a in rep.get('answers', [])} == set(answers_submitted) else '不一致'}")

print("== 7. 报告导出 PDF ==")
r = get(f"/report/{iid}/pdf")
ck("GET /report/{id}/pdf", r.status_code == 200 and r.content[:4] == b"%PDF",
   f"({r.status_code}) {len(r.content)} bytes, 魔数={r.content[:4]}")

print("== 8. 能力看板（camelCase） ==")
r = get("/growth")
dash = r.json()
ck("GET /growth",
   r.status_code == 200 and {"totalSessions", "avgScore", "weakDimension", "totalPracticeMin", "history"}.issubset(dash.keys()),
   f"({r.status_code}) sessions={dash.get('totalSessions')} avg={dash.get('avgScore')} weak={dash.get('weakDimension')}")

print("== 9. AI 答疑（中文） ==")
r = post("/qa", data={"question": "如何回答自我介绍？"})
ck("POST /qa", r.status_code == 200 and r.json().get("answer"),
   f"({r.status_code}) answer={r.json().get('answer', '')[:36]}...")

print("== 10. 模型设置读写 ==")
r = get("/user/settings")
ck("GET /user/settings", r.status_code == 200 and {"modelName", "apiKey", "baseUrl", "temperature", "maxTokens"}.issubset(r.json().keys()),
   f"({r.status_code}) 字段={sorted(r.json().keys())}")
r = requests.put(BASE + "/user/settings", json={
    "modelName": "deepseek-chat", "apiKey": "", "baseUrl": "https://api.deepseek.com/v1",
    "temperature": 0.5, "maxTokens": 2048,
}, timeout=10)
ck("PUT /user/settings (camelCase)", r.status_code == 200, f"({r.status_code}) {r.text}")

print("== 11. 异常场景：不存在的报告 ==")
r = get("/report/not-exist-id")
ck("GET /report/not-exist-id → 404", r.status_code == 404, f"({r.status_code}) {r.text}")

print("== 12. 异常场景：缺参答题（应 422） ==")
r = post("/answer", data={"answer": "没有题目 id"})
ck("POST /answer 缺 questionId → 422", r.status_code == 422, f"({r.status_code})")

print(f"\n=========== 结果: PASS={PASS} FAIL={FAIL} ===========")
sys.exit(0 if FAIL == 0 else 1)
