<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'text'
  size?: 'lg' | 'md' | 'sm'
  disabled?: boolean
  block?: boolean
}>()
</script>

<template>
  <button
    class="inline-flex items-center justify-center gap-2 rounded-md font-normal transition-all duration-200 select-none disabled:opacity-40 disabled:cursor-not-allowed"
    :class="[
      size === 'lg' ? 'h-11 px-6 text-base font-semibold' : '',
      size === 'md' ? 'h-9 px-4 text-body' : '',
      size === 'sm' ? 'h-7 px-3 text-caption' : '',
      block ? 'w-full' : '',
      variant === 'primary' ? 'bg-primary text-ink-inverse hover:bg-primary-hover' : '',
      variant === 'secondary' ? 'bg-card border border-line text-ink-primary hover:bg-hover hover:border-line-hover' : '',
      variant === 'ghost' ? 'bg-transparent text-primary hover:bg-primary-lighter' : '',
      variant === 'danger' ? 'bg-danger text-ink-inverse hover:opacity-90' : '',
      variant === 'text' ? 'bg-transparent text-primary px-1 h-auto' : ''
    ]"
  >
    <slot />
  </button>
</template>
