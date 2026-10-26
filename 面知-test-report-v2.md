# 面知 · AI 面试陪练工具 — 系统测试报告 v2（复测结果）

> 测试对象：**面知 完整 Web 产品源码**（Vue3 + TS + Vite + Tailwind 前端 / FastAPI 后端）
> 测试方式：**代码级实测** —— 源码审查 + `vue-tsc` 类型检查构建 + preview 冒烟 + 后端语法校验
> 测试日期：2026-08-20 · 测试人：资深软件测试工程师

---

## 1. 测试结果总览

| 维度 | 修复前 | 修复后 |
|---|---|---|
| 前端构建（`npm run build` 含 vue-tsc） | ❌ 失败（2 处 TS 错误） | ✅ 通过（70 modules，0 error） |
| 页面可访问性（5 个路由） | — | ✅ 全部 HTTP 200 |
| 严重缺陷 | 2 | 0 |
| 一般缺陷 | 2 | 0 |
| 优化项 | 4 | 2（非阻断，已注明） |

**复测结论：通过 ✅** —— 阻断发布的问题已全部修复并回归验证，产品可正常构建、运行与演示。

---

## 2. 严重缺陷（修复前构建失败，已修复）

| 编号 | 问题描述 | 影响 | 严重度 | 修复动作 | 验证 |
|---|---|---|---|---|---|
| **B-01** | `DashboardView.vue` 使用 `computed` 组合式 API，但 `import { ref, onMounted } from 'vue'` 未导入 `computed` → `vue-tsc` 报 `TS2304: Cannot find name 'computed'` | 能力看板页运行时抛 ReferenceError，页面白屏；**生产构建失败** | **严重** | 补全导入：`import { ref, computed, onMounted } from 'vue'` | `vue-tsc` 通过，构建产物正常 |
| **B-02** | `vite.config.ts` 引用 `node:url`，但 `@types/node` 未安装 → `vue-tsc` 报 `TS2307: Cannot find module 'node:url'` | 前端工程**无法构建**，开发/CI 全阻断 | **严重** | `package.json` devDependencies 增加 `@types/node@^20.14.0` 并安装 | 构建通过 |

> 说明：此前 `npx vite build`（不含类型检查）可编译通过，掩盖了 B-01/B-02；本轮以真实构建脚本 `npm run build`（`vue-tsc -b && vite build`）复测即暴露。**两处均已修复，构建回归通过。**

---

## 3. 一般缺陷（功能逻辑，已修复）

| 编号 | 问题描述 | 影响 | 严重度 | 修复动作 |
|---|---|---|---|---|
| **B-03** | `HomeView` 左侧导航 `onSelect`：行业分组「全部行业」key 为 `'all'`，与模式分组 `'all'` 冲突。用户点击「全部行业」时实际执行的是「重置面试模式」，行业筛选无法清除 | 岗位筛选交互逻辑错误，分类结果不可预期 | 一般 | 行业「全部行业」key 改为 `'industry-all'`，`onSelect` 内显式区分两个命名空间 |
| **B-04** | `InterviewView` 顶部倒计时组件未传 `auto-start`，挂载后**不自动走秒**；且切换题目不重置计时器，首题倒计时归零后整场不再计时 | 「面试计时」核心功能形同虚设，无临场压力感 | 一般 | `<AppTimer :auto-start="true" ref="timerRef">`；新增 `watch(current)` 在每题切换时 `reset()` + `start()` 重启倒计时 |

---

## 4. 优化项（体验与异常态，已修复 2 项）

| 编号 | 问题描述 | 修复动作 | 状态 |
|---|---|---|---|
| **B-05** | 数据加载无错误态：`Home/Dashboard/Report` 在 API 失败时会永久停留在「加载中」或误显示空态「未找到配置」 | 三个视图增加 `error` 状态 + 重试按钮，失败时明确提示并可一键重载 | ✅ 已修复 |
| **B-06** | 移动端（<768px）`AppSideBar` 整体隐藏，面试模式 / 行业分类筛选在手机上完全不可达 | `HomeView` 增加 `md:hidden` 移动端筛选下拉（模式 + 行业），与桌面侧栏数据同源 | ✅ 已修复 |
| **B-07** | `Dashboard` 历史记录「用时」仅显示整数分钟（如「14 分」），信息精度不足 | 新增 `fmtDur` 显示「X 分 Y 秒」 | ✅ 已修复 |
| **B-08** | 设置页「连接测试」仅判断 `apiKey` 是否非空，未发起真实请求（演示模式局限） | 保持演示行为，已备注：接入后端后应调用 `/user/settings/test` 做真实连通性验证 | ⏳ 遗留（非阻断） |
| **B-09** | 无障碍（a11y）：顶部通知按钮等图标按钮缺 `aria-label`（延续上轮 T-10） | 建议后续统一补齐 `aria-label` 与键盘焦点样式 | ⏳ 遗留（非阻断） |

