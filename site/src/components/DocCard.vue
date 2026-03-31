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
        <span v-if="doc.year" class="year-tag">{{ doc.year }}</span>
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
  border: 1px solid #ebe7de;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.03);
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  text-decoration: none;
  color: inherit;
}

.doc-card:hover {
  transform: translateY(-2px);
  border-color: #d7e1dc;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
}

.cover-wrap {
  width: 100%;
  aspect-ratio: 1 / 1.08;
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
  padding: 10px 12px 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.code-badge {
  font-size: 11px;
  font-weight: 600;
  color: #4a7c6f;
  background: #e8f4f0;
  padding: 2px 7px;
  border-radius: 4px;
  align-self: flex-start;
  white-space: nowrap;
}

.card-title {
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
  color: #2c3e2d;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  margin-top: auto;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 11px;
  color: #888;
}

.category-tag {
  background: #f5f4ee;
  padding: 2px 6px;
  border-radius: 3px;
}

.year-tag {
  color: #7f7f78;
}

.page-count {
  opacity: 0.7;
}
</style>
