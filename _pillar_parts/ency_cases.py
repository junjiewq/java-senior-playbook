# -*- coding: utf-8 -*-
"""公开技术分享常见做法 · 公司集群案例矩阵（归纳，禁止伪造机密）"""
from ency_factory import sec, deep
from helpers import plain, koujue, reflect, spine, mermaid, qa, today, tradeoff


DISCLAIMER = (
    '  <div class="callout"><div class="label">出处说明（必读）</div>'
    "<p>以下为<strong>公开技术分享常见做法 / 案例归纳</strong>："
    "综合业界公开演讲、工程博客、开源中间件实践中反复出现的落地套路，"
    "映射到本册交易/餐饮/跨境/物流/制造/金融场景，便于中厂裁剪。"
    "<b>不代表</b>上述公司未公开的内部架构、代号、机密指标或真实链接；"
    "<b>禁止</b>把本归纳当成内部泄密材料引用。</p></div>\n"
)


def _hub() -> str:
    return sec(
        "ency-case",
        "ENCY-CASE · 公开案例矩阵总图",
        "ENCY-CASE",
        "技术方案落地·公开案例矩阵（拼多多/肯德基麦当劳/阿里/用友/招行/美团饿了么/大疆/顺丰）",
        spine(
            "附录追加：把百科技术点挂到「公开分享里常见的落地套路」上，方便选型与面试叙事。",
            serves="交易/餐饮/金融/本地生活/物流/制造数字化",
            back="ENCY 百科 → 本矩阵 → 中厂裁剪清单",
        )
        + plain(
            "人话：别背公司名唬人——看的是<strong>可复用的方案骨架</strong>："
            "高并发怎么削峰、餐饮怎么定不可逆点、金融怎么高可用与风控分层、物流怎么轨迹最终一致。"
        )
        + DISCLAIMER
        + mermaid(
            "diag-ency-case-map",
            "flowchart TB\n"
            "  CASE[ENCY-CASE 公开案例矩阵] --> PDD[拼多多套路:拼团补贴成本]\n"
            "  CASE --> FOOD[肯德基麦当劳套路:高峰券餐损]\n"
            "  CASE --> ALI[阿里套路:大促中间件单元化]\n"
            "  CASE --> YON[用友套路:中台ERP B2B]\n"
            "  CASE --> CMB[招行套路:金融风控高可用]\n"
            "  CASE --> MT[美团饿了么套路:配送拼单]\n"
            "  CASE --> DJI[大疆套路:端云物联可靠]\n"
            "  CASE --> SF[顺丰套路:运单仓干配]\n"
            "  CASE --> Cut[中厂裁剪五问]\n",
        )
        + """  <h3>案例索引</h3>
  <table>
    <thead><tr><th>集群</th><th>公开主题归纳</th><th>挂本册场景</th><th>锚点</th></tr></thead>
    <tbody>
      <tr><td>拼多多</td><td>高并发拼团/补贴/极致成本</td><td>营销拼团、秒杀预占</td><td><a href="#ency-case-pdd">#ency-case-pdd</a></td></tr>
      <tr><td>肯德基/麦当劳</td><td>高峰、券核销、出餐、取消餐损</td><td>餐饮旋钮 B-Ind/B-X</td><td><a href="#ency-case-food">#ency-case-food</a></td></tr>
      <tr><td>阿里</td><td>大促、中间件、单元化/限流降级</td><td>大促三联、网关、MQ</td><td><a href="#ency-case-ali">#ency-case-ali</a></td></tr>
      <tr><td>用友</td><td>企业数字化、中台/ERP、B2B 单据</td><td>B2B 履约/清结算集成</td><td><a href="#ency-case-yonyou">#ency-case-yonyou</a></td></tr>
      <tr><td>招商银行</td><td>金融交易、风控、高可用（工程向）</td><td>支付/账户/对账</td><td><a href="#ency-case-cmb">#ency-case-cmb</a></td></tr>
      <tr><td>美团/饿了么</td><td>本地生活高峰、配送、拼单</td><td>履约调度、拼单</td><td><a href="#ency-case-local">#ency-case-local</a></td></tr>
      <tr><td>大疆</td><td>硬件+云、物联网/高可靠</td><td>设备/SN/售后寄修</td><td><a href="#ency-case-dji">#ency-case-dji</a></td></tr>
      <tr><td>顺丰</td><td>物流轨迹、运单、仓干配</td><td>OMS/WMS/物流</td><td><a href="#ency-case-sf">#ency-case-sf</a></td></tr>
    </tbody>
  </table>
"""
        + koujue("案例口诀：公开套路可学，内部机密不编，中厂裁剪五问。")
        + reflect("ency-case-hub-r1"),
        "p1",
    )


