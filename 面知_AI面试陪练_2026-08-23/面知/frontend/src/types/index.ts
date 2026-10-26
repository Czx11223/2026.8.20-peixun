// 面知 全局类型定义

export type Grade = 'S' | 'A' | 'B' | 'C' | 'D'
export type InterviewMode = 'normal' | 'pressure'
export type AnswerMode = 'text' | 'voice'
export type Industry = '互联网' | '国企' | '外企' | '文职' | '制造业' | '快消' | '医药'

export interface QuestionItem {
  id: string
  title: string
  type: string // 行为面试 STAR / 技术深挖 / 开放题 ...
  difficulty: '简单' | '中等' | '困难'
  industry: Industry
  company?: string // 题目来源企业（如 字节跳动/腾讯），校招通用题为空
  referenceAnswer: string
  template: string // 结构化答题模板
}

export interface JobConfig {
  id: string
  name: string // 岗位名称
  company: string // 所属企业（如 腾讯/华为），用于企业岗位
  industry: Industry // 所属行业
  duration: number // 面试时长(分钟)
  questionTypes: string[] // 题型范围
  answerMode: AnswerMode // 语音/文字
  mode: InterviewMode
  totalQuestions: number
}

export interface AnswerRecord {
  id: string
  questionId: string
  question: string
  answer: string
  score: number // 0-100
  grade: Grade
  isWeak: boolean // 是否薄弱/错题
  comment: string // AI 点评
  suggestion: string // 优化建议
  referenceAnswer: string
  template: string
}

export interface InterviewReport {
  id: string
  jobName: string
  mode: InterviewMode
  date: string
  totalScore: number
  grade: Grade
  durationSec: number
  summary: string
  dimensions: { name: string; score: number }[] // 各维度得分
  answers: AnswerRecord[]
}

export interface GrowthPoint {
  date: string
  total: number
  expression: number
  logic: number
}

export interface InterviewHistory {
  id: string
  date: string
  jobName: string
  mode: InterviewMode
  score: number
  grade: Grade
  durationSec: number
}

export interface DashboardStat {
  totalSessions: number
  avgScore: number
  weakDimension: string
  totalPracticeMin: number
  trend: GrowthPoint[]
  dimensions: { name: string; score: number }[]
  history: InterviewHistory[]
}

export interface ModelSettings {
  modelName: string
  apiKey: string
  baseUrl: string
  temperature: number
  maxTokens: number
}
