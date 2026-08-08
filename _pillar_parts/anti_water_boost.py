# -*- coding: utf-8 -*-
"""Reusable deep HTML boosters for thin front/pillar sections (anti-water)."""
from helpers import mermaid, floor, today, runbook, failbox, tradeoff, qa, five, company_prd, essence


def two_mmds(prefix: str, a_title: str, a_code: str, b_title: str, b_code: str) -> str:
    return (
        f"  <h4>{a_title}</h4>\n"
        + mermaid(f"diag-{prefix}-a", a_code)
        + f"  <h4>{b_title}</h4>\n"
        + mermaid(f"diag-{prefix}-b", b_code)
    )


def industry_cases(prefix: str, rows: list) -> str:
    """rows: (industry, scene, pick, pit, steps, effect)"""
    out = ['  <h4>跨行业/跨场景落地（案例归纳）</h4>']
    for i, (ind, scene, pick, pit, steps, effect) in enumerate(rows, 1):
        out.append(
            f'  <div class="company-prd" id="{prefix}-ind-{i}">'
            f'<div class="label">Case{i} · {ind}</div>'
            f'<p><b>业务场景：</b>{scene}</p>'
            f'<p><b>技术选型细节：</b>{pick}</p>'
            f'<p><b>具体坑点：</b>{pit}</p>'
            f'<p><b>解决步骤：</b>{steps}</p>'
            f'<p><b>落地效果（公开量级/工程目标）：</b>{effect}</p></div>'
        )
    return "\n".join(out)


def boost_rag() -> str:
    return "\n".join([
        essence(
            "客服/Agent 说的每一句退款口径必须能指回「现行有效知识块」；说错=资损。",
            "怕过期话术、无证据编造、跨版本混用。",
            "分块带元数据(kbVer/生效期/规则域) + 混合检索 + 强制 cite + HITL 金额闸 + 评测回归。",
            "向量相似度不是真理；无 cite / 无版本 = 拒答或转人工。",
            "无门禁→已发货单被承诺未发货秒退全额。",
        ),
        two_mmds(
            "aix-rag",
            "RAG 生产链路（挂售后）",
            "flowchart LR\n  Doc[规则/SOP]-->Chunk[分块+元数据]\n  Chunk-->Embed[向量/BM25]\n  Q[工单问题]-->Ret[检索TopK]\n  Ret-->Filter[版本/生效过滤]\n  Filter-->Rerank[重排]\n  Rerank-->Cite{强制cite?}\n  Cite -->|否| Refuse[拒答/转人工]\n  Cite -->|是| Draft[草稿]\n  Draft-->HITL[人工确认]\n  HITL-->SM[现有退款状态机]",
            "幻觉资损闭环",
            "flowchart TD\n  Bad[过期块入库存]-->Hit[TopK命中]\n  Hit-->Speak[客服照念]\n  Speak-->Loss[多退/错退]\n  Loss-->Audit[审计回放]\n  Audit-->Fix[回滚kbVer+补陷阱题]\n  Fix-->Gate[CI评测门禁]",
        ),
        floor(
            "分块与元数据",
            "块=可引用最小单位；字段至少 docId/kbVer/effectiveFrom/To/domain(售后|优惠|清关)。",
            "ingest pipeline：解析→切段(重叠)→写向量库+元数据索引；查询先 filter 再相似度。",
            "过期块未下线→幻觉承诺；跨域块混检→优惠口径套到清关。",
            "看：cite 命中率、陷阱题通过率、HITL 驳回「无依据」。",
        ),
        today("""<ul>
<li>知识发布单绑定 <code>kbVer</code>；应用配置钉死版本，禁「聊天改产提示」。</li>
<li>Agent 输出 JSON：<code>{answer, cites:[{docId,kbVer,span}], amountAdvice?}</code>；无 cites 前端不展示结论。</li>
<li>金额字段强制 HITL；模型不得调用 refund API。</li>
<li>CI：20 题金标+10 题陷阱+5 题无证据；失败阻断知识晋升。</li>
</ul>"""),
        industry_cases("aix-rag", [
            ("电商售后（阿里/拼多多类取向）", "大促规则周更，客服问「未发货能否秒退」",
             "kbVer 钉大促规则包；强制 cite；金额 HITL",
             "旧「一律全额」块仍在库",
             "①生效期过滤 ②陷阱题回归 ③驳回进负例",
             "工程目标：陷阱题通过率≥95%；错口径工单周环比下降（内部基线，非公开精确值）"),
            ("银行客服旁路（招行类取向）", "理财/渠道话术问答，禁止触账务写",
             "私有化模型+脱敏 MCP 只读查单；话术库双人评审",
             "提示注入藏在工单备注",
             "①工具结果非指令 ②白名单 ③审计回放",
             "工程目标：零自动账务写；注入样本评测全绿"),
            ("餐饮高峰（美团/饿了么类）", "出餐后取消口径与餐损规则",
             "门店态+规则版本联合检索；草稿仅解释不可改态",
             "处理时间窗口话术当事件时间用",
             "①规则带门店态条件 ②HITL ③高峰降级纯人工",
             "工程目标：午餐高峰草稿采纳率上升且餐损错退不增"),
            ("跨境清关（综合电商）", "清关失败能否退税/谁承担运费",
             "清关 SOP 独立 domain；无证据拒答",
             "混入国内售后块",
             "①domain 过滤 ②未知税率不编造 ③转海关专席",
             "工程目标：清关类幻觉拦截可审计"),
        ]),
        tradeoff("同一「售后口径助手」多解法", [
            ("纯 FAQ 检索无 LLM", "低幻觉", "体验硬", "低", "中厂冷启动"),
            ("RAG+强制cite+HITL", "可解释", "中", "中", "<b>推荐生产</b>"),
            ("Agent 自动退款", "快", "资损高", "高", "<b>禁止</b>"),
            ("全人工", "最稳", "人效差", "高人工", "高风险单兜底"),
        ]),
        five(
            "钉：错口径资损=0 的验收句+财务签字。",
            "拆：主=查单解释；异=无证据；逆=金额确认走状态机。",
            "标：过期块、注入、跨版本。",
            "选：元数据过滤+cite+HITL，不选自动写。",
            "验：评测集+审计抽检+错退监控。",
        ),
        qa("【详答】为何「加大 Top-K」往往让幻觉更糟？",
           ["K 大提高旧块/噪声入选概率；无版本过滤时更糟。应先 filter/rerank/cite，再考虑 K。",
            "召回不足投诉。", "只调大 K。", "看 cite 正确率与陷阱题。", "「召回是原料，门禁才是食品安全。」"],
           "aix-rag-deep-q1"),
        qa("【详答】知识库更新如何像发版？",
           ["草稿库→评测→晋升 kbVer→应用钉扎→观察采纳/驳回→可回滚上一版。",
            "运营周更。", "直接覆盖生产索引。", "发布单+回滚演练。", "「知识也有 revision。」"],
           "aix-rag-deep-q2"),
    ])


