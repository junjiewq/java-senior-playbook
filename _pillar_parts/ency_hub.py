# -*- coding: utf-8 -*-
"""附录索引：HARD GATE 以 ENCY-FM-* 为准"""
from helpers import plain, koujue, reflect, spine, mermaid


def build() -> str:
    map_mmd = mermaid(
        "diag-ency-map",
        "flowchart TB\n"
        "  ENCY[ENCY 附录索引] --> FM[ENCY-FM HARD GATE 全貌]\n"
        "  ENCY --> CASE[ENCY-CASE 公开案例矩阵]\n"
        "  FM --> MQ[Rocket/Kafka/Rabbit]\n"
        "  FM --> ST[Redis/MySQL/分布式库]\n"
        "  FM --> RT[JVM/JUC/Spring]\n"
        "  FM --> BD[Spark/Flink]\n"
        "  CASE --> Spine[B0 正逆向]\n"
        "  FM --> Spine\n",
    )
    return f"""
<section class="block" id="ency" data-toc="ENCY · 附录索引(HARD GATE)" data-prio="p0" data-tags="ency index">
  <h2><span class="sys-id">ENCY</span>附录索引 · 以 FULLMAP 硬门槛为准</h2>
{spine("主册之后追加。硬门槛条目在 ENCY-FM-*；公开公司套路在 ENCY-CASE-*。前序薄条目若存在仅作交叉，不以之为准。",
       serves="生产选型/排障/面试叙事",
       back="B0/T* → ENCY-FM → 验收")}
{plain("人话：不要再看「只讲事务消息」的侧面文。进 <a href='#ency-fm'>#ency-fm</a>，RocketMQ 金标从 CommitLog/刷盘/复制/死信/顺序一路串到金融vs电商vs物流。顶栏 <code>/</code> 全文搜索。")}
  <div class="callout danger"><div class="label">交付纪律</div>
    本附录 HARD GATE：原理+源码、3～4 跨行业案例（含公开量级/示意效果）、全链路、配置、Runbook、题库。
    不合格条目不进 ENCY-FM 区。
  </div>
{map_mmd}
  <table>
    <thead><tr><th>区</th><th>入口</th><th>门禁</th></tr></thead>
    <tbody>
      <tr><td>FULLMAP 总图</td><td><a href="#ency-fm">#ency-fm</a></td><td>PASS 索引</td></tr>
      <tr><td>RocketMQ 金标</td><td><a href="#ency-fm-rocket">#ency-fm-rocket</a></td><td>PASS</td></tr>
      <tr><td>Kafka / Rabbit</td><td><a href="#ency-fm-kafka">#ency-fm-kafka</a> · <a href="#ency-fm-rabbit">#ency-fm-rabbit</a></td><td>PASS</td></tr>
      <tr><td>Redis / MySQL</td><td><a href="#ency-fm-redis">#ency-fm-redis</a> · <a href="#ency-fm-mysql">#ency-fm-mysql</a></td><td>PASS</td></tr>
      <tr><td>PolarDB/Gauss/达梦/TDSQL</td><td><a href="#ency-fm-polardb">#ency-fm-polardb</a>…</td><td>PASS</td></tr>
      <tr><td>JVM/JUC/Spring/Spark/Flink</td><td><a href="#ency-fm-jvm">#ency-fm-jvm</a>…</td><td>PASS</td></tr>
      <tr><td>公开公司案例矩阵</td><td><a href="#ency-case">#ency-case</a></td><td>PASS（案例归纳）</td></tr>
    </tbody>
  </table>
{koujue("索引口诀：FM 硬门槛，CASE 学套路，搜索秒达。")}
{reflect("ency-hub-r1")}
</section>
"""
