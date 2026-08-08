# -*- coding: utf-8 -*-
"""FULLMAP HARD GATE · RocketMQ / Kafka / RabbitMQ"""
from ency_fullbar import gated_entry
from helpers import plain, spine, mermaid, reflect, koujue


def _hub():
    return f"""
<section class="block" id="ency-fm" data-toc="ENCY-FM · 全貌HARD GATE总图" data-prio="p0" data-tags="fullmap hub audit">
  <h2><span class="sys-id">ENCY-FM</span>全貌 HARD GATE 专章（可审计）</h2>
{spine("本专章条目按硬门槛交付；未达标条目不进本区。前序偏侧面百科可交叉，以本区为准。",
       serves="生产选型与排障", back="ENCY → ENCY-FM-*")}
{plain("质量条：原理+源码路径 → 双公司案例(坑+解) → 全链路串起来 → Runbook → 题库。RocketMQ 金标：CommitLog/ConsumeQueue/刷盘/复制/顺序哈希/死信/事务只是一块/堆积监控/金融vs电商。")}
  <table>
    <thead><tr><th>条目</th><th>锚点</th><th>门禁</th></tr></thead>
    <tbody>
      <tr><td>RocketMQ</td><td><a href="#ency-fm-rocket">#ency-fm-rocket</a></td><td>PASS（金标）</td></tr>
      <tr><td>Kafka</td><td><a href="#ency-fm-kafka">#ency-fm-kafka</a></td><td>PASS</td></tr>
      <tr><td>RabbitMQ</td><td><a href="#ency-fm-rabbit">#ency-fm-rabbit</a></td><td>PASS</td></tr>
      <tr><td>Redis</td><td><a href="#ency-fm-redis">#ency-fm-redis</a></td><td>PASS</td></tr>
      <tr><td>MySQL</td><td><a href="#ency-fm-mysql">#ency-fm-mysql</a></td><td>PASS</td></tr>
      <tr><td>PolarDB/Gauss/达梦/TDSQL</td><td><a href="#ency-fm-polardb">#ency-fm-polardb</a>…</td><td>PASS</td></tr>
      <tr><td>JVM/JUC/Spring</td><td><a href="#ency-fm-jvm">#ency-fm-jvm</a>…</td><td>PASS</td></tr>
      <tr><td>Spark/Flink</td><td><a href="#ency-fm-spark">#ency-fm-spark</a>…</td><td>PASS</td></tr>
    </tbody>
  </table>
{mermaid("diag-ency-fm-hub", "flowchart TB\n  FM[ENCY-FM HARD GATE] --> MQ[Rocket/Kafka/Rabbit]\n  FM --> ST[Redis/MySQL/分布式库]\n  FM --> RT[JVM/JUC/Spring]\n  FM --> BD[Spark/Flink]\n")}
{koujue("门禁口诀：无源码不进门，无双案例不进门，无全链路不进门。")}
{reflect("ency-fm-hub-r1")}
</section>
"""


