# Cloudflare Pages + Railway 部署指南

本文档指导你如何将 **CS Teachable Agent** 部署到：
- **前端** → Cloudflare Pages（全球 CDN，免费）
- **后端** → Railway（Python/FastAPI 托管，免费额度 $5/月）

---

## 📋 前置要求

1. [Cloudflare 账号](https://dash.cloudflare.com/sign-up)（免费）
2. [Railway 账号](https://railway.app/?referralCode=optional)（免费额度足够）
3. [GitHub 账号](https://github.com/signup)（代码托管）
4. 将本项目推送到 GitHub 仓库

---

## 第一步：部署后端到 Railway

### 1.1 创建 Railway 项目

1. 登录 [Railway Dashboard](https://railway.app/dashboard)
2. 点击 **"New Project"** → **"Deploy from GitHub repo"**
3. 选择你的 GitHub 仓库（需要先授权 Railway 访问 GitHub）
4. Railway 会自动检测到 `railway.toml` 和 `Dockerfile.backend`

### 1.2 配置环境变量

在 Railway 项目设置中添加以下环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `OPENAI_API_KEY` | `sk-...` | （可选）OpenAI API 密钥，用于 LLM 功能 |
| `DEEPSEEK_API_KEY` | `sk-...` | （可选）DeepSeek API 密钥 |
| `DATABASE_URL` | （不需要设置，默认使用 `./data/app.db`） | 数据库路径（SQLite 已自动配置） |
| `SECRET_KEY` | 随机字符串 | JWT 密钥，用于认证 |
| `FRONTEND_URL` | `https://your-pages.pages.dev` | 前端域名（Cloudflare Pages），用于 CORS |

> 💡 **生成 SECRET_KEY**：在终端运行 `openssl rand -hex 32`

### 1.3 添加持久化存储（SQLite 用）

如果使用 SQLite，需要添加 Volume：

1. 在 Railway 项目中点击 **"New"** → **"Volume"**
2. 挂载路径填写：`/app/data`
3. 大小：1GB 足够

### 1.4 获取后端 URL

部署完成后，Railway 会分配一个域名。

**你的后端地址**：`https://cs-teachable-agent-production.up.railway.app`

测试：访问 `https://cs-teachable-agent-production.up.railway.app/api/health` 应返回 `{"status": "ok"}`

> 如 Railway 分配了不同域名，请用实际的替换下文中所有 `cs-teachable-agent-production.up.railway.app`

---

## 第二步：部署前端到 Cloudflare Pages

### 2.1 配置环境变量

在项目根目录创建 `frontend/.env.production`：

```bash
# frontend/.env.production
VITE_API_URL=https://cs-teachable-agent-production.up.railway.app/api
```

> 如果 Railway 给你的后端地址不同，替换为实际的域名。

### 2.2 连接 Cloudflare Pages

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 点击 **"Pages"** → **"Create a project"**
3. 选择 **"Connect to Git"**
4. 授权 Cloudflare 访问你的 GitHub 仓库
5. 选择本项目仓库

### 2.3 构建设置

填写以下配置：

| 配置项 | 值 |
|--------|-----|
| **Project name** | `cs-teachable-agent`（或你喜欢的名字） |
| **Production branch** | `main` |
| **Build command** | `cd frontend && npm ci && npm run build` |
| **Build output directory** | `frontend/dist` |
| **Root directory** | `/`（留空或填 `/`） |

### 2.4 环境变量

在 Cloudflare Pages 设置中添加：

| 变量名 | 值 |
|--------|-----|
| `VITE_API_URL` | `https://cs-teachable-agent-production.up.railway.app/api` |
| `NODE_VERSION` | `20` |

> 确保 URL 与你 Railway 后端的实际地址一致。

### 2.5 部署

点击 **"Save and Deploy"**，Cloudflare 会自动：
1. 安装 Node.js 依赖
2. 构建前端（Vite 会读取 `VITE_API_URL`）
3. 部署到全球 CDN

部署完成后，你会得到一个类似 `https://cs-teachable-agent.pages.dev` 的链接。

---

## 第三步：配置 CORS（重要！）

由于前端和后端在不同域名，需要配置 CORS。

### 3.1 更新后端 CORS 设置

编辑 `src/api/main.py`：

```python
from fastapi.middleware.cors import CORSMiddleware

# 替换原有的 allow_origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.pages.dev",  # Cloudflare Pages 地址
        "http://localhost:3000",               # 本地开发
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3.2 Railway 环境变量配置

在 Railway 项目设置中添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `FRONTEND_URL` | `https://cs-teachable-agent.pages.dev` | 你的 Pages 前端地址（部署后获得） |
| `SECRET_KEY` | `openssl rand -hex 32` 生成的随机字符串 | JWT 密钥，用于认证 |

> 注意：`FRONTEND_URL` 必须与你实际的 Pages 域名完全一致（包括 https://）。部署 Pages 后，将获得的实际地址填入 Railway。

### 3.3 重新部署后端

推送代码后，Railway 会自动重新部署。

---

## 🎉 完成！访问你的应用

部署成功后，你将获得：

- **前端**：`https://cs-teachable-agent.pages.dev`（或你自定义的名称）
- **后端 API**：`https://cs-teachable-agent-production.up.railway.app/api/docs`

---

## 🔧 快速部署检查清单（Pages + 你的后端）

### Railway 后端（已部署）
- [ ] 后端运行正常：`https://cs-teachable-agent-production.up.railway.app/api/health` 返回 `{"status": "ok"}`
- [ ] 环境变量 `SECRET_KEY` 已设置（用于 JWT）
- [ ] 环境变量 `FRONTEND_URL` 设置为你的 Pages 地址（如 `https://cs-teachable-agent.pages.dev`）

### Cloudflare Pages 前端
- [ ] 项目已连接到 GitHub 仓库
- [ ] Build command: `cd frontend && npm ci && npm run build`
- [ ] Build output directory: `frontend/dist`
- [ ] 环境变量 `VITE_API_URL` = `https://cs-teachable-agent-production.up.railway.app/api`
- [ ] 环境变量 `NODE_VERSION` = `20`
- [ ] 构建成功，获得 Pages 链接

### 验证
- [ ] 访问 Pages 链接，页面正常显示（非空白）
- [ ] 打开开发者工具 (F12)，Console 无红色错误
- [ ] Network 面板中 API 请求返回 200
- [ ] 可以正常注册/登录账号

---

## 🔧 常见问题

### Q1: Railway 免费额度够用吗？
A: Railway 免费版提供 $5/月额度，本项目足够使用（SQLite + FastAPI 资源占用很低）。超出后按量付费或升级到 Hobby 计划 ($5/月固定)。

### Q2: 数据库用什么？
A: 默认 SQLite 存储在 Volume 中。生产环境建议切换到 PostgreSQL（Railway 提供一键部署）。

### Q3: 如何更新部署？
A: 推送代码到 GitHub，Railway 和 Cloudflare Pages 会自动重新部署。

### Q4: 自定义域名？
- **Cloudflare Pages**: 在 Pages 设置中添加自定义域名
- **Railway**: 在 Settings → Networking 中添加自定义域名

---

## 📁 部署相关文件

| 文件 | 用途 |
|------|------|
| `railway.toml` | Railway 部署配置 |
| `Dockerfile.backend` | 后端容器镜像 |
| `frontend/wrangler.toml` | Cloudflare 配置（可选） |
| `frontend/.nvmrc` | 指定 Node.js 版本 |
| `frontend/.env.example` | 环境变量示例 |
| `frontend/.env.production` | 生产环境配置（你需要创建） |

---

## 🚀 快速检查清单

部署前确认：
- [ ] Railway 后端 URL 可访问 (`/api/health`)
- [ ] `frontend/.env.production` 已配置正确 API URL
- [ ] Cloudflare Pages 环境变量 `VITE_API_URL` 已设置
- [ ] CORS 配置包含 Cloudflare Pages 域名
- [ ] 后端环境变量 `SECRET_KEY` 已设置（用于 JWT）

---

需要帮忙排查部署问题？检查以下日志：
- **Railway**: Dashboard → 你的服务 → Deployments → Logs
- **Cloudflare Pages**: Dashboard → Pages → 你的项目 → Builds

---

## 🔴 打开链接显示空白页 / 什么都没有

若访问前端地址（如 `https://cs-teachable-agent.xxx.workers.dev` 或 `https://xxx.pages.dev`）时页面完全空白，按下面顺序排查：

### 1. SPA 回退（前端路由）

- 本项目已在 `frontend/public/_redirects` 中配置：`/*    /index.html   200`。
- **Cloudflare Pages** 会读取该文件（构建时 `public` 会复制到 `dist`），确保所有路径都返回 `index.html`，由 React 路由接管。
- 若使用 **Workers** 部署静态站点，需确保 Worker 对未知路径也返回 `index.html`（部分 Workers 配置需单独设置）。

### 2. 前端 API 地址（必配）

- 生产构建时前端必须知道后端地址。在 **Cloudflare Pages 构建环境变量** 中设置：
  - `VITE_API_URL` = 你的 Railway 后端 API 根地址，例如：`https://你的项目.up.railway.app/api`
- 若未设置，前端会请求同源 `/api`，而 Pages/Workers 上没有后端，所有请求 404，可能导致白屏或报错。

### 3. 后端 CORS

- 后端需允许你的前端域名。在 **Railway 环境变量** 中设置其一（或都设）：
  - `FRONTEND_URL` = 你的前端完整地址，如：`https://你的项目.pages.dev`
  - `WORKERS_URL` = 若前端是 `*.workers.dev` 域名，如：`https://cs-teachable-agent.xmeng19.workers.dev`
- 设置后重新部署 Railway，否则浏览器会因 CORS 拦截 API 请求。

### 4. 浏览器排查

- 打开开发者工具 (F12) → **Console**：看是否有报错（如 Failed to fetch、CORS、404）。
- **Network**：检查对 `/api/...` 或后端域名的请求是否 404 或被 CORS 拒绝。
