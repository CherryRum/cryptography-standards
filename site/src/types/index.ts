export interface DocEntry {
  id: string
  title: string
  standardCode: string
  category: string
  categoryLabel: string
  year: string
  pageCount: number
  coverUrl: string
  pagesBaseUrl: string
  updatedAt: string
}

export interface SearchDoc {
  id: string
  standardCode: string
  title: string
  category: string
  categoryLabel: string
  year: string
  textExcerpt: string
  fulltext: string
}

export const CATEGORY_OPTIONS = [
  { slug: 'all', label: '全部' },
  { slug: 'gbt', label: '国家标准' },
  { slug: 'gmt', label: '行业标准（现行）' },
  { slug: 'gmt-deprecated', label: '行业标准（废止）' },
  { slug: 'public', label: '公开文档' },
  { slug: 'english', label: '英文标准' },
] as const
