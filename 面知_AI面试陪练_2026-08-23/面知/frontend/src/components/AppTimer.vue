<script setup lang="ts">
import { ref, onUnmounted, computed, watch } from 'vue'

const props = defineProps<{ durationSec: number; autoStart?: boolean }>()
const emit = defineEmits<{ end: [] }>()

const remaining = ref(props.durationSec)
const running = ref(false)
let timer: number | undefined

const mmss = computed(() => {
  const m = Math.floor(remaining.value / 60)
  const s = remaining.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})
const danger = computed(() => remaining.value <= 60)

function tick() {
  if (remaining.value > 0) {
    remaining.value--
    if (remaining.value === 0) {
      pause()
      emit('end')
    }
  }
}
function start() {
  if (running.value || remaining.value === 0) return
  running.value = true
  timer = window.setInterval(tick, 1000)
}
function pause() {
  running.value = false
  if (timer) { clearInterval(timer); timer = undefined }
}
function reset() {
  pause()
  remaining.value = props.durationSec
}

watch(() => props.durationSec, () => reset())
if (props.autoStart) start()
onUnmounted(pause)

defineExpose({ start, pause, reset, remaining })
</script>

<template>
  <div class="flex items-center gap-3">
    <svg class="w-5 h-5" :class="danger ? 'text-danger' : 'text-primary'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="12" cy="13" r="8" /><path d="M12 13V9M9 2h6" />
    </svg>
    <span
      class="text-h2 font-semibold tabular-nums"
      :class="danger ? 'text-danger' : 'text-ink-primary'"
    >{{ mmss }}</span>
    <div class="flex gap-1">
      <button type="button" class="text-caption text-primary px-1 hover:underline" @click="running ? pause() : start()">
        {{ running ? '暂停' : '继续' }}
      </button>
      <button type="button" class="text-caption text-ink-tertiary px-1 hover:underline" @click="reset">重置</button>
    </div>
  </div>
</template>
