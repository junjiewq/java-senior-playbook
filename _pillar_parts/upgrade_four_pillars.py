#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upgrade XXL-JOB / PolarDB / Kafka / AI APPX(+T-AI) chapters to production+source depth."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"


def mw(diag_id: str, body: str) -> str:
    return f"""  <div class="mermaid-wrap" id="{diag_id}">
    <div class="diag-actions"><button class="btn" type="button" data-png="{diag_id}">导出 PNG</button></div>
    <pre class="mermaid">
{body.strip()}
    </pre>
  </div>
"""


def polar_deep() -> str:
    return f"""  <!-- ========== POLAR DEEP ========== -->
  <h3 id="appx-polar-deep">3. PolarDB 原理与规范深挖（生产+源码加厚）</h3>
  <div class="plain"><div class="label">人话版</div>订单库先分清两款产品：<b>PolarDB 共享存储</b>=一写多读扩读；<b>PolarDB-X</b>=CN/DN/GMS 扩写。付后读己之写打主；CDC 旁路入湖，资损权威仍在库+Outbox。金标底座见 <a href="#ency-fm-polardb">#ency-fm-polardb</a>。</div>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>正逆向 OLTP：下单写主、详情读扩展、售后对账、CDC 喂搜推。<br><b>服务业务闭环：</b>支付回跳一致性 / 分片热点 / DDL 窗口<br><b>挂回：</b><a href="#ency-fm-polardb">ENCY 金标</a> · <a href="#appx-sql-agents">SQL 智能体</a> · <a href="#appx-kafka-src">Kafka CDC</a></div>
  <div class="callout"><div class="label">交付诚实</div>本节为「金标上再加厚」：补操作图、数据流、失败流、Runbook、红线。量级仅工程目标/示意，禁止伪造未公开 KPI。</div>

  <h4 id="appx-polar-pos">3.0 定位：在下单正逆向闭环里干什么</h4>
  <table>
    <thead><tr><th>链路步骤</th><th>Polar 角色</th><th>红线</th></tr></thead>
    <tbody>
      <tr><td>下单/支付写</td><td>Primary / 单分片 DN 本地事务</td><td>短事务；禁止长事务锁库存行</td></tr>
      <tr><td>付后详情</td><td>读主或 sticky；RO 仅非关键读</td><td>禁止「已付仍待支付」客诉窗口</td></tr>
      <tr><td>售后/对账</td><td>主库权威；报表可 RO</td><td>修数双人+工单</td></tr>
      <tr><td>搜推/数仓</td><td>CDC → Kafka/MQ</td><td>CDC≠账本；乱序/重复常态</td></tr>
    </tbody>
  </table>
{mw("diag-appx-polar-spine", '''
flowchart LR
  Pay[支付回调] --> W[写 Primary/DN]
  W --> Outbox[(Outbox/本地消息)]
  W --> Detail[付后读主]
  W --> CDC[CDC 旁路]
  CDC --> K[Kafka/搜推]
  RO[RO/报表] -.->|延迟窗口| Detail
  Outbox -->|资损优先| Fulfill[履约]
''')}

  <h4 id="appx-polar-product">3.1 产品边界</h4>
  <table>
    <thead><tr><th>产品</th><th>架构本质</th><th>扩展方式</th><th>典型误用</th></tr></thead>
    <tbody>
      <tr><td>PolarDB（MySQL 兼容·共享存储）</td><td>一写多读，计算存储分离</td><td>加 RO、升规格</td><td>把 RO 当强一致写后读</td></tr>
      <tr><td>PolarDB-X</td><td>CN 计算 / DN 存储 / GMS 元数据</td><td>分片扩展写</td><td>无分片键设计就上 X</td></tr>
    </tbody>
  </table>
{mw("diag-appx-polar", '''
flowchart LR
  App[应用连接串] --> CN{产品?}
  CN -->|共享存储 PolarDB| RW[RW 主]
  RW --> Shared[(共享存储)]
  RW --> RO1[RO]
  RW --> RO2[RO]
  CN -->|PolarDB-X| Calc[CN 计算层]
  Calc --> GMS[GMS]
  Calc --> DN1[(DN1)]
  Calc --> DN2[(DN2)]
  Calc --> CDC[CDC 旁路]
''')}

  <h4 id="appx-polar-src">3.2 原理/源码级路径（框架认知 · 示意）</h4>
  <p><b>共享存储 PolarDB（认知路径）：</b>Primary 写事务日志 → 共享存储多副本落盘 → RO 按 redo/位点追可见页。缓冲池与 InnoDB 同源思路；规格不足先表现为 RT 毛刺与 RO 追不上。</p>
  <p><b>PolarDB-X（认知路径）：</b></p>
  <pre><code>// 示意（非某一闭源文件字面量）
Client → CN.Frontend → Parser → Optimizer(meta←GMS)
      → Scheduler.scatter → DN.local_engine(begin/exec/commit|2PC)
      → Gather / 跨片协调
CDC ← DN binlog/redo 旁路（乱序/重复/DDL 暂停窗口）
</code></pre>
  <ul>
    <li><b>CN：</b>无状态入口；扩 CN ≠ 解 DN 热点。</li>
    <li><b>DN：</b>本地行锁/MVCC/redo；热点片=单 DN 打满。</li>
    <li><b>GMS：</b>schema_version / topology；DDL 后 CN 缓存失效。</li>
    <li><b>应用侧：</b>读写路由中间件 / 双数据源（项目代码）决定「何时打主」——框架不替你保付后一致。</li>
  </ul>
{mw("diag-appx-polar-cn-path", '''
sequenceDiagram
  participant App as 应用/JDBC
  participant CN as CN
  participant GMS as GMS
  participant DN as DN分片
  App->>CN: SQL
  CN->>GMS: 取 topology/schema_ver
  CN->>CN: 优化/路由计划
  alt 单片
    CN->>DN: 本地事务
    DN-->>CN: OK
  else 跨片
    CN->>DN: 2PC prepare/commit
  end
  CN-->>App: 结果集/错误
''')}

  <h4 id="appx-polar-dataflow">3.3 数据流图：写入 / 复制 / CDC</h4>
{mw("diag-appx-polar-dataflow", '''
flowchart TB
  subgraph Shared["PolarDB 共享存储"]
    W1[App 写] --> P[Primary]
    P --> S[(Shared Storage)]
    P -->|redo/位点| RO[RO]
    RO --> R1[报表/搜索读]
  end
  subgraph X["PolarDB-X"]
    W2[App 写] --> CN2[CN]
    CN2 --> DN[(DN 分片)]
    DN --> Bin[本地日志]
    Bin --> CDC2[CDC]
    CDC2 --> Bus[Kafka/MQ]
  end
  P -.->|可选 CDC| Bus
''')}
{mw("diag-appx-polar-readpath", '''
flowchart TD
  Req[读请求] --> Need{写后读己 / 事务内?}
  Need -->|是| Primary[强制 Primary]
  Need -->|否| Lag{RO lag &lt; SLA?}
  Lag -->|是| RO[RO]
  Lag -->|否| Primary
  Primary --> OK[返回]
  RO --> OK
''')}

  <h4 id="appx-polar-ops">3.4 操作图：部署 / 扩缩 / 切换 / 巡检</h4>
{mw("diag-appx-polar-ops", '''
flowchart TB
  Deploy[变更窗口] --> Backup[确认最近成功备份/PITR]
  Backup --> Canary[只读探活 + 拨测付后读主]
  Canary --> Scale{动作?}
  Scale -->|加 RO| AddRO[挂载 RO → 观察 lag]
  Scale -->|升规格| Resize[滚动计算节点]
  Scale -->|切主/HA| HA[演练切换 → 应用重连]
  Scale -->|扩 DN 片| Rebal[数据再均衡 + SQL 审核]
  AddRO --> Inspect[巡检]
  Resize --> Inspect
  HA --> Inspect
  Rebal --> Inspect
  Inspect --> Done[签字关闭窗口]
''')}
  <ol>
    <li><b>部署/变更前：</b>备份成功时间、参数快照 vs 大基线差分、只读账号探活。</li>
    <li><b>扩 RO：</b>观察复制延迟与连接串权重；关键业务拨测「付后读主」未改错。</li>
    <li><b>故障切换：</b>应用池重连/超时；禁止人工乱改 VIP 无演练。</li>
    <li><b>巡检命令级（只读示意）：</b></li>
  </ol>
  <pre><code>-- 参数/连接（只读账号）
SHOW GLOBAL VARIABLES WHERE Variable_name IN
 ('innodb_flush_log_at_trx_commit','sync_binlog','long_query_time','max_connections');
SHOW GLOBAL STATUS LIKE 'Threads_connected';
-- 复制延迟：以云监控/DAS 的 RO lag 为准（产品面板）；应用侧拨测付后读主
-- PolarDB-X：看跨片比例、热点 DN CPU、GMS 健康（控制台指标）
</code></pre>

  <h4 id="appx-polar-flow">3.5 流程图：正常路径 + 失败/降级</h4>
{mw("diag-appx-polar-fail", '''
flowchart TD
  OK[正常写主] --> Commit[提交成功]
  Commit --> Read[读主确认]
  Commit --> Async[CDC/异步]
  Fail[写入失败/超时] --> Retry{可重试?}
  Retry -->|幂等键命中| Idem[返回原结果]
  Retry -->|是| Backoff[退避重试]
  Retry -->|否| Degrade[降级公告/排队]
  LagSpike[RO 延迟尖刺] --> ForcePrimary[关键读切主]
  CrossShard[跨片拖垮] --> Block[SQL 审核阻断 + 改分片键]
  CDCBad[CDC 乱序重复] --> Upsert[下游幂等 upsert + 对账]
''')}

  <h4 id="appx-polar-spec">3.6 生产配置与规范</h4>
  <p><b>大基线（集群级，少变）：</b>金融向 flush/sync、超时、连接上限、慢日志阈值、只读权限。<b>小基规则（库/业务级）：</b>单表行数告警、禁止无 WHERE UPDATE、强制分片键等值、禁止 SELECT * 大宽表。</p>
  <table>
    <thead><tr><th>规范域</th><th>示例条款</th><th>巡检方式</th></tr></thead>
    <tbody>
      <tr><td>持久化</td><td>金融：flush/sync 取向 RPO≈0；电商可分级</td><td>参数快照 vs 大基线</td></tr>
      <tr><td>连接</td><td>max_connections 与池总和匹配；禁止应用 root</td><td>SHOW VARIABLES + 进程列表</td></tr>
      <tr><td>复制/RO</td><td>延迟阈值；读写分离策略文档化</td><td>延迟指标 + 连接串审计</td></tr>
      <tr><td>SQL</td><td>慢日志 ON；long_query_time 分级</td><td>变量 + 慢日志落地</td></tr>
      <tr><td>对象</td><td>主键、必要二级索引、禁止无端日期大扫</td><td>information_schema + EXPLAIN</td></tr>
      <tr><td>X 分片</td><td>过滤必带分片键或合法拓扑</td><td>SQL 审核 + 跨片比看板</td></tr>
    </tbody>
  </table>

  <h4 id="appx-polar-runbook">3.7 排障 Runbook</h4>
  <table>
    <thead><tr><th>症状</th><th>假设</th><th>验证</th><th>动作</th></tr></thead>
    <tbody>
      <tr><td>付后详情仍「待支付」</td><td>读到 RO 延迟窗口</td><td>对比主/RO 同行；看 lag</td><td>关键读切主；修路由中间件</td></tr>
      <tr><td>CN CPU 满、DN 空闲</td><td>大量跨片/广播计划</td><td>看计划类型与跨片比</td><td>补分片键；审核拦截；热点拆分</td></tr>
      <tr><td>单 DN 打满</td><td>热点买家/商品片</td><td>DN 负载与分片统计</td><td>加盐/隔离热点；限流写</td></tr>
      <tr><td>错片/找不到表</td><td>GMS 与 CN 缓存版本不一致</td><td>对 schema_version / 拓扑</td><td>失效 CN 缓存；DDL 窗口重做</td></tr>
      <tr><td>CDC 下游双记</td><td>重复投递当插入</td><td>查幂等键/位点</td><td>upsert；权威回库对账</td></tr>
      <tr><td>连接打满</td><td>池泄漏或 max_connections 过小</td><td>Threads_connected + 池监控</td><td>杀泄漏；调池与上限匹配</td></tr>
    </tbody>
  </table>

  <h4 id="appx-polar-redline">3.8 红线（一致性/资损）</h4>
  <ul>
    <li>付后读己之写必须打主；RO 延迟不是「偶发可接受」对支付回跳。</li>
    <li>PolarDB-X 无分片键设计禁止上生产写路径。</li>
    <li>CDC/Kafka 不得替代 Outbox 做资损权威。</li>
    <li>修数/DDL/改参：工单+双人；Agent/MCP 禁止写账号。</li>
  </ul>
  <div class="company-prd" id="appx-polar-case-1"><div class="label">Polar · 付后读 RO（案例归纳）</div>
    <p><b>完整业务场景：</b>支付成功后详情页读到旧订单态，客服以为未支付。</p>
    <p><b>技术落地配置：</b>交易读主；报表/搜索走 RO；连接串或中间件强制策略。</p>
    <p><b>线上真实故障：</b>延迟尖刺窗口读 RO。</p>
    <p><b>分步优化：</b>1) 会话级读主 2) 延迟监控 3) 关键路径拨测。</p>
    <p><b>落地效果数据：</b>工程目标：付后读己不一致客诉趋近 0（示意）。</p>
  </div>
  <div class="company-prd" id="appx-polar-case-2"><div class="label">PolarDB-X · 跨片事务拖垮（案例归纳）</div>
    <p><b>完整业务场景：</b>未带分片键的订单更新打成两阶段，大促 RT 崩。</p>
    <p><b>技术落地配置：</b>分片键=买家或订单号；SQL 审核拦截缺失分片键。</p>
    <p><b>线上真实故障：</b>CN CPU 打满，DN 空闲。</p>
    <p><b>分步优化：</b>1) 审核门禁 2) 热点片拆分 3) 压测回放。</p>
    <p><b>落地效果数据：</b>工程目标：跨片比例下降、P99 回落（示意）。</p>
  </div>
  <div class="koujue"><div class="label">口诀</div>Polar 口诀：先分产品，付后读主；跨片先审，CDC 旁路；权威在库，修数双人。</div>

"""