def boost_mcp() -> str:
    return "\n".join([
        essence(
            "MCP 把「模型能碰什么世界」变成显式工具面；碰错=越权与资损。",
            "怕提示注入、写工具暴露、数据外泄、恶意 Server。",
            "白名单注册 + 鉴权到人/租户 + 结果与系统提示隔离 + 限流审计。",
            "协议通道≠业务授权；用户内容永远不是系统指令。",
            "无白名单→模型被诱使调 refund.create。",
        ),
        two_mmds(
            "aix-mcp",
            "MCP 调用链（订单域）",
            "flowchart TB\n  U[用户/工单]-->Agent\n  Agent-->Policy[策略:白名单/配额]\n  Policy-->MCP[MCP Server]\n  MCP-->T1[order.get 只读]\n  MCP-->T2[ticket.get 只读]\n  MCP -.->|禁止注册| W[refund.create]\n  T1-->Sanitize[脱敏结果]\n  Sanitize-->Agent\n  Agent-->HITL[人工]\n  HITL-->API[现有退款API]",
            "提示注入防御",
            "flowchart TD\n  Note[工单藏指令]-->ToolOut[工具原文]\n  ToolOut-->Isolate[非指令通道]\n  Isolate-->Model[模型]\n  Model-->Guard[输出校验/金额闸]\n  Guard-->Human[HITL]",
        ),
        floor(
            "工具暴露原则",
            "每个工具：名称、入参 schema、鉴权、副作用等级(read/write)、超时、审计字段。",
            "MCP list_tools → call_tool；网关层再鉴权，不信任模型自述。",
            "写工具误注册→资损；错误详情回灌→死循环打爆依赖。",
            "看：工具拒绝次数、写工具调用=0、审计完整率。",
        ),
        industry_cases("aix-mcp", [
            ("电商客服", "查单+草稿", "只读 order/ticket；写在 HITL 后走原 API", "备注注入「批准退款」", "隔离+评测+白名单", "写工具调用持续为 0"),
            ("银行坐席辅助", "只读客户视图", "专有终点+字段级脱敏", "外泄完整证件号", "脱敏+DLP 审计", "抽检零明文外送"),
            ("物流轨迹客服", "运单查询", "waybill.get 限流", "批量爬取", "配额+缓存", "滥用告警可关停租户"),
            ("餐饮门店助手", "菜单/出餐状态只读", "店员身份绑定门店", "跨店越权", "租户隔离测试", "越权用例 CI 红线"),
        ]),
        runbook("疑似 MCP 越权 10 分钟",
                "<ol><li>切断写工具/降级只读。</li><li>拉审计：谁、何工具、何入参。</li><li>冻结相关售后单。</li><li>轮换密钥/下线可疑 Server。</li><li>补评测与白名单 diff。</li></ol>"),
        qa("【详答】MCP 与「函数调用」差在哪？",
           ["MCP 是可插拔工具协议+发现/鉴权面；业务上仍要白名单与副作用分级。别把协议当安全模型。",
            "选型会。", "接通就完事。", "注册表评审。", "「协议解决连接，政策解决敢不敢。」"],
           "aix-mcp-deep-q1"),
    ])


