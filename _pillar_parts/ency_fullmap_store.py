# -*- coding: utf-8 -*-
"""FULLMAP HARD GATE · Redis / MySQL / PolarDB / Gauss / 达梦 / TDSQL"""
from ency_fullbar import gated_entry


def redis():
    chain = """
  <h4 id="ency-fm-redis-ds">5.1 数据结构全谱</h4>
  <p>String/Hash/List/Set/ZSet/Bitmap/HyperLogLog/Stream/Geo；编码切换 ziplist/listpack/hashtable/skiplist。</p>
  <h4 id="ency-fm-redis-expire">5.2 过期 · 淘汰 · 持久化</h4>
  <p>惰性+定期过期；maxmemory-policy；RDB/AOF/混合；丢失窗口与性能权衡。</p>
  <h4 id="ency-fm-redis-ha">5.3 哨兵 / 集群槽</h4>
  <p>Sentinel 切主；Cluster 16384 槽；迁移期重试幂等。</p>
  <h4 id="ency-fm-redis-cache">5.4 缓存模式 · 锁 · 限流</h4>
  <p>Cache-Aside/Write-through；击穿穿透雪崩；SET NX EX+Lua 锁；令牌/滑动窗口限流。禁当账本。</p>
"""
    return gated_entry(
        "ency-fm-redis", "ENCY-FM · Redis全貌", "ENCY-FM-REDIS",
        "Redis 全貌：结构·过期淘汰·持久化·哨兵集群·缓存锁限流",
        ["redis", "cluster", "persistence", "fullmap"],
        plain_txt="Redis=内存数据结构服务器+复制。预占可以，账本不行。",
        spine_pos="秒杀预占、会话、热点、限流。",
        serves="库存预占/风控频控",
        back="T-Found-Redis → FULLMAP",
        caps=[
            ("结构全谱", "十大结构与编码", "业务选型"),
            ("过期淘汰", "惰性/抽样、maxmemory-policy", "预占 TTL"),
            ("持久化", "RDB/AOF/混合", "重启恢复"),
            ("高可用", "主从、哨兵、Cluster 槽", "故障"),
            ("缓存模式", "Aside/双删/逻辑过期", "商品价"),
            ("锁限流", "NX+Lua、令牌桶", "秒杀"),
            ("运维", "大 Key、热 Key、慢日志", "大促"),
        ],
        mmds=[
            ("diag-fm-redis-arch",
             "flowchart TB\n  App --> Redis\n  Redis --> Rep[主从/Cluster]\n  Redis --> Pers[(AOF/RDB)]\n  App --> Pattern[Cache-Aside]\n"),
            ("diag-fm-redis-stock",
             "flowchart TD\n  Ord[下单] --> Lua[DECR/Lua预占]\n  Lua -->|成功| Pay[待支付]\n  Lua -->|失败| Reject\n  Pay --> TTL[TTL释放/支付确认]\n"),
        ],
        sources=[
            ("命令执行",
             "server.c processCommand → call → 具体 t_string.c/t_zset.c 等",
             "aeProcessEvents → readQuery → processCommand\n"
             "decr → getLongLongFromObject → set\n"),
            ("分布式锁意识",
             "SET key token NX EX；Lua 校验删除",
             "SET lock:orderId token NX EX 30\n"
             "if get==token then del  // Lua 原子\n"),
        ],
        floors=[
            ("事件循环与过期",
             "单线程执行命令；IO 多路复用；过期惰性+activeExpireCycle。",
             "expire.c；evict.c。",
             "淘汰预占键→假可卖。",
             "看 evicted_keys、expired、ops。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "拼多多类秒杀（案例归纳）", "scene": "预占库存",
             "land": "Lua/DECR+TTL；支付确认落 DB；热 Key 分桶。",
             "pit": "Redis 当唯一账本且无补偿→重启超卖/少卖。",
             "fix": "预占可丢失要补偿对账；DB 最终权威。",
             "id": "ency-fm-redis-case-pdd"},
            {"company": "美团/饿了么类（案例归纳）", "scene": "频控与热点商家",
             "land": "滑动窗口限流；热点店铺本地+Redis 二级。",
             "pit": "大 Key 商家画像阻塞。",
             "fix": "拆 Key；监控 slowlog；物理隔离。",
             "id": "ency-fm-redis-case-mt"},
        ],
        trade_title="Redis 职责边界",
        trade_rows=[
            ("预占/限流", "适合", "—", "—"),
            ("账本余额", "禁止唯一真相", "MySQL/分布式库", "—"),
            ("搜索", "弱", "ES", "—"),
        ],
        runbook_title="热 Key / 大 Key / 内存打满",
        runbook_html="<ol><li>redis-cli --hotkeys/大 key 扫描。</li><li>淘汰策略与业务 TTL 对齐。</li><li>集群迁移期重试幂等。</li></ol>",
        fail_html="<ul><li>无 TTL 内存泄漏。</li><li>阻塞命令。</li></ul>",
        today_html="<ul><li>秒杀预占 Lua+对账；锁加业务 token。</li></ul>",
        conf_title="基线",
        conf_code="maxmemory-policy=volatile-lru  # 按场景\nappendonly 按 RPO 选\ntimeout/客户端池限流",
        qas=[
            ("【结构】ZSet 底层？", ["skiplist+dict；分值排序。", "原理。", "只背用途。", "讲编码。", "「跳表+哈希。」"], "fm-redis-q1"),
            ("【场景】预占丢了？", ["TTL/淘汰/重启；用对账补偿。", "秒杀。", "加持久化万事大吉。", "补偿。", "「预占可丢要补。」"], "fm-redis-q2"),
            ("【锁】误删锁？", ["token+Lua；续期看门狗。", "并发。", "只 DEL key。", "校验 token。", "「锁要认主人。」"], "fm-redis-q3"),
        ],
        koujue_txt="Redis 口诀：结构选对，预占可丢，账本在库，热键要拆。",
        rid="fm-redis-r1",
    )


