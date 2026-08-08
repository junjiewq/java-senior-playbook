# -*- coding: utf-8 -*-
"""基础件极致：JVM/JUC/MySQL/Redis/Kafka/Rabbit/RocketMQ — 人话→掀底板→落地→回扣"""
from anti_water_boost import boost_found_rocket
from helpers import (
    qa, c4, five, tradeoff, mermaid, spine, essence, plain, koujue,
    failbox, runbook, reflect, today, checklist, conf, floor, ban,
)


def build() -> str:
    hub = f"""
<section class="block" id="t-found-x" data-toc="T-Found-X · 基础件掀底板总图" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>基础件极致：人话引入 → 掀底板 → 落地 → 回扣正逆向</h2>
{spine("JVM/JUC/MySQL/Redis/三种 MQ：每项挂钩订单哪一步；底板讲清机制与源码路径；再给配置/代码改法。",
       serves="下单预占、支付回调、Outbox、售后回补、大促削峰",
       back="T3–T6 零件 → 本极致章 → B-X / S-Year M08")}
{plain("人话：别背「要建索引」「注意线程安全」。问自己：这层底板坏了时，支付回调会怎样？退款会双飞吗？下面每节都按：比喻 → 掀底板 → 今天改什么 → 业务实质。")}
  <table>
    <thead><tr><th>组件</th><th>挂正逆向哪步</th><th>锚点</th></tr></thead>
    <tbody>
      <tr><td>JVM</td><td>支付/售后 Pod OOM、停顿、发布排水</td><td><a href="#t-found-jvm">#t-found-jvm</a></td></tr>
      <tr><td>JUC</td><td>回调线程池、库存 CAS、并发退</td><td><a href="#t-found-juc">#t-found-juc</a></td></tr>
      <tr><td>MySQL</td><td>订单行锁、分摊、对账、幂等唯一键</td><td><a href="#t-found-mysql">#t-found-mysql</a></td></tr>
      <tr><td>Redis</td><td>秒杀预占、会话、热点 SKU</td><td><a href="#t-found-redis">#t-found-redis</a></td></tr>
      <tr><td>Kafka</td><td>日志/轨迹/对账流、高吞吐事件</td><td><a href="#t-found-kafka">#t-found-kafka</a></td></tr>
      <tr><td>RabbitMQ</td><td>中厂轻量异步、延迟重试小场景</td><td><a href="#t-found-rabbit">#t-found-rabbit</a></td></tr>
      <tr><td>RocketMQ</td><td>订单/支付事务消息、延时关单</td><td><a href="#t-found-rocket">#t-found-rocket</a></td></tr>
      <tr><td>选型矩阵</td><td>同一问题多方案对照</td><td><a href="#t-found-matrix">#t-found-matrix</a></td></tr>
    </tbody>
  </table>
{koujue("基础件口诀：人话进门，底板见血，配置收口，单号回扣。")}
{reflect("foundx-hub-r1")}
</section>
"""

    jvm = f"""
<section class="block" id="t-found-jvm" data-toc="T-Found-X · JVM掀底板" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>JVM：支付 Pod 为啥「假死」与 OOMKill</h2>
{plain("比喻：堆像仓库货架，GC 像盘点停业；容器 limit 是仓库大门高度——货架堆到门楣会被宿主机直接拆店（OOMKill）。")}
{c4(
    "支付回调线程卡住或频繁 Full GC，客人看到扣款成功却一直转圈；发布时杀进程丢在途请求。",
    "堆/非堆对齐容器；G1 目标停顿；优雅停机排水；回调池与业务池隔离。",
    "见掀底板：对象分配→TLAB→Eden→Region→GC Root 扫描；Safepoint 停顿。",
    "P99 与 GC 日志对齐；OOMKill 次数=0；回调解压不抖。",
    "大促分配速率飙升直接打出 GC 毛刺。",
)}
{floor(
    "运行时内存与 GC",
    "新生代/老年代（G1 为 Region 堆）；对象优先 Eden；存活晋升；GC Root（栈帧、静态、JNI）标记；混合收集；分配失败→Full GC。Safepoint 让线程停在可安全点，停顿体感=「接口突然卡住」。",
    "热点：<code>Thread.allocate</code> → TLAB；G1:<code>G1CollectedHeap</code>/<code>G1ConcurrentMark</code>；看 GC 日志 <code>gc*</code>。JDK 工具：<code>jstat -gcutil</code>、<code>jcmd GC.heap_info</code>、<code>jmap</code>。<b>调用链体感：</b>请求分配对象 → 堆不足 → 进入 SafePoint → mutator 停 → 回调 RT 尖刺。",
    "售后导出大 Excel 在支付同进程 → Old 涨 → 混合 GC 变长 → 支付 P99 从 80ms 变 2s；Xmx≥limit → cgroup OOMKill，Pod 重启，回调依赖渠道重试+本地幂等才不丢单。",
    "看：GC 日志 Pause、Allocation Rate、Old Occupancy；K8s OOMKilled；线程 <code>jstack</code> 是否大量 <code>VM Thread</code>/<code>GC task</code> 时段；支付成功率是否与 GC 尖刺同秒。",
)}
{conf("容器 JVM 起步（示例）", """# Deployment: memory request/limit 2Gi
JAVA_TOOL_OPTIONS: >-
  -XX:+UseG1GC -XX:MaxGCPauseMillis=200
  -XX:MaxRAMPercentage=65.0
  -XX:+AlwaysPreTouch
  -Xlog:gc*:file=/logs/gc.log:time,uptime,level,tags
