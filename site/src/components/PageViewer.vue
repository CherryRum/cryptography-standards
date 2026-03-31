<template>
  <div class="page-viewer">
    <div class="viewer-layout">
      <div class="pages-container">
        <div
          v-for="page in pageCount"
          :key="page"
          :ref="(el) => setPageRef(el as HTMLElement, page)"
          class="page-frame"
        >
          <img
            v-if="visiblePages.has(page)"
            :src="`${pagesBaseUrl}/${String(page).padStart(4, '0')}.webp`"
            :alt="`第 ${page} 页`"
            loading="lazy"
          />
          <div v-else class="page-placeholder">
            <span>第 {{ page }} 页</span>
          </div>
        </div>
      </div>

      <aside class="viewer-sidebar">
        <div class="viewer-toolbar">
          <div class="toolbar-header">
            <span class="toolbar-label">阅读控制</span>
            <strong>当前第 {{ currentPage }} 页</strong>
          </div>

          <div class="toolbar-actions">
            <button
              class="nav-button"
              @click="scrollToPage(currentPage - 1)"
              :disabled="currentPage <= 1"
            >
              上一页
            </button>
            <button
              class="nav-button"
              @click="scrollToPage(currentPage + 1)"
              :disabled="currentPage >= pageCount"
            >
              下一页
            </button>
          </div>

          <div class="page-jump">
            <label for="page-jump-input">跳转至页码</label>
            <div class="page-jump-controls">
              <input
                id="page-jump-input"
                type="number"
                min="1"
                :max="pageCount"
                v-model.number="jumpPage"
                @keydown.enter="scrollToPage(jumpPage)"
              />
              <button @click="scrollToPage(jumpPage)">前往</button>
            </div>
          </div>

          <button class="top-button" @click="scrollToTop">
            回到顶部
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps<{
  pagesBaseUrl: string
  pageCount: number
}>()

const jumpPage = ref(1)
const currentPage = ref(1)

// 预加载前 3 页
const visiblePages = reactive(new Set<number>(
  Array.from({ length: Math.min(3, props.pageCount) }, (_, i) => i + 1)
))

const pageRefs = new Map<number, HTMLElement>()

function setPageRef(el: HTMLElement | null, page: number) {
  if (el) pageRefs.set(page, el)
}

let lazyObserver: IntersectionObserver | null = null
let activeObserver: IntersectionObserver | null = null

function preloadAround(page: number) {
  const start = Math.max(1, page - 1)
  const end = Math.min(props.pageCount, page + 1)

  for (let current = start; current <= end; current += 1) {
    visiblePages.add(current)
  }
}

onMounted(() => {
  // 懒加载：使用 IntersectionObserver 监控每页进入视口
  lazyObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          const page = Number((entry.target as HTMLElement).dataset.page)
          if (page) preloadAround(page)
        }
      }
    },
    { rootMargin: '400px 0px' }
  )

  activeObserver = new IntersectionObserver(
    (entries) => {
      const visibleEntries = entries
        .filter((entry) => entry.isIntersecting)
        .map((entry) => ({
          page: Number((entry.target as HTMLElement).dataset.page),
          topOffset: Math.abs(entry.boundingClientRect.top)
        }))
        .filter((entry) => entry.page > 0)
        .sort((a, b) => a.topOffset - b.topOffset)

      if (!visibleEntries.length) return

      currentPage.value = visibleEntries[0].page
      jumpPage.value = visibleEntries[0].page
    },
    {
      rootMargin: '-64px 0px -45% 0px',
      threshold: 0.01
    }
  )

  nextTick(() => {
    for (const [page, el] of pageRefs) {
      el.dataset.page = String(page)
      lazyObserver!.observe(el)
      activeObserver!.observe(el)
    }
  })
})

onBeforeUnmount(() => {
  lazyObserver?.disconnect()
  activeObserver?.disconnect()
})

function scrollToPage(page: number) {
  const p = Math.max(1, Math.min(page, props.pageCount))
  currentPage.value = p
  jumpPage.value = p
  preloadAround(p)

  nextTick(() => {
    const el = pageRefs.get(p)
    el?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.page-viewer {
  width: 100%;
}

.viewer-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 220px;
  gap: 24px;
  align-items: start;
}

.viewer-sidebar {
  min-width: 0;
}

.viewer-toolbar {
  position: sticky;
  top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 18px;
  border: 1px solid #e4ddd1;
  border-radius: 16px;
  background: #fcfaf5;
  box-shadow: 0 8px 24px rgba(34, 48, 37, 0.06);
}

.toolbar-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #405246;
}

.toolbar-header strong {
  font-size: 18px;
}

.toolbar-label {
  font-size: 12px;
  letter-spacing: 0.08em;
  color: #7b6a4e;
}

.toolbar-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.nav-button,
.page-jump button,
.top-button {
  padding: 10px 12px;
  background: #4a7c6f;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s, opacity 0.2s;
}

.nav-button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.page-jump {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.page-jump-controls {
  display: flex;
  gap: 8px;
}

.page-jump input {
  min-width: 0;
  flex: 1;
  padding: 4px 8px;
  border: 1.5px solid #e0ddd5;
  border-radius: 6px;
  text-align: center;
  font-size: 14px;
}

.nav-button:hover:not(:disabled),
.page-jump button:hover,
.top-button:hover {
  background: #3d6a5e;
}

.pages-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
}

.page-frame {
  width: 100%;
  max-width: 860px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.08), 0 2px 16px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.page-frame img {
  display: block;
  width: 100%;
  height: auto;
}

.page-placeholder {
  width: 100%;
  aspect-ratio: 210 / 297;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #bbb;
  font-size: 16px;
  background: #fafaf6;
}

@media (max-width: 1024px) {
  .viewer-layout {
    grid-template-columns: 1fr;
  }

  .viewer-sidebar {
    order: -1;
  }

  .viewer-toolbar {
    position: static;
  }
}

@media (max-width: 768px) {
  .viewer-toolbar {
    padding: 16px;
    border-radius: 14px;
  }

  .toolbar-actions {
    grid-template-columns: 1fr 1fr;
  }

  .page-jump-controls {
    flex-direction: column;
  }

  .page-frame {
    border-radius: 0;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  }
}
</style>