def mysql():
    chain = """
  <h4 id="ency-fm-mysql-tx">5.1 事务隔离与 MVCC</h4>
  <p>RC/RR；ReadView；undo 版本链；当前读加锁。</p>
  <h4 id="ency-fm-mysql-lock">5.2 锁：记录/间隙/next-key</h4>
  <p>唯一键点查 vs 范围；死锁回滚成本低者。</p>
  <h4 id="ency-fm-mysql-idx">5.3 索引 B+ 与优化器</h4>
  <p>聚簇/二级；最左前缀；EXPLAIN。</p>
  <h4 id="ency-fm-mysql-repl">5.4 复制与高可用</h4>
  <p>binlog 行模式；半同步；MHA/Group Replication/云 HA；只读延迟。</p>
  <h4 id="ency-fm-mysql-shard">5.5 分库分表边界</h4>
  <p>分片键；跨片事务慎；归档优先于过早分片。</p>
"""
    return gated_entry(
        "ency-fm-mysql", "ENCY-FM · MySQL全貌", "ENCY-FM-MYSQL",
        "MySQL/InnoDB 全貌：隔离·锁·索引·复制 HA·分片边界",
        ["mysql", "innodb", "mvcc", "fullmap"],
        plain_txt="InnoDB=聚簇索引账本+MVCC+redo/undo。订单幂等与行锁都落这里。",
        spine_pos="订单/支付/售后账本。",
        serves="正逆向事务",
        back="T-Found-MySQL → FULLMAP",
        caps=[
            ("存储", "表空间、页、聚簇索引", "点查"),
            ("事务", "ACID、隔离、MVCC", "支付更新"),
            ("锁", "行/间隙/死锁", "并发退"),
            ("日志", "redo/undo/binlog", "恢复复制"),
            ("复制HA", "主从、半同步、切换", "RPO/RTO"),
            ("扩展", "读写分离、分片边界", "增长"),
        ],
        mmds=[
            ("diag-fm-mysql-tx",
             "flowchart TD\n  SQL --> Opt[优化器]\n  Opt --> InnoDB\n  InnoDB --> Redo[(redo)]\n  InnoDB --> Undo[(undo/MVCC)]\n  InnoDB --> Bin[(binlog)]\n"),
            ("diag-fm-mysql-pay",
             "sequenceDiagram\n  participant P as 支付回调\n  participant D as MySQL\n  P->>D: INSERT 幂等键\n  P->>D: UPDATE order WHERE status=CREATED\n  D-->>P: rowcount\n"),
        ],
        sources=[
            ("条件更新",
             "handler::ha_update_row / 锁模块 lock_rec",
             "UPDATE orders SET status='PAID' WHERE id=? AND status='CREATED';\n"
             "-- row_count=0 → 查现态做幂等成功/拒绝\n"),
            ("事务提交秩序意识",
             "InnoDB prepare → binlog → commit（组提交）",
             "crash-safe：binlog 与 redo 协调；复制看 binlog position/GTID\n"),
        ],
        floors=[
            ("MVCC+锁",
             "快照读看 ReadView；当前读加记录/间隙锁。",
             "lock0*; read0*; trx0trx.*（认知）。",
             "状态扫描 FOR UPDATE 锁扩大。",
             "看 data_locks、死锁日志、EXPLAIN。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "阿里系订单库（案例归纳）", "scene": "支付回调幂等",
             "land": "唯一键+条件更新；短事务。",
             "pit": "长事务包外部 HTTP→锁等待雪崩。",
             "fix": "先落库再异步；回调解耦。",
             "id": "ency-fm-mysql-case-ali"},
            {"company": "招行类账务（案例归纳）", "scene": "流水+余额",
             "land": "先流水后余额条件更新；热户治理。",
             "pit": "先改余额后写流水崩溃→账实不符。",
             "fix": "顺序强制；对账文件。",
             "id": "ency-fm-mysql-case-cmb"},
        ],
        trade_title="MySQL vs 分布式库",
        trade_rows=[
            ("单分片事务", "最清晰", "看产品", "—"),
            ("写扩展", "垂直/分片", "TDSQL/OB", "—"),
            ("读扩展", "从库/PolarDB RO", "—", "—"),
        ],
        runbook_title="死锁 / 慢查 / 主从延迟",
        runbook_html="<ol><li>死锁日志定锁序。</li><li>EXPLAIN+慢日志。</li><li>付后读主。</li></ol>",
        fail_html="<ul><li>无唯一键双付。</li><li>深分页。</li></ul>",
        today_html="<ul><li>支付/退款唯一键+条件更新；禁 float 金额。</li></ul>",
        conf_title="意识项",
        conf_code="transaction_isolation=READ-COMMITTED  # 按业务\nbinlog_format=ROW\nsync_binlog/innodb_flush_log_at_trx_commit 按 RPO",
        qas=[
            ("【锁】间隙锁何时？", ["RR 范围/非唯一。", "售后。", "怪并发。", "收紧条件。", "「范围即间隙。」"], "fm-mysql-q1"),
            ("【幂等】回调两次？", ["唯一键冲突当成功。", "支付。", "再扣一次。", "幂等表。", "「冲突即成功。」"], "fm-mysql-q2"),
            ("【分片】何时不上？", ["归档/RO/垂直拆够用。", "评审。", "提前分片。", "量化。", "「分片是手术。」"], "fm-mysql-q3"),
        ],
        koujue_txt="MySQL 口诀：唯一键幂等，条件更新，短事务，付后读主。",
        rid="fm-mysql-r1",
    )


