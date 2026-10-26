<script setup lang="ts">
import { useRoute } from 'vue-router'

// 唯一权威导航模型（修复测试 T-02：统一 5 项功能导航，首页涵盖「模拟面试+题库」）
const navItems = [
  { to: '/', label: '模拟面试', icon: 'M8 9l4-4 4 4M8 15l4 4 4-4' },
  { to: '/report', label: '面试报告', icon: 'M9 17v-6M12 17v-10M15 17v-4' },
  { to: '/dashboard', label: '能力看板', icon: 'M4 19V5M4 19h16M4 12l4-4 3 3 5-6 4 4' },
  { to: '/settings', label: '模型设置', icon: 'M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z' },
  { to: '/help', label: '帮助', icon: 'M9.1 9a3 3 0 1 1 4.5 2.6c-.8.4-1.6.9-1.6 1.9M12 17h.01' }
]
const route = useRoute()
</script>

<template>
  <header class="sticky top-0 z-40 h-14 bg-card border-b border-line flex items-center gap-6 px-6">
    <RouterLink to="/" class="flex items-center gap-2 text-[18px] font-semibold text-ink-primary shrink-0">
      <svg class="w-6 h-6 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M12 3v3M12 18v3M3 12h3M18 12h3" /><circle cx="12" cy="12" r="6" />
      </svg>
      <span>面知</span>
    </RouterLink>

    <nav class="hidden md:flex items-center gap-1 flex-1 overflow-x-auto">
      <RouterLink
        v-for="item in navItems" :key="item.to"
        :to="item.to"
        class="px-3.5 py-2 rounded-md text-body transition-all duration-200"
        :class="route.path === item.to || (item.to !== '/' && route.path.startsWith(item.to))
          ? 'bg-primary-light text-primary font-semibold'
          : 'text-ink-secondary hover:bg-hover hover:text-ink-primary'"
      >
        {{ item.label }}
      </RouterLink>
    </nav>

    <div class="flex items-center gap-3 ml-auto md:ml-0">
      <button class="text-ink-secondary hover:text-ink-primary" aria-label="通知">
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M10.3 21a1.94 1.94 0 0 0 3.4 0" />
        </svg>
      </button>
      <div class="w-8 h-8 rounded-full bg-primary-light text-primary flex items-center justify-center text-[13px] font-semibold">L</div>
    </div>
  </header>
</template>
