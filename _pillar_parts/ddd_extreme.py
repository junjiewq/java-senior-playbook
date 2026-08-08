# -*- coding: utf-8 -*-
"""DDD + 设计模式 + 架构思维 · 落到订单域（含聚合根唯一性/加载深节）"""
from ddd_agg_deep import build_agg, thicken_hub
from helpers import (
    qa, c4, five, tradeoff, mermaid, spine, plain, koujue,
    reflect, today, checklist, conf, floor, ban,
)


def build() -> str:
    hub = f"""
<section class="block" id="s-ddd-x" data-toc="S-DDD-X · 订单域DDD与模式" data-prio="p0">
  <h2><span class="sys-id">S-DDD-X</span>DDD · 设计模式 · 架构思维（落到订单/售后）</h2>
{spine("聚合怎么切、唯一性/加载怎么保证、模式对应哪条优惠/售后需求、单体模块化 vs 微服务怎么拍板——全是改代码用的，不背定义。",
       serves="B-F 结算履约 · B-R 售后",
       back="S2 → 本页 → <a href='#s-ddd-agg'>#s-ddd-agg</a> / S-MS-X / B-X")}
{plain("人话：DDD 不是画六边形好看。问三句就够——谁能改这张表？状态谁说了算？跨系统脏模型谁翻译？再加两刀：<b>唯一性如何多层保证</b>？<b>加载为何慢、如何又快又对</b>？深答见 <a href='#s-ddd-agg'>#s-ddd-agg</a>。")}
  <table>
    <thead><tr><th>子章</th><th>锚点</th></tr></thead>
    <tbody>
      <tr><td><b>聚合根：唯一性 · 加载 · 一致性</b></td><td><a href="#s-ddd-agg">#s-ddd-agg</a></td></tr>
      <tr><td>聚合 / 限界上下文怎么切</td><td><a href="#s-ddd-x-bc">#s-ddd-x-bc</a></td></tr>
      <tr><td>防腐层 · 领域事件 · 应用服务</td><td><a href="#s-ddd-x-acl">#s-ddd-x-acl</a></td></tr>
      <tr><td>模式对照真实需求</td><td><a href="#s-ddd-x-patterns">#s-ddd-x-patterns</a></td></tr>
      <tr><td>架构权衡与模块化 vs 微服务</td><td><a href="#s-ddd-x-arch">#s-ddd-x-arch</a></td></tr>
    </tbody>
  </table>
""" + thicken_hub() + f"""
{reflect("dddx-hub-r1")}
</section>
"""

    agg = build_agg()

    bc = f"""
<section class="block" id="s-ddd-x-bc" data-toc="S-DDD-X · 聚合与上下文切分" data-prio="p0">
  <h2><span class="sys-id">S-DDD-X</span>聚合 / 限界上下文：订单·优惠·库存·履约·售后</h2>
{c4(
    "五拨人别抢同一张订单表改库存字段；退款时要找得到「当时优惠快照」；同一 clientToken 不能开两单。",
    "订单聚合持单头+行+支付意图+优惠快照；优惠上下文持规则；库存持预占；OMS 持履约单；售后持售后单+退款单。唯一键落各自写权威库。",
    "聚合=事务与不变性边界；跨上下文用 ID+事件，不 join 他库。加载按命令最小图——详见 <a href='#s-ddd-agg'>#s-ddd-agg</a>。",
    "任意单号能指出写库服务；禁止售后 UPDATE 原优惠规则行；双单/双退=0。",
    "峰值下同步双写最容易资损。",
)}
{mermaid("diag-ddd-bc", '''flowchart LR
  subgraph OrderCtx[订单上下文]
    Ord[Order聚合]
  end
  subgraph PromoCtx[优惠上下文]
    Rule[规则/试算]
  end
  subgraph InvCtx[库存上下文]
    Res[预占/扣减]
  end
  subgraph FulfillCtx[履约上下文]
    OMS[履约单]
  end
  subgraph ASCtx[售后上下文]
    AS[售后单]
  end
  Rule -->|快照结果| Ord
  Ord -->|预占意图事件| Res
  Ord -->|支付成功事件| OMS
  AS -->|读快照/回补事件| Ord
  AS --> Res
''')}
  <table>
    <thead><tr><th>上下文</th><th>写权威表（例）</th><th>业务唯一键</th><th>别的上下文只能</th><th>今天代码怎么约束</th></tr></thead>
    <tbody>
      <tr><td>订单</td><td>orders, order_item, discount_snapshot</td><td>order_no / (user_id, client_token)</td><td>读快照 / 发事件</td><td>包 <code>order</code> 外禁止写 mapper</td></tr>
      <tr><td>优惠</td><td>promo_rule, coupon</td><td>rule_id+version</td><td>RPC 试算返回 DTO</td><td>规则热更不影响历史快照</td></tr>
      <tr><td>库存</td><td>sku_stock, stock_reserve</td><td>reserve_no</td><td>收事件确认/释放</td><td>无订单库账号</td></tr>
      <tr><td>履约</td><td>fulfillment_order</td><td>fulfillment_no / order_no</td><td>收支付成功</td><td>Inbox 去重</td></tr>
      <tr><td>售后</td><td>after_sale, refund</td><td>after_sale_no / refund_no</td><td>读订单快照</td><td>回退分摊写售后侧表</td></tr>
    </tbody>
  </table>
{today("""<ul>
<li>新建包：<code>domain.order</code> / <code>domain.stock</code>…；跨包只依赖接口或事件 DTO。</li>
<li>下单事务：写订单+快照+outbox，<b>不</b>写库存表；clientToken 唯一索引。</li>
<li>评审检查：有没有跨服务 join、有没有售后改历史规则、写路径是否万能大 join。</li>
<li>必读：<a href="#s-ddd-agg">#s-ddd-agg</a> 唯一性多层与加载最小图。</li>
</ul>""")}
{qa("【实战】优惠常变要独立服务，下单又要同事务——怎么切？",
    ["试算同步短超时；落单把结果拷进 discount_snapshot；规则服务可独立部署。退款只读快照。唯一性在订单库业务键，不靠优惠库锁。",
     "规则周更。", "订单库存可变脚本。", "快照表+版本号+订单唯一键。", "「可变规则外置，成交结果内聚。」"],
    "ddd-bc-q1")}
{reflect("ddd-bc-r1")}
</section>
"""

    acl = f"""
<section class="block" id="s-ddd-x-acl" data-toc="S-DDD-X · 防腐层事件应用服务" data-prio="p0">
  <h2><span class="sys-id">S-DDD-X</span>防腐层 · 领域事件 · 应用服务（今天怎么写）</h2>
{plain("人话：物流公司字段乱七八糟，别渗进你的售后单——中间加翻译层（ACL）。领域事件=「我这边事成了，你看着办」。应用服务=用例导演，不塞一堆业务 if。")}
{floor(
    "应用层与领域层调用链（落地认知）",
    "Controller→ApplicationService（事务边界）→聚合根方法（不变性）→仓储保存→同一事务写 Outbox。领域事件可进程内先应用到聚合，再落库发出。",
    "典型类：<code>RefundAppService.apply</code> → <code>AfterSale.approve</code> → <code>AfterSaleRepository.save</code> → <code>OutboxRepository.insert</code>。禁在 Controller 直接改三张表。",
    "物流回传状态码直接写进售后枚举→承运商一改你全库脏。ACL 译成内部 <code>IN_TRANSIT/SIGNED</code>。",
    "看：是否存在「上帝 Service」三千行；Outbox 与业务是否同事务（抽查事务日志/代码）。",
)}
{conf("应用服务骨架（示意）", """@Transactional
public void onPaid(PaidCmd cmd) {
  Order order = orderRepo.lockById(cmd.orderId());
  order.markPaid(cmd.tradeNo());          // 聚合内校验状态
  orderRepo.save(order);
  outbox.save(OrderPaidEvent.of(order)); // 同事务
}
""")}
{today("""<ul>
<li>物流/支付渠道包一层 <code>XxxAcl</code>，对外只暴露内部枚举。</li>
<li>写路径事件：先表后发（Outbox），别先发 MQ 再写库。</li>
<li>应用服务按用例命名：<code>CreateOrder</code>/<code>ApplyRefund</code>，别 <code>OrderManager</code>。</li>
</ul>""")}
{reflect("ddd-acl-r1")}
</section>
"""

    patterns = f"""
<section class="block" id="s-ddd-x-patterns" data-toc="S-DDD-X · 模式对照真实需求" data-prio="p0">
  <h2><span class="sys-id">S-DDD-X</span>策略 / 责任链 / 状态 / 工厂 / 模板 / 观察者——对照需求</h2>
  <table>
    <thead><tr><th>模式</th><th>真实需求（订单域）</th><th>今天怎么改代码</th><th>若不用会怎样</th></tr></thead>
    <tbody>
      <tr><td><b>策略</b></td><td>满减/折扣/券互斥算法可替换</td><td><code>DiscountStrategy</code> 接口+按 type 选实现；试算入口只调接口</td><td>巨大 if-else，大促改规则易发错版</td></tr>
      <tr><td><b>责任链</b></td><td>下单校验：库存→风控→限购→优惠</td><td><code>Checker</code> 链，失败短路；可配置顺序</td><td>校验散落控制器，漏限购</td></tr>
      <tr><td><b>状态</b></td><td>售后：待审→寄回→质检→退款</td><td>枚举+允许迁移表/<code>AfterSaleFSM</code>；非法迁移抛错</td><td>任意 UPDATE 状态→跳态资损</td></tr>
      <tr><td><b>工厂</b></td><td>创建售后单（仅退款/退货/寄修）不同类型</td><td><code>AfterSaleFactory.create(type, cmd)</code> 填初始状态与必填项</td><td>构造函数爆炸、漏字段</td></tr>
      <tr><td><b>模板方法</b></td><td>支付回调：验签→幂等→改态→发事件</td><td>抽象 <code>AbstractPayCallback</code>，渠道子类只实现验签/解析</td><td>每渠道复制粘贴漏幂等</td></tr>
      <tr><td><b>观察者/事件</b></td><td>支付成功通知 OMS、积分、短信</td><td>Outbox 事件；听者各自幂等</td><td>支付服务同步调五方，雪崩</td></tr>
    </tbody>
  </table>
{today("""<ul>
<li>本周只落地两件：① 售后状态迁移表 ② 支付回调模板方法抽公共幂等。</li>
<li>优惠策略：新活动加类，不改老策略类。</li>
<li>代码评审勾选：有没有「模式套娃」无需求？有则删。</li>
</ul>""")}
{conf("状态迁移守卫（示意）", """boolean canTransit(Status from, Status to) {
  return ALLOWED.getOrDefault(from, Set.of()).contains(to);
}
// APPROVED 只能走向 WAIT_BUYER_SHIP 或 REFUNDING，不能直接 REFUNDED 跳质检
""")}
{qa("【实战】寄修与退货并行，状态机怎么切？",
    ["售后单类型分状态机，或并行子单；库存预占用事件。禁止一个枚举硬塞所有分支。挂 B-X 寄修案。唯一性：售后单号+(orderId,type) 条件唯一。",
     "售后洪峰。", "布尔标志满天飞。", "类型+子状态。", "「并行就拆单或子状态，别叠 flag。」"],
    "ddd-pat-q1")}
{reflect("ddd-pat-r1")}
</section>
"""

    arch = f"""
<section class="block" id="s-ddd-x-arch" data-toc="S-DDD-X · 架构权衡与拆分" data-prio="p0">
  <h2><span class="sys-id">S-DDD-X</span>架构思维：权衡表 · 模块化单体 vs 微服务</h2>
  <h3 id="ddd-tradeoff-dim">权衡维度（拍板用）</h3>
  <table>
    <thead><tr><th>维度</th><th>问什么</th><th>订单域例子</th></tr></thead>
    <tbody>
      <tr><td>一致性</td><td>能否最终一致？窗口多大？</td><td>支付→OMS 秒级可接受</td></tr>
      <tr><td>延迟</td><td>用户同步等待哪些？</td><td>试算&lt;100ms；OMS 异步</td></tr>
      <tr><td>吞吐/热点</td><td>哪张表/哪个 SKU 热点？</td><td>库存独立扩展</td></tr>
      <tr><td>团队</td><td>几人维护？有无平台组？</td><td>8 人慎细拆</td></tr>
      <tr><td>故障面</td><td>挂了伤支付还是伤推荐？</td><td>支付链路独立池/进程</td></tr>
      <tr><td>变更频率</td><td>谁周周发、谁稳定？</td><td>优惠规则 vs 支付</td></tr>
      <tr><td>合规</td><td>数据能否共库？</td><td>部分渠道密钥隔离</td></tr>
    </tbody>
  </table>
{tradeoff("进程形态", [
    ("模块化单体+包边界", "同库事务简单", "扩展一体", "低运维", "<b>中厂默认</b>"),
    ("按资损边界拆 4–6 服务", "最终一致+对账", "可独立扩", "中", "库存/支付异变时"),
    ("按目录硬拆+共享库", "假微服务", "事故高", "高", "<b>禁止</b>"),
])}
{five(
    "先边界后进程；拆分写 ADR。",
    "主：买成退成闭环；异：峰值；逆：售后。",
    "服务个数 KPI、共享库双写。",
    "维度表打分；默认模块化。",
    "跨服务事务数、故障率、交付周期。",
)}
{ban("<ul><li>无 Outbox/幂等就拆支付与订单</li><li>为简历上微服务拆分</li><li>模式堆砌无变更点</li></ul>")}
{checklist("DDD/模式落地清单", [
    "画出 5 上下文写权威表与业务唯一键",
    "下单事务不含库存写；clientToken 唯一",
    "写路径最小图加载（见 #s-ddd-agg）",
    "售后状态允许迁移表代码化",
    "支付回调模板方法+幂等",
    "物流 ACL 已落地",
    "模块化 vs 拆分 ADR 一份",
])}
{qa("【题】老板要一周拆 20 服务，如何用权衡表挡？",
    ["把维度表打分摊开：团队、对账、事务成本；给模块化里程碑。对齐的是资损边界不是个数。聚合唯一性/加载问题不因拆分自动消失。",
     "转型会议。", "硬拆共享库。", "ADR。", "「先边界后进程。」"],
    "ddd-arch-q1")}
{reflect("ddd-arch-r1")}
</section>
"""
    return hub + agg + bc + acl + patterns + arch
