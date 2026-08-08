# -*- coding: utf-8 -*-
"""FULLMAP HARD GATE · JVM / JUC / Spring / Spark / Flink"""
from ency_fullbar import gated_entry


def jvm():
    chain = """
  <h4 id="ency-fm-jvm-mem">5.1 内存区域与对象分配</h4>
  <p>堆/元空间/直接内存/栈；TLAB；逃逸分析意识。</p>
  <h4 id="ency-fm-jvm-gc">5.2 GC：G1/ZGC 与 Safepoint</h4>
  <p>Region；并发标记；Pause 与分配速率。</p>
  <h4 id="ency-fm-jvm-diag">5.3 诊断：jstat/jcmd/jstack/dump</h4>
  <p>容器 MaxRAMPercentage；OOMKill≠堆满。</p>
"""
    return gated_entry(
        "ency-fm-jvm", "ENCY-FM · JVM全貌", "ENCY-FM-JVM",
        "JVM 全貌：内存·GC·诊断·容器",
        ["jvm", "gc", "fullmap"],
        plain_txt="JVM 停顿与 OOMKill 直接打支付 P99。先日志后猜。",
        spine_pos="支付/售后 Pod 稳定性。",
        serves="运行时",
        back="T-Found-JVM → FULLMAP",
        caps=[
            ("内存", "堆/非堆/直接内存", "OOMKill"),
            ("GC", "G1/ZGC、Safepoint", "停顿"),
            ("诊断", "jstat/jcmd/jstack/MAT", "排障"),
            ("容器", "cgroup、百分比", "K8s"),
            ("调优边界", "先降分配与泄漏", "大促"),
        ],
        mmds=[
            ("diag-fm-jvm-gc",
             "flowchart TD\n  Alloc --> Eden\n  Eden --> Old\n  Old --> GC[混合/Full]\n  GC --> SP[Safepoint]\n"),
            ("diag-fm-jvm-oom",
             "flowchart LR\n  Kill[OOMKill] --> Check{堆满?}\n  Check -->|否| Direct[Direct/Meta/线程]\n  Check -->|是| Leak[泄漏/大对象]\n"),
        ],
        sources=[
            ("分配与 GC 认知路径",
             "Thread Local Allocation Buffer → G1CollectedHeap / ConcurrentMark",
             "// 分配失败 → safepoint → 收集\n"
             "jstat -gcutil <pid> 1000\n"
             "jcmd <pid> GC.heap_info\n"),
        ],
        floors=[
            ("Safepoint 停顿体感",
             "线程到安全点；停顿≈接口卡住。",
             "GC 日志 Pause；分配速率。",
             "导出 Excel 同进程拖垮支付。",
             "看 GC Pause 与成功率同屏。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "阿里系支付（案例归纳）", "scene": "大促 GC",
             "land": "G1+独立支付进程；回调池隔离。",
             "pit": "堆=容器内存误解→OOMKill。",
             "fix": "MaxRAMPercentage+留非堆；NMT。",
             "id": "ency-fm-jvm-case-ali"},
            {"company": "美团类高峰（案例归纳）", "scene": "假死",
             "land": "GC 日志+P99 联动。",
             "pit": "只加 Xmx。",
             "fix": "先看直接内存与线程。",
             "id": "ency-fm-jvm-case-mt"},
        ],
        trade_title="GC 选型粗边界",
        trade_rows=[
            ("G1", "通用低停顿", "中", "默认常见"),
            ("ZGC", "超低停顿", "版本/场景", "要验证"),
        ],
        runbook_title="OOMKill / 停顿尖刺",
        runbook_html="<ol><li>分堆与非堆。</li><li>GC 日志对齐业务。</li><li>dump 前评估影响。</li></ol>",
        fail_html="<ul><li>同进程跑批。</li></ul>",
        today_html="<ul><li>支付独立 Deployment；开 GC 日志。</li></ul>",
        conf_title="容器起步",
        conf_code="-XX:+UseG1GC -XX:MaxRAMPercentage=65 -Xlog:gc*",
        qas=[
            ("【OOMKill】堆不满？", ["Direct/Meta/栈。", "容器。", "加 Xmx。", "NMT。", "「Kill 看 cgroup。」"], "fm-jvm-q1"),
            ("【GC】看啥？", ["Pause、分配速率、Old。", "值班。", "只看堆用了多少。", "日志。", "「Pause 对齐成功率。」"], "fm-jvm-q2"),
            ("【隔离】大导出？", ["独立进程。", "售后。", "同支付。", "拆进程。", "「别和支付同命。」"], "fm-jvm-q3"),
        ],
        koujue_txt="JVM 口诀：日志先开，堆非堆分清，支付单独住。",
        rid="fm-jvm-r1",
    )