def boost_ai_integrate() -> str:
    return "\n".join([
        two_mmds(
            "aix-int",
            "CI → 知识晋升 → 工单",
            "flowchart LR\n  PR[Skill/KB PR]-->CI[评测+lint]\n  CI -->|红| Block[阻断]\n  CI -->|绿| Promote[晋升kbVer]\n  Promote-->Ticket[工单侧栏草稿]\n  Ticket-->HITL[坐席确认]\n  HITL-->Core[状态机/API]",
            "值班复盘 Agent 边界",
            "flowchart TD\n  Alert[告警]-->Sum[摘要+Runbook链接]\n  Sum-->Human[值班勾选]\n  Human-->Act[回滚/限流/开关]\n  Sum -.->|禁止| Auto[自动执行回滚]",
        ),
        today("""<ul>
<li>CI job：<code>eval_suite</code> + secret scan；失败禁合并知识。</li>
<li>工单插件：只渲染草稿与 cite；确认按钮调现有售后 API。</li>
<li>值班：Agent 输出「建议动作 checklist」，执行权在人。</li>
<li>发布票据：应用版本 ↔ promptVer ↔ kbVer 三联。</li>
</ul>"""),
        industry_cases("aix-int", [
            ("电商大促值班", "告警风暴摘要", "只读复盘 Agent+HITL", "自动关告警掩盖事故", "禁止自动 resolve", "MTTR 不因摘要变差"),
            ("银行变更窗", "知识包与核心发布绑定", "双人审批晋升", "聊天改产提示", "票据三联", "审计可回放"),
        ]),
        five("钉集成验收：评测门禁+零自动写。", "拆 CI/工单/值班/发布四接点。", "标自动执行诱惑。", "选建议态。", "验演练记录。"),
    ])


def boost_found_rocket() -> str:
    return "\n".join([
        floor(
            "CommitLog / ConsumeQueue",
            "体顺序写 CommitLog；ConsumeQueue 是队列视图索引；消费位点按组+队列。",
            "DefaultMessageStore#putMessage → CommitLog#putMessage；Reput 构建 CQ。",
            "CQ 损坏→空洞/重复；业务必须幂等。",
            "put耗时、磁盘、consumeDiff、DLQ。",
        ),
        two_mmds(
            "found-rocket",
            "发送到消费",
            "flowchart LR\n  App-->NS[NameServer]\n  App-->B[Broker]\n  B-->CL[(CommitLog)]\n  CL-->CQ[(ConsumeQueue)]\n  C[Consumer]-->B",
            "支付成功→履约",
            "flowchart TD\n  PayOK-->Outbox-->MQ[RocketMQ]\n  MQ-->OMS\n  Fail-->Retry-->DLQ-->Ticket[工单修数]",
        ),
        industry_cases("found-rocket", [
            ("电商大促", "履约削峰", "ASYNC_FLUSH+SYNC_MASTER；订单键顺序", "热点队列", "加盐/扩队列", "发送 RT 压回可接受区间（公开分享常见目标：数十 ms 级）"),
            ("金融渠道", "结果事件", "SYNC_FLUSH+同步/DLedger", "异步切主丢尾", "演练+对账", "RPO 取向≈0 + 对账闭环"),
            ("物流轨迹", "节点事件", "至少一次+upsert", "无 key 乱序", "运单 key", "乱序可校正"),
            ("餐饮出餐", "状态通知", "有限重试+DLQ", "重试打爆门店", "maxReconsume+降级", "下游错误率回落"),
        ]),
        tradeoff("刷盘/复制", [
            ("SYNC+同步", "RPO 最小", "RT 高", "高", "账务核心"),
            ("ASYNC+同步", "均衡", "掉电丢 PageCache", "中", "履约常见"),
            ("ASYNC+异步", "吞吐", "切主丢尾", "低", "可丢可补旁路"),
        ]),
    ])


