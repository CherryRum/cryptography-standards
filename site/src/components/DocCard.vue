<template>
  <router-link :to="`/doc/${doc.id}`" class="doc-card">
    <div class="cover-wrap">
      <img
        :src="doc.coverUrl"
        :alt="doc.title"
        loading="lazy"
        @error="onCoverError"
      />
    </div>
    <div class="card-body">
      <span v-if="doc.standardCode" class="code-badge">{{ doc.standardCode }}</span>
      <h3 class="card-title">{{ doc.title }}</h3>
      <div class="card-meta">
        <span class="category-tag">{{ doc.categoryLabel }}</span>
        <span v-if="doc.pageCount" class="page-count">{{ doc.pageCount }} 页</span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import type { DocEntry } from '../types'

defineProps<{ doc: DocEntry }>()

function onCoverError(e: Event) {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
}
</script>

<style scoped>
.doc-card {
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06), 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s, box-shadow 0.2s;
  text-decoration: none;
  color: inherit;
}

.doc-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.cover-wrap {
  width: 100%;
  aspect-ratio: 3 / 4;
  background: #f0efe8;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.cover-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-body {
  padding: 14px 16px 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.code-badge {
  font-size: 12px;
  font-weight: 600;
  color: #4a7c6f;
  background: #e8f4f0;
  padding: 2px 8px;
  border-radius: 4px;
  align-self: flex-start;
  white-space: nowrap;
}

.card-title {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  color: #2c3e2d;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #888;
}

.category-tag {
  background: #f5f4ee;
  padding: 2px 6px;
  border-radius: 3px;
}

.page-count {
  opacity: 0.7;
}
</style>
