# PKCE（Proof Key for Code Exchange）来源与事实边界

生成日期：2026-07-19

## 一手来源

1. [RFC 7636 — Proof Key for Code Exchange by OAuth Public Clients](https://www.rfc-editor.org/rfc/rfc7636.html)
   - PKCE 旨在缓解公开客户端的 authorization code interception attack。
   - 每次授权请求生成 `code_verifier`；派生 `code_challenge`；Token Endpoint 用 verifier 重新计算并比较。
   - `code_verifier` 的格式范围是 43–128 个未保留字符；S256 为 `BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))`。
   - 能使用 S256 的客户端必须使用 S256；不匹配应返回 `invalid_grant`。

2. [RFC 8252 — OAuth 2.0 for Native Apps](https://www.rfc-editor.org/rfc/rfc8252.html)
   - 原生应用的 URI 回调可能发生授权码拦截；PKCE 使截获者在没有 verifier 时无法兑换 code。
   - 对公开原生应用，规范说明客户端和服务器使用 PKCE 的最佳实践背景。

3. [RFC 9700 — Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html)
   - 公开客户端必须使用 PKCE；保密客户端也建议使用。
   - 客户端应使用不在初始授权请求中暴露 verifier 的挑战方法；当前 S256 是此类方法。
   - 授权服务器必须正确执行 verifier 校验，并防范 PKCE downgrade attack。

4. [Google for Developers — OAuth 2.0 for iOS & Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
   - Google 的安装应用 OAuth 文档说明每个授权请求生成唯一 verifier 与 challenge。
   - 文档给出 S256、`code_challenge`、`code_challenge_method`、`state` 与 Token 请求中 `code_verifier` 的具体参数语境。

## 事实、类比与推演

- **事实**：协议流程、参数含义、公式、长度范围、S256 首选与当前安全建议均由上列一手材料支持。
- **类比**：报告中的“寄存柜回执 + 取件暗号”是解释性类比。它不是密码学或授权服务器存储策略的技术描述。
- **推演**：AI 日历助手和 AI 文档助手是教学场景，说明安装式 AI 工具连接第三方 API 时为何受益；不主张任何具体产品使用了特定 OAuth 配置，也不构成安全保证。
