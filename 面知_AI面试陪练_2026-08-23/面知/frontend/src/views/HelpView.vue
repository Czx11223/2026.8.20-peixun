<script setup lang="ts">
import { ref } from 'vue'
import AppCard from '@/components/AppCard.vue'

const faqs = [
  { q: '面知 适合哪些人使用？', a: '主要面向高校应届生，尤其是正在准备校招面试的同学。覆盖互联网、国企、外企、文职、制造业等多行业岗位题库。' },
  { q: '语音答题需要什么环境？', a: '语音答题依赖浏览器麦克风权限与语音识别能力。若环境不支持，可随时切换为文字答题，点评流程完全一致。' },
  { q: 'AI 点评的评分标准是什么？', a: '从内容完整度、逻辑结构、表达流畅度、岗位匹配度、抗压表现五个维度综合评分，并给出 S/A/B/C/D 等级与结构化优化建议。' },
  { q: '我的面试数据安全吗？', a: '演示模式下数据保存在本地浏览器。接入后端后，面试记录与答题内容仅用于生成你的个人报告，可在设置中管理模型与数据。' },
  { q: '如何导出面试报告？', a: '在面试报告页点击「导出 PDF」，系统将生成包含总分、维度分析、逐题点评与优化建议的 PDF 报告，便于复盘与分享。' }
]
const open = ref<number | null>(0)
</script>

<template>
  <div class="max-w-3xl">
    <div class="mb-6">
      <h1 class="text-h1 text-ink-primary">帮助中心</h1>
      <p class="text-body text-ink-secondary mt-1.5">面知 使用手册：从第一次模拟面试到能力持续提升的完整指引。</p>
    </div>

    <AppCard title="快速开始" class="mb-4">
      <ol class="list-decimal list-inside space-y-2 text-body text-ink-primary">
        <li>在「模拟面试」页选择岗位与面试模式（普通 / 压力面）。</li>
        <li>点击「开始面试」，按 AI 面试官提问依次作答（文字或语音）。</li>
        <li>每题提交后获得实时点评与评分，右侧面板显示语速、口头禅与答题模板。</li>
        <li>结束后查看「面试报告」，回看错题、AI 点评与优化建议。</li>
        <li>在「能力看板」追踪成长曲线，定位薄弱项并针对性复练。</li>
      </ol>
    </AppCard>

    <AppCard title="核心功能" class="mb-4">
      <dl class="space-y-3 text-body">
        <div><dt class="font-semibold text-ink-primary">全真模拟面试</dt><dd class="text-ink-secondary mt-1">AI 扮演 HR 一对一连续提问，模拟真实面试节奏与压力场景。</dd></div>
        <div><dt class="font-semibold text-ink-primary">实时 AI 点评</dt><dd class="text-ink-secondary mt-1">作答即时评分，指出问题并给出标准答案与结构化答题模板。</dd></div>
        <div><dt class="font-semibold text-ink-primary">面试报告 & 错题回看</dt><dd class="text-ink-secondary mt-1">保存每次记录，标记薄弱题型，支持重复专项练习。</dd></div>
        <div><dt class="font-semibold text-ink-primary">能力数据看板</dt><dd class="text-ink-secondary mt-1">可视化成长曲线与维度雷达，量化你的面试能力提升。</dd></div>
      </dl>
    </AppCard>

    <AppCard title="常见问题">
      <div class="divide-y divide-line">
        <div v-for="(f, i) in faqs" :key="i" class="py-3">
          <button class="w-full flex items-center justify-between text-left" @click="open = open === i ? null : i">
            <span class="text-body font-semibold text-ink-primary">{{ f.q }}</span>
            <svg class="w-4 h-4 text-ink-tertiary transition-transform" :class="open === i ? 'rotate-180' : ''" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 9l6 6 6-6" /></svg>
          </button>
          <p v-if="open === i" class="text-body text-ink-secondary mt-2">{{ f.a }}</p>
        </div>
      </div>
    </AppCard>
  </div>
</template>