def sql_agents() -> str:
    return f"""  <!-- ========== SQL AGENTS ========== -->
  <h3 id="appx-sql-agents">5. SQL 方向智能体完整落地（AgentScope + Skills + MCP + RAG）</h3>
  <div class="plain"><div class="label">人话版</div>SQL 智能体=用 AI 做「审核员/巡检员」：RAG 给条款 ID，Skill 给动作剧本，MCP 给只读手；写库只出变更单。主菜运行时见 <a href="#appx-agentscope-src">#appx-agentscope-src</a>。</div>
  <h4 id="appx-sql-arch">5.1 总架构</h4>
{mw("diag-appx-sql-agent", '''
flowchart TB
  User[DBA/研发/CI] --> Agent[AgentScope ReAct]
  Agent --> Skills[Skills: 参数/性能/基线/Git SQL/索引慢SQL]
  Agent --> MCP[MCP: Polar只读 / Git Diff / 工单]
  Agent --> RAG[RAG: 大基线+小基规则+历史慢SQL+事故复盘]
  Skills --> Report[结构化报告+变更单草稿]
  Report --> Gate[CI/合并门禁]
''')}
{mw("diag-appx-sql-dataflow", '''
flowchart LR
  Diff[PR Diff] --> Review[git-sql-review]
  Slow[慢日志 TopN] --> Audit[index-slow-audit]
  Snap[参数快照] --> Param[polar-param-inspect]
  Review --> Cite[条款 ID 引用]
  Audit --> Cite
  Param --> Cite
  Cite --> Draft[变更单草稿]
  Draft --> HITL[人工/DBA]
  HITL -->|通过| Change[变更窗口执行]
  HITL -.->|拒绝| Back[回评测集]
''')}
{mw("diag-appx-sql-fail", '''
flowchart TD
  Run[Agent 巡检] --> Risk{高危?}
  Risk -->|无 WHERE DELETE/UPDATE| Block[阻断合并]
  Risk -->|拟 DDL| DraftOnly[只出草稿禁止执行]
  Risk -->|证据不足| Ask[追问/转人工]
  Risk -->|MCP 超时| Degrade[降级: 仅静态规则]
  Block --> AuditLog[审计]
  DraftOnly --> AuditLog
''')}
  <h4 id="appx-sql-skills">5.2 Skills 清单</h4>
  <table>
    <thead><tr><th>Skill</th><th>输入</th><th>输出</th><th>红线</th></tr></thead>
    <tbody>
      <tr><td><code>polar-param-inspect</code></td><td>参数快照</td><td>违规条款、建议值、是否需重启</td><td>禁止改参，只建议</td></tr>
      <tr><td><code>polar-perf-inspect</code></td><td>状态/等待事件/TOP SQL</td><td>瓶颈假设、下一步取证</td><td>禁止杀会话除非人工确认</td></tr>
      <tr><td><code>baseline-large</code></td><td>集群角色(金融/电商)</td><td>大基线差分</td><td>条款 ID 必须来自 RAG</td></tr>
      <tr><td><code>baseline-small</code></td><td>库名/业务域</td><td>小基规则命中</td><td>无证据不判死刑</td></tr>
      <tr><td><code>git-sql-review</code></td><td>PR diff</td><td>风险 SQL、索引建议、是否阻断合并</td><td>不直接推远程</td></tr>
      <tr><td><code>index-slow-audit</code></td><td>慢日志+EXPLAIN</td><td>指纹治理清单</td><td>DDL 只出草稿</td></tr>
    </tbody>
  </table>
  <h4 id="appx-sql-mcp-rag">5.3 MCP 与 RAG</h4>
  <ul>
    <li><b>MCP-Polar-RO：</b>只读账号；语句白名单（SHOW/SELECT/EXPLAIN）；超时与行数上限。</li>
    <li><b>MCP-Git：</b>读 PR diff / 文件；不写仓库。</li>
    <li><b>MCP-Ticket：</b>创建变更单草稿（可选）。</li>
    <li><b>RAG 语料：</b>大基线 Markdown、小基规则 YAML、历史慢 SQL 指纹库、事故复盘；版本化；检索要带来源条款 ID。</li>
  </ul>
  <h4 id="appx-sql-runbook">5.4 排障 / 红线</h4>
  <table>
    <thead><tr><th>症状</th><th>假设</th><th>验证</th><th>动作</th></tr></thead>
    <tbody>
      <tr><td>Agent「建议直接 ALTER」</td><td>Skill 红线缺失</td><td>查 SKILL.md 禁止项</td><td>改 Skill；CI 断言无执行动词</td></tr>
      <tr><td>条款无来源 ID</td><td>RAG 未命中仍下结论</td><td>报告字段 cite</td><td>强制 cite 或标「证据不足」</td></tr>
      <tr><td>连上写账号</td><td>MCP 配错</td><td>账号权限审计</td><td>立刻撤写权限；事故复盘</td></tr>
    </tbody>
  </table>
  <h4 id="appx-sql-workflow">5.5 工作流</h4>
  <ol>
    <li>CI 触发：拉取 diff → <code>git-sql-review</code>。</li>
    <li>命中高危 → <b>阻断合并</b>。</li>
    <li>中危 → 评论区结构化意见 + 人工确认。</li>
    <li>周批：慢日志 TopN → <code>index-slow-audit</code> → 治理看板。</li>
  </ol>
  <pre><code># skills/git-sql-review/SKILL.md（示意片段）
名称: git-sql-review
描述: 审核 Git 变更中的 SQL/DDL/Mapper；输出风险与是否阻断。
禁止: 连接生产写账号；自动执行 DDL；跳过条款 ID。
</code></pre>
  <div class="koujue"><div class="label">口诀</div>SQL 智能体：RAG 给条款，Skill 给动作，MCP 给只读手；写库只出单。</div>

"""


