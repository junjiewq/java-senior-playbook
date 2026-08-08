# -*- coding: utf-8 -*-
"""附录·百科全书总索引（ENCY）— 业务 / Java / 数据中间件 / 大数据 / AI"""
from helpers import plain, koujue, reflect, spine, mermaid


def build() -> str:
    map_mmd = mermaid(
        "diag-ency-map",
        "flowchart TB\n"
        "  ENCY[ENCY 百科索引] --> BIZ[ENCY-BIZ 业务全谱]\n"
        "  ENCY --> J[ENCY-J Java]\n"
        "  ENCY --> D[ENCY-D 数据与中间件]\n"
        "  ENCY --> BD[ENCY-BD 大数据]\n"
        "  ENCY --> AI[ENCY-AI AI]\n"
        "  ENCY --> CASE[ENCY-CASE 公开案例矩阵]\n"
        "  BIZ --> B1[商品库存价格会员]\n"
        "  BIZ --> B2[营销券积分分摊]\n"
        "  BIZ --> B3[支付清结算风控]\n"
        "  BIZ --> B4[OMS WMS 物流售后]\n"
        "  D --> DB[PolarDB Gauss 达梦 TDSQL]\n"
        "  D --> MW[MySQL Redis MQ ES]\n"
        "  AI --> A1[RAG Agent MCP Skills]\n"
        "  CASE --> PDD[拼多多餐饮阿里用友]\n"
        "  CASE --> FIN[招行美团大疆顺丰]\n"
        "  J -.交叉.-> Spine[B0 正逆向]\n"
        "  BIZ --> Spine\n"
        "  CASE --> Spine\n",
    )
    return f"""
<section class="block" id="ency" data-toc="ENCY · 附录百科全书总索引" data-prio="p1">
  <h2><span class="sys-id">ENCY</span>附录·业务 / Java / 数据 / 大数据 / AI 百科全书</h2>
{spine("主册之后追加的极致百科：业务全谱 + Java 底板 + 分布式库/中间件 + 大数据 + AI。不改写前序 B0/S/T 正文。",
       serves="交易正逆向全链路、数据侧指标画像、AI 副驾工程化",
       back="S0/B0/T* → 本附录深挖 → 挂回验收与选型")}
{plain("人话：前面脊柱解决「买成→退成」怎么讲清楚；本附录把技术和业务做成可检索百科——每叶子按「人话→本质四段→掀底板→流程图→多解法→落地→多题详答→反思」。顶栏 <code>/</code> 可全文搜索跳转。")}

  <div class="callout"><div class="label">怎么用本附录</div>
    <ol>
      <li>顶栏搜索或本页索引表跳转 sys-id。</li>
      <li>每大节含 mermaid；业务回扣默认挂订单/售后/清结算。</li>
      <li>与前序交叉：<a href="#t-found-x">T-Found-X</a> · <a href="#t-ai-stack">T-AI-Stack</a> · <a href="#t-as">T-AS</a> · <a href="#b-main-spine">B0</a>——百科补深，不重复灌水。</li>
      <li><b>APPEND-ONLY</b>；目录由 <code>data-toc</code> 自动扫描。</li>
    </ol>
  </div>

{map_mmd}

  <h3>百科索引（全量）</h3>
  <table>
    <thead><tr><th>域</th><th>sys-id 前缀</th><th>覆盖</th><th>入口</th></tr></thead>
    <tbody>
      <tr><td>业务</td><td>ENCY-BIZ*</td><td>商品→售后全谱、餐饮/跨境、银行并发对账</td><td><a href="#ency-biz">#ency-biz</a></td></tr>
      <tr><td>Java</td><td>ENCY-J*</td><td>语言/并发/JVM/集合/IO/Netty/框架/测试/安全</td><td><a href="#ency-j">#ency-j</a></td></tr>
      <tr><td>数据中间件</td><td>ENCY-D*</td><td>MySQL/Redis/MQ/ES/分库分表/<b>PolarDB·Gauss·达梦·TDSQL</b></td><td><a href="#ency-d">#ency-d</a></td></tr>
      <tr><td>大数据</td><td>ENCY-BD*</td><td>数仓/同步/Spark/Flink/Hive/OLAP/治理指标</td><td><a href="#ency-bd">#ency-bd</a></td></tr>
      <tr><td>AI</td><td>ENCY-AI*</td><td>训练推理微调/RAG/Agent/MCP/Skills/评测/向量/合规</td><td><a href="#ency-ai">#ency-ai</a></td></tr>
      <tr><td>公开案例</td><td>ENCY-CASE*</td><td>拼多多/肯麦/阿里/用友/招行/美团饿了么/大疆/顺丰 · 落地套路归纳</td><td><a href="#ency-case">#ency-case</a></td></tr>
    </tbody>
  </table>
{koujue("百科口诀：索引先跳，四段钉死，底板见血，流程图挂墙，搜索秒达。")}
{reflect("ency-hub-r1")}
</section>
"""
