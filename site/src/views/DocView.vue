<template>
  <div class="doc-view" v-if="doc">
    <header class="doc-header">
      <router-link to="/" class="back-link">← 返回列表</router-link>
      <div class="doc-meta">
        <span v-if="doc.standardCode" class="code-badge">{{ doc.standardCode }}</span>
        <span class="category-tag">{{ doc.categoryLabel }}</span>
        <span v-if="doc.year" class="year-tag">{{ doc.year }} 年</span>
      </div>
      <h1 class="doc-title">{{ doc.title }}</h1>
      <div class="doc-info">
        <span>共 {{ doc.pageCount }} 页</span>
        <span>更新于 {{ doc.updatedAt }}</span>
      </div>
    </header>

    <section class="doc-body">
      <PageViewer
        :pages-base-url="doc.pagesBaseUrl"
        :page-count="doc.pageCount"
      />
    </section>
  </div>

  <div v-else-if="loading" class="status-msg">加载中…</div>
  <div v-else class="status-msg">
    <p>未找到该文档</p>
    <router-link to="/">返回首页</router-link>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useManifest } from '../composables/useManifest'
import PageViewer from '../components/PageViewer.vue'

const props = defineProps<{ id: string }>()
const { manifest, loading } = useManifest()

const doc = computed(() =>
  manifest.value.find((d) => d.id === props.id)
)
</script>

<style scoped>
.doc-view {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 20px 80px;
}

.back-link {
  display: inline-block;
  color: #4a7c6f;
  text-decoration: none;
  font-size: 14px;
  margin-bottom: 16px;
  transition: color 0.2s;
}

.back-link:hover {
  color: #3d6a5e;
}

.doc-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e0ddd5;
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.code-badge {
  font-size: 14px;
  font-weight: 600;
  color: #4a7c6f;
  background: #e8f4f0;
  padding: 4px 12px;
  border-radius: 6px;
}

.category-tag {
  font-size: 13px;
  color: #666;
  background: #f5f4ee;
  padding: 3px 10px;
  border-radius: 4px;
}

.year-tag {
  font-size: 13px;
  color: #888;
}

.doc-title {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.4;
  color: #2c3e2d;
  margin: 0 0 12px;
}

.doc-info {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #999;
}

.doc-body {
  margin-top: 16px;
}

.status-msg {
  text-align: center;
  padding: 80px 20px;
  font-size: 16px;
  color: #999;
}

.status-msg a {
  color: #4a7c6f;
  text-decoration: none;
}

@media (max-width: 768px) {
  .doc-view {
    padding: 16px 12px 60px;
  }

  .doc-title {
    font-size: 20px;
  }
}
</style>
