#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inject year roadmap + cognitive C4 loop + 5 production complex cases."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
MIRROR = ROOT.parent / "高级Java外包-系统学习技术白皮书.html"
sys.path.insert(0, str(ROOT / "_pillar_parts"))
from anti_water_boost import boost_bx_hub as _boost_bx_hub  # noqa: E402

CSS_EXTRA = """
.c4-loop {
  margin: 1rem 0 1.4rem; border: 1px solid rgba(240,180,41,.4); border-radius: 14px;
  overflow: hidden; background: rgba(240,180,41,.05);
}
.c4-loop .c4-item {
  padding: .75rem .95rem; border-bottom: 1px solid var(--line); color: #d5e1f0;
}
.c4-loop .c4-item:last-child { border-bottom: none; }
.c4-loop .c4-item .c4-n {
  display: inline-block; font-family: var(--font-mono); font-size: .72rem; font-weight: 700;
  padding: .1rem .4rem; border-radius: 5px; margin-right: .4rem;
  background: rgba(240,180,41,.2); color: var(--accent-2);
}
.c4-loop .c4-item b.ttl { color: var(--accent-2); }
.week-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: .5rem; margin: 1rem 0;
}
@media (max-width: 900px) { .week-grid { grid-template-columns: 1fr 1fr; } }
.week-card {
  border: 1px solid var(--line); border-radius: 10px; padding: .55rem .65rem;
  background: rgba(0,0,0,.18); font-size: .82rem; line-height: 1.45; color: #c9d8ea;
}
.week-card .wn { color: var(--accent); font-weight: 700; font-family: var(--font-mono); font-size: .75rem; }
.okr-box {
  margin: 1rem 0; padding: .9rem 1.1rem; border-radius: 14px;
  border: 1px solid rgba(91,157,255,.35); background: rgba(91,157,255,.07);
}
.okr-box .label {
  font-size: .72rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  color: var(--accent-3); margin-bottom: .4rem;
}
"""

def reflect(rid: str) -> str:
    return (
        f'<div class="reflect" data-reflect="{rid}">'
        f'<div class="reflect-head"><h5>我的反思与思考</h5>'
        f'<div class="reflect-tools"><button type="button" data-cmd="bold">B</button>'
        f'<button type="button" data-cmd="insertUnorderedList">•</button></div></div>'
        f'<div class="reflect-body" contenteditable="true" '
        f'data-placeholder="四段闭环：业务本质→技术实现→技术原理→业务实质；附本周交付物与差距">'
        f'</div><div class="reflect-foot">已自动保存到本机 localStorage</div></div>'
    )

def qa(q: str, layers: list, rid: str) -> str:
    parts = ['  <div class="qa">', f'    <div class="q">{q}</div>', '    <div class="a answer-detail">']
    labels = ["① 原理", "② 场景", "③ 坑", "④ 怎么落地", "⑤ 30秒亮点口述"]
    for i, t in enumerate(layers):
        parts.append(f'      <div class="layer"><b>{labels[i]}</b>{t}</div>')
    parts.append("    </div>\n  </div>")
    parts.append(reflect(rid))
    return "\n".join(parts)

def c4(biz, impl, principle, substance, hc="") -> str:
    hc_html = f'<p><b>高并发贯穿：</b>{hc}</p>' if hc else ""
    return f"""  <div class="c4-loop">
    <div class="c4-item"><span class="c4-n">C1</span><b class="ttl">业务本质</b> — {biz}</div>
    <div class="c4-item"><span class="c4-n">C2</span><b class="ttl">技术实现</b> — {impl}</div>
    <div class="c4-item"><span class="c4-n">C3</span><b class="ttl">技术原理</b> — {principle}</div>
    <div class="c4-item"><span class="c4-n">C4</span><b class="ttl">业务实质</b> — {substance}{hc_html}</div>
  </div>"""

def tradeoff_table(title, rows) -> str:
    lines = [
        f"  <h4>{title}</h4>",
        "  <table>",
        "    <thead><tr><th>解法</th><th>一致性</th><th>性能/峰值</th><th>成本/运维</th><th>推荐边界</th></tr></thead>",
        "    <tbody>",
    ]
    for r in rows:
        lines.append(
            f"      <tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
        )
    lines += ["    </tbody>", "  </table>"]
    return "\n".join(lines)

def five_steps_mini(nail, split, mark, pick, verify) -> str:
    return f"""  <div class="callout"><div class="label">挂五步法 · 钉拆标选验</div>
    <ol>
      <li><b>钉</b> {nail}</li>
      <li><b>拆</b> {split}</li>
      <li><b>标</b> {mark}</li>
      <li><b>选</b> {pick}</li>
      <li><b>验</b> {verify}</li>
    </ol>
  </div>"""

