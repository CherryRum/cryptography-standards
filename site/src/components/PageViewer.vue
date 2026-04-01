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
            <div class="toolbar-heading">
              <span class="toolbar-label">阅读控制</span>
              <span class="follow-indicator" :class="{ navigating: isNavigating }">
                {{ followStatusLabel }}
              </span>
            </div>
            <strong>当前第 {{ currentPage }} 页</strong>
            <div class="reading-state" :class="{ navigating: isNavigating }">
              <span class="state-label">{{ readingStateLabel }}</span>
              <strong>{{ readingStateValue }}</strong>
            </div>
          </div>

          <div class="progress-panel">
            <div class="progress-summary">
              <span>阅读进度</span>
              <strong>{{ currentPage }} / {{ pageCount }}</strong>
            </div>
            <div class="progress-meta">
              <span>{{ progressPercent }}%</span>
              <span>约 {{ currentSectionLabel }}</span>
            </div>
            <div class="progress-bar" aria-hidden="true">
              <div class="progress-bar-fill" :style="{ width: `${progressPercent}%` }"></div>
            </div>
            <input
              class="progress-slider"
              type="range"
              min="1"
              :max="pageCount"
              :value="currentPage"
              @input="handleSliderInput"
              aria-label="阅读进度滑块"
            />
            <div class="progress-scale" aria-hidden="true">
              <span>第 1 页</span>
              <span>第 {{ pageCount }} 页</span>
            </div>
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
import { computed, ref, shallowRef, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps<{
  pagesBaseUrl: string
  pageCount: number
}>()

const VIEWPORT_ANCHOR_OFFSET = 88
const NAVIGATION_COMPLETE_THRESHOLD = 24
const jumpPage = ref(1)
const currentPage = ref(1)
const lastSettledPage = ref(1)
const progressPercent = computed(() =>
  props.pageCount > 0 ? Math.round((currentPage.value / props.pageCount) * 100) : 0
)
const currentSectionLabel = computed(() => {
  const percent = progressPercent.value

  if (percent >= 100) return '文档末尾'
  if (percent >= 75) return '后段'
  if (percent >= 50) return '中后段'
  if (percent >= 25) return '中段'

  return '前段'
})
const isNavigating = computed(() => navigationTargetPage !== null)
const followStatusLabel = computed(() => (isNavigating.value ? '正在跟随' : '已同步'))
const readingStateLabel = computed(() => (isNavigating.value ? '目标页' : '稳定页'))
const readingStateValue = computed(() =>
  isNavigating.value && navigationTargetPage !== null
    ? `第 ${navigationTargetPage} 页`
    : `第 ${lastSettledPage.value} 页`
)

const INITIAL_PRELOAD_COUNT = 5
const ACTIVE_PRELOAD_RADIUS = 2
const TARGET_PRELOAD_RADIUS = 3
const SCROLL_SETTLE_DELAY = 220

// 预加载前几页，并在滚动时按需扩展
const visiblePages = shallowRef(new Set<number>(
  Array.from({ length: Math.min(INITIAL_PRELOAD_COUNT, props.pageCount) }, (_, i) => i + 1)
))

const pageRefs = new Map<number, HTMLElement>()
const activeEntries = new Map<number, IntersectionObserverEntry>()

function setPageRef(el: HTMLElement | null, page: number) {
  if (el) {
    pageRefs.set(page, el)
    el.dataset.page = String(page)
    return
  }

  pageRefs.delete(page)
}

let lazyObserver: IntersectionObserver | null = null
let activeObserver: IntersectionObserver | null = null
let scrollSettleTimer: ReturnType<typeof setTimeout> | null = null
let navigationTargetPage: number | null = null
let scrollSyncFrame: number | null = null

function clampPage(page: number) {
  return Math.max(1, Math.min(page, props.pageCount))
}

function setCurrentPage(page: number) {
  if (currentPage.value !== page) {
    currentPage.value = page
  }

  if (navigationTargetPage === null && jumpPage.value !== page) {
    jumpPage.value = page
  }
}

function setSettledPage(page: number) {
  lastSettledPage.value = page
}

function getPageTopDistance(page: number) {
  const el = pageRefs.get(page)
  if (!el) return Number.POSITIVE_INFINITY
  return Math.abs(el.getBoundingClientRect().top - VIEWPORT_ANCHOR_OFFSET)
}

function isNavigationAligned(page: number) {
  return getPageTopDistance(page) <= NAVIGATION_COMPLETE_THRESHOLD
}

function preloadRange(centerPage: number, radius: number) {
  const start = Math.max(1, centerPage - radius)
  const end = Math.min(props.pageCount, centerPage + radius)
  const nextVisiblePages = new Set(visiblePages.value)
  let changed = false

  for (let current = start; current <= end; current += 1) {
    if (!nextVisiblePages.has(current)) {
      nextVisiblePages.add(current)
      changed = true
    }
  }

  if (changed) {
    visiblePages.value = nextVisiblePages
  }
}

function syncCurrentPageFromViewport() {
  if (navigationTargetPage !== null) return

  let nextPage = 1
  let bestDistance = Number.POSITIVE_INFINITY

  for (const [page, el] of pageRefs) {
    const distance = Math.abs(el.getBoundingClientRect().top - VIEWPORT_ANCHOR_OFFSET)

    if (distance < bestDistance) {
      bestDistance = distance
      nextPage = page
    }
  }

  setCurrentPage(nextPage)
  setSettledPage(nextPage)
  preloadRange(nextPage, ACTIVE_PRELOAD_RADIUS)
}

function chooseObservedPage() {
  if (navigationTargetPage !== null) return

  let bestPage: number | null = null
  let bestScore = Number.NEGATIVE_INFINITY

  for (const [page, entry] of activeEntries) {
    if (!entry.isIntersecting) continue

    const topDistance = Math.abs(entry.boundingClientRect.top - VIEWPORT_ANCHOR_OFFSET)
    const score = entry.intersectionRatio * 1000 - topDistance

    if (score > bestScore) {
      bestScore = score
      bestPage = page
    }
  }

  if (bestPage !== null) {
    setCurrentPage(bestPage)
    setSettledPage(bestPage)
    preloadRange(bestPage, ACTIVE_PRELOAD_RADIUS)
  }
}

function clearScrollSettleTimer() {
  if (!scrollSettleTimer) return
  clearTimeout(scrollSettleTimer)
  scrollSettleTimer = null
}

function finishProgrammaticNavigation() {
  clearScrollSettleTimer()

  if (navigationTargetPage === null) return

  const targetPage = navigationTargetPage
  navigationTargetPage = null
  jumpPage.value = targetPage
  setSettledPage(targetPage)
  syncCurrentPageFromViewport()
  chooseObservedPage()
}

function scheduleScrollSettleCheck() {
  clearScrollSettleTimer()
  scrollSettleTimer = setTimeout(() => {
    finishProgrammaticNavigation()
  }, SCROLL_SETTLE_DELAY)
}

function handleScroll() {
  if (scrollSyncFrame !== null) return

  scrollSyncFrame = window.requestAnimationFrame(() => {
    scrollSyncFrame = null

    if (navigationTargetPage !== null) {
      if (isNavigationAligned(navigationTargetPage)) {
        finishProgrammaticNavigation()
        return
      }

      scheduleScrollSettleCheck()
      return
    }

    syncCurrentPageFromViewport()
  })
}

onMounted(() => {
  // 懒加载：使用 IntersectionObserver 监控每页进入视口
  lazyObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          const page = Number((entry.target as HTMLElement).dataset.page)
          if (page) preloadRange(page, ACTIVE_PRELOAD_RADIUS)
        }
      }
    },
    { rootMargin: '800px 0px' }
  )

  activeObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const page = Number((entry.target as HTMLElement).dataset.page)

        if (!page) continue

        if (entry.isIntersecting) {
          activeEntries.set(page, entry)
        } else {
          activeEntries.delete(page)
        }
      }

      if (navigationTargetPage !== null) {
        const targetEntry = activeEntries.get(navigationTargetPage)

        if (targetEntry?.isIntersecting) {
          setCurrentPage(navigationTargetPage)
          preloadRange(navigationTargetPage, TARGET_PRELOAD_RADIUS)

          if (isNavigationAligned(navigationTargetPage)) {
            finishProgrammaticNavigation()
          }
        }

        return
      }

      chooseObservedPage()
    },
    {
      rootMargin: `-${VIEWPORT_ANCHOR_OFFSET}px 0px -45% 0px`,
      threshold: 0.01
    }
  )

  nextTick(() => {
    for (const [, el] of pageRefs) {
      lazyObserver!.observe(el)
      activeObserver!.observe(el)
    }

    syncCurrentPageFromViewport()
    setSettledPage(currentPage.value)
  })

  window.addEventListener('scroll', handleScroll, { passive: true })
})

