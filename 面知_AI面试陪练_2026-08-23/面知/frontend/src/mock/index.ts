import type { JobConfig, QuestionItem, InterviewReport, DashboardStat, InterviewHistory, GrowthPoint } from '@/types'
import { seedJobs, seedQuestions } from './seed_data'

// ============ 岗位配置卡片（由 backend/tools/generate_seed.py 生成，104 个真实企业岗位） ============
export const jobConfigs: JobConfig[] = seedJobs

// ============ 题库（由 backend/tools/generate_seed.py 生成，78 道企业真题） ============
export const questions: QuestionItem[] = seedQuestions

// ============ 面试报告（报告页示例） ============
export const sampleReport: InterviewReport = {
  id: 'iv-20260820-001',
  jobName: 'Java 开发工程师',
  mode: 'normal',
  date: '2026-08-20 10:24',
  totalScore: 78,
  grade: 'B',
  durationSec: 14 * 60 + 32,
  summary:
    '整体表现良好，技术基础扎实，STAR 结构运用到位；逻辑表达清晰，但项目经历量化不足，口头禅偏多影响专业感，建议在表达精炼度上进一步提升。',
  dimensions: [
    { name: '内容完整度', score: 82 },
    { name: '逻辑结构', score: 80 },
    { name: '表达流畅度', score: 71 },
    { name: '岗位匹配度', score: 79 },
    { name: '抗压表现', score: 76 }
  ],
  answers: [
    {
      id: 'a1',
      questionId: 'q1',
      question: '请自我介绍，并说明为什么选择我们这个岗位？',
      answer: '我是 XX 大学计算机专业……然后……我觉得这个岗位挺好的，然后我学过 Java……',
      score: 85,
      grade: 'A',
      isWeak: false,
      comment: '结构清晰，岗位匹配点明确；但"然后"出现 6 次，口语冗余。',
      suggestion: '减少口头禅，用"首先/其次"替代"然后"，提升专业感。',
      referenceAnswer:
        '用 1 分钟概括教育背景与核心经历，再结合岗位 JD 说明匹配点：技术栈契合 + 项目经验 + 长期兴趣。',
      template: '背景 → 经历 → 匹配 → 动机'
    },
    {
      id: 'a2',
      questionId: 'q2',
      question: '说说你遇到过最难的技术问题，是如何解决的？',
      answer: '有一次线上报错……我看了看日志……然后定位到是并发问题。',
      score: 68,
      grade: 'C',
      isWeak: true,
      comment: '缺少量化结果与复盘；排查过程描述笼统，未体现方法论。',
      suggestion: '补充"最终 QPS 从 X 提升到 Y"等量化结果，并说明沉淀的排查 checklist。',
      referenceAnswer:
        '用 STAR 结构：情境 → 任务 → 行动(排查步骤) → 结果(量化收益与复盘)。',
      template: 'STAR：情境 → 任务 → 行动 → 结果'
    },
    {
      id: 'a3',
      questionId: 'q3',
      question: '如果你的方案被领导否定，你会怎么办？',
      answer: '我会先听领导的意见，然后看看哪里不对，再改一改。',
      score: 72,
      grade: 'B',
      isWeak: false,
      comment: '态度积极，但回答过于简略，缺少具体沟通策略。',
      suggestion: '补充"区分信息差与理念差、给出折中方案、执行并复盘"的具体动作。',
      referenceAnswer:
        '先倾听否定原因，区分信息差与理念差；主动沟通澄清目标，给出折中方案。',
      template: '倾听 → 澄清 → 折中 → 执行 → 复盘'
    }
  ]
}

// ============ 能力看板 ============
const trend: GrowthPoint[] = [
  { date: '07-21', total: 62, expression: 60, logic: 64 },
  { date: '07-28', total: 66, expression: 63, logic: 68 },
  { date: '08-04', total: 70, expression: 67, logic: 72 },
  { date: '08-11', total: 73, expression: 70, logic: 75 },
  { date: '08-15', total: 75, expression: 72, logic: 77 },
  { date: '08-20', total: 78, expression: 75, logic: 80 }
]

const history: InterviewHistory[] = [
  { id: 'h1', date: '2026-08-20', jobName: 'Java 开发工程师', mode: 'normal', score: 78, grade: 'B', durationSec: 872 },
  { id: 'h2', date: '2026-08-15', jobName: '产品经理', mode: 'normal', score: 75, grade: 'B', durationSec: 1180 },
  { id: 'h3', date: '2026-08-11', jobName: '国家电网 · 技术岗', mode: 'pressure', score: 73, grade: 'B', durationSec: 1402 },
  { id: 'h4', date: '2026-08-04', jobName: 'Java 开发工程师', mode: 'normal', score: 70, grade: 'C', durationSec: 845 },
  { id: 'h5', date: '2026-07-28', jobName: '人力资源专员', mode: 'normal', score: 66, grade: 'C', durationSec: 760 },
  { id: 'h6', date: '2026-07-21', jobName: 'Java 开发工程师', mode: 'normal', score: 62, grade: 'C', durationSec: 690 }
]

export const dashboardStat: DashboardStat = {
  totalSessions: 12,
  avgScore: 71,
  weakDimension: '表达流畅度',
  totalPracticeMin: 286,
  trend,
  dimensions: [
    { name: '内容完整度', score: 82 },
    { name: '逻辑结构', score: 80 },
    { name: '表达流畅度', score: 71 },
    { name: '岗位匹配度', score: 79 },
    { name: '抗压表现', score: 76 }
  ],
  history
}
