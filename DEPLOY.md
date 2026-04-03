# ARTS-CS 部署指南

**架构**: Cloudflare Pages（前端 CDN） + Render（后端 FastAPI）

---

## 部署文件清单

| 文件 | 用途 |
|------|------|
| `render.yaml` | Render Blueprint 自动部署配置 |
| `Dockerfile.backend` | 后端 Docker 镜像（含弹性启动） |
| `start.py` | 弹性启动包装器（错误时降级为诊断服务器） |
| `frontend/.env.production` | 前端生产环境变量 |
| `frontend/wrangler.toml` | Cloudflare Pages 配置参考 |
| `.github/workflows/deploy.yml` | GitHub Actions CI/CD |

---

## 第一步：部署后端到 Render

### 1.1 Blueprint 部署（推荐）

1. 登录 [Render Dashboard](https://dashboard.render.com)
2. **New** → **Blueprint** → 连接 GitHub 仓库
3. Render 自动读取 `render.yaml`，创建 `cs-teachable-agent-api` 服务
4. 首次部署需 3-5 分钟

### 1.2 环境变量

在 Render → Web Service → Environment 中配置：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `SECRET_KEY` | 自动生成 | JWT 密钥（render.yaml 已配置自动生成） |
| `DATABASE_URL` | `sqlite:///./data/app.db` | 已在 render.yaml 中配置 |
| `ENVIRONMENT` | `production` | 已在 render.yaml 中配置 |
| `FRONTEND_URL` | `https://cs-teachable-agent.pages.dev` | **手动设置**，CORS 使用 |
| `OPENAI_API_KEY` | `sk-...` | （可选）OpenAI 密钥 |
| `DEEPSEEK_API_KEY` | `sk-...` | （可选）DeepSeek 密钥 |
| `QWEN_API_KEY` | `sk-...` | （可选）Qwen 密钥 |

> 至少配置一个 LLM API Key 以启用 AI 对话功能。

### 1.3 验证

```bash
curl https://cs-teachable-agent-api.onrender.com/api/health
# 应返回: {"status":"ok","version":"2.0.0","cors":"CORSEverythingMiddleware"}
```

---

## 第二步：部署前端到 Cloudflare Pages

### 2.1 Cloudflare Pages Git 集成

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com) → **Pages** → **Create a project**
2. 选择 **Connect to Git** → 授权 GitHub → 选择仓库
3. 构建配置：

| 配置项 | 值 |
|--------|-----|
| **Project name** | `cs-teachable-agent` |
| **Production branch** | `main` |
| **Build command** | `cd frontend && npm ci && npm run build` |
| **Build output directory** | `frontend/dist` |

4. 环境变量：

| 变量名 | 值 |
|--------|-----|
| `VITE_API_URL` | `https://cs-teachable-agent-api.onrender.com/api` |
| `NODE_VERSION` | `20` |

5. 点击 **Save and Deploy**

### 2.2 验证

访问 `https://cs-teachable-agent.pages.dev`，使用 demo 账户登录：
- 学生: `demo_student` / `demo123`
- 教师: `demo_teacher` / `demo123`

---

## 第三步：回填 CORS

后端的 `FRONTEND_URL` 必须与 Cloudflare Pages 实际域名匹配：

```
FRONTEND_URL=https://cs-teachable-agent.pages.dev
```

在 Render Dashboard 设置后，服务会自动重新部署。

---

## 自动部署（CI/CD）

推送代码到 `main` 分支后：
- **GitHub Actions** 运行测试 → 触发 Render Deploy Hook → 构建并部署前端到 Cloudflare Pages
- **Render** 同时监听 GitHub push，自动拉取代码重新构建
- **Cloudflare Pages** 同时监听 GitHub push，自动重新构建前端

> 三方都有独立的 Git 监听，GitHub Actions 作为额外保障层。

---

## 线上地址

| 服务 | URL |
|------|-----|
| 前端 | https://cs-teachable-agent.pages.dev |
| 后端 API 文档 | https://cs-teachable-agent-api.onrender.com/docs |
| 健康检查 | https://cs-teachable-agent-api.onrender.com/api/health |

---

## 故障排查

### 前端空白页
1. 确认 `frontend/public/_redirects` 存在且内容为 `/* /index.html 200`
2. 检查浏览器 DevTools → Network → API 请求地址是否正确

### CORS 错误
1. 检查 Render 环境变量 `FRONTEND_URL` 是否匹配实际前端域名
2. 后端已使用 `CORSEverythingMiddleware` 全放行，正常不应有 CORS 问题

### 后端 500 错误
1. Render Dashboard → Logs 查看详细错误
2. `start.py` 会在应用启动失败时降级为诊断服务器，访问 `/api/debug` 查看错误详情

### Render 冷启动
免费 tier 15 分钟无活动后休眠，下次请求需 ~30s 冷启动。升级到 Starter ($7/月) 可避免。

---

## 本地开发

```bash
# 后端
pip install -r requirements.txt
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# 前端（另一个终端）
cd frontend && npm install && npm run dev
# Vite 开发服务器自动代理 /api → localhost:8000
```

或使用 Docker：

```bash
docker-compose up
```