def xxl_deep() -> str:
    return f"""  <!-- ========== XXL-JOB ========== -->
  <h3 id="appx-xxl">6. XXL-JOB 用法与原理深挖（生产+源码）</h3>
  <div class="plain"><div class="label">人话版</div>XXL-JOB=「谁在几点跑哪段业务」的调度台：Admin 负责触发与路由，Executor 嵌在业务 JVM 真正干活。调度至少一次 → Job 内必须业务幂等（对账/补数/关单/巡检同纪律）。</div>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>正逆向批处理：关单、对账、补数、缓存预热、SQL 巡检批、CDC 缺口回补。<br><b>服务业务闭环：</b>支付未知态对账 / 售后补偿 / 库存校准<br><b>挂回：</b><a href="#appx-kafka-src">Kafka 补数</a> · <a href="#appx-sql-agents">SQL Agent 批</a> · <a href="#ency-fm-polardb">Polar 权威库</a></div>

  <h4 id="appx-xxl-pos">6.0 定位</h4>
  <table>
    <thead><tr><th>闭环场景</th><th>XXL 干什么</th><th>不干什么</th></tr></thead>
    <tbody>
      <tr><td>支付未知态</td><td>按窗口拉渠道对账、写对账表</td><td>直接改余额无工单</td></tr>
      <tr><td>关单/超时取消</td><td>扫描过期预占 → 调状态机</td><td>无幂等盲更新</td></tr>
      <tr><td>售后补偿</td><td>失败补偿重试批</td><td>绕过状态机打款</td></tr>
      <tr><td>SQL/参数巡检</td><td>触发只读 Agent 批</td><td>自动 DDL/改参</td></tr>
    </tbody>
  </table>

  <h4 id="appx-xxl-arch">6.1 架构与源码级路径</h4>
  <ul>
    <li><b>Admin（调度中心）：</b>UI、任务配置、触发、日志、报警、执行器管理。</li>
    <li><b>Executor（执行器）：</b>嵌业务进程；注册、接收派发、跑 <code>IJobHandler</code>、回调日志。</li>
    <li><b>调度 ≠ 执行：</b>重业务禁止塞进 Admin 进程。</li>
  </ul>
  <pre><code>// 源码阅读地图（开源 xxl-job，版本以你们依赖为准 · 示意包名）
// admin:  JobScheduleHelper（调度线程扫描）
//         JobTriggerPoolHelper（触发线程池）
//         ExecutorBizClient（HTTP 调执行器）
// executor: XxlJobExecutor / EmbedServer
//           JobThread + TriggerCallbackThread
//           注解 @XxlJob → 方法级 Handler
// 存储:  xxl_job_info / xxl_job_log / xxl_job_registry（Admin DB）
</code></pre>
{mw("diag-appx-xxl", '''
sequenceDiagram
  participant Cron as JobScheduleHelper
  participant Pool as TriggerPool
  participant Admin as XXL-Admin
  participant Ex as Executor EmbedServer
  participant Biz as @XxlJob Handler
  Cron->>Pool: 到期任务
  Pool->>Admin: 选路由/写日志
  Admin->>Ex: HTTP run
  Ex->>Biz: 执行业务
  Biz-->>Ex: 成功/失败
  Ex-->>Admin: callback 日志
''')}
{mw("diag-appx-xxl-threads", '''
flowchart TB
  subgraph AdminJVM
    S[调度线程时间轮/扫描] --> T[触发线程池]
    T --> R[路由策略]
    R --> H[HTTP 派发]
    CB[回调接收] --> Log[(xxl_job_log)]
  end
  subgraph ExecJVM
    Reg[注册心跳] --> AdminJVM
    Emb[EmbedServer] --> JT[JobThread 队列]
    JT --> Hdl[JobHandler]
    Hdl --> CBout[CallbackThread]
    CBout --> CB
  end
''')}

  <h4 id="appx-xxl-dataflow">6.2 数据流：触发 → 业务 → 落库/MQ</h4>
{mw("diag-appx-xxl-dataflow", '''
flowchart LR
  Fire[调度触发] --> Admin[Admin 路由]
  Admin --> Ex[Executor]
  Ex --> Lock{幂等锁/runId}
  Lock -->|已跑| Skip[跳过]
  Lock -->|未跑| Biz[业务]
  Biz --> DB[(Polar 权威表)]
  Biz --> MQ[发 Kafka/Rocket 补偿]
  Biz --> Report[对账/巡检报告]
  Ex --> Log[回调 Admin 日志]
''')}

  <h4 id="appx-xxl-flow">6.3 正常 / 失败 / 重试 / 「死信」</h4>
{mw("diag-appx-xxl-flow", '''
flowchart TD
  Trig[触发] --> Run[Executor 执行]
  Run --> OK{成功?}
  OK -->|是| CB1[回调成功]
  OK -->|否| Retry{失败重试策略}
  Retry -->|可重试| Wait[退避/下次调度]
  Retry -->|超限| Alarm[告警+工单]
  Alarm --> Manual[人工补跑/修数]
  Block{阻塞策略} -->|单机串行| Queue[排队]
  Block -->|丢弃后续| Drop[记日志]
  Block -->|覆盖| KillPrev[终止前次·慎用]
''')}
  <p>XXL 无 Kafka 式 DLQ 主题；「死信」=失败超限日志+告警+人工。对账类必须可按 <code>runId</code> 重跑且幂等。</p>

  <h4 id="appx-xxl-ops">6.4 操作图：部署 / 扩缩 / 发布 / 巡检</h4>
{mw("diag-appx-xxl-ops", '''
flowchart TB
  Prep[非 root 部署 Admin+Executor] --> Health[探活 Admin UI / 执行器注册]
  Health --> Canary[灰度 1 台 Executor]
  Canary --> Full[扩容注册更多 Executor]
  Full --> Job[启停任务/改 Cron]
  Job --> Roll{发布?}
  Roll -->|业务发版| Drain[先停分片任务 → 发版 → 注册 → 试跑]
  Roll -->|回滚| Prev[回滚包 + 禁危险任务]
  Full --> Inspect[巡检: 失败率/耗时/注册丢失]
''')}
  <ol>
    <li><b>部署：</b>Admin、Executor 均非 root；Admin DB 独立；访问控制+登录审计。</li>
    <li><b>扩容：</b>加 Executor 实例自动注册；分片广播任务分片数与实例数匹配。</li>
    <li><b>发布：</b>先停长任务/锁分片 → 发版 → 注册成功 → 手工触发试跑 → 再开 Cron。</li>
    <li><b>巡检：</b></li>
  </ol>
  <pre><code># 示意
curl -fsS http://127.0.0.1:8080/xxl-job-admin/  # 需登录态/内网
# Admin DB
SELECT trigger_code, handle_code, COUNT(*) FROM xxl_job_log
 WHERE trigger_time &gt; NOW() - INTERVAL 1 HOUR GROUP BY 1,2;
# 执行器进程
jps | grep -i xxl
# 业务侧：对账表按 fireTime 缺口；禁止 root 启停
</code></pre>

  <h4 id="appx-xxl-prod">6.5 生产配置清单</h4>
  <table>
    <thead><tr><th>项</th><th>建议</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td>路由</td><td>故障转移 / 分片广播</td><td>分片键与数据分片一致</td></tr>
      <tr><td>阻塞</td><td>单机串行（对账）</td><td>慢 Job 勿「覆盖」乱杀</td></tr>
      <tr><td>超时</td><td>按 SLA 设；超时告警</td><td>超时≠自动幂等成功</td></tr>
      <tr><td>权限</td><td>按执行器组授权</td><td>生产改 Cron 走变更单</td></tr>
      <tr><td>多环境</td><td>Admin 隔离；Job 命名带 env</td><td>禁止测网打生产库</td></tr>
      <tr><td>监控</td><td>失败率、耗时 P99、注册数</td><td>注册丢失=静默停调度</td></tr>
    </tbody>
  </table>
  <pre><code>// 示意：Job 幂等键
String runId = jobId + ":" + shardIndex + ":" + fireTime;
if (!lock.try(runId)) return; // 已跑过
try {{ doBiz(); }} finally {{ /* 成功才标完成；失败可重跑 */ }}
</code></pre>

  <h4 id="appx-xxl-runbook">6.6 排障 Runbook</h4>
  <table>
    <thead><tr><th>症状</th><th>假设</th><th>验证</th><th>动作</th></tr></thead>
    <tbody>
      <tr><td>任务不触发</td><td>Cron/调度线程/注册丢失</td><td>Admin 下次触发时间；registry 表</td><td>修注册；检查 Admin 时钟</td></tr>
      <tr><td>重复执行双记</td><td>无幂等 + 失败重试</td><td>对账表唯一键冲突</td><td>补 runId 锁；修数工单</td></tr>
      <tr><td>大面积超时</td><td>下游库/接口慢</td><td>Job 日志 RT；DB 慢查询</td><td>降并发；切只读；扩容</td></tr>
      <tr><td>分片漏数据</td><td>分片数与模不一致</td><td>抽样缺口</td><td>对齐分片；全量补跑窗口</td></tr>
      <tr><td>执行器都挂</td><td>发版未注册 / 端口</td><td>registry 空</td><td>拉起 Executor；临时 Admin 禁任务</td></tr>
    </tbody>
  </table>

  <h4 id="appx-xxl-redline">6.7 红线</h4>
  <ul>
    <li><b>重复执行：</b>调度至少一次；无幂等=双扣/双补风险。</li>
    <li><b>覆盖杀任务：</b>可能留下半成功状态；金融批禁用。</li>
    <li><b>Admin 跑重业务：</b>拖垮调度中心=全域静默。</li>
    <li><b>测网 Job 打生产：</b>环境隔离与账号隔离必须物理分开。</li>
  </ul>
{mw("diag-appx-xxl-c4", '''
flowchart TB
  subgraph People
    Ops[值班/DBA]
  end
  subgraph System
    Admin[XXL-Admin]
    Exec[业务 Executor]
    BizAPI[订单/对账状态机]
    DB[(Polar)]
  end
  Ops --> Admin
  Admin -->|派发| Exec
  Exec --> BizAPI
  BizAPI --> DB
  Exec -->|禁止直改账| Ledger[(支付账本)]
''')}
  <div class="koujue"><div class="label">口诀</div>XXL 口诀：Admin 只调度，业务在 Executor；分片对齐，runId 幂等；失败告警，修数走工单。</div>

"""