def polardb():
    chain = """
  <h4 id="ency-fm-polardb-arch">5.1 计算存储分离 · 一写多读</h4>
  <p>Primary 写；RO 共享存储读；事务在主。</p>
  <h4 id="ency-fm-polardb-lag">5.2 复制延迟与付后读主</h4>
  <p>支付后读己之写必须主库；报表走 RO。</p>
  <h4 id="ency-fm-polardb-bound">5.3 适用边界</h4>
  <p>兼容 MySQL/PG 上升级；不是自动分片写扩展银弹。</p>
"""
    return gated_entry(
        "ency-fm-polardb", "ENCY-FM · PolarDB全貌", "ENCY-FM-POLARDB",
        "PolarDB 全貌：共享存储·RO·延迟·边界",
        ["polardb", "shared-storage", "fullmap"],
        plain_txt="PolarDB=共享存储一写多读。先治读，再谈分布式写。",
        spine_pos="订单库云上升级读扩展。",
        serves="OLTP 读扩展",
        back="ENCY-D-POLARDB → FULLMAP",
        caps=[
            ("架构", "计算存储分离、共享存储多副本", "云 HA"),
            ("读写", "Primary/RO 路由", "付后读主"),
            ("兼容", "MySQL/PG 协议", "迁移"),
            ("边界", "写仍单主；非分片", "选型"),
            ("运维", "切换、备份、只读延迟", "值班"),
        ],
        mmds=[
            ("diag-fm-polar-arch",
             "flowchart LR\n  W[写] --> Primary\n  R[读] --> RO\n  Primary --> Stor[(共享存储)]\n  RO --> Stor\n"),
            ("diag-fm-polar-rw",
             "flowchart TD\n  PayOK[支付成功] --> Read{读何处}\n  Read -->|读己之写| Primary\n  Read -->|报表| RO\n"),
        ],
        sources=[
            ("路由意识",
             "应用数据源：@Primary / @Replica 或中间件读写拆分",
             "if (needReadYourWrites) usePrimary();\n"
             "else useRO();\n"),
        ],
        floors=[
            ("共享存储语义",
             "数据一份，计算多头；RO 回放日志；写冲突由主串行。",
             "云厂商存储多副本；计算节点本地缓存失效。",
             "RO 延迟导致「已支付仍待支付」展示。",
             "看 RO lag、切换事件。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "阿里云消费零售（案例归纳）", "scene": "订单读扩展",
             "land": "报表/列表 RO；交易写主。",
             "pit": "支付回跳读 RO。",
             "fix": "会话粘滞主库。",
             "id": "ency-fm-polar-case-ali"},
            {"company": "用友类企业应用上云（案例归纳）", "scene": "兼容迁移",
             "land": "MySQL 兼容评估后迁 PolarDB。",
             "pit": "方言/函数差异。",
             "fix": "SQL 兼容套件。",
             "id": "ency-fm-polar-case-yy"},
        ],
        trade_title="PolarDB vs 分片库",
        trade_rows=[
            ("读扩展", "强", "中", "—"),
            ("写扩展", "弱(单主)", "TDSQL/OB 强", "—"),
            ("迁移成本", "低(兼容)", "高", "—"),
        ],
        runbook_title="RO 延迟 / 切换",
        runbook_html="<ol><li>延迟→读主开关。</li><li>切换后核对连接串与位点。</li></ol>",
        fail_html="<ul><li>读写分离误配。</li></ul>",
        today_html="<ul><li>付后读主写进代码规范。</li></ul>",
        conf_title="路由规范",
        conf_code="transactional datasource = primary\nreporting datasource = readonly",
        qas=[
            ("【本质】与分片区别？", ["一份盘多计算 vs 多片。", "选型。", "混谈。", "画图。", "「共享存储≠分片。」"], "fm-polar-q1"),
            ("【坑】付后读 RO？", ["粘滞主库。", "支付。", "怪前端。", "路由。", "「付后读主。」"], "fm-polar-q2"),
            ("【边界】写顶了？", ["垂直拆/分片/分布式库，不是加 RO。", "容量。", "加只读。", "写路径。", "「RO 不解写。」"], "fm-polar-q3"),
        ],
        koujue_txt="PolarDB 口诀：写主读 RO，付后读主，写扩展另案。",
        rid="fm-polar-r1",
    )