def rocket():
    chain = """
  <h4 id="ency-fm-rocket-storage">5.1 底层存储：CommitLog / ConsumeQueue / IndexFile</h4>
  <p>消息体顺序追加 <b>CommitLog</b>（顺序写吞吐）；按 Topic-Queue 建 <b>ConsumeQueue</b>（物理偏移+大小+TagHash）供消费检索；
  <b>IndexFile</b> 按 Key/时间哈希检索。消费只扫 ConsumeQueue，再回 CommitLog 读体。</p>
  <h4 id="ency-fm-rocket-flush">5.2 刷盘：同步 / 异步与丢消息权衡</h4>
  <p><code>flushDiskType=SYNC_FLUSH</code>：落盘成功才返回，延迟高、丢消息窗口极小（机器炸盘仍可能）。
  <code>ASYNC_FLUSH</code>：写入 PageCache 即返回，靠刷盘线程；宕机丢 PageCache 未刷部分。
  生产：金融核心倾向同步刷盘+同步复制；电商峰值常异步刷盘+同步/异步复制组合，用业务幂等兜底。</p>
  <h4 id="ency-fm-rocket-ha">5.3 主从复制与故障切换</h4>
  <p>经典主从：<code>brokerRole=SYNC_MASTER/ASYNC_MASTER</code> + Slave；或 <b>DLedger/Raft</b> 多数派选主。
  切换注意：未同步完成时异步复制可能丢尾部；切换后生产者感知 NameServer/路由刷新；消费位点在 Broker 侧按组保存，要核对断点。</p>
  <h4 id="ency-fm-rocket-order">5.4 顺序消息：哈希路由到队列</h4>
  <p>业务键（如 <code>orderId</code>）哈希到同一 MessageQueue，顺序消费者单线程消费该队列。
  坑：键倾斜（爆款店铺）→ 单队列热点；全局顺序不可用。金融流水常按账户ID；电商履约按订单ID。</p>
  <h4 id="ency-fm-rocket-dlq">5.5 重试 + 死信闭环（怎么修数据）</h4>
  <p>失败→重试 Topic（延时级别）→超限进入 <code>%DLQ%ConsumerGroup</code>。
  <b>业务闭环：</b>DLQ 告警→工单→查幂等键/单据态→人工/脚本补执行或补偿→标记 DLQ 已处理；禁止无审计重放。</p>
  <h4 id="ency-fm-rocket-tx">5.6 事务消息（只是一块）</h4>
  <p>半消息→本地事务→Commit/Rollback→回查。与 Outbox 二选一写清边界；不能代替消费幂等。</p>
  <h4 id="ency-fm-rocket-lag">5.7 堆积治理 / 位点 / 监控</h4>
  <p>指标：发送 RT/失败、Broker 磁盘与 PageCache、消费 diff、重试/DLQ 速率、半消息数。
  治理：扩消费者→降慢依赖→临时降级非核心→修后补；禁盲丢。</p>
  <h4 id="ency-fm-rocket-fin-ecom">5.8 金融 vs 电商 vs 物流差异小结</h4>
  <table>
    <thead><tr><th>维度</th><th>金融（招行类取向）</th><th>电商（阿里/拼多多类取向）</th><th>物流（顺丰类取向）</th></tr></thead>
    <tbody>
      <tr><td>刷盘/复制</td><td>SYNC_FLUSH + 同步复制/DLedger</td><td>ASYNC_FLUSH + 同步复制常见</td><td>常异步刷盘；轨迹可至少一次</td></tr>
      <tr><td>语义</td><td>可解释、回查、对账强</td><td>吞吐+业务幂等</td><td>最终一致+upsert</td></tr>
      <tr><td>顺序</td><td>账户维</td><td>订单维</td><td>运单号维</td></tr>
      <tr><td>死信</td><td>强制人工+审计</td><td>有限重试+死信台</td><td>轨迹可跳过坏点并告警</td></tr>
    </tbody>
  </table>
"""
    return gated_entry(
        "ency-fm-rocket", "ENCY-FM · RocketMQ金标全貌", "ENCY-FM-ROCKET",
        "RocketMQ 金标全貌：存储·刷盘·复制·顺序·死信·事务·堆积·金融/电商/物流",
        ["rocketmq", "commitlog", "consumequeue", "flush", "ha", "dlq", "order", "fullmap"],
        plain_txt="<b>开篇即底板：</b>PutMessage 顺序追加 CommitLog，再 dispatch 建 ConsumeQueue；SYNC/ASYNC_FLUSH 与主从复制决定 RPO；顺序靠哈希到队列；失败进重试/%DLQ% 工单修数。事务消息只是全链路中的一块。",
        spine_pos="支付成功后履约、关单、售后补偿的消息底座。",
        serves="下单/支付/履约/售后",
        back="T-Found-Rocket → 本金标",
        caps=[
            ("架构", "NameServer、Broker、Topic/Queue、主从/DLedger", "路由与高可用"),
            ("存储", "CommitLog 顺序写、ConsumeQueue、IndexFile", "吞吐与检索"),
            ("刷盘", "SYNC/ASYNC_FLUSH、与丢消息权衡", "金融/电商配置分叉"),
            ("复制", "同步/异步复制、切换注意点", "RPO"),
            ("收发", "同步/异步/oneway、批量、轨迹", "下单发出"),
            ("消费", "并发 vs 顺序、offset、再平衡", "履约消费"),
            ("顺序", "业务键哈希到队列", "订单内有序"),
            ("重试死信", "延时重试、%DLQ%、修数闭环", "售后补偿"),
            ("事务消息", "半消息/回查（非全部）", "支付原子"),
            ("堆积监控", "diff、磁盘、RT、半消息", "大促"),
            ("场景差异", "金融可靠 vs 电商削峰", "选型"),
        ],
        mmds=[
            ("diag-fm-rocket-arch",
             "flowchart TB\n  Prod --> NS[NameServer]\n  Prod --> Master[Broker Master]\n  Master --> CL[(CommitLog顺序写)]\n  CL --> CQ[(ConsumeQueue索引)]\n  CL --> IDX[(IndexFile)]\n  Master --> Flush{刷盘SYNC/ASYNC}\n  Master --> Slave[Slave/DLedger]\n  Cons --> Master\n"),
            ("diag-fm-rocket-dlq",
             "flowchart TD\n  C[Consumer业务失败] --> R[重试Topic延时]\n  R -->|超限| DLQ[%DLQ%]\n  DLQ --> Alert[告警工单]\n  Alert --> Fix[查单据幂等补执行/补偿]\n  Fix --> Audit[审计关闭DLQ]\n"),
            ("diag-fm-rocket-order",
             "flowchart LR\n  Key[orderId] --> Hash[队列哈希]\n  Hash --> Q0[Queue0]\n  Hash --> Q1[Queue1]\n  Q0 --> OC[顺序消费者单线程]\n"),
        ],
        sources=[
            ("PutMessage → CommitLog",
             "org.apache.rocketmq.store.DefaultMessageStore#putMessage → CommitLog#putMessage / MappedFile.append",
             "// 伪代码：顺序追加\n"
             "MappedFile file = commitLog.getLastMappedFile();\n"
             "file.append(msgBytes); // 顺序写 PageCache/磁盘\n"
             "dispatch to ConsumeQueue(topic, queueId, offset, size, tagHash);\n"
             "if (flushDiskType == SYNC_FLUSH) waitFlush();\n"),
            ("顺序消费选队列",
             "MessageQueueSelector / SelectMessageQueueByHash；顺序消费 ConsumeMessageOrderlyService",
             "// 发送侧保证同键同队列\n"
             "int idx = hash(orderId) % mqList.size();\n"
             "return mqList.get(idx);\n"
             "// 消费侧同队列串行回调\n"),
            ("事务半消息",
             "TransactionMQProducer / TransactionalMessageService",
             "sendMessageInTransaction → prepare(half)\n"
             "→ executeLocalTransaction → commit/rollback\n"
             "→ checkLocalTransaction (回查)\n"),
        ],
        floors=[
            ("存储与可见性",
             "CommitLog 全局顺序写；ConsumeQueue 逻辑队列索引；消费位点 ConsumerOffset 按组+队列。",
             "DefaultMessageStore.putMessage；ReputMessageService 转发构建 ConsumeQueue。",
             "ConsumeQueue  fort 损坏或落后→消费到空洞/重复；需校验与修复工具意识。",
             "看：putMessage 耗时、CommitLog 磁盘、consumeQueue diff。"),
        ],
        chain_html=chain,
        cases=[
            {"id": "ency-fm-rocket-case-ali", "company": "阿里系电商大促（案例归纳）",
             "scene": "大促下单/支付成功后履约事件削峰",
             "land": "ASYNC_FLUSH + SYNC_MASTER；支付/履约分 Topic；orderId 哈希顺序；非核心降级开关。",
             "pit": "同步刷盘+热点顺序队列叠加，发送 RT 升高拖垮下单。",
             "fix": "①链路分级配刷盘 ②热点 key 加盐 ③扩队列与消费者 ④压测带回调。",
             "effect": "公开分享量级/示意区间：大促链路常追求发送 RT 从数百 ms 压回数十 ms 级；堆积 diff 可在扩容后小时级消化（非未公开精确值）。"},
            {"id": "ency-fm-rocket-case-cmb", "company": "招行类金融工程取向（案例归纳）",
             "scene": "账务/渠道结果事件可靠投递与对账",
             "land": "SYNC_FLUSH + 同步复制或 DLedger；半消息/本地事务边界清晰；DLQ 强制人工。",
             "pit": "异步复制主切丢尾→渠道成功本地无单。",
             "fix": "①同步复制/多数派 ②切换演练 ③未知态查证 ④日终对账三针。",
             "effect": "公开分享量级/示意区间：金融侧更强调 RPO≈0 取向与对账闭环率接近 100% 的工程目标（示意，非某行内部精确披露）。"},
            {"id": "ency-fm-rocket-case-sf", "company": "顺丰类物流（案例归纳）",
             "scene": "运单轨迹/节点事件总线",
             "land": "高吞吐 Topic；waybillId 作 key；消费 upsert 轨迹；允许至少一次。",
             "pit": "无 key 乱序；坏消息毒丸卡住顺序队列。",
             "fix": "①强制运单 key ②毒丸进 DLQ 不堵主队列 ③轨迹乱序用序号校正。",
             "effect": "公开分享量级/示意区间：轨迹类常见十万～百万级/日事件（视业务体量示意）；lag 告警分钟级响应。"},
            {"id": "ency-fm-rocket-case-food", "company": "美团/饿了么或餐饮高峰（案例归纳）",
             "scene": "出餐/取消/配送状态异步通知",
             "land": "并发消费主路径；取消令牌幂等；失败有限重试+DLQ。",
             "pit": "无限重试打爆门店/配送下游。",
             "fix": "①maxReconsumeTimes 绑告警 ②DLQ 工单 ③高峰降级非核心推送。",
             "effect": "公开分享量级/示意区间：午餐高峰 QPS 可为平峰数倍～一个数量级（示意）；重试风暴治理后下游错误率显著回落。"},
        ],
        trade_title="RocketMQ vs Kafka vs Rabbit（全维度）",
        trade_rows=[
            ("存储", "CommitLog+CQ", "分区日志段", "队列文件"),
            ("刷盘/副本旋钮", "细（DISK/复制）", "acks/ISR", "persistent+镜像/仲裁"),
            ("事务/延时", "原生强", "事务有边界/延时弱", "TTL/插件"),
            ("顺序", "队列内+哈希", "分区内+key", "单消费者"),
            ("回放", "中", "强", "弱"),
            ("电商核心", "适合", "轨迹/CDC", "通知旁路"),
            ("金融可靠", "适合(配同步)", "适合(配 ISR)", "中小异步"),
        ],
        runbook_title="堆积 / 半消息 / DLQ / 磁盘",
        runbook_html=(
            "<ol>"
            "<li>看 diff、sendRT、disk、DLQ、半事务消息数。</li>"
            "<li>堆积：扩消费者→剖 consumeRT→降级下游→禁删位点。</li>"
            "<li>DLQ：导出消息体→对业务单号→补执行→审计。</li>"
            "<li>主从切换后核对路由与消费断点。</li>"
            "</ol>"
        ),
        fail_html="<ul><li>磁盘满。</li><li>异步复制丢尾。</li><li>顺序热点。</li><li>半消息悬挂。</li></ul>",
        today_html=(
            "<ul>"
            "<li>支付：事务消息或 Outbox + 履约幂等表。</li>"
            "<li>写清刷盘/复制级别进配置库；金融链路与营销链路分级。</li>"
            "<li>DLQ 必须有值班手册。</li>"
            "</ul>"
        ),
        conf_title="生产配置建议（分级示例）",
        conf_code=(
            "# 电商履约常见\n"
            "flushDiskType=ASYNC_FLUSH\n"
            "brokerRole=SYNC_MASTER\n"
            "# 金融核心取向\n"
            "flushDiskType=SYNC_FLUSH\n"
            "brokerRole=SYNC_MASTER  # 或 DLedger 多数派\n"
            "# 发送\n"
            "sendMsgTimeout=3000\n"
            "retryTimesWhenSendFailed=2\n"
        ),
        qas=[
            ("【存储】为何顺序写 CommitLog 还要 ConsumeQueue？",
             ["CommitLog 最大化磁盘顺序写；ConsumeQueue 提供按队列的 O(1) 偏移索引，避免消费扫整个日志。",
              "原理。", "说是两个日志重复。", "画索引关系。", "「账本+目录。」"],
             "fm-rocket-q1"),
            ("【刷盘】SYNC_FLUSH 是否绝对不丢？",
             ["显著降低丢 PageCache 窗口，仍受磁盘损坏/机房灾难约束；需复制与备份。",
              "金融。", "绝对安全。", "分级+演练。", "「同步刷盘≠永生。」"],
             "fm-rocket-q2"),
            ("【死信】DLQ 有消息怎么修售后单？",
             ["定位 afterSaleId→看态机是否可补→幂等补退款/关单→审计关闭 DLQ；禁盲重放打渠道。",
              "售后。", "一键重抛。", "工单闭环。", "「死信是工单不是垃圾桶。」"],
             "fm-rocket-q3"),
            ("【对比】电商大促为何常异步刷盘？",
             ["换吞吐；用同步复制+幂等控资损；核心账务链路单独提级。",
              "大促。", "全局同步刷盘。", "分级。", "「链路分级配可靠性。」"],
             "fm-rocket-q4"),
        ],
        koujue_txt="RocketMQ 金标口诀：CommitLog 顺序写，ConsumeQueue 做目录，刷盘复制分金融电商，死信必进工单。",
        rid="fm-rocket-r1",
    )