def juc():
    chain = """
  <h4 id="ency-fm-juc-jmm">5.1 JMM 与 happens-before</h4>
  <p>可见性/有序性；锁与 volatile 发布。</p>
  <h4 id="ency-fm-juc-aqs">5.2 AQS / 池 / CHM</h4>
  <p>state+CLH；TPE 路径；CHM 树化扩容。</p>
  <h4 id="ency-fm-juc-order">5.3 订单并发套路</h4>
  <p>幂等键优先；锁外 IO；有界池。</p>
"""
    return gated_entry(
        "ency-fm-juc", "ENCY-FM · JUC全貌", "ENCY-FM-JUC",
        "JUC 全貌：JMM·AQS·池·CHM·订单并发",
        ["juc", "aqs", "fullmap"],
        plain_txt="并发不是加 synchronized 了事——hb、池边界、幂等才是支付救命绳。",
        spine_pos="回调并发与库存。",
        serves="支付/售后并发",
        back="T-Found-JUC → FULLMAP",
        caps=[
            ("JMM", "hb、可见、发布", "单例/配置"),
            ("AQS", "锁/信号量/门闩", "互斥"),
            ("线程池", "有界队列、拒绝策略", "回调舱壁"),
            ("CHM", "扩容、树化", "本地结构"),
            ("业务", "幂等>锁", "双扣双退"),
        ],
        mmds=[
            ("diag-fm-juc-hb",
             "flowchart LR\n  W[写] --> Unlock\n  Unlock --> Lock\n  Lock --> R[读可见]\n"),
            ("diag-fm-juc-pool",
             "flowchart TD\n  Task --> Core[核心线程]\n  Task --> Q[有界队列]\n  Task --> Max[最大线程]\n  Task --> Rej[拒绝策略]\n"),
        ],
        sources=[
            ("AQS",
             "AbstractQueuedSynchronizer.acquireQueued / release",
             "if (!tryAcquire()) enqueue + park();\n"
             "release → unparkSuccessor();\n"),
            ("线程池",
             "ThreadPoolExecutor.execute / addWorker",
             "workerCount < core → addWorker\n"
             "else offer(queue) → else addWorker(max) → reject\n"),
        ],
        floors=[
            ("池耗尽链路",
             "队列满+最大线程满→拒绝→Tomcat 线程反压。",
             "AbortPolicy 打点；禁 Cached 无界。",
             "退款客户端无界池 OOM。",
             "看 Active/Queue/Reject。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "阿里支付回调（案例归纳）", "scene": "舱壁池",
             "land": "独立池+幂等表。",
             "pit": "锁内调渠道 HTTP。",
             "fix": "锁外 IO。",
             "id": "ency-fm-juc-case-ali"},
            {"company": "拼多多秒杀（案例归纳）", "scene": "库存",
             "land": "Redis/DB 原子；禁 JVM Atomic 多副本。",
             "pit": "本地 Atomic 当库存。",
             "fix": "分布式原子。",
             "id": "ency-fm-juc-case-pdd"},
        ],
        trade_title="并发控库存",
        trade_rows=[
            ("DB 条件更新", "强", "热点争用", "中低并发"),
            ("Redis DECR", "高", "要补偿", "秒杀"),
            ("JVM Atomic 多副本", "错", "—", "禁止"),
        ],
        runbook_title="池打满 / AQS 堆积",
        runbook_html="<ol><li>看 Reject。</li><li>jstack 锁对象。</li><li>缩临界区。</li></ol>",
        fail_html="<ul><li>无界池。</li></ul>",
        today_html="<ul><li>回调有界池+幂等键。</li></ul>",
        conf_title="池示例",
        conf_code="core=16 max=32 queue=500 AbortPolicy + metrics",
        qas=[
            ("【hb】锁的可见？", ["解锁 hb 加锁。", "原理。", "只背互斥。", "讲 hb。", "「锁有可见。」"], "fm-juc-q1"),
            ("【池】拒策略？", ["Abort 打点依赖重试。", "支付。", "CallerRuns 反压。", "舱壁。", "「拒绝要可见。」"], "fm-juc-q2"),
            ("【库存】多实例？", ["Redis/DB 原子。", "秒杀。", "AtomicInteger。", "分布式。", "「本地计数不准。」"], "fm-juc-q3"),
        ],
        koujue_txt="JUC 口诀：hb 可见，池有界，幂等先于锁。",
        rid="fm-juc-r1",
    )


