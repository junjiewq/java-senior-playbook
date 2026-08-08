#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""APPEND-ONLY: inject encyclopedia + full-text search. Sync index.html + Chinese mirror."""
from __future__ import annotations

import hashlib
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "_pillar_parts"
INDEX = ROOT / "index.html"
MIRROR = ROOT.parent / "高级Java外包-系统学习技术白皮书.html"

sys.path.insert(0, str(PARTS))

from ency_hub import build as build_hub  # noqa: E402
from ency_biz import build as build_biz  # noqa: E402
from ency_java import build as build_java  # noqa: E402
from ency_data import build as build_data  # noqa: E402
from ency_bd import build as build_bd  # noqa: E402
from ency_ai import build as build_ai  # noqa: E402
from ency_cases import build as build_cases  # noqa: E402

MARKER_START = "<!-- ENCYCLOPEDIA-START -->"
MARKER_END = "<!-- ENCYCLOPEDIA-END -->"
SEARCH_CSS_MARK = "/* ENCY-SEARCH-CSS */"
SEARCH_JS_MARK = "/* ENCY-SEARCH-JS */"
CONTENT_END = "  </div><!-- .content -->"

SEARCH_CSS = """
/* ENCY-SEARCH-CSS */
.topbar { flex-wrap: wrap; gap: .55rem; align-items: center; }
.topbar-search {
  position: relative; flex: 1 1 220px; min-width: 160px; max-width: 420px;
}
.topbar-search input {
  width: 100%; padding: .45rem .7rem .45rem 2rem;
  border-radius: 10px; border: 1px solid var(--line);
  background: var(--bg2); color: var(--text);
  font: inherit; font-size: .88rem; outline: none;
}
.topbar-search input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(61,207,182,.15); }
.topbar-search .search-ico {
  position: absolute; left: .55rem; top: 50%; transform: translateY(-50%);
  color: var(--faint); font-size: .85rem; pointer-events: none;
}
.search-panel {
  display: none; position: absolute; left: 0; right: 0; top: calc(100% + 6px);
  max-height: min(60vh, 420px); overflow: auto; z-index: 80;
  background: var(--panel-solid); border: 1px solid var(--line-strong);
  border-radius: 12px; box-shadow: var(--shadow); padding: .35rem;
}
.search-panel.open { display: block; }
.search-hit {
  display: block; width: 100%; text-align: left; border: 0; cursor: pointer;
  background: transparent; color: var(--text); padding: .55rem .65rem;
  border-radius: 8px; font: inherit; font-size: .84rem; line-height: 1.45;
}
.search-hit:hover, .search-hit.active { background: rgba(61,207,182,.12); }
.search-hit .hit-title { font-weight: 700; color: var(--accent); margin-bottom: .15rem; }
.search-hit .hit-snip { color: var(--muted); font-size: .78rem; }
.search-hit mark { background: rgba(240,180,41,.35); color: var(--text); border-radius: 2px; padding: 0 .1rem; }
.search-empty { padding: .7rem; color: var(--faint); font-size: .84rem; }
section.block.search-flash {
  outline: 2px solid var(--accent-2);
  box-shadow: 0 0 0 6px rgba(240,180,41,.18);
  transition: outline .2s, box-shadow .2s;
}
@media (max-width: 900px) {
  .topbar-search { flex: 1 1 100%; max-width: none; order: 3; }
}
"""

SEARCH_TOPBAR = """    <div class="topbar-search" id="topbarSearch">
      <span class="search-ico" aria-hidden="true">/</span>
      <input id="docSearch" type="search" placeholder="搜索全文（中文/英文）…" autocomplete="off" aria-label="全文搜索" />
      <div class="search-panel" id="searchPanel" role="listbox" aria-label="搜索结果"></div>
    </div>
"""

