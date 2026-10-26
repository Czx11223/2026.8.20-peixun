<script setup lang="ts">
defineProps<{ title?: string; extra?: string }>()
</script>

<template>
  <section class="bg-card border border-line rounded-lg overflow-hidden">
    <header v-if="title || $slots.extra || extra" class="flex items-center justify-between px-5 py-4 border-b border-line">
      <h3 class="text-h3 text-ink-primary">{{ title }}</h3>
      <span class="text-caption text-ink-secondary"><slot name="extra">{{ extra }}</slot></span>
    </header>
    <div class="p-5">
      <slot />
    </div>
  </section>
</template>
