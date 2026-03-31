import { ref, readonly } from 'vue'
import MiniSearch from 'minisearch'
import type { SearchDoc, DocEntry } from '../types'

const miniSearch = ref<MiniSearch<SearchDoc> | null>(null)
const indexLoading = ref(false)
const indexLoaded = ref(false)

async function loadIndex() {
  if (indexLoaded.value || indexLoading.value) return
  indexLoading.value = true
  try {
    const resp = await fetch('/data/search-index.json')
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
    const docs: SearchDoc[] = await resp.json()

    const ms = new MiniSearch<SearchDoc>({
      fields: ['standardCode', 'title', 'categoryLabel', 'year', 'textExcerpt', 'fulltext'],
      storeFields: ['id'],
      searchOptions: {
        boost: { standardCode: 3, title: 2 },
        fuzzy: 0.2,
        prefix: true,
      },
      tokenize: (text) => {
        // 支持中文：按非中文字符分词 + 中文逐字/双字
        const words = text.split(/[\s/\-_.，。、；：""''（）()[\]【】]+/).filter(Boolean)
        const cjk = text.match(/[\u4e00-\u9fff]{1,2}/g) || []
        return [...words, ...cjk]
      },
    })
    ms.addAll(docs)
    miniSearch.value = ms
    indexLoaded.value = true
  } catch (e) {
    console.error('搜索索引加载失败', e)
  } finally {
    indexLoading.value = false
  }
}

export function useSearch() {
  function search(query: string, manifest: DocEntry[]): DocEntry[] {
    if (!query.trim()) return manifest

    // 确保索引已加载
    if (!miniSearch.value) {
      loadIndex()
      // 索引未就绪时退回简单过滤
      const q = query.toLowerCase()
      return manifest.filter(
        (d) =>
          d.title.toLowerCase().includes(q) ||
          d.standardCode.toLowerCase().includes(q)
      )
    }

    const results = miniSearch.value.search(query)
    const idSet = new Set(results.map((r) => r.id))
    return manifest.filter((d) => idSet.has(d.id))
  }

  return {
    search,
    loadIndex,
    indexLoading: readonly(indexLoading),
    indexLoaded: readonly(indexLoaded),
  }
}
