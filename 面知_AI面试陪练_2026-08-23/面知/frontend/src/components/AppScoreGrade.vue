<script setup lang="ts">
import type { Grade } from '@/types'
defineProps<{ grade: Grade; size?: 'sm' | 'md' | 'lg' }>()
</script>

<template>
  <span
    class="inline-flex items-center justify-center rounded-sm font-semibold"
    :class="[
      size === 'lg' ? 'w-12 h-12 text-h2' : size === 'sm' ? 'w-7 h-7 text-caption' : 'w-9 h-9 text-body',
      (grade === 'S' || grade === 'A') ? 'bg-success-light text-success' : '',
      grade === 'B' ? 'bg-warning-light text-warning' : '',
      (grade === 'C' || grade === 'D') ? 'bg-danger-light text-danger' : ''
    ]"
  >
    {{ grade }}
  </span>
</template>
