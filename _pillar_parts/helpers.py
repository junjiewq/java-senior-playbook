# -*- coding: utf-8 -*-
"""Shared HTML helpers for extreme pillar injection."""


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


def five(nail, split, mark, pick, verify) -> str:
    return f"""  <div class="callout"><div class="label">挂五步法 · 钉拆标选验</div>
    <ol>
      <li><b>钉</b> {nail}</li>
      <li><b>拆</b> {split}</li>
      <li><b>标</b> {mark}</li>
      <li><b>选</b> {pick}</li>
      <li><b>验</b> {verify}</li>
    </ol>
  </div>"""


def tradeoff(title, rows) -> str:
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


def mermaid(diag_id: str, code: str) -> str:
    return f'''  <div class="mermaid-wrap" id="{diag_id}">
    <div class="diag-actions"><button class="btn" type="button" data-png="{diag_id}">导出 PNG</button></div>
    <pre class="mermaid">
{code}
    </pre>
  </div>
'''


def spine(pos: str, serves: str = "", back: str = "") -> str:
    extra = ""
    if serves:
        extra += f"<br><b>服务业务闭环：</b>{serves}"
    if back:
        extra += f"<br><b>挂回：</b>{back}"
    return (
        f'  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>'
        f"{pos}{extra}</div>\n"
    )


def essence(biz_one, biz_exp, tech_one, tech_exp, without="") -> str:
    wo = f"<p><b>若没有它，业务哪一步会坏：</b>{without}</p>" if without else ""
    return f"""  <div class="essence">
    <div class="essence-col">
      <div class="label">业务本质</div>
      <p class="one">{biz_one}</p>
      <p>{biz_exp}</p>
    </div>
    <div class="essence-col">
      <div class="label">技术本质</div>
      <p class="one">{tech_one}</p>
      <p>{tech_exp}</p>
    </div>
    {wo}
  </div>
"""


def company_prd(bg, scope_in, scope_out, main_flow, ex_flow, accept, observe) -> str:
    return f"""  <div class="company-prd">
    <div class="label">像在公司做需求 · 评审口吻</div>
    <p><b>背景：</b>{bg}</p>
    <p><b>In Scope：</b>{scope_in}</p>
    <p><b>Out of Scope：</b>{scope_out}</p>
    <p><b>主流程：</b>{main_flow}</p>
    <p><b>异常流程：</b>{ex_flow}</p>
    <p><b>验收：</b>{accept}</p>
    <p><b>上线观察：</b>{observe}</p>
  </div>
"""


def plain(text: str) -> str:
    return f'  <div class="plain"><div class="label">人话版</div>{text}</div>\n'


def koujue(text: str) -> str:
    return f'  <div class="koujue"><div class="label">口诀</div>{text}</div>\n'


def failbox(title: str, body: str) -> str:
    return f'  <div class="failbox"><div class="label">故障模式 · {title}</div>{body}</div>\n'


def runbook(title: str, steps_html: str) -> str:
    return f'  <div class="callout"><div class="label">生产 Runbook · {title}</div>{steps_html}</div>\n'


def pit(text: str) -> str:
    return f'  <div class="callout danger"><div class="label">踩坑</div>{text}</div>\n'


def ban(text: str) -> str:
    return f'  <div class="callout danger"><div class="label">禁止清单（写死）</div>{text}</div>\n'


def today(text: str) -> str:
    """今天在订单/售后怎么改代码或配配置 — 反理论强制落地块."""
    return (
        f'  <div class="callout ok"><div class="label">今天怎么落地（别只背定义）</div>'
        f"{text}</div>\n"
    )


def checklist(title: str, items: list) -> str:
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'  <h4>{title}</h4>\n  <ul class="checklist">{lis}</ul>\n'


def conf(title: str, code: str) -> str:
    return f"  <h4>{title}</h4>\n  <pre><code>{code}</code></pre>\n"


def floor(title: str, structure: str, source_path: str, online: str, verify: str) -> str:
    """掀底板：数据结构/源码路径 → 线上现象 → 验证指标（服务实战，不是两张皮）."""
    return f"""  <div class="callout"><div class="label">掀底板 · {title}</div>
    <p><b>底板结构/算法/协议：</b>{structure}</p>
    <p><b>源码/实现路径（认知级）：</b>{source_path}</p>
    <p><b>订单/售后线上怎么露馅：</b>{online}</p>
    <p><b>排查时看什么能验证你懂了底板：</b>{verify}</p>
  </div>
"""