SEARCH_JS = r"""
  /* ENCY-SEARCH-JS */
  (function initDocSearch() {
    const input = document.getElementById("docSearch");
    const panel = document.getElementById("searchPanel");
    if (!input || !panel) return;

    const index = [...document.querySelectorAll("section.block")].map((sec) => {
      const title = (sec.querySelector("h2")?.textContent || sec.dataset.toc || sec.id || "").replace(/\s+/g, " ").trim();
      const text = sec.innerText.replace(/\s+/g, " ").trim();
      return { id: sec.id, title, text, el: sec };
    });

    let hits = [];
    let active = -1;

    function snip(text, q) {
      const i = text.toLowerCase().indexOf(q.toLowerCase());
      if (i < 0) return text.slice(0, 120) + (text.length > 120 ? "…" : "");
      const start = Math.max(0, i - 40);
      const end = Math.min(text.length, i + q.length + 80);
      let s = (start > 0 ? "…" : "") + text.slice(start, end) + (end < text.length ? "…" : "");
      const re = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "ig");
      return s.replace(re, (m) => "<mark>" + m + "</mark>");
    }

    function render() {
      if (!input.value.trim()) {
        panel.classList.remove("open");
        panel.innerHTML = "";
        hits = [];
        active = -1;
        return;
      }
      if (!hits.length) {
        panel.innerHTML = '<div class="search-empty">无匹配。试试「分摊」「PolarDB」「Checkpoint」「Agent」</div>';
        panel.classList.add("open");
        return;
      }
      panel.innerHTML = hits.map((h, i) => (
        '<button type="button" class="search-hit' + (i === active ? " active" : "") + '" data-i="' + i + '" role="option">' +
        '<div class="hit-title">' + escapeHtml(h.title) + '</div>' +
        '<div class="hit-snip">' + h.snipHtml + '</div></button>'
      )).join("");
      panel.classList.add("open");
    }

    function search(q) {
      q = q.trim();
      if (!q) { hits = []; render(); return; }
      const ql = q.toLowerCase();
      hits = [];
      for (const item of index) {
        const t = item.title.toLowerCase();
        const b = item.text.toLowerCase();
        const inTitle = t.includes(ql);
        const inBody = b.includes(ql);
        if (!inTitle && !inBody) continue;
        let score = inTitle ? 100 : 0;
        score += (inTitle ? 0 : 0) + (b.split(ql).length - 1);
        hits.push({
          id: item.id,
          title: item.title,
          snipHtml: snip(inTitle ? item.title + " — " + item.text.slice(0, 200) : item.text, q),
          score
        });
      }
      hits.sort((a, b) => b.score - a.score);
      hits = hits.slice(0, 40);
      active = hits.length ? 0 : -1;
      render();
    }

    function go(i) {
      const h = hits[i];
      if (!h) return;
      const el = document.getElementById(h.id);
      if (!el) return;
      panel.classList.remove("open");
      input.blur();
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      el.classList.add("search-flash");
      setTimeout(() => el.classList.remove("search-flash"), 2200);
      history.replaceState(null, "", "#" + h.id);
    }

    let timer;
    input.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(() => search(input.value), 120);
    });
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); if (hits.length) { active = (active + 1) % hits.length; render(); } }
      else if (e.key === "ArrowUp") { e.preventDefault(); if (hits.length) { active = (active - 1 + hits.length) % hits.length; render(); } }
      else if (e.key === "Enter") { e.preventDefault(); if (active >= 0) go(active); }
      else if (e.key === "Escape") { panel.classList.remove("open"); input.blur(); }
    });
    panel.addEventListener("click", (e) => {
      const btn = e.target.closest(".search-hit");
      if (!btn) return;
      go(+btn.dataset.i);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "/" && !e.metaKey && !e.ctrlKey && !e.altKey) {
        const tag = (e.target && e.target.tagName) || "";
        if (tag === "INPUT" || tag === "TEXTAREA" || e.target.isContentEditable) return;
        e.preventDefault();
        input.focus();
        input.select();
      }
      if (e.key === "Escape") panel.classList.remove("open");
    });
    document.addEventListener("click", (e) => {
      if (!e.target.closest("#topbarSearch")) panel.classList.remove("open");
    });
  })();
"""


def strip_ency(html: str) -> str:
    return re.sub(
        rf"\n?{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n?",
        "\n",
        html,
        count=1,
        flags=re.S,
    )


