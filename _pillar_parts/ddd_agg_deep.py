# -*- coding: utf-8 -*-
"""S-DDD-AGG · 聚合根：唯一性 · 加载 · 一致性（生产级深节）"""
from helpers import (
    qa, c4, five, mermaid, spine, plain, koujue, today, floor, conf,
    tradeoff, ban, checklist, reflect, failbox, runbook,
)
from anti_water_boost import industry_cases, two_mmds


def build_agg() -> str:
    return f"""
<section class="block" id="s-ddd-agg" data-toc="S-DDD-X · 聚合根唯一性加载一致性" data-prio="p0" data-tags="ddd aggregate uniqueness load">
  <h2><span class="sys-id">S-DDD-AGG</span>聚合根：唯一性 · 加载 · 一致性（生产级）</h2>
{spine("面试/进组高频刀口：聚合根如何保证业务唯一？为何一 load 就慢？如何既快又正确？本节强制多层保证+源码示意+跨行业案+详答。",
       serves="B-F 下单支付 · B-R 售后寄修 · 对账幂等",
       back="S-DDD-X hub → 本页 → #s-ddd-x-bc / B-X")}
{plain("人话：聚合根不是「一个大对象」。它是<strong>一致性边界的门卫</strong>——外面只能拿业务单号找它；门卫保证「同单不会开两张、状态跳不了、加载不会把十年轨迹塞进一次 SQL」。唯一性靠多层（业务键+DB+并发+号段），不是靠「先查再插」碰运气。")}
{c4(
    "同一买家连点/渠道重试不能开出两张同业务键订单；售后/支付意图号全局可对账；加载命令路径要秒级可响应。",
    "业务唯一键落唯一索引+幂等表；聚合内 version/条件更新；仓储按命令最小图 reconstitution；读模型与写模型分离。",
    "不变式在 create/command 强制；跨请求唯一靠 DB 约束而非内存；加载慢根因是聚合过大/N+1/懒加载陷阱/塞进非一致性数据。",
    "任意单号：能证明唯一、能解释冲突、能在压测下保持 P99；客诉「重复单/加载转圈」可定位到键或加载图。",
    "峰值双写+热点聚合行是资损与超时双重雷区。",
)}

  <h3 id="s-ddd-agg-uniq">A. 唯一性如何保证（多层）</h3>
  <table>
    <thead><tr><th>层</th><th>保证什么</th><th>订单域例子</th><th>失败时人话</th></tr></thead>
    <tbody>
      <tr><td><b>业务唯一键</b></td><td>业务语义「同一笔意图只成功一次」</td><td>订单号 <code>orderNo</code>、售后单号、支付意图号 <code>payIntentNo</code>、客户端 <code>idempotency-key</code></td><td>技术自增 ID 永远涨，但业务上仍可能开两张「同购物车提交」</td></tr>
      <tr><td><b>技术主键</b></td><td>行定位 / 分片路由</td><td>雪花/号段 <code>id</code>；与业务键分离</td><td>别拿自增当业务单号对外暴露（泄漏量级+难迁）</td></tr>
      <tr><td><b>DB 约束</b></td><td>跨进程最终防线</td><td><code>UNIQUE(order_no)</code>、<code>UNIQUE(user_id, client_token)</code>、幂等表 <code>UNIQUE(biz_type, biz_key)</code></td><td>应用「先查后插」在并发下必穿；唯一索引冲突才是权威</td></tr>
      <tr><td><b>并发控制</b></td><td>同聚合更新不丢改/不双改</td><td>乐观锁 <code>version</code>；热点行悲观 <code>SELECT … FOR UPDATE</code></td><td>两个退款线程都读到可退→双退</td></tr>
      <tr><td><b>分布式发号</b></td><td>全局或分片内不撞号</td><td>号段（美团 Leaf 取向）、雪花、DB 步长；分片内唯一+映射表</td><td>多机 UUID 能唯一但不适合当作有序业务单号/索引友好键</td></tr>
    </tbody>
  </table>

{floor(
    "唯一性与不变式强制点",
    "不变式例：①同一 <code>clientToken</code> 仅一单；②订单实付=行合计−分摊（分内）；③状态仅允许迁移表边；④支付成功后不可直接删行。强制点：<b>create</b>（工厂校验+落唯一键）→ <b>load</b>（完整性，行缺失即损坏）→ <b>command</b>（方法内校验+version）→ <b>save</b>（唯一冲突/版本冲突翻译成领域错误）。",
    "示意路径：<code>CreateOrderAppService</code> → <code>OrderAgg.create(cmd)</code> → <code>OrderRepository.save</code> → 捕获 <code>DuplicateKeyException</code> → 查已存在聚合返回「幂等成功」而非 500。<code>RefundAppService</code> → <code>repo.loadForUpdate(id)</code> → <code>agg.applyRefund</code> → <code>UPDATE … SET version=version+1 WHERE version=?</code>。",
    "连点下单：两请求同时通过「先查无单」→ 无唯一索引则双单；有唯一索引则一成功一冲突转幂等。售后双点：无 version 则双退款单。",
    "看：唯一键冲突 QPS（应为幂等命中）、version 冲突率、重复支付/重复退款监控=0、对账「同 client_token 多单」日终=0。",
)}

{conf("OrderAgg.create / Repository.save（冲突处理伪代码）", """// 领域：只认业务键与不变式
public static OrderAgg create(CreateOrderCmd c) {
  Objects.requireNonNull(c.clientToken());
  if (c.lines().isEmpty()) throw new DomainEx("EMPTY_LINES");
  Money pay = Lines.total(c.lines()).minus(c.discountSnapshot());
  return new OrderAgg(OrderNo.of(c.orderNo()), c.clientToken(), c.lines(),
                      pay, Status.CREATED, 0L);
}

