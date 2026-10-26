<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import type { JobConfig, QuestionItem, AnswerRecord, AnswerMode } from '@/types'
import AppTimer from '@/components/AppTimer.vue'
import AppSegmented from '@/components/AppSegmented.vue'
import AppCard from '@/components/AppCard.vue'
import AppButton from '@/components/AppButton.vue'
import AppTag from '@/components/AppTag.vue'
import AppProgress from '@/components/AppProgress.vue'
import AppScoreGrade from '@/components/AppScoreGrade.vue'

const route = useRoute()
const router = useRouter()

const job = ref<JobConfig | null>(null)
const questions = ref<QuestionItem[]>([])
const interviewId = ref('')
const current = ref(0)
const answerMode = ref<AnswerMode>('text')
// 当前题的编辑内容（切题时从 answersMap 加载/保存，答题框相互独立）
const currentAnswer = ref('')
const recording = ref(false)
const recordingSec = ref(0)
const saving = ref(false) // 自动保存进行中
// 每题已保存的作答+点评（questionId -> 记录），支持回看「上一题」
const answersMap = ref<Record<string, AnswerRecord>>({})
const lastComment = ref<AnswerRecord | null>(null)
const timerRef = ref<InstanceType<typeof AppTimer> | null>(null)
const error = ref('')
const startTime = ref(0) // 面试开始时间戳，用于统计实际练习时长

const q = computed(() => questions.value[current.value])
const isLast = computed(() => current.value === questions.value.length - 1)
const perQuestionSec = computed(() => (job.value ? Math.round((job.value.duration * 60) / Math.max(1, job.value.totalQuestions)) : 120))

// ============ 自动保存（作答即保存 + AI 自动评分） ============
let saveTimer: number | undefined

async function saveCurrent() {
  if (saveTimer) { clearTimeout(saveTimer); saveTimer = undefined }
  const cur = q.value
  if (!cur || !interviewId.value || saving.value) return
  const content = currentAnswer.value.trim()
  if (!content) return // 空作答不保存
  if (answersMap.value[cur.id]?.answer === content) return // 内容未变化不重复保存
  saving.value = true
  try {
    const rec = await api.submitAnswer({
      interviewId: interviewId.value,
      questionId: cur.id,
      answer: content,
      mode: answerMode.value
    })
    answersMap.value[cur.id] = rec
    if (q.value?.id === cur.id) lastComment.value = rec // 保存完成时仍在本题才更新点评，避免串题
  } catch (e: any) {
    if (e?.status === 404) await load() // 会话失效重建
  } finally {
    saving.value = false
  }
}

function scheduleSave() {
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = window.setTimeout(saveCurrent, 1200) // 输入停顿 1.2s 自动保存
}

// 切换题目：同步切换答题框（新题立即清空 / 回显已保存内容，各题独立互不干扰），重置计时器。
// 注意：当前题作答的保存必须在 current 变化之前由 next()/prev() 触发（此刻 q.value 仍是当前题），避免串题。
watch(
  () => current.value,
  () => {
    if (saveTimer) { clearTimeout(saveTimer); saveTimer = undefined }
    const rec = q.value ? answersMap.value[q.value.id] : undefined
    currentAnswer.value = rec?.answer ?? '' // 新题无作答 → 直接清空；已有作答 → 回显
    lastComment.value = rec ?? null
    timerRef.value?.reset()
    timerRef.value?.start()
  }
)

// 实时分析（基于当前作答内容估算；已保存题目展示 AI 评分）
const analysis = computed(() => {
  const text = currentAnswer.value
  const chars = text.replace(/\s/g, '').length
  const speechRate = recording.value ? 138 : Math.min(180, 90 + Math.round(chars / 6))
  const fillers = (text.match(/然后|那个|就是说|嗯|其实/g) || []).length
  return {
    score: lastComment.value?.score ?? Math.max(40, Math.min(95, 55 + Math.floor(chars / 10) - fillers * 3)),
    speechRate,
    rateLevel: speechRate > 160 ? '偏快' : speechRate < 100 ? '偏慢' : '适中',
    fillerCount: fillers,
    template: q.value?.template ?? 'STAR：情境 → 任务 → 行动 → 结果'
  }
})

let recTimer: number | undefined
function toggleRecord() {
  recording.value = !recording.value
  if (recording.value) {
    recordingSec.value = 0
    recTimer = window.setInterval(() => recordingSec.value++, 1000)
  } else {
    if (recTimer) clearInterval(recTimer)
    // 模拟 ASR 结果（真实环境由后端 /asr 返回），转写后立即自动保存并评分
    currentAnswer.value = '我觉得这个岗位挺好的，然后我学过相关技术，然后做过类似项目，就是说比较有经验。'
    saveCurrent()
  }
}

