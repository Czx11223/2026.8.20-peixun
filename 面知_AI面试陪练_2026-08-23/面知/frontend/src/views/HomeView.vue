<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import type { JobConfig } from '@/types'
import AppSideBar from '@/components/AppSideBar.vue'
import AppCard from '@/components/AppCard.vue'
import AppButton from '@/components/AppButton.vue'
import AppTag from '@/components/AppTag.vue'

const router = useRouter()
const jobs = ref<JobConfig[]>([])
const activeMode = ref<'all' | 'normal' | 'pressure'>('all')
const activeIndustry = ref<string>('all')
const keyword = ref('')
const error = ref('')

const modeNav = computed(() => {
  const cnt = (m: string) => (m === 'all' ? jobs.value.length : jobs.value.filter((j) => j.mode === m).length)
  return {
    label: '面试模式',
    items: [
      { key: 'all', label: `全部模拟 ${cnt('all')}`, icon: 'M4 6h16M4 12h16M4 18h16', active: activeMode.value === 'all' },
      { key: 'normal', label: `普通模拟 ${cnt('normal')}`, icon: 'M8 9l4-4 4 4M8 15l4 4 4-4', active: activeMode.value === 'normal' },
      { key: 'pressure', label: `压力面模拟 ${cnt('pressure')}`, icon: 'M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z', active: activeMode.value === 'pressure' }
    ]
  }
})
const industryNav = computed(() => {
  const cnt = (ind: string) => (ind === 'all' ? jobs.value.length : jobs.value.filter((j) => j.industry === ind).length)
  return {
    label: '岗位题库',
    items: [
      { key: 'industry-all', label: `全部行业 ${cnt('all')}`, icon: 'M3 12h18', active: activeIndustry.value === 'all' },
      { key: '互联网', label: `互联网 ${cnt('互联网')}`, icon: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18', active: activeIndustry.value === '互联网' },
      { key: '国企', label: `国企 ${cnt('国企')}`, icon: 'M4 21V5h16v16', active: activeIndustry.value === '国企' },
      { key: '外企', label: `外企 ${cnt('外企')}`, icon: 'M12 3c3 4 3 14 0 18M12 3c-3 4-3 14 0 18', active: activeIndustry.value === '外企' },
      { key: '文职', label: `文职 ${cnt('文职')}`, icon: 'M5 4h14v16H5z', active: activeIndustry.value === '文职' },
      { key: '制造业', label: `制造业 ${cnt('制造业')}`, icon: 'M4 19V5M4 19h16M4 12l4-4 3 3 5-6 4 4', active: activeIndustry.value === '制造业' },
      { key: '快消', label: `快消 ${cnt('快消')}`, icon: 'M5 4h14v16H5z', active: activeIndustry.value === '快消' },
      { key: '医药', label: `医药 ${cnt('医药')}`, icon: 'M12 21v-6m0-6V3M3 21v-6m18 6v-6', active: activeIndustry.value === '医药' }
    ]
  }
})

const filtered = computed(() =>
  jobs.value.filter((j) => {
    if (activeMode.value !== 'all' && j.mode !== activeMode.value) return false
    if (activeIndustry.value !== 'all' && j.industry !== activeIndustry.value) return false
    if (keyword.value &&
        !j.name.includes(keyword.value) && !j.industry.includes(keyword.value) && !j.company.includes(keyword.value)) return false
    return true
  })
)

function onSelect(key: string) {
  // 修复：行业「全部行业」原 key 为 'all'，与模式 'all' 冲突，点击会误重置面试模式。
  // 现改为 'industry-all'，明确区分两个命名空间。
  if (key === 'industry-all') activeIndustry.value = 'all'
  else if (['all', 'normal', 'pressure'].includes(key)) activeMode.value = key as any
  else activeIndustry.value = key
}

async function load() {
  error.value = ''
  try {
    jobs.value = await api.getJobs()
  } catch (e) {
    error.value = '岗位配置加载失败，请检查网络或后端服务后重试'
  }
}

onMounted(load)
</script>

<template>
  <div class="flex gap-6">
    <AppSideBar :groups="[modeNav, industryNav]" @select="onSelect" />

    <div class="flex-1 min-w-0">
      <div class="mb-6">
        <h1 class="text-h1 text-ink-primary">模拟面试</h1>
        <p class="text-body text-ink-secondary mt-1.5">选择岗位与面试模式，开启全真 AI 模拟面试，实时点评帮你快速提升。</p>
      </div>

      <!-- 操作栏（不再放置全局「开始面试」：它只能启动第一个筛选结果，易误入其他岗位；开始面试以各岗位卡片按钮为准） -->
      <div class="flex flex-wrap items-center gap-3 mb-6">
        <div class="relative flex-1 min-w-[200px]">
          <svg class="w-4 h-4 text-ink-tertiary absolute left-3 top-1/2 -translate-y-1/2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="7" /><path d="M21 21l-4-4" />
          </svg>
          <input v-model="keyword" placeholder="搜索岗位 / 企业 / 行业" class="w-full h-11 pl-9 pr-3 bg-card border border-line rounded-md text-body text-ink-primary" />
        </div>
        <AppButton variant="secondary" @click="router.push('/dashboard')">历史记录</AppButton>
      </div>

      <!-- 移动端筛选（桌面左侧导航在 md 以下隐藏，此处补充分类筛选，保证移动端可达） -->
      <div class="md:hidden flex flex-wrap gap-2 mb-6">
        <select v-model="activeMode" class="h-9 px-3 bg-card border border-line rounded-md text-body text-ink-primary">
          <option value="all">全部模拟</option>
          <option value="normal">普通模拟</option>
          <option value="pressure">压力面模拟</option>
        </select>
        <select v-model="activeIndustry" class="h-9 px-3 bg-card border border-line rounded-md text-body text-ink-primary">
          <option value="all">全部行业</option>
          <option value="互联网">互联网</option>
          <option value="国企">国企</option>
          <option value="外企">外企</option>
          <option value="文职">文职</option>
          <option value="制造业">制造业</option>
        </select>
      </div>

      <!-- 配置卡片列表 -->
      <div v-if="error" class="text-center py-16">
        <p class="text-body text-danger">{{ error }}</p>
        <AppButton variant="secondary" size="sm" class="mt-4" @click="load">重试</AppButton>
      </div>
      <template v-else>
        <div v-if="filtered.length" class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          <AppCard v-for="job in filtered" :key="job.id">
            <div class="flex items-start justify-between gap-2">
              <div>
                <h3 class="text-h3 text-ink-primary">{{ job.name }}</h3>
                <div class="mt-2 flex gap-2 flex-wrap">
                  <AppTag v-if="job.company" tone="analysis">{{ job.company }}</AppTag>
                  <AppTag tone="subject">{{ job.industry }}</AppTag>
                  <AppTag :tone="job.mode === 'pressure' ? 'danger' : 'default'">{{ job.mode === 'pressure' ? '压力面' : '普通面' }}</AppTag>
                  <AppTag>{{ job.answerMode === 'voice' ? '语音答题' : '文字答题' }}</AppTag>
                </div>
              </div>
            </div>

            <dl class="mt-4 space-y-2 text-caption text-ink-secondary">
              <div class="flex justify-between"><dt>面试时长</dt><dd class="text-ink-primary">{{ job.duration }} 分钟</dd></div>
              <div class="flex justify-between"><dt>题目数量</dt><dd class="text-ink-primary">{{ job.totalQuestions }} 题</dd></div>
              <div>
                <dt class="mb-1">题型范围</dt>
                <dd class="flex flex-wrap gap-1.5">
                  <span v-for="t in job.questionTypes" :key="t" class="inline-flex h-[22px] px-2 items-center rounded-sm bg-page border border-line text-caption text-ink-secondary">{{ t }}</span>
                </dd>
              </div>
            </dl>

            <AppButton variant="primary" block class="mt-5" @click="router.push(`/interview/${job.id}`)">开始面试</AppButton>
          </AppCard>
        </div>

        <div v-else class="text-center py-16 text-ink-tertiary text-body">未找到匹配的岗位配置，试试调整筛选条件。</div>
      </template>
    </div>
  </div>
</template>