// 应用+仓储：DB 唯一约束是跨请求唯一的真理
@Transactional
public OrderId create(CreateOrderCmd c) {
  OrderAgg agg = OrderAgg.create(c);
  try {
    return orderRepo.insert(agg); // INSERT orders + items + discount_snapshot + outbox
  } catch (DuplicateKeyException dup) {
    OrderAgg existed = orderRepo.mustFindByClientToken(c.userId(), c.clientToken());
    return existed.id(); // 幂等：返回原单，不开第二张
  }
}

// 命令更新：乐观锁
public void pay(OrderId id, PayCmd cmd) {
  OrderAgg agg = orderRepo.load(id);           // 最小图：头+支付意图+必要行
  agg.markPaid(cmd.tradeNo());                 // 内含状态迁移守卫
  int n = orderRepo.saveWithVersion(agg);      // UPDATE ... WHERE version=?
  if (n == 0) throw new ConflictEx("ORDER_VERSION"); // 让上层重试或409
}
""")}

  <h4>并发：同聚合乐观/悲观；跨请求仍唯一</h4>
  <ul>
    <li><b>同聚合多命令</b>：默认乐观锁 version；冲突率高的热点（秒杀库存行）再悲观或改成分段库存，不把整单 FOR UPDATE 包 HTTP。</li>
    <li><b>跨请求唯一</b>：两台机器各建一单——内存锁无效；必须落 <code>UNIQUE</code> 或幂等表 insert。</li>
    <li><b>防重 token</b>：网关/接口 <code>Idempotency-Key</code> → 幂等表（处理中/成功/失败+响应摘要）→ 聚合业务键双保险。</li>
  </ul>

  <h4>分布式发号：全局唯一 vs 分片唯一</h4>
  <table>
    <thead><tr><th>方案</th><th>特点</th><th>坑</th><th>订单域建议</th></tr></thead>
    <tbody>
      <tr><td>号段（Leaf-segment 取向）</td><td>吞吐高、可含业务前缀</td><td>号段丢失造成号洞（可接受）；中心依赖</td><td><b>业务单号常用</b></td></tr>
      <tr><td>雪花</td><td>本地发号、趋势递增</td><td>时钟回拨；workerId 管理</td><td>技术主键 / 部分单号</td></tr>
      <tr><td>分片内唯一+全局映射</td><td>片内自增快</td><td>跨片查询要映射</td><td>分库后订单号仍建议全局发号器</td></tr>
      <tr><td>UUID</td><td>易唯一</td><td>索引页分裂、难读</td><td>作关联 token，慎作聚簇主键</td></tr>
    </tbody>
  </table>

{mermaid("diag-ddd-agg-uniq-fail", '''flowchart TD
  A[请求A clientToken=T1] --> CA[OrderAgg.create]
  B[请求B clientToken=T1] --> CB[OrderAgg.create]
  CA --> IA[INSERT orders]
  CB --> IB[INSERT orders]
  IA -->|成功| OK[返回订单号]
  IB -->|UNIQUE冲突| DUP[DuplicateKey]
  DUP --> LOAD[按 token 加载已存在聚合]
  LOAD --> IDEM[幂等返回同一订单号]
  OK --> OUT[同事务 Outbox]
  IDEM --> SKIP[不再发第二条创建事件]
''')}

  <h3 id="s-ddd-agg-load">B. 加载为什么慢 · 如何保证性能与正确</h3>
  <table>
    <thead><tr><th>慢因</th><th>人话</th><th>正确做法</th></tr></thead>
    <tbody>
      <tr><td>大聚合</td><td>把「用户一生订单」塞进一个根</td><td>按一致性边界切：一单一根；历史列表走读模型</td></tr>
      <tr><td>N+1</td><td>头一行循环查行/券/轨迹</td><td>仓储一次 SQL/IN 批量；或明确的两段查询</td></tr>
      <tr><td>行项目过多</td><td>B2B 上千行一次 hydrate</td><td>命令只需改部分行时按行 ID 子集加载；汇总字段冗余在头</td></tr>
      <tr><td>快照过大</td><td>优惠/报关 XML 塞聚合每次加载</td><td>大对象外置对象存储，聚合只持引用+哈希</td></tr>
      <tr><td>懒加载陷阱</td><td>JPA 出了事务再碰 collection → 爆炸或 N+1</td><td>DDD 仓储显式 reconstitution；禁 Open Session In View 当设计</td></tr>
      <tr><td>一次加载历史售后</td><td>订单详情把 3 年售后单 join 进来</td><td>售后是另一聚合；详情页 CQRS 读模型拼装</td></tr>
    </tbody>
  </table>

{floor(
    "最小图 reconstitution",
    "命令要什么就加载什么：<code>loadForPay(orderId)</code>→头+支付意图+状态+version；<code>loadForRefund</code>→头+分摊快照+可退行。禁止 <code>findById</code> 默认 fetch join 全世界。轨迹/评论/客服备注/物流细节点不进写侧聚合。",
    "仓储接口按用例：<code>OrderRepository.loadForCommand(OrderId, LoadGraph)</code>；实现用显式 SQL/MyBatis，不靠魔法懒加载。<b>快照 vs 事件溯源：</b>中厂默认状态快照+领域事件出站；事件溯源仅在审计极强且团队熟时用——坑是重放版本漂移、快照滞后、运维复杂。",
    "客服开详情：ORM 把 order_items+after_sales+tracks 全拉 → RT 3s+；大促支付标已付却因加载慢超时重试 → 靠幂等救命。",
    "看：慢 SQL（rows examined）、聚合加载 P99、一次 load 行数直方图、OSIV 开关、是否在事务外触懒加载异常。",
)}

  <h4>缓存聚合？一般不要；缓存读模型</h4>
  <ul>
    <li><b>写侧聚合</b>：缓存易脏（多实例改 version）、穿透一致性难；默认不缓存，靠主键点查+连接池。</li>
    <li><b>读模型</b>：订单列表/详情卡可缓存；失效用订单号维度删除；允许短暂旧读，付后关键态读主。</li>
  </ul>

  <h4>拆分过大聚合的信号与步骤</h4>
  <ol>
    <li><b>信号</b>：单聚合表&gt;5 且常一起锁；加载 P99&gt;200ms；无关用例互相阻塞；团队争议「改优惠却要锁订单整图」。</li>
    <li><b>步骤</b>：标出不变式集合→切开只需最终一致的部分（轨迹/评论/售后）→引用改 ID→补对账/事件→压测对比加载行数。</li>
  </ol>

{runbook("加载慢 / 慢 SQL 排查清单", """<ol>
<li>慢日志：<code>long_query_time</code>；抓到 SQL 做 <code>EXPLAIN</code>（type/rows/Extra）。</li>
<li>是否 select * + 大 JSON；是否无 order_id 索引；是否深分页。</li>
<li>应用：一次命令加载实体数；N+1 计数（datasource-proxy / p6spy）。</li>
<li>是否 OSIV；是否详情接口误走写侧仓储。</li>
<li>治理：加读模型接口；缩 LoadGraph；大字段外置；必要时拆聚合。</li>
</ol>""")}

{mermaid("diag-ddd-agg-load-goodbad", '''flowchart TB
  subgraph Bad[坏的加载]
    B1[详情/支付同一 findById] --> B2[join 行+售后+轨迹+评论]
    B2 --> B3[事务长 + P99爆]
  end
  subgraph Good[好的加载]
    G1[PayCmd] --> G2[loadForPay 最小图]
    G3[客服详情] --> G4[CQRS 读模型拼装]
    G5[售后命令] --> G6[AfterSale 聚合独立加载]
  end
''')}

  <h3 id="s-ddd-agg-cases">C. 跨行业案例（场景·选型·坑·步骤·量级）</h3>
{industry_cases("ddd-agg", [
    ("电商订单（综合零售取向）",
     "大促连点下单 + 支付回调并发；客服详情要看轨迹但不该拖垮支付标已付",
     "业务键 orderNo+clientToken 唯一索引；支付命令最小图；详情走读模型；version 乐观锁",
     "先查后插无唯一索引→双单；JPA 默认懒加载把售后集合带进支付事务",
     "①幂等表+唯一索引 ②LoadGraph 分用例 ③OSIV 关闭 ④压测连点与回调重放",
     "工程目标：连点双单=0；支付命令 P99 回到百 ms 级（示意，非某厂未公开 KPI）"),
    ("银行账户（分户账取向）",
     "同账户借贷并发；跨户转账不能一个聚合锁两户到超时",
     "账户聚合强一致+凭证；跨户用记账凭证/Saga；技术主键与账号分离；日终对账",
     "长事务锁两账户→死锁；用缓存账户余额当账本",
     "①单户命令短事务 ②跨户异步凭证 ③余额以分户账为准 ④日终三方平",
     "工程目标：日终平账；热点户冲突可重试且无双花（示意）"),
    ("物流运单",
     "运单状态唯一推进；轨迹点海量、乱序到达",
     "运单聚合只持状态/版本；轨迹独立写入+序号 upsert；运单号全局唯一",
     "轨迹当聚合内集合每次加载→RT 崩；无运单号唯一→重复运单",
     "①运单/轨迹拆分 ②waybillNo 唯一 ③轨迹按 seq 校正 ④读模型展示",
     "工程目标：轨迹乱序可校正；运单状态无回退脏写（示意）"),
    ("售后寄修",
     "用户连点申请；寄修∥换新并行时库存与状态不能双开冲突单",
     "售后单号唯一+（orderId,type,sku）条件唯一；售后聚合独立；换新预占另一事务",
     "把历史寄修记录塞进订单聚合；无唯一键双售后单双退",
     "①售后独立聚合 ②防重 token ③并行策略表 ④质检回执驱动分支",
     "工程目标：重复申请幂等；并行资损单=0（示意）"),
])}

  <h3 id="s-ddd-agg-qa">D. 详答题（唯一性与加载）</h3>
{qa("【详答】有技术主键了，为何还要业务唯一键？",
   ["技术主键只保证行身份；业务唯一键保证「同一业务意图」跨重试/跨实例只成功一次。对账、客服、渠道回调都认业务单号。缺业务唯一键时，自增 ID 再漂亮也会双单。",
    "支付回调重试、用户连点。", "只靠先查后插。", "UNIQUE(业务键)+幂等响应。", "「主键认行，业务键认意图。」"],
   "ddd-agg-q1")}
{qa("【详答】聚合加载慢，加 Redis 缓存聚合根可以吗？",
   ["一般不建议缓存写侧聚合：多实例更新 version、部分字段更新、与 DB 权威冲突时极难。应缩加载图+CQRS 读模型缓存。若缓存，只能短 TTL 且当提示，命令路径仍读库。",
    "详情 RT 差。", "缓存整个 Order 图当银弹。", "读模型缓存+写最小图。", "「缓存读模型，别缓存门卫。」"],
   "ddd-agg-q2")}
{qa("【详答】乐观锁冲突频繁怎么办？会不会丢唯一性？",
   ["唯一性仍由唯一索引保证；version 冲突只表示并发更新，应可重试命令或串行化热点。不要为了减少冲突去掉唯一约束。热点可拆行（库存分段）或排队。",
    "秒杀退款/标已付。", "去掉 version 或改用无约束。", "冲突指标+有限重试+拆热点。", "「冲突是信号，不是让你拆掉护栏。」"],
   "ddd-agg-q3")}
{qa("【详答】事件溯源是否能解决加载慢？",
   ["不一定。事件多了要快照；快照过大同样慢；重放与版本漂移是坑。中厂订单默认状态快照+Outbox 事件更稳。审计强需求再评估溯源。",
    "架构炫技。", "全站上溯源。", "写清 ADR：默认快照。", "「溯源是审计武器，不是默认加速器。」"],
   "ddd-agg-q4")}

{five(
    "钉：双单=0、双退=0、支付命令 P99、加载行数上限。",
    "拆：主=create/pay/refund 最小图；异=冲突重试；逆=售后独立聚合。",
    "标：先查后插、大聚合、缓存写侧、OSIV。",
    "选：业务键唯一+version+按命令加载；读走 CQRS。",
    "验：连点/重放压测、EXPLAIN、差账、慢 SQL 清零。",
)}
{ban("<ul><li>用「先查后插」代替唯一索引</li><li>支付命令 fetch join 售后/轨迹</li><li>缓存写侧聚合当真理</li><li>把用户历史订单做成一个聚合根</li></ul>")}
{koujue("聚合口诀：业务键唯一垫底，version 防并发，加载按命令最小图，轨迹售后别塞进根。")}
{reflect("ddd-agg-r1")}
</section>
"""


