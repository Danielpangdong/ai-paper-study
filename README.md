# 📚 AI 论文学习站

把「每日 AI 论文精读」与 `reports/` 下的概念精讲、论文精选，整理成一个可搜索、可筛选、可连续阅读的本地学习网站。

## 使用方式

**直接打开**：双击 `index.html`（或拖进浏览器），无需服务器。
也可以用任意静态服务器：

```bash
cd "AI论文解读" && python3 -m http.server 8000
# 打开 http://127.0.0.1:8000/index.html
```

## 站点结构

| 文件 | 说明 |
| --- | --- |
| `index.html` | 学习站首页：统计、搜索、机构/类型/主题筛选、卡片与时间线视图 |
| `reader.html` | 阅读页：内嵌文章 + 上一篇/下一篇、独立打开、复制链接 |
| `data/papers.js` | 自动生成的文章索引（`window.PAPERS`） |
| `assets/` | 样式与首页逻辑 |
| `tools/build.py` | 索引生成器：扫描全部文章 HTML，提取日期/标题/机构/标签/摘要 |

## 重新生成索引

文章新增或修改后：

```bash
python3 tools/build.py
```

生成器会扫描：
- 顶层 `*.html` → 每日精读（`2026-08-22_xxx解读.html` 这类）
- `reports/*/*.html` → 概念精讲（`2026-05-03_RAG` 下划线目录）与论文精选（连字符目录）

并按标题去重、排除 `reports/source_papers/` 原始抓取页。

## 文章从哪里来

内容为人工 + AI 整理的论文解读笔记（中文），覆盖 Anthropic / OpenAI / DeepMind / Meta 等机构
2026 年 4 月以来的前沿论文与报告，仅供学习交流。

---

## 🚀 发布上线（GitHub Pages + 每日自动更新）

站点已配置好完整的自动发布链路，只需**一次性登录授权 + 建仓推送**：

### 一次性操作（发布前只需做这一步）

```bash
# 1. 登录 GitHub（浏览器弹出授权，选 HTTPS 即可）
gh auth login
gh auth setup-git        # 让 git 使用 gh 的登录凭证

# 2. 在 GitHub 上创建公开仓库并推送（约 370MB，首次推送需几分钟）
gh repo create ai-paper-study --public --source=. --remote=origin --push
```

> 私有仓库也行：`--private`。之后想改仓库名，改完同步改设置里的路径即可。

### 3. 开启 Pages 部署（约 30 秒）

浏览器打开 `https://github.com/<你的用户名>/ai-paper-study/settings/pages`：
- **Source** 选择 **`GitHub Actions`**（不是 Deploy from a branch！）
- 工作流文件 `.github/workflows/pages.yml` 已备好，推送后会自动触发部署

### 4. 访问网站

`https://<你的用户名>.github.io/ai-paper-study/`

### 日常自动更新（已配置，无需干预）

| 环节 | 机制 |
| --- | --- |
| 每日 09:30 / 14:30 | crontab 自动运行 `tools/site-update.sh` |
| 重建索引 | 脚本先执行 `tools/build.py`，有新文章才有变更 |
| 提交推送 | 有变更才 commit + push（确定性构建，无文章时自动跳过） |
| 自动部署 | GitHub Actions 检测到 push 即重新部署 Pages（约 1 分钟） |

查看更新日志：`tools/logs/site-update.log`；手动更新一次：`bash tools/site-update.sh`。

### 仓库体积说明

- `.gitignore` 已排除约 **774MB** 的本地 PDF 离线存档（网页文章引用的是外网 PDF，不影响展示）
- 线上仓库 ≈ **370MB**（文章 HTML + 配图），属 GitHub 正常范围；后续每日推送只有几 KB
- 想进一步瘦身可启用 Git LFS 托管图片（当前无必要）

### 常见问题

- **push 失败 / 401**：重新 `gh auth login` + `gh auth setup-git`
- **部署后页面空白**：确认 Pages Source 选了 **GitHub Actions**，并在 Actions 页看部署日志
- **想换平台**（Cloudflare Pages / Netlify / Vercel）：它们都支持"连接 GitHub 仓库自动部署"，把仓库公开后按平台向导接入即可，无需改代码

Sun Aug 23 14:38:56 CST 2026