def boost_k8s_workload() -> str:
    return "\n".join([
        two_mmds(
            "k8sx-w",
            "订单链路工作负载拆分",
            "flowchart TB\n  GW-->Ord[order-api]\n  GW-->PayCB[pay-callback 独立部署]\n  Ord-->Redis\n  Ord-->DB[(MySQL/Polar)]\n  PayCB-->DB\n  Ord-->OB[Outbox Worker]\n  OB-->MQ-->OMS[oms-api]\n  OMS-->WMS",
            "探针与发布",
            "flowchart LR\n  Ready[readiness 可接客]-->Svc\n  Live[liveness 轻]-->Restart\n  Canary[金丝雀]-->Gate{支付/退款成功率}\n  Gate -->|跌| Rollback\n  Gate -->|稳| Promote",
        ),
        floor(
            "JVM 对齐 limit",
            "堆用 MaxRAMPercentage；直接内存/元空间/线程栈另留；禁 Xmx>limit。",
            "容器 cgroup 感知；OOMKill≠堆 OOM。",
            "只加 Xmx→被 kube OOMKill；强依赖当 liveness→连环重启。",
            "NMT、重启原因、探针失败率、支付成功率。",
        ),
        today("""<ul>
<li>pay-callback 独立 Deployment+独立池；PDB 防自愿中断抽干。</li>
<li>readiness：数据源+关键依赖浅检；liveness：本地 /healthz 无 DB。</li>
<li>金丝雀观察：支付成功、退款成功、Outbox 年龄、5xx。</li>
<li>HPA：对 CPU 可；秒杀入口靠限流/预热，不靠现场手搓扩容赌运气。</li>
</ul>"""),
        industry_cases("k8sx-w", [
            ("电商支付回调", "独立舱壁", "独立部署+HPA 谨慎", "与浏览共用池", "拆分+限流", "回调成功率稳定"),
            ("银行渠道", "变更窗金丝雀", "小流量+强门禁", "全量星期五", "窗口+回滚指挥官", "RTO 达标演练"),
            ("物流 OMS", "节点故障", "PDB+多 AZ", "单副本有状态误放", "无状态+外部位点", "杀节点演练通过"),
            ("餐饮高峰", "门店热点", "副本预热+出口限流", "HPA 反应慢", "T-1 预热", "午高峰不雪崩"),
        ]),
        runbook("金丝雀跌支付成功率",
                "<ol><li>停滚动/缩金丝雀为 0。</li><li>revision 回滚。</li><li>核对 Outbox/回调池。</li><li>单号串链定位。</li><li>复盘进发布清单。</li></ol>"),
    ])


def boost_bx_hub() -> str:
    return "\n".join([
        essence(
            "组合拳场景才是外包第一周真实火力：促销×支付×仓配×售后同时炸。",
            "怕单点知识拼不出可验收交付。",
            "每案强制四段+五步+多解法+压测数字；技术必须回溯 PRD。",
            "不会讲组合拳=只会背中间件名。",
            "无组合训练→大促现场抓瞎。",
        ),
        two_mmds(
            "bx-hub",
            "五案挂正逆向",
            "flowchart TB\n  BF[B-F 正向]-->BX1[拼团券退]\n  BF-->BX2[付后缺货]\n  BR[B-R 逆向]-->BX3[寄修换新]\n  BI[B-Ind]-->BX4[餐饮取消]\n  BI-->BX5[跨境清关]\n  BX1-->SM[S-Method]\n  BX2-->SM",
            "学习用法",
            "flowchart LR\n  Read[读四段]-->Trade[取舍表]-->Drill[练手]-->Reflect[反思]-->Year[S-Year 复做]",
        ),
        company_prd(
            "进组可能同时撞上促销退款与仓配缺货，需要可讲解组合方案。",
            "五案各含四段/五步/取舍/题；压测与对账口径。",
            "玩具 demo、只讲框架。",
            "按案走主/异/逆。",
            "并发临界、重复回调、跨系统竞态。",
            "每案能讲清验收句与回滚。",
            "作品集截图：压测、对账、演练。",
        ),
    ])