def thicken_bc() -> str:
    """Extra depth appended into #s-ddd-x-bc via anti-water marker."""
    return "\n".join([
        floor(
            "上下文切分与聚合唯一/加载挂钩",
            "每个上下文一张「写权威表」；订单聚合持单头+行+优惠成交快照+支付意图；库存/售后/轨迹不进订单写事务。跨上下文只传 ID+事件。唯一键落在写权威库，不靠他库 join 判重。",
            "包结构 <code>domain.order</code> / <code>domain.aftersale</code>；仓储接口按聚合；禁止他包 Mapper 写订单表。加载：订单命令不 load 售后集合。",
            "售后服务直写 orders.discount → 历史退款口径被改；详情 join 五库 → 慢与脏。",
            "看：跨库事务数、写权威违规 MR 扫描、订单命令 SQL 表集合。",
        ),
        two_mmds(
            "ddd-bc-deep",
            "唯一键落点（按上下文）",
            "flowchart TB\n  Ord[订单库 UNIQUE order_no/client_token]\n  Pay[支付库 UNIQUE pay_intent_no]\n  AS[售后库 UNIQUE after_sale_no]\n  Inv[库存库 UNIQUE reserve_no]\n  Ord -.事件.-> Inv\n  Pay -.回调幂等.-> Ord\n  AS -.读快照.-> Ord",
            "加载边界",
            "flowchart LR\n  Cmd[命令]-->Min[最小聚合图]\n  Query[客服查询]-->RM[读模型]\n  Min-->DB[(写库点查)]\n  RM-->RO[(RO/ES/宽表)]",
        ),
        industry_cases("ddd-bc", [
            ("电商", "优惠周更 vs 下单要快照", "规则上下文试算；成交快照进订单聚合；快照只读",
             "售后改 promo_rule 行", "①快照落库 ②退款只读快照 ③规则热更不影响历史",
             "工程目标：退款可解释；规则发布不改历史单（示意）"),
            ("银行", "分户与凭证", "账户聚合内强一致；跨户凭证异步",
             "跨户长事务", "①单户短事务 ②凭证 ③日终平",
             "工程目标：日终平（示意）"),
            ("物流", "运单 vs 轨迹", "运单聚合状态；轨迹上下文事件写入",
             "轨迹反写打乱状态", "①状态机守卫 ②轨迹 upsert ③读模型展示",
             "工程目标：状态单调可校正（示意）"),
            ("寄修售后", "订单与售后拆分", "售后聚合+订单快照引用",
             "售后挂订单集合懒加载", "①独立单号 ②独立加载 ③事件回补库存",
             "工程目标：售后洪峰不拖支付（示意）"),
        ]),
        qa("【详答】聚合边界划错，唯一性与加载会怎样？",
           ["边界过大：唯一约束难设计、加载必慢、锁争用高。边界过小：不变式跨库无法原子，只能靠补偿且易双单/双补。应按不变式集合切，不是按名词切。",
            "订单+库存+售后一张表家族。", "按微服务个数切聚合。", "不变式清单评审。", "「不变式决定边界，边界决定唯一与加载。」"],
           "ddd-bc-deep-q1"),
        today("""<ul>
<li>本周交付：五上下文写权威表 + 每表业务唯一键清单。</li>
<li>订单仓储拆 <code>loadForPay</code>/<code>loadForRefund</code>，禁万能 <code>getOrderDetail</code> 上写路径。</li>
<li>连点与回调重放压测各 1 条用例进 CI。</li>
</ul>"""),
    ])


