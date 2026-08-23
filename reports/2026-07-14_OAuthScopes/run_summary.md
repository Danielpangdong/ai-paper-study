# 2026-07-14 OAuth 授权范围（OAuth Scopes）交付记录

- 运行时间：2026-07-14 08:17:44 CST
- Automation：每日AI概念精讲HTML (`ai-pdf`)
- 主题：OAuth 授权范围（OAuth Scopes）——登录后，AI 到底能碰什么？
- 选题理由：承接 2026-07-13 的“最小权限”，把抽象原则落到用户能看见、授权服务器能签发、资源服务器能执行的权限边界；Sent 预检未发现同主题邮件。
- 知识路径：系统提示词（行为说明）→ 最小权限（拥有多少能力）→ OAuth Scopes（外部系统实际批准哪些访问范围）→ Access Token 与 PKCE（令牌如何安全流转）。

## 成品

- `report.html`：自包含、无外部 CSS/脚本依赖。
- `2026-07-14_OAuth授权范围.pdf`：7 页 A4。
- `sources.md`：5 个一手规范/官方来源及关键事实边界。
- `email_subject.txt`、`email_body.txt`。
- `assets/`：本期不需要位图资源；3 个教学图均为内联 SVG。

## 教学视觉

1. “夜班值班证”类比图：任务 → 范围清单 → 门禁逐项放行/拒绝。
2. OAuth 授权流程图：最小申请 → 用户确认 → 实际获批范围 → 资源服务器核验。
3. 认证 / Scope / 资源策略三层对比图，配合移动端可横向阅读的对照表。

## 验证

- HTML：UTF-8 与 HTMLParser 通过；13/13 正文固定章节、3 个 SVG、0 个脚本；标题页合计为第 14 个规定内容项。
- 桌面浏览器：1440×1080 检查封面和相近概念页，无重叠、裁切或文字过小。
- 移动端：390×844 检查封面与对照表；页面级 `scrollWidth=390`，无横向溢出。宽表保留原字号、容器内横向滚动，并显示阅读提示。
- PDF：A4（594.96×841.92 pt）、7 页、未加密、1,916,596 bytes；渲染页已目视检查，避免卡片跨页和空白尾页。
- HTML/PDF 一致性：`pdftotext` 可提取 13/13 个核心章节，PDF 与 HTML 均为自包含视觉内容。

## 发送

- Gmail Message ID / Thread ID：`19f5dfc51b37164f`。
- 邮件主题：`【AI每日深度科普】OAuth 授权范围：登录后，AI 到底能碰什么？`
- Sent 回读：已确认收件人 `pangdong@sf-express.com`、`seekiingforhappiness@gmail.com`，及附件 `report.html`（33,860 bytes）与 `2026-07-14_OAuth授权范围.pdf`（1,916,596 bytes）。

## Proof gap

- 已生成、已验证、已发送、Sent 回读均完成。
- 未验证收件人实际打开/阅读；Gmail 连接器不提供该级别的收件人行为证明。
- 文中 scope 示例仅用于教学，具体名称与语义应以各授权服务器的官方文档和同意页为准。

## 下一讲建议

1. Access Token 与 PKCE：令牌为何不应直接暴露在浏览器地址里。
2. Refresh Token：一次授权为什么可能持续有效，怎样撤销与轮换。
3. Token Audience（受众限制）：同一张令牌为什么不该被转交给别的服务。
