# 抖音 Web 签名体系逆向结论（2026-06）

## ✅ 已跑通（方案 1：Node 补环境复现 secsdk）

feed 接口已通过纯 Node 补环境的三件套签名拿到 **HTTP 200 + 完整数据**（`Request.getJSON` 端到端验证）：

| 参数 | 生成方式 | 文件 |
|------|---------|------|
| `a_bogus` | bdms 补环境（JSVMP） | `lib/index.js` + `lib/sign_cli.js` |
| `timestamp` + `x-secsdk-web-signature` + `uifid` | secsdk 补环境 | `lib/secsdk_runtime.js` + `lib/websign_env.js` + `lib/websign_index.js` + `lib/sign_websign.js` |

关键结论：
1. **`webSignUrl` 由 `secsdk_runtime.js` 自身注册**（在 `SDKRuntime.global` 里），**无需加载 bdms**，补对环境即可 `window.use('webSignUrl')(url)`。
2. **免握手**：把实时浏览器导出的会话密钥（`security-sdk/s_sdk_crypt_sdk`=ECDSA P-256 私钥、`s_sdk_server_cert_key`、`web_runtime_security_uid` 等）注入 mock 的 localStorage（`lib/abogus_rebuild/websign_env.json`），secsdk 初始化时恢复密钥，**同步**出签，不再向服务器握手。
3. **字节级一致**：固定时间戳下 Node 签名 == 浏览器签名（实测同 url+ts → 同 `d09b2c51...`）。
4. **签名顺序（重要）**：先算 `a_bogus`（URL **不含** secsdk 三参数），再由 secsdk 在 query 末尾追加 `uifid` + `timestamp` + `x-secsdk-web-signature`。
5. **同源要求**：请求携带的 cookie 必须与 `websign_env.json` 的密钥来自**同一浏览器会话**（uifid 由 `web_runtime_security_uid` 派生，服务器校验一致性）。
6. secsdk 补环境**不能加载 bdms**（会卡死初始化），webSign 也不需要它。

> 路由：`utils/request.py` 的 `WEBSIGN_URIS` 列出需要三件套的接口；`getJSON` 先 `get_sign_bdms` 出 a_bogus，再 `get_websign` 追加 secsdk 三参数。

---

## 核心发现：feed 等接口需要**三件套**签名

服务器端实测（用实时浏览器 cookie 重放可用 URL，逐个删参数验证）：

| 参数 | 来源 | 删掉后 |
|------|------|--------|
| `a_bogus` | bdms/webmssdk (JSVMP) | 403 |
| `timestamp` | `Date.now()/1000` | **403 Sign Invalid** |
| `x-secsdk-web-signature` | securitySDK | **403 Sign Invalid** |

> 三者齐全 → HTTP 200，拿到完整 feed 数据。
> 本项目（旧 douyin.js 与 bdms 补环境）**只产出 a_bogus，从未产出 x-secsdk-web-signature**，这是 feed/favorite 等接口一直 403 的真正根因。

## a_bogus（已深度逆向）
- 算法 = SM3(双哈希) + RC4(**固定 keystream**) + s4 自定义 base64
- 结构：`a_bogus = s4_encode(random_head(4) + (bb XOR 固定keystream))`
- RC4 keystream 已抓取固定（`FIXED_keystream.json`，132+125 字节）
- **bb 是变长结构序列化**（T=...016 → 134 字节，多数时间戳非 133 长），时间值存 3 份复制、6-bit 打包、含交织 XOR 校验
- 时间→bb 位映射大部分已解（`time_bits.json`），但变长序列化器需逐条逆向 VM opcode
- **可用方案**：Node 跑官方 `bdms.js` 补环境（`lib/index.js`+`lib/env.js`），已能产出 a_bogus

## x-secsdk-web-signature（已定位机制）
- 浏览器里 `window.use("webSignUrl")(url)` 直接返回带 `uifid`+`timestamp`+`x-secsdk-web-signature` 的完整 URL
- 128-bit（32 hex），**确定性**：同 url+timestamp → 同签名；随 url、timestamp 变化
- 由 `window.securitySDK.cryptoSDK` 计算（**纯 JS**，非 WASM）：方法含 `sign/pureSign/getTSSign/initECDHKey/getCertSignRequest/getTicket`
- 依赖 localStorage 会话密钥：
  - `security-sdk/s_sdk_crypt_sdk` — ECDSA P-256 私钥（PEM 明文）
  - `security-sdk/s_sdk_server_cert_key` — 服务器证书（2022→2052）
  - `security-sdk/s_sdk_sign_data_key/web_protect` — `ticket` + `ts_sign`（服务器签发）
  - `web_runtime_security_uid` — 会话 UUID
- **关键观测**：清空全部 secsdk localStorage 后，`webSignUrl` 仍能产出签名（密钥客户端可重生），说明基础签名不强依赖服务器 ticket
- 完整 secsdk 栈：`runtime_bundler_34.js`(177KB) + `webmssdk.es5.js` + `sdk-glue.js`，握手端点 `security.zijieapi.com`

## 已下载/保存的资产
- `lib/bdms.js`、`lib/abogus_rebuild/secsdk_bundle.js`(runtime_bundler_34)
- `FIXED_keystream.json`、`time_bits.json`、`time_precise.json`、`grab_bb.json`
- `live_cookies.json`（实时会话 cookie，可用）

## 实现路径选项
1. **Node 跑完整 secsdk 栈补环境**：让官方 JS 自己握手+签名（webSignUrl）。需加载 runtime_bundler+glue+crypto 多 bundle + 补 window/document/localStorage/crypto.subtle 环境。工作量大但最贴近官方、最准确。
2. **导出密钥 + Node 跑 secsdk 签名**：把 localStorage 密钥导出注入 Node，跳过握手只签名。ticket 过期需刷新。
3. **secsdk 那步用浏览器**：webSignUrl 调实时浏览器，a_bogus 用 Node 补环境。
