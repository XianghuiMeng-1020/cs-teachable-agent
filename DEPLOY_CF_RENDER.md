# Cloudflare Pages + Render 部署指南

## 架构

- **前端** → Cloudflare Pages（全球 CDN，免费）
- **后端** → Render（Python/FastAPI，免费 tier）

---

## 第一步：部署后端到 Render

### 1.1 创建 Render Web Service

1. 登录 [Render Dashboard](https://dashboard.render.com)
2. 点击 **New** → **Web Service**
3. 连接你的 GitHub 仓库
4. Render 会检测到 `render.yaml`，自动配置

### 1.2 手动配置（如不使用 render.yaml）

| 配置项 | 值 |
|--------|-----|
| **Name** | `cs-teachable-agent-api` |
| **Runtime** | Docker |
| **Dockerfile Path** | `./Dockerfile.backend` |
| **Plan** | Free |
| **Health Check Path** | `/api/health` |

### 1.3 环境变量

在 Render 设置 → Environment 中添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `SECRET_KEY` | 随机字符串 | JWT 密钥（`openssl rand -hex 32` 生成） |
| `FRONTEND_URL` | `https://your-project.pages.dev` | 前端域名，用于 CORS |
| `OPENAI_API_KEY` | `sk-...` | （可选）OpenAI API 密钥 |
| `DEEPSEEK_API_KEY` | `sk-...` | （可选）DeepSeek API 密钥 |
| `ENVIRONMENT` | `production` | 生产环境标记 |

### 1.4 持久化存储

Render 免费 tier 不支持持久化磁盘。数据库选项：

- **免费 tier**：SQLite 存在容器内（重新部署时数据丢失，适合演示）
- **推荐**：Render PostgreSQL（$7/月）或 Supabase 免费 PostgreSQL
  - 设置 `DATABASE_URL=postgresql://user:pass@host:5432/dbname`

### 1.5 验证

部署完成后访问：`https://cs-teachable-agent-api.onrender.com/api/health`

应返回 `{"status": "ok"}`

---

## 第二步：部署前端到 Cloudflare Pages

### 2.1 连接 Cloudflare Pages

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. **Pages** → **Create a project** → **Connect to Git**
3. 选择 GitHub 仓库

### 2.2 构建设置

| 配置项 | 值 |
|--------|-----|
| **Project name** | `cs-teachable-agent` |
| **Production branch** | `main` |
| **Build command** | `cd frontend && npm ci && npm run build` |
| **Build output directory** | `frontend/dist` |

### 2.3 环境变量

| 变量名 | 值 |
|--------|-----|
| `VITE_API_URL` | `https://cs-teachable-agent-api.onrender.com/api` |
| `NODE_VERSION` | `20` |

### 2.4 部署

点击 **Save and Deploy**。完成后获得 `https://cs-teachable-agent.pages.dev`。

---

## 第三步：回填 CORS

在 Render 环境变量中设置：

```
FRONTEND_URL=https://cs-teachable-agent.pages.dev
```

重新部署后端。

---

## 验证清单

- [ ] `https://your-api.onrender.com/api/health` 返回 `{"status": "ok"}`
- [ ] `https://your-frontend.pages.dev` 页面正常显示
- [ ] 可以注册和登录
- [ ] Teach / Test 功能正常

---

## 常见问题

**Q: Render 免费 tier 会休眠吗？**
A: 是的，15 分钟无活动后休眠，下次请求需 ~30s 冷启动。升级到 Starter ($7/月) 可避免。

**Q: 数据会丢失吗？**
A: 免费 tier 使用 SQLite 时，每次部署数据重置。建议使用外部 PostgreSQL。

**Q: 如何更新？**
A: 推送代码到 GitHub，Render 和 Cloudflare Pages 自动重新部署。
