# -*- coding: utf-8 -*-
"""业务知识百科：交易域全谱（极深）"""
from ency_factory import sec, deep
from helpers import mermaid, reflect, koujue, plain, spine, qa, tradeoff, today


def _hub() -> str:
    return sec(
        "ency-biz",
        "ENCY-BIZ · 业务百科总图",
        "ENCY-BIZ",
        "业务知识百科：交易域全谱总图",
        deep(
            plain_txt="人话：业务百科不是 PRD 复述——每主题钉清「钱/货/权」哪条会坏，再给多解法边界与验收。",
            biz="买成、履约、退成/修好全链路可解释、可对账、可回滚。",
            impl="状态机+幂等+分摊账本+领域事件；行业旋钮（餐饮/跨境）挂同一脊柱。",
            principle="本质四段：业务本质→实现→原理（并发/一致）→业务实质（客诉/资损指标）。",
            substance="验收=支付成功率、退款时效、分摊平衡、库存一致、对账三针。",
            hc="大促拼团+券+并发退是压力测试全集。",
            mermaid_id="diag-ency-biz-map",
            mermaid_code="""flowchart LR
  SKU[商品] --> INV[库存]
  PRICE[价格] --> MKT[营销券积分]
  MKT --> PAY[支付]
  PAY --> OMS[OMS]
  OMS --> WMS[WMS]
  WMS --> LOG[物流]
  LOG --> AS[售后逆向]
  AS --> SETTLE[清结算]
  RISK[风控] --> PAY
  VIP[会员权益] --> MKT
""",
            today_html="<ul><li>新需求先填：钱货权终态 + 异常分支 + 对账口径。</li><li>禁止技术拼凑：没有业务验收指标不上线。</li></ul>",
            koujue_txt="业务口诀：钱货权三线，状态机记账，分摊可逆，对账收口。",
            reflect_id="ency-biz-hub-r1",
            spine_pos="业务百科挂 B0 正逆向；每叶回扣买成/退成。",
            serves="全交易域",
            back="B0 → 本百科 → S-Method",
            qas=[
                ("【综合】用一句话定义「交易域业务本质」并举三个验收指标。",
                 ["钱货权一致可达终态；指标：支付成功率、退款 T+时效、分摊合计=头。",
                  "方案评审。", "只讲微服务不讲验收。", "评审模板强制三指标。", "「终态可对账才叫做完。」"],
                 "ency-biz-hub-q1"),
            ],
        ),
        "p1",
    )


