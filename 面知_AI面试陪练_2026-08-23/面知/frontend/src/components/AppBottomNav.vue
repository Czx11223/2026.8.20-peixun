<script setup lang="ts">
import { useRoute } from 'vue-router'

// 移动端底部导航（修复测试 T-01：覆盖全部 5 个页面，含能力看板与帮助，避免移动端不可达）
const items = [
  { to: '/', label: '面试', icon: 'M8 9l4-4 4 4M8 15l4 4 4-4' },
  { to: '/report', label: '报告', icon: 'M9 17v-6M12 17v-10M15 17v-4' },
  { to: '/dashboard', label: '看板', icon: 'M4 19V5M4 19h16M4 12l4-4 3 3 5-6 4 4' },
  { to: '/settings', label: '设置', icon: 'M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z' },
  { to: '/help', label: '帮助', icon: 'M9.1 9a3 3 0 1 1 4.5 2.6c-.8.4-1.6.9-1.6 1.9M12 17h.01' }
]
const route = useRoute()
</script>

<template>
  <nav class="md:hidden fixed bottom-0 left-0 right-0 h-14 bg-card border-t border-line z-50 flex">
    <RouterLink
      v-for="item in items" :key="item.to"
      :to="item.to"
      class="flex-1 flex flex-col items-center justify-center gap-0.5 text-[11px] transition-colors"
      :class="(route.path === item.to || (item.to !== '/' && route.path.startsWith(item.to)))
        ? 'text-primary' : 'text-ink-tertiary'"
    >
      <svg class="w-[22px] h-[22px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path :d="item.icon" />
      </svg>
      <span>{{ item.label }}</span>
    </RouterLink>
  </nav>
</template>
