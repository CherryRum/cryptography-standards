<template>
  <div class="page-viewer">
    <div class="viewer-toolbar">
      <span class="page-info">共 {{ pageCount }} 页</span>
      <div class="page-jump">
        <label>跳转至</label>
        <input
          type="number"
          min="1"
          :max="pageCount"
          v-model.number="jumpPage"
          @keydown.enter="scrollToPage(jumpPage)"
        />
        <button @click="scrollToPage(jumpPage)">Go</button>
      </div>
    </div>

    <div class="pages-container" ref="containerRef">
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

    <button
      v-show="showBackTop"
      class="back-top"
      @click="scrollToTop"
      title="回到顶部"
    >
      ↑
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps<{
  pagesBaseUrl: string
  pageCount: number
}>()

const jumpPage = ref(1)
const showBackTop = ref(false)

// 预加载前 3 页
const visiblePages = reactive(new Set<number>(
  Array.from({ length: Math.min(3, props.pageCount) }, (_, i) => i + 1)
))

const pageRefs = new Map<number, HTMLElement>()

function setPageRef(el: HTMLElement | null, page: number) {
  if (el) pageRefs.set(page, el)
}

let observer: IntersectionObserver | null = null

onMounted(() => {
  // 懒加载：使用 IntersectionObserver 监控每页进入视口
  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          const page = Number((entry.target as HTMLElement).dataset.page)
          if (page) visiblePages.add(page)
        }
      }
    },
    { rootMargin: '400px 0px' }
  )

  nextTick(() => {
    for (const [page, el] of pageRefs) {
      el.dataset.page = String(page)
      observer!.observe(el)
    }
  })

  window.addEventListener('scroll', onScroll, { passive: true })
})

onBeforeUnmount(() => {
  observer?.disconnect()
  window.removeEventListener('scroll', onScroll)
})

function onScroll() {
  showBackTop.value = window.scrollY > 600
}

function scrollToPage(page: number) {
  const p = Math.max(1, Math.min(page, props.pageCount))
  // 确保目标页已加载
  visiblePages.add(p)
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

.viewer-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  margin-bottom: 16px;
  border-bottom: 1px solid #e0ddd5;
  flex-wrap: wrap;
  gap: 8px;
}

.page-info {
  font-size: 14px;
  color: #666;
}

.page-jump {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #666;
}

.page-jump input {
  width: 60px;
  padding: 4px 8px;
  border: 1.5px solid #e0ddd5;
  border-radius: 6px;
  text-align: center;
  font-size: 14px;
}

.page-jump button {
  padding: 4px 12px;
  background: #4a7c6f;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.page-jump button:hover {
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
  max-width: 900px;
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

.back-top {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  background: #4a7c6f;
  color: #fff;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: background 0.2s;
  z-index: 100;
}

.back-top:hover {
  background: #3d6a5e;
}

@media (max-width: 768px) {
  .page-frame {
    border-radius: 0;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  }

  .back-top {
    bottom: 20px;
    right: 20px;
  }
}
</style>