def kafka():
    chain = """
  <h4 id="ency-fm-kafka-log">5.1 日志存储：Partition / Segment / Index</h4>
  <p>分区内顺序追加 segment；offset 索引时间索引；保留按时间/大小。回放是一等能力。</p>
  <h4 id="ency-fm-kafka-isr">5.2 副本 ISR / HW / acks 生产配置</h4>
  <p><code>acks=all</code> + <code>min.insync.replicas≥2</code>；ISR 收缩告警；控制器/KRaft 选主。</p>
  <h4 id="ency-fm-kafka-eos">5.3 幂等生产与 EOS 边界</h4>
  <p>enable.idempotence；事务读写 Kafka 内；写 MySQL 仍要业务幂等。</p>
  <h4 id="ency-fm-kafka-cg">5.4 消费者组 / rebalance / lag</h4>
  <p>一分区一消费者；静态成员减风暴；手动提交 offset。</p>
  <h4 id="ency-fm-kafka-connect">5.5 Connect / 调优</h4>
  <p>CDC 入湖；调优副本延迟、页面缓存、网络、生产者批量。</p>
"""
    return gated_entry(
        "ency-fm-kafka", "ENCY-FM · Kafka全貌", "ENCY-FM-KAFKA",
        "Kafka 全貌：日志·ISR·消费者组·EOS 边界·Connect·多场景",
        ["kafka", "isr", "eos", "connect", "fullmap"],
        plain_txt="Kafka=分布式提交日志。分区并行、ISR 耐打、消费者组读进度；恰好一次有边界。",
        spine_pos="轨迹/CDC/对账高吞吐事件。",
        serves="物流轨迹/清结算/画像",
        back="T-Found-Kafka → FULLMAP",
        caps=[
            ("架构", "Broker、KRaft/Controller、Topic、Partition、Segment", "集群"),
            ("副本", "Leader/Follower、ISR、HW/LEO、acks", "不丢"),
            ("生产", "key 分区、压缩、幂等/事务生产", "Outbox 转发"),
            ("消费", "Group、rebalance、offset", "对账消费"),
            ("EOS 边界", "Kafka 内 vs 外储", "账务慎吹"),
            ("生态", "Connect、Streams 边界", "CDC"),
            ("运维", "URP、lag、磁盘倾斜", "值班"),
        ],
        mmds=[
            ("diag-fm-kafka-arch",
             "flowchart TB\n  P[Producer] --> L[Leader]\n  L --> ISR[Followers in ISR]\n  L --> Seg[(Segments)]\n  G[ConsumerGroup] --> L\n"),
            ("diag-fm-kafka-lag",
             "flowchart TD\n  Lag[Consumer Lag] --> Cause{原因}\n  Cause -->|处理慢| Opt[优化/扩容]\n  Cause -->|分区不足| Part[评估扩分区]\n  Cause -->|再均衡风暴| Static[静态成员]\n"),
        ],
        sources=[
            ("生产写入",
             "KafkaProducer.doSend → RecordAccumulator → Sender → Broker ReplicaManager.appendRecords",
             "if (acks==all) wait ISR required replicas\n"
             "update HW for consumer visibility\n"),
            ("消费位移",
             "ConsumerCoordinator / SubscriptionState",
             "poll → process → commitSync(offsets)  // 业务成功后\n"),
        ],
        floors=[
            ("ISR 与可见性",
             "HW 之前对消费可见；LEO 为末端；ISR 缩小影响容错。",
             "ReplicaManager；高水位推进。",
             "acks=1 丢支付事件。",
             "看 UnderReplicatedPartitions、ISR shrink。"),
        ],
        chain_html=chain,
        cases=[
            {"id": "ency-fm-kafka-case-sf", "company": "顺丰类物流（案例归纳）", "scene": "运单轨迹",
             "land": "waybillId 作 key 保序；至少一次+upsert；lag 看板。",
             "pit": "无 key → 轨迹乱序展示。",
             "fix": "强制分区键；消费端序号校正。"},
            {"id": "ency-fm-kafka-case-ali", "company": "阿里系数据总线（案例归纳）", "scene": "CDC/对账流",
             "land": "Connect/Flink 入湖；与 T+1 对账。",
             "pit": "吹 EOS 直接当账本写库导致双记。",
             "fix": "外储幂等；Kafka 事务仅限链路内。"},
        ],
        trade_title="Kafka 定位对照",
        trade_rows=[
            ("回放/流", "最强", "中", "弱"),
            ("延时/事务电商", "弱/有边界", "Rocket 强", "插件"),
            ("运维", "中高", "中", "中低"),
        ],
        runbook_title="URP / Lag / Rebalance",
        runbook_html="<ol><li>URP→磁盘网络 GC。</li><li>Lag→RT 与分区。</li><li>Rebalance→会话与静态成员。</li></ol>",
        fail_html="<ul><li>热点分区。</li><li>自动提交丢偏移。</li></ul>",
        today_html="<ul><li>轨迹用 Kafka；支付事务事件优先 Rocket/Outbox。</li><li>acks=all + min.insync.replicas=2。</li></ul>",
        conf_title="可靠写",
        conf_code="acks=all\nmin.insync.replicas=2\nenable.idempotence=true\nenable.auto.commit=false",
        qas=[
            ("【原理】HW 与 LEO？", ["LEO 末端；HW 可见水位。", "排障。", "混用。", "画图。", "「可见看 HW。」"], "fm-kafka-q1"),
            ("【语义】EOS 写 MySQL？", ["不能只靠 Kafka 事务；要业务幂等。", "对账。", "开事务即可。", "幂等表。", "「EOS 有边界。」"], "fm-kafka-q2"),
            ("【案例】轨迹乱序？", ["key=运单号；同分区。", "物流。", "多分区无键。", "强制 key。", "「有序靠 key。」"], "fm-kafka-q3"),
        ],
        koujue_txt="Kafka 口诀：分区并行，ISR 耐打，外储幂等。",
        rid="fm-kafka-r1",
    )


