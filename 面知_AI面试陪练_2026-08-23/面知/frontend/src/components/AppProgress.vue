<script setup lang="ts">
defineProps<{ value: number; tone?: 'primary' | 'success' | 'warning' | 'danger' }>()
</script>

<template>
  <div class="h-1.5 bg-active rounded-full overflow-hidden">
    <div
      class="h-full rounded-full transition-all duration-500"
      :class="{
        'bg-primary': !tone || tone === 'primary',
        'bg-success': tone === 'success',
        'bg-warning': tone === 'warning',
        'bg-danger': tone === 'danger'
      }"
      :style="{ width: Math.min(100, Math.max(0, value)) + '%' }"
    />
  </div>
</template>
