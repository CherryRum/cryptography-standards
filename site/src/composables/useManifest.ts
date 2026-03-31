import { ref, type Ref } from 'vue'
import type { DocEntry } from '../types'

const manifest = ref<DocEntry[]>([])
const loading = ref(false)
const loaded = ref(false)
const error = ref<string | null>(null)

async function fetchManifest() {
  if (loaded.value || loading.value) return
  loading.value = true
  error.value = null
  try {
    const resp = await fetch('/data/manifest.json')
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
    manifest.value = await resp.json()
    loaded.value = true
  } catch (e: any) {
    error.value = e.message || '加载失败'
  } finally {
    loading.value = false
  }
}

export function useManifest() {
  fetchManifest()
  return {
    manifest: manifest as Ref<DocEntry[]>,
    loading: loading as Ref<boolean>,
    error: error as Ref<string | null>,
  }
}