def rabbit():
    chain = """
  <h4 id="ency-fm-rabbit-ex">5.1 Exchange 类型与绑定</h4>
  <p>direct/topic/fanout/headers；绑定 key 错误会静默无消费。</p>
  <h4 id="ency-fm-rabbit-ha">5.2 持久化 · Confirm/Ack · 仲裁队列</h4>
  <p>persistent + publisher confirm + manual ack；队列类型 quorum（优于老镜像不演练）。</p>
  <h4 id="ency-fm-rabbit-ttl">5.3 TTL / DLX / 堆积流控</h4>
  <p>过期进 DLX；内存高水位 flow control；prefetch 调控 Unacked。</p>
"""
    return gated_entry(
        "ency-fm-rabbit", "ENCY-FM · RabbitMQ全貌", "ENCY-FM-RABBIT",
        "RabbitMQ 全貌：交换·队列·仲裁·TTL/DLX·堆积",
        ["rabbitmq", "quorum", "dlx", "fullmap"],
        plain_txt="Rabbit=路由邮局。交换机分流，队列存消息，仲裁保活，TTL/DLX 处理过期死信。",
        spine_pos="中厂通知与轻量异步。",
        serves="通知/轻补偿",
        back="T-Found-Rabbit → FULLMAP",
        caps=[
            ("模型", "Exchange/Binding/Queue/vhost", "隔离"),
            ("路由", "四类交换机", "事件分发"),
            ("可靠", "confirm、ack、prefetch、persistent", "不丢"),
            ("HA", "quorum/镜像", "节点故障"),
            ("TTL/DLX", "死信闭环", "超时任务"),
            ("流控", "内存水位、队列深度", "高峰"),
        ],
        mmds=[
            ("diag-fm-rabbit-arch",
             "flowchart LR\n  P --> X[Exchange]\n  X --> Q[Queue quorum]\n  Q --> C[Consumer ack]\n  Q --> DLX[DLX]\n"),
            ("diag-fm-rabbit-flow",
             "flowchart TD\n  Mem[内存高水位] --> FC[Flow Control]\n  FC --> Block[生产者阻塞]\n  Block --> Act[扩容/降持久化压力]\n"),
        ],
        sources=[
            ("发布确认",
             "Channel.confirmSelect / waitForConfirms；basicPublish",
             "ch.confirmSelect();\n"
             "ch.basicPublish(ex, key, propsPersistent, body);\n"
             "ch.waitForConfirmsOrDie(timeout);\n"),
            ("消费确认",
             "basicConsume + basicAck/Nack",
             "deliver → biz → basicAck(tag, false)\n"
             "onFailure → basicNack(tag, false, requeue|dlx)\n"),
        ],
        floors=[
            ("Confirm/Ack 语义",
             "confirm=到 Broker；ack=处理完；二者缺一都可能丢。",
             "信道复用；连接泄漏。",
             "自动 ack 崩进程丢售后通知。",
             "看 Unacked、Ack rate、Connections。"),
        ],
        chain_html=chain,
        cases=[
            {"id": "ency-fm-rabbit-case-food", "company": "肯德基/麦当劳类餐饮（案例归纳）", "scene": "出餐通知/取消",
             "land": "topic 路由门店；失败入 DLX；取消幂等。",
             "pit": "自动 ack + 门店系统慢 → 丢通知。",
             "fix": "manual ack；prefetch 限流；DLX 人工补推。"},
            {"id": "ency-fm-rabbit-case-yonyou", "company": "用友类企业集成（案例归纳）", "scene": "B2B 单据异步过账",
             "land": "单据事件入队；ERP 消费者幂等过账。",
             "pit": "无持久化队列节点重启丢单。",
             "fix": "quorum+persistent；confirm。"},
        ],
        trade_title="Rabbit 适用边界",
        trade_rows=[
            ("路由灵活", "优", "中", "中"),
            ("超高吞吐", "弱", "Kafka", "Rocket 中高"),
            ("核心支付", "旁路", "视配置", "更常见"),
        ],
        runbook_title="连接打满 / Unacked / 流控",
        runbook_html="<ol><li>查泄漏连接。</li><li>Unacked→消费者卡死。</li><li>流控→内存与生产者。</li></ol>",
        fail_html="<ul><li>绑错 key。</li><li>非 persistent。</li></ul>",
        today_html="<ul><li>通知用 Rabbit quorum；支付核心用 Rocket/Outbox。</li></ul>",
        conf_title="可靠基线",
        conf_code="publisher confirms=on\nmanual ack=true\nqueue type=quorum\nprefetch=按RT",
        qas=[
            ("【路由】四种 Exchange？", ["direct/topic/fanout/headers 与用例。", "设计。", "只会一种。", "举例。", "「先选路由。」"], "fm-rabbit-q1"),
            ("【HA】为何 quorum？", ["Raft 语义清晰；要演练。", "运维。", "单机。", "演练。", "「HA 要杀节点。」"], "fm-rabbit-q2"),
            ("【排障】Ready=0 无消费？", ["看 Unacked/绑定/DLX。", "值班。", "盲重发。", "查消费者。", "「先看死没死。」"], "fm-rabbit-q3"),
        ],
        koujue_txt="Rabbit 口诀：路由+确认+仲裁，通知友好支付旁路。",
        rid="fm-rabbit-r1",
    )


def build():
    return "\n".join([_hub(), rocket(), kafka(), rabbit()])
