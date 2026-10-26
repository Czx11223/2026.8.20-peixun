<script setup lang="ts">
defineProps<{ tone?: 'default' | 'subject' | 'analysis' | 'success' | 'warning' | 'danger' }>()
</script>

<template>
  <span
    class="inline-flex items-center h-[22px] px-2 rounded-sm text-caption"
    :class="{
      'bg-page border border-line text-ink-secondary': tone === 'default' || !tone,
      'text-subject bg-subject-light border border-subject': tone === 'subject',
      'text-analysis bg-analysis-light border border-analysis': tone === 'analysis',
      'bg-success-light text-success': tone === 'success',
      'bg-warning-light text-warning': tone === 'warning',
      'bg-danger-light text-danger': tone === 'danger'
    }"
  >
    <slot />
  </span>
</template>
