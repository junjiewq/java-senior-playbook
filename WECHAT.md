# 微信公众号 × 白皮书 × Studio 对话

**合体入口（推荐写进公众号菜单）**  
https://junjiewq.github.io/java-senior-playbook/wechat.html

> 本文说明可行性与运维步骤。仓库**不会**替你完成公众号注册、认证或菜单配置。

## 能不能做？

| 目标 | 结论 |
|------|------|
| 菜单 / 自动回复打开 **HTTPS H5**（白皮书 + 对话入口） | **可以** |
| 在微信里用 iframe 嵌一整站 Studio（复杂三栏 IDE） | 体验差；用本页链出去 + Studio `?embed=1` 更合适 |
| 用户在**公众号会话气泡**里直接跟 Agent 聊 | **另一套**：需微信消息回调 / 客服接口，不是静态 Pages |

## 两种嵌入方式（别混）

### 方式 1 — H5 入口（本仓库交付的）

1. 公众号菜单「跳转网页」→ `wechat.html`
2. 用户点「打开白皮书」→ Pages 上的 `index.html`
3. 用户点「打开对话」→ 你的 **公网 Studio**（`PUBLIC_STUDIO_URL` + `?embed=1`）

需要：公网 **HTTPS**、Studio 进程在线、隧道或域名能转发 **WSS**（`/ws/agent`）。

### 方式 2 — 真·公众号消息会话

用户在聊天列表发文字给公众号 → 微信服务器 POST 到你的后端 → 你再调 Agent / 回文本。  
这与打开 H5 **无关**，要单独做接入与审核，本仓库未实现。

## 公众号菜单怎么填

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)（需已有公众号；未注册请自行申请）。
2. 自定义菜单 → 跳转网页 → URL：

```text
https://junjiewq.github.io/java-senior-playbook/wechat.html
```

3. 若已有**稳定** Studio 域名，可给「对话」单独做菜单项，直链：

```text
https://你的域名/?embed=1
```

（临时 `*.trycloudflare.com` 会变，不适合写死在菜单里长期用。）

4. JS 安全域名 / 业务域名：若要用微信 JSSDK，把 Pages 域名与 Studio 域名配进公众号后台；**纯打开外链 H5** 通常只需菜单 URL 可访问。

## 配置 `PUBLIC_STUDIO_URL`

三选一（优先级从高到低）：

1. 合体页 URL：`wechat.html?studio=https://xxxx.trycloudflare.com`
2. 合体页里粘贴地址并「保存」（写入该手机浏览器的 localStorage）
3. 编辑仓库 [`assets/studio-config.js`](./assets/studio-config.js)：

```js
window.PLAYBOOK_STUDIO = {
  publicStudioUrl: "https://studio.example.com",
  chatQuery: "embed=1",
};
```

改完后 `git push`，Pages 才会更新配置。

**不要**把 `DEEPSEEK_API_KEY`、`AGENT_WS_TOKEN` 写进公开仓库。

## 本机 Studio + 隧道（练级）

```bash
# 终端 1
cd agentscope-java-programmer
mvn -q spring-boot:run

# 终端 2
bash scripts/remote-access.sh
# 打印 https://….trycloudflare.com
```

把该 HTTPS 填进合体页或 `studio-config.js`。  
微信打开对话时会走 `wss://同一主机/ws/agent`。

可选鉴权：`.env` 设 `AGENT_ALLOW_ANONYMOUS=false` + `AGENT_WS_TOKEN=…`，链接加 `?embed=1&token=…`（token 勿发到公开群）。

## 微信内限制（说清楚）

| 能力 | 说明 |
|------|------|
| 文字对话 | 最稳；依赖 HTTPS + WSS |
| 麦克风 / 通话 | 需安全上下文；**微信内置浏览器**对 `getUserMedia`、后台播放、部分 TTS 支持不稳定 |
| Edge TTS 朗读 | 可能可用，失败时前端有系统语音兜底；勿依赖「一定能播」 |
| localhost | **不行**；用户手机打不开你的电脑 localhost |

## 本地文件策略

| 文件 | 策略 |
|------|------|
| `wechat.html` | 公众号菜单主入口（Pages） |
| `index.html` | 完整白皮书单页（仍较大；拆章为次要优化） |
| `高级Java外包-系统学习技术白皮书.txt` | **仅本地**，不上 Pages |
| 仓库外 `../高级Java外包-系统学习技术白皮书.html` | 改为跳转 stub → Pages 合体页（不再与 index 字节同步） |

## Studio `?embed=1`

打开 `https://你的Studio/?embed=1` 时隐藏左右 Explorer/Diff 重壳，偏聊天，适合微信 WebView。改静态资源后需**重启** Spring Boot。