# ---------- Section: Cognitive C4 hub ----------
SEC_C4 = f"""
<section class="block" id="s-c4" data-toc="S2+ · 认知闭环四段" data-prio="p0">
  <h2><span class="sys-id">S2+</span>认知闭环四段：业务本质 → 实现 → 原理 → 业务实质</h2>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>每个加深案例强制走完四段，防止「只讲中间件」或「只讲故事」。<br><b>挂环：</b>S2 需求模板 → 本页 → <a href="#bx-prod">B-X 复杂场景</a> → <a href="#s-method">S-Method</a></div>

  <div class="essence">
    <div class="essence-col">
      <div class="label">业务本质</div>
      <p class="one">先说客人/财务怕什么坏：资损、体验、合规。</p>
      <p>外包验收：四段写不全，方案不算过审。</p>
    </div>
    <div class="essence-col">
      <div class="label">技术本质</div>
      <p class="one">实现回答「怎么做」；原理回答「为何稳」；实质把技术拉回验收。</p>
      <p>高并发不是独立章节，是贯穿峰值/热点/削峰/降级的约束。</p>
    </div>
    <p><b>若没有它，业务哪一步会坏：</b>技术炫技跑偏，或业务描述无法落地成可观测交付。</p>
  </div>

  <div class="plain"><div class="label">人话版</div>人话：C1 讲清楚「怕什么」；C2 讲「系统怎么干」；C3 讲「为什么不会炸」；C4 用资损/体验/对账数字证明没跑偏。四段缺一，面试官会拆穿。</div>

  <table>
    <thead><tr><th>段</th><th>强制问句</th><th>禁止写法</th><th>高并发要带什么</th></tr></thead>
    <tbody>
      <tr><td><b>C1 业务本质</b></td><td>谁疼？验收句？不可逆点？</td><td>上来就 Redis/Kafka</td><td>峰值量级、热点 SKU、可接受降级</td></tr>
      <tr><td><b>C2 技术实现</b></td><td>状态机/表/消息/接口怎么落地？</td><td>只有架构图无表结构</td><td>削峰队列、预热、限流位</td></tr>
      <tr><td><b>C3 技术原理</b></td><td>为何幂等/为何最终一致够用？</td><td>背名词无因果</td><td>锁粒度、分区、舱壁、背压</td></tr>
      <tr><td><b>C4 业务实质</b></td><td>对账差、客诉、资损阈值过了吗？</td><td>「理论上可行」收尾</td><td>压测数字、降级开关演练结果</td></tr>
    </tbody>
  </table>

  <div class="mermaid-wrap" id="diag-c4-loop">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-c4-loop">导出 PNG</button></div>
    <pre class="mermaid">
flowchart LR
  C1[C1 业务本质] --> C2[C2 技术实现]
  C2 --> C3[C3 技术原理]
  C3 --> C4[C4 业务实质]
  C4 -->|跑偏则回钉| C1
  HC[峰值·热点·削峰·降级] -.贯穿.-> C1
  HC -.贯穿.-> C2
  HC -.贯穿.-> C3
  HC -.贯穿.-> C4
    </pre>
  </div>

  <div class="koujue"><div class="label">口诀</div>四段口诀：怕什么 → 怎么干 → 为何稳 → 账过了没。高并发四字：峰热削降。</div>

{qa("【练手】用四段讲「支付成功必须进 OMS」30 秒。",
    ["C1 怕付了钱没货；C2 Outbox+投递；C3 本地事务与消息同命运；C4 日终支付≈OMS 创建。",
     "评审/面试。", "只说用了 RocketMQ。", "补峰值：支付回调洪峰走舱壁线程池。", "「四段闭环，不只报 MQ。」"],
    "c4-q1")}

{reflect("c4-r1")}
</section>
"""

# ---------- Section: Year roadmap ----------
MONTHS = [
    ("M01", "正逆向导航 + 五步法肌肉记忆", "S0–S2 / S-Method / B0", "并发入门口诀", "默画 B0；默写钉拆标选验"),
    ("M02", "正向结算：拼团·券·分摊", "B-F F1/F2", "Redis 预占 / 幂等", "分摊表+未成团退 ADR"),
    ("M03", "正向履约：支付·OMS·WMS", "B-F F3", "Outbox / MQ", "缺货补偿状态机+对账"),
    ("M04", "逆向全谱与双退防护", "B-R R1", "状态机 / 渠道限流", "售后状态机+退款幂等"),
    ("M05", "权益·寄修·换新库存锁", "B-R R2 + B-X", "库存锁粒度", "寄修∥换新并发剧本"),
    ("M06", "行业旋钮：餐饮高峰餐损", "B-Ind 餐饮 + B-X", "热点门店限流", "不可逆点配置表"),
    ("M07", "行业旋钮：跨境清关失败", "B-Ind 跨境 + B-X", "多币种/锁汇", "清关闸门+逆向退"),
    ("M08", "数据与缓存深水", "T3–T5 挂主线", "分库边界 / 击穿", "热点 SKU 压测报告"),
    ("M09", "治理：限流熔断可观测", "T6 / S-MS", "舱壁 / SLO", "大促开关演练记录"),
    ("M10", "发布弹性：Docker/K8s", "T-K8s", "金丝雀/回滚", "订单域发布检查单"),
    ("M11", "AI 副驾：Skills/MCP/RAG/Agent", "T-AI-Stack", "HITL 红线", "质检草稿 Skill 作品集"),
    ("M12", "路考·作品集·一年复盘", "S3 / S4 / B-X 全量", "容量复盘", "90 秒录音+ADR 册"),
]

WEEKS_RITUAL = """  <div class="company-prd">
    <div class="label">每周固定仪式（52 周不换格式）</div>
    <p><b>①读一节</b>（主线优先，零件按需）→ <b>②练手题</b>（至少 2 道详答）→ <b>③复盘框</b>（四段闭环各一句）→ <b>④可交付物</b>（笔记 / 小实验 / 故障演练三选一落盘）</p>
    <p>时间盒建议：读 90min · 练 60min · 复盘 30min · 交付物 60–120min。忙周可砍读，不可砍④。</p>
  </div>"""

month_rows = "\n".join(
    f"      <tr><td>{m[0]}</td><td>{m[1]}</td><td>{m[2]}</td><td>{m[3]}</td><td>{m[4]}</td></tr>"
    for m in MONTHS
)

