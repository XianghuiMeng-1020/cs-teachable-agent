# 部署配置总结

已配置 **Cloudflare Pages + Render** 完整部署。

---

## 📁 部署相关文件

| 文件 | 用途 |
|------|------|
| `render.yaml` | Render Blueprint 部署配置（Docker 构建） |
| `Dockerfile.backend` | 后端 Docker 镜像 |
| `frontend/wrangler.toml` | Cloudflare Pages 配置 |
| `frontend/.env.production` | 前端生产环境变量（指向 Render 后端） |
| `DEPLOY_RENDER_CF.md` | 📖 详细部署指南 |
| `.github/workflows/deploy.yml` | GitHub Actions 自动部署 |

---

## 🚀 快速开始

### 第 1 步：部署后端（Render）

1. 登录 [Render Dashboard](https://dashboard.render.com)
2. 点击 **New → Blueprint** → 连接 GitHub 仓库
3. Render 自动读取 `render.yaml`，创建 `cs-teachable-agent-api` 服务
4. 设置环境变量：`FRONTEND_URL`, `OPENAI_API_KEY`/`DEEPSEEK_API_KEY`

Render 后端 URL：
```
https://cs-teachable-agent-api.onrender.com
```

### 第 2 步：部署前端（Cloudflare Pages）

前端通过 Cloudflare Pages Git 集成自动部署，或手动：
```bash
cd frontend && npm ci && npm run build
npx wrangler pages deploy dist --project-name=cs-teachable-agent
```

---

## 🌍 线上地址

| 服务 | URL |
|------|----------|
| 前端 | `https://cs-teachable-agent.pages.dev` |
| 后端 API | `https://cs-teachable-agent-api.onrender.com/api/docs` |
| 健康检查 | `https://cs-teachable-agent-api.onrender.com/api/health` |

---

## ✅ 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] Render 服务已通过 Blueprint 创建
- [ ] Render 环境变量 `SECRET_KEY`, `OPENAI_API_KEY` 已设置
- [ ] Render 后端健康检查通过 (`/api/health` 返回 OK)
- [ ] Cloudflare Pages 构建并部署成功
- [ ] 前端登录流程正常