TOPICS = [
    # (id, toc, sys, title, dict for deep)
    ("ency-biz-product", "ENCY-BIZ · 商品与类目", "ENCY-BIZ-SKU", "商品 / 类目 / SPU·SKU / 上下架", {
        "plain_txt": "比喻：SPU 是「某款手机」说明书，SKU 是「黑色 256G」可卖单元；上下架是柜台灯开关。",
        "biz": "可卖信息准确：价、库存、渠道、合规标签一致，避免超卖与错价客诉。",
        "impl": "商品中心主数据；SKU 唯一；上下架事件驱动搜索/缓存失效；渠道价独立表。",
        "principle": "主数据 vs 交易快照：下单瞬间固化 SKU 快照，防事后改价污染历史单。",
        "substance": "错价率、不可售拦截率、搜索一致性延迟。",
        "hc": "大促改价风暴打爆缓存与搜索刷新。",
        "floor_title": "商品主数据与交易快照",
        "structure": "SPU→SKU→渠道价→库存视图；订单行存 sku_snapshot（价/税/名）。",
        "source_path": "读写：商品写模型 → Outbox → 搜索/Redis；下单读快照写入 order_item。",
        "online": "活动改价未失效 CDN→用户看见旧价下单→客诉；或改价后历史单展示被污染。",
        "verify": "看：改价事件 lag、缓存 TTL、订单行 snapshot 与当前价差异告警。",
        "mermaid_id": "diag-ency-biz-sku",
        "mermaid_code": """flowchart TD
  Edit[运营改价/上下架] --> Write[商品写库]
  Write --> Outbox[领域事件]
  Outbox --> Cache[Redis/CDN失效]
  Outbox --> ES[搜索索引]
  Order[下单] --> Snap[固化SKU快照]
  Snap --> Item[order_item]
""",
        "today_html": "<ul><li>订单行禁止只存 sku_id 事后 join 现价。</li><li>上下架与可售校验放在下单事务前。</li></ul>",
        "trade_title": "改价生效策略",
        "trade_rows": [
            ("立即生效+缓存删", "强", "尖刺", "低", "常规改价"),
            ("定时生效任务", "可预期", "时钟漂移", "中", "大促预约价"),
            ("仅新单生效", "历史安全", "展示复杂", "中", "<b>推荐默认</b>"),
        ],
        "qas": [("【线上】用户下单后看到价格变了，如何定责？",
                 ["查 order_item 快照 vs 当前价；展示层误用现价则修展示；若下单时价错则补差/客服策略。",
                  "客诉。", "事后改快照。", "快照不可变+审计。", "「成交价以快照为准。」"],
                 "ency-biz-sku-q1")],
        "reflect_id": "ency-biz-sku-r1",
        "koujue_txt": "商品口诀：主数据可变，成交快照钉死。",
    }),
    ("ency-biz-inv", "ENCY-BIZ · 库存与预占", "ENCY-BIZ-INV", "库存：可售 / 锁定 / 实扣 / SN", {
        "plain_txt": "比喻：可售是货架标牌数，锁定是客人手里捏着的号，实扣是出库撕标；SN 是每台机器的身份证。",
        "biz": "不超卖、不超退；锁定超时释放；SN 全生命周期可追溯。",
        "impl": "预占（Redis/DB）→ 支付成功实扣 → 取消/超时回补；WMS 实拣回传校正。",
        "principle": "库存是多视图：销售库存≠实物库存；跨仓分配要版本号。",
        "substance": "超卖=0；预占释放时效；盘点差异率。",
        "hc": "秒杀同 SKU 热点行/热 Key。",
        "floor_title": "预占与实扣状态机",
        "structure": "available/locked/sold；条件更新 WHERE qty>=?；SN: produce→in→out→sale→aftersale。",
        "source_path": "路径：下单 DECR/条件更新 → 支付回调 confirm → OMS 下发 → WMS 扣实物。",
        "online": "只减 Redis 不补偿；或支付失败不释放导致假缺货。",
        "verify": "预占≈支付转化；对账销售库存 vs WMS。",
        "mermaid_id": "diag-ency-biz-inv",
        "mermaid_code": """stateDiagram-v2
  [*] --> Available
  Available --> Locked: 下单预占
  Locked --> Sold: 支付成功实扣
  Locked --> Available: 超时/取消释放
  Sold --> Available: 售后退货回库
""",
        "today_html": "<ul><li>预占带 TTL + 支付成功幂等确认。</li><li>SN 商品售后必须校验 SN 状态机。</li></ul>",
        "qas": [("【设计】多仓如何避免超卖又避免锁死全国库存？",
                 ["仓维度库存+分配策略；全局再平衡异步；热点仓本地预留。",
                  "履约。", "全局一把锁。", "仓分片+预留。", "「锁仓不锁国。」"],
                 "ency-biz-inv-q1")],
        "reflect_id": "ency-biz-inv-r1",
        "koujue_txt": "库存口诀：预占有时限，实扣看支付，回补看单据。",
    }),
    ("ency-biz-price", "ENCY-BIZ · 价格引擎", "ENCY-BIZ-PRICE", "价格：基础价 / 活动价 / 会员价 / 锁价", {
        "plain_txt": "人话：标价是橱窗，成交价是收银台算完优惠后的数；锁价防止「购物车趴一夜价格漂移」。",
        "biz": "展示价可信、成交价可解释、锁价窗口内一致。",
        "impl": "价格中心计算 API；购物车/结算锁价 token；下单再算一遍校验。",
        "principle": "价格是规则组合结果；必须可复现（同输入同输出）以便审计。",
        "substance": "价差客诉率、锁价冲突率。",
        "mermaid_id": "diag-ency-biz-price",
        "mermaid_code": """flowchart TD
  Base[基础价] --> Eng[价格引擎]
  Act[活动价] --> Eng
  Vip[会员价] --> Eng
  Eng --> Show[展示价]
  Eng --> Lock[锁价Token]
  Lock --> Checkout[结算校验]
  Checkout --> Order[下单固化]
""",
        "today_html": "<ul><li>结算与下单两次计价；差额超阈拒绝并提示刷新。</li></ul>",
        "qas": [("【坑】只信前端传来的 payAmount 会怎样？",
                 ["资损。服务端必须重算；前端金额仅展示。", "支付。", "信任客户端。", "服务端重算+签名。", "「钱只信服务端。」"],
                 "ency-biz-price-q1")],
        "reflect_id": "ency-biz-price-r1",
        "koujue_txt": "价格口诀：展示可漂，成交重算，快照钉死。",
    }),
    ("ency-biz-member", "ENCY-BIZ · 会员与等级", "ENCY-BIZ-VIP", "会员：等级 / 权益 / 积分账户", {
        "plain_txt": "比喻：会员像俱乐部通行证；积分是店内代币；权益是「免运/延保」券包。",
        "biz": "权益发放可追溯、过期可解释、退款可追回（按规则）。",
        "impl": "会员账户+权益实例表；积分流水不可改只可冲正；等级规则引擎。",
        "principle": "权益与订单绑定：购买赠送 vs 会员自动；逆向要定义是否收回。",
        "substance": "错发权益率、积分对账平衡。",
        "mermaid_id": "diag-ency-biz-vip",
        "mermaid_code": """flowchart LR
  PayOK[支付成功] --> Grant[发放权益/积分]
  Grant --> Ledger[权益/积分流水]
  AS[售后完成] --> Claw[按规则追回/冲正]
  Claw --> Ledger
""",
        "today_html": "<ul><li>积分用整数分；流水+余额快照；禁止直接改余额字段。</li></ul>",
        "qas": [("【售后】积分已使用再退货怎么处理？",
                 ["按规则：可退余额部分冲正；已消耗部分转现金扣减或拒绝部分退——规则写死并提示用户。",
                  "逆向。", "静默扣。", "规则配置化+客服话术。", "「积分有债要先算清。」"],
                 "ency-biz-vip-q1")],
        "reflect_id": "ency-biz-vip-r1",
        "koujue_txt": "会员口诀：权益实例化，流水可冲正。",
    }),
    ("ency-biz-mkt", "ENCY-BIZ · 营销活动", "ENCY-BIZ-MKT", "营销：满减 / 折扣 / 秒杀 / 拼团拼单", {
        "plain_txt": "人话：营销是「在规则允许下让 gu 客觉得划算」；拼团是社交锁客+库存名额游戏。",
        "biz": "活动预算可控、名额不超发、成团/失败自动退清晰。",
        "impl": "活动中心+名额计数；拼团状态机；预算扣减与告警。",
        "principle": "活动与券叠加是组合优化；必须定义互斥与最优解策略。",
        "substance": "超发=0；失败自动退时效；预算耗尽熔断。",
        "hc": "拼团成团瞬间并发退款与库存回补。",
        "floor_title": "拼团名额与成团",
        "structure": "group_order 状态：INIT→JOINING→SUCCESS/FAIL；名额 CAS/Redis。",
        "source_path": "参团→名额+1→满员成团事件→履约；超时 Job/延时消息→FAIL→退款。",
        "online": "成团与支付回调竞态导致多退或未退。",
        "verify": "名额≤上限；FAIL 单退款闭环率 100%。",
        "mermaid_id": "diag-ency-biz-group",
        "mermaid_code": """stateDiagram-v2
  [*] --> Joining
  Joining --> Success: 满员
  Joining --> Fail: 超时
  Success --> Fulfill: 履约
  Fail --> Refund: 自动退
""",
        "trade_title": "拼团失败退款",
        "trade_rows": [
            ("扫表 Job", "最终一致", "延迟分钟级", "低", "MVP"),
            ("延时消息", "更快", "运维中", "中", "<b>中厂常用</b>"),
            ("强事务同步退", "强", "耦合渠道", "高", "慎"),
        ],
        "today_html": "<ul><li>成团/失败事件幂等；退款单号=groupId+orderId。</li></ul>",
        "qas": [("【并发】最后两名同时参团超员怎么防？",
                 ["名额原子扣减，失败走候补或失败态；禁先插再数。", "大促。", "先插后数。", "Redis/DB 原子。", "「名额先原子再落单。」"],
                 "ency-biz-mkt-q1")],
        "reflect_id": "ency-biz-mkt-r1",
        "koujue_txt": "营销口诀：名额原子，失败必退，预算熔断。",
    }),
    ("ency-biz-coupon", "ENCY-BIZ · 券与积分抵扣", "ENCY-BIZ-COUPON", "券：领取 / 核销 / 返还；积分抵扣", {
        "plain_txt": "比喻：券是一次性门票；核销是检票撕票；退货要决定能不能「粘回去」。",
        "biz": "不重复核销、退货返还规则清晰、与分摊联动。",
        "impl": "券实例状态；核销流水；退货按原核销单返还或作废。",
        "principle": "券资产与订单优惠分摊行关联，逆向按分摊回退。",
        "substance": "重复核销=0；返还准确率。",
        "mermaid_id": "diag-ency-biz-coupon",
        "mermaid_code": """flowchart TD
  Claim[领券] --> Inst[券实例AVAILABLE]
  Inst --> Use[下单核销USED]
  Use --> Alloc[写入分摊行]
  AS[售后] --> Ret{可返还?}
  Ret -->|是| Back[回到AVAILABLE/新券]
  Ret -->|否| Dead[作废]
""",
        "today_html": "<ul><li>核销幂等键：couponInstanceId+orderId。</li><li>积分抵扣走独立流水并参与分摊。</li></ul>",
        "qas": [("【逆向】部分退货券怎么退？",
                 ["按分摊行比例或整券规则（配置）；禁止口头约定。", "售后。", "整单退券但只退一货。", "规则表+分摊。", "「券跟着分摊走。」"],
                 "ency-biz-coupon-q1")],
        "reflect_id": "ency-biz-coupon-r1",
        "koujue_txt": "券口诀：实例状态机，核销可幂等，返还看规则。",
    }),
    ("ency-biz-alloc", "ENCY-BIZ · 优惠分摊", "ENCY-BIZ-ALLOC", "优惠分摊：入账 / 部分退 / 末行差", {
        "plain_txt": "人话：整单便宜了 30 块，财务要知道每个 SKU「摊到多少」——否则部分退算不清。",
        "biz": "行合计=头；部分退可逆；审计可解释。",
        "impl": "整数分分摊+末行吃差；落 order_discount_allocation；逆向读原分摊。",
        "principle": "组合优化选优惠后，必须固化分摊结果，不能每次重算漂移。",
        "substance": "分摊不平衡告警=0；财务抽检通过。",
        "floor_title": "整数分摊算法",
        "structure": "份额=行金额/可分摊基数；分摊分=floor；最后一行=总额-已分。",
        "source_path": "计价引擎 → allocation 表 → 退款服务读取回退。",
        "online": "用 double 导致差 1 分；或退货重算分摊与原单不一致。",
        "verify": "SUM(alloc)=header；退款模拟用例。",
        "mermaid_id": "diag-ency-biz-alloc",
        "mermaid_code": """flowchart TD
  Disc[优惠总额] --> Split[按行比例整数分]
  Split --> Rows[分摊行]
  Rows --> Last[末行吃差]
  Last --> Save[落库不可变]
  AS[部分退] --> Read[读原分摊]
  Read --> Refund[按份额退]
""",
        "today_html": "<ul><li>金额用「分」整数；禁止 float。</li><li>分摊行与订单同行号绑定。</li></ul>",
        "qas": [("【财务】部分退差 1 分不签字，根因？",
                 ["舍入策略未用末行差或退款重算。固化原分摊+整数。", "售后。", "double。", "整数+末行。", "「差一分也是事故。」"],
                 "ency-biz-alloc-q1")],
        "reflect_id": "ency-biz-alloc-r1",
        "koujue_txt": "分摊口诀：整数分，末行差，退货读原账。",
    }),
    ("ency-biz-pay", "ENCY-BIZ · 支付", "ENCY-BIZ-PAY", "支付：预支付 / 回调 / 幂等 / 渠道", {
        "plain_txt": "比喻：预支付是开单号，回调是银行盖章；盖章可能敲两次——你得认出同一章。",
        "biz": "不错账、不漏单、可对账；用户感知「扣成功就要履约」。",
        "impl": "支付单状态机；渠道 trade_no 唯一；回调先幂等再推进订单。",
        "principle": "渠道是不可靠网络；本地消息/Outbox 驱动下游。",
        "substance": "支付成功率、回调重复安全、对账差异。",
        "hc": "大促回调洪峰打满线程池。",
        "floor_title": "支付回调幂等",
        "structure": "UNIQUE(channel,trade_no)；订单 CREATED→PAID 条件更新。",
        "source_path": "回调→幂等表 insert→更新支付单→Outbox→OMS。",
        "online": "先调 OMS 再落库导致重复履约；或忽略重复回调当失败。",
        "verify": "幂等冲突计数；支付与订单状态一致性巡检。",
        "mermaid_id": "diag-ency-biz-pay",
        "mermaid_code": """sequenceDiagram
  participant U as 用户
  participant O as 订单
  participant P as 支付
  participant C as 渠道
  U->>O: 下单
  O->>P: 创建支付单
  P->>C: 预支付
  C-->>P: 回调(可能重复)
  P->>P: 幂等落库
  P->>O: 置PAID+Outbox
""",
        "today_html": "<ul><li>回调线程池舱壁；渠道重试依赖本地幂等。</li></ul>",
        "qas": [("【线上】回调成功但订单仍待支付？",
                 ["查幂等是否成功、Outbox 是否投递、条件更新是否被并发取消抢先。", "支付。", "只重推回调。", "对账三表。", "「三表对上再动手。」"],
                 "ency-biz-pay-q1")],
        "reflect_id": "ency-biz-pay-r1",
        "koujue_txt": "支付口诀：幂等先落，状态条件更，下游看 Outbox。",
    }),
    ("ency-biz-settle", "ENCY-BIZ · 清结算", "ENCY-BIZ-SETTLE", "清结算：分账 / 对账 / 轧差", {
        "plain_txt": "人话：清结算是「今天该给商家/渠道/平台各多少」——和用户支付不是同一笔账。",
        "biz": "分账准确、周期可出报表、差异可定位。",
        "impl": "结算单+明细；T+N 批处理；渠道对账文件解析；差异工单。",
        "principle": "业务账 vs 渠道账 vs 内部账三角对；差异分类：时延/丢单/金额。",
        "substance": "对账差异闭环时效；分账差错率。",
        "mermaid_id": "diag-ency-biz-settle",
        "mermaid_code": """flowchart TD
  Trade[交易完成] --> Bill[生成结算明细]
  Bill --> Batch[T+N汇总]
  File[渠道对账文件] --> Diff[三方对账]
  Batch --> Diff
  Diff --> OK[平]
  Diff --> Ticket[差异工单]
""",
        "today_html": "<ul><li>结算口径文档化；禁止客服口头改数。</li></ul>",
        "qas": [("【对账】渠道多一笔我们没有？",
                 ["查是否回调丢失；补单或挂待查；禁直接改结算。", "清结算。", "手工改平。", "补单流程。", "「差异要工单不要抹平。」"],
                 "ency-biz-settle-q1")],
        "reflect_id": "ency-biz-settle-r1",
        "koujue_txt": "清结算口诀：三角对账，差异工单，禁口头抹平。",
    }),
    ("ency-biz-risk", "ENCY-BIZ · 风控", "ENCY-BIZ-RISK", "风控：规则 / 画像 / 人审 / 处置", {
        "plain_txt": "比喻：风控是门口保安——指纹、行为、频次；有的直接拦，有的喊经理（人审）。",
        "biz": "拦欺诈又少误伤好人；处置可申诉。",
        "impl": "规则引擎+特征服务；同步拦+异步复核；处置码驱动支付/发货。",
        "principle": "可解释优先于黑盒；高风险必须 HITL。",
        "substance": "欺诈损失、误伤率、人审时效。",
        "mermaid_id": "diag-ency-biz-risk",
        "mermaid_code": """flowchart TD
  Req[下单/支付] --> Feat[特征:设备IP行为]
  Feat --> Rule[规则/模型]
  Rule --> Pass[通过]
  Rule --> Review[人审]
  Rule --> Block[拦截]
""",
        "today_html": "<ul><li>处置结果写审计；禁止静默改单。</li></ul>",
        "qas": [("【平衡】大促误伤升高怎么办？",
                 ["降敏规则+白名单+加速人审；看误伤率仪表。", "大促。", "全关风控。", "动态阈值。", "「风控可调不是可关。」"],
                 "ency-biz-risk-q1")],
        "reflect_id": "ency-biz-risk-r1",
        "koujue_txt": "风控口诀：特征进门，规则分流，高危人审。",
    }),
    ("ency-biz-oms", "ENCY-BIZ · OMS", "ENCY-BIZ-OMS", "OMS：接单 / 拆合单 / 下发 / 取消令牌", {
        "plain_txt": "人话：OMS 是「交易告诉仓库干什么」的翻译官；取消要抢在拣货前。",
        "biz": "下发准确、取消有结果、缺货可补偿。",
        "impl": "履约单；与 WMS 协议；取消令牌/版本号防竞态。",
        "principle": "仓态决定能否秒退；OMS 是状态权威之一。",
        "substance": "下发成功率、取消成功率、缺货闭环。",
        "mermaid_id": "diag-ency-biz-oms",
        "mermaid_code": """sequenceDiagram
  participant O as 订单
  participant M as OMS
  participant W as WMS
  O->>M: 支付成功下发
  M->>W: 创建出库单
  O->>M: 用户取消
  M->>W: 取消令牌
  W-->>M: 接受/拒绝(已拣货)
""",
        "today_html": "<ul><li>取消与拣货竞态用版本/令牌；拒绝则转售后路径。</li></ul>",
        "qas": [("【竞态】取消与拣货同时到达？",
                 ["WMS 原子判态；拒绝则 OMS 转不可秒退。", "履约。", "当成功秒退。", "令牌协议。", "「仓态说了算。」"],
                 "ency-biz-oms-q1")],
        "reflect_id": "ency-biz-oms-r1",
        "koujue_txt": "OMS 口诀：下发有单号，取消看仓态。",
    }),
    ("ency-biz-wms", "ENCY-BIZ · WMS", "ENCY-BIZ-WMS", "WMS：拣货 / 缺货 / 回传 / 库存校正", {
        "plain_txt": "比喻：WMS 是仓库操作系统；缺货是货架空了还接了单——要立刻补偿用户。",
        "biz": "实物与销售库存收敛；缺货自动触发售中逆向。",
        "impl": "出库回传；短拣/缺货事件；触发退款或换发。",
        "principle": "实物权威在仓；销售层必须订阅校正。",
        "substance": "缺货闭环时效；盘点差异。",
        "mermaid_id": "diag-ency-biz-wms",
        "mermaid_code": """flowchart TD
  Pick[拣货] --> OK[出库回传]
  Pick --> Short[短拣/缺货]
  Short --> Comp[售中补偿:退/换]
  OK --> Track[物流轨迹]
""",
        "today_html": "<ul><li>缺货事件幂等；补偿单绑定原履约单。</li></ul>",
        "qas": [("【资损】缺货仍显示已发货？",
                 ["回传状态机错误或消息乱序；以 WMS 终态校正前台。", "履约。", "信 OMS 臆测。", "回传权威。", "「仓回传是真理。」"],
                 "ency-biz-wms-q1")],
        "reflect_id": "ency-biz-wms-r1",
        "koujue_txt": "WMS 口诀：实物权威，缺货必补偿。",
    }),
    ("ency-biz-logistics", "ENCY-BIZ · 物流", "ENCY-BIZ-LOG", "物流：运单 / 轨迹 / 签收 / 拦截", {
        "plain_txt": "人话：运单号是包裹身份证；轨迹是快递日记；拦截是「还能不能喊回来」。",
        "biz": "轨迹可信、签收驱动确认收货、拦截影响逆向。",
        "impl": "物流公司对接；轨迹落库；签收事件；拦截指令状态。",
        "principle": "物流外部系统不可强一致；用最终一致+用户可见态。",
        "substance": "轨迹延迟、拦截成功率。",
        "mermaid_id": "diag-ency-biz-log",
        "mermaid_code": """flowchart LR
  Ship[出库] --> Waybill[运单]
  Waybill --> Trace[轨迹同步]
  Trace --> Sign[签收]
  Sign --> Confirm[确认收货/售后窗]
""",
        "today_html": "<ul><li>售后策略依赖物流态：未签收 vs 已签收。</li></ul>",
        "qas": [("【售后】已发货未签收退货怎么走？",
                 ["优先拦截；失败则拒收/退货流程。", "逆向。", "直接退款不管货。", "拦截+关单。", "「货在路上先拦。」"],
                 "ency-biz-log-q1")],
        "reflect_id": "ency-biz-log-r1",
        "koujue_txt": "物流口诀：轨迹可见，拦截有态，签收开窗。",
    }),
    ("ency-biz-as", "ENCY-BIZ · 售后全逆向", "ENCY-BIZ-AS", "售后：仅退款 / 退货退款 / 换货 / 维修 / 翻新 / 换新", {
        "plain_txt": "人话：售后是「把钱货权再搬一次」——搬错一步就双退或货丢。",
        "biz": "类型清晰、状态机合法、钱与货与权益一致终态。",
        "impl": "售后单聚合；审核/质检节点；退款与库存回补编排。",
        "principle": "逆向不是正向镜像；存在不可逆点（餐损、已激活权益）。",
        "substance": "退款时效、重复售后拦截、权益悬挂监控。",
        "hc": "并发重复申请与自动审。",
        "floor_title": "售后状态机",
        "structure": "创建→审→寄回→质检→退款/换新/维修…；每迁移动作校验。",
        "source_path": "申请→风控/规则→人审可选→仓储收货→退款服务。",
        "online": "自动审误过期券返还；或换新未锁库存超卖。",
        "verify": "状态非法迁移=0；退款与渠道对平。",
        "mermaid_id": "diag-ency-biz-as",
        "mermaid_code": """stateDiagram-v2
  [*] --> Created
  Created --> Auditing
  Auditing --> WaitReturn: 需退货
  Auditing --> Refunding: 仅退款
  WaitReturn --> QC
  QC --> Refunding
  QC --> Exchange: 换货/换新
  QC --> Repair: 寄修
  Refunding --> Done
  Exchange --> Done
  Repair --> Done
""",
        "mermaid_id2": "diag-ency-biz-as-money",
        "mermaid_code2": """flowchart TD
  AS[售后单] --> Calc[按分摊算应退]
  Calc --> Pay[退款渠道]
  Calc --> Coup[券/积分处理]
  Calc --> Inv[库存/SN回库]
""",
        "today_html": "<ul><li>售后单号唯一；退款 attempt 表防双退。</li><li>换新先锁库存再关闭旧履约。</li></ul>",
        "qas": [("【双退】用户重复点申请？",
                 ["进行中售后互斥；幂等键 user+order+type。", "售后。", "每次新建。", "互斥锁/唯一。", "「一单一次进行中。」"],
                 "ency-biz-as-q1")],
        "reflect_id": "ency-biz-as-r1",
        "koujue_txt": "售后口诀：类型定路径，状态合法迁，钱货权同终态。",
    }),
    ("ency-biz-benefit", "ENCY-BIZ · 权益与增值服务", "ENCY-BIZ-BENEFIT", "权益 / 延保 / 增值服务绑定解绑", {
        "plain_txt": "比喻：延保像给手机买的保险单；退货时要决定保单作废还是迁移到换新机。",
        "biz": "绑定时机清晰、解绑/迁移规则可执行、跨区合规。",
        "impl": "服务实例绑定 order/sku/sn；售后策略：作废/迁移/折算。",
        "principle": "增值服务有独立生命周期，不能只藏在订单备注。",
        "substance": "错绑率、解绑遗漏导致重复履约成本。",
        "mermaid_id": "diag-ency-biz-benefit",
        "mermaid_code": """flowchart TD
  Buy[购买] --> Bind[绑定服务实例]
  Bind --> Active[生效]
  AS[售后] --> Migrate{换新?}
  Migrate -->|是| Move[迁移到新SN]
  Migrate -->|否| Void[作废]
""",
        "today_html": "<ul><li>服务实例表；售后编排显式调用解绑/迁移。</li></ul>",
        "qas": [("【跨境】增值服务区域不可用？",
                 ["下单校验区域；售后按合规作废并退差价。", "跨境。", "忽略合规。", "区域码校验。", "「权益看辖区。」"],
                 "ency-biz-benefit-q1")],
        "reflect_id": "ency-biz-benefit-r1",
        "koujue_txt": "权益口诀：实例化绑定，售后显式解绑或迁移。",
    }),
    ("ency-biz-food", "ENCY-BIZ · 餐饮行业", "ENCY-BIZ-FOOD", "餐饮：高峰取消 / 餐损 / 不可逆点", {
        "plain_txt": "人话：菜下锅了就不是「取消退全款」那么简单——餐损是行业旋钮。",
        "biz": "出餐前进取消可退；出餐后规则化餐损；高峰稳定性。",
        "impl": "门店态/出餐态；取消策略配置；高峰限流与厨房队列。",
        "principle": "不可逆点=开始制作；状态要门店回传。",
        "substance": "取消纠纷率、出餐时效。",
        "mermaid_id": "diag-ency-biz-food",
        "mermaid_code": """flowchart TD
  Order[下单] --> Queue[厨房队列]
  Queue --> Cook[制作中=不可逆]
  Cancel[取消] --> Gate{已制作?}
  Gate -->|否| FullRefund[全退]
  Gate -->|是| Loss[餐损规则]
""",
        "today_html": "<ul><li>门店回传制作态；取消接口读态决策。</li></ul>",
        "qas": [("【高峰】取消接口超时用户重复点？",
                 ["幂等取消令牌；结果可查询。", "餐饮高峰。", "每次新取消。", "幂等。", "「取消也要幂等。」"],
                 "ency-biz-food-q1")],
        "reflect_id": "ency-biz-food-r1",
        "koujue_txt": "餐饮口诀：制作态为界，餐损规则化。",
    }),
    ("ency-biz-cross", "ENCY-BIZ · 跨境", "ENCY-BIZ-XB", "跨境：税费 / 清关 / 多币种 / 失败逆向", {
        "plain_txt": "比喻：跨境多了海关这一关——清关失败要把钱货路径倒回去。",
        "biz": "计税准确、清关可追踪、失败可全链路逆向。",
        "impl": "计税服务；报关单；汇率锁；清关失败事件驱动退款/退运。",
        "principle": "多币种以支付锁汇为准；税费与商品分摊要可退。",
        "substance": "清关失败闭环、汇率客诉。",
        "mermaid_id": "diag-ency-biz-xb",
        "mermaid_code": """flowchart TD
  Pay[支付锁汇] --> Declare[报关]
  Declare --> Clear{清关}
  Clear -->|成功| Deliver[境内配送]
  Clear -->|失败| Rev[逆向:退款/退运]
""",
        "today_html": "<ul><li>清关失败状态机与客服话术模板绑定。</li></ul>",
        "qas": [("【清关失败】税金怎么退？",
                 ["按实缴与政策；分摊回退税金行。", "跨境。", "忽略税金。", "税行独立。", "「税也是一行账。」"],
                 "ency-biz-xb-q1")],
        "reflect_id": "ency-biz-xb-r1",
        "koujue_txt": "跨境口诀：锁汇报关，失败全逆向。",
    }),
    ("ency-biz-bank", "ENCY-BIZ · 银行账户并发对账", "ENCY-BIZ-BANK", "银行/账户工程向：并发记账与对账", {
        "plain_txt": "人话：账户像保险箱日记账——同一账户并发入账要串行化或分片；每天和银行文件对平。",
        "biz": "余额不错、流水可追溯、对账差异可关单。",
        "impl": "账户行锁/版本；流水先写入；日终对账；热账户分片。",
        "principle": "借贷必相等；禁止直接改余额无流水。",
        "substance": "对账平账率、热账户 RT。",
        "hc": "热点商户账户。",
        "floor_title": "账户并发与流水",
        "structure": "account+ledger；UPDATE bal WHERE version；或热点账户分片汇总。",
        "source_path": "交易→记账服务→流水→余额；日终文件对账 Job。",
        "online": "先改余额后写流水崩溃→账实不符。",
        "verify": "流水合计=余额变动；与渠道文件差异。",
        "mermaid_id": "diag-ency-biz-bank",
        "mermaid_code": """flowchart TD
  Tx[交易事件] --> Ledger[写流水]
  Ledger --> Bal[条件更新余额]
  File[银行对账文件] --> Recon[对账引擎]
  Ledger --> Recon
  Recon --> Diff[差异工单]
""",
        "today_html": "<ul><li>记账顺序：流水→余额；热户分片。</li><li>对账差异禁止手工改余额抹平。</li></ul>",
        "qas": [("【热点】大商户账户锁等待爆炸？",
                 ["账户分片/缓冲记账延迟汇总；或队列串行化单账户。", "清结算。", "加大锁超时。", "分片。", "「热户要切开。」"],
                 "ency-biz-bank-q1")],
        "reflect_id": "ency-biz-bank-r1",
        "koujue_txt": "账户口诀：先流水后余额，对账靠文件，热户要分片。",
    }),
]


