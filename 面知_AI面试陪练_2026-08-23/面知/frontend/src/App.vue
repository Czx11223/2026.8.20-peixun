<script setup lang="ts">
import AppTopBar from '@/components/AppTopBar.vue'
import AppBottomNav from '@/components/AppBottomNav.vue'
</script>

<template>
  <div class="min-h-screen bg-page flex flex-col">
    <AppTopBar />
    <main class="flex-1 w-full max-w-contentWide mx-auto px-6 md:px-8 py-8 pb-24 md:pb-8">
      <RouterView />
    </main>
    <AppBottomNav />
  </div>
</template>