def spring():
    chain = """
  <h4 id="ency-fm-spring-ioc">5.1 IoC 生命周期与循环依赖</h4>
  <p>三级缓存；构造器注入循环要破。</p>
  <h4 id="ency-fm-spring-tx">5.2 事务代理失效</h4>
  <p>自调用、非 public、错误传播/回滚异常。</p>
  <h4 id="ency-fm-spring-boot">5.3 Boot 自动配置与生产</h4>
  <p>条件装配；配置刷新面；Actuator 暴露面。</p>
"""
    return gated_entry(
        "ency-fm-spring", "ENCY-FM · Spring全貌", "ENCY-FM-SPRING",
        "Spring 全貌：IoC·AOP 事务·Boot·生产边界",
        ["spring", "transaction", "fullmap"],
        plain_txt="Spring 事务失效=资损温床。先怀疑代理，再怀疑数据库。",
        spine_pos="订单服务事务边界。",
        serves="应用框架",
        back="T2 → FULLMAP",
        caps=[
            ("IoC", "Bean 生命周期、循环依赖", "装配"),
            ("AOP", "代理、切面顺序", "鉴权/日志"),
            ("事务", "传播、失效点、只读", "支付"),
            ("Boot", "自动配置、配置优先级", "交付"),
            ("生态", "Security/Data/Cloud 边界", "选型"),
        ],
        mmds=[
            ("diag-fm-spring-tx",
             "flowchart TD\n  Ctrl --> Proxy[事务代理]\n  Proxy --> Svc\n  Svc -->|自调用| Svc\n"),
            ("diag-fm-spring-life",
             "flowchart LR\n  Inst[实例化] --> Pop[属性填充]\n  Pop --> Init[初始化]\n  Init --> Ready[就绪]\n"),
        ],
        sources=[
            ("事务拦截",
             "TransactionInterceptor.invoke → PlatformTransactionManager",
             "@Transactional on public method via proxy\n"
             "self.txMethod()  // 同类调用 → 无代理 → 失效\n"),
        ],
        floors=[
            ("代理失效",
             "JDK/CGLIB 代理；同类自调用不走拦截器。",
             "AnnotationTransactionAttributeSource。",
             "售后自调用未开事务双写。",
             "集成测试断言回滚。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "阿里订单服务（案例归纳）", "scene": "事务边界",
             "land": "事务方法拆 Bean；外部调用出事务。",
             "pit": "自调用失效。",
             "fix": "注入自身或拆类+测试。",
             "id": "ency-fm-spring-case-ali"},
            {"company": "用友类（案例归纳）", "scene": "长事务过 ERP",
             "land": "本地事务短；ERP 异步。",
             "pit": "事务内调 ERP。",
             "fix": "Outbox。",
             "id": "ency-fm-spring-case-yy"},
        ],
        trade_title="事务策略",
        trade_rows=[
            ("本地短事务+Outbox", "推荐", "最终", "支付履约"),
            ("XA", "慎", "强", "短"),
        ],
        runbook_title="事务未回滚",
        runbook_html="<ol><li>查代理/异常类型。</li><li>查传播。</li><li>补集成测试。</li></ol>",
        fail_html="<ul><li>吞异常。</li></ul>",
        today_html="<ul><li>支付更新独立 Bean；测试回滚。</li></ul>",
        conf_title="意识",
        conf_code="rollbackFor=Exception.class 按需\nreadOnly on query",
        qas=[
            ("【失效】自调用？", ["拆 Bean/暴露代理。", "资损。", "怪 DB。", "测回滚。", "「先疑代理。」"], "fm-spring-q1"),
            ("【循环】怎么破？", ["构造器避免环；Setter/事件。", "启动。", "靠三级缓存硬刚。", "改设计。", "「环是设计味。」"], "fm-spring-q2"),
            ("【安全】Actuator？", ["暴露面最小化。", "生产。", "全开。", "网关鉴权。", "「端点也是攻击面。」"], "fm-spring-q3"),
        ],
        koujue_txt="Spring 口诀：事务看代理，IO 出事务，端点要收口。",
        rid="fm-spring-r1",
    )