# Compact 52-week: 4 weeks per month with read/drill/deliverable
week_cards = []
themes_w = [
    ("读：S0 总图", "练：默画 B0", "交付：体系一页纸"),
    ("读：S2 模板", "练：PRD→溯源", "交付：需求模板填满"),
    ("读：S-Method", "练：钉拆标选验口述", "交付：五步冰箱贴"),
    ("读：B0 总图", "练：拒拼凑提案", "交付：周复盘四段"),
    ("读：拼团 F1", "练：成团临界", "交付：团状态机图"),
    ("读：券分摊 F2", "练：部分退分摊", "交付：allocation 样例"),
    ("读：互斥最优", "练：取舍表 3 行", "交付：优惠 ADR"),
    ("读：大促入口", "练：限流位设计", "交付：削峰开关清单"),
    ("读：支付幂等", "练：双回调", "交付：支付状态机"),
    ("读：Outbox", "练：堆积演练", "交付：投递 Runbook"),
    ("读：OMS/WMS", "练：缺货补偿", "交付：补偿时序图"),
    ("读：物流 ACL", "练：签收乱序", "交付：承运商防腐笔记"),
    ("读：逆向全谱", "练：双退防护", "交付：售后状态机"),
    ("读：仅退款", "练：未发货秒退", "交付：渠道幂等键规范"),
    ("读：退货质检", "练：回执乱序", "交付：质检回执用例"),
    ("读：部分退", "练：分摊回退", "交付：退款对账 SQL"),
    ("读：延保权益", "练：解绑时机", "交付：权益悬挂告警"),
    ("读：寄修并行", "练：换新锁库存", "交付：并发剧本"),
    ("读：翻新再售", "练：SN 追踪", "交付：SN 轨迹表设计"),
    ("读：B-X 案例加深", "练：四段闭环写满", "交付：案例 STAR"),
    ("读：餐饮不可逆", "练：出餐后取消", "交付：餐损规则表"),
    ("读：高峰排队", "练：门店热点", "交付：限流压测数"),
    ("读：骑手取消", "练：赔付口径", "交付：异常流程卡"),
    ("读：中厂裁剪", "练：无 WMS 版", "交付：配置化旋钮"),
    ("读：清关闸门", "练：失败逆向", "交付：清关状态机"),
    ("读：税费锁汇", "练：退税争议", "交付：财务验收句"),
    ("读：国际段物流", "练：丢件责任", "交付：ACL 边界笔记"),
    ("读：多时区", "练：展示/存储", "交付：UTC 约定"),
    ("读：MySQL 慢查", "练：EXPLAIN", "交付：索引变更单"),
    ("读：Redis 击穿", "练：单飞", "交付：热点 Key 预案"),
    ("读：分库边界", "练：订单号路由", "交付：分片 ADR"),
    ("读：对账批处理", "练：日终差", "交付：对账剧本"),
    ("读：限流熔断", "练：半开误伤", "交付：Sentinel 规则"),
    ("读：链路追踪", "练：trace 贯主线", "交付：三针看板"),
    ("读：舱壁线程池", "练：回调隔离", "交付：池参数表"),
    ("读：SLO 告警", "练：误报治理", "交付：告警降噪"),
    ("读：模块化单体", "练：何时不拆", "交付：拆分决策树"),
    ("读：发布金丝雀", "练：一键回滚", "交付：发布检查单"),
    ("读：K8s 探针", "练：OOMKill", "交付：资源配额"),
    ("读：配置开关", "练：大促预案", "交付：开关演练录屏"),
    ("读：Skills", "练：质检检查单", "交付：Skill.md"),
    ("读：MCP 只读", "练：鉴权卡写", "交付：工具白名单"),
    ("读：RAG 引用", "练：压幻觉", "交付：分块策略"),
    ("读：多智能体 HITL", "练：禁直退", "交付：人机审批流"),
    ("读：S3 路考", "练：一单正逆向", "交付：90 秒录音"),
    ("读：并发库", "练：8 题口述", "交付：错题本"),
    ("读：事故案例集", "练：STAR×2", "交付：脱敏案例卡"),
    ("读：作品集整理", "练：ADR 装订", "交付：作品集目录"),
    ("读：全年薄弱回炉", "练：自测清单", "交付：差距 OKR"),
    ("读：模拟面试", "练：被追问原理", "交付：录像复盘"),
    ("读：容量复盘", "练：峰热削降", "交付：容量一页纸"),
    ("读：带走 OS", "练：教别人五步", "交付：个人方法论终版"),
]
assert len(themes_w) == 52
for i, (a, b, c) in enumerate(themes_w, 1):
    week_cards.append(
        f'<div class="week-card"><div class="wn">W{i:02d}</div>{a}<br>{b}<br><b>{c}</b></div>'
    )

QUARTERS = """
  <div class="okr-box">
    <div class="label">Q1 OKR（M01–M03）· 能讲清「买成」</div>
    <ul>
      <li><b>O：</b>独立用五步+四段讲完拼团/分摊/支付→OMS。</li>
      <li><b>KR1：</b>B0 默画 1 次满分；KR2：分摊+Outbox 各 1 份 ADR；KR3：缺货补偿时序可讲解；KR4：周交付物 ≥10。</li>
    </ul>
  </div>
  <div class="okr-box">
    <div class="label">Q2 OKR（M04–M06）· 能讲清「退成/修好」+餐饮旋钮</div>
    <ul>
      <li><b>O：</b>售后双退防护与寄修∥换新能压测口述；餐饮不可逆点配置化。</li>
      <li><b>KR1：</b>售后状态机落地笔记；KR2：B-X 至少完成 2 个案例四段；KR3：餐损演练 1 次；KR4：并发库答对率 ≥80%。</li>
    </ul>
  </div>
  <div class="okr-box">
    <div class="label">Q3 OKR（M07–M09）· 跨境 + 数据治理扛峰值</div>
    <ul>
      <li><b>O：</b>清关失败逆向可对账；热点与限流有数字。</li>
      <li><b>KR1：</b>清关闸门方案；KR2：热点 SKU 压测报告；KR3：三针看板截图；KR4：大促开关演练记录。</li>
    </ul>
  </div>
  <div class="okr-box">
    <div class="label">Q4 OKR（M10–M12）· 发布弹性 + AI 副驾 + 作品集收官</div>
    <ul>
      <li><b>O：</b>金丝雀会回滚；AI 只草稿不改账；作品集可面试。</li>
      <li><b>KR1：</b>发布检查单实战 1 次；KR2：Skill+MCP+RAG 三联 demo；KR3：90 秒路考录音；KR4：个人方法论终版。</li>
    </ul>
  </div>
"""

