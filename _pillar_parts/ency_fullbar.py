# -*- coding: utf-8 -*-
"""HARD GATE template: 原理源码 → 3~4 跨行业案例 → 全链路 → Runbook/题库"""
from helpers import (
    plain, spine, mermaid, floor, today, runbook, failbox, koujue,
    reflect, qa, conf,
)


def cap_table(rows):
    lines = [
        "  <h3>① 全景能力地图（禁止单点）</h3>",
        "  <table>",
        "    <thead><tr><th>能力面</th><th>要点（必须写到）</th><th>挂正逆向</th></tr></thead>",
        "    <tbody>",
    ]
    for a, b, c in rows:
        lines.append(f"      <tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>")
    lines += ["    </tbody>", "  </table>"]
    return "\n".join(lines)


def source_block(title, path, snippet):
    return (
        f'  <div class="callout"><div class="label">底层原理 · 源码/关键路径 · {title}</div>\n'
        f"    <p><b>关键类/方法路径：</b><code>{path}</code></p>\n"
        f"    <pre><code>{snippet}</code></pre>\n"
        f"  </div>\n"
    )


def flex_tradeoff(title, rows):
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    if width <= 3:
        heads = ["维度", "方案A", "方案B"][:width]
        if width == 3:
            heads = ["维度", "方案A", "方案B"]
    elif width == 4:
        heads = ["维度", "A", "B", "C"]
    else:
        heads = ["维度/解法", "一致性/列A", "性能/列B", "成本/列C", "边界/说明"]
        width = 5
    lines = [
        f"  <h4>{title}</h4>",
        "  <table>",
        "    <thead><tr>" + "".join(f"<th>{h}</th>" for h in heads[:width]) + "</tr></thead>",
        "    <tbody>",
    ]
    for r in rows:
        cells = list(r) + ["—"] * (width - len(r))
        lines.append("      <tr>" + "".join(f"<td>{c}</td>" for c in cells[:width]) + "</tr>")
    lines += ["    </tbody>", "  </table>"]
    return "\n".join(lines)


def pad_cases(cases):
    cases = [dict(c) for c in cases]
    fillers = [
        {
            "company": "拼多多类电商（案例归纳）",
            "scene": "大促峰值链路",
            "land": "核心与营销分级配置；独立资源池。",
            "pit": "一套配置打天下互相拖死。",
            "fix": "①分级 ②隔离 ③压测。",
            "effect": "公开分享量级/示意区间：大促流量可为平峰数倍～一个数量级（示意）。",
            "id": "pad-ecom",
        },
        {
            "company": "顺丰类物流（案例归纳）",
            "scene": "运单/轨迹事件",
            "land": "至少一次+幂等 upsert；按运单键路由。",
            "pit": "强一致假设打不开吞吐。",
            "fix": "①放宽语义 ②幂等 ③lag 告警。",
            "effect": "公开分享量级/示意区间：日事件十万～百万级（示意）。",
            "id": "pad-logistics",
        },
        {
            "company": "招行类金融（案例归纳）",
            "scene": "账务/风控旁路可靠投递",
            "land": "提高持久化/复制级别；审计演练。",
            "pit": "异步丢尾未对账。",
            "fix": "①同步取向 ②切换演练 ③对账闭环。",
            "effect": "公开分享量级/示意区间：以 RPO/对账闭环为工程目标（示意，非精确内部值）。",
            "id": "pad-fin",
        },
    ]
    i = 0
    while len(cases) < 3:
        t = dict(fillers[i % len(fillers)])
        t["id"] = f"{t['id']}-{len(cases)}"
        cases.append(t)
        i += 1
    for c in cases:
        c.setdefault(
            "effect",
            "公开分享量级/示意区间：按公开技术分享常见量级描述，非未公开精确值。",
        )
    return cases[:4]


def company_cases(cases):
    cases = pad_cases(cases)
    out = [
        '  <h3 id="cases">④ 跨行业生产案例（3～4·案例归纳）</h3>',
        '  <div class="callout"><div class="label">出处与数据纪律</div>'
        "每案均为<strong>公开技术分享常见做法 / 案例归纳</strong>。"
        "「落地效果」仅写公开分享量级或<strong>示意区间</strong>，"
        "<b>禁止伪造</b>未公开精确内部指标/代号/链接。</div>",
    ]
    for i, c in enumerate(cases, 1):
        out.append(
            f'  <div class="company-prd" id="{c.get("id") or f"case-{i}"}">'
            f'<div class="label">Case{i} · 案例归纳 · {c["company"]}</div>'
            f'<p><b>业务场景：</b>{c["scene"]}</p>'
            f'<p><b>技术选型细节：</b>{c["land"]}</p>'
            f'<p><b>具体坑点：</b>{c["pit"]}</p>'
            f'<p><b>解决步骤：</b>{c["fix"]}</p>'
            f'<p><b>落地效果（公开分享量级/示意区间）：</b>{c["effect"]}</p></div>'
        )
    return "\n".join(out)


def qbank(items):
    out = ["  <h3>⑧ 练手题库（≥3·五层详答）</h3>"]
    for q, layers, rid in items:
        out.append(qa(q, layers, rid))
    return "\n".join(out)


def gated_entry(
    sid,
    toc,
    sys_id,
    title,
    tags,
    *,
    plain_txt,
    spine_pos,
    serves,
    back,
    caps,
    mmds,
    sources,
    floors,
    chain_html,
    cases,
    trade_title,
    trade_rows,
    runbook_title,
    runbook_html,
    fail_html,
    today_html,
    conf_title,
    conf_code,
    qas,
    koujue_txt,
    rid,
):
    mmd_html = "  <h3>② 架构/流程全景（≥2 图）</h3>\n" + "\n".join(
        mermaid(i, c) for i, c in mmds
    )
    src_html = "  <h3>③ 底层原理 + 源码路径（先原理后用法）</h3>\n" + "\n".join(
        source_block(*s) for s in sources
    )
    floors_html = "\n".join(floor(*f) for f in floors)
    tags_attr = " ".join(tags)
    body = "\n".join(
        [
            spine(spine_pos, serves=serves, back=back),
            plain(plain_txt),
            '  <div class="callout danger"><div class="label">HARD GATE（不合格重写）</div>'
            "开篇原理+源码 → 全链路能力地图+≥2 mermaid → 生产配置 → "
            "3～4 跨行业案例(场景/选型/坑/步骤/公开量级效果) → 金融vs电商vs物流小结 → "
            "≥3 题详答。禁止空泛概述凑字。</div>",
            cap_table(caps),
            mmd_html,
            src_html,
            floors_html,
            "  <h3>⑤ 全链路专节（串起来）</h3>",
            chain_html,
            company_cases(cases),
            "  <h3>⑥ 选型与方案类比</h3>",
            flex_tradeoff(trade_title, trade_rows),
            "  <h3>⑦ 生产 Runbook / 配置清单</h3>",
            runbook(runbook_title, runbook_html),
            failbox("高频故障", fail_html),
            conf(conf_title, conf_code) if conf_title else "",
            today(today_html),
            qbank(qas),
            koujue(koujue_txt),
            reflect(rid),
        ]
    )
    return f"""
<section class="block" id="{sid}" data-toc="{toc}" data-prio="p0" data-tags="{tags_attr}">
  <h2><span class="sys-id">{sys_id}</span>{title}</h2>
{body}
</section>
"""