def kafka_deep() -> str:
    return f"""  <!-- ========== KAFKA SRC ========== -->
  <h3 id="appx-kafka-src">7. Kafka 用法 / 原理 / 底层源码深挖（生产加厚）</h3>
  <div class="plain"><div class="label">人话版</div>Kafka=分布式提交日志：按分区并行写、ISR 保副本、消费者组读进度。恰好一次有边界——跨出 Kafka 进 Polar 仍靠外储幂等+对账。全貌索引见 <a href="#ency-fm-kafka">#ency-fm-kafka</a>（ENCY 仍标骨架；<b>本节为生产+源码加厚主菜</b>）。</div>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>轨迹/CDC/对账/画像高吞吐事件总线；与 Rocket 事务消息分工不同。<br><b>服务业务闭环：</b>物流轨迹、清结算流水、搜推入湖、补数回放<br><b>挂回：</b><a href="#ency-fm-polardb">Polar CDC</a> · <a href="#appx-xxl">XXL 补数</a> · Outbox</div>
  <div class="callout danger"><div class="label">诚实门禁</div>ENCY-FM-Kafka 未宣称金标；本 APPX 节补齐操作/数据流/失败流/Runbook。勿把本节写成「全书 Kafka 已金标」。</div>

  <h4 id="appx-kafka-pos">7.0 定位</h4>
  <table>
    <thead><tr><th>场景</th><th>Kafka 角色</th><th>权威仍在</th></tr></thead>
    <tbody>
      <tr><td>运单轨迹</td><td>按 waybillId 保序投递</td><td>轨迹 upsert 表</td></tr>
      <tr><td>CDC 入湖</td><td>变更总线</td><td>OLTP 库 / Outbox</td></tr>
      <tr><td>清结算流水</td><td>隔离 topic 高可靠投递</td><td>分户账+日终对账</td></tr>
      <tr><td>画像点击</td><td>高吞吐可丢窗口+补数</td><td>补数任务/数仓校验</td></tr>
    </tbody>
  </table>

  <h4 id="appx-kafka-log">7.1 日志存储源码路径</h4>
  <ul>
    <li><b>Partition = 有序日志：</b>*.log + *.index + *.timeindex。</li>
    <li><b>顺序写：</b>页缓存 + append；吞吐来自顺序 I/O。</li>
    <li><b>零拷贝：</b>热路径 sendfile/transferTo 思想；冷读不总是。</li>
    <li><b>HW / LEO：</b>ISR 内最小 LEO 推进 HW；消费者可见性≤HW。</li>
  </ul>
  <pre><code>// Apache Kafka 源码地图（版本以依赖为准）
// produce: KafkaProducer.doSend → RecordAccumulator → Sender
// broker:  ReplicaManager.appendRecords → UnifiedLog / LogSegment
// replica: Partition / ISR 收缩膨胀 / ReplicaFetcherThread
// group:   GroupCoordinator / __consumer_offsets
// network: SocketServer / KafkaChannel
</code></pre>
{mw("diag-appx-kafka-src", '''
flowchart TB
  Prod[Producer] -->|acks/ISR| Leader[Leader Partition]
  Leader --> Seg[LogSegment]
  Leader --> Followers[ISR Followers]
  Cons[Consumer Group] -->|fetch &lt;=HW| Leader
  Cons --> Coord[GroupCoordinator]
''')}
{mw("diag-appx-kafka-produce-path", '''
sequenceDiagram
  participant P as KafkaProducer
  participant Acc as Accumulator
  participant Br as Broker Leader
  participant ISR as ISR Followers
  P->>Acc: doSend/分区/批次
  Acc->>Br: ProduceRequest
  Br->>Br: append LogSegment
  Br->>ISR: 复制
  alt acks=all 且 ISR 足够
    Br-->>P: 成功 offset
  else ISR &lt; min.insync
    Br-->>P: NotEnoughReplicas
  end
''')}

  <h4 id="appx-kafka-dataflow">7.2 端到端数据流</h4>
{mw("diag-appx-kafka-dataflow", '''
flowchart LR
  App[业务写 Polar] --> OB[Outbox]
  OB --> Prod[Producer key=orderId]
  Prod --> T[Topic-Partition]
  T --> ISR[ISR 复制]
  T --> CG[Consumer Group]
  CG --> Idem[(幂等表)]
  CG --> Down[履约/搜推/数仓]
  CDC[Polar CDC] -.->|旁路| T2[cdc topic]
  T2 --> Lake[入湖]
''')}
{mw("diag-appx-kafka-consume", '''
flowchart TD
  Poll[poll] --> Proc[处理业务]
  Proc --> OK{成功?}
  OK -->|是| Commit[commitSync 位移]
  OK -->|否| Retry[重试/退避]
  Retry -->|超限| DLQ[死信 topic 或旁路表]
  DLQ --> Alert[告警+XXL 补数]
  Note[禁止: 先提交后处理]
''')}

  <h4 id="appx-kafka-flow">7.3 正常 / 失败 / 重试 / 死信 / 降级</h4>
{mw("diag-appx-kafka-fail", '''
flowchart TD
  Write[生产] --> WOK{写入成功?}
  WOK -->|ISR 不足| WFail[失败可重试/告警]
  WOK -->|是| Avail[HW 可见]
  Avail --> Cons[消费]
  Cons --> COK{处理成功?}
  COK -->|是| Commit[提交位移]
  COK -->|可重试| R1[不提交 · 重试]
  COK -->|毒消息| DLQ[DLQ + 跳过提交策略]
  Rebalance[频繁 rebalance] --> Fix[降处理时长/调 max.poll.interval]
  Hot[单分区热点] --> Salt[key 加盐/扩分区]
''')}

  <h4 id="appx-kafka-ops">7.4 操作图：部署 / 扩缩 / 切换 / 巡检</h4>
{mw("diag-appx-kafka-ops", '''
flowchart TB
  Deploy[ZK/KRaft 集群部署] --> Topic[建 Topic RF/min.insync]
  Topic --> ACL[ACL/SSL 多环境隔离]
  ACL --> Scale{扩缩?}
  Scale -->|加 Broker| Reassign[分区再分配]
  Scale -->|扩分区| Warn[注意 key 保序历史]
  Scale -->|控副本| Prefer[优先副本选举]
  Scale --> Inspect[巡检]
  Inspect --> Lag[消费组 lag]
  Inspect --> ISR[ISR 不足告警]
  Inspect --> Disk[磁盘/保留]
''')}
  <pre><code># 命令级巡检示意（路径/脚本按发行版调整）
kafka-topics.sh --bootstrap-server $BS --describe --topic order_event
kafka-consumer-groups.sh --bootstrap-server $BS --describe --group fulfill_cg
# 关注: LAG、LOG-END-OFFSET、成员数、分区分配
# 生产拒绝: 无变更单重置位点；无隔离共集群挤 ISR
</code></pre>

  <h4 id="appx-kafka-isr">7.5 复制 ISR / EOS / 消费者组</h4>
  <ul>
    <li><code>acks=all</code> + <code>min.insync.replicas</code>：ISR 不足拒绝写入。</li>
    <li>PID+序号：会话内防重试双写；<b>不等于</b>下游 DB 恰好一次。</li>
    <li>事务/EOS：链路内原子可见；外系统仍要幂等表+对账。</li>
    <li>位移：手动提交；先处理成功再提交。</li>
  </ul>

  <h4 id="appx-kafka-ops-cfg">7.6 生产配置清单</h4>
  <table>
    <thead><tr><th>层</th><th>基线（示意）</th><th>注意</th></tr></thead>
    <tbody>
      <tr><td>Topic</td><td>RF=3，min.insync=2</td><td>金融与营销隔离</td></tr>
      <tr><td>Producer</td><td>acks=all，idempotence=true</td><td>业务 key 保序</td></tr>
      <tr><td>Consumer</td><td>auto.commit=false</td><td>幂等外储</td></tr>
      <tr><td>保留</td><td>覆盖补数窗口</td><td>与 CDC/对账对齐</td></tr>
      <tr><td>监控</td><td>ISR、lag、UnderReplicated</td><td>进值班看板</td></tr>
    </tbody>
  </table>

  <h4 id="appx-kafka-runbook">7.7 排障 Runbook</h4>
  <table>
    <thead><tr><th>症状</th><th>假设</th><th>验证</th><th>动作</th></tr></thead>
    <tbody>
      <tr><td>轨迹乱序</td><td>无 key / 错分区</td><td>看消息 key 与分区</td><td>强制业务 key；消费 seq upsert</td></tr>
      <tr><td>生产报错 NotEnoughReplicas</td><td>ISR&lt;min.insync</td><td>描述 topic ISR</td><td>修慢副本/磁盘；勿盲目降 min.insync</td></tr>
      <tr><td>lag 飙升</td><td>消费慢/下游挂</td><td>组 describe + 下游 RT</td><td>扩消费者；修下游；临时限产</td></tr>
      <tr><td>重复入账</td><td>吹 EOS 无外储幂等</td><td>唯一键冲突/对账差</td><td>补幂等表；对账修数</td></tr>
      <tr><td>频繁 rebalance</td><td>处理超 max.poll.interval</td><td>成员反复加入退出</td><td>降批或提间隔；查 GC</td></tr>
    </tbody>
  </table>

  <h4 id="appx-kafka-redline">7.8 红线</h4>
  <ul>
    <li>无 key 却要求业务有序 → 轨迹回退/客诉。</li>
    <li>EOS 当跨系统账本 → 双记资损。</li>
    <li>先提交位移后处理 → 丢更新。</li>
    <li>清结算与营销高吞吐共挤 ISR → RPO 事故。</li>
  </ul>
{mw("diag-appx-kafka-c4", '''
flowchart TB
  ProdSys[订单/轨迹服务] --> KP[KafkaProducer]
  KP --> Cluster[Kafka Cluster]
  Cluster --> Fulfill[履约消费组]
  Cluster --> Lake[CDC/入湖]
  Cluster --> Recon[对账消费组]
  Fulfill --> Polar[(Polar 幂等/状态机)]
  Recon --> XXL[XXL 缺口补数]
''')}
  <div class="koujue"><div class="label">口诀</div>Kafka 口诀：认 HW/ISR，key 保序；位移后置，幂等外储；EOS 不跨库，对账收口。</div>

"""