SEC_YEAR = f"""
<section class="block" id="s-year" data-toc="S-Year · 一年坚持路线" data-prio="p0">
  <h2><span class="sys-id">S-Year</span>一年坚持路线：12 月主题 × 52 周仪式 × 季度 OKR</h2>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>把「想加厚」变成公司 OKR 式可执行计划。每月主题必须挂回正逆向主线，横向能力（并发/JVM/数据/MQ/治理/K8s/AI）按需插入。<br><b>挂回：</b><a href="#s4-review">S4</a> 自测 → 本页执行 → <a href="#bx-prod">B-X</a> 加深 → <a href="#s-method">S-Method</a></div>

  <div class="essence">
    <div class="essence-col">
      <div class="label">业务本质</div>
      <p class="one">一年后你能独立对「一笔买成+一笔退成」负责，而不是收藏夹更厚。</p>
      <p>像在公司：有主题、有交付、有季度验收，没有「学了再说」。</p>
    </div>
    <div class="essence-col">
      <div class="label">技术本质</div>
      <p class="one">用节奏消灭散装学习的不确定性：主线螺旋上升，零件服务主线。</p>
      <p>忙周砍广度不砍交付物；交付物必须能挂回 B-F/B-R 某步。</p>
    </div>
    <p><b>若没有它，业务哪一步会坏：</b>没有年度闭环：三个月后回到名词焦虑。</p>
  </div>

  <div class="plain"><div class="label">人话版</div>人话：别问「还要学啥」。打开本页看你在第几周，做完本周④交付物打勾。一年维度=52 次小闭环，不是一次读完。</div>

{WEEKS_RITUAL}

  <h3 id="s-year-12m">12 个月主题（挂主线 + 横向）</h3>
  <table>
    <thead><tr><th>月</th><th>主题（挂正逆向）</th><th>主线锚点</th><th>横向能力</th><th>月末交付物</th></tr></thead>
    <tbody>
{month_rows}
    </tbody>
  </table>

  <h3 id="s-year-okr">季度里程碑（公司 OKR 体）</h3>
{QUARTERS}

  <h3 id="s-year-52">52 周卡片（读·练·交付）</h3>
  <p>每张卡片三行：读什么 / 练什么 / <b>可交付物</b>。点开对应主线章节深读；练手详答写在反思框。</p>
  <div class="week-grid">
{"".join(week_cards)}
  </div>

  <h3 id="s-year-check">全年自测清单（季末勾选）</h3>
  <ul class="checklist">
    <li>能默画 B0，并指出峰值限流插在哪一段</li>
    <li>能用四段闭环讲清 B-X 五个复杂场景中的任意两个</li>
    <li>能从 PRD 句推出技术溯源表，并给 ≥2 解法取舍</li>
    <li>能讲清分摊回退、双退防护、缺货补偿、清关失败逆向</li>
    <li>能做一次金丝雀回滚口述 + 一次大促开关演练笔记</li>
    <li>AI 作品：Skill + 只读 MCP + RAG 引用，且禁止直改账务</li>
    <li>作品集：≥6 份 ADR/时序/对账 SQL，可脱敏面试</li>
    <li>路考：90 秒正逆向录音，被追问原理不崩</li>
  </ul>

  <div class="callout warn"><div class="label">防跑偏</div>
    <p>横向章节（JVM/K8s/AI）若当周映射不进 B0，标记「零件停车场」，下周必须写回主线验收句，否则不算学完。</p>
  </div>

{qa("【验收】怎样算「坚持了一年」而不是「打开过一年」？",
    ["52 周里 ≥40 周有④交付物落盘；四季度 OKR 各过一条 KR；能四段讲两个 B-X 案例。",
     "自我管理。", "只读不写、只收藏题库。", "用本页清单季末打分，差距回炉对应月。", "「交付物计数，不是页数。」"],
    "year-q1")}

{reflect("year-r1")}
</section>
"""

# ---------- Complex cases ----------
def case_shell(cid, toc, title, prd, c4_html, five, tradeoffs, drills, reflect_id):
    body = f"""
<section class="block" id="{cid}" data-toc="{toc}" data-prio="p0">
  <h2><span class="sys-id">B-X</span>{title}</h2>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>生产级加深：强制四段闭环 + 五步法 + 多解法。非 demo。<br><b>挂回：</b>B0 → 本案例 → T 零件按需 → S-Method</div>
  <div class="company-prd">
    <div class="label">公司 PRD（摘要）</div>
    {prd}
  </div>
  <h3>认知闭环四段（强制）</h3>
{c4_html}
{five}
  <h3>多解法取舍</h3>
{tradeoffs}
  <h3>练手详答</h3>
{drills}
{reflect(reflect_id)}
</section>
"""
    return body

# Case 1
CASE1 = case_shell(
    "bx-group-coupon",
    "B-X · 大促拼团+券分摊退",
    "大促拼团 + 券叠加 + 分摊后并发退款",
    """<p><b>一句话：</b>大促拼团叠加平台券与积分，成团后部分退/未成团自动退，分摊回退在并发下不错账、不超退。</p>
    <p><b>谁：</b>交易/营销/财务　<b>峰值：</b>成团临界 QPS 与退款回调洪峰叠加</p>
    <p><b>验收：</b>日终 团失败≈退款成功+挂账；部分退 ≤ 分摊实付；券积分不超回。</p>""",
    c4(
        "怕的是「促销看起来热闹，退款时财务对不上、客人超退或少退」。本质是优惠承诺与资金终态在并发下仍可解释。",
        "团状态机（拼中/成团/失败）+ 券核销唯一键 + 积分冻结/确认 + order_discount_allocation 落表；失败/部分退引用分摊行回退；退款幂等表（申请号+渠道号）；大促入口限流+成团名额分段锁。",
        "分摊把「整单优惠」变成「行级债权」；幂等键把渠道至少一次投递变成业务至多一次资金变动；名额用原子扣减+版本，避免超成团；最终一致靠对账与挂账，不靠同步长事务扛峰值。",
        "用资损与体验验收：抽检部分退金额=分摊公式；压测成团临界无超卖；退款重复回调资金不变。跑偏信号：分摊不平衡告警、券库存为负、客诉「退少了」。",
        "峰值打在成团与退款两端→削峰用异步退款队列；热点团 ID 分段；名额抢光快速失败；财务核对可降级为「先退实付、券积分日终补差」需开关与公示。",
    ),
    five_steps_mini(
        "签字口径：未成团全退；部分退按分摊；禁止超退。",
        "主：成团履约；异：超时/支付晚到；逆：自动退与部分退。",
        "名额并发、回调重复、分摊引用、退款渠道限流。",
        "状态机+预占+分摊表+幂等；扫表或延迟消息解散团。",
        "对账三针+分摊不平衡监控+大促开关演练。",
    ),
    tradeoff_table("解散团与自动退", [
        ("定时扫到期团", "最终一致（分钟）", "稳，峰值可削", "运维简单", "<b>中厂默认</b>"),
        ("延迟消息到点", "更准时", "依赖 MQ 延迟", "平台能力", "大促高时效"),
        ("同步退款链路", "强一致外观", "拖垮成团 RT", "高", "禁止用于峰值主路径"),
    ]) + "\n" + tradeoff_table("部分退优惠回退", [
        ("按 allocation 行回退", "财务可解释", "依赖正向质量", "中", "<b>主线默认</b>"),
        ("整单比例估算", "弱", "快", "低", "仅非财务验收"),
        ("人工工单补差", "灵活", "人效差", "高人工", "长尾边缘"),
    ]),
    "\n".join([
        qa("【练手1】两人同时凑满最后一名额，如何不超成团？",
           ["名额原子 DECR/乐观版本，仅一人成功；失败者走失败补偿或下一团。",
            "大促临界。", "先查后改无锁。", "分段锁+唯一成团事务号。", "「名额是库存，不是计数器装饰。」"],
           "bx1-q1"),
        qa("【练手2】成团后部分退一件，平台券与积分怎么退？",
           ["查该行 allocation；券按行退回额度或作废规则；积分按冻结/确认状态回退；总和≤实付。",
            "售后退货。", "按整单比例拍脑袋。", "退款单带分摊快照版本号。", "「退的是行债权，不是感觉。」"],
           "bx1-q2"),
        qa("【练手3】退款回调来两次，如何证明不双退？",
           ["幂等键落库，第二次返回成功但不再次打款；对账渠道流水。",
            "渠道抖动。", "靠「大概不会重复」。", "单测+线下重复推送演练。", "「重复是常态，幂等是本职。」"],
           "bx1-q3"),
    ]),
    "bx1-r1",
)

