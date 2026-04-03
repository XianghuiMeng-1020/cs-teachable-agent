# Render + Cloudflare Pages 部署指南

本文档指导你如何将 **ARTS-CS** (AI Resistant Teaching System for Computer Science) 部署到：
- **前端** → Cloudflare Pages（全球 CDN，免费）
- **后端** → Render（Python/FastAPI 托管，免费额度充足）

> **部署架构**: Render (后端) + Cloudflare Pages (前端)
> - Render 提供免费且稳定的 Python/FastAPI 托管
> - Render 的免费 tier 包含 750 小时/月的运行时间
> - 自动部署 + 健康检查 + 持久化存储支持

---

## 📋 前置要求

1. [Cloudflare 账号](https://dash.cloudflare.com/sign-up)（免费）
2. [Render 账号](https://render.com/signup)（免费）
3. [GitHub 账号](https://github.com/signup)（代码托管）
4. 代码已推送到 GitHub 仓库

---

## 第一步：部署后端到 Render

### 1.1 创建 Blueprint 部署

1. 登录 [Render Dashboard](https://dashboard.render.com)
2. 点击 **"Blueprint"** → **"New Blueprint Instance"**
3. 选择 **"Connect a repository"**
4. 授权 Render 访问你的 GitHub 仓库
5. 选择本项目仓库
6. Render 会自动读取根目录的 `render.yaml` 文件

### 1.2 配置环境变量

在 Render Dashboard 中找到创建的 Web Service，进入 **"Environment"** 标签页，添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `OPENAI_API_KEY` | `sk-...` | （可选）OpenAI API 密钥 |
| `DEEPSEEK_API_KEY` | `sk-...` | （可选）DeepSeek API 密钥 |
| `FRONTEND_URL` | `https://arts-cs.pages.dev` | 前端域名（Cloudflare Pages），用于 CORS |
| `WORKERS_URL` | `https://arts-cs.xmeng19.workers.dev` | （可选）备用前端域名 |

> 💡 **注意**: `SECRET_KEY` 和 `DATABASE_URL` 已在 `render.yaml` 中配置

### 1.3 验证部署

部署完成后，Render 会分配一个域名，例如：
- `https://arts-cs-api.onrender.com`
- 或 `https://cs-teachable-agent-api.onrender.com`

**测试**：访问 `https://<your-domain>/api/health` 应返回：
```json
{"status": "ok", "version": "1.0.0"}
```

---

## 第二步：部署前端到 Cloudflare Pages

### 2.1 更新前端环境变量

在项目根目录确认 `frontend/.env.production` 内容：

```bash
# frontend/.env.production
VITE_API_URL=https://arts-cs-api.onrender.com/api
```

> 如果 Render 给你的后端地址不同，替换为实际的域名。

### 2.2 通过 Dashboard 部署（推荐）

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 点击 **"Pages"** → **"Create a project"**
3. 选择 **"Connect to Git"**
4. 授权 Cloudflare 访问你的 GitHub 仓库
5. 选择本项目仓库
6. 配置构建设置：

| 设置项 | 值 |
|--------|-----|
| **Project name** | `arts-cs`（或你喜欢的名称） |
| **Production branch** | `main` |
| **Build command** | `cd frontend && npm install && npm run build` |
| **Build output directory** | `frontend/dist` |

7. 添加环境变量（在 Pages 设置中）：

| 变量名 | 值 |
|--------|-----|
| `NODE_VERSION` | `20` |

8. 点击 **"Save and Deploy"**

### 2.3 验证前端部署

部署完成后，Cloudflare 会分配一个域名，例如：
- `https://arts-cs.pages.dev`

**测试**：
1. 访问首页应显示 ARTS-CS 登录界面
2. 用 demo 账户 `demo_student` / `demo123` 登录
3. 测试教学、测试、掌握度等功能

---

## 第三步：配置 CORS（关键！）

### 3.1 获取实际域名

确认以下域名：
- **前端 Pages 域名**: `https://arts-cs.pages.dev`（在 Cloudflare Pages 项目设置中查看）
- **后端 Render 域名**: `https://arts-cs-api.onrender.com`（在 Render Dashboard 中查看）

### 3.2 更新 Render 环境变量

在 Render Dashboard → 你的 Web Service → Environment 中更新：

```
FRONTEND_URL=https://arts-cs.pages.dev
```

### 3.3 硬编码 CORS 配置（备用方案）

如果 CORS 仍有问题，编辑 `src/api/main.py`，在 `allowed_origins` 列表中添加：

```python
allowed_origins = [
    # 从环境变量读取
    os.getenv("FRONTEND_URL", ""),
    os.getenv("WORKERS_URL", ""),
    # 硬编码 Render + Cloudflare Pages 域名（作为备用）
    "https://arts-cs.pages.dev",
    "https://arts-cs-api.onrender.com",
    # 本地开发
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

然后提交并推送，Render 会自动重新部署。

---

## 第四步：验证完整部署

### 4.1 API 健康检查

```bash
curl https://arts-cs-api.onrender.com/api/health
```

### 4.2 CORS 预检检查

```bash
curl -H "Origin: https://arts-cs.pages.dev" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://arts-cs-api.onrender.com/api/auth/login -v
```

应看到响应头包含：`access-control-allow-origin: https://arts-cs.pages.dev`

### 4.3 端到端测试

1. 访问 `https://arts-cs.pages.dev`
2. 点击 "Sign in"
3. 使用 demo 账户：
   - 学生：`demo_student` / `demo123`
   - 教师：`demo_teacher` / `demo123`
4. 验证功能：
   - 学生端：Dashboard → Teach TA → Test TA → Mastery → History
   - 教师端：Overview → Students → Transcripts → Analytics

---

## 🔧 故障排查

### 空白页 / 无法加载

1. **检查 SPA fallback**: Cloudflare Pages 需要 `_redirects` 文件
   - 确认 `frontend/public/_redirects` 存在且内容为：
   ```
   /*    /index.html   200
   ```

2. **检查 API URL**: 浏览器 DevTools → Network → 确认 API 请求地址正确

### CORS 错误

1. **检查 Render 环境变量**: `FRONTEND_URL` 必须等于实际 Pages 域名
2. **检查 `src/api/main.py`**: `allowed_origins` 列表是否包含 Pages 域名
3. **重新部署**: 修改后推送代码，Render 会自动重新部署

### API 返回 500

1. 检查 Render Logs: Dashboard → Web Service → Logs
2. 检查数据库是否初始化：首次部署可能需要手动运行迁移
3. 检查环境变量：所有必需变量是否已设置

---

## 📊 部署架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         部署架构 (Render + Cloudflare)              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌──────────────────┐              ┌──────────────────────┐      │
│    │   Cloudflare     │              │   Render             │      │
│    │   Pages          │──────────────│   (FastAPI)          │      │
│    │   (Frontend)     │   HTTPS/API  │   arts-cs-api        │      │
│    │                  │              │   .onrender.com      │      │
│    │   arts-cs.       │◄─────────────│                      │      │
│    │   pages.dev      │   JSON/Data  │   SQLite DB          │      │
│    └──────────────────┘              │   (持久化存储)       │      │
│                                      └──────────────────────┘      │
│                                                                     │
│    ┌──────────────────┐                                           │
│    │   GitHub         │                                           │
│    │   (源码)         │─── 自动部署 ──► Render + Cloudflare       │
│    │                  │                                           │
│    └──────────────────┘                                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 生产环境优化建议

### 1. 数据库迁移
- Render 的免费 tier SQLite 存储在磁盘，可能重启后丢失
- 建议迁移到 PostgreSQL（Render 提供托管 PostgreSQL）

### 2. 监控
- Render 自带健康检查和日志
- 可考虑添加 Sentry 进行错误追踪

### 3. 自定义域名
- Cloudflare Pages：Settings → Custom domains → 添加你的域名
- Render：Settings → Custom domains → 添加你的域名

---

## 📚 相关文档

- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)
- [Render Web Services 文档](https://render.com/docs/web-services)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)

---

**部署状态**: 🟢 前端 Cloudflare Pages + 🟢 后端 Render  
**Demo 地址**: https://arts-cs.pages.dev  
**Demo 账户**: demo_student / demo123（学生）, demo_teacher / demo123（教师）
