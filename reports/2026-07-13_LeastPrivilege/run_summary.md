# 2026-07-13 最小权限（Least Privilege）交付记录

- 运行时间：2026-07-13 23:18 CST
- Automation：每日AI概念精讲HTML (`ai-pdf`)
- 主题：最小权限（Least Privilege）——为什么 AI 会思考，不等于它应该拥有所有按钮？
- 知识路径：承接 2026-07-12 的系统提示词（谁为 AI 规定工作方式），转入 Agent 的真实行动边界（AI 实际被允许做什么）。避免重复既有的 Function Calling、Tool Use、AI Workflow、Agent、MCP 与 Prompt Injection 选题。

## 成品

- `2026-07-13_最小权限（Least Privilege）.html`
- `2026-07-13_最小权限（Least Privilege）.pdf`
- `assets/least-privilege-boundary.png`
- `assets/least-privilege-approval-flow.png`
- `html_preview.png`

## 图解

- 两张图均使用 ChatGPT Image 2.0 生成，随后复制进本报告的 `assets/` 并嵌入 HTML/PDF。
- 图 1 解释“查询订单只需读权限；付款、导出通讯录、改账户设置应隔离”。
- 图 2 解释“先读、后确认、再执行、留痕”的差旅 Agent 行动链。

## 验证

- HTML parser：9 个 `h2`、8 个目录锚点、2 张图片、0 个脚本；九段必需结构均在。
- PDF：8 页 A4、未加密、4,890,604 bytes。
- `pdfimages -list`：两张嵌入图均为 1672×941。
- `pdftotext`：确认主题、关键术语、八段正文、人工确认与作用域等核心内容可提取。
- 全页 HTML 预览已目视检查：中文无乱码，图文排版完整，无重叠或裁切。

## 来源

- NIST CSRC：Least Privilege glossary。
- OpenAI Help Center：ChatGPT Workspace Agents（审批与 connector action constraints）。
- Model Context Protocol：Authorization（scope minimization 与 step-up authorization）。
- OpenAI：Running Codex safely at OpenAI（边界、审批与遥测）。

## 发送

- Gmail message/thread id：`19f5c0ef42b135da`。
- Sent 搜索与摘要回读确认两个收件人：`pangdong@sf-express.com`、`seekiingforhappiness@gmail.com`。
- 邮件主题：`【AI每日深度科普】最小权限：为什么 AI 不该拥有所有按钮？`。
- 附件：PDF（4,890,604 bytes）与 HTML（19,248 bytes）。

## 建议下一讲

- OAuth 授权范围（OAuth Scopes）：延续“最小权限”，进一步讲“登录了 ≠ 可以访问所有数据；授权范围、时效与撤销如何工作”。
