<template>
  <router-link :to="`/doc/${doc.id}`" class="doc-list-item">
    <div class="primary">
      <span v-if="doc.standardCode" class="standard-code">{{ doc.standardCode }}</span>
      <h3 class="title">{{ doc.title }}</h3>
    </div>

    <dl class="meta-grid">
      <div class="meta-item">
        <dt>分类</dt>
        <dd>{{ doc.categoryLabel }}</dd>
      </div>
      <div class="meta-item">
        <dt>年份</dt>
        <dd>{{ doc.year || '—' }}</dd>
      </div>
      <div class="meta-item">
        <dt>页数</dt>
        <dd>{{ doc.pageCount ? `${doc.pageCount} 页` : '—' }}</dd>
      </div>
    </dl>
  </router-link>
</template>

<script setup lang="ts">
import type { DocEntry } from '../types'

defineProps<{ doc: DocEntry }>()
</script>

<style scoped>
.doc-list-item {
  display: grid;
  grid-template-columns: minmax(0, 2.2fr) minmax(280px, 1fr);
  gap: 16px;
  align-items: center;
  padding: 14px 16px;
  border: 1px solid #e7e3da;
  border-radius: 10px;
  background: #fff;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}

.doc-list-item:hover {
  border-color: #cddbd5;
  box-shadow: 0 6px 20px rgba(34, 58, 48, 0.08);
  transform: translateY(-1px);
}

.primary {
  min-width: 0;
}

.standard-code {
  display: inline-block;
  margin-bottom: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #4a7c6f;
}

.title {
  margin: 0;
  font-size: 15px;
  line-height: 1.4;
  color: #2c3e2d;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin: 0;
}

.meta-item {
  min-width: 0;
}

.meta-item dt {
  margin-bottom: 4px;
  font-size: 11px;
  color: #8a8a83;
}

.meta-item dd {
  margin: 0;
  font-size: 13px;
  color: #4f4f4a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 768px) {
  .doc-list-item {
    grid-template-columns: 1fr;
    gap: 12px;
    padding: 12px 14px;
  }

  .title {
    font-size: 14px;
  }

  .meta-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
  }
}

@media (max-width: 520px) {
  .meta-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .meta-item {
    display: flex;
    justify-content: space-between;
    gap: 12px;
  }

  .meta-item dt {
    margin-bottom: 0;
  }

  .meta-item dd {
    text-align: right;
  }
}
</style>