def gauss():
    chain = """
  <h4 id="ency-fm-gauss-topo">5.1 先认拓扑：集中式 vs 分布式形态</h4>
  <p>落地前确认节点角色、副本、是否分片、事务模型文档。</p>
  <h4 id="ency-fm-gauss-mig">5.2 迁移：兼容套件 → 双跑 → 切换 → 演练</h4>
  <p>方言/隔离/工具链差异是最大静默风险。</p>
"""
    return gated_entry(
        "ency-fm-gauss", "ENCY-FM · GaussDB全貌", "ENCY-FM-GAUSS",
        "GaussDB 全貌：拓扑·一致性·迁移·信创落地",
        ["gaussdb", "xinchuang", "fullmap"],
        plain_txt="GaussDB 常见政企/金融信创清单——先认清买的是哪套拓扑再迁流量。",
        spine_pos="信创订单/报备库。",
        serves="合规 OLTP",
        back="ENCY-D-GAUSS → FULLMAP",
        caps=[
            ("形态", "集中/分布式", "架构评审"),
            ("一致", "强一致取向与副本", "账务"),
            ("兼容", "SQL/驱动/工具", "迁移"),
            ("运维", "备份恢复演练", "RTO"),
            ("边界", "跨片事务成本", "模型"),
        ],
        mmds=[
            ("diag-fm-gauss-mig",
             "flowchart TD\n  A[兼容评估] --> B[双跑]\n  B --> C[切换]\n  C --> D[故障演练]\n"),
            ("diag-fm-gauss-topo",
             "flowchart LR\n  App --> CN[协调/计算]\n  CN --> DN[(数据节点/主备)]\n"),
        ],
        sources=[
            ("迁移校验",
             "应用层：JDBC URL/方言；核心 SQL 回归集",
             "for sql in critical_suite:\n"
             "  assert same_result(mysql, gauss)\n"),
        ],
        floors=[
            ("拓扑决定事务",
             "集中式≈主备切换；分布式要问分片键与跨片。",
             "厂商文档：副本协议与隔离级别。",
             "假设 MySQL 方言 100%→分摊算错。",
             "看兼容失败用例、切换 RTO。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "招行类信创替换（案例归纳）", "scene": "核心交易评估",
             "land": "兼容套件+压测支付回调。",
             "pit": "未测隔离差异导致幻读业务假设失败。",
             "fix": "隔离级别与用例钉死。",
             "id": "ency-fm-gauss-case-cmb"},
            {"company": "用友类政企（案例归纳）", "scene": "单据库迁移",
             "land": "双跑对账。",
             "pit": "工具链备份未演练。",
             "fix": "定期恢复演练。",
             "id": "ency-fm-gauss-case-yy"},
        ],
        trade_title="Gauss 选型",
        trade_rows=[
            ("信创强制", "高优先级", "达梦等同池", "—"),
            ("生态熟练度", "要培训", "MySQL 熟", "—"),
        ],
        runbook_title="切换 / 兼容回归",
        runbook_html="<ol><li>切换检查表。</li><li>核心 SQL 红线用例。</li></ol>",
        fail_html="<ul><li>未认拓扑就上分片功能。</li></ul>",
        today_html="<ul><li>先拓扑确认会再迁。</li></ul>",
        conf_title="迁移门禁",
        conf_code="critical_sql_suite=green\nbackup_restore_drill=ok\npay_callback_perf=baseline",
        qas=[
            ("【第一步】最该问啥？", ["拓扑与事务模型。", "选型。", "比报价。", "认拓扑。", "「先问拓扑。」"], "fm-gauss-q1"),
            ("【风险】最大静默坑？", ["方言/隔离差异。", "迁移。", "只迁数据。", "用例。", "「用例锁命。」"], "fm-gauss-q2"),
            ("【演练】为何必须？", ["RTO 真实才算数。", "运维。", "文档说说。", "杀节点。", "「不演练=没备份。」"], "fm-gauss-q3"),
        ],
        koujue_txt="Gauss 口诀：先认拓扑，用例锁命，演练才算数。",
        rid="fm-gauss-r1",
    )


