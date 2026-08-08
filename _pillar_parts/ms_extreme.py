# -*- coding: utf-8 -*-
"""A. 分布式微服务 · 极致落地"""
from helpers import (
    qa, c4, five, tradeoff, mermaid, spine, essence, company_prd,
    plain, koujue, failbox, runbook, pit, reflect, ban, today, checklist,
)


def build() -> str:
    hub = f"""
<section class="block" id="s-ms-x" data-toc="S-MS-X · 微服务极致落地总图" data-prio="p0">
  <h2><span class="sys-id">S-MS-X</span>分布式微服务极致落地（挂正逆向脊柱）</h2>
{spine("卡点难点亮点之上的「公司真落地」加厚：边界纠纷、编排风暴、治理压测、资损可观测、中大厂对照、故障场景题。",
       serves="下单→优惠→库存→支付→OMS→售后全链",
       back="S-MS → 本极致章 → <a href='#x-promo-trinity'>交叉大促</a> / <a href='#s-year'>S-Year M09</a>")}
{essence(
    "拆服务是为了让「买成/退成」在组织与峰值下仍可对账、可回滚、可扩容——不是为了服务个数好看。",
    "验收方：交易产品、财务对账、值班 SRE。怕边界扯皮、重复支付/退款、雪崩、半灰度资损。",
    "用数据归属+调用形态+幂等/Outbox+超时舱壁+全链路压测把分布式不确定性压成可验证闭环。",
    "同步/编排/事件是手段；一致性窗口与爆炸半径是约束；指标与演练是验收。",
    "边界不清→双写打架；无幂等→重复扣款；无舱壁→库存拖死下单；无资损告警→隔天财务才发现。",
)}
{plain("人话：微服务极致落地=把「谁写哪张表、超时了怎么办、重复了怎么办、挂了伤多大」写成能值班执行的东西，而不是 PPT 上的六边形。")}
{company_prd(
    "大促前交易域要完成服务边界复盘与治理加固；历史「订单库万能」导致优惠/库存/售后互相 join。",
    "订单/优惠/库存/履约/售后边界 ADR；同步 vs 事件决策树；超时矩阵；Outbox/Inbox；限流熔断舱壁；资损告警；故障注入剧本。",
    "服务网格全家桶、自研注册中心、跨城强一致。",
    "钉验收句→拆边界→标卡点→选调用形态→验压测/对账。",
    "下游超时注入、重复回调、重复退款、灰度回滚。",
    "跨服务事务数下降；支付/退款幂等冲突可解释；全链路压测报告签字；中厂裁剪表可执行。",
    "大促窗口：支付成功率、退款成功率、Outbox 堆积、熔断次数、P99、资损告警归零。",
)}
{mermaid("diag-ms-x-spine", '''flowchart TB
  subgraph Spine[正逆向脊柱]
    O[订单聚合]
    P[优惠试算/分摊]
    I[库存预占/扣减]
    Pay[支付]
    OMS[履约 OMS]
    AS[售后/退款]
  end
  O -->|读试算| P
  O -->|预占意图 Outbox| I
  O -->|支付意图| Pay
  Pay -->|支付成功事件| OMS
  AS -->|退款/回补事件| I
  AS -->|分摊回退读| P
  GW[治理:限流熔断舱壁超时] -.-> O
  GW -.-> Pay
  GW -.-> AS
  OB[可观测:trace资损告警] -.-> Spine
''')}
  <table>
    <thead><tr><th>极致子章</th><th>锚点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>服务划分与数据归属</td><td><a href="#s-ms-x-boundary">#s-ms-x-boundary</a></td><td>订单/优惠/库存/履约真实边界纠纷</td></tr>
      <tr><td>同步·编排·事件</td><td><a href="#s-ms-x-orch">#s-ms-x-orch</a></td><td>超时重试风暴、幂等键、Outbox/Inbox</td></tr>
      <tr><td>治理与压测灰度</td><td><a href="#s-ms-x-govern">#s-ms-x-govern</a></td><td>舱壁超时矩阵全链路压测对交易影响</td></tr>
      <tr><td>可观测与资损告警</td><td><a href="#s-ms-x-observe">#s-ms-x-observe</a></td><td>trace 打在正逆向关键节点</td></tr>
      <tr><td>中厂裁剪 vs 大厂</td><td><a href="#s-ms-x-scale">#s-ms-x-scale</a></td><td>对照表可执行</td></tr>
      <tr><td>场景题详答</td><td><a href="#s-ms-x-drills">#s-ms-x-drills</a></td><td>故障注入/重复支付退款/下游超时</td></tr>
    </tbody>
  </table>
{koujue("极致口诀：归属先于拆分；事件写、同步读；超时是预算；幂等是门票；对账是毕业证。")}
{today("""<ul>
<li>今天下午就能做：画出订单/优惠/库存/履约/售后五张「写权威表」清单，贴到仓库 ADR。</li>
<li>把 Feign 写路径重试关掉；读路径超时改成矩阵表里的数（别全员 5s）。</li>
<li>支付回调加唯一键；OMS 消费加 Inbox；预发重放三条重复消息看是否双履约。</li>
</ul>""")}
{checklist("微服务极致最小交付", [
    "写权威表清单", "超时矩阵进配置", "Outbox+Inbox 跑通支付→OMS", "舱壁隔离慢依赖", "资损告警接支付/退款差账",
])}
{reflect("msx-hub-r1")}
</section>
"""

    boundary = f"""
<section class="block" id="s-ms-x-boundary" data-toc="S-MS-X · 服务划分与数据归属" data-prio="p0">
  <h2><span class="sys-id">S-MS-X</span>服务划分与数据归属：订单 / 优惠 / 库存 / 履约</h2>
{spine("真实边界纠纷：谁是写权威、谁只能复制只读、跨服务禁止 join。",
       serves="B-F 结算/履约 · B-R 分摊回退",
       back="S-MS 卡点A → 本页 → Outbox 章")}
{c4(
    "财务要「一笔订单能解释优惠与库存与发货」；工程要「别四个人改同一张表」。纠纷点在写权威，不在服务名。",
    "订单聚合持订单+行项目+支付意图；优惠服务持规则与试算结果快照；库存持预占/实物；OMS 持履约单。跨域只传 ID+事件。",
    "聚合根边界=事务边界；复制只读模型允许最终一致；禁止跨库 join 用宽表查询掩盖归属混乱。",
    "验收：任意单号能指出写库；对账科目能映射归属服务；无「万能订单库更新库存字段」。",
    "峰值下同步双写最易资损；热点 SKU 库存必须独立扩展。",
)}
{five(
    "每张写表只有一个服务可写；跨服务写必须走事件+幂等。",
    "主：下单写订单；支：试算/预占/支付/履约；异：超时释放；逆：退款回补。",
    "双写、跨库 join、共享 DB「先拆进程」、优惠结果不落快照。",
    "模块化单体包边界 → 按资损边界拆进程；读可 RPC，写用 Outbox。",
    "禁止他库账号；跨服务事务数监控；故障注入双写检测。",
)}
  <h3 id="msx-b-dispute">真实边界纠纷四则（公司味）</h3>
  <table>
    <thead><tr><th>纠纷</th><th>错误拆法</th><th>落地裁定</th><th>若坚持错误会坏哪步</th></tr></thead>
    <tbody>
      <tr><td>优惠要不要进订单库</td><td>订单服务直接改规则表</td><td>规则在优惠域；下单落 <code>discount_snapshot</code>+分摊行</td><td>规则热更导致历史单无法退</td></tr>
      <tr><td>库存预占谁发起</td><td>库存回调直接改订单状态</td><td>订单发预占意图；库存回执；订单状态机推进</td><td>回执乱序「无单有占」</td></tr>
      <tr><td>OMS 能否改支付态</td><td>仓配缺货直接标支付失败</td><td>OMS 只发履约失败事件；支付/售后域决定退</td><td>财务科目错乱</td></tr>
      <tr><td>售后改分摊</td><td>售后服务 UPDATE 原订单优惠行</td><td>售后持退款单+回退分摊；原单只读锁定</td><td>重复退/分摊不平衡</td></tr>
    </tbody>
  </table>
{tradeoff("边界落地形态", [
    ("模块化单体+schema 边界", "单库事务强", "扩展受单体限", "低运维", "<b>中厂默认</b>"),
    ("按资损边界拆进程+Outbox", "最终一致+对账", "高（可独立扩）", "中", "支付/库存/售后异变频率不同时"),
    ("按代码目录硬拆+共享库", "假一致", "差（分布式单体）", "高事故", "<b>禁止</b>"),
])}
{pit("「先拆服务再理归属」=把扯皮分布式化。正确顺序：上下文图→写模型表→禁止跨服务 join→再谈进程。")}
{qa("【场景题】优惠团队说「分摊算法常变要独立服务」，订单团队说「下单必须同事务算完」。怎么裁？",
    ["C1：怕试算慢拖垮下单，也怕历史退款对不上规则。C2：同步 RPC 试算（短超时）+ 落快照进订单事务；规则热更不影响已落单。C3：试算可最终一致到缓存，落单快照是退款真理。C4：部分退按快照分摊回退，规则版本进审计。",
     "大促前规则周更。", "订单库直接存可变规则脚本。", "超时矩阵：试算≤80ms；失败降级「无券下单」开关。", "「可变规则外置，可变结果快照内聚。」"],
    "msx-b-q1")}
{qa("【场景题】库存服务要查订单「是否已支付」再扣减，是否允许同步调订单？",
    ["读可同步（只读 API/只读副本）；写禁止互相调。更好：只消费支付成功事件再「确认扣减」，预占阶段用意图 ID。",
     "支付成功到扣减窗口。", "库存持有订单写连接。", "Inbox 去重支付事件；预占→确认→释放状态机。", "「库存不读订单写库，只信事件与意图。」"],
    "msx-b-q2")}
{reflect("msx-b-r1")}
</section>
"""

    orch = f"""
<section class="block" id="s-ms-x-orch" data-toc="S-MS-X · 同步编排与事件" data-prio="p0">
  <h2><span class="sys-id">S-MS-X</span>同步调用 vs 编排 vs 编排+事件</h2>
{spine("超时重试风暴、幂等键设计、Outbox/Inbox——正逆向写路径核心。",
       serves="支付成功→OMS；售后退款→回补库存/优惠",
       back="S-MS 卡点B → 本页 → T-一致性")}
{c4(
    "客人付了钱必须进履约；退了款库存/券必须回得干净。怕的是「有的成功有的没有」且说不清。",
    "读多短超时同步；跨服务写默认 Outbox→MQ→Inbox 幂等；长流程用编排状态机+补偿表；禁止默认 XA。",
    "至少一次投递+业务幂等≈恰好一次；本地事务把业务行与 outbox 行同命运；Inbox 唯一键挡住重放。",
    "日终：支付成功数≈OMS 创建数；退款成功数≈库存回补数；差异工单有主。",
    "回调洪峰与大促重试是风暴源；舱壁+退避+熔断必须同时在。",
)}
{mermaid("diag-ms-x-orch", '''sequenceDiagram
  participant Ord as 订单
  participant DB as 订单库
  participant OB as Outbox轮询
  participant MQ as MQ
  participant OMS as OMS
  participant IB as Inbox
  Ord->>DB: 本地事务写订单+outbox
  OB->>DB: 拉取未发送
  OB->>MQ: 投递 payment_paid
  MQ->>OMS: 至少一次
  OMS->>IB: 幂等键去重
  alt 首次
    OMS->>OMS: 创建履约单
  else 重复
    OMS-->>MQ: ACK 忽略
  end
''')}
  <h3 id="msx-o-compare">三种形态对照（挂交易）</h3>
  <table>
    <thead><tr><th>形态</th><th>典型用法</th><th>爆炸点</th><th>必备配套</th></tr></thead>
    <tbody>
      <tr><td>同步 RPC 链</td><td>下单页试算、风控短判定</td><td>超时层层放大、线程占满</td><td>超时预算、舱壁、只读/可降级</td></tr>
      <tr><td>同步编排（编排服务调多方）</td><td>开户类短流程、中厂「下单门面」</td><td>编排中心变上帝、难扩</td><td>严格超时、补偿表、勿堆长事务</td></tr>
      <tr><td>编排+事件（状态机+Outbox）</td><td>支付→OMS→WMS、售后回补</td><td>消息堆积、乱序、重复</td><td>幂等键、Inbox、对账、延迟队列</td></tr>
    </tbody>
  </table>
  <h3 id="msx-o-idem">幂等键设计清单（写死）</h3>
  <table>
    <thead><tr><th>场景</th><th>幂等键</th><th>存储</th><th>重复语义</th></tr></thead>
    <tbody>
      <tr><td>支付回调</td><td><code>channel + trade_no</code></td><td>唯一索引</td><td>返回首次成功结果</td></tr>
      <tr><td>OMS 创建</td><td><code>order_id + paid_event_id</code></td><td>Inbox</td><td>忽略</td></tr>
      <tr><td>库存确认扣减</td><td><code>reserve_id</code> 或 <code>order_line_id</code></td><td>状态机</td><td>已确认则成功幂等</td></tr>
      <tr><td>退款申请</td><td><code>after_sale_id + refund_attempt</code></td><td>退款单唯一</td><td>禁止第二笔并行</td></tr>
      <tr><td>券回补</td><td><code>refund_id + coupon_id</code></td><td>Inbox</td><td>忽略</td></tr>
    </tbody>
  </table>
{failbox("超时重试风暴",
         "网关 3s、服务 3s、下游 3s，全部自动重试 3 次：一次故障变 27 倍压力。支付非幂等 POST 被重试→重复扣款风险。止血：写路径默认重试=0；仅标幂等接口可重试；指数退避+抖动；熔断后停；客户端与服务端重试职责唯一。")}
{runbook("Outbox 堆积 10 分钟",
         """<ol>
      <li>看堆积量/最老消息年龄；是否发布或 DB 慢。</li>
      <li>区分「发送失败」与「下游处理慢」：MQ lag vs Inbox 冲突。</li>
      <li>扩消费者前先查下游饱和与慢 SQL。</li>
      <li>毒消息进死信+告警，禁止无限重试打爆。</li>
      <li>对账任务核对支付≈OMS；差异建单。</li>
    </ol>""")}
{tradeoff("支付成功通知 OMS", [
    ("本地消息表 Outbox", "最终一致可证", "秒级", "低", "<b>默认</b>"),
    ("RocketMQ 事务消息", "最终一致", "高", "中（依赖 MQ）", "已有可靠 MQ 平台"),
    ("同步 Feign 创建 OMS", "看似强、实则脆", "差（占线程）", "低短线高长线", "仅内网演示，生产慎"),
    ("Seata AT 两库", "强一致幻觉", "锁成本高", "高运维", "无平台组禁止"),
])}
{qa("【场景题】下游 OMS 超时，订单侧已提交本地事务，用户刷新看到「支付成功未发货」？",
    ["正常窗口：Outbox 重试投递；页面展示「履约处理中」；超时 SLA 后进对账与客服工具。禁止再调一次「同步创建」造成双履约。",
     "大促回调洪峰。", "前端轮询直接插 OMS。", "Inbox 幂等+状态机；告警 outbox age。", "「本地已提交就信 Outbox，不信用户手抖。」"],
    "msx-o-q1")}
{qa("【场景题】如何设计退款的 Inbox，防止「库存回补两次」？",
    ["消费者以 refund_id 为幂等键；库存状态 PRE→REFUNDED 单向；重复消息 ACK；监控「幂等命中率」区分正常重投与 bug。",
     "渠道重复回调。", "用随机 UUID 当业务键。", "唯一索引+状态机守卫。", "「回补次数由状态机决定，不由消息次数决定。」"],
    "msx-o-q2")}
{reflect("msx-o-r1")}
</section>
"""

    govern = f"""
<section class="block" id="s-ms-x-govern" data-toc="S-MS-X · 治理压测灰度" data-prio="p0">
  <h2><span class="sys-id">S-MS-X</span>治理：限流熔断舱壁 · 超时矩阵 · 全链路压测 · 灰度回滚</h2>
{spine("治理不是中间件展览，是交易峰值下的爆炸半径控制。",
       serves="大促下单/支付回调/售后退款洪峰",
       back="S-MS 卡点C → 本页 → T-K8s 发布")}
{c4(
    "峰值时宁可少卖，不能把支付/退款打成糊涂账；灰度坏版本必须秒级止血。",
    "入口限流+热点限流；下游熔断半开；线程池按依赖舱壁；超时矩阵入库；全链路压测用真实比例；金丝雀看支付/退款三针。",
    "舱壁阻止慢依赖抽干公共线程；熔断牺牲局部保整体；压测暴露协调问题而非单机 QPS。",
    "演练记录：开关、回滚、熔断阈值、压测瓶颈复盘进 ADR。",
    "秒杀是否与 HPA 联动见 K8s 极致章；治理侧先保证不雪崩。",
)}
  <h3 id="msx-g-timeout">超时矩阵（示例·交易链）</h3>
  <table>
    <thead><tr><th>跳</th><th>预算</th><th>重试</th><th>失败策略</th></tr></thead>
    <tbody>
      <tr><td>网关→交易</td><td>2.0s</td><td>0</td><td>快速失败+提示</td></tr>
      <tr><td>交易→优惠试算</td><td>80–120ms</td><td>0</td><td>降级无券/缓存价</td></tr>
      <tr><td>交易→风控</td><td>100–150ms</td><td>0</td><td>高风险拒；超时走人工队列（可配）</td></tr>
      <tr><td>交易→库存预占</td><td>200ms</td><td>幂等可 1 次</td><td>失败不建单</td></tr>
      <tr><td>支付回调处理</td><td>1.0s 内落库</td><td>渠道侧</td><td>本地幂等；异步 OMS</td></tr>
      <tr><td>售后→退款渠道</td><td>3–5s</td><td>仅幂等查询</td><td>挂起+对账，禁盲重放退款</td></tr>
    </tbody>
  </table>
  <h3 id="msx-g-gray">灰度 / 回滚对交易的影响</h3>
  <table>
    <thead><tr><th>变更类型</th><th>灰度策略</th><th>回滚风险</th><th>额外闸门</th></tr></thead>
    <tbody>
      <tr><td>兼容 bugfix</td><td>滚动+就绪探针</td><td>低</td><td>支付成功率</td></tr>
      <tr><td>优惠口径/分摊</td><td>金丝雀 1%→5%→全量</td><td>中（新旧单混）</td><td>分摊不平衡告警；规则版本钉扎</td></tr>
      <tr><td>退款状态机</td><td>金丝雀+双写影子校验</td><td>高</td><td>禁止自动全量；退款成功率+人工抽检</td></tr>
      <tr><td>DB schema 不兼容</td><td>expand/contract</td><td>极高</td><td>禁止蓝绿靠感觉；先扩列</td></tr>
    </tbody>
  </table>
{failbox("半开误伤",
         "熔断半开放一探针请求打到仍慢的依赖→再次打开，但若探针选在支付主路径，会间歇性资损体验。半开流量走影子或只读探测；写路径半开要人工确认。")}
{runbook("全链路压测（交易）",
         """<ol>
      <li>模型：浏览:下单:支付:售后 = 接近大促比例；含回调与 Outbox。</li>
      <li>数据：热点 SKU、真实分片键、影子库或染色流量。</li>
      <li>观察：线程池拒绝、DB 锁等待、MQ lag、熔断、缓存命中。</li>
      <li>验收：目标 QPS 下支付成功率、P99、错误预算；写出瓶颈 ADR。</li>
      <li>禁止：只压单接口、用均匀随机打爆连接池却得「胜利」。 </li>
    </ol>""")}
{qa("【场景题】库存 RT 变 2s，未熔断，下单全站超时。根因与止血？",
    ["公共线程池被同步库存调用占满（无舱壁）。止血：隔离库存线程池+快速失败+熔断；入口限流；预占改异步仅当产品接受延迟。",
     "大促库存热点。", "全局限流却不隔离开。", "舱壁池参数表+超时矩阵演练。", "「慢依赖必须住单间。」"],
    "msx-g-q1")}
{qa("【场景题】灰度 5% 新退款逻辑，资损告警响了，能否「再观察 10 分钟」？",
    ["资损类禁止观察赌运气：立即缩金丝雀到 0 或 revision 回滚；冻结相关售后单人工复核；保留 trace 与规则版本。",
     "退款口径变更。", "用平均成功率安慰。", "发布检查单写死资损即回滚。", "「资损告警=火灾铃，不是天气预报。」"],
    "msx-g-q2")}
{reflect("msx-g-r1")}
</section>
"""

    observe = f"""
<section class="block" id="s-ms-x-observe" data-toc="S-MS-X · 可观测资损告警" data-prio="p0">
  <h2><span class="sys-id">S-MS-X</span>可观测：正逆向关键节点 Trace · 资损告警</h2>
{spine("看不见的链路等于不可值班；资损告警必须挂业务语义。",
       serves="支付/OMS/退款/分摊回退",
       back="T-可观测 → 本页 → 交叉大促演练")}
{c4(
    "出事故时要在 5 分钟内回答：这单卡在哪、钱有没有多退、库存有没有双回补。",
    "traceId 从网关贯到 Outbox/消费者；关键 span 打业务单号；指标三针+资损专用告警；日志结构化禁密钥。",
    "分布式追踪回答因果；指标回答趋势；对账回答钱；三者缺一不可复盘。",
    "验收：任意投诉单号 1 分钟拉齐调用链与状态机轨迹；资损告警有演练记录。",
    "峰值下采样策略不能抽掉支付失败样本。",
)}
  <h3 id="msx-obs-nodes">正逆向关键节点埋点清单</h3>
  <table>
    <thead><tr><th>节点</th><th>Span/日志必带</th><th>资损相关指标</th></tr></thead>
    <tbody>
      <tr><td>优惠落快照</td><td>orderId, ruleVersion, amount</td><td>快照失败率</td></tr>
      <tr><td>库存预占/确认/释放</td><td>reserveId, skuId, qty</td><td>超卖、重复确认</td></tr>
      <tr><td>支付回调</td><td>tradeNo, payId, result</td><td>幂等冲突、重复支付嫌疑</td></tr>
      <tr><td>Outbox 发送</td><td>eventId, age</td><td>堆积年龄</td></tr>
      <tr><td>OMS 创建</td><td>orderId, inboxHit</td><td>支付≈OMS 差</td></tr>
      <tr><td>售后退款</td><td>afterSaleId, refundId, channelResp</td><td>重复退、退款失败挂起</td></tr>
      <tr><td>分摊回退</td><td>allocationId, delta</td><td>分摊不平衡金额</td></tr>
    </tbody>
  </table>
  <h3 id="msx-obs-alert">资损告警（写死阈值思路）</h3>
  <ul>
    <li><b>重复支付嫌疑：</b>同 order 多笔成功支付且无解释关闭单 → P0。</li>
    <li><b>重复退款嫌疑：</b>同 after_sale 多笔渠道成功 → P0 立即熔断自动退。</li>
    <li><b>分摊不平衡：</b>行分摊合计与头不一致超阈值 → P0/P1。</li>
    <li><b>支付成功无 OMS：</b>超过 SLA（如 3min）→ P1 升 P0。</li>
    <li><b>Outbox 年龄：</b>最老 &gt; 阈值 → P1。</li>
  </ul>
{ban("<ul><li>只告警 CPU/内存不告警业务差账</li><li>支付失败样本被采样丢光</li><li>日志打印完整卡号/密钥</li><li>用「平均支付成功率」掩盖分区故障</li></ul>")}
{qa("【场景题】客诉「钱扣了没单」，你如何用观测体系定位？",
    ["用 tradeNo/orderId 查支付回调 span→本地订单态→Outbox 是否发送→OMS Inbox；区分「回调未到」「本地失败」「Outbox 积」「OMS 拒」。",
     "晚高峰。", "只重启 Pod。", "单号检索 Runbook+对账补单工具。", "「先串链，再动手。」"],
    "msx-obs-q1")}
{reflect("msx-obs-r1")}
</section>
"""

    scale = f"""
<section class="block" id="s-ms-x-scale" data-toc="S-MS-X · 中厂vs大厂对照" data-prio="p0">
  <h2><span class="sys-id">S-MS-X</span>中厂裁剪 vs 大厂标配对照表</h2>
{spine("同一正逆向闭环，配置不同；禁止照搬平台。", serves="V1 配置层加厚", back="V1 → 本页 → S-Year")}
  <table>
    <thead><tr><th>能力</th><th>大厂标配（公开常见）</th><th>中厂裁剪（可交付）</th><th>不可再砍</th></tr></thead>
    <tbody>
      <tr><td>服务拆分</td><td>细域+中台+平台组</td><td>模块化单体或 4–6 进程</td><td>写归属清晰</td></tr>
      <tr><td>注册配置</td><td>自研/统一配置中心</td><td>Nacos/K8s Config</td><td>变更审计</td></tr>
      <tr><td>限流熔断</td><td>统一治理平台</td><td>网关+Sentinel/Resilience4j</td><td>超时矩阵+舱壁</td></tr>
      <tr><td>可靠消息</td><td>事务消息平台</td><td>Outbox 表+RocketMQ/Kafka</td><td>幂等+对账</td></tr>
      <tr><td>全链路压测</td><td>染色流量平台</td><td>季度压测+影子库</td><td>大促前至少 1 次</td></tr>
      <tr><td>灰度</td><td>统一发布平台</td><td>K8s 金丝雀+开关</td><td>资损即回滚</td></tr>
      <tr><td>追踪</td><td>自研 APM</td><td>SkyWalking/OTel</td><td>单号可检索</td></tr>
      <tr><td>服务网格</td><td>部分业务渐进</td><td><b>默认不上</b></td><td>见 K8s-Mesh 章</td></tr>
    </tbody>
  </table>
{plain("人话：大厂买的是平台与编制；中厂买的是纪律。纪律四件套：归属、幂等、超时舱壁、对账。")}
{qa("【场景题】老板要「对齐大厂微服务」，一周内上 20 个服务怎么拒？",
    ["用 ADR：收益/成本/回滚/数据归属；展示分布式单体风险；给模块化+Outbox 路径与里程碑。",
     "转型 KPI。", "硬拆共享库。", "先 S-MS-X 边界表签字。", "「对齐的是闭环能力，不是服务个数。」"],
    "msx-s-q1")}
{reflect("msx-s-r1")}
</section>
"""

    drills = f"""
<section class="block" id="s-ms-x-drills" data-toc="S-MS-X · 场景题详答" data-prio="p0">
  <h2><span class="sys-id">S-MS-X</span>场景题详答：故障注入 · 重复支付 · 重复退款 · 下游超时</h2>
{spine("把极致章收束为可练手详答；挂四段+五步。", back="本极致章 → B-X / S-Year")}
{koujue("答题骨架：C1 怕什么 → C2 怎么做 → C3 为何稳 → C4 账过了没；再补钉拆标选验一句。")}

{qa("【故障注入】在预发对库存服务注入 2s 延迟+10% 错误，期望看到什么？怎样算演练通过？",
    ["期望：库存舱壁打满但不拖死支付；熔断打开；入口限流生效；Outbox 不爆炸；错误预算可控。通过标准：支付成功率≥SLO；无跨域双写；回滚/关开关演练成功；复盘更新超时矩阵。",
     "大促前演练。", "注入后只看 CPU。", "剧本入库+签字。", "「演练通过=爆炸半径符合设计。」"],
    "msx-d-q1")}

{qa("【重复支付】用户连点+渠道重复回调，如何保证只成功一笔？",
    ["前端防抖不依赖；服务端 pay_request 幂等键；回调 channel+trade_no 唯一；状态机 CREATED→PAID 单向；第二笔成功支付进「溢收款」人工/自动退，禁止静默忽略资金。",
     "弱网。", "只靠 UI disable。", "对账任务扫多支付。", "「幂等防重复意，对账防重复钱。」"],
    "msx-d-q2")}

{qa("【重复退款】售后渠道超时，本地不知结果，值班重推退款按钮？",
    ["先查单（幂等查询）再决定；退款 attempt 带幂等键；渠道成功则本地对齐；禁止「再发一笔新退款」。状态机锁定退款中。",
     "客诉催退。", "盲重放。", "工具只暴露「查询对齐」「对账补推」。", "「退款重推=查询对齐，不是再打一枪。」"],
    "msx-d-q3")}

{qa("【下游超时】优惠试算超时，要不要重试 3 次？",
    ["读路径可谨慎重试 1 次（幂等、短超时、有预算）；写路径与下单主事务内忌多重试。更好：本地缓存价/降级无券，保证下单通路。",
     "大促试算打满。", "与写接口同一重试策略。", "降级开关演练。", "「读可闪断降级，写不靠重试救命。」"],
    "msx-d-q4")}

{qa("【编排选择题】寄修+换新并行（见 B-X），同步编排还是事件？",
    ["库存预占与售后状态用事件+状态机；同步仅用于短查询。并行分支用关联 ID，禁双向同步写。",
     "售后洪峰。", "一个编排服务同步锁两库。", "挂回 bx-repair-exchange。", "「并行分支事件化，终态对账化。」"],
    "msx-d-q5")}

{qa("【30秒】口述「我们交易域微服务怎么落地」",
    ["按资损边界拆；写 Outbox 读可 RPC；超时舱壁矩阵；金丝雀看支付退款；对账毕业。中厂可模块化单体但纪律不少。",
     "面试。", "背组件清单。", "准备一张失败传播图。", "「讲纪律与验收，不讲购物车。」"],
    "msx-d-q6")}

{reflect("msx-d-r1")}
</section>
"""
    return hub + boundary + orch + govern + observe + scale + drills