# 原则：MaxRAMPercentage 后堆仍 < limit，留 Metaspace/Direct/线程栈
""")}
{today("""<ul>
<li>支付服务独立 Deployment；回调 Executor 单独池，拒绝策略 <code>CallerRuns</code> 慎用（会反压 Tomcat）。</li>
<li><code>preStop</code>：sleep 若干秒 + 先 readiness=false，等 in-flight 回调结束再杀。</li>
<li>大促前用生产采样流量压一轮，盯 GC Pause P99 与支付成功率同屏。</li>
</ul>""")}
{qa("【线上】支付 Pod 反复 OOMKill，堆才 1.2G，limit 2G，为何？",
    ["Direct Buffer/线程栈/Metaspace/原生内存不计入堆；Netty/RocketMQ 客户端爱吃直接内存。查 NMT/<code>-XX:MaxDirectMemorySize</code>，降连接或提 limit，别只加 Xmx。",
     "回调高峰。", "以为堆=容器内存。", "NMT + 限 Direct。", "「OOMKill 看的是 cgroup，不只是堆。」"],
    "found-jvm-q1")}
{reflect("found-jvm-r1")}
</section>
"""

    juc = f"""
<section class="block" id="t-found-juc" data-toc="T-Found-X · JUC掀底板" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>JUC：回调池、AQS、ConcurrentHashMap、库存 CAS</h2>
{plain("比喻：AQS 像银行叫号器——抢到 state 的办业务，其余排队（CLH 变体）；CHM 像超市多条收银通道，扩容时要挪篮子。")}
{c4(
    "支付回调并发敲同一笔；库存预占要原子；线程池打满会拒单或拖死容器。",
    "幂等键落库优先；热点用 CAS/分段；池有界+舱壁；少用全局 synchronized 包整单。",
    "见掀底板：AQS state+队列；CHM 树化与扩容；线程池 Worker 与拒绝策略。",
    "无双扣、无双退；池拒绝有指标；锁等待可解释。",
    "大促回调 QPS×RT≈线程占用（Little's Law）。",
)}
{floor(
    "AQS / 线程池 / CHM",
    "<b>AQS：</b>volatile state + CLH 风格等待队列；<code>acquire</code> 失败 park；释放 unpark 后继。ReentrantLock/CountDownLatch/Semaphore 全建在这上。<b>ThreadPoolExecutor：</b>ctl 打包 runState+workerCount；任务路径：核心线程→队列→最大线程→拒绝策略。<b>ConcurrentHashMap：</b>数组+链表/红黑树；扩容 transfer 按桶迁移；sizeCtl 协调。",
    "路径：<code>AbstractQueuedSynchronizer.acquireQueued</code> / <code>addWaiter</code>；<code>ThreadPoolExecutor.execute</code>→<code>addWorker</code>；<code>ConcurrentHashMap.putVal</code>→<code>treeifyBin</code>/<code>transfer</code>。锁竞争看 <code>jstack</code> 的 <code>park</code> 与 <code>-locked</code>。",
    "退款渠道客户端用无界队列线程池→堆积 OOM；库存用 <code>AtomicInteger</code> 只适合单机演示，多实例必须 Redis/DB 原子。CHM 作本地「退款中」集合，扩容尖刺会放大 P99。",
    "看：池 Active/Queue/Reject；锁 <code>blocked</code> 线程；DB 死锁日志；业务幂等冲突计数（正常重放 vs bug）。",
)}
{conf("支付回调舱壁池（示意）", """ThreadPoolExecutor payCallbackPool = new ThreadPoolExecutor(
  16, 32, 60, TimeUnit.SECONDS,
  new ArrayBlockingQueue<>(500),
  new ThreadFactoryBuilder().setNameFormat("pay-cb-%d").build(),
  new AbortPolicy() // 拒绝要打点+依赖渠道重试，别静默丢
);
// 禁止：Executors.newCachedThreadPool() 无界洪水
""")}
{today("""<ul>
<li>回调入口：先唯一键 insert，冲突当成功返回；再异步推 Outbox。</li>
<li>库存多实例：Redis <code>DECR</code>/<code>Lua</code> 或 DB <code>UPDATE ... WHERE qty&gt;=?</code>，别信单机 Atomic。</li>
<li>池指标挂看板：reject&gt;0 立刻扩或限流，别先加机器盲扩。</li>
</ul>""")}
{tradeoff("并发控库存", [
    ("DB 乐观锁 version/条件更新", "强、可审计", "热点行争用", "低", "中低并发 SKU"),
    ("Redis DECR+异步落库", "高", "要补偿", "中", "<b>秒杀预占</b>"),
    ("分布式锁再读改写", "易错用", "锁粒度大则慢", "中", "慎：锁内别调远端"),
    ("JVM Atomic 多副本", "错", "数据各飞", "—", "<b>禁止</b>"),
])}
{qa("【线上】jstack 见大量线程 WAITING on AQS，支付 RT 高，怎么判？",
    ["看锁对象是业务锁还是池/连接池；若是同一订单锁，检查锁范围是否包了远端调用。缩临界区，远端移出锁外。",
     "退款并发。", "盲目加线程。", "锁外 IO。", "「锁里调 HTTP=自造死锁剧场。」"],
    "found-juc-q1")}
{reflect("found-juc-r1")}
</section>
"""

    mysql = f"""
<section class="block" id="t-found-mysql" data-toc="T-Found-X · MySQL掀底板" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>MySQL/InnoDB：订单行锁、幂等、分摊不平</h2>
{plain("比喻：聚簇索引像一本按主键钉死的账本，二级索引是目录只记页码；行锁是「锁这一行账」，缺口锁防幻读像锁住「插不进的缝」。")}
{c4(
    "同一售后单并发退、对账要对上分摊行；慢 SQL 拖垮支付同库。",
    "幂等唯一键；状态机条件更新；索引覆盖查询；短事务；热点拆。",
    "见掀底板：B+ 聚簇、事务隔离、锁类型、undo/redo。",
    "无双退；分摊合计平；慢查询&lt;阈值。",
    "大促插入热点页与 gap lock 等待。",
)}
{floor(
    "InnoDB 索引与锁",
    "聚簇索引叶子=整行；二级索引叶子=主键。MVCC：undo 链+Read View。锁：record / gap / next-key；<code>UPDATE</code> 加锁范围由检索条件是否走唯一索引决定。redo 崩溃恢复；undo 回滚+MVCC。",
    "认知路径：优化器选索引→InnoDB handler 加锁→行在 page 内；死锁检测 rollback 成本低者。<code>SHOW ENGINE INNODB STATUS</code>；<code>performance_schema.data_locks</code>（8.0）。EXPLAIN：type/key/rows。",
    "退款 <code>SELECT ... FOR UPDATE</code> 未走 after_sale_id 唯一键而扫状态→锁范围扩大→并发售后排队；支付回调与订单更新死锁（两事务锁序相反）。分摊用浮点或先入为主舍入导致行合计≠头。",
    "看：锁等待/死锁日志；EXPLAIN；<code>innodb_row_lock_time</code>；业务「幂等冲突」「分摊不平衡」告警。",
)}
{conf("幂等 + 状态机条件更新", """-- 支付回调幂等
INSERT INTO pay_idempotent(channel, trade_no, order_id, created_at)
VALUES (?, ?, ?, NOW());  -- UNIQUE(channel, trade_no)