function next() {
  if (isLast.value) return
  saveCurrent() // 先保存当前题（此刻 q.value 仍是当前题），再切换
  current.value++
}

function prev() {
  if (current.value === 0) return
  saveCurrent() // 先保存当前题，再回看上一题
  current.value--
}

async function goBack() {
  // 中途退出：删除会话（含全部作答），不保存为历史记录；删除失败也照常返回
  if (interviewId.value) {
    try {
      await api.cancelInterview(interviewId.value)
    } catch (e) {
      /* 忽略 */
    }
  }
  router.push('/')
}

async function goReport() {
  // 先上报实际练习时长（用于报告「用时」与看板「练习总时长」），再跳转报告页
  if (interviewId.value) {
    const elapsed = Math.max(1, Math.round((Date.now() - startTime.value) / 1000))
    try {
      await api.finishInterview(interviewId.value, elapsed)
    } catch (e) {
      /* 上报失败不阻断跳转 */
    }
  }
  router.push(interviewId.value ? `/report/${interviewId.value}` : '/report')
}

// 最后一题：保存当前作答后完成面试，生成报告
async function complete() {
  if (saveTimer) { clearTimeout(saveTimer); saveTimer = undefined }
  await saveCurrent()
  await goReport()
}

async function load() {
  error.value = ''
  try {
    const jobs = await api.getJobs()
    job.value = jobs.find((j) => j.id === route.params.jobId) || jobs[0]
    answerMode.value = job.value?.answerMode ?? 'text'
    const started = await api.startInterview(job.value!.id)
    interviewId.value = started.interviewId
    questions.value = started.questions
    startTime.value = Date.now() // 面试正式开始计时
  } catch (e) {
    error.value = '面试初始化失败，请检查网络或后端服务后重试'
  }
}

onMounted(load)
</script>