CASE2 = case_shell(
    "bx-pay-wms-short",
    "B-X · 支付成功WMS缺货",
    "支付成功 → OMS 下发 → WMS 缺货补偿",
    """<p><b>一句话：</b>钱已收，仓发现短拣/缺货，要在体验与资损间完成拆单、取消、退款或调拨补偿，且与取消令牌并发安全。</p>
    <p><b>谁：</b>交易/OMS/仓储/客服　<b>峰值：</b>大促出库回执洪峰 + 用户催取消</p>
    <p><b>验收：</b>缺货必触达用户可选方案；不出现「钱货双无」；取消与拣货竞态可解释。</p>""",
    c4(
        "业务怕「付了款却无限等待或静默关单」。本质是仓实物流与支付终态的对齐，以及用户选择权。",
        "支付成功 Outbox→OMS 创建→下发 WMS；WMS 回执：接单/拣货中/短拣/出库；短拣触发补偿 Saga：拆单发可得、整单退、调拨等待（配置）；取消令牌带 OMS 版本；退款走 B-R 幂等。",
        "用状态机把仓异步世界变成可判定状态；版本号解决取消 vs 下架竞态；Outbox 保证「付成功必尝试履约」；补偿动作幂等，避免重复调拨/重复退。",
        "实质看：缺货工单关闭时长、自动退成功率、客诉「没收到货还扣钱」归零。压测回执乱序与取消并发。跑偏=只加人工不管状态机。",
        "回执洪峰舱壁隔离；热点仓分区消费；削峰：非实时调拨改队列；降级：缺货默认「整单退」开关，保资损优先。",
    ),
    five_steps_mini(
        "缺货可见、可退、可选；禁止静默。",
        "主：下发履约；异：短拣/超时；逆：退款或拆单。",
        "取消∥拣货、回执乱序、重复下发。",
        "OMS/WMS 协议+版本+Outbox+补偿 Saga。",
        "缺货率/补偿时效/取消成功监控+金丝雀。",
    ),
    tradeoff_table("缺货补偿策略", [
        ("整单自动退", "资损清晰", "体验一般", "低", "开关默认·保底"),
        ("拆单发可得", "体验更好", "分摊/运费复杂", "中", "多仓/多SKU"),
        ("等待调拨", "尽力履约", "时效不确定", "客服成本", "高价值单"),
        ("人工工单", "灵活", "峰值不可扩", "高", "长尾"),
    ]),
    "\n".join([
        qa("【练手1】用户点取消时 WMS 已下架，系统怎么回？",
           ["取消令牌带版本；若仓态≥下架，拒绝秒退，转「拦截/退货」逆向。",
            "催取消。", "直接当未发货退。", "仓态枚举+用户文案映射。", "「取消不是按钮，是仓态函数。」"],
           "bx2-q1"),
        qa("【练手2】WMS 重复投递「短拣」消息？",
           ["补偿单幂等键=发货单号+短拣事件号；第二次空操作。",
            "MQ 至少一次。", "每次都建工单。", "消费侧去重表。", "「回执乱序+重复是设计输入。」"],
           "bx2-q2"),
        qa("【练手3】为何不用同步事务串支付与 WMS？",
           ["仓延迟秒~分钟，长事务拖垮支付；用最终一致+补偿。",
            "架构评审。", "强一致迷信。", "Outbox+对账。", "「一致的是账，不是同一把 DB 锁。」"],
           "bx2-q3"),
    ]),
    "bx2-r1",
)

