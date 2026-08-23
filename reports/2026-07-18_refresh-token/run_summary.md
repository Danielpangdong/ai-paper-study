# 2026-07-18 Refresh Token（刷新令牌）交付记录

- 完成时间：2026-07-18 08:14 CST
- Automation：每日AI概念精讲HTML (`ai-pdf`)
- 今日概念：Refresh Token（刷新令牌）——AI 为什么能在你不在场时继续工作？
- 选题理由：承接 2026-07-17 的 Access Token。上一讲解释“调用 API 时拿什么短期凭证”，本讲解释“短期凭证到期后怎样安全换新”，并强调长期便利与长期秘密风险的边界。
- 发送预检：`in:sent subject:"【AI每日深度科普】Refresh Token" has:attachment` 未发现旧邮件；自动化 memory 当次运行前缺失，但本地上一期已有已验证且 Sent 回读完成的 Access Token 报告，因此未重发旧产物。

## 产物

- `report.html`：自包含中文 HTML；内联 CSS 与 3 个内联 SVG，无脚本、无图片或本地资源依赖。
- `2026-07-18_刷新令牌.pdf`：A4、9 页、1,907,556 bytes。
- `sources.md`：RFC 6749、RFC 9700、RFC 6750、RFC 7009 与 Google OAuth 官方文档，以及事实/类比/推断边界。
- `email_subject.txt`、`email_body.txt`、`pdf_text.txt`、`assets/`。

## 教学视觉

1. “一日工作证与续证合同”生活类比图：Access Token 与 Refresh Token 的保存等级和接收方。
2. “输入 → 核验 → 输出”刷新流程图：API 到期信号、授权服务器刷新与再次调用。
3. Access Token / Refresh Token / ID Token 岗位分工对比图，附四类凭据的对照表。

## 验证

- HTML：UTF-8 与 `HTMLParser` 通过；13/13 固定章节、13 个 H2、3 个 SVG、0 个脚本、0 个 `img`、0 个 `src` 资源依赖。
- 旧主题残留：检查本目录，未发现旧的 Access Token/OAuth Scopes 标题或旧日期残留。
- 桌面浏览器：1280×720 本地 Chromium 加载成功；页面级 `scrollWidth=clientWidth=1280`；标题、13 个章节、3 个 SVG 均可访问。
- 移动端：390×844 本地 Chromium；页面级 `scrollWidth=clientWidth=390`。三张宽图保留可读字号，在各自容器内 356→784px 横向阅读，并显示“手机请左右滑动查看完整图”提示。
- PDF：`pdfinfo` 确认 A4（595.92×842.88 pt）、9 页、未加密；`pdftotext` 找到全部 13 个固定章节。
- PDF 渲染：使用 Poppler 将全部 9 页渲染为 PNG 并逐页目视检查；封面、三张 SVG、术语卡、对照表、误区卡、理解题和来源页均无裁切、重叠或乱码。
- HTML/PDF 一致性：PDF 由同一 HTML 的 print 样式导出；全部固定章节与核心图文一致。移动端提示仅在窄屏 CSS 生效，不影响 PDF 内容。

## 发送与回读

- Gmail Message ID / Thread ID：`19f7292b5be9169d`
- 主题：`【AI每日深度科普】Refresh Token：AI 为什么能在你不在场时继续工作？`
- 收件人：`pangdong@sf-express.com`、`seekiingforhappiness@gmail.com`
- Sent 回读：已确认主题、两个收件人、正文摘要与附件 `report.html`（32,935 bytes）、`2026-07-18_刷新令牌.pdf`（1,907,556 bytes）。

## Proof gap

- 已生成、已验证、已发送、Sent 回读均完成。
- 未验证收件人实际打开或阅读；Gmail 连接器不提供该级别的行为证明。
- 本文的 Google 日历助手是基于官方 OAuth 文档的教学系统案例，不主张任何特定 AI 产品采用完全相同的令牌策略或时长。

## 后续候选

1. PKCE：授权码被截获时，为什么拦截者换不到令牌。
2. Token Revocation：用户怎样撤销应用授权，为什么撤销不一定瞬时体现在所有系统。
3. DPoP：怎样把令牌绑定到持有者，降低“捡到就能用”的风险。
