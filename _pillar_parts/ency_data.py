# -*- coding: utf-8 -*-
"""数据与中间件百科：MySQL/Redis/MQ/ES/分库分表 + PolarDB/Gauss/达梦/TDSQL"""
from ency_factory import sec, deep
from helpers import plain, qa, koujue, reflect, mermaid, tradeoff, today, floor, c4, spine


def build() -> str:
    parts = []
    parts.append(sec(
        "ency-d", "ENCY-D · 数据中间件总图", "ENCY-D", "数据与中间件百科总图",
        deep(
            plain_txt="人话：交易账本在哪安家——单机 MySQL、共享存储云库、分布式库、还是分库分表中间件——先问一致性与运维成本。",
            biz="订单/支付/售后数据不丢不错，查询可扩展。",
            impl="OLTP 选型 + 缓存 + MQ + 搜索；分布式库单独深挖。",
            principle="共享存储 vs 分片共享无所；CAP/PACELC 权衡。",
            substance="RPO/RTO、主从延迟、分布式事务边界。",
            mermaid_id="diag-ency-d-map",
            mermaid_code="""flowchart TB
  App[交易应用] --> OLTP[OLTP库]
  App --> Redis[Redis]
  App --> MQ[Kafka/RMQ/Rocket]
  App --> ES[ES搜索]
  OLTP --> MySQL[MySQL/InnoDB]
  OLTP --> Cloud[PolarDB]
  OLTP --> Dist[TDSQL/OceanBase/TiDB]
  OLTP --> Local[Gauss/达梦]
""",
            today_html="<ul><li>先定：强一致账务 vs 可搜索查询分离。</li><li>分布式库与分库分表不是一回事——见下节对照。</li></ul>",
            reflect_id="ency-d-hub-r1",
            koujue_txt="数据口诀：账本强一致，搜索可最终，缓存不当事务。",
            spine_pos="数据层托住正逆向账本与查询。",
            serves="订单/支付/售后",
            back="T3/T4/T5/T9 → 本百科",
        ),
    ))

    # Distributed DB hub + each vendor
    parts.append(sec(
        "ency-d-dist", "ENCY-D · 分布式数据库总览", "ENCY-D-DIST",
        "分布式数据库：PolarDB / GaussDB / 达梦 / TDSQL（及对照）",
        spine("选型挂交易：支付库要强一致低延迟；分析可旁路。", serves="订单账本/报备库", back="T4 → 本总览 → 各库专节")
        + plain("人话：别被「分布式」三字唬住——先分清：<b>共享存储一写多读</b>（类 PolarDB）、<b>分片中间件/分布式库</b>（类 TDSQL/OceanBase/TiDB）、<b>本地化信创库</b>（达梦/Gauss 常见部署形态）。")
        + c4(
            "账本不丢、切换可预期、合规可落地。",
            "按架构族选型：共享存储 / 分片 / 集中式信创；配套备份与演练。",
            "见对照表与各节掀底板：计算存储分离、分片键、一致性协议。",
            "RPO≈0 或可接受；订单事务成功率；运维人力可承受。",
            "大促写放大与跨分片事务是分水岭。",
        )
        + """  <h4>架构族对照（先看这张再进专节）</h4>
  <table>
    <thead><tr><th>产品</th><th>架构族</th><th>分片/存储</th><th>一致性要点</th><th>交易场景适合度</th><th>运维画像</th></tr></thead>
    <tbody>
      <tr><td><b>MySQL</b></td><td>单机/主从</td><td>无原生分片</td><td>InnoDB 事务</td><td>中小；分表到顶</td><td>成熟生态</td></tr>
      <tr><td><b>Oracle</b></td><td>集中式/RAC</td><td>共享存储 RAC</td><td>强；贵</td><td>传统核心</td><td>重专才</td></tr>
      <tr><td><b>PolarDB</b></td><td>共享存储一写多读</td><td>计算存储分离</td><td>事务在主；RO 物理复制</td><td>兼容 MySQL/PG 的云上升级</td><td>云托管为主</td></tr>
      <tr><td><b>GaussDB</b></td><td>集中/分布式形态</td><td>可分布式部署</td><td>强一致取向</td><td>政务/金融信创常见</td><td>厂商+自研规范</td></tr>
      <tr><td><b>达梦 DM</b></td><td>集中式为主</td><td>集群/数据守护</td><td>强一致</td><td>信创替换 Oracle 路径</td><td>国产工具链</td></tr>
      <tr><td><b>TDSQL</b></td><td>分片分布式</td><td>水平拆分</td><td>分布式事务/约束</td><td>高并发交易拆分</td><td>分片键治理重</td></tr>
      <tr><td><b>TiDB</b></td><td>计算存储分离+Region</td><td>自动调度</td><td>Percolator/Raft</td><td>HTAP 倾向；注意延迟</td><td>生态云原生</td></tr>
      <tr><td><b>OceanBase</b></td><td>共享无所多副本</td><td>分区+日志复制</td><td>Paxos 多数派</td><td>金融级交易常见</td><td>专用运维</td></tr>
    </tbody>
  </table>
"""
        + mermaid("diag-ency-d-dist-arch", """flowchart TB
  subgraph Shared[共享存储族]
    P[PolarDB Primary] --> Stor[(共享存储)]
    RO[Read Only] --> Stor
  end
  subgraph Shard[分片族]
    Proxy[代理/计算层] --> DN1[(DN1)]
    Proxy --> DN2[(DN2)]
  end
  subgraph Local[信创集中族]
    DM[达梦/Gauss主备] --> Sync[日志复制]
  end
""")
        + tradeoff("订单库怎么选（边界）", [
            ("MySQL 单库+读写分离", "强(单分片)", "垂直顶", "低", "中厂起步"),
            ("PolarDB MySQL 兼容", "强(主)", "RO 扩展读", "中(云)", "读多写单上升"),
            ("分库分表中间件", "跨库难", "高", "中", "分片键清晰时"),
            ("TDSQL/OB 分布式", "看产品能力", "高", "高", "金融级拆分"),
            ("TiDB HTAP", "强", "写延迟要测", "中高", "分析混合慎直接替支付"),
        ])
        + today("""<ul>
<li>支付/退款库：优先「单分片可解释事务」；跨分片事务当例外。</li>
<li>选型五问：兼容性、RPO/RTO、跨分片、运维编制、退出成本。</li>
<li>专节：<a href="#ency-d-polardb">PolarDB</a> · <a href="#ency-d-gauss">GaussDB</a> · <a href="#ency-d-dm">达梦</a> · <a href="#ency-d-tdsql">TDSQL</a></li>
</ul>""")
        + qa("【选型】订单库从 MySQL 上云，读被报表打爆，优先 PolarDB 还是直接上 TiDB？",
            ["报表打爆读→PolarDB RO 或只读实例常更平滑；TiDB 要评估写延迟与 SQL 兼容、运维模型。先读写分离/PolarDB，分析走旁路数仓。",
             "容量。", "为了分布式而上分布式。", "读扩展优先。", "「先治读，再谈分布式。」"],
            "ency-d-dist-q1")
        + qa("【本质】共享存储与分片共享无所差在哪？",
            ["共享存储：一份数据多计算节点，写通常单主；分片：数据切开，扩展写，但跨片事务与治理复杂。",
             "架构评审。", "混为一谈。", "画两张图。", "「一份盘 vs 多份片。」"],
            "ency-d-dist-q2")
        + koujue("分布式库口诀：先定架构族，再谈品牌名。")
        + reflect("ency-d-dist-r1"),
    ))

    dist_topics = [
        ("ency-d-polardb", "ENCY-D · PolarDB", "ENCY-D-POLARDB", "PolarDB：共享存储 · 一写多读 · 兼容", {
            "plain_txt": "比喻：一块高级共享硬盘插多个计算头——一个主刀写，多个只读头帮报表/查询分担。",
            "biz": "MySQL/PG 兼容路径上升级；读扩展缓解订单查询压力。",
            "impl": "主库写订单；RO 扛列表/后台；注意复制延迟读己之写。",
            "principle": "计算存储分离；RO 物理复制；事务在 Primary。",
            "substance": "写延迟、RO 延迟、故障切换 RTO。",
            "floor_title": "共享存储与 RO",
            "structure": "Primary 写 redo/页面到共享存储；RO 拉日志回放；会话落在计算节点。",
            "source_path": "认知：缓冲池在计算节点；存储多副本由云保障；切换提升 RO/备。",
            "online": "支付后立刻读 RO 看不到已支付——读写分离延迟。",
            "verify": "RO lag；切换演练；只写主。",
            "mermaid_id": "diag-ency-d-polar",
            "mermaid_code": """flowchart LR
  AppW[写:下单支付] --> Primary
  AppR[读:列表报表] --> RO1
  AppR --> RO2
  Primary --> Stor[(共享存储多副本)]
  RO1 --> Stor
  RO2 --> Stor
""",
            "today_html": "<ul><li>支付后读己之写走主库。</li><li>大事务/长 DDL 评估存储与复制。</li></ul>",
            "qas": [("【延迟】用户支付成功刷新仍待支付？", ["打到 RO 延迟；强制主读或会话粘滞。", "支付。", "怪前端。", "读写路由。", "「付后读主。」"], "ency-d-polar-q1")],
            "reflect_id": "ency-d-polar-r1",
            "koujue_txt": "PolarDB 口诀：写主读 RO，付后读主。",
        }),
        ("ency-d-gauss", "ENCY-D · GaussDB", "ENCY-D-GAUSS", "GaussDB（高斯）：形态 · 一致性 · 信创落地", {
            "plain_txt": "人话：GaussDB 常见于政企/金融信创清单——形态可能是集中式或分布式，落地前先钉「你们买的是哪套拓扑」。",
            "biz": "合规替换 + 交易稳定性；SQL/工具链迁移成本可控。",
            "impl": "兼容评估（语法/函数/隔离级别）；备份恢复演练；监控对接。",
            "principle": "分布式形态下的分片与强一致复制；集中式则主备切换。",
            "substance": "迁移回归用例绿；RTO 达标；关键交易 RT。",
            "floor_title": "选型与迁移底板",
            "structure": "先确认：节点角色、副本、分片键（若有）、事务模型文档。",
            "source_path": "迁移：结构→数据→流量双跑→切换；差异 SQL 清单。",
            "online": "隐式类型转换/函数差异导致分摊金额错；或分布式跨片事务超时。",
            "verify": "兼容性套件；压测支付回调；切换演练。",
            "mermaid_id": "diag-ency-d-gauss",
            "mermaid_code": """flowchart TD
  Assess[兼容评估] --> Pilot[双跑]
  Pilot --> Cut[切换]
  Cut --> Drill[主备/分片故障演练]
""",
            "today_html": "<ul><li>订单核心 SQL 建立兼容白名单测试。</li><li>禁止假设「MySQL 方言 100% 可用」。</li></ul>",
            "qas": [("【迁移】最大风险是什么？", ["方言/隔离/运维工具差异导致静默错账。", "信创。", "只迁数据不测 SQL。", "用例库。", "「先锁兼容套件。」"], "ency-d-gauss-q1")],
            "reflect_id": "ency-d-gauss-r1",
            "koujue_txt": "Gauss 口诀：先认拓扑，再迁流量，用例锁命。",
        }),
        ("ency-d-dm", "ENCY-D · 达梦", "ENCY-D-DM", "达梦（Dameng）：信创替换与运维要点", {
            "plain_txt": "比喻：达梦常被当作「Oracle 岗位的国产方向盘」——语法习惯近，但工具链与生态细节要重新拿本本。",
            "biz": "信创合规下的交易/报备库可运行、可备份、可审计。",
            "impl": "对象/权限/备份策略重建；驱动与连接池验证；监控指标对接。",
            "principle": "集中式事务引擎+数据守护/集群；别按 MySQL 运维惯性照搬。",
            "substance": "备份可恢复；权限最小化；关键作业 RT。",
            "floor_title": "替换 Oracle 的工程路径",
            "structure": "评估语法→改应用层方言→数据迁移→演练切换。",
            "source_path": "应用：JDBC URL/方言；ORM 兼容；批量写入策略。",
            "online": "序列/分页/空字符串语义差异导致售后查询错页。",
            "verify": "对账作业；分页用例；备份恢复演练。",
            "mermaid_id": "diag-ency-d-dm",
            "mermaid_code": """flowchart LR
  Ora[(Oracle)] --> Eval[差异清单]
  Eval --> App[改应用/SQL]
  App --> DM[(达梦)]
  DM --> Bak[备份恢复演练]
""",
            "today_html": "<ul><li>建立「Oracle→DM」差异表进仓库。</li><li>连接池与超时按 DM 文档重测。</li></ul>",
            "qas": [("【运维】没有云 RDS 控制台怎么保障 RPO？", ["标准备份+日志+定期恢复演练+告警。", "信创机房。", "只靠盘阵。", "演练。", "「备份不演练=没备份。」"], "ency-d-dm-q1")],
            "reflect_id": "ency-d-dm-r1",
            "koujue_txt": "达梦口诀：差异表进仓，备份必演练。",
        }),
        ("ency-d-tdsql", "ENCY-D · TDSQL", "ENCY-D-TDSQL", "TDSQL：分片 · 分布式事务 · 治理", {
            "plain_txt": "人话：TDSQL 一类把数据切开——你选的分片键决定后半生幸福程度；跨片事务是税率一样的东西：能少则少。",
            "biz": "高并发订单水平扩展；跨片尽量避免。",
            "impl": "分片键选 user_id/order_id 策略；全局二级索引评估；分布式事务慎用。",
            "principle": "分片路由；两阶段/优化事务；广播 SQL 危害。",
            "substance": "跨片比例、慢查询、扩容迁移窗口。",
            "hc": "热点分片（网红商户）。",
            "floor_title": "分片键与跨片",
            "structure": "代理层解析 SQL→路由 DN；跨片 join/事务走额外协议。",
            "source_path": "订单号带分片暗示或雪花；禁止无键全表扫。",
            "online": "按非分片键查订单导致扇出；跨片退款超时。",
            "verify": "跨片 SQL 审计；热点分片监控。",
            "mermaid_id": "diag-ency-d-tdsql",
            "mermaid_code": """flowchart TD
  SQL[SQL] --> Proxy[TDSQL代理]
  Proxy --> R{分片键?}
  R -->|有| One[单DN事务]
  R -->|无/跨| Many[扇出/分布式事务]
  Many --> Risk[延迟与失败率上升]
""",
            "trade_title": "分片键候选",
            "trade_rows": [
                ("user_id", "用户维清晰", "用户维倾斜", "中", "C 端常见"),
                ("order_id", "订单点查快", "用户订单列表可能跨片", "中", "需全局索引/宽表"),
                ("店铺_id", "B 端友好", "爆店热点", "中", "需再拆"),
            ],
            "today_html": "<ul><li>售后查询路径与分片键对齐设计。</li><li>禁止管理端无键大扫抽数——走数仓。</li></ul>",
            "qas": [("【热点】单商户写爆一分片？", ["二级拆分/隔离库/限流；或键加盐。", "大促。", "盲目加 DN。", "热点治理。", "「先治倾斜。」"], "ency-d-tdsql-q1")],
            "reflect_id": "ency-d-tdsql-r1",
            "koujue_txt": "TDSQL 口诀：分片键定终身，跨片当事故。",
        }),
    ]
    for sid, toc, sys_id, title, kw in dist_topics:
        kw.setdefault("spine_pos", "分布式/信创库挂订单账本选型。")
        kw.setdefault("serves", "支付/订单 OLTP")
        kw.setdefault("back", "ENCY-D-DIST → 本叶 → 演练")
        parts.append(sec(sid, toc, sys_id, title, deep(**kw)))

    # MySQL Redis MQ ES sharding
    other = [
        ("ency-d-mysql", "ENCY-D · MySQL加深", "ENCY-D-MYSQL", "MySQL/InnoDB 百科加深", {
            "plain_txt": "交叉 <a href='#t-found-mysql'>T-Found-MySQL</a>：补隔离级别场景与红蓝对抗式排查。",
            "biz": "订单行锁可解释；幻读不导致超发。",
            "impl": "唯一键幂等；短事务；索引设计。",
            "principle": "MVCC+锁；undo/redo；间隙锁。",
            "substance": "死锁率、慢查。",
            "mermaid_id": "diag-ency-d-mysql",
            "mermaid_code": """flowchart TD
  Tx[事务] --> ReadView[ReadView]
  Tx --> Locks[行/间隙锁]
  Tx --> Redo[redo]
  Tx --> Undo[undo]
""",
            "today_html": "<ul><li>退款 FOR UPDATE 走唯一键。</li></ul>",
            "qas": [("【隔离】RR 下间隙锁何时爆？", ["范围条件更新/非唯一索引。", "售后。", "怪高并发。", "收紧条件。", "「范围即间隙。」"], "ency-d-mysql-q1")],
            "reflect_id": "ency-d-mysql-r1",
            "koujue_txt": "MySQL 口诀：唯一键幂等，范围慎锁。",
            "floor_title": "锁与隔离",
            "structure": "RC/RR；当前读加锁；快照读 MVCC。",
            "source_path": "handler 加锁；死锁回滚成本低者。",
            "online": "状态扫描锁扩大。",
            "verify": "data_locks；死锁日志。",
        }),
        ("ency-d-redis", "ENCY-D · Redis加深", "ENCY-D-REDIS", "Redis 百科加深", {
            "plain_txt": "交叉 T-Found-Redis：补集群槽与内存淘汰对订单预占影响。",
            "biz": "预占准确；热 Key 不打穿。",
            "impl": "Lua/DECR；拆热 Key；禁当账本。",
            "principle": "单线程命令；过期；AOF/RDB；槽迁移。",
            "substance": "超卖=0；内存水位。",
            "mermaid_id": "diag-ency-d-redis",
            "mermaid_code": """flowchart TD
  Cmd[命令] --> AE[事件循环]
  AE --> Exp[过期]
  AE --> Mem[淘汰策略]
""",
            "today_html": "<ul><li>预占 TTL+补偿；热 SKU 分桶。</li></ul>",
            "qas": [("【集群】迁移槽导致超时？", ["盯迁移窗口；重试幂等。", "大促。", "加超时盲重。", "观察 slots。", "「迁移期当半故障。」"], "ency-d-redis-q1")],
            "reflect_id": "ency-d-redis-r1",
            "koujue_txt": "Redis 口诀：预占可丢要补偿，账本在 DB。",
            "floor_title": "淘汰与预占",
            "structure": "maxmemory-policy；volatile vs allkeys。",
            "source_path": "expire.c；cluster 迁移。",
            "online": "淘汰预占键假可卖。",
            "verify": "evicted keys；业务超卖。",
        }),
        ("ency-d-mq", "ENCY-D · 三MQ对照", "ENCY-D-MQ", "Kafka / RabbitMQ / RocketMQ 对照加深", {
            "plain_txt": "交叉 T-Found MQ：一张表钉死订单场景选型。",
            "biz": "可靠投递、顺序、延时关单。",
            "impl": "见下表；Outbox 统一。",
            "principle": "日志型 vs 队列型；事务消息。",
            "substance": "丢失=0；积压可扩。",
            "mermaid_id": "diag-ency-d-mq",
            "mermaid_code": """flowchart LR
  Outbox[本地Outbox] --> K[Kafka高吞吐]
  Outbox --> R[Rocket事务/延时]
  Outbox --> B[Rabbit轻量]
""",
            "trade_title": "订单场景选型",
            "trade_rows": [
                ("Kafka", "高", "极高", "中", "轨迹/对账流"),
                ("RocketMQ", "高", "高", "中", "<b>事务消息/延时关单</b>"),
                ("RabbitMQ", "高", "中", "低", "中厂轻量异步"),
            ],
            "today_html": "<ul><li>支付成功下游统一 Outbox，别直发。</li></ul>",
            "qas": [("【选型】延时关单？", ["Rocket 延时或时间轮；Kafka 需自建。", "订单。", "睡线程。", "延时消息。", "「关单用延时。」"], "ency-d-mq-q1")],
            "reflect_id": "ency-d-mq-r1",
            "koujue_txt": "MQ 口诀：Outbox 出门，场景选对型。",
        }),
        ("ency-d-es", "ENCY-D · Elasticsearch", "ENCY-D-ES", "Elasticsearch：订单/售后检索", {
            "plain_txt": "比喻：ES 是图书馆索引卡——不是账本；账以 DB 为准，卡可以晚一点。",
            "biz": "客服/用户可搜订单；别用 ES 做库存扣减。",
            "impl": "双写/Outbox 同步；search_after；索引按时间。",
            "principle": "倒排；近实时 refresh；主分片。",
            "substance": "索引延迟；检索 P99。",
            "mermaid_id": "diag-ency-d-es",
            "mermaid_code": """flowchart TD
  DB[(订单DB)] --> Out[Outbox]
  Out --> Idx[索引订单文档]
  Idx --> Search[客服检索]
""",
            "today_html": "<ul><li>支付态以 DB 为准；ES 仅查询。</li></ul>",
            "qas": [("【一致】ES 显示已支付 DB 未付？", ["同步乱序/重复；修消费幂等并以 DB 校准。", "客服。", "改 ES 当真相。", "对账校准。", "「ES 不是账本。」"], "ency-d-es-q1")],
            "reflect_id": "ency-d-es-r1",
            "koujue_txt": "ES 口诀：可搜可晚，账在库里。",
            "floor_title": "近实时",
            "structure": "refresh 可见；flush 落盘；merge。",
            "source_path": "bulk 索引；版本冲突。",
            "online": "深度分页撑爆。",
            "verify": "indexing lag。",
        }),
        ("ency-d-shard", "ENCY-D · 分库分表", "ENCY-D-SHARD", "分库分表中间件边界", {
            "plain_txt": "人话：中间件分片像自己建迷你 TDSQL——能力越弱，越要守分片键戒律。",
            "biz": "单表过大前规划；避免误上分布式事务。",
            "impl": "ShardingSphere 等；键设计；扩容预案。",
            "principle": "路由；错位；分布式主键。",
            "substance": "跨库占比；扩容成功率。",
            "mermaid_id": "diag-ency-d-shard",
            "mermaid_code": """flowchart TD
  App --> Mid[分片中间件]
  Mid --> DB1[(db_0)]
  Mid --> DB2[(db_1)]
""",
            "today_html": "<ul><li>能垂直拆域优先于盲目分片。</li></ul>",
            "qas": [("【何时】不到分片？", ["垂直拆分/归档/PolarDB 读扩展仍够。", "评审。", "提前分片。", "量化。", "「分片是手术。」"], "ency-d-shard-q1")],
            "reflect_id": "ency-d-shard-r1",
            "koujue_txt": "分片口诀：键先设计，跨库当例外。",
        }),
    ]
    for sid, toc, sys_id, title, kw in other:
        kw.setdefault("spine_pos", "中间件挂交易链路。")
        kw.setdefault("serves", "订单数据面")
        kw.setdefault("back", "ENCY-D → 本叶")
        parts.append(sec(sid, toc, sys_id, title, deep(**kw)))

    parts.append(sec(
        "ency-d-drill", "ENCY-D · 数据综合题", "ENCY-D-DRILL", "数据百科综合演练",
        plain("把 PolarDB/TDSQL/分片/ES 放同一评审桌。")
        + qa("【综合】支付强一致 + 客服搜索，如何架构？",
            ["OLTP（MySQL/PolarDB/合规库）为账本；Outbox→ES；付后读主；禁 ES 扣库存。",
             "架构。", "ES 当主库。", "CQRS。", "「账本与搜索分手。」"],
            "ency-d-drill-q1")
        + qa("【综合】信创要求达梦，报表却要跑垮主库？",
            ["主库仅交易；报表只读副本或同步到数仓/OLAP。",
             "信创。", "同库跑批。", "读写隔离。", "「批跑远离账本。」"],
            "ency-d-drill-q2")
        + reflect("ency-d-drill-r1"),
    ))
    return "\n".join(parts)
