<script setup lang="ts">
defineProps<{ title?: string; desc?: string }>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <svg class="w-12 h-12 text-ink-tertiary mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <path d="M8 9h8M8 13h5" />
    </svg>
    <p class="text-body text-ink-secondary">{{ title ?? '暂无数据' }}</p>
    <p v-if="desc" class="text-caption text-ink-tertiary mt-1">{{ desc }}</p>
    <slot />
  </div>
</template>