def boost_mgmt() -> str:
    return "\n".join([
        two_mmds(
            "mgmt",
            "故事拆到可演示",
            "flowchart LR\n  Epic[史诗]-->Story[用户故事]\n  Story-->Tech[技术卡:表/消息/开关/监控/回滚]\n  Tech-->Demo[预发可点]\n  Demo-->UAT[验收句]",
            "阶段门 vs 小步",
            "flowchart TD\n  Req{爆炸半径/不可逆?}\n  Req -->|小| Agile[周迭代+金丝雀]\n  Req -->|大| Gate[设计冻结→迁移→双轨→切流]\n",
        ),
        industry_cases("mgmt", [
            ("电商退款口径变更", "分摊算法改", "敏捷+财务门禁+对账用例", "当普通文案周更", "双周+双跑抽样", "错退率不升"),
            ("银行换渠道", "支付通道", "阶段门+演练", "敏捷天天切", "冻结设计→沙箱→灰度", "窗口内 RTO 达标"),
            ("物流 OMS 改造", "多仓路由", "阶段门+双轨", "现场改键", "双写影子→切流", "短拣补偿不回退"),
            ("餐饮峰值需求", "取消规则", "小步+开关", "大促当天全量", "T-7 冻结+开关", "餐损可解释"),
        ]),
        failbox("排期反模式", "<ul><li>联调写「有空再联」。</li><li>故事无可演示切片。</li><li>监控/回滚不进 DoD。</li><li>大促窗改退款口径全量。</li></ul>"),
    ])


def boost_p0_diag() -> str:
    return "\n".join([
        two_mmds(
            "p0-diag",
            "线上排障总戏本",
            "flowchart TD\n  Alert-->Triage{资损?}\n  Triage -->|是| Freeze[冻结资金动作]\n  Triage -->|否| Scope[划界:入口/依赖/发布]\n  Freeze-->Trace[单号串链]\n  Scope-->Trace\n  Trace-->Hyp[假设≤3]\n  Hyp-->Prove[日志/指标/库态证明]\n  Prove-->Fix[止血→根治→复盘]",
            "支付回调慢",
            "flowchart LR\n  CB[回调池打满]-->Dep[下游慢]\n  Dep-->Bulkhead[舱壁]\n  CB-->Idem[幂等表]\n  Bulkhead-->Recover[恢复]",
        ),
        runbook("P0 头 15 分钟",
                "<ol><li>三针：支付成功、退款成功、Outbox 年龄。</li><li>是否发布中/开关误触。</li><li>单号：订单→支付→履约→售后。</li><li>止血：限流/回滚/关新逻辑。</li><li>财务差账通道。</li></ol>"),
        industry_cases("p0-diag", [
            ("电商大促", "下单 RT 飙升", "先看限流与热点库存非盲扩", "全员重启", "分层定位", "RT 回落且超卖=0"),
            ("银行日终", "对账不平", "先冻再查流水", "先补账后查", "三方对齐", "差账可解释清零"),
        ]),
        qa("【详答】为何禁止「先重启再看」？",
           ["重启毁掉现场（线程/连接/半消息）；先抓 jstack/指标/单号再决定。",
            "值班惯性。", "重启当万能药。", "Runbook 写死取证序。", "「现场是证据，不是障碍。」"],
           "p0-diag-deep-q1"),
    ])


def boost_ddd_hub() -> str:
    return "\n".join([
        two_mmds(
            "ddd-hub",
            "订单域上下文地图",
            "flowchart TB\n  Promo[优惠]-->Snap[快照进订单]\n  Order[订单]-->Stock[库存预占事件]\n  Order-->Pay[支付]\n  Pay-->OMS[履约]\n  AS[售后]-->Snap\n  AS-->Refund[退款]",
            "聚合事务边界",
            "flowchart LR\n  Cmd[命令]-->AR[聚合根校验]\n  AR-->DB[(本上下文库)]\n  AR-->OB[Outbox事件]\n  OB-->Other[其他上下文]",
        ),
        industry_cases("ddd-hub", [
            ("电商", "优惠常变", "规则外置+成交快照内聚", "售后改历史规则行", "快照只读", "退款可解释"),
            ("银行", "账户分户", "账户聚合强一致", "跨户长事务", "记账凭证+异步", "日终平"),
            ("物流", "运单状态", "运单聚合+轨迹事件", "轨迹反写核心乱序", "序号 upsert", "展示可校正"),
            ("餐饮", "门店履约", "门店/订单上下文分离", "中央库硬锁门店", "店维度分区", "高峰可扩"),
        ]),
    ])


