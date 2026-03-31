import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/',
  build: {
    outDir: '../dist',
    emptyOutDir: false, // 不清空，因为 Python 脚本先写入 docs/ 和 data/
  },
})