def ai_agentscope_extra() -> str:
    """Insert before UT gate in agentscope section."""
    return f"""
  <h4 id="appx-as-ops-deep">4.1 操作图：多环境发布 / 回滚 / 扩缩</h4>
{mw("diag-appx-as-ops", '''
flowchart TB
  Dev[dev 匿名可开] --> Staging[staging 强制 Token]
  Staging --> Canary[canary 小流量]
  Canary --> Prod[prod allow-anonymous=false]
  Prod --> Health[ /health + WS 冒烟]
  Health --> Scale{{扩缩}}
  Scale -->|加副本| Sticky[粘性会话或外置 StateStore]
  Scale -->|缩容| Drain[interrupt 进行中会话]
  Prod --> Roll{{回滚}}
  Roll -->|坏模型/提示| Pin[钉回 model+prompt+kb 版本]
  Roll -->|坏工具| Disable[下线工具组 + checkpoint 指引]
''')}
{mw("diag-appx-as-dataflow", '''
flowchart LR
  U[用户] --> WS[WS chat]
  WS --> Mem[注入个人记忆块]
  Mem --> RA[ReActAgent]
  RA --> LLM[DeepSeek]
  RA --> Tools[Toolkit 白名单]
  Tools --> Sandbox[SandboxPathGuard]
  Tools --> RO[只读 MCP/Polar]
  Tools -.->|拒绝| WriteDB[写库/打款]
  RA --> State[(agent_state)]
  RA --> Audit[审计事件流]
''')}
{mw("diag-appx-as-mcp-deny", '''
stateDiagram-v2
  [*] --> ToolCall
  ToolCall --> PermissionCheck
  PermissionCheck --> Allow: 白名单只读
  PermissionCheck --> Deny: 写库/打款/DDL
  Allow --> Execute
  Execute --> Observe
  Deny --> ObserveDeny: 写入观察「拒绝原因」
  Observe --> [*]
  ObserveDeny --> [*]
''')}
  <h4 id="appx-as-runbook-deep">4.2 AI 支柱排障表（补强）</h4>
  <table>
    <thead><tr><th>症状</th><th>假设</th><th>验证</th><th>动作</th></tr></thead>
    <tbody>
      <tr><td>模型建议退款并要调工具</td><td>写工具误注册</td><td>Toolkit 列表 / Permission 日志</td><td>物理下线写工具；复盘 Skill</td></tr>
      <tr><td>口径与过期规则一致</td><td>RAG kbVer 未钉扎</td><td>审计中的 kbVer</td><td>回滚知识版本；评测门禁</td></tr>
      <tr><td>改码越出沙箱</td><td>路径校验绕过</td><td>Sandbox 拒绝日志</td><td>修 Guard；吊销会话</td></tr>
      <tr><td>公网匿名滥用</td><td>allow-anonymous=true</td><td>配置与限流计数</td><td>关匿名+Token；收紧限流</td></tr>
    </tbody>
  </table>
  <h4 id="appx-as-redline">4.3 AI 红线汇总</h4>
  <ul>
    <li>MCP/Tool <b>禁止</b>生产写库、打款、改分摊；只出草稿+HITL。</li>
    <li>Studio 对照：真实接线为 DeepSeek + Edge TTS + <code>SandboxPathGuard</code> + 三盘记忆；不编造 KPI。</li>
    <li>评测集不过禁止升 kb/prompt；大促可降级关闭 Agent 写意图通道。</li>
  </ul>

"""


