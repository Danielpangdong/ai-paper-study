# Refresh Token（刷新令牌）来源与事实边界

## 一手来源

1. [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
   - §1.5：Refresh Token 是用来获得 Access Token 的凭据；当前 Access Token 无效或过期时可取得新的 Access Token。
   - §1.5、图 2、§6：Refresh Token 由授权服务器签发，只发给/使用于授权服务器，不给资源服务器；刷新时授权服务器可返回新的 Access Token 和可选的新 Refresh Token。
   - §10.4：Refresh Token 必须在传输与存储中保密，并绑定到签发给它的客户端。
2. [RFC 9700 — Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700)
   - §2.2.2：公共客户端 Refresh Token 必须采用 sender-constrained 或 refresh token rotation。
   - §4.14：Refresh Token 对攻击者有吸引力；签发应基于风险评估，绑定用户同意的 scope 和资源服务器；轮换可帮助发现重放。
3. [RFC 6750 — Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
   - Bearer Token 的持有者即可使用，因此机密性和 TLS 传输非常重要。
4. [RFC 7009 — OAuth 2.0 Token Revocation](https://www.rfc-editor.org/rfc/rfc7009)
   - 定义授权服务器的 token revocation endpoint；支持撤销 Access Token 或 Refresh Token。
5. [Google for Developers — OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)
   - 离线访问时可获得 Refresh Token；短期 Access Token 到期后可用 Refresh Token 换新；令牌需要安全、长期保存，可能被撤销或失效。

## 事实、类比、推断的边界

- **事实**：协议中的角色、令牌用途、传输边界、轮换/撤销建议，均由上述 RFC 或 Google 官方文档支持。
- **类比**：一日工作证、续证合同、仓库前台仅用于建立直觉，不描述真实令牌的数据格式或实现细节。
- **推断**：AI Agent 应把模型推理与秘密存储、刷新和高影响操作确认分离，是基于最小权限和凭据保护原则的工程建议；并非某个 RFC 对某一产品的强制架构。