def _case_block(
    sid,
    toc,
    sys_id,
    title,
    plain_txt,
    essence,
    steps_html,
    trade_rows,
    mmd_id,
    mmd,
    pits_html,
    cut_html,
    qas,
    rid,
):
    body = (
        spine("公开案例归纳 → 映射本册正逆向/行业旋钮 → 中厂可裁剪清单。", serves=title, back="ENCY-CASE → 本叶")
        + plain(plain_txt)
        + DISCLAIMER
        + f'  <div class="essence"><div class="essence-col"><div class="label">业务本质（归纳）</div><p>{essence}</p></div>'
        f'<div class="essence-col"><div class="label">技术本质（归纳）</div><p>用公开常见工程手段把峰值、一致、可观测、可回滚做成可验收能力。</p></div></div>\n'
        + f'  <div class="callout ok"><div class="label">方案落地步骤（公开套路归纳）</div>{steps_html}</div>\n'
        + tradeoff("技术选型类比（中厂视角）", trade_rows)
        + mermaid(mmd_id, mmd)
        + f'  <div class="failbox"><div class="label">踩坑（公开分享高频）</div>{pits_html}</div>\n'
        + f'  <div class="company-prd"><div class="label">中厂裁剪</div>{cut_html}</div>\n'
        + today(
            "<ul><li>先写验收指标与回滚，再选组件品牌。</li>"
            "<li>引用对外分享时只说「公开常见做法」，不编造内部代号。</li></ul>"
        )
    )
    for q, layers, qid in qas:
        body += qa(q, layers, qid)
    body += koujue("落地口诀：步骤可抄，指标自定，规模按刀裁。")
    body += reflect(rid)
    return sec(sid, toc, sys_id, title, body, "p1")


