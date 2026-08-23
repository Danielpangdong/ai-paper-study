# 2026-07-17 Access Token（访问令牌）交付记录

- 运行时间：2026-07-17 08:12:58 CST
- Automation：每日AI概念精讲HTML (`ai-pdf`)
- 主题：访问令牌（Access Token）——AI 怎么被允许替你调用外部服务？
- 选题理由：承接 2026-07-14 的 OAuth Scopes。上一讲回答“用户允许什么范围”，本讲回答“应用实际拿什么凭证调用 API”；Sent 预检未发现同主题邮件。
- 知识路径：系统提示词 → 最小权限 → OAuth Scopes → Access Token → PKCE / Refresh Token → Audience。

## 成品

- `report.html`：自包含、无脚本和资源依赖的中文 HTML。
- `2026-07-17_访问令牌.pdf`：9 页 A4 PDF。
- `sources.md`：5 个 IETF/Google 一手来源及关键事实边界。
- `email_subject.txt`、`email_body.txt`、`pdf_text.txt`。
- `assets/`：本期不需要位图资源；3 个教学视觉均为内联 SVG。

## 教学视觉

1. “图书馆限时取书证”类比图：任务 → 授权服务台 → 日历 API 柜台。
2. “输入 → 核验 → 输出”流程图：用户、AI 客户端、授权服务器、资源服务器的令牌链路。
3. Access Token / ID Token / Refresh Token 的岗位分工对比图。

## 验证

- HTML：UTF-8 与 `HTMLParser` 通过；13/13 固定章节完整、3 个内联 SVG、0 个脚本、0 个 `src` 资源引用，31,355 bytes。
- 桌面浏览器：1440×1080 本地 Chromium 渲染；标题、13 个 H2 与 3 个 SVG 均存在，`scrollWidth=clientWidth=1440`。截图：`/Users/mac/Desktop/AI论文解读/output/playwright/access-token-desktop.png`。
- 移动端：390×844 本地 Chromium 渲染；`scrollWidth=clientWidth=390`，无页面级横向溢出。宽对照表在可滚动容器中保留可读字号。截图：`/Users/mac/Desktop/AI论文解读/output/playwright/access-token-mobile.png`。
- PDF：A4（595.92×842.88 pt）、9 页、未加密、1,848,954 bytes；使用 Poppler 渲染页目视检查，首图、流程图、理解题与来源页均无裁切、重叠或分裂卡片。
- HTML/PDF 一致性：`pdftotext` 可提取 13/13 固定章节；PDF 由同一份 HTML 的 print CSS 导出。

## 发送

- Gmail 预检：`in:sent subject:"【AI每日深度科普】Access Token"` 无旧邮件。
- Gmail Message ID / Thread ID：`19f6d6ae0985f28f`。
- 邮件主题：`【AI每日深度科普】Access Token：AI 怎么被允许替你调用外部服务？`
- Sent 回读：已确认收件人 `pangdong@sf-express.com`、`seekiingforhappiness@gmail.com`，附件 `report.html`（31,355 bytes）与 `2026-07-17_访问令牌.pdf`（1,848,954 bytes）。

## Proof gap

- 已生成、已验证、已发送、Sent 回读均完成。
- 未验证收件人实际打开/阅读；Gmail 连接器不提供该级别的行为证明。
- 文中“日历助手”是基于 Google OAuth/API 文档的教学系统案例，不主张任何特定 AI 产品当前使用相同架构。

## 下一讲建议

1. PKCE：授权码被截获时，为什么偷到的人换不到令牌。
2. Refresh Token：短期 Access Token 到期后怎样安全换新、撤销与轮换。
3. Token Audience：为什么同一令牌不能随便交给另一个 API。