CASE3 = case_shell(
    "bx-repair-exchange",
    "B-X · 寄修∥换新锁库存",
    "售后退货与寄修并行、换新锁定库存",
    """<p><b>一句话：</b>同一订单行可能并行「退货退款」与「寄修」，或「寄修转换新」；换新必须锁库存且旧件未定性前不双发、不双退。</p>
    <p><b>谁：</b>售后/仓储/库存/财务　<b>峰值：</b>活动后售后洪峰、质检回执集中</p>
    <p><b>验收：</b>并行单互斥规则可配置；换新预占有 TTL；旧件报废/再售路径可追 SN。</p>""",
    c4(
        "怕「修好又换新」或「退了款货还在修」。本质是同一债权标的上的互斥与库存承诺。",
        "售后聚合根+类型策略；并行策略表（互斥/可并行）；换新：库存预占（SKU+仓）TTL；质检回执驱动分支：退款/寄修完成/换新发货；SN 轨迹；权益迁移/解绑。",
        "互斥用售后单状态+行锁/乐观版本；预占与支付域库存模型一致（预占→确认/释放）；质检异步用状态机消化乱序；禁止跨聚合直接改库存无单据。",
        "实质：无双发；无「退款+换新货」双出；库存盘点与售后预占对得上。跑偏信号：预占泄漏、SN 两处在库。",
        "售后洪峰：申请入口限流；质检回执多消费者分区（售后单号）；热点 SKU 换新用分段库存；降级：暂停换新只留退货。",
    ),
    five_steps_mini(
        "钱货 SN 终态唯一；并行规则产品签字。",
        "主：寄修/换新；异：质检驳回；逆：转退款。",
        "并行提交、预占超卖、回执乱序。",
        "策略+预占 TTL+SN 轨迹+幂等回执。",
        "预占泄漏监控、双出对账、TTL 扫表。",
    ),
    tradeoff_table("换新库存", [
        ("下单式预占+TTL", "防超卖", "需扫释放", "中", "<b>默认</b>"),
        ("发货时再扣", "实现简单", "高峰无货爽约", "低", "非承诺场景"),
        ("全仓预留池", "体验稳", "库存浪费", "高占用", "爆款官方换新"),
    ]),
    "\n".join([
        qa("【练手1】用户同时提交退货与寄修？",
           ["并行策略：默认互斥，后者拒绝或提示取消前者；配置允许则拆行。",
            "客服并发建单。", "都建成功。", "行级唯一「活跃售后」约束。", "「并行是产品规则，不是技术巧合。」"],
           "bx3-q1"),
        qa("【练手2】换新预占成功但质检判责用户，如何释放？",
           ["驳回事件→预占释放+通知；幂等防重复释放成负数。",
            "质检驳回。", "人工改库存。", "领域事件+库存流水。", "「释放与扣减同等重要。」"],
           "bx3-q2"),
        qa("【练手3】寄修完成应发回旧机，却误走换新？",
           ["质检结论枚举驱动策略，禁止人工改库跳状态；特征开关灰度。",
            "流程配错。", "DB 手改状态。", "状态机单测+抽样审计。", "「结论驱动流转，不手搓终态。」"],
           "bx3-q3"),
    ]),
    "bx3-r1",
)

CASE4 = case_shell(
    "bx-food-peak",
    "B-X · 餐饮高峰取消餐损",
    "餐饮高峰取消与餐损（不可逆点）",
    """<p><b>一句话：</b>高峰出餐前后取消规则不同；餐损谁承担要配置化；与骑手接单/到店状态协同，避免「出餐后全额退」资损。</p>
    <p><b>谁：</b>门店/平台/骑手/客服　<b>峰值：</b>午晚高峰下单与取消尖刺</p>
    <p><b>验收：</b>不可逆点后取消走餐损规则；门店与用户两侧账单可解释。</p>""",
    c4(
        "本质是「食物一旦制作，边际成本不可逆」。怕的是高峰刷单取消与门店亏损。",
        "门店接单→制作中→待取餐→骑手配送状态机；不可逆点配置（接单后 N 分钟/点击出餐）；取消策略引擎；餐损分摊（用户/平台/门店）；高峰限流与排队；支付/退款幂等同主线。",
        "把不可逆点做成显式状态阈值，而不是藏在 if；策略模式按城市/品类；高峰用门店维度热点限流+排队；最终退款仍走幂等与对账。",
        "实质：餐损率、取消率、门店投诉率在阈值内；抽检出餐后取消未全额退。跑偏=全国一刀切规则。",
        "热点门店独立限流；取消接口削峰；降级：停止接单、拉长 ETA、关闭神券。",
    ),
    five_steps_mini(
        "不可逆点与餐损承担方产品+门店签字。",
        "主：履约出餐；异：骑手取消/超时；逆：按点退。",
        "高峰取消尖刺、状态乱序、重复退。",
        "配置化不可逆点+策略引擎+门店限流。",
        "餐损对账、取消成功率、门店心跳。",
    ),
    tradeoff_table("不可逆点设计", [
        ("点击出餐为点", "清晰", "依赖店员操作", "中", "<b>常见默认</b>"),
        ("接单后 T 分钟", "可自动", "误伤慢制作", "低", "标准快餐"),
        ("骑手到店为点", "偏体验", "门店风险大", "争议", "慎用"),
    ]),
    "\n".join([
        qa("【练手1】出餐后用户取消，如何算？",
           ["命中不可逆点→按餐损规则部分退或仅退配送费；账单展示原因。",
            "高峰。", "无脑全额退。", "规则表+客服话术。", "「出餐是餐饮的清关。」"],
           "bx4-q1"),
        qa("【练手2】骑手接单后取消，库存/餐怎么办？",
           ["订单回门店待分配或触发餐损；避免重复制作指令。",
            "运力不足。", "再推一次制作。", "配送状态与制作状态解耦对账。", "「制作指令只发一次。」"],
           "bx4-q2"),
        qa("【练手3】与电商退货比，不可逆点差异？",
           ["电商多在出库/签收；餐饮在出餐；都是把物理不可逆编码进状态机。",
            "B-Ind 对比。", "两套完全无关系统思维。", "同一正逆向模板换旋钮。", "「旋钮不同，脊柱相同。」"],
           "bx4-q3"),
    ]),
    "bx4-r1",
)

