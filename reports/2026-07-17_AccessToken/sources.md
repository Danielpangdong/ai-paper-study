# Access Token 来源与关键事实

检索与核对：2026-07-17（Asia/Shanghai）

| 来源 | 用途与可核验事实 |
|---|---|
| [RFC 6749 — OAuth 2.0](https://www.rfc-editor.org/rfc/rfc6749) | §1.4：Access Token 是访问受保护资源的凭证，代表授给客户端的授权，通常对客户端不透明；可代表范围、时长和其他访问属性，并可为后台查询标识或包含可验证数据的字符串。§1.2：客户端取得令牌后向资源服务器提交，资源服务器验证后服务请求。 |
| [RFC 6750 — Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750) | §1：持有 bearer token 的一方无需证明密钥所有权即可使用；令牌需要在存储和传输中避免泄露。 |
| [RFC 7662 — Token Introspection](https://www.rfc-editor.org/rfc/rfc7662) | §2.2：令牌内省响应的 `active` 指示令牌当前是否有效，响应可包含 scope、client_id、aud、exp 等属性；令牌无效、未知或资源服务器无权查询时应返回 `active:false`。 |
| [RFC 9700 — OAuth 2.0 Security BCP](https://www.rfc-editor.org/rfc/rfc9700) | §2.2–2.3：建议对访问令牌做持有者绑定以降低泄露重放风险；令牌权限应限制为特定应用/用例的最小需要，并限制到特定资源服务器、资源和动作；资源服务器应逐请求验证令牌是否面向自己与当前动作。 |
| [Google OAuth 2.0 Authorization](https://developers.google.com/identity/protocols/oauth2) | 取得令牌后，应用应核对实际获批范围；令牌通过 HTTP Authorization 请求头发送；例如给 Calendar API 的令牌不因此获得 Contacts API 权限；令牌寿命有限，必要时可通过 refresh token 取得新令牌。 |

## 写作边界

- “日历助手”是基于官方 OAuth/API 流程的系统级教学案例，不是对任何单一 AI 产品当前架构的断言。
- `read`、`delete`、`calendar` 等措辞是教学示例；真实 scope 名称、令牌格式与到期策略由各授权服务器定义。
- ID Token 的对比仅说明它在 OpenID Connect 身份层的典型职责；本文的主题是 OAuth Access Token。
