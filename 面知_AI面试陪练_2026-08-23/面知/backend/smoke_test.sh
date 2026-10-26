#!/bin/bash
# 面知 后端 API 冒烟测试（需先启动 uvicorn app.main:app --port 8000）
BASE="http://127.0.0.1:8000/api"
PY="C:\\Users\\20454\\.workbuddy\\binaries\\python\\envs\\default\\Scripts\\python.exe"
PASS=0; FAIL=0
ck() { # ck <name> <expected_http> <actual_http>
  if [ "$2" = "$3" ]; then PASS=$((PASS+1)); echo "  ✓ $1 ($3)";
  else FAIL=$((FAIL+1)); echo "  ✗ $1 期望$2 实际$3"; fi
}

echo "== 1. 健康检查 =="
code=$(curl -s -o /tmp/smoke_health.json -w "%{http_code}" "$BASE/health"); ck "GET /health" 200 "$code"
echo "   body: $(cat /tmp/smoke_health.json)"

echo "== 2. 岗位配置 =="
code=$(curl -s -o /tmp/smoke_jobs.json -w "%{http_code}" "$BASE/questions/jobs"); ck "GET /questions/jobs" 200 "$code"
"$PY" -c "import json;d=json.load(open('/tmp/smoke_jobs.json'));print(f'   {len(d)} 个岗位, 首项字段: {sorted(d[0].keys())}')" 2>/dev/null || head -c 200 /tmp/smoke_jobs.json

echo "== 3. 题库（行业过滤） =="
code=$(curl -s -o /tmp/smoke_q.json -w "%{http_code}" "$BASE/questions?industry=%E4%BA%92%E8%81%94%E7%BD%91"); ck "GET /questions?industry=互联网" 200 "$code"
"$PY" -c "import json;d=json.load(open('/tmp/smoke_q.json'));print(f'   {len(d)} 题, 首题字段: {sorted(d[0].keys())}')" 2>/dev/null

echo "== 4. 开始面试 =="
code=$(curl -s -o /tmp/smoke_start.json -w "%{http_code}" -X POST "$BASE/interview/start?jobId=java-dev"); ck "POST /interview/start?jobId=java-dev" 200 "$code"
"$PY" -c "
import json;d=json.load(open('/tmp/smoke_start.json'))
print(f'   interviewId={d[\"interviewId\"][:8]}... jobName={d[\"jobName\"]} mode={d[\"mode\"]} 题目数={len(d[\"questions\"])}')
open('/tmp/smoke_iid.txt','w').write(d['interviewId'])" 2>/dev/null || head -c 300 /tmp/smoke_start.json

echo "== 5. 提交作答（AI 点评降级 mock） =="
iid=$(cat /tmp/smoke_iid.txt 2>/dev/null)
code=$(curl -s -o /tmp/smoke_ans.json -w "%{http_code}" -X POST "$BASE/answer" -H "Content-Type: application/json" \
  -d "{\"questionId\":\"q2\",\"question\":\"说说你遇到过最难的技术问题\",\"answer\":\"我遇到了一个并发问题，然后我查了日志，就是说定位到了缓存击穿，最后加了锁解决了。\",\"mode\":\"text\"}")
ck "POST /answer (camelCase 入参)" 200 "$code"
"$PY" -c "
import json;d=json.load(open('/tmp/smoke_ans.json'))
print(f'   score={d[\"score\"]} grade={d[\"grade\"]} isWeak={d[\"isWeak\"]} 字段={sorted(d.keys())}')" 2>/dev/null || head -c 300 /tmp/smoke_ans.json

echo "== 6. 生成报告 =="
code=$(curl -s -o /tmp/smoke_report.json -w "%{http_code}" "$BASE/report/$iid"); ck "GET /report/{id}" 200 "$code"
"$PY" -c "
import json;d=json.load(open('/tmp/smoke_report.json'))
print(f'   totalScore={d[\"totalScore\"]} grade={d[\"grade\"]} dims={len(d[\"dimensions\"])} answers={len(d[\"answers\"])} 字段={sorted(d.keys())}')" 2>/dev/null || head -c 300 /tmp/smoke_report.json

echo "== 7. 报告 PDF =="
code=$(curl -s -o /tmp/smoke_report.pdf -w "%{http_code}" "$BASE/report/$iid/pdf"); ck "GET /report/{id}/pdf" 200 "$code"
head -c 8 /tmp/smoke_report.pdf | grep -q "%PDF" && { echo "   ✓ PDF 魔数 %PDF"; PASS=$((PASS+1)); } || { echo "   ✗ 非 PDF"; FAIL=$((FAIL+1)); }

echo "== 8. 能力看板 =="
code=$(curl -s -o /tmp/smoke_growth.json -w "%{http_code}" "$BASE/growth"); ck "GET /growth" 200 "$code"
"$PY" -c "
import json;d=json.load(open('/tmp/smoke_growth.json'))
print(f'   sessions={d[\"totalSessions\"]} avg={d[\"avgScore\"]} weak={d[\"weakDimension\"]} 字段={sorted(d.keys())}')" 2>/dev/null || head -c 300 /tmp/smoke_growth.json

echo "== 9. AI 答疑 =="
code=$(curl -s -o /tmp/smoke_qa.json -w "%{http_code}" -X POST "$BASE/qa" -H "Content-Type: application/json" -d '{"question":"如何回答自我介绍？"}')
ck "POST /qa" 200 "$code"
"$PY" -c "import json;print('   answer:',json.load(open('/tmp/smoke_qa.json'))['answer'][:40]+'...')" 2>/dev/null

echo "== 10. 模型设置读写 =="
code=$(curl -s -o /tmp/smoke_set.json -w "%{http_code}" "$BASE/user/settings"); ck "GET /user/settings" 200 "$code"
code=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE/user/settings" -H "Content-Type: application/json" \
  -d '{"modelName":"deepseek-chat","apiKey":"","baseUrl":"https://api.deepseek.com/v1","temperature":0.5,"maxTokens":2048}')
ck "PUT /user/settings (camelCase)" 200 "$code"

echo ""
echo "=========== 结果: PASS=$PASS FAIL=$FAIL ==========="
[ "$FAIL" -eq 0 ] && echo "SMOKE_OK" || echo "SMOKE_FAIL"
