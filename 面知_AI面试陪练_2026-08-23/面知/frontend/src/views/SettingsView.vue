<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import type { ModelSettings } from '@/types'
import AppCard from '@/components/AppCard.vue'
import AppButton from '@/components/AppButton.vue'
import AppTag from '@/components/AppTag.vue'

const form = ref<ModelSettings>({
  modelName: 'deepseek-chat',
  apiKey: '',
  baseUrl: 'https://api.deepseek.com/v1',
  temperature: 0.7,
  maxTokens: 2048
})
const saved = ref(false)
const testing = ref(false)
const testResult = ref<'' | 'ok' | 'fail'>('')

onMounted(async () => { form.value = await api.getSettings() })

async function save() {
  await api.saveSettings(form.value)
  saved.value = true
  setTimeout(() => (saved.value = false), 2000)
}

async function test() {
  testing.value = true
  testResult.value = ''
  await new Promise((r) => setTimeout(r, 800))
  testing.value = false
  testResult.value = form.value.apiKey ? 'ok' : 'fail'
}
</script>

<template>
  <div class="max-w-2xl">
    <div class="mb-6">
      <h1 class="text-h1 text-ink-primary">模型设置</h1>
      <p class="text-body text-ink-secondary mt-1.5">配置用于 AI 点评与出题的大模型 API。密钥仅保存在本地浏览器，不会上传至第三方。</p>
    </div>

    <AppCard title="大模型 API 配置">
      <div class="space-y-5">
        <div class="flex flex-col gap-1.5">
          <label class="text-caption text-ink-secondary">模型名称</label>
          <select v-model="form.modelName" class="h-11 px-3 bg-card border border-line rounded-md text-body text-ink-primary">
            <option value="deepseek-chat">DeepSeek Chat</option>
            <option value="deepseek-reasoner">DeepSeek Reasoner</option>
            <option value="gpt-4o-mini">GPT-4o-mini</option>
          </select>
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-caption text-ink-secondary">API 密钥</label>
          <input v-model="form.apiKey" type="password" placeholder="sk-xxxxxxxxxxxxxxxx" class="h-11 px-3 bg-card border border-line rounded-md text-body text-ink-primary" />
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-caption text-ink-secondary">Base URL</label>
          <input v-model="form.baseUrl" placeholder="https://api.deepseek.com/v1" class="h-11 px-3 bg-card border border-line rounded-md text-body text-ink-primary" />
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-caption text-ink-secondary flex justify-between">
            <span>温度 (Temperature)</span><span class="text-ink-primary tabular-nums">{{ form.temperature }}</span>
          </label>
          <input v-model.number="form.temperature" type="range" min="0" max="1" step="0.1" class="w-full accent-[#007AFF]" />
          <p class="text-caption text-ink-tertiary">越低越稳定保守，越高越发散有创意。点评建议 0.3–0.7。</p>
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-caption text-ink-secondary">最大 Token 数</label>
          <input v-model.number="form.maxTokens" type="number" min="256" max="8192" step="256" class="h-11 px-3 bg-card border border-line rounded-md text-body text-ink-primary" />
        </div>
      </div>

      <div class="flex items-center gap-3 mt-6">
        <AppButton variant="primary" @click="save">保存设置</AppButton>
        <AppButton variant="secondary" :disabled="testing" @click="test">{{ testing ? '测试中…' : '连接测试' }}</AppButton>
        <AppTag v-if="saved" tone="success">已保存</AppTag>
        <AppTag v-if="testResult === 'ok'" tone="success">连接正常</AppTag>
        <AppTag v-if="testResult === 'fail'" tone="warning">请先填写密钥</AppTag>
      </div>
    </AppCard>

    <AppCard title="语音识别 (ASR)" class="mt-4">
      <p class="text-body text-ink-secondary">语音答题依赖浏览器内置语音识别或后端 ASR SDK。当前演示模式使用内置模拟转写，部署时可在后端接入语音转文字服务。</p>
    </AppCard>
  </div>
</template>