def build() -> str:
    parts = [_hub()]

    parts.append(
        _case_block(
            "ency-case-pdd",
            "ENCY-CASE · 拼多多套路",
            "ENCY-CASE-PDD",
            "拼多多集群：高并发拼团 / 补贴 / 极致成本（公开套路归纳）",
            "公开技术讨论里，拼团电商常被归纳为：名额原子、补贴预算可控、链路极简降本——而不是堆最贵中间件。",
            "在补贴与社交裂变下仍「不超发名额、预算不穿、失败可自动退」，并用极简链路扛峰值。",
            "<ol>"
            "<li><b>钉验收：</b>名额不超过、FAIL 必退、补贴账可对。</li>"
            "<li><b>名额原子：</b>Redis/DB 条件更新；先占名额再落单。</li>"
            "<li><b>状态机：</b>参团→成团/失败；失败走退款编排。</li>"
            "<li><b>预算闸门：</b>补贴账户扣减+熔断；防活动超发。</li>"
            "<li><b>极致成本：</b>同步路径极短；重计算异步；能缓存不穿透。</li>"
            "<li><b>对账：</b>名额/支付/退款三针巡检。</li>"
            "</ol>",
            [
                ("Redis 名额+异步成团", "最终", "极高", "低", "<b>拼团峰值常见</b>"),
                ("单库条件更新", "强", "中", "低", "中低并发"),
                ("全链路分布式事务", "强", "低", "高", "通常过重"),
            ],
            "diag-ency-case-pdd",
            "flowchart TD\n"
            "  Join[参团请求] --> Gate[预算/风控闸]\n"
            "  Gate --> Seat[原子占名额]\n"
            "  Seat -->|成功| Order[落参团单]\n"
            "  Seat -->|失败| Reject[拒绝/候补]\n"
            "  Order --> Full{满员?}\n"
            "  Full -->|是| OK[成团事件→履约]\n"
            "  Full -->|超时| Fail[失败→自动退]\n",
            "<ul><li>先插单再数名额→超员。</li><li>失败退款无幂等→双退或漏退。</li>"
            "<li>为「极致」省掉对账→补贴穿桶后才发现。</li></ul>",
            "<p>中厂：名额用 Redis+DB 对账即可；预算闸门先做日限额；"
            "不必上完整活动中台。交叉 <a href='#ency-biz-mkt'>ENCY-BIZ-MKT</a>、<a href='#bx-group-coupon'>B-X 拼团</a>。</p>",
            [
                (
                    "【落地】拼团最后两名并发如何不超员？",
                    [
                        "名额原子扣减，失败拒绝；公开套路强调「先占后单」。",
                        "大促拼团。",
                        "先插再数。",
                        "DECR/条件更新+幂等。",
                        "「名额是库存的另一种说法。」",
                    ],
                    "ency-case-pdd-q1",
                ),
                (
                    "【裁剪】没有自研活动中台怎么做补贴熔断？",
                    [
                        "补贴账户表+日/活动限额；超限拒绝领券或下单；异步对账。",
                        "中厂。",
                        "只靠运营人工看。",
                        "限额闸门。",
                        "「预算也要状态机。」",
                    ],
                    "ency-case-pdd-q2",
                ),
            ],
            "ency-case-pdd-r1",
        )
    )

    parts.append(
        _case_block(
            "ency-case-food",
            "ENCY-CASE · 肯德基麦当劳套路",
            "ENCY-CASE-FOOD",
            "肯德基 / 麦当劳集群：餐饮高峰 · 券核销 · 出餐履约 · 取消餐损（公开套路归纳）",
            "餐饮公开分享常见主题：高峰排队、券/套餐核销、门店出餐状态、取消与餐损边界——核心是「制作态不可逆」。",
            "高峰下单仍可达出餐；券不重复核销；取消规则对用户可解释、对门店可执行。",
            "<ol>"
            "<li><b>门店态：</b>接单→制作中→出餐→完成；制作中为不可逆点。</li>"
            "<li><b>高峰：</b>限流+厨房队列；展示排队/出餐时效。</li>"
            "<li><b>券核销：</b>实例状态机；核销幂等键；与分摊联动。</li>"
            "<li><b>取消：</b>读制作态决策全退/餐损；幂等取消令牌。</li>"
            "<li><b>对账：</b>门店实收 vs 平台券结算。</li>"
            "</ol>",
            [
                ("门店回传制作态+规则引擎", "可解释", "中", "中", "<b>推荐</b>"),
                ("固定下单后 N 分钟不可取消", "粗", "高", "低", "MVP"),
                ("门店人工电话改单", "差", "低", "高", "应淘汰"),
            ],
            "diag-ency-case-food",
            "flowchart TD\n"
            "  Order[用户下单] --> Shop[门店接单]\n"
            "  Shop --> Cook[制作中不可逆]\n"
            "  Cook --> Ready[出餐]\n"
            "  Cancel[取消] --> Gate{已制作?}\n"
            "  Gate -->|否| Full[全退+释券]\n"
            "  Gate -->|是| Loss[餐损规则]\n"
            "  Coupon[券] --> Verify[核销幂等]\n"
            "  Verify --> Order\n",
            "<ul><li>取消接口非幂等→重复退。</li><li>券核销与支付回调乱序。</li>"
            "<li>高峰无队列→门店接单雪崩。</li></ul>",
            "<p>中厂：一张「制作态」枚举+取消规则配置表就能落地；"
            "交叉 <a href='#ency-biz-food'>ENCY-BIZ-FOOD</a>、<a href='#bx-food-peak'>B-X 餐饮高峰</a>。</p>",
            [
                (
                    "【落地】用户在制作中点取消，系统如何答？",
                    [
                        "读门店态；走餐损或拒绝全退并提示；记录审计。",
                        "餐饮。",
                        "一律全退。",
                        "状态决策。",
                        "「锅已下油，规则说话。」",
                    ],
                    "ency-case-food-q1",
                ),
            ],
            "ency-case-food-r1",
        )
    )

    parts.append(
        _case_block(
            "ency-case-ali",
            "ENCY-CASE · 阿里套路",
            "ENCY-CASE-ALI",
            "阿里集群：大促 · 中间件 · 单元化 / 限流降级（公开套路归纳）",
            "阿里系公开技术主题里反复出现：大促备战、中间件（网关/MQ/限流）、多单元/异地、降级开关——本质是「把故障域切小、把峰值削平」。",
            "峰值可卖可付；局部故障不全局雪崩；降级有清单可演练。",
            "<ol>"
            "<li><b>流量分层：</b>接入限流→热点隔离→库存预热。</li>"
            "<li><b>中间件：</b>网关、配置中心、MQ、分布式限流（公开产品思路可对标 Sentinel 等）。</li>"
            "<li><b>单元化思路：</b>用户/地域单元封闭，减少跨单元写。</li>"
            "<li><b>降级开关：</b>非核心（推荐/积分展示）可关；核心支付保护。</li>"
            "<li><b>演练：</b>全链路压测与故障注入（公开分享常见）。</li>"
            "</ol>",
            [
                ("网关限流+热点缓存+MQ 削峰", "最终", "高", "中", "<b>中厂大促常用</b>"),
                ("完整多活单元化", "高", "高", "很高", "体量不够慎上"),
                ("只加机器", "差", "短", "浪费", "不可持续"),
            ],
            "diag-ency-case-ali",
            "flowchart TD\n"
            "  Traffic[大促流量] --> GW[网关限流]\n"
            "  GW --> Hot[热点隔离]\n"
            "  Hot --> Core[核心下单支付]\n"
            "  Hot --> Deg[非核心降级]\n"
            "  Core --> MQ[异步削峰]\n"
            "  Core --> Unit[单元内闭环]\n",
            "<ul><li>降级无名单→误关支付。</li><li>压测不带回调/DB→上线失真。</li>"
            "<li>单元化未改数据访问→假多活。</li></ul>",
            "<p>中厂：先网关限流+降级开关+热点 SKU；单元化留到多地域有强需求。"
            "交叉 <a href='#x-promo-trinity'>X-大促</a>、<a href='#t-k8s-x'>T-K8s-X</a>。</p>",
            [
                (
                    "【落地】大促先做哪三件事？",
                    [
                        "核心链路识别、限流降级清单、带回调的压测。",
                        "备战。",
                        "先拆微服务。",
                        "清单+压测。",
                        "「先保支付，再谈花活。」",
                    ],
                    "ency-case-ali-q1",
                ),
            ],
            "ency-case-ali-r1",
        )
    )

    parts.append(
        _case_block(
            "ency-case-yonyou",
            "ENCY-CASE · 用友套路",
            "ENCY-CASE-YONYOU",
            "用友集群：企业数字化 · 中台/ERP 集成 · B2B 单据（公开套路归纳）",
            "企业数字化/ERP 公开实践常见：主数据统一、单据状态机、集成总线（或 iPaaS）、对账与权限——慢请求但强正确。",
            "B2B 单据从商机到应收应付可追溯；与电商订单域通过防腐层集成，不互相污染模型。",
            "<ol>"
            "<li><b>主数据：</b>客户/物料/组织统一编码。</li>"
            "<li><b>单据流：</b>订单-发货-应收状态机；驳回可逆点明确。</li>"
            "<li><b>集成：</b>API/消息+幂等；ERP 与交易中台 ACL。</li>"
            "<li><b>权限审计：</b>岗位职责分离；操作留痕。</li>"
            "<li><b>对账：</b>业务单据 vs 财务凭证。</li>"
            "</ol>",
            [
                ("中台单据+ERP 异步过账", "最终", "中", "中", "<b>常见</b>"),
                ("交易库直连改 ERP 表", "险", "短", "高", "<b>禁止</b>"),
                ("人工导 Excel", "差", "低", "隐形成本", "过渡可，勿长期"),
            ],
            "diag-ency-case-yonyou",
            "flowchart LR\n"
            "  CRM[商机/合同] --> SO[销售订单]\n"
            "  SO --> DN[发货单]\n"
            "  DN --> AR[应收]\n"
            "  SO --> ACL[防腐层]\n"
            "  ACL --> Mall[电商履约域]\n"
            "  AR --> ERP[ERP过账]\n",
            "<ul><li>两套物料编码未映射→发错货。</li><li>同步强堵 ERP→电商下单超时。</li>"
            "<li>无幂等重推→重复过账。</li></ul>",
            "<p>中厂：先 ACL+单据幂等；中台别一口吃成。「用友」此处指企业数字化公开套路，不绑定特定产品版本。</p>",
            [
                (
                    "【落地】电商单如何进 ERP 而不互相锁死？",
                    [
                        "异步过账+幂等凭证号；电商状态机独立；失败进补偿队列。",
                        "B2B。",
                        "同库事务硬绑。",
                        "ACL+异步。",
                        "「单据可追踪，系统可解耦。」",
                    ],
                    "ency-case-yonyou-q1",
                ),
            ],
            "ency-case-yonyou-r1",
        )
    )

    parts.append(
        _case_block(
            "ency-case-cmb",
            "ENCY-CASE · 招行套路",
            "ENCY-CASE-CMB",
            "招商银行集群：金融交易 · 风控 · 高可用（工程向·合规表述·公开套路归纳）",
            "银行系公开工程讨论常见：账务与渠道分离、风控分层、多活/容灾、审计与变更管控——"
            "表述保持合规：只谈工程能力，不谈未公开业务数据。",
            "资金类操作可审计、可回滚或可冲正；峰值与故障下核心可用；风险决策可解释、可人审。",
            "<ol>"
            "<li><b>账务：</b>流水先行、余额条件更新；热账户治理。</li>"
            "<li><b>渠道：</b>超时重试+幂等；对账文件闭环。</li>"
            "<li><b>风控：</b>同步规则+异步模型；高风险 HITL。</li>"
            "<li><b>高可用：</b>多副本、切换演练、变更窗口。</li>"
            "<li><b>合规工程：</b>最小权限、审计日志、敏感脱敏。</li>"
            "</ol>",
            [
                ("本地账务库+渠道适配+日终对账", "强/最终混合", "中高", "中", "<b>中厂支付常见</b>"),
                ("分布式库金融版", "看产品", "高", "高", "有编制再上"),
                ("风控全异步事后拦", "弱", "高", "低", "资损风险大"),
            ],
            "diag-ency-case-cmb",
            "flowchart TD\n"
            "  Req[交易请求] --> Risk[风控分层]\n"
            "  Risk -->|拒绝| End[拒绝原因码]\n"
            "  Risk -->|人审| HITL[人工]\n"
            "  Risk -->|通过| Acct[记账:流水→余额]\n"
            "  Acct --> Ch[渠道]\n"
            "  Ch --> Recon[对账]\n"
            "  HA[多活/演练] -.-> Acct\n",
            "<ul><li>先改余额后写流水。</li><li>对账差异口头抹平。</li>"
            "<li>演练从未切换→真故障不会切。</li></ul>",
            "<p>中厂支付：流水+幂等+对账三件套先于「中台名词」。"
            "交叉 <a href='#ency-biz-bank'>ENCY-BIZ-BANK</a>、<a href='#ency-d-dist'>ENCY-D-DIST</a>。"
            "表述仅工程向，不涉及未公开业务细节。</p>",
            [
                (
                    "【落地】渠道超时不知成功失败怎么办？",
                    [
                        "查询单+幂等键；本地态悬挂；对账兜底；禁盲目重扣。",
                        "支付。",
                        "直接再扣。",
                        "查证模式。",
                        "「未知当悬挂，对账收口。」",
                    ],
                    "ency-case-cmb-q1",
                ),
            ],
            "ency-case-cmb-r1",
        )
    )

    parts.append(
        _case_block(
            "ency-case-local",
            "ENCY-CASE · 美团饿了么套路",
            "ENCY-CASE-LOCAL",
            "美团 / 饿了么集群：本地生活高峰 · 配送 · 拼单（公开套路归纳）",
            "本地生活公开分享常见：高峰调度、骑手/运力匹配、拼单凑运力、状态回传——履约是「人货场+运力」动态优化。",
            "高峰仍能分配运力；用户可见送达预期；拼单/拼车规则不破坏接单承诺。",
            "<ol>"
            "<li><b>订单态：</b>支付→商家→骑手→送达。</li>"
            "<li><b>调度：</b>区域化分单；高峰潮汐运力。</li>"
            "<li><b>拼单：</b>合单约束（距离/时间窗）；失败回退普通单。</li>"
            "<li><b>体验：</b>ETA 预测；异常（恶劣天气）降级话术。</li>"
            "<li><b>结算：</b>骑手/商家账单与平台对账。</li>"
            "</ol>",
            [
                ("区域调度+状态回传+ETA", "最终", "高", "中", "<b>常见骨架</b>"),
                ("全局最优化每单求解", "理论优", "慢", "高", "峰值慎用"),
                ("不管运力只推单", "差", "短", "客诉", "不可取"),
            ],
            "diag-ency-case-local",
            "flowchart TD\n"
            "  Pay[支付成功] --> Shop[商家接单]\n"
            "  Shop --> Disp[运力调度]\n"
            "  Disp --> Ride[骑手取送]\n"
            "  Group[拼单] --> Disp\n"
            "  Ride --> ETA[ETA更新]\n"
            "  Ride --> Done[送达]\n",
            "<ul><li>拼单超时未回退→骑手空跑。</li><li>ETA 与真实态脱节→客诉。</li>"
            "<li>雨天无降级策略→超时爆炸。</li></ul>",
            "<p>中厂外卖/同城：先状态机+区域队列；拼单用时间窗规则即可。"
            "交叉 <a href='#ency-biz-logistics'>ENCY-BIZ-LOG</a>、<a href='#ency-biz-oms'>OMS</a>。</p>",
            [
                (
                    "【落地】拼单失败如何不影响已支付用户？",
                    [
                        "拼单会话与支付单解耦；失败自动转普通配送并重算运费规则（预先披露）。",
                        "本地生活。",
                        "卡在拼单态。",
                        "回退路径。",
                        "「拼单可失败，履约要闭环。」",
                    ],
                    "ency-case-local-q1",
                ),
            ],
            "ency-case-local-r1",
        )
    )

    parts.append(
        _case_block(
            "ency-case-dji",
            "ENCY-CASE · 大疆套路",
            "ENCY-CASE-DJI",
            "大疆集群：硬件 + 云 · 物联网 / 高可靠（公开向归纳）",
            "硬件+云公开工程主题常包括：设备身份与固件、遥测链路可靠、端云协同升级、售后 SN 追溯——可靠与安全优先于「炫功能」。",
            "设备可识别、指令可追踪、售后 SN 生命周期不断链；云侧故障不导致危险指令乱飞（安全设计）。",
            "<ol>"
            "<li><b>设备身份：</b>SN/证书；绑定用户。</li>"
            "<li><b>上行遥测：</b>可靠投递/补传；乱序处理。</li>"
            "<li><b>下行指令：</b>鉴权+幂等+回执。</li>"
            "<li><b>固件：</b>灰度升级；失败回滚。</li>"
            "<li><b>售后：</b>SN 态机与寄修/换新联动。</li>"
            "</ol>",
            [
                ("设备影子+消息回执+SN 态机", "高", "中", "中", "<b>可落地骨架</b>"),
                ("纯 HTTP 短轮询无回执", "弱", "低", "低", "不可靠场景慎"),
                ("云端直控无鉴权", "危险", "—", "—", "<b>禁止</b>"),
            ],
            "diag-ency-case-dji",
            "flowchart TD\n"
            "  Device[设备] -->|遥测| Cloud[云接入]\n"
            "  Cloud --> Shadow[设备影子/状态]\n"
            "  App[App/业务] --> Cmd[指令鉴权]\n"
            "  Cmd --> Device\n"
            "  Device --> Ack[回执]\n"
            "  SN[SN生命周期] --> AS[寄修换新]\n",
            "<ul><li>无回执以为成功。</li><li>固件全量一次推→变砖风险。</li>"
            "<li>售后忽略 SN 态→重复换新。</li></ul>",
            "<p>中厂硬件售后：先 SN 态机+寄修工单；云控做鉴权回执。"
            "交叉 <a href='#ency-biz-inv'>库存 SN</a>、<a href='#ency-biz-as'>售后</a>。</p>",
            [
                (
                    "【落地】换新如何迁移云端绑定？",
                    [
                        "旧 SN 退役、新 SN 绑定、权益迁移事务或补偿；双绑互斥。",
                        "硬件售后。",
                        "只改订单备注。",
                        "SN 态机。",
                        "「换新是身份迁移。」",
                    ],
                    "ency-case-dji-q1",
                ),
            ],
            "ency-case-dji-r1",
        )
    )

    parts.append(
        _case_block(
            "ency-case-sf",
            "ENCY-CASE · 顺丰套路",
            "ENCY-CASE-SF",
            "顺丰集群：物流轨迹 · 运单 · 仓干配协同（公开套路归纳）",
            "物流公开分享常见：运单为中心、轨迹事件化、仓-干-配协同、异常（拦截/退回）状态机——强调轨迹最终一致与节点回传。",
            "运单全程可追踪；仓出库与干线/配送节点事件可衔接；拦截/退回路径清晰。",
            "<ol>"
            "<li><b>运单模型：</b>运单号贯穿；关联订单/包裹。</li>"
            "<li><b>轨迹：</b>节点扫码事件入总线；用户可见态映射。</li>"
            "<li><b>仓干配：</b>出库→干线→末端派送状态机。</li>"
            "<li><b>异常：</b>拦截、退回、破损定责流程。</li>"
            "<li><b>协同：</b>与电商 OMS/WMS 事件对接，幂等。</li>"
            "</ol>",
            [
                ("运单事件总线+可见态映射", "最终", "高", "中", "<b>推荐</b>"),
                ("电商轮询物流官网", "弱", "差", "低", "仅兜底"),
                ("无运单只靠订单备注", "差", "—", "—", "禁止"),
            ],
            "diag-ency-case-sf",
            "flowchart LR\n"
            "  WMS[出库] --> Waybill[运单]\n"
            "  Waybill --> Trunk[干线]\n"
            "  Trunk --> Last[末端派送]\n"
            "  Last --> Sign[签收]\n"
            "  Waybill --> Trace[轨迹事件]\n"
            "  Intercept[拦截] --> Waybill\n",
            "<ul><li>轨迹乱序覆盖新态。</li><li>拦截指令无回执→以为召回成功。</li>"
            "<li>仓干配三套编码不映射。</li></ul>",
            "<p>中厂：运单表+轨迹事件+签收驱动售后窗；物流公司对接用适配器。"
            "交叉 <a href='#ency-biz-logistics'>ENCY-BIZ-LOG</a>、<a href='#ency-biz-wms'>WMS</a>。</p>",
            [
                (
                    "【落地】已发货未签收用户要退，先做什么？",
                    [
                        "查运单态→发起拦截→根据回执走退款或退货；公开套路强调态驱动。",
                        "逆向。",
                        "直接全退不管货。",
                        "拦截协议。",
                        "「货在路上先拦。」",
                    ],
                    "ency-case-sf-q1",
                ),
            ],
            "ency-case-sf-r1",
        )
    )

    # cross drill + mid-size cut
    parts.append(
        sec(
            "ency-case-cut",
            "ENCY-CASE · 中厂裁剪五问",
            "ENCY-CASE-CUT",
            "中厂裁剪五问 · 综合演练（多套路对照）",
            spine("把各集群公开套路收成决策清单，避免「大厂同款」空喊。", serves="方案评审", back="ENCY-CASE-* → 评审")
            + DISCLAIMER
            + plain("人话：每个套路问五次——体量？分片键/不可逆点？编制？演练？退出成本？")
            + """  <table>
    <thead><tr><th>五问</th><th>拼团/补贴</th><th>餐饮</th><th>大促</th><th>金融</th><th>物流</th></tr></thead>
    <tbody>
      <tr><td>体量是否到必须分布式？</td><td>名额热点</td><td>门店峰值</td><td>流量层</td><td>账务热户</td><td>轨迹吞吐</td></tr>
      <tr><td>不可逆点在哪？</td><td>成团/预算</td><td>制作中</td><td>支付成功</td><td>记账成功</td><td>出库/签收</td></tr>
      <tr><td>编制能否运维？</td><td>对账即可</td><td>门店回传</td><td>开关演练</td><td>容灾演练</td><td>承运适配</td></tr>
      <tr><td>失败怎么对用户说？</td><td>自动退</td><td>餐损规则</td><td>降级提示</td><td>原因码</td><td>拦截结果</td></tr>
      <tr><td>退出/降级成本？</td><td>关活动</td><td>关拼单</td><td>关非核心</td><td>只读/排队</td><td>换承运商</td></tr>
    </tbody>
  </table>
"""
            + mermaid(
                "diag-ency-case-cut",
                "flowchart TD\n"
                "  Q1[体量?] -->|不够| Simple[单单元+缓存+对账]\n"
                "  Q1 -->|够| Q2[不可逆点清晰?]\n"
                "  Q2 -->|否| Model[先补状态机]\n"
                "  Q2 -->|是| Q3[能演练?]\n"
                "  Q3 -->|否| Drill[先做演练与开关]\n"
                "  Q3 -->|是| Land[落地公开套路裁剪版]\n",
            )
            + qa(
                "【综合】中厂同时做拼团 + 餐饮外卖，如何避免两套峰值方案互相抄错？",
                [
                    "拼团看名额/预算；餐饮看制作态/运力——不可逆点不同；公用的是限流、幂等、对账，不要共用错误状态机。",
                    "评审。",
                    "一套状态打天下。",
                    "分域状态机。",
                    "「峰值手段可共用，业务态不能混。」",
                ],
                "ency-case-cut-q1",
            )
            + qa(
                "【综合】要把「阿里大促单元化」写进方案，评审怎么挡？",
                [
                    "要数据访问封闭与演练编制；否则降级为限流+降级+热点。标注公开套路，不装内部实践。",
                    "架构评审。",
                    "点名大厂压人。",
                    "五问裁剪。",
                    "「学骨架，别贴标。」",
                ],
                "ency-case-cut-q2",
            )
            + koujue("裁剪口诀：五问不过就不上复杂度。")
            + reflect("ency-case-cut-r1"),
            "p1",
        )
    )

    return "\n".join(parts)
