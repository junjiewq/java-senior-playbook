#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild pillars + encyclopedia, deepen P0 diag, inject doc-audit, sync mirror."""
from __future__ import annotations

import hashlib
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
MIRROR = ROOT.parent / "高级Java外包-系统学习技术白皮书.html"
PARTS = ROOT / "_pillar_parts"
sys.path.insert(0, str(PARTS))

from anti_water_boost import DOC_AUDIT, boost_p0_diag  # noqa: E402


def replace_section_inner(html: str, sid: str, insert_after_h2: str) -> str:
    """Insert boost HTML after the section's h2 (keep rest). Idempotent via marker."""
    mark = f"<!-- ANTI-WATER:{sid} -->"
    if mark in html:
        # remove previous boost block until next marker end
        html = re.sub(
            rf"{re.escape(mark)}.*?<!-- /ANTI-WATER:{sid} -->\n?",
            "",
            html,
            count=1,
            flags=re.S,
        )
    m = re.search(rf'(<section[^>]*id="{re.escape(sid)}"[^>]*>.*?</h2>)', html, re.S)
    if not m:
        print(f"WARN: section {sid} not found")
        return html
    chunk = f"{mark}\n{insert_after_h2}\n<!-- /ANTI-WATER:{sid} -->\n"
    return html[: m.end()] + "\n" + chunk + html[m.end() :]


def inject_doc_audit(html: str) -> str:
    mark_s, mark_e = "<!-- DOC-AUDIT-START -->", "<!-- DOC-AUDIT-END -->"
    html = re.sub(
        rf"\n?{re.escape(mark_s)}.*?{re.escape(mark_e)}\n?",
        "\n",
        html,
        count=1,
        flags=re.S,
    )
    # place before encyclopedia or at content end
    if "<!-- ENCYCLOPEDIA-START -->" in html:
        html = html.replace(
            "<!-- ENCYCLOPEDIA-START -->",
            f"{mark_s}\n{DOC_AUDIT}\n{mark_e}\n<!-- ENCYCLOPEDIA-START -->",
            1,
        )
    else:
        html = html.replace(
            "  </div><!-- .content -->",
            f"{mark_s}\n{DOC_AUDIT}\n{mark_e}\n  </div><!-- .content -->",
            1,
        )
    return html


def deepen_bx_cases(html: str) -> str:
    """Add dual mermaid to each BX case if missing."""
    boosts = {
        "bx-group-coupon": """
  <div class="mermaid-wrap" id="diag-bx1-flow">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx1-flow">导出 PNG</button></div>
    <pre class="mermaid">
flowchart TD
  Join[参团支付] --> Seat[占座]
  Seat --> Full{满员?}
  Full -->|是| Confirm[成团确认预占]
  Full -->|否超时| Fail[解散]
  Fail --> Refund[自动退+券积分回退]
  Confirm --> Partial[部分退查allocation]
  Partial --> Idem[退款幂等键]
    </pre>
  </div>
  <div class="mermaid-wrap" id="diag-bx1-race">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx1-race">导出 PNG</button></div>
    <pre class="mermaid">
flowchart LR
  A[用户A抢末席] --> CAS[名额原子DECR]
  B[用户B抢末席] --> CAS
  CAS -->|一人成功| OK[成团]
  CAS -->|失败| Comp[失败补偿]
    </pre>
  </div>
""",
        "bx-pay-wms-short": """
  <div class="mermaid-wrap" id="diag-bx2-saga">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx2-saga">导出 PNG</button></div>
    <pre class="mermaid">
flowchart TD
  PayOK --> OB[Outbox] --> OMS --> WMS
  WMS -->|短拣| Saga{补偿策略}
  Saga --> Refund[整单退]
  Saga --> Split[拆单发可得]
  Saga --> Wait[调拨等待]
  UserCancel --> Ver[OMS版本令牌]
  Ver --> Gate{仓态可取消?}
    </pre>
  </div>
  <div class="mermaid-wrap" id="diag-bx2-race">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx2-race">导出 PNG</button></div>
    <pre class="mermaid">
flowchart LR
  Cancel[用户取消] --> V1[带版本]
  Pick[WMS下架] --> St[仓态>=拣货]
  V1 --> Decide{比较}
  St --> Decide
  Decide -->|已下架| AS[转售后拦截]
  Decide -->|未下架| Close[关单释放]
    </pre>
  </div>
""",
        "bx-repair-exchange": """
  <div class="mermaid-wrap" id="diag-bx3-par">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx3-par">导出 PNG</button></div>
    <pre class="mermaid">
flowchart TB
  AS[售后单] --> RMA[退货寄修]
  AS --> Ex[换新预占]
  RMA --> QC[质检]
  QC -->|可修| Fix[维修再发]
  QC -->|换新| Ex
  Ex --> Lock[库存预占TTL]
  Lock --> Ship[发换新]
    </pre>
  </div>
  <div class="mermaid-wrap" id="diag-bx3-lock">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx3-lock">导出 PNG</button></div>
    <pre class="mermaid">
flowchart LR
  ExReq[换新] --> Res[预占]
  Res -->|失败| Queue[排队/驳回]
  Res -->|成功| Hold[持有至发货/释放]
    </pre>
  </div>
""",
        "bx-food-peak": """
  <div class="mermaid-wrap" id="diag-bx4-peak">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx4-peak">导出 PNG</button></div>
    <pre class="mermaid">
flowchart TD
  Order[高峰下单] --> Kitchen[出餐态]
  Cancel[取消尖刺] --> Rule{出餐前/后}
  Rule -->|前| Free[无损取消]
  Rule -->|后| Loss[餐损规则]
  Loss --> HITL[门店确认可选]
    </pre>
  </div>
  <div class="mermaid-wrap" id="diag-bx4-hot">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx4-hot">导出 PNG</button></div>
    <pre class="mermaid">
flowchart LR
  HotShop[爆店] --> Shard[店维度分片/限流]
  Shard --> Queue[出餐队列]
  Queue --> Deg[非核心推送降级]
    </pre>
  </div>
""",
        "bx-cross-border": """
  <div class="mermaid-wrap" id="diag-bx5-clear">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx5-clear">导出 PNG</button></div>
    <pre class="mermaid">
flowchart TD
  Pay --> Declare[报关] --> Customs{放行?}
  Customs -->|否| Fail[清关失败]
  Fail --> Gate[逆向闸门]
  Gate --> Refund[退款/退税规则]
  Gate --> Freight[运费承担]
    </pre>
  </div>
  <div class="mermaid-wrap" id="diag-bx5-storm">
    <div class="diag-actions"><button class="btn" type="button" data-png="diag-bx5-storm">导出 PNG</button></div>
    <pre class="mermaid">
flowchart LR
  Storm[失败风暴] --> Rate[限流工单]
  Rate --> Batch[批量对账]
  Batch --> Notify[用户通知模板]
    </pre>
  </div>
""",
    }
    for sid, frag in boosts.items():
        mark = f"<!-- BX-MMD:{sid} -->"
        if mark in html:
            continue
        m = re.search(rf'(<section[^>]*id="{sid}"[^>]*>.*?</h2>)', html, re.S)
        if not m:
            print("WARN missing", sid)
            continue
        html = html[: m.end()] + f"\n{mark}\n{frag}\n" + html[m.end() :]
        print("BX mermaid+", sid)
    return html


