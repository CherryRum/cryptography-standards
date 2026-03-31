<template>
  <div class="search-bar">
    <div class="search-icon">🔍</div>
    <input
      ref="inputRef"
      type="text"
      :value="modelValue"
      :placeholder="placeholder"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      @keydown.escape="$emit('update:modelValue', '')"
    />
    <button
      v-if="modelValue"
      class="clear-btn"
      @click="$emit('update:modelValue', '')"
    >
      ✕
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

defineProps<{
  modelValue: string
  placeholder?: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()

const inputRef = ref<HTMLInputElement>()

onMounted(() => {
  // 桌面端自动聚焦
  if (window.innerWidth > 768) {
    inputRef.value?.focus()
  }
})
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  background: #fff;
  border: 2px solid #e0ddd5;
  border-radius: 12px;
  padding: 0 16px;
  height: 52px;
  width: 100%;
  max-width: 640px;
  margin: 0 auto;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-bar:focus-within {
  border-color: #4a7c6f;
  box-shadow: 0 0 0 3px rgba(74, 124, 111, 0.12);
}

.search-icon {
  font-size: 18px;
  margin-right: 10px;
  opacity: 0.5;
}

input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  background: transparent;
  color: #2c3e2d;
}

input::placeholder {
  color: #a0a09a;
}

.clear-btn {
  border: none;
  background: none;
  font-size: 16px;
  cursor: pointer;
  color: #999;
  padding: 4px 8px;
}

.clear-btn:hover {
  color: #555;
}
</style>