-- 仅允许 CREATED -> PAID
UPDATE orders SET status='PAID', pay_time=NOW()
 WHERE order_id=? AND status='CREATED';
-- row_count=0 → 查现态，已是 PAID 则当成功
""")}
{today("""<ul>
<li>售后单 <code>UNIQUE(after_sale_id)</code> + 退款 attempt 表唯一键，禁「无条件 UPDATE 金额」。</li>
<li>分摊：整型分到分，末行吃差；落 <code>order_discount_allocation</code>。</li>
<li>长事务：回调里禁调外部 HTTP；先落库再异步。</li>
</ul>""")}
{qa("【线上】部分退分摊差 1 分，财务不签字，根因？",
    ["比例法每次 round 造成误差。落地：按分整数分摊，最后一行 = 总额 - 已分；回退用原分摊行比例或原整型份额。",
     "售后。", "用 double。", "整数分+末行差。", "「钱用整数分，别用乐观近似。」"],
    "found-mysql-q1")}
{reflect("found-mysql-r1")}
</section>
"""

    redis = f"""
<section class="block" id="t-found-redis" data-toc="T-Found-X · Redis掀底板" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>Redis：秒杀预占、过期、热 Key</h2>
{plain("比喻：Redis 像极快的柜台，单线程干活（执行命令），旁边用 IO 多路复用接客；过期像「临期商品」懒删+定期抽查。")}
{c4(
    "秒杀超卖、热 SKU 把一台 Redis 打满、缓存与 DB 不一致导致可卖数为负。",
    "Lua/DECR 原子预占；短 TTL+补偿；热 Key 拆分；缓存不当事务账本。",
    "见掀底板：事件循环、对象编码、过期、持久化与复制。",
    "预占≈支付转化可对上；无长期大 Key。",
    "大促热 Key 带宽打满。",
)}
{floor(
    "事件循环 / 过期 / 结构",
    "主线程 <code>aeProcessEvents</code>：读套接字→命令→执行→写回；过期：惰性删除+activeExpireCycle 抽样。String/ziplist/listpack/hashtable/skiplist 等编码随长度切换。RDB/AOF；主从复制 backlog。",
    "源码认知：<code>server.c</code> processCommand；<code>expire.c</code>；<code>decr</code> 在 <code>t_string.c</code>。<b>集群：</b>CRC16 槽迁移。慢命令 <code>SLOWLOG</code>；<code>INFO commandstats</code>。",
    "用 <code>KEYS *</code> 运维扫键→阻塞→支付读库存全超时；热 SKU 单 Key DECR QPS 打满单核；缓存当账：Redis 丢了但 DB 未补→超卖或少卖。",
    "看：<code>instantaneous_ops_per_sec</code>、blocked、evicted、hot key；业务预占失败率与 DB 对账差。",
)}
{conf("预占 Lua（示意）", """-- KEYS[1]=stock:{sku}  ARGV[1]=qty
local left = redis.call('GET', KEYS[1])
if not left or tonumber(left) < tonumber(ARGV[1]) then return -1 end
return redis.call('DECRBY', KEYS[1], ARGV[1])
-- 成功后发 MQ 落单；超时关单再 INCRBY 补偿（幂等）
""")}
{today("""<ul>
<li>预占成功写 <code>reserve_id</code> 到 DB/Outbox，禁只改 Redis。</li>
<li>热卖 SKU：分桶 <code>stock:sku:{{0..15}}</code> 或本地限流+多副本只读。</li>
<li>禁止生产 <code>KEYS</code>；用 SCAN；大 Key 拆。 </li>
</ul>""")}
{tradeoff("锁 vs 队列削峰", [
    ("Redis 锁短临界区", "互斥", "锁粒度大易崩", "中", "库存片段更新"),
    ("队列削峰+单消费者改库存", "平滑", "延迟", "中", "<b>大促下单</b>"),
    ("DB 乐观锁", "准", "热点差", "低", "平峰"),
])}
{qa("【线上】Redis 内存突然满，淘汰了预占 Key，后果？",
    ["预占真相丢失→可能超卖或无法释放。预占必须以 DB/订单状态可重建；Redis 只加速。设 maxmemory 策略勿对库存键乱 LRU。",
     "大促。", "全信 Redis。", "可重建设计。", "「缓存可丢，账不能只活在缓存。」"],
    "found-redis-q1")}
{reflect("found-redis-r1")}
</section>
"""

    kafka = f"""
<section class="block" id="t-found-kafka" data-toc="T-Found-X · Kafka掀底板" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>Kafka：高吞吐事件、对账流、分区有序</h2>
{plain("比喻：分区像高速公路车道，同 orderId 固定车道才保序；ISR 像「还跟得上队长的跟车队」，掉队太多就降可靠。")}
{c4(
    "轨迹/日志/对账流要扛量大；同一订单事件希望分区内有序。",
    "Key=orderId；acks=all；消费者手动提交+幂等；滞后告警。",
    "见掀底板：日志分段、副本、ISR、消费者位移。",
    "lag 可控；重复消费不双记账。",
    "突发流量靠分区并行。",
)}
{floor(
    "分区日志 / ISR / 消费",
    "Partition=有序 append log（segment 文件）；Leader 写，Follower 拉；ISR=同步副本集合；HW/LEO 控制可见性。<code>acks=all</code> 等 ISR 达标。消费者 offset 存群组协调（__consumer_offsets）。",
    "路径认知：Producer → <code>RecordAccumulator</code> → 网络 → <code>ReplicaManager</code> append；Consumer <code>poll</code>→处理→<code>commitSync</code>。看 <code>under_replicated_partitions</code>、<code>isr_shrinks</code>。",
    "支付成功事件用随机分区→同单乱序，OMS 先见取消后见支付；消费者自动提交→处理失败丢位移→漏单或重复看业务幂等。",
    "看：ISR、URP、consumer lag、生产 <code>error-rate</code>；业务 Inbox 命中率。",
)}
{today("""<ul>
<li>订单域关键事件：<code>key=orderId</code>；消费端 Inbox 表去重。</li>
<li>交易核心若要事务消息语义，中厂常 <b>Outbox+Kafka</b> 或直接 RocketMQ 事务消息（见矩阵）。</li>
<li>lag&gt;阈值告警，先扩消费者再查慢处理。</li>
</ul>""")}
{reflect("found-kafka-r1")}
</section>
"""

    rabbit = f"""
<section class="block" id="t-found-rabbit" data-toc="T-Found-X · RabbitMQ掀底板" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>RabbitMQ：中厂轻量异步与重试</h2>
{plain("比喻：交换机像邮局分拣口（direct/topic/fanout），队列像信箱；镜像/仲裁队列决定信箱掉不掉。")}
{c4(
    "中小流量异步通知、简单重试；别扛日志洪峰。",
    "持久化队列+发布确认；消费手动 ack；失败进死信；幂等。",
    "见掀底板：AMQP 信道、队列索引、确认。",
    "无丢通知、死信可回放。",
    "堆积时内存/磁盘告警。",
)}
{floor(
    "AMQP 与确认",
    "Connection/Channel；消息进 queue（可持久化）；publisher confirm；consumer ack/nack/requeue。经典队列镜像 vs Quorum（Raft）。",
    "路径：Channel.basicPublish → 路由到 queue → basicConsume 回调；未 ack 堆积→prefetch 调控。管理台看 Ready/Unacked。",
    "售后通知短信：自动 ack 放在业务成功前→一异常就丢通知；requeue 无上限→毒消息刷屏。",
    "看：Unacked、DLX 长度、节点磁盘；业务通知到达率。",
)}
{today("""<ul>
<li>prefetch 设合理（如 20）；业务成功再 ack。</li>
<li>毒消息：nack 不 requeue → DLX → 人工。</li>
<li>流量上来评估迁 Kafka/RocketMQ，别垂直硬撑。</li>
</ul>""")}
{reflect("found-rabbit-r1")}
</section>
"""

    rocket = f"""
<section class="block" id="t-found-rocket" data-toc="T-Found-X · RocketMQ掀底板" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>RocketMQ：订单事务消息、延时关单</h2>
{plain("比喻：CommitLog 像一本总流水账，ConsumeQueue 像按主题建的目录；事务消息像「先记草稿，半消息，本地事务成功再转正」。")}
{c4(
    "支付成功必达 OMS；30 分钟未支付关单释放库存。",
    "事务消息或 Outbox；延时消息关单；消费幂等。",
    "见掀底板：CommitLog/ConsumeQueue、事务半消息、刷盘复制。",
    "支付≈OMS；关单不误杀已支付。",
    "发送失败可查询回查。",
)}
{floor(
    "CommitLog / 半消息",
    "所有主题消息顺序追加 CommitLog；ConsumeQueue 存偏移索引。事务：Half 消息对消费不可见→本地事务→Commit/Rollback；Broker 回查 Producer。<code>TransactionListener</code>。复制：同步/异步双写；刷盘 SYNC/ASYNC。",
    "路径：<code>TransactionMQProducer</code> → half → <code>executeLocalTransaction</code> → commit；消费 <code>MessageListenerConcurrently</code>。刷盘/复制看 Broker 配置与发送 RT。",
    "本地事务成功但 commit 丢→靠回查；回查实现错误把已支付判回滚→OMS 永不到。延时关单消息乱，已支付被关→需状态机守卫。",
    "看：半消息堆积、发送失败、消费重试 %DLQ%；业务支付与 OMS 差账。",
)}
{conf("本地事务+关单守卫（示意）", """// 关单消费者
if (order.status == PAID || order.status == CLOSED) return SUCCESS; // 幂等
if (order.status == CREATED) markClosedAndReleaseStock();
""")}
{today("""<ul>
<li>支付→OMS：优先事务消息或 Outbox，二选一写清 ADR。</li>
<li>回查方法必须能根据 orderId 真实查库，禁写死 UNKNOWN。</li>
<li>DLQ 必告警+可重放工具。</li>
</ul>""")}
{qa("【线上】事务消息回查一直 UNKNOWN，会发生什么？",
    ["半消息长期不转正，OMS 收不到；Broker 反复回查打 Producer。修回查逻辑对终态返回 Commit/Rollback。",
     "支付高峰。", "回查直接抛异常。", "回查单测+指标。", "「回查是事务消息的命门。」"],
    "found-rocket-q1")}
""" + boost_found_rocket() + f"""
{reflect("found-rocket-r1")}
</section>
"""

    matrix = f"""
<section class="block" id="t-found-matrix" data-toc="T-Found-X · 选型与类比矩阵" data-prio="p0">
  <h2><span class="sys-id">T-Found-X</span>类比表 + 方案选型矩阵（服务落地，不炫博学）</h2>
  <h3 id="found-analogy">组件间类比（选型用）</h3>
  <table>
    <thead><tr><th>对比</th><th>人话</th><th>订单域怎么选</th></tr></thead>
    <tbody>
      <tr><td>缓存 vs DB</td><td>柜台小票 vs 会计总账</td><td>预占可走 Redis，钱与状态以 DB 为准</td></tr>
      <tr><td>锁 vs 队列削峰</td><td>门口拦人 vs 发号排队</td><td>秒杀下单优先队列/限流，锁只护短更新</td></tr>
      <tr><td>Kafka vs RocketMQ vs Rabbit</td><td>高速日志车道 vs 交易快递仓 vs 小区邮局</td><td>见下表</td></tr>
      <tr><td>Redis 锁 vs DB 乐观锁</td><td>门口保安 vs 改账时核对版本</td><td>跨服务互斥短临界用 Redis；行级状态用 DB</td></tr>
    </tbody>
  </table>
  <h3 id="found-mq-matrix">三种 MQ 选型矩阵</h3>
  <table>
    <thead><tr><th>问题</th><th>Kafka</th><th>RocketMQ</th><th>RabbitMQ</th><th>推荐</th></tr></thead>
    <tbody>
      <tr><td>支付成功→OMS 可靠</td><td>Outbox+自建</td><td>事务消息香</td><td>小流量可</td><td><b>RocketMQ 或 Outbox+Kafka</b></td></tr>
      <tr><td>延时关单</td><td>需额外</td><td>延时级别/定时</td><td>插件/TTL</td><td><b>RocketMQ</b></td></tr>
      <tr><td>日志/轨迹海量</td><td>最强</td><td>可</td><td>弱</td><td><b>Kafka</b></td></tr>
      <tr><td>中厂轻量通知</td><td>重</td><td>中</td><td>轻</td><td><b>Rabbit 起步</b></td></tr>
      <tr><td>分区有序</td><td>Key 分区</td><td>顺序消息</td><td>单队列</td><td>按已有中间件</td></tr>
    </tbody>
  </table>
  <h3 id="found-lock-matrix">锁 / 一致性方案矩阵</h3>
  <table>
    <thead><tr><th>问题</th><th>方案 A</th><th>方案 B</th><th>怎么选</th></tr></thead>
    <tbody>
      <tr><td>防重复支付回调</td><td>DB 唯一键</td><td>Redis SETNX</td><td><b>DB 唯一键托底</b>，Redis 仅加速</td></tr>
      <tr><td>库存预占</td><td>Redis DECR</td><td>DB 条件更新</td><td>秒杀 Redis+补偿；平峰 DB 也可</td></tr>
      <tr><td>防并发退两次</td><td>状态机条件更新</td><td>分布式锁</td><td><b>状态机+唯一退款单</b>，锁可选</td></tr>
      <tr><td>跨库支付→OMS</td><td>Outbox</td><td>Seata AT</td><td>中厂 <b>Outbox</b></td></tr>
    </tbody>
  </table>
{ban("<ul><li>「统一上 Kafka」却不会做业务幂等</li><li>用 JVM 锁解决多实例库存</li><li>把 Redis 当唯一账本</li></ul>")}
{checklist("基础件落地总清单", [
    "JVM：堆与 limit 对齐，GC 日志开，支付池隔离",
    "JUC：有界队列，禁 CachedThreadPool 上回调",
    "MySQL：幂等唯一键+条件更新，分摊整数分",
    "Redis：Lua 预占可重建，禁 KEYS",
    "MQ：Inbox 去重，lag/DLQ 告警，关单状态守卫",
    "矩阵：每种选型写一句「为何不选另一个」进 ADR",
])}
{qa("【题】面试问 Kafka 和 RocketMQ 区别，如何「线上怎么做」回答？",
    ["我们支付→OMS 用 RocketMQ 事务消息/Outbox，因为要半消息回查；轨迹流用 Kafka 扛量。不是背吞吐数字，而是讲 CommitLog/半消息如何避免付了没单。",
     "选型会。", "只背官网对比表。", "挂差账指标。", "「用事故链路讲底板。」"],
    "found-mx-q1")}
{reflect("found-mx-r1")}
</section>
"""
    return hub + jvm + juc + mysql + redis + kafka + rabbit + rocket + matrix
