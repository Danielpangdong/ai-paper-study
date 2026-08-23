# OAuth 授权范围（OAuth Scopes）来源与关键事实

检索日期：2026-07-14（Asia/Shanghai）

| 来源 | 用途与可核验事实 |
|---|---|
| [RFC 6749 — OAuth 2.0](https://www.rfc-editor.org/rfc/rfc6749) | §3.3：scope 是由授权服务器定义的、空格分隔、大小写敏感的字符串集合；每个字符串增加访问范围。授权服务器可部分或全部忽略请求范围；实际授予范围不同于请求范围时必须在响应中带回 `scope`。§4.1：授权码流程中的角色与基本步骤。 |
| [RFC 9700 — OAuth 2.0 Security BCP](https://www.rfc-editor.org/info/rfc9700/) | §2.3：访问令牌的权限应限制为特定应用/用例的最小所需；应限制到具体资源服务器、资源和动作，以降低令牌泄露的影响。§2.1.1：PKCE 的现行安全实践。 |
| [Google OAuth 2.0 Authorization](https://developers.google.com/identity/protocols/oauth2) | 文档说明：应用获得令牌后应核对实际获批 scopes；范围只覆盖令牌请求描述的操作/资源；建议在需要时增量申请，而非预先请求。 |
| [Google — Handle granular permissions](https://developers.google.com/identity/protocols/oauth2/resources/granular-permissions) | 建议只请求任务所需的特定范围；避免首次登录时捆绑多个范围；检查用户实际批准了哪些范围；在用户明确要用该功能时再请求。页面最后更新 2026-05-26。 |
| [MCP Authorization Specification (2025-11-25)](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) | MCP 客户端应遵从最小权限；支持按需升级范围；资源服务器应验证令牌是否为自己签发；不足 scope 的运行时请求应返回 403 与所需范围提示。 |

## 写作边界

- `calendar.read`、`mail.delete` 等是教学示意；OAuth 不为所有服务统一规定 scope 的业务词义。
- “范围小可减小泄露影响”是协议安全实践的归纳，不代表小范围令牌没有隐私或业务风险。
- 本文没有声称某一具体 AI 产品当前申请或使用了何种 OAuth 范围。