def build() -> str:
    parts = [_hub()]
    for sid, toc, sys_id, title, kw in TOPICS:
        kw.setdefault("spine_pos", "挂交易正逆向主线，服务买成/退成验收。")
        kw.setdefault("serves", "订单/售后/清结算")
        kw.setdefault("back", "B0 / B-X → 本叶 → 对账")
        parts.append(sec(sid, toc, sys_id, title, deep(**kw)))
    parts.append(sec(
        "ency-biz-drill",
        "ENCY-BIZ · 综合演练题",
        "ENCY-BIZ-DRILL",
        "业务百科综合演练（多题详答）",
        plain("把多域串起来：大促拼团+券分摊+支付回调+缺货+售后——按五步与四段作答。")
        + qa("【综合】拼团成功后 WMS 缺货，平台券与积分如何处理？",
             ["钉：钱货权终态；拆：成团成功→下发→缺货事件→售中退；标：券返还/积分冲正/分摊回退；选：自动退+客服；验：分摊平、券态正确、库存回补。",
              "大促。", "只退现金忘券。", "编排清单。", "「缺货退要退全套资产。」"],
             "ency-biz-drill-q1")
        + qa("【综合】跨境清关失败且用户已用积分，如何闭环？",
             ["清关失败逆向；积分按规则冲正；税金行回退；客服话术；对账三针。",
              "跨境。", "只退货款。", "资产清单。", "「跨境逆向=税+分+货。」"],
             "ency-biz-drill-q2")
        + qa("【综合】寄修与换新并行时库存与 SN？",
             ["换新锁新库存；旧 SN 进入维修态；完成迁移权益；禁止两路都发货。",
              "售后。", "两路并行发。", "互斥令牌。", "「一路货权。」"],
             "ency-biz-drill-q3")
        + koujue("演练口诀：资产清单先列全，再谈状态机。")
        + reflect("ency-biz-drill-r1"),
    ))
    return "\n".join(parts)
