# 域名 xjj985.top · DNS / Pages / Studio 隧道

> **2026-08-09 状态**  
> - 注册商审核：**已通过**（WHOIS `Domain Status: ok`，DNSPod / 腾讯云）  
> - 权威 NS：`barley.dnspod.net` / `deep.dnspod.net`（已在注册局）  
> - 公网 `dig`：多数递归仍 **NXDOMAIN**（新域 `addPeriod` / 委派传播中）  
> - **DNSPod 权威区无 A/CNAME**：`@` / `www` / `chat` 均未添加记录 → 自定义域尚不可用  
> - GitHub Pages：已设 Custom domain `xjj985.top`（仓库 `CNAME` 已推送）；**Enforce HTTPS** 需等解析到 Pages 后证书签发才能开  
> - Studio：本机 **无** `~/.cloudflared` 登录态 → 暂无法绑命名隧道 `chat.xjj985.top`

## 目标拓扑

| 用途 | 主机名 | 指向 |
|------|--------|------|
| WeChat Hub + 白皮书（GitHub Pages） | `xjj985.top`（可选 `www`） | GitHub Pages |
| Studio（本机/服务器 + cloudflared） | `chat.xjj985.top` | Cloudflare Tunnel |

就绪后期望 URL：

- Hub：`https://xjj985.top/wechat.html`
- Studio：`https://chat.xjj985.top/?embed=1`
- 配置里的 `publicStudioUrl`：`https://chat.xjj985.top`（见 `assets/studio-config.js`）

**现在菜单仍用（DNS 未加记录前）：**

```text
https://junjiewq.github.io/java-senior-playbook/wechat.html
```

## 审核通过后清单

| 项 | 状态 |
|----|------|
| 域名审核通过（可配置解析） | ✅ 已通过 |
| 在 DNSPod 添加 apex A/AAAA + www CNAME | ⬜ 待你在控制台添加（见下表） |
| 公网 dig 不再 NXDOMAIN，apex → GitHub IP | ⬜ |
| GitHub Pages Custom domain = `xjj985.top` | ✅ API 已确认 |
| 仓库根 `CNAME` = `xjj985.top` | ✅ 已在 main |
| Pages Enforce HTTPS | ⬜ 证书未签发（DNS 到位后再勾选 / API） |
| `https://xjj985.top/wechat.html` 可打开 | ⬜ |
| `cloudflared tunnel login` + 命名隧道绑 `chat` | ⬜ 本机无凭证 |
| `chat.xjj985.top` CNAME → `*.cfargotunnel.com` | ⬜ |
| 公众号菜单改为自定义域 | ⬜ DNS+HTTPS OK 后再改 |

## 请在 DNSPod / 腾讯云 DNS 控制台添加的解析（完整）

