import fs from 'node:fs'
import path from 'node:path'
import { defineConfig, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'

const GENERATED_ASSET_PREFIXES = ['/data/', '/docs/']
const MIME_TYPES: Record<string, string> = {
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
}

function serveGeneratedAssets(): Plugin {
  const generatedDir = path.resolve(__dirname, '..', 'dist')

  return {
    name: 'serve-generated-assets',
    apply: 'serve',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url?.split('?')[0] ?? ''
        if (!GENERATED_ASSET_PREFIXES.some((prefix) => url.startsWith(prefix))) {
          next()
          return
        }

        const relativePath = decodeURIComponent(url).replace(/^\/+/, '')
        const filePath = path.resolve(generatedDir, relativePath)
        const relativeToGeneratedDir = path.relative(generatedDir, filePath)

        if (
          relativeToGeneratedDir.startsWith('..') ||
          path.isAbsolute(relativeToGeneratedDir)
        ) {
          res.statusCode = 403
          res.end('Forbidden')
          return
        }

        if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
          next()
          return
        }

        const ext = path.extname(filePath).toLowerCase()
        res.setHeader(
          'Content-Type',
          MIME_TYPES[ext] ?? 'application/octet-stream'
        )
        res.setHeader('Cache-Control', 'no-store')
        fs.createReadStream(filePath).pipe(res)
      })
    },
  }
}

export default defineConfig({
  plugins: [vue(), serveGeneratedAssets()],
  base: '/',
  build: {
    outDir: '../dist',
    emptyOutDir: false, // 不清空，因为 Python 脚本先写入 docs/ 和 data/
  },
})