def thicken_hub() -> str:
    return "\n".join([
        plain("总图之下必读深节：<a href='#s-ddd-agg'>#s-ddd-agg 聚合根：唯一性·加载·一致性</a>——勿只停在上下文地图。"),
        industry_cases("ddd-hub", [
            ("电商订单/优惠",
             "规则周更，成交口径要冻结；大促连点不能双单",
             "优惠上下文外置规则；订单聚合内折扣快照；orderNo+clientToken 唯一；支付最小图加载",
             "售后 UPDATE 历史规则行；详情把轨迹 join 进写模型；先查后插",
             "①快照只读 ②唯一索引+幂等 ③CQRS 详情 ④见 #s-ddd-agg",
             "工程目标：退款可解释；双单=0（示意）"),
            ("银行分户",
             "账户并发借贷与日终平账",
             "账户聚合强一致+version；跨户凭证；账号业务键与技术主键分离",
             "跨户长事务死锁；缓存余额当账本",
             "①短事务 ②凭证异步 ③日终三方对账",
             "工程目标：日终平；无双花（示意）"),
            ("物流运单",
             "运单状态唯一推进，轨迹高并发乱序",
             "运单聚合+轨迹上下文；waybillNo 唯一；轨迹 seq upsert",
             "轨迹塞进运单集合每次加载；无唯一键重复运单",
             "①拆轨迹 ②强制运单号 ③读模型",
             "工程目标：展示可校正；状态无脏回退（示意）"),
            ("餐饮门店履约",
             "高峰店维度热点，订单与门店主数据分离",
             "门店/订单上下文分离；店维度分区/限流；订单业务键唯一",
             "中央库硬锁门店行；大聚合加载出餐队列",
             "①店维拆分 ②出餐读模型 ③高峰降级非核心",
             "工程目标：午高峰可扩、取消可解释（示意）"),
        ]),
        two_mmds(
            "ddd-hub",
            "订单域上下文地图",
            "flowchart TB\n  Promo[优惠]-->Snap[快照进订单]\n  Order[订单]-->Stock[库存预占事件]\n  Order-->Pay[支付]\n  Pay-->OMS[履约]\n  AS[售后]-->Snap\n  AS-->Refund[退款]",
            "聚合事务边界",
            "flowchart LR\n  Cmd[命令]-->AR[聚合根校验]\n  AR-->DB[(本上下文库)]\n  AR-->OB[Outbox事件]\n  OB-->Other[其他上下文]",
        ),
    ])
