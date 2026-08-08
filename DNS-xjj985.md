# 域名 xjj985.top · DNS / Pages / Studio 隧道

> 状态说明：若域名仍在**实名/注册审核**，解析尚未生效属正常。  
> 当前 `dig` 若为 `NXDOMAIN`，**不要**假定自定义域已可用；公众号菜单请继续用 GitHub Pages 备用地址。

## 目标拓扑

| 用途 | 主机名 | 指向 |
|------|--------|------|
| WeChat Hub + 白皮书（GitHub Pages） | `xjj985.top`（可选 `www`） | GitHub Pages |
| Studio（本机/服务器 + cloudflared） | `chat.xjj985.top` | Cloudflare Tunnel |

审核通过后期望 URL：

- Hub：`https://xjj985.top/wechat.html`（或 `https://xjj985.top/` → 可再跳到 wechat）
- Studio：`https://chat.xjj985.top/?embed=1`
- 配置里的 `publicStudioUrl`：`https://chat.xjj985.top`（见 `assets/studio-config.js`）

**审核期间备用 Hub（菜单先填这个）：**

```text
https://junjiewq.github.io/java-senior-playbook/wechat.html
```

## 审核期间做什么

1. 等域名审核通过（阿里云/注册商控制台显示可解析）。
2. 公众号菜单继续用上面的 `github.io` 合体页。
3. Studio 练级：本机起服务 → `bash scripts/remote-access.sh` → 把临时 HTTPS 粘贴进合体页（会覆盖默认的 `chat.xjj985.top`）。
4. 本仓库已放好 `CNAME`（内容 `xjj985.top`）与 `publicStudioUrl`，审核+DNS 就绪后无需再改代码（除非改拓扑）。

## 审核通过后：在域名控制台添加的解析（逐条）

以下主机记录名以**阿里云 DNS** 为例（`主机记录` / `记录类型` / `记录值`）。其他厂商字段名类似。

### A. Hub → GitHub Pages（apex `xjj985.top`）

多数国内注册商 **apex（@）不能做 CNAME**，请用 GitHub 官方 A/AAAA：

| 主机记录 | 类型 | 记录值 |
|----------|------|--------|
| `@` | A | `185.199.108.153` |
| `@` | A | `185.199.109.153` |
| `@` | A | `185.199.110.153` |
| `@` | A | `185.199.111.153` |
| `@` | AAAA | `2606:50c0:8000::153` |
| `@` | AAAA | `2606:50c0:8000::068` |
| `@` | AAAA | `2606:50c0:8000::17` |
| `@` | AAAA | `2606:50c0:8000::10` |

可选 www：

| 主机记录 | 类型 | 记录值 |
|----------|------|--------|
| `www` | CNAME | `junjiewq.github.io` |

若 DNS 在 **Cloudflare** 且支持 CNAME flattening，apex 也可：

| 主机记录 | 类型 | 记录值 |
|----------|------|--------|
| `@` | CNAME | `junjiewq.github.io` |

### B. Studio → Cloudflare Tunnel（`chat.xjj985.top`）

**方式 1（推荐）**：在 Cloudflare Zero Trust / cloudflared 控制台给隧道绑定 hostname `chat.xjj985.top` → `http://127.0.0.1:18080`，再按控制台提示加一条 CNAME（值形如 `<tunnel-id>.cfargotunnel.com`，以你控制台为准）：

| 主机记录 | 类型 | 记录值 |
|----------|------|--------|
| `chat` | CNAME | `<你的-tunnel-id>.cfargotunnel.com` |

**方式 2（域名 DNS 不在 Cloudflare）**：把 `chat` 的 NS/托管迁到 Cloudflare，或使用 Cloudflare 提供的 CNAME 目标；不要手写假的 tunnel id。

### C. GitHub Pages 后台

1. 仓库 Settings → Pages → Custom domain 填：`xjj985.top`
2. 勾选 Enforce HTTPS（证书签发需 DNS 已指向 GitHub）
3. 本仓库根目录 `CNAME` 文件内容已是 `xjj985.top`（勿改成带 `https://`）

## Studio 隧道还要做什么（本机尚无命名隧道凭证时）

当前环境通常 **没有** `~/.cloudflared` 登录态时，**无法**自动绑 `chat.xjj985.top`。按下面做一次即可：

```bash
# 1) 安装/找到 cloudflared（仓库旁 bank-agent/.tools/cloudflared 或 brew）
# 2) 登录（浏览器授权，勿把证书/token 发到公开群）
cloudflared tunnel login

# 3) 创建命名隧道（名字自定）
cloudflared tunnel create studio-xjj985

# 4) 配置 ingress：chat.xjj985.top → http://127.0.0.1:18080
#    编辑 ~/.cloudflared/config.yml（示例结构，UUID 以你机器为准）
#
# tunnel: <TUNNEL-UUID>
# credentials-file: /Users/你/.cloudflared/<TUNNEL-UUID>.json
# ingress:
#   - hostname: chat.xjj985.top
#     service: http://127.0.0.1:18080
#   - service: http_status:404

# 5) 路由 DNS（若域名已接入 Cloudflare 可用）
cloudflared tunnel route dns studio-xjj985 chat.xjj985.top

# 6) 先起 Studio，再跑隧道
cd agentscope-java-programmer
# mvn -q spring-boot:run   或 scripts/start-studio.sh
cloudflared tunnel run studio-xjj985
```

练级临时穿透（域名未就绪时）仍用：

```bash
bash scripts/remote-access.sh
# 得到 https://….trycloudflare.com → 粘贴进 wechat.html
```

## 公众号菜单填哪个 URL

| 阶段 | 菜单「跳转网页」URL |
|------|---------------------|
| **现在（审核中 / dig 为 NXDOMAIN）** | `https://junjiewq.github.io/java-senior-playbook/wechat.html` |
| DNS + Pages HTTPS 都 OK 后 | `https://xjj985.top/wechat.html` |
| 可选：对话单独菜单（需 Studio 隧道在线） | `https://chat.xjj985.top/?embed=1` |

微信公众平台若校验业务域名，把 `xjj985.top`、`chat.xjj985.top`（以及过渡期的 `junjiewq.github.io`）按需加入。

## 自检命令（不要凭感觉说「已经好了」）

```bash
dig +short xjj985.top A
dig +short www.xjj985.top CNAME
dig +short chat.xjj985.top CNAME
curl -sI https://xjj985.top/wechat.html | head -n5
curl -sI https://chat.xjj985.top/health | head -n5
```

- Hub：应解析到 GitHub Pages IP，且 HTTPS 200。
- Studio：`chat` 应有 CNAME 到 `*.cfargotunnel.com`，且本机隧道 + Java :18080 在跑时 `/health` 才通。
