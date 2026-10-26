<script setup lang="ts">
defineProps<{
  groups: { label?: string; items: { key: string; label: string; icon: string; active?: boolean }[] }[]
}>()
const emit = defineEmits<{ select: [string] }>()
</script>

<template>
  <!-- 修复测试 T-03：平板(768-1024)折叠为 64px 图标栏并隐藏文字，避免文字裁切；≥1024 展开 240px -->
  <aside class="hidden md:block w-16 lg:w-60 shrink-0 bg-card border-r border-line py-5 px-3 lg:px-3 sticky top-14 h-[calc(100vh-56px)] overflow-y-auto">
    <div v-for="(g, gi) in groups" :key="gi" class="mb-2">
      <p v-if="g.label" class="hidden lg:block text-caption text-ink-tertiary px-3 pt-3 pb-1.5">{{ g.label }}</p>
      <button
        v-for="item in g.items" :key="item.key"
        type="button"
        class="w-full flex items-center gap-2.5 lg:gap-3 px-3 py-2.5 rounded-md text-body transition-all duration-200 justify-center lg:justify-start"
        :class="item.active
          ? 'bg-primary-light text-primary font-semibold'
          : 'text-ink-secondary hover:bg-hover hover:text-ink-primary'"
        :title="item.label"
        @click="emit('select', item.key)"
      >
        <svg class="w-[18px] h-[18px] shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path :d="item.icon" />
        </svg>
        <span class="hidden lg:inline">{{ item.label }}</span>
      </button>
    </div>
  </aside>
</template>