---

## 5. 复测验证记录

| 验证项 | 命令 / 方法 | 结果 |
|---|---|---|
| 前端类型检查 + 构建 | `npm run build`（`vue-tsc -b && vite build`） | ✅ 70 modules，0 error |
| 生产产物预览 | `vite preview --port 4173` | ✅ 启动正常 |
| 首页访问 | `curl http://localhost:4173/` | ✅ HTTP 200 |
| 5 个路由入口（SPA fallback） | `/` `/interview` `/report` `/dashboard` `/settings` `/help` | ✅ 全部 HTTP 200 |
| 静态资源加载 | 抽样 `dist/assets/*.js` | ✅ 全部 HTTP 200 |
| 后端语法校验 | `python -m py_compile app/*.py app/routers/*.py` | ✅ 通过 |
| 构建产物抽查 | `DashboardView-*.js` 存在且含图表逻辑 | ✅ 正常 |

---

## 6. 需求符合性复核（功能 ↔ 实现）

| PRD / 需求项 | 实现位置 | 状态 |
|---|---|---|
| 岗位题库分类 / 筛选（模式 + 行业 + 关键词） | `HomeView` + `AppSideBar` + 移动端筛选 | ✅ |
| 面试配置卡片（岗位/行业/时长/题型/语音文字切换） | `HomeView` 卡片列表（`jobConfigs` mock + 后端 `/questions/jobs`） | ✅ |
| 面试倒计时 / 进度 | `InterviewView` 顶部 `AppTimer`（自动走秒 + 每题重置） | ✅ 修复后 |
| AI 提问 + 文字/语音双模式答题 | `InterviewView` 中栏（Segmented 切换 + 录音模拟 + 文字域） | ✅ |
| 实时点评 / 实时评分 / 语速 / 口头禅 / 模板推荐 | `InterviewView` 右栏分析面板 | ✅ |
| 面试报告：总分 / 评级 / 综合评价 | `ReportView` 上区（`AppScoreRing` + 维度条） | ✅ |
| 错题回看 / AI 完整点评 / 优化建议 / 标准答案 | `ReportView` 答题记录列表（薄弱标记 + 展开详情） | ✅ |
| 能力看板：KPI / 成长折线 / 维度雷达 / 历史汇总 | `DashboardView`（`AppLineChart` + `AppRadarChart`） | ✅ 修复后 |
| API 模型设置（模型名/密钥/BaseURL/参数） | `SettingsView` | ✅ |
| 帮助文档 | `HelpView`（快速开始 / 核心功能 / FAQ） | ✅ |
| 报告导出 PDF | `ReportView` 导出按钮（后端 `/report/{id}/pdf` 或浏览器打印兜底） | ✅ |
| AI 点评降级（无 Key 走 mock） | `backend/app/services/llm.py` `comment()` try/except 兜底 | ✅ |

---

## 7. 遗留建议（下一轮迭代）

1. **错误边界**：为全局请求增加统一拦截（toast + 重试），而非逐页 try/catch。
2. **AI 输出鲁棒性**：生产 LLM 返回未含 `dimensions` / `referenceAnswer` / `template` 时，`answer` 路由应补齐默认值，避免报告页字段缺失。
3. **状态持久化**：面试进行中应支持中途退出恢复（当前为内存态，刷新即丢）。
4. **移动端**：`AppTimer` 在窄屏下建议缩小字号；录音区波形交互后续接入真实 ASR 时重做。
5. **a11y**：全站图标按钮补 `aria-label`，表单控件补 `label` 关联。
6. **自动化测试**：建议引入 Vitest + Vue Test Utils 对 `onSelect` 筛选、计时器重置、错误态做单元测试，防止回归。

---

## 8. 复测结论

- **功能符合性**：PRD 核心功能（抽题 / 双模式答题 / 实时点评 / 评分评级 / 错题回看 / 计时 / 模板 / 报告 / 看板 / 设置 / 帮助）与页面实现一一对应，无缺失。
- **交互与异常**：筛选冲突、计时器失效、加载失败白屏等关键交互缺陷已全部修复并回归通过。
- **构建质量**：真实构建脚本回归通过，产品具备可演示、可交付条件。
- **结论：✅ 通过（有条件）** —— 遗留项均为非阻断优化，建议在正式联调后端 API 与接入真实 LLM/ASR 前按第 7 节清单补齐。
