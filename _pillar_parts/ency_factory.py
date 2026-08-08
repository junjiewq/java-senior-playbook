# -*- coding: utf-8 -*-
"""Compact section factory for encyclopedia thickness."""
from helpers import (
    qa, c4, mermaid, spine, plain, koujue, reflect, today, floor, tradeoff, conf, checklist,
)


def sec(sid: str, toc: str, sys_id: str, title: str, body: str, prio: str = "p1") -> str:
    return f"""
<section class="block" id="{sid}" data-toc="{toc}" data-prio="{prio}">
  <h2><span class="sys-id">{sys_id}</span>{title}</h2>
{body}
</section>
"""


def deep(
    *,
    plain_txt: str,
    biz: str,
    impl: str,
    principle: str,
    substance: str,
    hc: str = "",
    floor_title: str = "",
    structure: str = "",
    source_path: str = "",
    online: str = "",
    verify: str = "",
    mermaid_id: str = "",
    mermaid_code: str = "",
    mermaid_id2: str = "",
    mermaid_code2: str = "",
    today_html: str = "",
    trade_title: str = "",
    trade_rows=None,
    conf_title: str = "",
    conf_code: str = "",
    qas=None,
    koujue_txt: str = "",
    reflect_id: str = "",
    spine_pos: str = "",
    serves: str = "",
    back: str = "",
    extra_html: str = "",
) -> str:
    parts = []
    if spine_pos:
        parts.append(spine(spine_pos, serves=serves, back=back))
    parts.append(plain(plain_txt))
    parts.append(c4(biz, impl, principle, substance, hc))
    if floor_title:
        parts.append(floor(floor_title, structure, source_path, online, verify))
    if mermaid_id and mermaid_code:
        parts.append(mermaid(mermaid_id, mermaid_code))
    if mermaid_id2 and mermaid_code2:
        parts.append(mermaid(mermaid_id2, mermaid_code2))
    if trade_title and trade_rows:
        parts.append(tradeoff(trade_title, trade_rows))
    if conf_title and conf_code:
        parts.append(conf(conf_title, conf_code))
    if today_html:
        parts.append(today(today_html))
    if extra_html:
        parts.append(extra_html)
    if koujue_txt:
        parts.append(koujue(koujue_txt))
    for i, item in enumerate(qas or []):
        q, layers, rid = item
        parts.append(qa(q, layers, rid))
    if reflect_id:
        parts.append(reflect(reflect_id))
    return "\n".join(parts)
