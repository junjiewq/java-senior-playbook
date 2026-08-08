# -*- coding: utf-8 -*-
"""微服务/Spring 底板加深：挂 S-MS-X，人话→掀底板→落地"""
from helpers import qa, plain, floor, today, conf, checklist, reflect, spine, koujue


def build() -> str:
    return f"""
<section class="block" id="s-ms-x-floor" data-toc="S-MS-X · Spring调用链掀底板" data-prio="p0">
  <h2><span class="sys-id">S-MS-X</span>Spring Cloud 调用链掀底板（超时/重试从哪来）</h2>
{spine("补齐微服务章的底层：请求从过滤器到 Feign 到线程池如何占用；避免只念「要设超时」。",
       serves="下单 RPC 试算、支付回调",
       back="S-MS-X 治理 → 本页 → T-Found-X JUC")}
{plain("人话：一次下单像快递过安检（Filter）→ 导台（Dispatcher）→ 你的 Contoller → 若 Feign 调优惠，等于再派一辆车出去——两头都占着线程。超时不是拍脑袋填 5 秒，是这条链上的预算表。")}
{floor(
    "Servlet 线程 + Feign/HTTP 客户端",
    "Tomcat 工作线程执行整段同步调用；Feign 默认用同步 HTTP（如 OkHttp/HttpClient）。下游慢=工作线程不归还→池耗尽→新请求排队/拒绝。重试在客户端或 Ribbon/Spring Retry 层放大流量。",
    "路径认知：<code>ApplicationFilterChain</code> → <code>DispatcherServlet</code> → <code>XxxController</code> → <code>FeignInvocationHandler.invoke</code> → 编码器 → <code>Client.execute</code> → 解码。超时：连接/读超时在 client 配置；Sentinel/Resilience4j 在此前后熔断。看 Tomcat <code>currentThreadsBusy</code>、Feign/RT 直方图。",
    "优惠试算 2s 无舱壁→下单线程打满→支付回调同进程也 503；Feign 重试 3 次×网关重试=风暴，非幂等写会双下单风险。",
    "看：线程池 active、拒绝次数、下游 P99、重试指标、业务重复建单。",
)}
{conf("超时与禁重试（示意）", """# 交易 → 优惠试算（读，可短）
feign.client.config.promo.connectTimeout: 100
feign.client.config.promo.readTimeout: 120
# 写接口：关闭自动重试
spring.cloud.loadbalancer.retry.enabled: false
# 舱壁：优惠调用单独线程池（Resilience4j bulkhead / 自建）
""")}
{today("""<ul>
<li>画一张「下单同步链路」：每跳填超时，上游 &gt; 下游之和。</li>
<li>支付回调与下单入口线程池分开（或独立部署）。</li>
<li>预发注入优惠延迟，确认忙碌线程上升但支付池不动。</li>
</ul>""")}
{checklist("Spring/微服务底板验收", [
    "超时矩阵进仓库并与 Feign 配置一致",
    "写路径无客户端自动重试",
    "慢依赖有舱壁或独立池",
    "故障注入演练有截图",
])}
{koujue("调用链口诀：线程是租的，下游 RT 是租金；重试是特权。")}
{qa("【线上】只加大 Tomcat maxThreads 能否救优惠变慢？",
    ["不能从根上救：更多线程更容易打满 DB/下游。先超时+舱壁+降级，再谈扩容。",
     "大促。", "只加线程。", "注入演练。", "「加线程是加债，先降 RT。」"],
    "ms-floor-q1")}
{reflect("ms-floor-r1")}
</section>
"""