def main() -> None:
    before = INDEX.stat().st_size if INDEX.exists() else 0
    print("BEFORE", before)

    # 1) pillars extreme
    import _inject_pillars_extreme as pe

    pe.main()

    # 2) year depth refresh for BX hub (re-strip and re-add is complex; patch HTML directly)
    html = INDEX.read_text(encoding="utf-8")

    # deepen p0-diag
    html = replace_section_inner(html, "p0-diag-playbook", boost_p0_diag())

    # BX case mermaids
    html = deepen_bx_cases(html)

    # bx-prod hub boost if thin
    if "diag-bx-hub-a" not in html and 'id="bx-prod"' in html:
        html = replace_section_inner(html, "bx-prod", _boost_from_module())

    INDEX.write_text(html, encoding="utf-8")

    # 3) encyclopedia (includes PolarDB CN/DN/GMS)
    import _inject_ency as ie

    ie.main()

    html = INDEX.read_text(encoding="utf-8")
    html = inject_doc_audit(html)
    # re-apply p0/bx marks if ency strip somehow... ency shouldn't touch them
    INDEX.write_text(html, encoding="utf-8")
    shutil.copyfile(INDEX, MIRROR)

    after = INDEX.stat().st_size
    h1 = hashlib.md5(INDEX.read_bytes()).hexdigest()
    h2 = hashlib.md5(MIRROR.read_bytes()).hexdigest()
    assert h1 == h2, "mirror mismatch"

    html2 = INDEX.read_text(encoding="utf-8")
    checks = {
        "ency-fm-polardb-cn": 'id="ency-fm-polardb-cn"' in html2,
        "ency-fm-polardb-dn": 'id="ency-fm-polardb-dn"' in html2,
        "ency-fm-polardb-gms": 'id="ency-fm-polardb-gms"' in html2,
        "ency-fm-polardb-cdc": 'id="ency-fm-polardb-cdc"' in html2,
        "doc-audit": 'id="doc-audit"' in html2,
        "diag-aix-rag": "diag-aix-rag" in html2,
        "diag-bx-hub": "diag-bx-hub" in html2 or "diag-bx1-flow" in html2,
        "CN count in polar": html2[html2.find('id="ency-fm-polardb"'):html2.find('id="ency-fm-polardb"')+50000].count("CN") if 'id="ency-fm-polardb"' in html2 else 0,
    }
    print("AFTER", after, "DELTA", after - before)
    print("MD5", h1)
    for k, v in checks.items():
        print(f"  {k}: {v}")
    print("mermaid total", html2.count('class="mermaid"'))


def _boost_from_module() -> str:
    from anti_water_boost import boost_bx_hub

    return boost_bx_hub()


if __name__ == "__main__":
    main()