def spark():
    chain = """
  <h4 id="ency-fm-spark-rdd">5.1 RDD/DF/Dataset 与 Catalyst</h4>
  <p>DF 优先；宽窄依赖；Shuffle。</p>
  <h4 id="ency-fm-spark-tune">5.2 倾斜 · AQE · 分区裁剪</h4>
  <p>加盐；广播小表；看 Spark UI Stages。</p>
"""
    return gated_entry(
        "ency-fm-spark", "ENCY-FM · Spark全貌", "ENCY-FM-SPARK",
        "Spark 全貌：DF·Shuffle·倾斜·调优·对账场景",
        ["spark", "shuffle", "fullmap"],
        plain_txt="Spark=批计算引擎。Shuffle 是账单，倾斜是刺客。",
        spine_pos="日批对账/画像。",
        serves="数仓批",
        back="ENCY-BD-SPARK → FULLMAP",
        caps=[
            ("API", "RDD/DF/SQL", "开发"),
            ("执行", "Stage/Task/Shuffle", "性能"),
            ("调优", "倾斜、AQE、广播", "SLA"),
            ("可靠", "推测执行、重跑幂等", "对账"),
            ("部署", "YARN/K8s", "运维"),
        ],
        mmds=[
            ("diag-fm-spark-shuffle",
             "flowchart TD\n  Map --> Wide{宽依赖?}\n  Wide -->|是| Shuf[Shuffle]\n  Wide -->|否| Pipe[流水线]\n"),
            ("diag-fm-spark-skew",
             "flowchart LR\n  Skew[倾斜] --> Salt[加盐]\n  Skew --> Two[两阶段聚合]\n"),
        ],
        sources=[
            ("宽依赖边界",
             "DAGScheduler 按 shuffle 切 Stage",
             "exchange → new stage\n"
             "Spark UI: Shuffle Read/Write\n"),
        ],
        floors=[
            ("Shuffle 落盘",
             "map 输出分区；reduce 拉取；磁盘与内存压力。",
             "SortShuffleManager（认知）。",
             "热点店铺 join OOM。",
             "看 Stage 倾斜条。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "阿里数仓（案例归纳）", "scene": "GMV 对账",
             "land": "DF+分区裁剪；覆盖写幂等。",
             "pit": "倾斜 key。",
             "fix": "加盐/单独热点。",
             "id": "ency-fm-spark-case-ali"},
            {"company": "美团数据（案例归纳）", "scene": "特征批",
             "land": "AQE；小表广播。",
             "pit": "全表扫。",
             "fix": "分区+列裁剪。",
             "id": "ency-fm-spark-case-mt"},
        ],
        trade_title="Spark vs Flink",
        trade_rows=[
            ("批", "强", "可", "—"),
            ("流", "微批", "强", "—"),
        ],
        runbook_title="慢作业",
        runbook_html="<ol><li>UI 找倾斜 Stage。</li><li>检查扫描量。</li><li>重跑幂等。</li></ol>",
        fail_html="<ul><li>驱动 OOM 收齐大结果。</li></ul>",
        today_html="<ul><li>对账作业幂等覆盖。</li></ul>",
        conf_title="意识",
        conf_code="spark.sql.adaptive.enabled=true\nbroadcast join threshold 按数据",
        qas=[
            ("【Shuffle】为何慢？", ["宽依赖落盘网络。", "调优。", "加机器。", "看 UI。", "「先看 Shuffle。」"], "fm-spark-q1"),
            ("【倾斜】店铺爆？", ["加盐。", "批。", "盲扩。", "治倾斜。", "「热点拆开。」"], "fm-spark-q2"),
            ("【幂等】重跑？", ["覆盖写/分区替换。", "对账。", "追加双份。", "幂等表。", "「重跑可安全。」"], "fm-spark-q3"),
        ],
        koujue_txt="Spark 口诀：DF 优先，盯 Shuffle，治倾斜。",
        rid="fm-spark-r1",
    )


