# Sources — Token Revocation（令牌撤销）

生成日期：2026-07-20（Asia/Shanghai）

## 一手标准与官方产品资料

1. [RFC 7009 — OAuth 2.0 Token Revocation](https://www.rfc-editor.org/info/rfc7009/)
   - 支撑：实现必须支持 Refresh Token 撤销、应支持 Access Token 撤销；撤销请求的 HTTPS/POST 约束；`token` 与可选 `token_type_hint`；客户端与令牌归属检查；HTTP 200 对有效/无效令牌的语义；传播延迟；级联策略；在线与离线验证的撤销取舍。
2. [RFC 9700 — Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html)
   - 支撑：Refresh Token 的风险、公共客户端的轮换或发送者绑定、在密码变更和授权服务器注销等安全事件中可能自动撤销、短期 Access Token 降低泄露影响。
3. [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/info/rfc6749/)
   - 支撑：Access Token、Refresh Token、authorization grant、authorization server、client、resource server 的基础角色与定义。
4. [Google Account Help — Share some access to your Google Account data with third-party apps](https://support.google.com/accounts/answer/14012355?hl=en-EN)
   - 支撑：用户可查看或移除第三方应用访问；移除后应用不能继续访问 Google Account；已被第三方取得的数据可能需要另行要求删除。
5. [Google Account Help — Manage links between your Google Account and apps from other developers](https://support.google.com/accounts/answer/13533235?hl=en)
   - 支撑：账户连接管理页面中的移除访问操作以及由此造成的功能变化。

## 事实、类比与推断的边界

- **事实**：以上标准与官方帮助页直接陈述的协议要求、响应语义、产品可见行为与安全建议。
- **类比**：物业档案、管理员钥匙、当日门禁卡均用于解释授权许可、Refresh Token 和 Access Token；它们不是实际系统的物理结构。
- **教学推断**：Google 账户中“移除访问”的产品动作说明了收回授权的用户价值，但本文不声称每类 Google 连接都通过 RFC 7009 的同一端点或同一内部实现完成。
- **实现差异**：撤销级联范围、Access Token 是否可即时拒绝、传播窗口、客户端认证和数据删除策略应以具体身份提供方当前文档为准。
