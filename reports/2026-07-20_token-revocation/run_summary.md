# 2026-07-20 令牌撤销（Token Revocation）交付记录

- 完成时间：2026-07-20 08:17:34 CST
- Automation：每日 AI 概念精讲 HTML（`ai-pdf`）
- 最终状态：`sent_verified`
- 今日概念：**令牌撤销（Token Revocation）**——卸载 AI 助手后，旧授权真的收回了吗？

## 选题与知识地图

- 选题理由：2026-07-19 的 PKCE 解释“如何安全换到第一张 Token”；本讲沿同一 OAuth 安全路径解释“已经签发的授权何时、如何收回”。它直接连接此前的 OAuth Scopes、Access Token、Refresh Token 与 PKCE，避免重复前几日概念。
- 知识路径：最小权限 → OAuth Scopes → Access Token → Refresh Token → PKCE → **Token Revocation** → DPoP → OAuth Authorization Server Metadata。
- 前置知识：理解 scope、Access Token、Refresh Token 与授权服务器的基本职责。
- 本讲后的下一步：DPoP（复制令牌后的重放防护）；OAuth Authorization Server Metadata（端点与能力发现）；OAuth Token Introspection（资源服务器如何在线查询令牌状态）。

## 研究与教学内容

- 一手依据：RFC 7009、RFC 9700、RFC 6749；Google Account 的第三方访问和账户连接管理官方帮助页。
- 核心边界：撤销可阻止未来使用/续发并可按策略连带处理相关令牌；它不等于第三方已取得数据的删除，也不保证每个分布式节点同一时刻完成状态同步。
- 真实案例：Google Account 的“移除访问权限”。文稿明确标注为产品层场景，不宣称每类 Google 连接都对应 RFC 7009 的同一 HTTP 调用。

## 产物

- 目录：`/Users/mac/Desktop/AI论文解读/reports/2026-07-20_token-revocation/`
- `report.html`：34,841 bytes；自包含 UTF-8、内联 CSS、3 个内联 SVG、0 脚本、0 `src` 本地/外部资源依赖。
- `2026-07-20_令牌撤销.pdf`：626,350 bytes；11 页 A4（595.276 × 841.89 pt）、未加密。
- `sources.md`、`email_subject.txt`、`email_body.txt`、`pdf_text.txt`、本文件与空 `assets/` 目录均已具备。

## 三个教学视觉模块

1. “物业档案 + 管理员钥匙 + 当日门禁卡”类比图：对应授权许可、Refresh Token、Access Token 与撤销级联边界。
2. “触发 → 认证 → 失效 → 资源服务器拒绝”流程图：包含传播延迟与在线/离线校验的取舍。
3. 生命周期工具箱对比图：令牌撤销、过期、应用登出与 DPoP 的职责和不能保证的事。

## 验证结果

- HTML：`HTMLParser` 通过；标题页 + 13 个固定教学章节（14/14）齐全；3 个 SVG 以 XML 解析通过；无 JavaScript、无 `src` 资源、无 PKCE/CDFM 等旧主题残留。
- PDF：从同一 HTML 导出；`pdfinfo` 有效、11 页 A4、未加密；`pdftotext` 能找到全部 13 个教学章节；最终 PDF 用 Poppler 渲染为 11 张 PNG 并逐页视觉检查。
- PDF 视觉：修复步骤编号与标题的间距后重新冻结；最终版无空白尾页、裁切、重叠或不可读的图表/表格。
- 浏览器：通过临时本地 HTTP 服务而非 `file://` 验证。1280×900：文档 `scrollWidth/clientWidth = 1280/1280`、控制台无错误；390×844：`390/390`、控制台无错误。三张宽 SVG 仅在各自图框内部（356px / 714px）横向滚动；正文页面无横向溢出。临时服务器与预览页均已清理。

## 邮件发送与 Sent 回读

- 发送预检：精确 Sent 查询 `in:sent subject:"【AI每日深度科普】令牌撤销：卸载 AI 助手后，旧授权真的收回了吗？" has:attachment` 返回 0 条，未重发旧邮件。
- Gmail Message ID / Thread ID：`19f7ce23d75cfb1c`
- 主题：`【AI每日深度科普】令牌撤销：卸载 AI 助手后，旧授权真的收回了吗？`
- 收件人：`pangdong@sf-express.com`、`seekiingforhappiness@gmail.com`
- Sent 回读：主题、两个收件人、正文和附件均已确认；附件为 `report.html`（34,841 bytes，`text/html`）与 `2026-07-20_令牌撤销.pdf`（626,350 bytes，`application/pdf`）。

## Proof gap 与可复用重试路径

- Proof gap：Gmail 连接器无法证明收件人实际打开或阅读；其余产物、桌面/移动浏览器、发送与 Sent 回读均已验证。
- 重试路径：无需重建内容。若用户要求重发，先以精确主题和上述 Message ID 查询 Sent；确认需要后，复用本目录的 PDF、HTML 与 `email_body.txt`。
