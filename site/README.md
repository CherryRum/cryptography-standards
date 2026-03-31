# site

前端站点会直接消费仓库根目录 `dist/` 下的生成产物：

- `/data/manifest.json`
- `/data/search-index.json`
- `/docs/**`

本地开发前，先在仓库根目录生成资源：

```powershell
.venv\Scripts\python.exe scripts\build_assets.py
```

然后启动前端：

```powershell
cd site
npm install
npm run dev
```

`vite dev` 已额外映射仓库根目录 `../dist/data` 和 `../dist/docs`，所以生成完资源后可以直接在开发环境读取。