def dm():
    chain = """
  <h4 id="ency-fm-dm-ora">5.1 Oracle 替换工程路径</h4>
  <p>差异表（类型/空串/分页/序列）进仓库；驱动与池重测。</p>
  <h4 id="ency-fm-dm-ha">5.2 数据守护 / 备份恢复</h4>
  <p>无云控制台也要标准备份+演练。</p>
"""
    return gated_entry(
        "ency-fm-dm", "ENCY-FM · 达梦全貌", "ENCY-FM-DM",
        "达梦全貌：替换路径·守护·备份·边界",
        ["dameng", "xinchuang", "fullmap"],
        plain_txt="达梦常作 Oracle 岗位国产方向盘——习惯近，工具链与细节要重拿本本。",
        spine_pos="信创交易/报备。",
        serves="合规 OLTP",
        back="ENCY-D-DM → FULLMAP",
        caps=[
            ("引擎", "集中式事务、对象权限", "账本"),
            ("高可用", "数据守护/集群", "切换"),
            ("迁移", "Oracle 差异清单", "改造"),
            ("运维", "备份演练、监控对接", "RPO"),
            ("边界", "生态与人才", "编制"),
        ],
        mmds=[
            ("diag-fm-dm-mig",
             "flowchart LR\n  Ora[(Oracle)] --> Diff[差异清单]\n  Diff --> App[改SQL/应用]\n  App --> DM[(达梦)]\n"),
            ("diag-fm-dm-bak",
             "flowchart TD\n  Bak[备份] --> Drill[恢复演练]\n  Drill --> OK{成功?}\n  OK -->|否| Fix[修脚本]\n"),
        ],
        sources=[
            ("分页/序列差异意识",
             "应用 DAO 层方言适配",
             "-- Oracle rownum vs DM LIMIT/FETCH\n"
             "-- sequence.nextval 行为核对\n"),
        ],
        floors=[
            ("替换不是改驱动",
             "语义差异导致静默错页/错序。",
             "JDBC 方言；ORM 方言。",
             "售后列表错页。",
             "看分页用例、备份演练记录。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "政企用友生态（案例归纳）", "scene": "Oracle→DM",
             "land": "差异表+双跑。",
             "pit": "空字符串与 NULL 语义差。",
             "fix": "用例覆盖空串。",
             "id": "ency-fm-dm-case-yy"},
            {"company": "金融信创（案例归纳）", "scene": "报备库",
             "land": "守护+演练。",
             "pit": "只靠盘阵无演练。",
             "fix": "定期恢复。",
             "id": "ency-fm-dm-case-fin"},
        ],
        trade_title="达梦边界",
        trade_rows=[
            ("Oracle 替换", "常见路径", "Gauss 等同池", "—"),
            ("互联网生态", "弱于 MySQL", "MySQL/PolarDB", "—"),
        ],
        runbook_title="备份恢复",
        runbook_html="<ol><li>备份校验。</li><li>恢复演练签字。</li></ol>",
        fail_html="<ul><li>未改分页方言。</li></ul>",
        today_html="<ul><li>差异表进 Git。</li></ul>",
        conf_title="门禁",
        conf_code="dialect_diff_sheet=in_repo\nrestore_drill_last_30d=ok",
        qas=[
            ("【迁移】先做什么？", ["差异清单。", "项目。", "直接切。", "清单。", "「差异表进仓。」"], "fm-dm-q1"),
            ("【RPO】如何证？", ["恢复演练。", "运维。", "有备份文件。", "演练。", "「演练才算备份。」"], "fm-dm-q2"),
            ("【应用】分页坑？", ["方言重测。", "列表。", "照搬 rownum。", "适配层。", "「分页必回归。」"], "fm-dm-q3"),
        ],
        koujue_txt="达梦口诀：差异表进仓，备份必演练。",
        rid="fm-dm-r1",
    )


