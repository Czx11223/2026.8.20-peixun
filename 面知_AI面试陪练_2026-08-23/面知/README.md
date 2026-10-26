# 面知 · AI 面试陪练工具（Web 全栈）

面向高校应届生的 AI 面试模拟陪练平台。支持岗位题库随机抽题、语音/文字双模式答题、AI 实时点评打分、面试报告与错题回看、个人能力成长看板。

> 设计语言：**极简蓝调（Apple 变体）** —— 无阴影、主色 `#007AFF`、双字重（400/600）、四级圆角、8px 栅格。

## 技术栈

| 层 | 选型 | 说明 |
|---|---|---|
| 前端 | Vue 3 + TypeScript + Vite + Tailwind CSS | 组件化、Pinia 状态、Vue Router |
| 后端 | FastAPI + Uvicorn | 异步 API，分层 router / service / model |
| 数据库 | SQLite | 零运维文件库 |
| 向量库 | ChromaDB（可选） | `use_vector=false` 时退化为关键字匹配 |
| 大模型 | DeepSeek API（可替换） | 无 Key 时自动降级本地 mock，开箱即跑 |
| 语音识别 | ASR SDK（可选） | 演示环境内置模拟转写 |
| 报告导出 | ReportLab | 生成 PDF 面试报告 |

## 目录结构

```
面知/
├── frontend/                 # Vue 3 + Vite
│   ├── src/
│   │   ├── components/       # App 前缀组件（设计系统）
│   │   ├── views/            # 6 大页面
│   │   ├── api/              # 接口封装（含 mock 兜底）
│   │   ├── mock/             # 演示数据
│   │   ├── router/ stores/ types/
│   │   └── style.css         # 设计令牌
│   └── tailwind.config.js    # 设计令牌注入
└── backend/                  # FastAPI
    └── app/
        ├── routers/          # 8 个路由模块
        ├── services/         # llm / asr / analysis / pdf / data
        ├── models.py schemas.py db.py config.py
        └── main.py
```

## 快速开始

### 前端
```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

### 后端
```bash
cd backend
pip install -r requirements.txt        # 核心依赖
pip install -r requirements-optional.txt  # 可选：ChromaDB 向量检索（体积大）
uvicorn app.main:app --reload --port 8000
```
访问 `http://127.0.0.1:8000/docs` 查看接口文档（自动生成，可在线调试）。

### 前后端联调
- 前端 `vite.config.ts` 已把 `/api` 代理到 `8000`。
- 后端统一输出 **camelCase**（与前端 TS 类型对齐），`src/api/index.ts` 通过环境变量开关后端：
  - `frontend/.env.development` 中 `VITE_USE_BACKEND=true` → `npm run dev` 即联调真实后端
  - 未配置时回退 `false` → 内置 mock，离线开箱即跑
- 完整主链路：模拟面试主页 → 开始面试（`POST /api/interview/start`）→ 逐题作答（`POST /api/answer`，实时点评）→ 生成报告（`GET /api/report/{id}`）→ 能力看板（`GET /api/growth`）。

## 接入真实大模型
在 `backend/.env` 配置（或环境变量 `MIANZHI_API_KEY` 等）：
```
MIANZHI_API_KEY=sk-xxxx
MIANZHI_MODEL_NAME=deepseek-chat
MIANZHI_BASE_URL=https://api.deepseek.com/v1
```
未配置 Key 时，后端自动降级为内置 mock 点评（`services/llm.py`），主流程不受影响。

## 题库与岗位数据（104 个真实企业岗位 + 78 道企业真题）
- 数据源：`backend/app/seed_data/{jobs,questions}.json`（单一事实来源）
- 重新生成 / 幂等合并：`python tools/generate_seed.py`（一次定义，同步输出后端 JSON 与前端 `src/mock/seed_data.ts`）
- **批量导入**：`python tools/import_jobs.py jobs.csv`（岗位）或 `python tools/import_jobs.py questions.csv --type question`（题目），CSV 表头见脚本顶部说明；导入后重跑生成器同步前端
- 抽题规则：**企业优先 → 行业 → 全量**（如「腾讯·AI全栈工程师」优先抽腾讯真题）
- 说明：内置岗位/题目基于公开招聘信息与公开面经整理；如需从招聘平台批量获取，请使用合规渠道（平台开放 API/导出功能）后通过 CSV 导入，避免违反平台协议。

## 6 大页面
1. 模拟面试主页（岗位筛选 + 配置卡片）
2. 面试进行中（倒计时 + AI 提问 + 作答 + 实时分析）
3. 面试报告 & 错题回看
4. 个人能力数据看板（折线 + 雷达 + 历史）
5. API 模型设置
6. 帮助中心

## 测试说明
已交付《面知 系统测试报告 v2》（`面知-test-report-v2.md`）：修复 2 个构建阻断（DashboardView 缺 computed 导入、缺 @types/node）、2 个功能缺陷（首页筛选键冲突、面试倒计时不自动走）、3 项优化（加载错误态、移动端筛选、用时精度），`npm run build` 回归通过。后端代码级测试与联调见本轮交付说明。
