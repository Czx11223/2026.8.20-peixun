<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import type { InterviewReport } from '@/types'
import AppCard from '@/components/AppCard.vue'
import AppButton from '@/components/AppButton.vue'
import AppTag from '@/components/AppTag.vue'
import AppProgress from '@/components/AppProgress.vue'
import AppScoreRing from '@/components/AppScoreRing.vue'
import AppScoreGrade from '@/components/AppScoreGrade.vue'

const route = useRoute()
const router = useRouter()
const report = ref<InterviewReport | null>(null)
const onlyWeak = ref(false)
const expanded = ref<string | null>(null)
const error = ref('')

const list = computed(() =>
  (report.value?.answers ?? []).filter((a) => !onlyWeak.value || a.isWeak)
)

function fmt(sec: number) {
  const m = Math.floor(sec / 60)
  return `${m} 分 ${sec % 60} 秒`
}

async function exportPdf() {
  // 真实环境：GET /report/{id}/pdf 下载；演示环境调用浏览器打印
  if ((import.meta as any).env?.VITE_USE_BACKEND) {
    window.open(`/api/report/${report.value?.id}/pdf`, '_blank')
  } else {
    window.print()
  }
}

// 返回：从能力看板进入时回到看板，其余场景回岗位广场
function goBack() {
  if (route.query.from === 'dashboard') router.push('/dashboard')
  else router.push('/')
}

async function load() {
  report.value = null
  error.value = ''
  try {
    const id = (route.params.id as string) || ''
    // 无 id（直接访问 /report）：展示最近一次面试的真实报告
    report.value = id ? await api.getReport(id) : await api.getRecentReport()
  } catch (e) {
    error.value = '报告加载失败，请检查网络或后端服务后重试'
  }
}

// 路由 id 变化时自动重新加载（同一组件实例复用场景）
watch(() => route.params.id, load, { immediate: true })
</script>

<template>
  <div v-if="report">
    <!-- 返回（从能力看板进入显示「返回能力看板」，其余回岗位广场） -->
    <div class="mb-4">
      <AppButton variant="ghost" size="sm" @click="goBack">
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 12H5M11 18l-6-6 6-6" /></svg>
        {{ route.query.from === 'dashboard' ? '返回能力看板' : '返回' }}
      </AppButton>
    </div>

    <!-- 上方：总分 / 评级 / 综合评价 -->
    <div class="grid grid-cols-1 lg:grid-cols-[auto_1fr] gap-6 mb-6">
      <AppCard class="flex items-center gap-6">
        <AppScoreRing :score="report.totalScore" :grade="report.grade" :size="140" />
        <div>
          <h1 class="text-h1 text-ink-primary">{{ report.jobName }}</h1>
          <div class="flex items-center gap-2 mt-2">
            <AppTag :tone="report.mode === 'pressure' ? 'danger' : 'default'">{{ report.mode === 'pressure' ? '压力面' : '普通面' }}</AppTag>
            <span class="text-caption text-ink-secondary">{{ report.date }}</span>
            <span class="text-caption text-ink-secondary">· 用时 {{ fmt(report.durationSec) }}</span>
          </div>
        </div>
      </AppCard>

      <AppCard title="综合评价">
        <p class="text-body text-ink-primary leading-relaxed">{{ report.summary }}</p>
        <div class="mt-4 space-y-2">
          <div v-for="d in report.dimensions" :key="d.name" class="flex items-center gap-3">
            <span class="text-caption text-ink-secondary w-20 shrink-0">{{ d.name }}</span>
            <AppProgress :value="d.score" class="flex-1" />
            <span class="text-caption text-ink-primary tabular-nums w-8 text-right">{{ d.score }}</span>
          </div>
        </div>
      </AppCard>
    </div>

    <!-- 下方：答题记录 / 错题回看 -->
    <AppCard>
      <template #extra>
        <div class="flex items-center gap-2">
          <AppButton variant="secondary" size="sm" @click="onlyWeak = !onlyWeak">{{ onlyWeak ? '显示全部' : '只看错题' }}</AppButton>
          <AppButton variant="ghost" size="sm" @click="exportPdf">导出 PDF</AppButton>
          <AppButton variant="primary" size="sm" @click="router.push('/')">再次面试</AppButton>
        </div>
      </template>

      <div class="space-y-3">
        <article
          v-for="(a, i) in list" :key="a.id"
          class="border border-line rounded-md overflow-hidden"
          :class="a.isWeak ? 'border-l-4 border-l-danger' : ''"
        >
          <button class="w-full flex items-center gap-3 p-4 text-left hover:bg-hover transition-colors" @click="expanded = expanded === a.id ? null : a.id">
            <span class="text-caption text-ink-tertiary w-8 shrink-0">Q{{ i + 1 }}</span>
            <span class="flex-1 min-w-0 truncate text-body text-ink-primary">{{ a.question }}</span>
            <AppTag v-if="a.isWeak" tone="danger" class="shrink-0">薄弱</AppTag>
            <AppScoreGrade :grade="a.grade" size="sm" class="shrink-0" />
            <svg class="w-4 h-4 text-ink-tertiary shrink-0 transition-transform" :class="expanded === a.id ? 'rotate-180' : ''" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 9l6 6 6-6" /></svg>
          </button>

          <div v-if="expanded === a.id" class="px-4 pb-4 space-y-3 border-t border-line pt-3">
            <div>
              <p class="text-caption text-ink-tertiary mb-1">你的回答</p>
              <p class="text-body text-ink-primary">{{ a.answer }}</p>
            </div>
            <div>
              <p class="text-caption text-ink-tertiary mb-1">AI 完整点评</p>
              <p class="text-body text-ink-primary">{{ a.comment }}</p>
            </div>
            <div class="bg-analysis-light border border-analysis rounded-md p-3">
              <p class="text-caption text-analysis font-semibold mb-1">优化建议</p>
              <p class="text-body text-ink-primary">{{ a.suggestion }}</p>
            </div>
            <div class="bg-subject-light border border-subject rounded-md p-3">
              <p class="text-caption text-subject font-semibold mb-1">标准答案参考</p>
              <p class="text-body text-ink-primary">{{ a.referenceAnswer }}</p>
              <p class="text-caption text-subject mt-2">推荐模板：{{ a.template }}</p>
            </div>
          </div>
        </article>

        <p v-if="!list.length" class="text-center py-8 text-ink-tertiary text-body">没有薄弱题目，表现很棒！</p>
      </div>
    </AppCard>
  </div>
  <div v-else-if="error" class="text-center py-20">
    <p class="text-body text-danger">{{ error }}</p>
    <AppButton variant="secondary" size="sm" class="mt-4" @click="load">重试</AppButton>
  </div>
  <div v-else class="text-center py-20 text-ink-tertiary">报告加载中…</div>
</template>
