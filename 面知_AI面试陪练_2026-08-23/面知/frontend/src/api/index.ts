import type {
  JobConfig, QuestionItem, InterviewReport, DashboardStat, ModelSettings, AnswerRecord
} from '@/types'
import * as mock from '@/mock'

// 是否启用真实后端。
// 默认读环境变量 VITE_USE_BACKEND：npm run dev 联调时 .env.development 置为 true；
// 构建产物未配置时回退 false → 内置 mock，保证离线开箱即跑。
const USE_BACKEND = (import.meta as any).env?.VITE_USE_BACKEND === 'true' || false

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init
  })
  if (!res.ok) {
    const err = new Error(`API ${res.status}`) as Error & { status: number }
    err.status = res.status
    throw err
  }
  return res.json() as Promise<T>
}

// 开始面试的返回结构（真实后端契约）
export interface StartedInterview {
  interviewId: string
  jobName: string
  mode: string
  questions: QuestionItem[]
}

export const api = {
  // 岗位配置卡片
  async getJobs(): Promise<JobConfig[]> {
    if (!USE_BACKEND) return mock.jobConfigs
    return request<JobConfig[]>('/questions/jobs')
  },

  // 题库（按岗位/行业筛选）
  async getQuestions(industry?: string): Promise<QuestionItem[]> {
    if (!USE_BACKEND) return mock.questions
    return request<QuestionItem[]>(`/questions?industry=${industry ?? ''}`)
  },

  // 开始面试：返回题目列表
  async startInterview(jobId: string): Promise<StartedInterview> {
    if (!USE_BACKEND) {
      // mock 模式：按岗位题量(普通8/压力10)与行业优先取题，与后端逻辑一致
      const job = mock.jobConfigs.find((j) => j.id === jobId) ?? mock.jobConfigs[0]
      const total = job?.totalQuestions ?? 8
      const pool = job
        ? [...mock.questions.filter((q) => q.industry === job.industry), ...mock.questions.filter((q) => q.industry !== job.industry)]
        : mock.questions
      return {
        interviewId: 'iv-' + Date.now(),
        jobName: job?.name ?? '',
        mode: job?.mode ?? 'normal',
        questions: pool.slice(0, total)
      }
    }
    return request<StartedInterview>(`/interview/start?jobId=${jobId}`, { method: 'POST' })
  },

  // 提交作答，返回 AI 点评
  async submitAnswer(payload: {
    interviewId?: string; questionId: string; answer: string; mode: string
  }): Promise<AnswerRecord> {
    if (!USE_BACKEND) {
      const q = mock.questions.find((x) => x.id === payload.questionId)
      return mockAnswer(q?.title ?? '面试题目', payload.answer)
    }
    return request<AnswerRecord>('/answer', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  },

  // 生成报告（真实记录不存在时降级为示例报告，保证演示不破）
  async getReport(interviewId: string): Promise<InterviewReport> {
    if (!USE_BACKEND) return mock.sampleReport
    try {
      return await request<InterviewReport>(`/report/${interviewId}`)
    } catch (e: any) {
      if (e?.status === 404) return mock.sampleReport
      throw e
    }
  },

  // 最近一次面试的报告（报告页无 id 时默认展示）
  async getRecentReport(): Promise<InterviewReport> {
    if (!USE_BACKEND) return mock.sampleReport
    try {
      return await request<InterviewReport>('/report/recent')
    } catch (e: any) {
      if (e?.status === 404) return mock.sampleReport
      throw e
    }
  },

  // 结束面试：上报实际练习时长（秒），用于报告「用时」与看板「练习总时长」
  async finishInterview(interviewId: string, durationSec: number): Promise<void> {
    if (!USE_BACKEND) return
    await request(`/interview/${interviewId}/finish`, {
      method: 'POST',
      body: JSON.stringify({ durationSec })
    })
  },

  // 取消/退出面试：删除会话及其作答，不产生历史记录
  async cancelInterview(interviewId: string): Promise<void> {
    if (!USE_BACKEND) return
    await request(`/interview/${interviewId}`, { method: 'DELETE' })
  },

  // 能力看板
  async getDashboard(): Promise<DashboardStat> {
    if (!USE_BACKEND) return mock.dashboardStat
    return request<DashboardStat>('/growth')
  },

  // 历史记录
  async getHistory(): Promise<InterviewReport['answers'] | DashboardStat['history']> {
    if (!USE_BACKEND) return mock.dashboardStat.history
    return request('/interviews')
  },

  // 模型设置
  async getSettings(): Promise<ModelSettings> {
    if (!USE_BACKEND) {
      return { modelName: 'deepseek-chat', apiKey: '', baseUrl: 'https://api.deepseek.com/v1', temperature: 0.7, maxTokens: 2048 }
    }
    return request<ModelSettings>('/user/settings')
  },
  async saveSettings(s: ModelSettings): Promise<void> {
    if (!USE_BACKEND) return
    return request<void>('/user/settings', { method: 'PUT', body: JSON.stringify(s) })
  },

  // AI 答疑（真实后端返回 { answer }，此处抽取文本）
  async askAi(question: string): Promise<string> {
    if (!USE_BACKEND) {
      return `关于「${question}」：建议使用 STAR 结构（情境-任务-行动-结果）组织回答，先抛结论再展开细节，并保持与岗位 JD 的强关联。如需针对具体题目，可在模拟面试中练习。`
    }
    const res = await request<{ answer: string }>('/qa', { method: 'POST', body: JSON.stringify({ question }) })
    return res.answer
  }
}

// 本地 mock 点评生成（无后端时使用）
function mockAnswer(question: string, answer: string): AnswerRecord {
  const len = answer.trim().length
  let score = 60 + Math.min(30, Math.floor(len / 12))
  if (/然后|那个|就是说|嗯/.test(answer)) score -= 6
  score = Math.max(40, Math.min(95, score))
  const grade = score >= 85 ? 'A' : score >= 75 ? 'B' : score >= 65 ? 'C' : 'D'
  return {
    id: 'a' + Date.now(),
    questionId: 'q',
    question,
    answer,
    score,
    grade,
    isWeak: score < 70,
    comment:
      score >= 80
        ? '回答结构清晰，要点完整，与岗位匹配度高。'
        : score >= 70
        ? '整体尚可，但部分要点展开不足，建议补充量化结果。'
        : '回答偏简略，缺少结构化组织，建议用 STAR 法重新梳理。',
    suggestion: '使用 STAR 结构，先给结论再展开，并补充可量化的成果数据。',
    referenceAnswer: '（示例）结合岗位要求，用 STAR 法组织：情境→任务→行动→结果(量化)。',
    template: 'STAR：情境 → 任务 → 行动 → 结果'
  }
}

export default api