CASE5 = case_shell(
    "bx-cross-border",
    "B-X · 跨境清关失败逆向",
    "跨境清关失败后的逆向闭环",
    """<p><b>一句话：</b>清关失败不得继续国际段履约；税费/货款/运费按锁定口径回退；与国内仓退货路径分流。</p>
    <p><b>谁：</b>关务/跨境运营/财务/仓储　<b>峰值：</b>政策变更日失败单突增</p>
    <p><b>验收：</b>清关态闸门挡住出库；失败单自动进 B-R；锁汇汇率下退款可解释。</p>""",
    c4(
        "怕「货卡关、钱不清、税紊乱」。本质是跨境增加「监管态」这一不可逆门槛。",
        "订单增加清关态（申报/查验/放行/失败）；放行前禁止 WMS 出境出库；失败事件→逆向：货款退、税退规则、运费规则；汇率下单锁定；国内段与国际段 ACL 分离。",
        "闸门=状态机前置条件；资金用支付时汇率快照保证可解释；失败风暴用队列削峰+客服工单批量；对账分「货款/税/运费」三科目。",
        "实质：清关失败零错误出库；退款科目抽检通过；客诉「税退了货没退」归零。跑偏=只对接海关接口不做闸门。",
        "失败突增削峰；热点口岸队列；降级：暂停该品类申报、入口提示。",
    ),
    five_steps_mini(
        "清关失败必停履约、必可退；财务科目签字。",
        "主：申报放行；异：查验；逆：失败退。",
        "失败风暴、重复申报、汇率争议。",
        "清关态闸门+科目退款+Outbox 事件。",
        "失败出库率=0 监控、科目对账、开关停售。",
    ),
    tradeoff_table("清关失败处理", [
        ("自动全额退货款+税规则退", "体验快", "规则要准", "中", "<b>默认</b>"),
        ("人工关务审核后返", "可控", "峰值堆单", "高人工", "高货值"),
        ("改寄国内仓再售", "挽留", "合规复杂", "高", "少数品类"),
    ]),
    "\n".join([
        qa("【练手1】放行消息晚到，本地已按失败退款？",
           ["清关态版本+终态保护；已退则走「异常挽单」人工，禁止自动再扣。",
            "渠道乱序。", "再扣款发货。", "终态机+告警。", "「晚到的成功不能复活已退单。」"],
           "bx5-q1"),
        qa("【练手2】税已缴清关失败，税怎么退？",
           ["按关务回执与合同：可退税走税科目退款单；不可退则成本科目+客诉口径。",
            "财务争议。", "和货款混一笔。", "三科目分账。", "「税是第三本账。」"],
           "bx5-q2"),
        qa("【练手3】用四段+五步 60 秒口述本案例。",
           ["C1 监管不可逆；C2 闸门+逆向；C3 状态前置+科目；C4 零错误出库。钉拆标选验各一句。",
            "面试。", "只讲报关 API。", "挂回 B-Ind 旋钮。", "「跨境是旋钮，不是第二主线。」"],
           "bx5-q3"),
    ]),
    "bx5-r1",
)

# Hub section listing all B-X
SEC_BX_HUB = f"""
<section class="block" id="bx-prod" data-toc="B-X · 生产级复杂场景" data-prio="p0">
  <h2><span class="sys-id">B-X</span>生产级复杂场景加深（正逆向主线）</h2>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>把 B-F/B-R/B-Ind 拧成「会在生产爆炸」的组合题。每案强制：四段闭环 · 钉拆标选验 · 多解法 · 练手详答 · 反思。<br><b>挂回：</b><a href="#s-c4">S-C4</a> → 下列案例 → <a href="#s-year">S-Year</a></div>

  <div class="plain"><div class="label">人话版</div>人话：下面不是玩具 demo，是外包进组第一周就可能撞上的组合拳。每个案例先写四段，再看取舍表，再做题。</div>

  <table>
    <thead><tr><th>#</th><th>场景</th><th>主线位置</th><th>高并发焦点</th><th>锚点</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>大促拼团+券叠加+分摊后退款并发</td><td>B-F↔B-R</td><td>成团临界·退款洪峰</td><td><a href="#bx-group-coupon">#bx-group-coupon</a></td></tr>
      <tr><td>2</td><td>支付成功 OMS→WMS 缺货补偿</td><td>B-F F3</td><td>回执洪峰·取消竞态</td><td><a href="#bx-pay-wms-short">#bx-pay-wms-short</a></td></tr>
      <tr><td>3</td><td>退货与寄修并行、换新锁库存</td><td>B-R</td><td>售后洪峰·预占</td><td><a href="#bx-repair-exchange">#bx-repair-exchange</a></td></tr>
      <tr><td>4</td><td>餐饮高峰取消与餐损</td><td>B-Ind</td><td>门店热点·取消尖刺</td><td><a href="#bx-food-peak">#bx-food-peak</a></td></tr>
      <tr><td>5</td><td>跨境清关失败逆向</td><td>B-Ind</td><td>失败风暴·闸门</td><td><a href="#bx-cross-border">#bx-cross-border</a></td></tr>
    </tbody>
  </table>
  <div class="koujue"><div class="label">口诀</div>复杂场景口诀：组合拳先四段，取舍表后五步，压测数字收口。</div>
""" + _boost_bx_hub() + f"""
{reflect("bx-hub-r1")}
</section>
"""

NEW_SECTIONS = SEC_C4 + SEC_BX_HUB + CASE1 + CASE2 + CASE3 + CASE4 + CASE5 + SEC_YEAR