onBeforeUnmount(() => {
  clearScrollSettleTimer()
  if (scrollSyncFrame !== null) {
    window.cancelAnimationFrame(scrollSyncFrame)
  }
  lazyObserver?.disconnect()
  activeObserver?.disconnect()
  window.removeEventListener('scroll', handleScroll)
})

function scrollWindowToPage(page: number) {
  const el = pageRefs.get(page)

  if (!el) return

  const top = window.scrollY + el.getBoundingClientRect().top - VIEWPORT_ANCHOR_OFFSET
  window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
}

function scrollToPage(page: number) {
  const p = clampPage(page)
  navigationTargetPage = p
  currentPage.value = p
  jumpPage.value = p
  preloadRange(p, TARGET_PRELOAD_RADIUS)
  scheduleScrollSettleCheck()

  nextTick(() => {
    scrollWindowToPage(p)
  })
}

function handleSliderInput(event: Event) {
  const value = Number((event.target as HTMLInputElement).value)
  scrollToPage(value)
}

function scrollToTop() {
  navigationTargetPage = 1
  currentPage.value = 1
  jumpPage.value = 1
  preloadRange(1, TARGET_PRELOAD_RADIUS)
  scheduleScrollSettleCheck()
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
  position: sticky;
  top: 16px;
  min-width: 0;
  align-self: start;
  z-index: 2;
}

