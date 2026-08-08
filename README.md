# 高级 Java · 下单正逆向闭环白皮书

**主线**：买成 → 履约 → 退成/修好（优惠分摊 / 支付 / OMS-WMS / 售后寄修换新）。  
**写法**：业务本质 × 技术本质 × 像在公司做需求。  
**认知闭环四段**：业务本质 → 技术实现 → 技术原理 → 业务实质（高并发贯穿：峰/热/削/降）。  
**一年坚持**：S-Year · 12 月主题 × 52 周仪式 × 季度 OKR。  
**收官五步法**：**钉拆标选验** — 钉本质验收 → 拆主/异/逆 → 标并发一致 → 选技对需求 → 验·观·滚·复盘。  
**AI 重头戏**：Skills · MCP · RAG · 多智能体 · AgentScope（挂订单域，禁止直改账务）。  
**极致加厚写法**：人话 → **掀底板**（源码/数据结构路径）→ 今天落地清单 → 回扣买成/退成。  
**本地双文件**：`index.html` 与 `../高级Java外包-系统学习技术白皮书.html` **必须字节一致**（inject 后 `cp` + md5 校验）。

## 体系导航

| ID | 含义 |
|----|------|
| S0–S4 | 目标 → 问题域 → 方法 → 路考 → 复习 |
| **S-C4** | **认知闭环四段** |
| **S-Year** | **一年坚持路线（52 周）** |
| B0 / B-F / B-R / B-Ind | **业务主线** |
| **B-X** | **生产级复杂场景 ×5** |
| **S-MS-X / T-K8s-X / T-AI-X** | **微服务·云原生·AI 极致落地** |
| **S-DDD-X / S-Mgmt-X / T-Found-X** | **DDD模式·管理排期·基础件掀底板** |
| **X-大促** | **微服务×K8s×AI 演练剧本** |
| T-K8s | 发布弹性（金丝雀/回滚） |
| **T-AI-Stack** / Skills / MCP / RAG / Agents | **AI 重头戏** |
| S-MS | 微服务卡点·难点·亮点 |
| **S-Method** | **钉拆标选验五步法** |

## 锚点速链（Pages）

| 章节 | 锚点 | URL |
|------|------|-----|
| **一年路线** | `#s-year` | https://junjiewq.github.io/java-senior-playbook/#s-year |
| **认知四段** | `#s-c4` | https://junjiewq.github.io/java-senior-playbook/#s-c4 |
| **B-X 总览** | `#bx-prod` | https://junjiewq.github.io/java-senior-playbook/#bx-prod |
| 拼团+券分摊退 | `#bx-group-coupon` | https://junjiewq.github.io/java-senior-playbook/#bx-group-coupon |
| 支付→WMS 缺货 | `#bx-pay-wms-short` | https://junjiewq.github.io/java-senior-playbook/#bx-pay-wms-short |
| 寄修∥换新 | `#bx-repair-exchange` | https://junjiewq.github.io/java-senior-playbook/#bx-repair-exchange |
| 餐饮餐损 | `#bx-food-peak` | https://junjiewq.github.io/java-senior-playbook/#bx-food-peak |
| 跨境清关失败 | `#bx-cross-border` | https://junjiewq.github.io/java-senior-playbook/#bx-cross-border |
| 五步法 | `#s-method` / `#s-five-steps` | https://junjiewq.github.io/java-senior-playbook/#s-method |
| AI 总图 | `#t-ai-stack` | https://junjiewq.github.io/java-senior-playbook/#t-ai-stack |
| Skills | `#t-skills` | https://junjiewq.github.io/java-senior-playbook/#t-skills |
| MCP | `#t-mcp` | https://junjiewq.github.io/java-senior-playbook/#t-mcp |
| RAG | `#t-rag` | https://junjiewq.github.io/java-senior-playbook/#t-rag |
| 多智能体专章 | `#t-agents-deep` | https://junjiewq.github.io/java-senior-playbook/#t-agents-deep |
| **写法约束** | `#s-tone-x` | https://junjiewq.github.io/java-senior-playbook/#s-tone-x |
| **微服务极致** | `#s-ms-x` | https://junjiewq.github.io/java-senior-playbook/#s-ms-x |
| **云原生极致** | `#t-k8s-x` | https://junjiewq.github.io/java-senior-playbook/#t-k8s-x |
| **AI 极致** | `#t-ai-x` | https://junjiewq.github.io/java-senior-playbook/#t-ai-x |
| **DDD·模式** | `#s-ddd-x` |
| **DDD·模式** | `#s-ddd-x` | https://junjiewq.github.io/java-senior-playbook/#s-ddd-x |
| **聚合根唯一性/加载** | `#s-ddd-agg` | https://junjiewq.github.io/java-senior-playbook/#s-ddd-agg |
| **管理排期** | `#s-mgmt-x` | https://junjiewq.github.io/java-senior-playbook/#s-mgmt-x |
| **基础件掀底板** | `#t-found-x` | https://junjiewq.github.io/java-senior-playbook/#t-found-x |
| MQ 选型矩阵 | `#found-mq-matrix` | https://junjiewq.github.io/java-senior-playbook/#found-mq-matrix |
| 锁/一致性矩阵 | `#found-lock-matrix` | https://junjiewq.github.io/java-senior-playbook/#found-lock-matrix |
| **大促三联** | `#x-promo-trinity` | https://junjiewq.github.io/java-senior-playbook/#x-promo-trinity |
| **交付冻结 v1.1** | `#delivery-status` | https://junjiewq.github.io/java-senior-playbook/#delivery-status |
| **全书去水审计** | `#doc-audit` | https://junjiewq.github.io/java-senior-playbook/#doc-audit |
| **ENCY HARD GATE** | `#ency-fm` / `#ency-audit` | https://junjiewq.github.io/java-senior-playbook/#ency-fm |
| PolarDB-X CN/DN/GMS/CDC | `#ency-fm-polardb-cn` … | https://junjiewq.github.io/java-senior-playbook/#ency-fm-polardb |

## 微信公众号合体入口（优先）

| 项 | URL / 文件 |
|----|------------|
| **菜单填这个** | https://junjiewq.github.io/java-senior-playbook/wechat.html |
| 白皮书 | [`index.html`](./index.html)（入口 A） |
| 对话机器人 | 链到公网 Studio（入口 B，需隧道/域名） |
| 说明 | [`WECHAT.md`](./WECHAT.md) |
| Studio 地址配置 | [`assets/studio-config.js`](./assets/studio-config.js)（`publicStudioUrl` ≈ `PUBLIC_STUDIO_URL`） |

完整 TXT 仍**仅本地**：`高级Java外包-系统学习技术白皮书.txt`（不上 Pages）。

## 本地打开

1. [`wechat.html`](./wechat.html) — 公众号式双入口  
2. [`index.html`](./index.html) — 白皮书全文（需联网 CDN）  
3. 仓库外旧镜像 `../高级Java外包-系统学习技术白皮书.html`：**改为跳转 stub → Pages 合体页**（不再要求与 index 字节一致）

构建（改内容时）：

```bash
python3 _inject_pillars_extreme.py   # 极致章
python3 _inject_ency.py              # ENCY-FM 全貌 + 搜索
python3 _apply_anti_water.py         # 去水加厚 + #doc-audit（可选一键）
```

## GitHub Pages

- 首页：https://junjiewq.github.io/java-senior-playbook/  
- **公众号入口**：https://junjiewq.github.io/java-senior-playbook/wechat.html

## 声明

学习面试用途。公开实践归纳。AI 不直接改生产账务。勿粘贴密钥与未脱敏数据。