def t_ai_boost_skills() -> str:
    return f"""
  <h3 id="tskills-ops">生产操作：Skill 发布 / 回滚 / 多环境</h3>
{mw("diag-tskills-ops", '''
flowchart TB
  Edit[改 SKILL.md] --> PR[PR 评审]
  PR --> CI[评测集冒烟]
  CI --> Pin[钉 skillVer]
  Pin --> Stg[staging 显式触发]
  Stg --> Prod[prod 灰度描述触发]
  Prod --> Bad{{口径漂移?}}
  Bad -->|是| Rollback[回滚 skillVer]
  Bad -->|否| Keep[保留并记采纳率]
''')}
{mw("diag-tskills-dataflow", '''
flowchart LR
  Ticket[工单/用户问] --> Match[描述匹配]
  Match --> Skill[加载步骤]
  Skill --> MCP[只读 MCP]
  Skill --> RAG[带 cite RAG]
  Skill --> Draft[检查单草稿]
  Draft --> HITL[人工]
  HITL --> SM[状态机 API]
''')}
  <table>
    <thead><tr><th>症状</th><th>假设</th><th>验证</th><th>动作</th></tr></thead>
    <tbody>
      <tr><td>同场景口径不一致</td><td>多 Skill 冲突/未版本化</td><td>审计 skillVer</td><td>合并 Skill；强制显式触发</td></tr>
      <tr><td>跳过资损检查项</td><td>步骤非强制</td><td>输出缺字段</td><td>改 schema 门禁</td></tr>
    </tbody>
  </table>
"""


