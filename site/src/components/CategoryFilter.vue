<template>
  <div class="category-filter">
    <button
      v-for="opt in options"
      :key="opt.slug"
      :class="['filter-btn', { active: modelValue === opt.slug }]"
      @click="$emit('update:modelValue', opt.slug)"
    >
      {{ opt.label }}
      <span v-if="counts[opt.slug] !== undefined" class="count">({{ counts[opt.slug] }})</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { DocEntry } from '../types'
import { CATEGORY_OPTIONS } from '../types'

const props = defineProps<{
  modelValue: string
  docs: DocEntry[]
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()

const options = CATEGORY_OPTIONS

const counts = computed(() => {
  const m: Record<string, number> = { all: props.docs.length }
  for (const doc of props.docs) {
    m[doc.category] = (m[doc.category] || 0) + 1
  }
  return m
})
</script>

<style scoped>
.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.filter-btn {
  border: 1.5px solid #e0ddd5;
  background: #fff;
  color: #555;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.filter-btn:hover {
  border-color: #4a7c6f;
  color: #4a7c6f;
}

.filter-btn.active {
  background: #4a7c6f;
  border-color: #4a7c6f;
  color: #fff;
}

.count {
  font-size: 12px;
  opacity: 0.7;
  margin-left: 2px;
}
</style>
