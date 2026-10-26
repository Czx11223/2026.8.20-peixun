<script setup lang="ts">
import { computed } from 'vue'
import type { Grade } from '@/types'

const props = defineProps<{ score: number; grade?: Grade; size?: number }>()
const size = computed(() => props.size ?? 120)
const stroke = 10
const r = computed(() => (size.value - stroke) / 2)
const c = computed(() => 2 * Math.PI * r.value)
const offset = computed(() => c.value * (1 - Math.min(100, Math.max(0, props.score)) / 100))
const color = computed(() => {
  const g = props.grade
  if (g === 'S' || g === 'A') return 'var(--success)'
  if (g === 'B') return 'var(--warning)'
  return 'var(--danger)'
})
</script>

<template>
  <div class="relative inline-flex items-center justify-center" :style="{ width: size + 'px', height: size + 'px' }">
    <svg :width="size" :height="size" class="-rotate-90">
      <circle :cx="size / 2" :cy="size / 2" :r="r" fill="none" stroke="var(--active)" :stroke-width="stroke" />
      <circle
        :cx="size / 2" :cy="size / 2" :r="r" fill="none" :stroke="color" :stroke-width="stroke"
        stroke-linecap="round" :stroke-dasharray="c" :stroke-dashoffset="offset"
        style="transition: stroke-dashoffset .6s ease"
      />
    </svg>
    <div class="absolute flex flex-col items-center">
      <span class="text-h1 font-semibold text-ink-primary tabular-nums">{{ score }}</span>
      <span v-if="grade" class="text-caption font-semibold" :class="{
        'text-success': grade === 'S' || grade === 'A',
        'text-warning': grade === 'B',
        'text-danger': grade === 'C' || grade === 'D'
      }">{{ grade }} 级</span>
    </div>
  </div>
</template>
