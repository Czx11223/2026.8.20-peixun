<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import type { DashboardStat } from '@/types'
import AppCard from '@/components/AppCard.vue'
import AppButton from '@/components/AppButton.vue'
import AppLineChart from '@/components/AppLineChart.vue'
import AppRadarChart from '@/components/AppRadarChart.vue'
import AppScoreGrade from '@/components/AppScoreGrade.vue'

const router = useRouter()
const stat = ref<DashboardStat | null>(null)
const error = ref('')

const series = computed(() => [
  { name: '综合', color: '#007AFF', data: stat.value?.trend.map((t) => t.total) ?? [] },
  { name: '表达', color: '#34C759', data: stat.value?.trend.map((t) => t.expression) ?? [] },
  { name: '逻辑', color: '#FF9500', data: stat.value?.trend.map((t) => t.logic) ?? [] }
])
const labels = computed(() => stat.value?.trend.map((t) => t.date) ?? [])

function fmtMin(m: number) {
  const h = Math.floor(m / 60)
  return h ? `${h} 小时 ${m % 60} 分` : `${m} 分钟`
}
function fmtDur(sec: number) {
  const m = Math.floor(sec / 60)
  const s = sec % 60
  return s ? `${m} 分 ${s} 秒` : `${m} 分`
}

async function load() {
  stat.value = null
  error.value = ''
  try {
    stat.value = await api.getDashboard()
  } catch (e) {
    error.value = '数据加载失败，请检查网络或后端服务后重试'
  }
}

onMounted(load)
</script>

<template>
  <div v-if="stat">
    <div class="mb-6">
      <h1 class="text-h1 text-ink-primary">能力看板</h1>
      <p class="text-body text-ink-secondary mt-1.5">追踪你的面试能力成长曲线，定位薄弱项，针对性提升。</p>
    </div>

    <!-- 顶部指标 -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <AppCard>
        <p class="text-caption text-ink-secondary">面试总场次</p>
        <p class="text-h1 font-semibold text-ink-primary mt-2 tabular-nums">{{ stat.totalSessions }}</p>
      </AppCard>
      <AppCard>
        <p class="text-caption text-ink-secondary">平均得分</p>
        <p class="text-h1 font-semibold text-ink-primary mt-2 tabular-nums">{{ stat.avgScore }}</p>
      </AppCard>
      <AppCard>
        <p class="text-caption text-ink-secondary">薄弱能力项</p>
        <p class="text-h2 font-semibold text-warning mt-2">{{ stat.weakDimension }}</p>
      </AppCard>
      <AppCard>
        <p class="text-caption text-ink-secondary">练习总时长</p>
        <p class="text-h2 font-semibold text-ink-primary mt-2">{{ fmtMin(stat.totalPracticeMin) }}</p>
      </AppCard>
    </div>

    <!-- 图表区 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
      <AppCard title="面试能力成长曲线">
        <AppLineChart :labels="labels" :series="series" :height="220" />
      </AppCard>
      <AppCard title="各维度能力雷达">
        <AppRadarChart v-if="stat.dimensions.length" :dimensions="stat.dimensions" :size="240" />
        <p v-else class="text-center text-caption text-ink-tertiary py-10">暂无能力维度数据，完成一次面试后生成</p>
      </AppCard>
    </div>

    <!-- 历史汇总 -->
    <AppCard title="历史面试汇总">
      <div class="overflow-x-auto">
        <table class="w-full text-body">
          <thead>
            <tr class="text-caption text-ink-secondary text-left border-b border-line">
              <th class="py-2 pr-4 font-normal">日期</th>
              <th class="py-2 pr-4 font-normal">岗位</th>
              <th class="py-2 pr-4 font-normal">模式</th>
              <th class="py-2 pr-4 font-normal">得分</th>
              <th class="py-2 pr-4 font-normal">等级</th>
              <th class="py-2 pr-4 font-normal">用时</th>
              <th class="py-2 font-normal">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="h in stat.history" :key="h.id" class="border-b border-line last:border-0">
              <td class="py-3 pr-4 text-ink-secondary">{{ h.date }}</td>
              <td class="py-3 pr-4 text-ink-primary">{{ h.jobName }}</td>
              <td class="py-3 pr-4"><span class="text-caption" :class="h.mode === 'pressure' ? 'text-danger' : 'text-ink-secondary'">{{ h.mode === 'pressure' ? '压力面' : '普通面' }}</span></td>
              <td class="py-3 pr-4 text-ink-primary tabular-nums">{{ h.score }}</td>
              <td class="py-3 pr-4"><AppScoreGrade :grade="h.grade" size="sm" /></td>
              <td class="py-3 pr-4 text-ink-secondary">{{ fmtDur(h.durationSec) }}</td>
              <td class="py-3">
                <AppButton variant="ghost" size="sm" @click="router.push(`/report/${h.id}?from=dashboard`)">查看报告</AppButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </AppCard>
  </div>
  <div v-else-if="error" class="text-center py-20">
    <p class="text-body text-danger">{{ error }}</p>
    <AppButton variant="secondary" size="sm" class="mt-4" @click="load">重试</AppButton>
  </div>
  <div v-else class="text-center py-20 text-ink-tertiary">看板加载中…</div>
</template>