def t_ai_boost_mcp() -> str:
    return f"""
  <h3 id="tmcp-ops">生产操作与数据流加深</h3>
{mw("diag-tmcp-dataflow", '''
sequenceDiagram
  participant A as Agent
  participant C as MCP Client
  participant G as 工具网关
  participant S as order.get
  A->>C: tools/call
  C->>G: 身份+租户+限流
  alt 写工具
    G-->>C: 403 拒绝+审计
  else 只读允许
    G->>S: 查询
    S-->>A: 结构化脱敏结果
  end
''')}
{mw("diag-tmcp-fail", '''
flowchart TD
  Call[工具调用] --> Auth{鉴权}
  Auth -->|失败| Deny[拒绝]
  Auth -->|通过| RO{只读?}
  RO -->|否| Block[默认阻断写]
  RO -->|是| Exec[执行]
  Exec --> Timeout{超时?}
  Timeout -->|是| Deg[降级人工查后台]
  Timeout -->|否| OK[返回]
''')}
  <table>
    <thead><tr><th>症状</th><th>假设</th><th>验证</th><th>动作</th></tr></thead>
    <tbody>
      <tr><td>批量查单打满库</td><td>无限流</td><td>QPS 与慢查询</td><td>网关限流；熔断工具</td></tr>
      <tr><td>越权看他单</td><td>身份未穿透</td><td>审计 userId 范围</td><td>修数据范围校验</td></tr>
    </tbody>
  </table>
"""


def t_ai_boost_rag() -> str:
    return f"""
  <h3 id="trag-ops">RAG 数据流 / 失败降级 / 红线</h3>
{mw("diag-trag-dataflow", '''
flowchart LR
  Doc[规则/Runbook] --> Chunk[分块+版本]
  Chunk --> Emb[向量/BM25]
  Emb --> Ret[TopK 检索]
  Ret --> Cite[强制引用条款 ID]
  Cite --> Gen[生成草稿]
  Gen --> HITL[人工]
''')}
{mw("diag-trag-fail", '''
flowchart TD
  Q[提问] --> Hit{检索命中?}
  Hit -->|否| Abstain[拒绝编造/转人工]
  Hit -->|是| Conf{置信/条款有效?}
  Conf -->|过期| Warn[提示过期+阻口径]
  Conf -->|有效| Ans[带 cite 作答]
  Ans --> Eval[评测集回归]
''')}
  <ul>
    <li>无 cite 不展示退款/优惠口径。</li>
    <li>kbVer 与 promptVer、modelId 三位钉扎发布。</li>
    <li>幻觉退款口径=资损红线，进评测陷阱题。</li>
  </ul>
"""


def kafka_ency_inject() -> str:
    return f"""
  <h4 id="ency-fm-kafka-appx-bridge">5.8 APPX 生产加厚入口（本轮）</h4>
  <div class="callout"><div class="label">导航</div>操作图 / 数据流 / Runbook / 红线主菜已加厚到 <a href="#appx-kafka-src">#appx-kafka-src</a>。本节 ENCY 仍保留骨架索引，<b>不伪称金标</b>。</div>
{mw("diag-fm-kafka-e2e", '''
flowchart LR
  Outbox[业务 Outbox] --> P[Producer]
  P --> L[Leader+ISR]
  L --> CG[Consumer]
  CG --> Idem[幂等表]
  Idem --> SM[状态机]
  Fail[失败] --> DLQ[DLQ]
  DLQ --> XXL[XXL 补数]
''')}
{mw("diag-fm-kafka-ops", '''
flowchart TB
  Alert[ISR/Lag 告警] --> Triage[分诊]
  Triage --> SlowBroker[修磁盘/网络/慢副本]
  Triage --> SlowCons[扩消费者/修下游]
  Triage --> HotKey[key 加盐]
  Triage --> ACL[查误重置位点]
''')}
"""