def ensure_search_css(html: str) -> str:
    if SEARCH_CSS_MARK in html:
        html = re.sub(
            rf"\n?/\* ENCY-SEARCH-CSS \*/.*?@media \(max-width: 900px\) \{{.*?\n\}}\n",
            "\n",
            html,
            count=1,
            flags=re.S,
        )
    # insert before closing </style> of main block — first </style>
    return html.replace("</style>", SEARCH_CSS + "\n</style>", 1)


def ensure_search_topbar(html: str) -> str:
    if 'id="docSearch"' in html:
        return html
    anchor = '    <div class="toolbar">'
    if anchor not in html:
        raise SystemExit("toolbar not found")
    return html.replace(anchor, SEARCH_TOPBAR + anchor, 1)


def ensure_search_js(html: str) -> str:
    if SEARCH_JS_MARK in html:
        html = re.sub(
            rf"\n?  {re.escape(SEARCH_JS_MARK)}.*?\)\(\);\n",
            "\n",
            html,
            count=1,
            flags=re.S,
        )
    # append before final IIFE closing — insert before last `})();` of main script
    needle = "  // PNG export for diagrams"
    if needle not in html:
        raise SystemExit("png export marker not found for JS inject")
    return html.replace(needle, SEARCH_JS + "\n" + needle, 1)


def build_ency_html() -> str:
    body = "\n".join([
        build_hub(),
        build_biz(),
        build_java(),
        build_data(),
        build_bd(),
        build_ai(),
        build_cases(),
    ])
    return f"\n{MARKER_START}\n{body}\n{MARKER_END}\n"


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    before = INDEX.stat().st_size
    front_h1 = re.search(r"<h1>.*?</h1>", html, re.S)
    front_s0 = 'id="s0-system"' in html

    html = strip_ency(html)
    html = ensure_search_css(html)
    html = ensure_search_topbar(html)
    html = ensure_search_js(html)

    chunk = build_ency_html()
    if CONTENT_END not in html:
        raise SystemExit("content end marker not found")
    html = html.replace(CONTENT_END, chunk + CONTENT_END, 1)

    # soft TOC chip in hero — only add if missing; do not rewrite lead
    if "ENCY 百科" not in html and '<span class="chip"><b>收官</b> S-Method</span>' in html:
        html = html.replace(
            '<span class="chip"><b>收官</b> S-Method</span>',
            '<span class="chip"><b>收官</b> S-Method</span>\n    <span class="chip"><b>附录</b> ENCY 百科</span>',
            1,
        )

    INDEX.write_text(html, encoding="utf-8")
    shutil.copyfile(INDEX, MIRROR)

    after = INDEX.stat().st_size
    h1 = hashlib.md5(INDEX.read_bytes()).hexdigest()
    h2 = hashlib.md5(MIRROR.read_bytes()).hexdigest()
    if h1 != h2:
        raise SystemExit("mirror mismatch")

    # verify front unchanged essentials
    html2 = INDEX.read_text(encoding="utf-8")
    front_h1_after = re.search(r"<h1>.*?</h1>", html2, re.S)
    if not front_s0 or 'id="s0-system"' not in html2:
        raise SystemExit("s0-system missing")
    if front_h1 and front_h1_after and front_h1.group(0) != front_h1_after.group(0):
        raise SystemExit("H1 changed — abort semantics")

    ency_bytes = len(chunk.encode("utf-8"))
    print(f"before={before} after={after} delta={after-before} ency_chunk≈{ency_bytes}")
    print(f"md5={h1}")
    for a in [
        "ency", "ency-biz", "ency-j", "ency-d", "ency-d-dist", "ency-d-polardb",
        "ency-d-gauss", "ency-d-dm", "ency-d-tdsql", "ency-bd", "ency-ai",
        "ency-case", "ency-case-pdd", "ency-case-cmb", "ency-case-sf", "docSearch",
    ]:
        print(f"  #{a}: {html2.count(a)}")


if __name__ == "__main__":
    main()