.viewer-toolbar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 18px;
  border: 1px solid #e4ddd1;
  border-radius: 16px;
  background: #fcfaf5;
  box-shadow: 0 8px 24px rgba(34, 48, 37, 0.06);
  max-height: calc(100vh - 32px);
  overflow-y: auto;
  scrollbar-gutter: stable;
}

.toolbar-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #405246;
}

.toolbar-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.toolbar-header strong {
  font-size: 18px;
}

.toolbar-label {
  font-size: 12px;
  letter-spacing: 0.08em;
  color: #7b6a4e;
}

.follow-indicator,
.reading-state {
  border-radius: 999px;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}

.follow-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 5px 10px;
  border: 1px solid #cfe0d9;
  background: #eef5f2;
  color: #4a7c6f;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.follow-indicator.navigating {
  border-color: #d8c6a4;
  background: #f7efdf;
  color: #8a6a2f;
}

.reading-state {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  border: 1px solid #d8e4dd;
  background: #f7fbf8;
  color: #405246;
}

.reading-state.navigating {
  border-color: #ead9b6;
  background: #fff8eb;
}

.state-label {
  font-size: 12px;
  color: #7b6a4e;
}

.reading-state strong {
  font-size: 14px;
}

.toolbar-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.progress-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px;
  border: 1px solid #e7dfd2;
  border-radius: 12px;
  background: linear-gradient(180deg, #fffdf8 0%, #f6f1e7 100%);
}

.progress-summary,
.progress-meta,
.progress-scale {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.progress-summary {
  color: #405246;
  font-size: 14px;
}

.progress-summary strong,
.progress-meta span:first-child {
  font-weight: 700;
}

.progress-meta {
  font-size: 12px;
  color: #7b6a4e;
}

.progress-bar {
  position: relative;
  height: 8px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(74, 124, 111, 0.14);
}

.progress-bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #4a7c6f 0%, #6da693 100%);
  transition: width 0.18s ease-out;
}

.progress-slider {
  width: 100%;
  accent-color: #4a7c6f;
  cursor: pointer;
}

.progress-scale {
  font-size: 12px;
  color: #8a7a5e;
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
  scroll-margin-top: 16px;
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
    position: static;
    order: -1;
  }

  .viewer-toolbar {
    max-height: none;
    overflow-y: visible;
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

  .progress-summary,
  .progress-meta,
  .progress-scale {
    flex-wrap: wrap;
  }

  .page-frame {
    border-radius: 0;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  }
}
</style>