def polar_ency_inject() -> str:
    return f"""
  <h4 id="ency-fm-polardb-appx-bridge">5.10 APPX 操作/Runbook 加厚入口</h4>
  <div class="callout"><div class="label">导航</div>金标能力面仍在本章；生产操作图、失败流、排障表加厚见 <a href="#appx-polar-deep">#appx-polar-deep</a>。</div>
{mw("diag-fm-polar-ops", '''
flowchart TB
  Window[变更窗口] --> Bak[备份确认]
  Bak --> Act{{扩RO/切主/扩片}}
  Act --> Probe[付后读主拨测]
  Probe --> Close[关闭窗口]
''')}
"""


def replace_between(text: str, start: str, end: str, new: str) -> str:
    i = text.find(start)
    j = text.find(end)
    if i < 0 or j < 0 or j <= i:
        raise SystemExit(f"markers not found or ordered wrong: {start!r} .. {end!r}")
    return text[:i] + new + text[j:]


def insert_before(text: str, marker: str, payload: str) -> str:
    i = text.find(marker)
    if i < 0:
        raise SystemExit(f"insert marker missing: {marker!r}")
    return text[:i] + payload + text[i:]


def main() -> None:
    html = HTML.read_text(encoding="utf-8")

    html = replace_between(
        html,
        "  <!-- ========== POLAR DEEP ========== -->",
        "  <!-- ========== INDEX / SLOW SQL ========== -->",
        polar_deep(),
    )
    html = replace_between(
        html,
        "  <!-- ========== SQL AGENTS ========== -->",
        "  <!-- ========== XXL-JOB ========== -->",
        sql_agents(),
    )
    html = replace_between(
        html,
        "  <!-- ========== XXL-JOB ========== -->",
        "  <!-- ========== KAFKA SRC ========== -->",
        xxl_deep(),
    )
    html = replace_between(
        html,
        "  <!-- ========== KAFKA SRC ========== -->",
        '  <h3 id="appx-close">8. 收口：今天怎么用这章</h3>',
        kafka_deep(),
    )

    # AgentScope extra before UT gate
    if 'id="appx-as-ops-deep"' not in html:
        html = insert_before(
            html,
            "  <!-- ========== 5 UT GATE ========== -->",
            ai_agentscope_extra(),
        )

    # T-AI boosts
    if 'id="tskills-ops"' not in html:
        # insert before end of t-skills section — find next section t-mcp
        html = insert_before(html, '<section class="block" id="t-mcp"', t_ai_boost_skills() + "\n")
    if 'id="tmcp-ops"' not in html:
        html = insert_before(html, '<section class="block" id="t-rag"', t_ai_boost_mcp() + "\n")
    if 'id="trag-ops"' not in html:
        html = insert_before(html, '<section class="block" id="t-agents-deep"', t_ai_boost_rag() + "\n")

    # ENCY bridges
    if 'id="ency-fm-kafka-appx-bridge"' not in html:
        html = insert_before(
            html,
            '<h4 id="ency-fm-kafka-fin-ecom">',
            kafka_ency_inject(),
        )
    if 'id="ency-fm-polardb-appx-bridge"' not in html:
        html = insert_before(
            html,
            '<h4 id="ency-fm-polardb-fin-ecom">',
            polar_ency_inject(),
        )

    # Delivery / audit honesty updates
    old_k = '<tr><td>Kafka</td><td><a href="#ency-fm-kafka">#ency-fm-kafka</a></td><td>log · isr · eos · cg</td><td>骨架可用 · 待深化</td></tr>'
    new_k = '<tr><td>Kafka</td><td><a href="#ency-fm-kafka">#ency-fm-kafka</a> · <a href="#appx-kafka-src">#appx-kafka-src</a></td><td>log · isr · eos · cg · APPX 操作/数据流/Runbook</td><td>ENCY 骨架 · <b>APPX 已加厚（非金标）</b></td></tr>'
    if old_k in html:
        html = html.replace(old_k, new_k, 1)

    # APPX TOC note
    html = html.replace(
        '<td><a href="#appx-xxl">#appx-xxl</a></td><td>XXL-JOB 用法与原理深挖</td></tr>',
        '<td><a href="#appx-xxl">#appx-xxl</a></td><td><b>XXL-JOB 生产+源码加厚</b>（操作/数据流/Runbook）</td></tr>',
        1,
    )
    html = html.replace(
        '<td><a href="#appx-kafka-src">#appx-kafka-src</a></td><td>Kafka 用法/原理/底层源码深挖</td></tr>',
        '<td><a href="#appx-kafka-src">#appx-kafka-src</a></td><td><b>Kafka 生产+源码加厚</b>（非 ENCY 金标）</td></tr>',
        1,
    )
    html = html.replace(
        '<td><a href="#appx-polar-deep">#appx-polar-deep</a></td><td><b>PolarDB 原理与规范深挖</b>（金标加厚）</td></tr>',
        '<td><a href="#appx-polar-deep">#appx-polar-deep</a></td><td><b>PolarDB 金标上再加厚</b>（操作/数据流/Runbook/红线）</td></tr>',
        1,
    )

    # Close section update
    old_close = """  <h3 id="appx-close">8. 收口：今天怎么用这章</h3>
  <ol>
    <li>先把 Polar 大基线/小基规则写成 RAG 语料 + 条款 ID。</li>
    <li>落地 2 个 Skill：<code>git-sql-review</code> + <code>index-slow-audit</code>，挂 CI。</li>
    <li>XXL 周批跑参数巡检；报告进工单，不自动改参。</li>
    <li>Kafka/Polar 探活与非 root 启停写进值班 Runbook。</li>
  </ol>
  <div class="koujue"><div class="label">口诀</div>Polar 分产品，索引看回表，慢 SQL 看指纹；Agent 只读手，条款必带来源；调度幂等，Kafka 认 HW/ISR。</div>
"""
    new_close = """  <h3 id="appx-close">8. 收口：今天怎么用这章</h3>
  <ol>
    <li>Polar：大基线/小基规则进 RAG；付后读主拨测进发布门禁；深挖见 <a href="#appx-polar-deep">#appx-polar-deep</a>。</li>
    <li>落地 Skill：<code>git-sql-review</code> + <code>index-slow-audit</code> 挂 CI；MCP 只读。</li>
    <li>XXL：对账/补数 Job 必须 runId 幂等；周批巡检只出报告；见 <a href="#appx-xxl">#appx-xxl</a>。</li>
    <li>Kafka：关键 topic RF/ISR 基线 + lag 看板；EOS 不跨库；见 <a href="#appx-kafka-src">#appx-kafka-src</a>。</li>
    <li>AI：Studio 白名单工具 + HITL；主菜 <a href="#appx-agentscope-src">#appx-agentscope-src</a>。</li>
  </ol>
  <div class="koujue"><div class="label">口诀</div>Polar 分产品付后读主；XXL 幂等；Kafka 认 HW/ISR；Agent 只读手，条款必 cite。</div>
"""
    if old_close in html:
        html = html.replace(old_close, new_close, 1)

    HTML.write_text(html, encoding="utf-8")
    print(f"updated {HTML}")


if __name__ == "__main__":
    main()
