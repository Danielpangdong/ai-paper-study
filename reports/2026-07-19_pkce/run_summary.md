# 2026-07-19 PKCE（Proof Key for Code Exchange）交付记录

- 完成时间：2026-07-19 08:13:36 CST
- Automation：每日AI概念精讲HTML (`ai-pdf`)
- 今日概念：PKCE（Proof Key for Code Exchange）——授权码被截获，为什么偷到的人仍换不到令牌？
- 选题理由：承接 2026-07-17 的 Access Token 与 2026-07-18 的 Refresh Token。前两讲回答“调用 API 用什么凭据”与“过期后怎样续证”；本讲回答“第一张 Token 前的授权码怎样安全兑换”。
- 知识路径：最小权限 → OAuth Scopes → Access Token → Refresh Token → **PKCE** → Token Revocation → DPoP。
- 前置知识：理解 scope、授权码、Access Token 与 Refresh Token 的基本职责即可。
- 发送预检：发送前两次查询 `in:sent subject:"【AI每日深度科普】PKCE" has:attachment`，均无既有匹配邮件，因此没有重发旧产物。

## 产物

- `report.html`：33,664 bytes，自包含 UTF-8 HTML；内联 CSS、3 个内联 SVG、0 个脚本、0 个 `src` 资源依赖。
- `2026-07-19_PKCE.pdf`：12 页 A4、636,043 bytes、未加密。
- `sources.md`：RFC 7636、RFC 8252、RFC 9700 与 Google 安装应用 OAuth 官方文档，列明事实、类比与教学推演的边界。
- `email_subject.txt`、`email_body.txt`、`pdf_text.txt`、`assets/`（本期不需要位图资源）。

## 教学视觉

1. “寄存柜回执 + 取件暗号”生活类比图：原始 verifier、challenge、授权码回执与截获者的边界。
2. “输入 → 绑定 → 核验 → 输出”流程图：生成 verifier、S256 challenge、授权码回调与 Token Endpoint 比对。
3. 安全链路岗位图：PKCE 与 `state`、Client secret、Access Token、DPoP 的阶段和职责对比，附详细对照表。

## 验证

- HTML：`HTMLParser` 通过；13/13 固定章节完整；3 个 SVG；无脚本和外部资源依赖；未发现旧主题标题、日期或示例残留。
- PDF：最终冻结后 `pdfinfo` 确认 A4（595.276×841.89 pt）、12 页、未加密；`pdftotext` 找到全部 13 个固定章节。
- PDF 视觉：先用 Poppler 对导出稿全部 13 页逐页检查，并发现仅页脚的空白尾页；移除 print-only 页脚后重新冻结。最终 PDF 已重新渲染，封面、跨页对照表和来源页复核正常，空白尾页消失；其余内容版式未变。
- HTML/PDF 一致性：PDF 从同一 `report.html` 导出；固定章节、核心图文与引用一致。
- 浏览器/移动端：内置浏览器的本地 `file://` 导航被安全策略拒绝，未使用绕过手段。因此 1280px 桌面与 390px 手机的真实浏览器布局检查均为 **未验证**；HTML 已具备响应式窄屏规则、最小宽图横向滚动容器与 390px 阅读提示，但这不是浏览器实测证明。

## 发送与 Sent 回读

- Gmail Message ID / Thread ID：`19f77b729e4f7cf3`
- 主题：`【AI每日深度科普】PKCE：授权码被截获，为什么偷到的人仍换不到令牌？`
- 收件人：`pangdong@sf-express.com`、`seekiingforhappiness@gmail.com`
- Sent 回读：已确认主题、两个收件人、完整正文摘要与附件：`report.html`（33,664 bytes）、`2026-07-19_PKCE.pdf`（636,043 bytes）。

## Proof gap

- 已生成、HTML/PDF 验证、PDF 最终渲染检查、邮件发送、Sent 回读均完成。
- 收件人实际打开/阅读行为不可由 Gmail 连接器确认。
- 本地浏览器安全策略阻止 `file://`，所以桌面与 390px 移动端的真实浏览器布局验证缺失；不要将响应式 CSS 的静态存在误报为实测通过。
- “AI 日历/文档助手”均为基于一手 OAuth 文档的教学场景，不主张具体产品采用相同配置。

## 后续候选

1. Token Revocation：用户撤销授权后，令牌与会话为何不一定同时失效。
2. DPoP：令牌已经签发后，怎样绑定持有者、降低复制后的重放风险。
3. OAuth Authorization Server Metadata：客户端如何发现服务器的端点、PKCE 能力和支持方法。
