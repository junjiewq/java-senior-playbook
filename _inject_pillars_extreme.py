#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inject extreme pillars into index.html + mirror. Idempotent via per-block markers."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "_pillar_parts"
INDEX = ROOT / "index.html"
MIRROR = ROOT.parent / "高级Java外包-系统学习技术白皮书.html"

sys.path.insert(0, str(PARTS))

from ms_extreme import build as build_ms  # noqa: E402
from k8s_extreme import build as build_k8s  # noqa: E402
from ai_extreme import build as build_ai  # noqa: E402
from cross_trinity import build as build_cross  # noqa: E402
from foundations_extreme import build as build_found  # noqa: E402
from ddd_extreme import build as build_ddd  # noqa: E402
from mgmt_extreme import build as build_mgmt  # noqa: E402
from spring_ms_floor import build as build_ms_floor  # noqa: E402

BLOCKS = [
    "TONE",
    "DDD_MGMT",
    "K8S",
    "AI",
    "FOUND",
    "MS",
    "CROSS",
]


def mark(name: str, body: str) -> str:
    return f"\n<!-- PILLAR-{name}-START -->\n{body}\n<!-- PILLAR-{name}-END -->\n"


def strip_blocks(html: str) -> str:
    for name in BLOCKS:
        html = re.sub(
            rf"\n?<!-- PILLAR-{name}-START -->.*?<!-- PILLAR-{name}-END -->\n?",
            "\n",
            html,
            count=1,
            flags=re.S,
        )
    # legacy single-marker cleanup
    html = re.sub(
        r"\n?<!-- PILLAR-EXTREME-START -->.*?<!-- PILLAR-EXTREME-END -->\n?",
        "\n",
        html,
        count=1,
        flags=re.S,
    )
    return html


TONE_BANNER = """
<section class="block" id="s-tone-x" data-toc="S-Tone · 实战+底板写法" data-prio="p0">
  <h2><span class="sys-id">S-Tone</span>本册加厚写法：人话 → 掀底板 → 落地 → 回扣业务</h2>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>约束极致章文风：通俗但不浅、底层但不悬空。<br><b>挂回：</b>S-C4 四段 → 本约束 → 各极致章</div>
  <div class="plain"><div class="label">人话版</div>先讲今天单子会怎么坏；再掀数据结构/源码路径；再给配置和代码改法；最后用对账/客诉验收。禁止只堆名词。</div>
  <table>
    <thead><tr><th>段落</th><th>必须有</th><th>禁止</th></tr></thead>
    <tbody>
      <tr><td>人话引入</td><td>比喻或真实场景</td><td>空泛定义段</td></tr>
      <tr><td>掀底板</td><td>结构/协议 + 关键类/路径 + 线上现象 + 验证指标</td><td>只写「注意线程安全」</td></tr>
      <tr><td>今天落地</td><td>配置/SQL/清单/状态机</td><td>「原则上应该」</td></tr>
      <tr><td>业务实质</td><td>挂买成/退成验收</td><td>离开订单谈中间件</td></tr>
    </tbody>
  </table>
  <div class="koujue"><div class="label">口诀</div>人话进门，底板见血，清单收口，单号回扣。</div>
</section>
"""