def main():
    html = INDEX.read_text(encoding="utf-8")
    if "id=\"s-year\"" in html and "id=\"bx-prod\"" in html and "id=\"s-c4\"" in html:
        print("Already injected; refreshing by removing old markers…")
        # idempotent: strip previous injection between markers
        import re
        html = re.sub(
            r"\n<!-- YEAR-DEPTH-START -->.*?<!-- YEAR-DEPTH-END -->\n",
            "\n",
            html,
            count=1,
            flags=re.S,
        )
        # also remove CSS if re-adding
        html = html.replace(CSS_EXTRA, "")

    if CSS_EXTRA.strip() not in html:
        html = html.replace(".toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }\n</style>",
                            ".toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }\n"
                            + CSS_EXTRA + "</style>")

    # Update hero chips
    old_chips = """  <div class="hero-meta">
    <span class="chip"><b>主线</b> 正逆向+售后</span>
    <span class="chip"><b>写法</b> 本质优先</span>
    <span class="chip"><b>工程</b> K8s·AI</span>
    <span class="chip"><b>收官</b> S-Method</span>
  </div>"""
    new_chips = """  <div class="hero-meta">
    <span class="chip"><b>主线</b> 正逆向+售后</span>
    <span class="chip"><b>认知</b> 四段闭环</span>
    <span class="chip"><b>一年</b> 52 周 OKR</span>
    <span class="chip"><b>加深</b> B-X 生产案</span>
    <span class="chip"><b>收官</b> S-Method</span>
  </div>"""
    if old_chips in html:
        html = html.replace(old_chips, new_chips)

    # Update hero lead slightly
    html = html.replace(
        "写法像在公司做需求，拒绝技术拼凑。收官带走你自己的方法论 OS。",
        "写法像在公司做需求，拒绝技术拼凑。一年维度用 <a href=\"#s-year\">S-Year</a> 坚持；复杂场景强制 <a href=\"#s-c4\">四段闭环</a>。收官带走 <a href=\"#s-method\">钉拆标选验</a> OS。",
    )

    # Update weekend-plan pointer
    html = html.replace(
        "完整 10 周路线与自测清单已收口到 <b>S4</b>；此处只保留协作向提醒，避免双路线打架。",
        "8 周速成见 <b>S4</b>；<b>一年坚持</b>见 <a href=\"#s-year\">S-Year</a>（52 周·季度 OKR）。此处只保留协作向提醒。",
    )
    html = html.replace(
        "别同时追两条学习路线。统一走 <a href=\"#s4-review\">S4 复习地图</a>：测→补→再测。",
        "别同时追两条学习路线。速成走 <a href=\"#s4-review\">S4</a>；一年走 <a href=\"#s-year\">S-Year</a>：测→补→再测。",
    )

    # Expand S4 with link to year
    s4_marker = "  <h3>8 周主线路线</h3>"
    s4_extra = """  <div class="callout ok"><div class="label">一年维度</div>
    <p>8 周是「入门闭环」。若要以一年坚持加厚：进入 <a href="#s-year"><b>S-Year · 一年坚持路线</b></a>（12 月主题 · 52 周卡片 · 季度 OKR）。复杂生产案见 <a href="#bx-prod">B-X</a>。</p>
  </div>
  <h3>8 周主线路线</h3>"""
    if s4_marker in html and "S-Year · 一年坚持路线" not in html.split(s4_marker)[0][-500:]:
        html = html.replace(s4_marker, s4_extra, 1)

    # Insert C4 after s2-method section ends (before biz-4d-hub)
    anchor_c4 = '<section class="block" id="biz-4d-hub"'
    payload = "\n<!-- YEAR-DEPTH-START -->\n" + NEW_SECTIONS + "\n<!-- YEAR-DEPTH-END -->\n"
    # Actually split: put C4 before biz-4d; put BX+cases after b-industry; put year after s4
    # Simpler: one block before casebook
    insert_at = '<section class="block" id="casebook"'
    if "<!-- YEAR-DEPTH-START -->" not in html:
        if insert_at not in html:
            raise SystemExit("casebook anchor not found")
        # Split NEW_SECTIONS: C4 early, rest before casebook
        # Put all before casebook for simpler TOC order near production cases + year before accidents
        # Better TOC: C4 after S2, BX after B-Ind, Year after S4
        pass

    # Triple injection for better TOC order
    if 'id="s-c4"' not in html:
        if anchor_c4 not in html:
            raise SystemExit("biz-4d-hub not found")
        html = html.replace(
            anchor_c4,
            "\n<!-- YEAR-DEPTH-START -->\n" + SEC_C4 + "\n" + anchor_c4,
            1,
        )

    if 'id="bx-prod"' not in html:
        lateral = '<section class="block" id="b-lateral"'
        if lateral not in html:
            raise SystemExit("b-lateral not found")
        html = html.replace(
            lateral,
            SEC_BX_HUB + CASE1 + CASE2 + CASE3 + CASE4 + CASE5 + "\n" + lateral,
            1,
        )

    if 'id="s-year"' not in html:
        after_s4 = '<section class="block" id="casebook"'
        if after_s4 not in html:
            raise SystemExit("casebook not found for year insert")
        html = html.replace(
            after_s4,
            SEC_YEAR + "\n<!-- YEAR-DEPTH-END -->\n" + after_s4,
            1,
        )

    # Update meta description
    html = html.replace(
        'content="需求驱动：下单正向（优惠/支付/OMS/WMS）× 逆向售后维修；餐饮/跨境为配置；T 层与 S-MS 为零件。可迁移、可讲解、可落地。"',
        'content="需求驱动正逆向闭环：一年52周OKR、认知四段闭环、B-X生产级复杂场景；Skills/MCP/RAG；钉拆标选验。可迁移、可讲解、可落地。"',
    )

    # S0 table row for new nodes
    s0_row_anchor = "<tr><td><code>S-Method</code></td><td><b>钉拆标选验五步法</b>（收官）</td></tr>"
    s0_extra = (
        "<tr><td><code>S-C4</code></td><td><b>认知闭环四段</b>（本质→实现→原理→实质）</td></tr>\n"
        "      <tr><td><code>S-Year</code></td><td><b>一年坚持</b>（12月·52周·季度OKR）</td></tr>\n"
        "      <tr><td><code>B-X</code></td><td><b>生产级复杂场景</b>×5（挂主线）</td></tr>\n"
        "      " + s0_row_anchor
    )
    if "S-Year" not in html.split("S-Method")[0] and s0_row_anchor in html:
        # check if already added
        pass
    if "<code>S-Year</code>" not in html and s0_row_anchor in html:
        html = html.replace(s0_row_anchor, s0_extra, 1)

    INDEX.write_text(html, encoding="utf-8")
    MIRROR.write_text(html, encoding="utf-8")
    print(f"Wrote {INDEX} ({INDEX.stat().st_size} bytes)")
    print(f"Wrote {MIRROR} ({MIRROR.stat().st_size} bytes)")
    # counts
    for aid in ["s-c4", "s-year", "bx-prod", "bx-group-coupon", "bx-pay-wms-short",
                "bx-repair-exchange", "bx-food-peak", "bx-cross-border"]:
        print(f"  anchor #{aid}:", html.count(f'id="{aid}"'))


if __name__ == "__main__":
    main()