def tdsql():
    chain = """
  <h4 id="ency-fm-tdsql-shard">5.1 分片键与路由</h4>
  <p>代理解析 SQL→DN；无键扇出；跨片 join/事务额外协议。</p>
  <h4 id="ency-fm-tdsql-xa">5.2 分布式事务边界</h4>
  <p>能单片就单片；跨片当成本事件。</p>
  <h4 id="ency-fm-tdsql-hot">5.3 热点分片治理</h4>
  <p>爆店/大 V 用户倾斜；加盐/隔离库。</p>
"""
    return gated_entry(
        "ency-fm-tdsql", "ENCY-FM · TDSQL全貌", "ENCY-FM-TDSQL",
        "TDSQL 全貌：分片·分布式事务·热点·治理",
        ["tdsql", "sharding", "fullmap"],
        plain_txt="TDSQL 类=数据切开。分片键定终身；跨片当事故预算。",
        spine_pos="高并发订单水平扩展。",
        serves="订单写扩展",
        back="ENCY-D-TDSQL → FULLMAP",
        caps=[
            ("架构", "代理/计算 + DN", "路由"),
            ("分片键", "user/order/店铺策略", "模型"),
            ("事务", "单片 vs 分布式", "支付"),
            ("索引", "全局二级索引成本", "查询"),
            ("治理", "热点、扩容迁移", "大促"),
            ("运维", "跨片 SQL 审计", "规范"),
        ],
        mmds=[
            ("diag-fm-tdsql-route",
             "flowchart TD\n  SQL --> Proxy\n  Proxy --> R{分片键?}\n  R -->|有| One[单DN]\n  R -->|无| Fan[扇出/风险]\n"),
            ("diag-fm-tdsql-hot",
             "flowchart LR\n  Hot[热点片] --> Salt[加盐/拆]\n  Hot --> Limit[限流]\n"),
        ],
        sources=[
            ("路由意识",
             "SQL 必须带分片键；中间件路由",
             "SELECT * FROM orders WHERE order_id=?  -- order_id 含片或映射\n"
             "-- 禁止无键全表扫管理端抽数\n"),
        ],
        floors=[
            ("跨片成本",
             "分布式事务/扇出放大延迟与失败率。",
             "代理计划；两阶段。",
             "按非键查订单扇出。",
             "看跨片比例、慢 SQL。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "腾讯云金融/支付类（案例归纳）", "scene": "交易分片",
             "land": "按用户/商户键；严格单片事务。",
             "pit": "管理报表无键扫生产。",
             "fix": "报表走数仓。",
             "id": "ency-fm-tdsql-case-fin"},
            {"company": "电商大促（案例归纳）", "scene": "热点商户",
             "land": "热点隔离+限流。",
             "pit": "单商户写爆一片。",
             "fix": "二级拆分/隔离。",
             "id": "ency-fm-tdsql-case-ecom"},
        ],
        trade_title="TDSQL vs PolarDB vs 中间件分片",
        trade_rows=[
            ("写扩展", "强", "弱", "中(自建)"),
            ("运维", "厂商", "云托管", "自建重"),
            ("跨片", "贵", "无", "贵"),
        ],
        runbook_title="跨片审计 / 热点",
        runbook_html="<ol><li>审计无键 SQL。</li><li>热点片限流与拆分。</li></ol>",
        fail_html="<ul><li>误用广播 SQL。</li></ul>",
        today_html="<ul><li>售后查询路径与分片键对齐。</li></ul>",
        conf_title="红线",
        conf_code="require_shard_key=true\ncross_shard_tx_budget=monitored",
        qas=[
            ("【键】怎么选？", ["对齐最高频点查；接受列表二次设计。", "模型。", "随意。", "评审键。", "「键定终身。」"], "fm-tdsql-q1"),
            ("【热点】怎么办？", ["加盐/隔离/限流。", "大促。", "加 DN 盲扩。", "治倾斜。", "「先治倾斜。」"], "fm-tdsql-q2"),
            ("【事务】跨片？", ["当例外；能避则避。", "支付。", "随便开。", "单片设计。", "「跨片当事故。」"], "fm-tdsql-q3"),
        ],
        koujue_txt="TDSQL 口诀：分片键定终身，跨片当事故，报表走数仓。",
        rid="fm-tdsql-r1",
    )


def build():
    # fix gauss today_html unclosed
    return "\n".join([redis(), mysql(), polardb(), gauss(), dm(), tdsql()])
