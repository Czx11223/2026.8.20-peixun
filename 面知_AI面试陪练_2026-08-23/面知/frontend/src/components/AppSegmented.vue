<script setup lang="ts" generic="T extends string">
defineProps<{ modelValue: T; options: { value: T; label: string }[] }>()
const emit = defineEmits<{ 'update:modelValue': [T] }>()
</script>

<template>
  <div class="inline-flex bg-active rounded-md p-0.5">
    <button
      v-for="opt in options"
      :key="opt.value"
      type="button"
      class="h-8 px-3.5 rounded-md text-[13px] text-ink-secondary transition-all duration-200"
      :class="modelValue === opt.value ? 'bg-card text-ink-primary font-semibold border border-line' : ''"
      @click="emit('update:modelValue', opt.value)"
    >
      {{ opt.label }}
    </button>
  </div>
</template>