控制台入口（任选）：[DNSPod](https://console.dnspod.cn/) 或 [腾讯云 DNS 解析](https://console.cloud.tencent.com/cns) → 域名 `xjj985.top` → 添加记录。

### A. Hub → GitHub Pages（apex `xjj985.top`）

apex（`@`）请用 GitHub 官方 A/AAAA（不要对 `@` 做普通 CNAME，除非厂商明确支持 flattening）：

| 主机记录 | 记录类型 | 记录值 | TTL |
|----------|----------|--------|-----|
| `@` | A | `185.199.108.153` | 600 |
| `@` | A | `185.199.109.153` | 600 |
| `@` | A | `185.199.110.153` | 600 |
| `@` | A | `185.199.111.153` | 600 |
| `@` | AAAA | `2606:50c0:8000::153` | 600 |
| `@` | AAAA | `2606:50c0:8000::068` | 600 |
| `@` | AAAA | `2606:50c0:8000::17` | 600 |
| `@` | AAAA | `2606:50c0:8000::10` | 600 |

可选 www：

| 主机记录 | 记录类型 | 记录值 | TTL |
|----------|----------|--------|-----|
| `www` | CNAME | `junjiewq.github.io` | 600 |

### B. Studio → Cloudflare Tunnel（`chat.xjj985.top`）

**先**完成本机命名隧道（见下方命令），拿到真实 tunnel id 后再加：

| 主机记录 | 记录类型 | 记录值 | TTL |
|----------|----------|--------|-----|
| `chat` | CNAME | `<你的-tunnel-id>.cfargotunnel.com` | 600 |

若域名 DNS 留在 DNSPod：不要手写假的 tunnel id；用 `cloudflared tunnel route dns`（需把域名接到 Cloudflare）或在 Zero Trust 控制台复制给出的 CNAME 目标，贴到 DNSPod。

### C. GitHub Pages（仓库侧已就绪）

1. Settings → Pages → Custom domain：`xjj985.top` ✅  
2. DNS 生效后勾选 **Enforce HTTPS**（当前 API：`The certificate does not exist yet`）  
3. 仓库 `CNAME` 内容保持一行：`xjj985.top`

## Studio 命名隧道（本机尚无凭证）

当前 **没有** `~/.cloudflared`，无法自动绑 `chat.xjj985.top`。在本机执行一次：

```bash
# 可用仓库旁二进制
CF=/Users/Zhuanz/Downloads/test2/agentscope-java-programmer/.tools/cloudflared

"$CF" tunnel login
"$CF" tunnel create studio-xjj985

# 编辑 ~/.cloudflared/config.yml（UUID 以 create 输出为准）
# tunnel: <TUNNEL-UUID>
# credentials-file: /Users/你/.cloudflared/<TUNNEL-UUID>.json
# ingress:
#   - hostname: chat.xjj985.top
#     service: http://127.0.0.1:18080
#   - service: http_status:404

# 若域名已接入 Cloudflare DNS：
"$CF" tunnel route dns studio-xjj985 chat.xjj985.top
# 否则：把控制台给的 <uuid>.cfargotunnel.com 填到 DNSPod 的 chat CNAME

cd /Users/Zhuanz/Downloads/test2/agentscope-java-programmer
# 终端 1：起 Studio（:18080）
# 终端 2：
"$CF" tunnel run studio-xjj985
```

**练级临时穿透（推荐现在就用）：**

```bash
cd /Users/Zhuanz/Downloads/test2/agentscope-java-programmer
bash scripts/remote-access.sh
# 得到 https://….trycloudflare.com → 粘贴进 wechat.html 或 ?studio=
```

## 公众号菜单填哪个 URL

| 阶段 | 菜单「跳转网页」URL |
|------|---------------------|
| **现在（解析记录未加 / dig 仍空）** | `https://junjiewq.github.io/java-senior-playbook/wechat.html` |
| DNS + Pages HTTPS 都 OK 后 | `https://xjj985.top/wechat.html` |
| 可选：对话单独菜单（需 Studio 隧道在线） | `https://chat.xjj985.top/?embed=1` |

微信业务域名按需加：`xjj985.top`、`chat.xjj985.top`、过渡期 `junjiewq.github.io`。

## 自检命令

```bash
dig +short xjj985.top A
dig @barley.dnspod.net +short xjj985.top A
dig +short www.xjj985.top CNAME
dig +short chat.xjj985.top CNAME
curl -sI https://xjj985.top/wechat.html | head -n5
curl -sI https://junjiewq.github.io/java-senior-playbook/wechat.html | head -n5
curl -sI https://chat.xjj985.top/health | head -n5
```

- Hub：权威与公网均应看到 GitHub Pages IP，且 HTTPS 200。  
- Studio：`chat` → `*.cfargotunnel.com`，且本机隧道 + Java :18080 在跑时 `/health` 才通。

> 状态更新（2026-08-10）：DNS A/CNAME 已生效，`http://xjj985.top/wechat.html` 可打开；GitHub Pages **自定义域证书尚未签发**（仍返回 `*.github.io`），`https://` 与微信菜单暂不可用自有域名。证书好后在 Pages 勾选 Enforce HTTPS，菜单改 `https://xjj985.top/wechat.html`。
