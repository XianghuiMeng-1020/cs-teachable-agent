# 部署配置完成总结

已为你创建 **Cloudflare Pages + Railway** 完整部署配置。

---

## 📁 新增/修改的文件

| 文件 | 用途 |
|------|------|
| `railway.toml` | Railway 部署配置（Docker 构建） |
| `frontend/wrangler.toml` | Cloudflare Pages 配置 |
| `frontend/.nvmrc` | 指定 Node.js 版本 (20) |
| `frontend/.env.example` | 前端环境变量示例 |
| `frontend/.env.production` | ⚠️ 你需要创建，填写 Railway 后端 URL |
| `DEPLOY_CF_RAILWAY.md` | 📖 详细部署指南 |
| `.github/workflows/deploy.yml` | GitHub Actions 自动部署 |
| `src/api/main.py` | 更新 CORS 支持 Cloudflare 域名 |
| `frontend/src/api/client.ts` | 支持 `VITE_API_URL` 环境变量 |
| `README.md` | 添加部署链接 |
| `DEPLOY.md` | 添加推荐方案链接 |

---

## 🚀 快速开始（3 步部署）

### 第 1 步：部署后端（Railway）

```bash
# 1. 推送代码到 GitHub
git add .
git commit -m "Add deployment configs"
git push origin main

# 2. 登录 Railway，创建项目，选择 GitHub 仓库
# Railway 会自动读取 railway.toml 和 Dockerfile.backend

# 3. 在 Railway 设置环境变量：
# - SECRET_KEY: openssl rand -hex 32
# - OPENAI_API_KEY: （可选）sk-...
# - FRONTEND_URL: （部署前端后填写）https://your-frontend.pages.dev
```

Railway 会给你的后端一个 URL，类似：
```
https://cs-teachable-agent-production.up.railway.app
```

### 第 2 步：配置前端环境变量

```bash
cd frontend
cp .env.example .env.production
# 编辑 .env.production，填写 Railway URL：
# VITE_API_URL=https://cs-teachable-agent-production.up.railway.app/api
```

### 第 3 步：部署前端（Cloudflare Pages）

1. 登录 [Cloudflare Pages](https://dash.cloudflare.com)
2. 创建项目 → 连接 GitHub 仓库
3. 构建设置：
   - **Build command**: `cd frontend && npm ci && npm run build`
   - **Output directory**: `frontend/dist`
   - **Environment variable**: `VITE_API_URL=https://your-backend.up.railway.app/api`
4. 保存并部署

---

## ⚙️ 关键配置说明

### CORS 跨域
后端已配置为允许：
- 本地开发：`localhost:3000`, `localhost:5173`
- Cloudflare Pages：所有 `*.pages.dev`
- 自定义域名：通过 `FRONTEND_URL` 环境变量

### API URL 切换
- **开发**：`npm run dev` 使用 Vite 代理 `/api` → `localhost:8000`
- **生产**：前端构建时读取 `VITE_API_URL`，指向 Railway 后端

### 数据库
- 默认 SQLite（文件存储在 Railway Volume）
- 生产建议：Railway 提供一键 PostgreSQL，修改 `DATABASE_URL` 即可

---

## 🔗 部署后访问地址

| 服务 | 地址示例 |
|------|----------|
| 前端 | `https://cs-teachable-agent.pages.dev` |
| 后端 API | `https://cs-teachable-agent.up.railway.app/api/docs` |
| 健康检查 | `https://cs-teachable-agent.up.railway.app/api/health` |

---

## 📖 详细文档

- **[DEPLOY_CF_RAILWAY.md](DEPLOY_CF_RAILWAY.md)** — 完整部署步骤、FAQ、故障排查
- **[DEPLOY.md](DEPLOY.md)** — 其他部署方案（Streamlit、自托管）
- **[README.md](README.md)** — 项目概述和快速开始

---

## ✅ 部署检查清单

部署前确认：
- [ ] 代码已推送到 GitHub
- [ ] Railway 项目已创建，正在部署
- [ ] Railway 环境变量 `SECRET_KEY` 已设置
- [ ] Railway 后端 URL 可访问 (`/api/health` 返回 OK)
- [ ] `frontend/.env.production` 已创建并配置正确的 `VITE_API_URL`
- [ ] Cloudflare Pages 构建设置正确
- [ ] Cloudflare Pages 环境变量 `VITE_API_URL` 已设置
- [ ] CORS 包含 Cloudflare Pages 域名

---

## 💡 后续优化建议

1. **自定义域名**：
   - Cloudflare Pages：支持免费自定义域名（在 Pages 设置中添加）
   - Railway：支持自定义域名（Settings → Networking）

2. **数据库升级**：
   - 在 Railway 添加 PostgreSQL 服务
   - 修改 `DATABASE_URL` 为 PostgreSQL 连接字符串

3. **HTTPS**：
   - Cloudflare Pages 自动 HTTPS
   - Railway 自动 HTTPS
   - 无需额外配置

4. **CDN 加速**：
   - Cloudflare 全球 CDN 已启用
   - 静态资源自动缓存

---

**需要帮助？** 查看 [DEPLOY_CF_RAILWAY.md](DEPLOY_CF_RAILWAY.md) 的故障排查部分。
