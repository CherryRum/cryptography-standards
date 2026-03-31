const isDev = import.meta.env.DEV

export async function fetchJsonArray<T>(url: string): Promise<T[]> {
  const resp = await fetch(url, { cache: isDev ? 'no-cache' : 'default' })

  if (!resp.ok) {
    throw new Error(`加载 ${url} 失败（HTTP ${resp.status}）`)
  }

  const data = await resp.json()
  if (!Array.isArray(data)) {
    throw new Error(`${url} 返回的不是数组`)
  }

  return data as T[]
}

export async function fetchJsonArrayOrEmpty<T>(url: string): Promise<T[]> {
  try {
    return await fetchJsonArray<T>(url)
  } catch (err) {
    console.error(`[data] ${url} load failed`, err)
    return []
  }
}
