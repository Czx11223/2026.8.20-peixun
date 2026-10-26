<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ dimensions: { name: string; score: number }[]; size?: number }>()
const size = computed(() => props.size ?? 260)
const cx = size.value / 2
const cy = size.value / 2
const R = size.value / 2 - 36
const n = computed(() => props.dimensions.length)

const angle = (i: number) => (n.value === 0 ? 0 : (Math.PI * 2 * i) / n.value - Math.PI / 2)
const point = (i: number, ratio: number) => {
  const a = angle(i)
  return [cx + R * ratio * Math.cos(a), cy + R * ratio * Math.sin(a)]
}
const axisPoints = computed(() =>
  props.dimensions.map((_, i) => point(i, 1))
)
const dataPolygon = computed(() =>
  props.dimensions.map((d, i) => point(i, Math.min(100, d.score) / 100).join(',')).join(' ')
)
const rings = [0.25, 0.5, 0.75, 1]
</script>

<template>
  <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" class="mx-auto">
    <!-- 网格环 -->
    <polygon
      v-for="ring in rings" :key="ring"
      :points="dimensions.map((_, i) => point(i, ring).join(',')).join(' ')"
      fill="none" stroke="var(--border)" stroke-width="1"
    />
    <!-- 轴线 -->
    <line v-for="(p, i) in axisPoints" :key="'ax' + i" :x1="cx" :y1="cy" :x2="p[0]" :y2="p[1]" stroke="var(--border)" stroke-width="1" />
    <!-- 数据多边形 -->
    <polygon :points="dataPolygon" fill="rgba(0,122,255,0.12)" stroke="var(--primary)" stroke-width="2" />
    <circle v-for="(d, i) in dimensions" :key="'d' + i" :cx="point(i, d.score / 100)[0]" :cy="point(i, d.score / 100)[1]" r="3" fill="var(--primary)" />
    <!-- 标签 -->
    <text
      v-for="(d, i) in dimensions" :key="'lb' + i"
      :x="point(i, 1.18)[0]" :y="point(i, 1.18)[1] + 4"
      text-anchor="middle" font-size="11" fill="var(--text-secondary)"
    >{{ d.name }}</text>
  </svg>
</template>
