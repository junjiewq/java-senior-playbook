# -*- coding: utf-8 -*-
"""大数据百科（全）"""
from ency_factory import sec, deep
from helpers import plain, qa, koujue, reflect


def build() -> str:
    parts = []
    parts.append(sec(
        "ency-bd", "ENCY-BD · 大数据总图", "ENCY-BD", "大数据百科总图",
        deep(
            plain_txt="人话：大数据不是另起炉灶炫技——是给交易/售后提供「看得见的指标与可回放的事实」。",
            biz="经营指标准、实时可控、合规可追溯。",
            impl="数仓分层+同步+计算引擎+OLAP+治理。",
            principle="批流一体是产品能力，落地仍要分层与口径。",
            substance="指标时效、口径一致性、任务失败可觉察。",
            mermaid_id="diag-ency-bd-map",
            mermaid_code="""flowchart LR
  OLTP[交易库] --> Sync[CDC同步]
  Sync --> ODS[ODS]
  ODS --> DWD[DWD]
  DWD --> DWS[DWS]
  DWS --> ADS[ADS指标]
  Sync --> Stream[Flink实时]
  Stream --> ADS
  ADS --> App[看板/画像/风控]
""",
            today_html="<ul><li>指标口径文档与任务同发。</li><li>实时与离线对账。</li></ul>",
            reflect_id="ency-bd-hub-r1",
            koujue_txt="大数据口诀：口径先于引擎，分层先于堆表。",
            spine_pos="数据侧服务交易复盘与风控画像。",
            serves="指标/画像/实时售后",
            back="B0 → 本百科 → 经营会",
        ),
    ))
    topics = [
        ("ency-bd-dw", "ENCY-BD · 数仓分层", "ENCY-BD-DW", "数仓分层与批流一体落地", {
            "plain_txt": "比喻：ODS 是原料区，DWD 是洗净切好，DWS 是半成品，ADS 是装盘上桌的指标。",
            "biz": "同一「支付成功率」口径上下一致。",
            "impl": "分层规范；主题域（交易/售后/流量）；批流共用语义层。",
            "principle": "明细可重放；汇总可回刷；实时是加速不是第二口径。",
            "substance": "口径冲突工单↓；任务血缘清晰。",
            "mermaid_id": "diag-ency-bd-dw",
            "mermaid_code": """flowchart TD
  ODS --> DWD
  DWD --> DWS
  DWS --> ADS
  Stream[实时] --> ADS
  Batch[离线] --> ADS
  ADS --> Recon[实时vs离线对账]
""",
            "today_html": "<ul><li>禁止报表直连 OLTP。</li><li>ADS 指标注册制。</li></ul>",
            "qas": [("【冲突】实时与 T+1 不一致？", ["对账窗口+以离线校准+查延迟。", "经营会。", "改实时讨好。", "对账。", "「先对账再吵。」"], "ency-bd-dw-q1")],
            "reflect_id": "ency-bd-dw-r1",
            "koujue_txt": "分层口诀：原料洗净半成品装盘。",
            "floor_title": "语义层",
            "structure": "统一维度（用户/商品/渠道）；事实表粒度。",
            "source_path": "模型设计→ETL→质量校验。",
            "online": "粒度混用导致重复计算 GMV。",
            "verify": "质量规则；复算。",
        }),
        ("ency-bd-hadoop", "ENCY-BD · Hadoop", "ENCY-BD-HADOOP", "Hadoop / HDFS / YARN：要什么、何时不用", {
            "plain_txt": "人话：HDFS 是大仓库货架，YARN 是车间调度；云上对象存储+弹性计算常替代「自建一整套」。",
            "biz": "海量历史订单明细低成本存。",
            "impl": "冷数据进对象存储/HDFS；计算用 Spark on YARN/K8s。",
            "principle": "块复制；NameNode；容器调度资源。",
            "substance": "存储成本；小文件治理。",
            "mermaid_id": "diag-ency-bd-hadoop",
            "mermaid_code": """flowchart TD
  Client --> NN[NameNode]
  Client --> DN[DataNodes]
  App --> YARN[YARN/RM]
  YARN --> NM[NodeManager]
""",
            "trade_title": "何时不用自建 Hadoop",
            "trade_rows": [
                ("数据<几十 TB 且云仓可用", "—", "—", "低", "<b>优先云数仓/对象存储</b>"),
                ("强监管本地化", "—", "—", "高", "可自建/一体机"),
                ("只要 SQL 分析", "—", "—", "中", "直接 OLAP/仓"),
            ],
            "today_html": "<ul><li>小文件合并；生命周期冷热。</li></ul>",
            "qas": [("【选型】中厂要不要自建？", ["多数不需要完整 Hadoop；要存算与治理。", "评审。", "跟风。", "云优先。", "「先问治理再问集群。」"], "ency-bd-hadoop-q1")],
            "reflect_id": "ency-bd-hadoop-r1",
            "koujue_txt": "Hadoop 口诀：大文件友好，小文件要命，云常可替。",
        }),
        ("ency-bd-spark", "ENCY-BD · Spark", "ENCY-BD-SPARK", "Spark：RDD / DataFrame / 作业调优", {
            "plain_txt": "比喻：RDD 是弹性分布式数据集说明书；DataFrame 是带 schema 的表格优化器入口。",
            "biz": "日批对账、分摊复算、画像离线特征。",
            "impl": "DF/SQL 优先；分区倾斜治理；AQE。",
            "principle": "窄依赖宽依赖；Shuffle；Catalyst/Tungsten。",
            "substance": "作业 SLA；失败可重跑。",
            "mermaid_id": "diag-ency-bd-spark",
            "mermaid_code": """flowchart TD
  Read[读ODS/DWD] --> Trans[转换]
  Trans --> Shuffle{宽依赖?}
  Shuffle -->|是| Ex[Exchange Shuffle]
  Shuffle -->|否| Narrow[流水线]
  Ex --> Write[写DWS/ADS]
""",
            "mermaid_id2": "diag-ency-bd-spark-tune",
            "mermaid_code2": """flowchart TD
  Slow[作业慢] --> Skew[查倾斜]
  Slow --> Scan[查扫描量]
  Skew --> Salt[加盐/两阶段聚合]
  Scan --> Part[分区裁剪/列裁剪]
""",
            "today_html": "<ul><li>对账作业幂等覆盖写。</li><li>大表 join 广播小表。</li></ul>",
            "qas": [("【倾斜】某店铺订单爆？", ["加盐或单独处理热点键。", "批处理。", "加机器硬顶。", "倾斜治理。", "「热点要拆开。」"], "ency-bd-spark-q1")],
            "reflect_id": "ency-bd-spark-r1",
            "koujue_txt": "Spark 口诀：DF 优先，盯 Shuffle，治倾斜。",
            "floor_title": "Shuffle",
            "structure": "map 输出分区；reduce 拉取；落盘。",
            "source_path": "Stage 边界=宽依赖；Spark UI 看 Shuffle Read。",
            "online": "OOM 在 shuffle 文件。",
            "verify": "Spark UI Stages。",
        }),
        ("ency-bd-flink", "ENCY-BD · Flink", "ENCY-BD-FLINK", "Flink：流式 · Checkpoint · 订单实时", {
            "plain_txt": "比喻：Flink 是流水线传送带；Checkpoint 是定期拍照，出事从照片续上。",
            "biz": "实时支付成功量、售后风险、库存卖点。",
            "impl": "Kafka→Flink→指标/画像；恰好一次语义靠 checkpoint+sink 幂等。",
            "principle": "Barrier 对齐；状态后端；水位线乱序。",
            "substance": "端到端延迟；状态大小；恰好一次可证。",
            "mermaid_id": "diag-ency-bd-flink",
            "mermaid_code": """flowchart LR
  Kafka[订单事件] --> Flink
  Flink --> CK[Checkpoint]
  Flink --> Sink[指标/告警/画像]
  CK --> State[(StateBackend)]
""",
            "mermaid_id2": "diag-ency-bd-flink-order",
            "mermaid_code2": """sequenceDiagram
  participant O as 订单
  participant K as Kafka
  participant F as Flink
  participant M as 实时大盘
  O->>K: OrderPaid
  K->>F: 消费
  F->>F: 窗口聚合
  F->>M: 支付成功率
""",
            "today_html": "<ul><li>sink 幂等（upsert）；水位线按业务事件时间。</li></ul>",
            "qas": [("【重复】checkpoint 恢复重复写？", ["sink 幂等/事务 sink。", "实时。", "只加并行。", "幂等键。", "「恰好一次靠两端。」"], "ency-bd-flink-q1")],
            "reflect_id": "ency-bd-flink-r1",
            "koujue_txt": "Flink 口诀：事件时间，Checkpoint，Sink 幂等。",
            "floor_title": "Checkpoint",
            "structure": "注入 barrier→对齐→快照状态→ack。",
            "source_path": "CheckpointCoordinator；KeyedState。",
            "online": "反压导致 CK 超时。",
            "verify": "CK 时长；反压指标。",
        }),
        ("ency-bd-olap", "ENCY-BD · OLAP选型", "ENCY-BD-OLAP", "Hive / Iceberg / ClickHouse / Doris 选型", {
            "plain_txt": "人话：Hive 老仓管家；Iceberg 表格式治乱；CK/Doris 是分析加速器。",
            "biz": "分析师秒级看板 vs 批量治理。",
            "impl": "见对照表；明细 Iceberg/仓；看板 CK/Doris。",
            "principle": "表格式 vs 引擎；列存；物化视图。",
            "substance": "查询 P95；存储成本；新鲜度。",
            "extra_html": """  <h4>OLAP 选型类比</h4>
  <table>
    <thead><tr><th>组件</th><th>角色</th><th>优势</th><th>代价</th><th>交易侧用法</th></tr></thead>
    <tbody>
      <tr><td>Hive</td><td>批 SQL 入口</td><td>生态熟</td><td>延迟高</td><td>T+1 重报</td></tr>
      <tr><td>Iceberg</td><td>表格式</td><td>ACID/时光旅行/演进</td><td>要引擎支持</td><td>明细湖仓</td></tr>
      <tr><td>ClickHouse</td><td>列存 OLAP</td><td>宽表聚合猛</td><td>更新弱</td><td>行为/日志分析</td></tr>
      <tr><td>Doris/StarRocks</td><td>实时数仓</td><td>高并发点查+分析</td><td>运维</td><td>经营看板</td></tr>
    </tbody>
  </table>
""",
            "mermaid_id": "diag-ency-bd-olap",
            "mermaid_code": """flowchart TD
  Lake[Iceberg明细] --> Batch[Spark/Hive]
  Lake --> Serve[Doris/CK]
  Serve --> BI[看板]
""",
            "today_html": "<ul><li>更新频繁的订单态别硬塞 CK 当主。</li></ul>",
            "qas": [("【选型】售后专题看板？", ["Doris/SR 或 CK 宽表；明细留 Iceberg。", "分析。", "全上 Hive。", "分层。", "「看板要加速器。」"], "ency-bd-olap-q1")],
            "reflect_id": "ency-bd-olap-r1",
            "koujue_txt": "OLAP 口诀：湖管明细，仓管口径，引擎管加速。",
        }),
        ("ency-bd-sync", "ENCY-BD · 数据同步", "ENCY-BD-SYNC", "同步：Canal / Debezium / Kafka Connect", {
            "plain_txt": "比喻：CDC 是「数据库的行车记录仪转播」——把变更送到总线。",
            "biz": "订单变更近实时进仓/搜索/风控。",
            "impl": "binlog→Canal/Debezium→Kafka→消费者；Schema 演进。",
            "principle": "位点；恰好一次难；要幂等消费。",
            "substance": "延迟；丢改可测；表结构兼容。",
            "mermaid_id": "diag-ency-bd-sync",
            "mermaid_code": """flowchart LR
  MySQL[(Binlog)] --> CDC[Canal/Debezium]
  CDC --> Kafka
  Kafka --> ES
  Kafka --> Flink
  Kafka --> DW[数仓]
""",
            "today_html": "<ul><li>消费幂等；DDL 变更流程。</li><li>敏感字段脱敏。</li></ul>",
            "qas": [("【对照】Canal vs Debezium？", ["都做 CDC；生态/部署差异；选团队熟+可运维。", "同步。", "迷信品牌。", "试点。", "「位点与幂等最重要。」"], "ency-bd-sync-q1")],
            "reflect_id": "ency-bd-sync-r1",
            "koujue_txt": "CDC 口诀：位点可续，消费幂等，DDL 有流程。",
            "floor_title": "位点",
            "structure": "binlog filename+pos 或 GTID；Kafka offset。",
            "source_path": "连接器→解析→发事件。",
            "online": "位点回退重复；或跳过丢数。",
            "verify": "行数对账；延迟监控。",
        }),
        ("ency-bd-metric", "ENCY-BD · 指标画像", "ENCY-BD-METRIC", "指标与画像对交易/售后的支撑", {
            "plain_txt": "人话：指标告诉老板「卖得怎样」；画像告诉风控/营销「这人怎样」——都要挂回单据可解释。",
            "biz": "GMV/支付成功率/退款率/履约时效；用户风险分。",
            "impl": "指标平台注册；画像特征离线+实时；反哺风控与推荐（合规）。",
            "principle": "原子指标→派生；维度退化；特征点-in-time 防穿越。",
            "substance": "口径争议↓；特征穿越事故=0。",
            "mermaid_id": "diag-ency-bd-metric",
            "mermaid_code": """flowchart TD
  Fact[交易事实] --> Atomic[原子指标]
  Atomic --> Derived[派生:成功率]
  Feat[特征] --> Risk[风控]
  Feat --> Mkt[营销]
  Derived --> Board[经营看板]
""",
            "today_html": "<ul><li>退款率分母定义写死。</li><li>特征训练用历史快照。</li></ul>",
            "qas": [("【穿越】画像用了未来售后标签？", ["点-in-time 校正；重训。", "模型。", "忽略。", "时间旅行校验。", "「特征不能偷看未来。」"], "ency-bd-metric-q1")],
            "reflect_id": "ency-bd-metric-r1",
            "koujue_txt": "指标口诀：原子可复用，画像防穿越。",
        }),
        ("ency-bd-gov", "ENCY-BD · 数据治理", "ENCY-BD-GOV", "治理：质量 / 血缘 / 权限 / 成本", {
            "plain_txt": "比喻：治理是图书馆规则——谁能看、书从哪来、坏了怎么修、电费谁出。",
            "biz": "数据可信、可审计、成本可控。",
            "impl": "质量规则；血缘；列级权限；生命周期。",
            "principle": "生产者责任制；SLO 于数据集。",
            "substance": "质检覆盖；成本单位指标。",
            "mermaid_id": "diag-ency-bd-gov",
            "mermaid_code": """flowchart TD
  Prod[数据产品] --> Qual[质量门禁]
  Prod --> Lineage[血缘]
  Prod --> ACL[权限]
  Prod --> Cost[成本]
""",
            "today_html": "<ul><li>ADS 发布过质量门。</li></ul>",
            "qas": [("【成本】小文件+常全扫？", ["合并+分区+列裁剪+生命周期。", "账单。", "加集群。", "治数据。", "「先治表再加机器。」"], "ency-bd-gov-q1")],
            "reflect_id": "ency-bd-gov-r1",
            "koujue_txt": "治理口诀：质量门禁，血缘可追，权限最小。",
        }),
    ]
    for sid, toc, sys_id, title, kw in topics:
        kw.setdefault("spine_pos", "大数据服务交易指标与画像。")
        kw.setdefault("serves", "经营/风控/售后分析")
        kw.setdefault("back", "ENCY-BD → 本叶")
        parts.append(sec(sid, toc, sys_id, title, deep(**kw)))
    return "\n".join(parts)