def patch_nav(html: str) -> str:
    s0_anchor = "<tr><td><code>S-MS</code></td><td>拆分卡点，服务主线边界</td></tr>"
    if "S-MS-X / T-K8s-X" not in html and s0_anchor in html:
        html = html.replace(
            s0_anchor,
            s0_anchor
            + "\n      <tr><td><code>S-MS-X / T-K8s-X / T-AI-X</code></td><td><b>三大支柱极致落地</b>（含掀底板）</td></tr>"
            + "\n      <tr><td><code>S-DDD-X / S-Mgmt-X / T-Found-X</code></td><td><b>DDD模式·管理·基础件底板</b></td></tr>"
            + "\n      <tr><td><code>X-大促</code></td><td>微服务×K8s×AI 演练剧本</td></tr>",
            1,
        )
    s1_row = (
        '<tr><td>Skills / MCP / RAG / 多智能体</td><td>人效辅驾（重头戏）</td>'
        '<td><a href="#t-ai-stack">T-AI-Stack</a></td></tr>'
    )
    if 'href="#s-ms-x"' not in html and s1_row in html:
        html = html.replace(
            s1_row,
            s1_row
            + '\n      <tr><td>微服务/K8s/AI 极致</td><td>工程+副驾加深</td>'
            '<td><a href="#s-ms-x">S-MS-X</a> · <a href="#t-k8s-x">T-K8s-X</a> · <a href="#t-ai-x">T-AI-X</a></td></tr>'
            + '\n      <tr><td>DDD·模式·管理·基础件底板</td><td>可交付方法论</td>'
            '<td><a href="#s-ddd-x">S-DDD-X</a> · <a href="#s-mgmt-x">S-Mgmt-X</a> · <a href="#t-found-x">T-Found-X</a></td></tr>'
            + '\n      <tr><td>大促三联演练</td><td>交叉章</td><td><a href="#x-promo-trinity">X-大促</a></td></tr>',
            1,
        )
    old = '<span class="chip"><b>加深</b> B-X 生产案</span>'
    new = (
        '<span class="chip"><b>加深</b> B-X·极致支柱</span>\n'
        '    <span class="chip"><b>底板</b> 源码级原理</span>'
    )
    if old in html and "源码级原理" not in html:
        html = html.replace(old, new, 1)
    html = html.replace(
        'content="需求驱动正逆向闭环：一年52周OKR、认知四段闭环、B-X生产级复杂场景；Skills/MCP/RAG；钉拆标选验。可迁移、可讲解、可落地。"',
        'content="需求驱动正逆向闭环：微服务/K8s/AI极致、DDD模式、管理排期、JVM/JUC/MySQL/Redis/MQ掀底板；一年OKR；钉拆标选验。"',
    )
    return html


def insert_after_section(html: str, section_id: str, chunk: str) -> str:
    pattern = rf'(<section class="block" id="{section_id}".*?</section>)'
    m = re.search(pattern, html, re.S)
    if not m:
        raise SystemExit(f"section not found: {section_id}")
    return html.replace(m.group(1), m.group(1) + chunk, 1)


def insert_before_section(html: str, section_id: str, chunk: str) -> str:
    anchor = f'<section class="block" id="{section_id}"'
    if anchor not in html:
        raise SystemExit(f"section not found: {section_id}")
    return html.replace(anchor, chunk + anchor, 1)


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    before = len(html.encode("utf-8"))
    html = strip_blocks(html)

    html = insert_after_section(html, "s-c4", mark("TONE", TONE_BANNER))
    html = insert_after_section(html, "s-tone-x", mark("DDD_MGMT", build_ddd() + build_mgmt()))
    html = insert_after_section(html, "t-docker-k8s", mark("K8S", build_k8s()))
    # prefer after deepest AI chapter
    ai_host = "t-as-deep" if 'id="t-as-deep"' in html else "t-ai-stack"
    html = insert_after_section(html, ai_host, mark("AI", build_ai()))
    html = insert_before_section(html, "s-ms", mark("FOUND", build_found()))
    html = insert_after_section(html, "s-ms-highlights", mark("MS", build_ms() + build_ms_floor()))
    html = insert_after_section(html, "s-ms-x-floor", mark("CROSS", build_cross()))

    html = patch_nav(html)

    INDEX.write_text(html, encoding="utf-8")
    MIRROR.write_text(html, encoding="utf-8")
    # hard sync + verify identical (local Chinese mirror must always match)
    import hashlib
    import shutil

    shutil.copyfile(INDEX, MIRROR)
    h1 = hashlib.md5(INDEX.read_bytes()).hexdigest()
    h2 = hashlib.md5(MIRROR.read_bytes()).hexdigest()
    if h1 != h2:
        raise SystemExit(f"mirror mismatch: {h1} != {h2}")
    after = INDEX.stat().st_size
    print(f"Wrote {INDEX} ({after} bytes) delta_vs_read={after - before}")
    print(f"Synced {MIRROR} md5={h1}")

    for a in [
        "s-tone-x", "s-ddd-x", "s-mgmt-x", "t-found-x", "t-found-matrix",
        "found-mq-matrix", "found-lock-matrix", "s-ms-x", "s-ms-x-floor",
        "t-k8s-x", "t-ai-x", "x-promo-trinity", "s-ddd-x-patterns",
        "mgmt-waterfall-agile", "t-found-jvm", "t-found-rocket",
    ]:
        print(f"  #{a}: {html.count(f'id=\"{a}\"')}")


if __name__ == "__main__":
    main()