DOC_AUDIT = """
<section class="block" id="doc-audit" data-toc="DOC-AUDIT · 全书去水审计" data-prio="p0" data-tags="audit anti-water">
  <h2><span class="sys-id">DOC-AUDIT</span>全书去水审计（诚实 before/after）</h2>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>质量账本：写清本轮重写了哪些、仍有何风险。禁止假 PASS。</div>
  <div class="plain"><div class="label">人话版</div>用户反馈「不只是附录，都太水」。本轮范围=整书：正逆向脊柱、B-X、T 层、S-MS/K8s/AI/DDD/管理/年路线、ENCY 全貌（含 PolarDB-X CN/DN/GMS/CDC）。</div>

  <p><b>体积：</b>本轮任务起点约 <code>942KB</code> → 去水重写后约 <code>1.07MB</code>（双 HTML 同 MD5）。mermaid 约 81 → 120+。</p>
  <h3>Before（审计快照）</h3>
  <table>
    <thead><tr><th>区域</th><th>症状</th><th>证据</th></tr></thead>
    <tbody>
      <tr><td>ENCY-FM 多条目</td><td>能力面一行带过；案例 2 条+垫片；「示意区间」套话重复</td><td>链节 &lt;1KB；PolarDB 无 CN/DN/GMS/CDC 锚点</td></tr>
      <tr><td>T-AI-X 子章</td><td>表格式清单、无双流程图、案例单薄</td><td>rag/mcp/integrate 约 0.3～0.5KB 有效叙述</td></tr>
      <tr><td>T-Found / T-K8s-X</td><td>口诀+短表，缺生产串链</td><td>多节 mermaid=0</td></tr>
      <tr><td>B-X</td><td>有四段但仍缺流程图与跨行业对照</td><td>hub/案 mermaid=0</td></tr>
      <tr><td>P0/P1 加深</td><td>速查残留、口诀堆砌</td><td>多节 &lt;800 字</td></tr>
      <tr><td>管理/DDD hub</td><td>目录感强于落地</td><td>缺跨行业与双图</td></tr>
    </tbody>
  </table>

  <h3>After（本轮已做）</h3>
  <table>
    <thead><tr><th>重写/加厚区域</th><th>动作</th><th>锚点举例</th></tr></thead>
    <tbody>
      <tr><td>ENCY-FM 存储/运行时/MQ</td><td>CHAINS 深链 + PolarDB-X CN/DN/GMS/CDC 专节 + 4 案</td><td><code>#ency-fm-polardb-cn</code> 等</td></tr>
      <tr><td>T-AI-X rag/mcp/integrate</td><td>本质+双 mermaid+跨行业+五步+详答</td><td><code>#t-ai-x-rag</code></td></tr>
      <tr><td>T-Found-Rocket / T-K8s workload</td><td>底板+双图+行业案+Runbook</td><td><code>#t-found-rocket</code> <code>#t-k8s-x-workload</code></td></tr>
      <tr><td>B-X hub / 管理 / DDD hub / P0 排障</td><td>去目录水、补全链路与案例</td><td><code>#bx-prod</code> <code>#s-mgmt-x</code> <code>#doc-audit</code></td></tr>
      <tr><td>假 PASS 收敛</td><td>ENCY hub 改为可审计表述；本页列剩余风险</td><td><code>#ency-fm</code> <code>#doc-audit</code></td></tr>
    </tbody>
  </table>

  <h3>Remaining risks（未宣称全绿）</h3>
  <ul>
    <li>P1 速查页（如 T12）有意保持短链+跳转极致章；若读者只停在速查仍会觉得薄——请跟锚点进 T-K8s-X / ENCY-FM。</li>
    <li>部分「公开量级/工程目标」仍非某厂未公开精确值；禁止把示意写成内部 KPI。</li>
    <li>Spark/Flink 等大数据条目深度低于 RocketMQ 金标；若面试主攻实时数仓需再加厚算子级调优。</li>
    <li>双 HTML 需同 MD5；若只改其一即为回归失败。</li>
  </ul>
  <div class="koujue"><div class="label">口诀</div>去水口诀：有底板、有双图、有行业案、有配置坑、有五步回扣；目录当文章=水。</div>
</section>
"""
