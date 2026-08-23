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