def flink():
    chain = """
  <h4 id="ency-fm-flink-ck">5.1 Checkpoint / 屏障对齐 / 状态</h4>
  <p>Exactly-once 端到端靠 CK + 幂等/事务 sink。</p>
  <h4 id="ency-fm-flink-time">5.2 事件时间与水位线</h4>
  <p>乱序窗口；外卖 ETA/支付成功实时大盘。</p>
  <h4 id="ency-fm-flink-back">5.3 反压与调优</h4>
  <p>反压致 CK 超时；扩并行/降状态。</p>
"""
    return gated_entry(
        "ency-fm-flink", "ENCY-FM · Flink全貌", "ENCY-FM-FLINK",
        "Flink 全貌：Checkpoint·水位线·反压·订单实时",
        ["flink", "checkpoint", "fullmap"],
        plain_txt="Flink=有状态流计算。Checkpoint 是拍照续跑，Sink 幂等才闭环。",
        spine_pos="实时支付成功率/风控特征。",
        serves="实时数仓",
        back="ENCY-BD-FLINK → FULLMAP",
        caps=[
            ("运行时", "JobManager/TaskManager、算子链", "拓扑"),
            ("状态", "KeyedState、后端", "窗口"),
            ("容错", "Checkpoint/Savepoint", "恢复"),
            ("时间", "事件时间、Watermark", "乱序"),
            ("连接", "Kafka source/sink 语义", "入出"),
            ("运维", "反压、CK 时长", "值班"),
        ],
        mmds=[
            ("diag-fm-flink-ck",
             "flowchart LR\n  Src --> Op[算子状态]\n  Op --> CK[Checkpoint]\n  CK --> Backend[(StateBackend)]\n  Op --> Sink\n"),
            ("diag-fm-flink-order",
             "sequenceDiagram\n  participant K as Kafka\n  participant F as Flink\n  participant M as 大盘\n  K->>F: OrderPaid\n  F->>F: 窗口聚合\n  F->>M: 指标\n"),
        ],
        sources=[
            ("Checkpoint 协调",
             "CheckpointCoordinator 注入 barrier → 算子快照 → ack",
             "align barriers → snapshot state → confirm\n"
             "sink exactly-once: transactional / idempotent writer\n"),
        ],
        floors=[
            ("端到端语义",
             "CK 保证 Flink 内；外系统要幂等或两阶段。",
             "Kafka exactly-once sink 事务。",
             "恢复重复写指标双计。",
             "看 CK duration、反压、sink 重复。"),
        ],
        chain_html=chain,
        cases=[
            {"company": "阿里实时数仓（案例归纳）", "scene": "支付大盘",
             "land": "Kafka→Flink→指标；upsert sink。",
             "pit": "CK 超时因反压。",
             "fix": "扩并行/降状态/隔离慢算子。",
             "id": "ency-fm-flink-case-ali"},
            {"company": "美团/饿了么（案例归纳）", "scene": "配送实时",
             "land": "事件时间水位线。",
             "pit": "处理时间窗口在乱序下错账。",
             "fix": "事件时间+允许延迟。",
             "id": "ency-fm-flink-case-mt"},
        ],
        trade_title="Flink 边界",
        trade_rows=[
            ("实时指标", "适合", "Spark 微批可", "—"),
            ("账本事务", "不替代 OLTP", "MySQL", "—"),
        ],
        runbook_title="CK 失败 / 反压",
        runbook_html="<ol><li>看反压链路。</li><li>增大间隔或隔离。</li><li>sink 幂等校验。</li></ol>",
        fail_html="<ul><li>状态无限增长。</li></ul>",
        today_html="<ul><li>实时大盘 upsert；水位线按事件时间。</li></ul>",
        conf_title="意识",
        conf_code="checkpoint interval 与超时\nstate.backend 按规模\nwatermark 策略",
        qas=[
            ("【CK】重复写？", ["sink 幂等。", "实时。", "只加并行。", "幂等键。", "「恰好一次靠两端。」"], "fm-flink-q1"),
            ("【时间】为何事件时间？", ["乱序业务时钟。", "配送。", "处理时间偷懒。", "水位线。", "「业务时钟说话。」"], "fm-flink-q2"),
            ("【反压】怎么判？", ["监控反压链路与 CK。", "值班。", "加内存。", "剖算子。", "「反压有方向。」"], "fm-flink-q3"),
        ],
        koujue_txt="Flink 口诀：事件时间，Checkpoint，Sink 幂等。",
        rid="fm-flink-r1",
    )


def build():
    return "\n".join([jvm(), juc(), spring(), spark(), flink()])
