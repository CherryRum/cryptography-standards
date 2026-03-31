<template>
  <div class="home">
    <header class="hero">
      <h1>📜 密码标准文档库</h1>
      <p class="subtitle">中国商用密码国家标准 · 行业标准 · 公开文档</p>
      <SearchBar
        v-model="query"
        placeholder="搜索标准编号、名称或关键词…"
        @update:model-value="onQueryChange"
      />
    </header>

    <main class="main-content">
      <CategoryFilter
        v-model="activeCategory"
        :docs="allDocs"
      />

      <div class="sort-bar">
        <span class="result-count">{{ filteredDocs.length }} 份文档</span>
        <select v-model="sortBy" class="sort-select">
          <option value="code">按编号排序</option>
          <option value="year-desc">按年份（新→旧）</option>
          <option value="year-asc">按年份（旧→新）</option>
          <option value="pages">按页数排序</option>
        </select>
      </div>

      <div v-if="loading" class="status-msg">加载中…</div>
      <div v-else-if="error" class="status-msg error">{{ error }}</div>
      <div v-else-if="filteredDocs.length === 0" class="status-msg">
        没有找到匹配的文档
      </div>

      <div class="card-grid" v-if="filteredDocs.length > 0">
        <DocCard
          v-for="doc in filteredDocs"
          :key="doc.id"
          :doc="doc"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import SearchBar from '../components/SearchBar.vue'
import CategoryFilter from '../components/CategoryFilter.vue'
import DocCard from '../components/DocCard.vue'
import { useManifest } from '../composables/useManifest'
import { useSearch } from '../composables/useSearch'
import type { DocEntry } from '../types'

const { manifest, loading, error } = useManifest()
const { search, loadIndex } = useSearch()

const query = ref('')
const activeCategory = ref('all')
const sortBy = ref('code')

// 全部文档（当前分类筛选后的）
const allDocs = computed(() => manifest.value)

// 搜索结果 → 分类筛选 → 排序
const filteredDocs = computed(() => {
  let docs: DocEntry[] = query.value
    ? search(query.value, manifest.value)
    : [...manifest.value]

  // 分类筛选
  if (activeCategory.value !== 'all') {
    docs = docs.filter((d) => d.category === activeCategory.value)
  }

  // 排序
  docs.sort((a, b) => {
    switch (sortBy.value) {
      case 'year-desc':
        return (b.year || '0').localeCompare(a.year || '0')
      case 'year-asc':
        return (a.year || '0').localeCompare(b.year || '0')
      case 'pages':
        return b.pageCount - a.pageCount
      default: // code
        return a.standardCode.localeCompare(b.standardCode)
    }
  })

  return docs
})

function onQueryChange(val: string) {
  if (val.trim()) loadIndex()
}

// 搜索时重置分类到「全部」以展示所有结果
watch(query, (val) => {
  if (val.trim()) activeCategory.value = 'all'
})
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.hero {
  text-align: center;
  padding: 60px 24px 40px;
  background: linear-gradient(180deg, #e8f4f0 0%, #f5f4ee 100%);
}

.hero h1 {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e2d;
  margin: 0 0 8px;
}

.subtitle {
  font-size: 16px;
  color: #777;
  margin: 0 0 28px;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px 60px;
}

.sort-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 20px 0 16px;
  font-size: 14px;
  color: #888;
}

.sort-select {
  padding: 4px 10px;
  border: 1.5px solid #e0ddd5;
  border-radius: 6px;
  font-size: 13px;
  color: #555;
  background: #fff;
  cursor: pointer;
}

.result-count {
  font-weight: 500;
  color: #666;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.status-msg {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
  color: #999;
}

.status-msg.error {
  color: #c44;
}

@media (max-width: 768px) {
  .hero {
    padding: 40px 16px 28px;
  }

  .hero h1 {
    font-size: 24px;
  }

  .card-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
  }
}
</style>
