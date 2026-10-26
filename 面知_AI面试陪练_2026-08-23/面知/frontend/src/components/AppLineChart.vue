<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  labels: string[]
  series: { name: string; color: string; data: number[] }[]
  max?: number
  height?: number
}>()

const W = 520
const H = computed(() => props.height ?? 220)
const padL = 32, padR = 12, padT = 16, padB = 28
const max = computed(() => props.max ?? 100)
const innerW = computed(() => W - padL - padR)
const innerH = computed(() => H.value - padT - padB)

const xAt = (i: number) =>
  padL + (props.labels.length <= 1 ? 0 : (innerW.value * i) / (props.labels.length - 1))
const yAt = (v: number) => padT + innerH.value * (1 - v / max.value)

const paths = computed(() =>
  props.series.map((s) => ({
    name: s.name,
    color: s.color,
    d: s.data.map((v, i) => `${i === 0 ? 'M' : 'L'}${xAt(i)},${yAt(v)}`).join(' ')
  }))
)
const gridY = computed(() => [0, 25, 50, 75, 100].filter((g) => g <= max.value))
</script>

<template>
  <div class="w-full overflow-x-auto">
    <svg :viewBox="`0 0 ${W} ${H}`" class="w-full min-w-[480px]" preserveAspectRatio="xMidYMid meet">
      <!-- 网格 -->
      <line v-for="g in gridY" :key="'g' + g" :x1="padL" :x2="W - padR" :y1="yAt(g)" :y2="yAt(g)" stroke="var(--border)" stroke-width="1" />
      <text v-for="g in gridY" :key="'t' + g" :x="padL - 6" :y="yAt(g) + 4" text-anchor="end" font-size="10" fill="var(--text-tertiary)">{{ g }}</text>
      <!-- 折线 -->
      <path v-for="p in paths" :key="p.name" :d="p.d" fill="none" :stroke="p.color" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
      <circle v-for="(v, i) in (series[0]?.data ?? [])" :key="'c' + i" :cx="xAt(i)" :cy="yAt(v)" r="2.5" :fill="series[0].color" />
      <!-- X 标签 -->
      <text v-for="(lb, i) in labels" :key="'x' + i" :x="xAt(i)" :y="H - 8" text-anchor="middle" font-size="10" fill="var(--text-tertiary)">{{ lb }}</text>
    </svg>
    <div class="flex gap-4 mt-2 justify-center">
      <span v-for="s in series" :key="'lg' + s.name" class="inline-flex items-center gap-1.5 text-caption text-ink-secondary">
        <i class="w-2.5 h-2.5 rounded-full" :style="{ background: s.color }" />{{ s.name }}
      </span>
    </div>
  </div>
</template>