<template>
  <div>
    <div v-if="error" class="mb-6 p-4 rounded-md border border-danger-light bg-danger-light text-danger text-body flex items-center justify-between">
      <span>{{ error }}</span>
      <button class="underline shrink-0 ml-3" @click="load">重试</button>
    </div>
    <!-- 顶部：返回 + 倒计时 + 进度 -->
    <div class="flex items-center justify-between flex-wrap gap-4 mb-6">
      <div class="flex items-center gap-3 min-w-0">
        <AppButton variant="ghost" size="sm" class="shrink-0" @click="goBack" aria-label="返回岗位列表">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 12H5M11 18l-6-6 6-6" /></svg>
          返回
        </AppButton>
        <div class="min-w-0">
          <h1 class="text-h2 text-ink-primary truncate">{{ job?.name }} · {{ job?.mode === 'pressure' ? '压力面' : '普通面' }}模拟</h1>
          <p class="text-caption text-ink-secondary mt-1">第 {{ current + 1 }} / {{ questions.length }} 题</p>
        </div>
      </div>
      <AppTimer ref="timerRef" :duration-sec="perQuestionSec" :auto-start="true" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-[320px_1fr_320px] gap-4">
      <!-- 左：AI 面试官提问 -->
      <AppCard title="AI 面试官">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-full bg-primary-light text-primary flex items-center justify-center font-semibold">AI</div>
          <div>
            <p class="text-body font-semibold text-ink-primary">HR · 小la</p>
            <p class="text-caption text-ink-tertiary">{{ job?.mode === 'pressure' ? '压力面试官' : '模拟面试官' }}</p>
          </div>
        </div>
        <div class="bg-subject-light border border-subject rounded-md p-4 text-body text-ink-primary leading-relaxed">
          {{ q?.title }}
        </div>
        <div class="mt-3 flex gap-2">
          <AppButton variant="ghost" size="sm" @click="prev">上一题</AppButton>
          <!-- 最后一题「下一题」消失；点「上一题」离开末题后恢复显示 -->
          <AppButton v-if="!isLast" variant="ghost" size="sm" @click="next">下一题</AppButton>
        </div>
      </AppCard>

      <!-- 中：作答区（作答自动保存 + AI 自动评分） -->
      <AppCard :title="answerMode === 'voice' ? '语音作答' : '文字作答'">
        <div class="flex items-center justify-between mb-3">
          <AppSegmented v-model="answerMode" :options="[{ value: 'text', label: '文字' }, { value: 'voice', label: '语音' }]" />
          <span class="text-caption text-ink-tertiary">{{ currentAnswer.length }} 字 · {{ saving ? '保存中…' : (currentAnswer.trim() ? '已自动保存' : '') }}</span>
        </div>

        <textarea
          v-if="answerMode === 'text'"
          v-model="currentAnswer"
          @input="scheduleSave"
          @blur="saveCurrent"
          placeholder="在此输入你的回答，建议使用 STAR 结构组织内容（作答将自动保存并评分）…"
          class="w-full min-h-[160px] p-3 bg-card border border-line rounded-md text-body text-ink-primary resize-y leading-relaxed"
        />
        <div v-else class="min-h-[160px] border border-line rounded-md flex flex-col items-center justify-center gap-3 bg-page">
          <div class="flex items-end gap-1 h-12">
            <span v-for="n in 9" :key="n" class="w-1 rounded-full bg-primary transition-all"
              :style="{ height: recording ? (8 + ((n * 7 + recordingSec * 3) % 32)) + 'px' : '8px', opacity: recording ? 1 : 0.3 }" />
          </div>
          <p class="text-caption text-ink-secondary">{{ recording ? `录音中 ${recordingSec}s` : '点击下方按钮开始录音，结束后自动转写并评分' }}</p>
          <AppButton :variant="recording ? 'danger' : 'primary'" size="md" @click="toggleRecord">
            {{ recording ? '停止录音' : '开始录音' }}
          </AppButton>
          <textarea v-if="currentAnswer" v-model="currentAnswer" class="w-11/12 min-h-[60px] p-3 bg-card border border-line rounded-md text-body" />
        </div>

        <div class="flex items-center justify-between mt-4">
          <!-- 非末题：无提交按钮，作答自动保存；末题才出现「完成提交」 -->
          <span class="text-caption text-ink-tertiary">
            {{ isLast ? '最后一题，完成提交后生成面试报告' : '作答自动保存并评分，点击「下一题」继续' }}
          </span>
          <AppButton v-if="isLast" variant="primary" :disabled="saving" @click="complete">
            {{ saving ? '保存中…' : '完成提交' }}
          </AppButton>
        </div>

        <!-- 本题 AI 点评（已保存并评分后展示） -->
        <div v-if="lastComment" class="mt-4 border-t border-line pt-4">
          <div class="flex items-center gap-2 mb-2">
            <AppScoreGrade :grade="lastComment.grade" size="sm" />
            <span class="text-body text-ink-primary font-semibold">{{ lastComment.score }} 分</span>
            <span class="text-caption text-ink-secondary">本题 AI 点评</span>
          </div>
          <p class="text-caption text-ink-secondary">{{ lastComment.comment }}</p>
        </div>
      </AppCard>

      <!-- 右：实时分析面板 -->
      <div class="flex flex-col gap-4">
        <AppCard title="实时得分评级">
          <div class="flex items-center gap-3">
            <AppScoreGrade :grade="analysis.score >= 85 ? 'A' : analysis.score >= 75 ? 'B' : analysis.score >= 65 ? 'C' : 'D'" size="lg" />
            <div>
              <p class="text-h2 font-semibold text-ink-primary tabular-nums">{{ analysis.score }}</p>
              <p class="text-caption text-ink-tertiary">实时综合评分</p>
            </div>
          </div>
          <AppProgress :value="analysis.score" class="mt-3" />
        </AppCard>

        <AppCard title="语速检测">
          <div class="flex items-baseline gap-2">
            <span class="text-h2 font-semibold text-ink-primary tabular-nums">{{ analysis.speechRate }}</span>
            <span class="text-caption text-ink-secondary">字/分钟</span>
            <AppTag :tone="analysis.rateLevel === '适中' ? 'success' : 'warning'" class="ml-auto">{{ analysis.rateLevel }}</AppTag>
          </div>
        </AppCard>

        <AppCard title="口头禅识别">
          <div v-if="analysis.fillerCount" class="flex items-center gap-2">
            <span class="text-body text-ink-primary">检测到口头禅</span>
            <AppTag tone="warning">{{ analysis.fillerCount }} 处</AppTag>
            <span class="text-caption text-ink-tertiary ml-auto">建议精简</span>
          </div>
          <p v-else class="text-caption text-ink-tertiary">暂未检测到明显口头禅，表达干净。</p>
        </AppCard>

        <AppCard title="结构化答题模板">
          <div class="bg-analysis-light border border-analysis rounded-md p-3 text-body text-ink-primary">
            {{ analysis.template }}
          </div>
          <p class="text-caption text-ink-tertiary mt-2">按此模板组织回答，逻辑更清晰、得分更高。</p>
        </AppCard>
      </div>
    </div>
  </div>
</template>
