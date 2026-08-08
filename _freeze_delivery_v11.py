#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Honest delivery freeze v1.1 — label depth, stop infinite thicken."""
from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
MIRROR = ROOT.parent / "高级Java外包-系统学习技术白皮书.html"

GOLD = {
    "s-ddd-agg",
    "ency-fm-rocket",
    "ency-fm-polardb",
}

# Leaf sections that are usable skeleton but must NOT claim gold/PASS
SKELETON_PILLARS = [
    ("s-ddd-x-bc", ["业务唯一键落点表可作索引", "缺更多冲突演练剧本与真实慢 SQL 样例", "加载最小图细节以 #s-ddd-agg 为准，本节勿单独背完"]),
    ("s-ddd-x-acl", ["调用链骨架在", "缺多渠道 ACL 对照表深度", "Outbox 与聚合协作细节分散在他节"]),
    ("s-ddd-x-patterns", ["模式↔需求对照表可用", "缺生产代码级策略注册/FSM 全表", "并行寄修细节挂 B-X，勿当已完工"]),
    ("s-ddd-x-arch", ["权衡维度表可用", "缺完整 ADR 范文与团队编制算账", "勿把「先边界后进程」当已落地清单"]),
    ("t-found-jvm", ["GC/容器对齐要点在", "缺完整 GC 日志判读案例集", "DirectMemory/NMT 实战样例不足"]),
    ("t-found-juc", ["池/AQS/库存路径骨架在", "缺完整 jstack 对照集", "跨机互斥边界需结合 MySQL/Redis 节"]),
    ("t-found-mysql", ["幂等/短事务要点在", "缺分库分表迁移全案", "锁等待排查样例不够多"]),
    ("t-found-redis", ["预占/击穿骨架在", "缺 Cluster 槽迁移实战", "大 Key 治理清单未成 Runbook 全集"]),
    ("t-found-kafka", ["分区/ISR/幂等边界在", "缺 Connect/CDC 作业级深度", "EOS 边界勿背成「恰好一次账本」"]),
    ("t-found-rabbit", ["Confirm/Ack/DLX 骨架在", "缺 quorum 运维全案", "高吞吐场景应转 Kafka/Rocket，本节勿吹满"]),
    ("t-found-rocket", ["事务消息/关单要点在", "存储链金标以 #ency-fm-rocket 为准", "本节是入口不是金标正文"]),
    ("t-found-matrix", ["选型矩阵可拍板用", "缺每格 ADR 链接与压测数字", "矩阵≠已完成中间件落地"]),
    ("s-ms-x-boundary", ["写权威表思路在", "缺账号/CI 扫描落地配置", "跨服务禁止 join 的执法工具未写全"]),
    ("s-ms-x-orch", ["Outbox/Inbox 骨架在", "缺半消息/堆积联调剧本全集", "超时矩阵需按你们环境重填"]),
    ("s-ms-x-govern", ["舱壁/金丝雀门禁思路在", "缺全链路压测签字模板全文", "网格重试等平台细节未展开"]),
    ("s-ms-x-observe", ["差账指标思路在", "缺具体 Prometheus 规则全文", "单号串链工具链需自建"]),
    ("s-ms-x-scale", ["中厂裁剪表可用", "缺编制/成本数字", "勿抄大厂全家桶当已裁完"]),
    ("s-ms-x-drills", ["演练题骨架在", "缺可执行故障注入脚本", "证明幂等要用你们库态，勿背答案"]),
    ("t-k8s-x-workload", ["支付舱壁拆分在", "缺完整 YAML/HPA 基线全文", "探针参数需按服务重测"]),
    ("t-k8s-x-release", ["金丝雀门禁思路在", "缺具体 SLO 阈值与 undo 脚本", "变更窗纪律要写进你们日历"]),
    ("t-k8s-x-ops", ["配置/密钥/配额要点在", "缺 Secret 轮换完整 Runbook", "大促冻结清单需本地化"]),
    ("t-k8s-x-mesh", ["要不要 Mesh 决策树在", "缺 mTLS 分期落地步骤", "中厂默认可不上——本节勿当已上 Mesh"]),
    ("t-k8s-x-drills", ["演练项列表在", "缺杀节点/演练记录模板", "探针混用坑需结合你们探针配置"]),
    ("t-ai-x-rag", ["cite/HITL/kbVer 门禁在", "缺完整评测集文件", "勿背成「已可自动退款」"]),
    ("t-ai-x-mcp", ["白名单/禁写思路在", "缺具体 MCP server 注册表", "协议≠已授权"]),
    ("t-ai-x-integrate", ["CI/工单接点在", "缺流水线 YAML", "值班 Agent 必须保持建议态"]),
    ("t-ai-x-agents", ["多角色骨架在", "缺生产编排配置", "金额动作必须 HITL"]),
    ("t-ai-x-forbid", ["禁止清单可用", "缺违规审计样例", "清单≠控制系统已上线"]),
    ("t-ai-x-prod", ["五件套清单在", "缺发布三联票据模板全文", "大促降级开关需自配"]),
    ("bx-group-coupon", ["组合拳主路径在", "缺你们券中心字段映射", "压测数字为示意勿当 KPI"]),
    ("bx-pay-wms-short", ["Saga/补偿思路在", "缺 WMS 状态机对接表", "版本令牌需与仓系统对齐"]),
    ("bx-repair-exchange", ["并行寄修骨架在", "缺质检回执码表", "库存 TTL 参数需压测"]),
    ("bx-food-peak", ["餐损规则思路在", "缺门店态事件契约", "高峰限流键要本地化"]),
    ("bx-cross-border", ["清关失败闸门在", "缺海关/税接口细节", "退税规则按主体重写"]),
    ("s-mgmt-x", ["排期/阶段门可用", "缺完整故事拆卡范文库", "财务门禁要写进你们 DoD"]),
    ("x-promo-trinity", ["三联演练时钟在", "缺完整 T-7 检查表附件", "演练未做=未完成"]),
    ("p0-diag-playbook", ["排障序可用", "缺你们监控面板截图/链接", "先取证再变更——需值班演练固化"]),
    ("p0-capacity", ["容量/告警思路在", "缺 SLO 数字基线", "勿背示意量级当容量结论"]),
    ("p0-mysql", ["MySQL 排障入口在", "深度以 ENCY/Found 为准", "本节勿单独当金标"]),
    ("p0-redis", ["Redis 排障入口在", "深度以 ENCY/Found 为准", "本节勿单独当金标"]),
    ("p0-jvm", ["JVM 排障入口在", "深度以 ENCY/Found 为准", "本节勿单独当金标"]),
    ("ency-fm-kafka", ["日志/ISR/EOS 骨架在", "生产调优与故障全集弱于 Rocket 金标", "勿把 EOS 背成跨系统账本"]),
    ("ency-fm-rabbit", ["路由/Confirm/DLX 骨架在", "仲裁队列运维深度不足", "高吞吐勿硬扛本节"]),
    ("ency-fm-redis", ["结构/过期/锁骨架在", "Cluster 迁移与大 Key Runbook 未满金标", "预占≠账本"]),
    ("ency-fm-mysql", ["MVCC/锁/索引骨架在", "分库迁移与长事务全集弱于金标线", "付后读主要配进你们读写路由"]),
    ("ency-fm-gauss", ["拓扑/迁移门禁骨架在", "方言/隔离用例集未达金标", "未签字拓扑前勿迁核心"]),
    ("ency-fm-dm", ["Oracle 替换路径骨架在", "分页/空串/备份演练细节待补全", "备份不演练=零"]),
    ("ency-fm-tdsql", ["分片/跨片预算骨架在", "热点片与全局索引实战待补", "无键扫生产禁止"]),
    ("ency-fm-jvm", ["内存/GC/容器骨架在", "判读案例集弱于金标", "结合 T-Found-JVM 用"]),
    ("ency-fm-juc", ["JMM/AQS/池骨架在", "订单并发模式样例待补", "结合 T-Found-JUC 用"]),
    ("ency-fm-spring", ["IoC/事务代理骨架在", "多数据源/失效场景全集待补", "自调用坑必须用你们代码验"]),
    ("ency-fm-spark", ["DF/Shuffle/倾斜骨架在", "算子级调优明显弱于 MQ 金标", "对账作业规范需自建"]),
    ("ency-fm-flink", ["CK/水位/反压骨架在", "状态 TTL/EOS 分级待加深", "勿背成端到端恰好一次万能"]),
]

MARK_DS = "<!-- DELIVERY-STATUS-V11 -->"
MARK_SK = "<!-- SKELETON-BANNER:{sid} -->"

DELIVERY_STATUS = f"""
{MARK_DS}
<section class="block" id="delivery-status" data-toc="交付冻结 v1.1 · 怎么读/能信什么" data-prio="p0" data-tags="delivery freeze honest">
  <h2><span class="sys-id">DELIVERY v1.1</span>诚实交付冻结（停止无限加厚）</h2>
  <div class="spine-pos"><div class="label">本节在闭环中的位置</div>
    打开本书先看这里。承认：全书不可能「每一节都金标」。本页把<strong>能信什么 / 骨架可读什么 / 勿背什么</strong>钉死，避免假 PASS。
  </div>
  <div class="plain"><div class="label">人话版</div>
    用户反馈「没法完了」「交付质量/态度有问题」——正确。继续整书无限加厚=永远交不了。
    <b>v1.1 冻结策略：</b>结构与目录保留；只认 3 块金标；其余标明骨架或勿背；禁止再开「整书去水循环」。
  </div>

  <div class="callout danger"><div class="label">态度与纪律</div>
    <ul>
      <li>不把「有目录 / 有批处理加厚」说成「全书 HARD GATE PASS」。</li>
      <li>金标只有下面三块；其它节即使字多，默认最多算「骨架可用」。</li>
      <li>下一步深化由你按优先级点名（最多 5 项），不再自动扩 scope。</li>
    </ul>
  </div>

  <h3>① 金标完成（可以认真学、可以对外讲）</h3>
  <table>
    <thead><tr><th>锚点</th><th>为何算金标</th><th>怎么用</th></tr></thead>
    <tbody>
      <tr>
        <td><a href="#s-ddd-agg"><code>#s-ddd-agg</code></a></td>
        <td>聚合根唯一性多层（业务键/DB/并发/号段）+ 加载慢因与最小图 + 冲突/好坏加载图 + 跨行业案 + 详答</td>
        <td>面试/进组讲「双单怎么防、加载为何慢」从这里进</td>
      </tr>
      <tr>
        <td><a href="#ency-fm-rocket"><code>#ency-fm-rocket</code></a></td>
        <td>CommitLog/ConsumeQueue/刷盘/复制/顺序/DLQ/事务存储链齐；金融 vs 电商 vs 物流</td>
        <td>消息底座金标；T-Found-Rocket 只作入口</td>
      </tr>
      <tr>
        <td><a href="#ency-fm-polardb"><code>#ency-fm-polardb</code></a>
          （<a href="#ency-fm-polardb-cn">CN</a>·<a href="#ency-fm-polardb-dn">DN</a>·<a href="#ency-fm-polardb-gms">GMS</a>·<a href="#ency-fm-polardb-cdc">CDC</a>）</td>
        <td>共享存储 vs PolarDB-X 控制面/数据面拆清；付后读主/CDC 边界</td>
        <td>分布式库选型与排障从这里进</td>
      </tr>
    </tbody>
  </table>

  <h3>② 骨架可用（可浏览、可当索引；勿宣称完工）</h3>
  <p>正逆向主线 B0/B-F/B-R、B-X 五案、S-MS-X / T-K8s-X / T-AI-X / T-Found 其它子章、多数 <code>#ency-fm-*</code>：结构在、能导航、有部分底板与案例，但<strong>深度不及上表三金标</strong>。节内若见「骨架·待深化」红/黄标，以该标缺项为准。</p>
  <ul>
    <li>用法：跟主线读 → 卡点再点名深化；不要整本顺序硬背。</li>
    <li>ENCY 里除 Rocket / PolarDB 外，门禁列已降为「骨架可用」，不再假 PASS。</li>
  </ul>

  <h3>③ 未达标 · 勿背（单独拿出去会误导）</h3>
  <ul>
    <li>P1/P2 速查、glossary、cheatsheet：只有跳转价值，不是深度正文。</li>
    <li>任何仍写「HARD GATE PASS」却不在上表三金标内的说法：以本页为准作废。</li>
    <li>案例里的「工程目标/示意」量级：禁止当成某厂未公开 KPI。</li>
    <li>Spark/Flink 等大数据条目：明显弱于 MQ 金标，面试主攻实时数仓勿只靠本节。</li>
  </ul>

  <h3>④ 若继续深化（最多 5 项 · 你来选）</h3>
  <ol>
    <li><code>#ency-fm-kafka</code> 或 <code>#ency-fm-mysql</code> 提到接近 Rocket 金标</li>
    <li><code>#s-ms-x-orch</code> Outbox/Inbox 生产联调剧本补全</li>
    <li><code>#t-k8s-x-release</code> 金丝雀 SLO/undo 可执行附件</li>
    <li><code>#t-ai-x-rag</code> 评测集文件 + 陷阱题包</li>
    <li>某一个 B-X 案（你指定）补真实字段映射与压测表</li>
  </ol>
  <p><b>冻结声明：</b>未点名之前，不启动「整书再去水」循环。审计页 <a href="#doc-audit">#doc-audit</a> / <a href="#ency-audit">#ency-audit</a> 已按 v1.1 对齐。</p>
  <div class="koujue"><div class="label">口诀</div>先信三金标，骨架当地图，速查勿当饭，深化你点名。</div>
</section>
<!-- /DELIVERY-STATUS-V11 -->
"""


def skeleton_banner(sid: str, gaps: list[str]) -> str:
    lis = "".join(f"<li>{g}</li>" for g in gaps[:3])
    return f"""{MARK_SK.format(sid=sid)}
  <div class="callout danger"><div class="label">骨架·待深化（v1.1 冻结 · 非金标）</div>
    <p>本节<strong>可以当索引/提纲</strong>，但<strong>不要当作已金标完工</strong>。金标仅见 <a href="#delivery-status">#delivery-status</a> 三块。</p>
    <p><b>缺什么（诚实）：</b></p>
    <ul>{lis}</ul>
  </div>
<!-- /SKELETON-BANNER:{sid} -->
"""


def inject_delivery_status(html: str) -> str:
    if MARK_DS in html:
        html = re.sub(
            rf"{re.escape(MARK_DS)}.*?<!-- /DELIVERY-STATUS-V11 -->\n?",
            "",
            html,
            count=1,
            flags=re.S,
        )
    # after hero header
    m = re.search(r"</header>\s*", html)
    if not m:
        raise SystemExit("hero </header> not found")
    return html[: m.end()] + DELIVERY_STATUS + html[m.end() :]


def rewrite_ency_audit(html: str) -> str:
    """Replace fake all-PASS table with honest freeze statuses."""
    new_table = """
  <table>
    <thead><tr><th>技术</th><th>专章</th><th>关键细锚点（证据）</th><th>v1.1 门禁（诚实）</th></tr></thead>
    <tbody>
      <tr><td>RocketMQ</td><td><a href="#ency-fm-rocket">#ency-fm-rocket</a></td><td><a href="#ency-fm-rocket-storage">storage</a> · flush · ha · order · dlq · tx</td><td><b>金标完成</b></td></tr>
      <tr><td>PolarDB / PolarDB-X</td><td><a href="#ency-fm-polardb">#ency-fm-polardb</a></td><td><a href="#ency-fm-polardb-cn">CN</a> · <a href="#ency-fm-polardb-dn">DN</a> · <a href="#ency-fm-polardb-gms">GMS</a> · <a href="#ency-fm-polardb-cdc">CDC</a></td><td><b>金标完成</b></td></tr>
      <tr><td>Kafka</td><td><a href="#ency-fm-kafka">#ency-fm-kafka</a></td><td>log · isr · eos · cg</td><td>骨架可用 · 待深化</td></tr>
      <tr><td>RabbitMQ</td><td><a href="#ency-fm-rabbit">#ency-fm-rabbit</a></td><td>ex · ha · ttl · dlx</td><td>骨架可用 · 待深化</td></tr>
      <tr><td>Redis</td><td><a href="#ency-fm-redis">#ency-fm-redis</a></td><td>ds · expire · lock · ops</td><td>骨架可用 · 待深化</td></tr>
      <tr><td>MySQL</td><td><a href="#ency-fm-mysql">#ency-fm-mysql</a></td><td>tx · lock · idx · repl</td><td>骨架可用 · 待深化</td></tr>
      <tr><td>GaussDB</td><td><a href="#ency-fm-gauss">#ency-fm-gauss</a></td><td>topo · mig · ops</td><td>骨架可用 · 待深化</td></tr>
      <tr><td>达梦</td><td><a href="#ency-fm-dm">#ency-fm-dm</a></td><td>ora · ha · bak</td><td>骨架可用 · 待深化</td></tr>
      <tr><td>TDSQL</td><td><a href="#ency-fm-tdsql">#ency-fm-tdsql</a></td><td>arch · shard · xa</td><td>骨架可用 · 待深化</td></tr>
      <tr><td>JVM / JUC / Spring</td><td>对应 #ency-fm-*</td><td>见专章细锚</td><td>骨架可用 · 待深化</td></tr>
      <tr><td>Spark / Flink</td><td>对应 #ency-fm-*</td><td>见专章细锚</td><td><b>未达标勿背作金标</b>（弱于 MQ）</td></tr>
    </tbody>
  </table>
  <div class="callout danger"><div class="label">v1.1 冻结 · 取消假 PASS</div>
    旧表「14 项全 PASS」作废。全书只有 RocketMQ + PolarDB-X（CN/DN/GMS/CDC）+ 正文章 <a href="#s-ddd-agg">#s-ddd-agg</a> 认金标。
    其余 FULLMAP 专章保留结构供导航，标「骨架可用」。详见 <a href="#delivery-status">#delivery-status</a>。
  </div>
"""
    # replace tbody table inside ency-audit section
    m = re.search(
        r'(<section class="block" id="ency-audit".*?)(<table>.*?</table>)(\s*<div class="callout"><div class="label">诚实说明</div>.*?</div>)',
        html,
        re.S,
    )
    if not m:
        # fallback: replace PASS rows coarsely
        html = html.replace(
            "<td>PASS（金标）</td>",
            "<td><b>金标完成</b></td>",
        )
        html = re.sub(
            r'(#ency-fm-kafka.*?</td><td>)PASS(</td>)',
            r'\1骨架可用 · 待深化\2',
            html,
            count=1,
            flags=re.S,
        )
        # blunt: all remaining PASS in ency-audit → 骨架
        def repl_audit_section(sec: str) -> str:
            sec = sec.replace("<td>PASS</td>", "<td>骨架可用 · 待深化</td>")
            sec = sec.replace("<td>PASS（金标）</td>", "<td><b>金标完成</b></td>")
            return sec

        html = re.sub(
            r'(<section class="block" id="ency-audit".*?</section>)',
            lambda m: repl_audit_section(m.group(1)),
            html,
            count=1,
            flags=re.S,
        )
        return html

    old_honest = m.group(3)
    new_honest = """
  <div class="callout"><div class="label">诚实说明（v1.1）</div>
    公司案例矩阵 <a href="#ency-case">#ency-case</a> 为横切套路库。停止「整书再开一轮加深」循环；深化由用户点名（见 <a href="#delivery-status">#delivery-status</a>）。
  </div>
"""
    return html[: m.start(2)] + new_table + new_honest + html[m.end(3) :]


def downgrade_hard_gate_labels(html: str) -> str:
    """For ENCY sections that are not gold, rename HARD GATE banner."""
    # Keep rocket & polardb HARD GATE as 金标门禁
    def per_section(m: re.Match) -> str:
        sid, attrs, body = m.group(1), m.group(2), m.group(3)
        if sid in ("ency-fm-rocket", "ency-fm-polardb"):
            body = body.replace(
                "HARD GATE（不合格重写）",
                "金标门禁（v1.1 已达标 · 保持）",
            )
        elif sid.startswith("ency-fm-"):
            body = body.replace(
                "HARD GATE（不合格重写）",
                "骨架·待深化（非金标 · v1.1）",
            )
            body = body.replace(
                "禁止空泛概述凑字。",
                "结构保留供导航；深度未达 Rocket/Polar 金标，勿背作 PASS。详见 #delivery-status。",
            )
        return f'<section class="block" id="{sid}"{attrs}>{body}</section>'

    return re.sub(
        r'<section class="block" id="([^"]+)"([^>]*)>(.*?)</section>',
        per_section,
        html,
        flags=re.S,
    )


def add_skeleton_banners(html: str) -> str:
    for sid, gaps in SKELETON_PILLARS:
        mark = MARK_SK.format(sid=sid)
        if mark in html:
            html = re.sub(
                rf"{re.escape(mark)}.*?<!-- /SKELETON-BANNER:{sid} -->\n?",
                "",
                html,
                count=1,
                flags=re.S,
            )
        if f'id="{sid}"' not in html:
            continue
        # skip if somehow gold
        if sid in GOLD:
            continue
        banner = skeleton_banner(sid, gaps)
        m = re.search(rf'(<section[^>]*id="{re.escape(sid)}"[^>]*>.*?</h2>)', html, re.S)
        if not m:
            continue
        html = html[: m.end()] + "\n" + banner + html[m.end() :]
    return html


def patch_hero(html: str) -> str:
    html = html.replace(
        '<span class="chip"><b>底板</b> 源码级原理</span>',
        '<span class="chip"><b>冻结</b> <a href="#delivery-status" style="color:inherit">v1.1 诚实交付</a></span>',
        1,
    )
    # soften lead claim
    if "v1.1 诚实交付冻结" not in html.split("id=\"hero\"", 1)[-1][:800]:
        html = html.replace(
            '<div class="hero-meta">',
            '<p class="hero-lead" style="margin-top:-.5rem"><b>阅读前先看</b> <a href="#delivery-status">#delivery-status</a>：金标只有 3 块，其它多为骨架。</p>\n  <div class="hero-meta">',
            1,
        )
    return html


def patch_doc_audit(html: str) -> str:
    freeze_note = """
  <div class="callout danger"><div class="label">v1.1 交付冻结（取代「整书去水循环」）</div>
    <p>停止无限加厚。诚实状态页：<a href="#delivery-status">#delivery-status</a>。</p>
    <ul>
      <li><b>金标：</b><code>#s-ddd-agg</code> · <code>#ency-fm-rocket</code> · <code>#ency-fm-polardb</code>（CN/DN/GMS/CDC）</li>
      <li><b>其余：</b>骨架可用或勿背；ENCY 假「全 PASS」已撤销</li>
      <li><b>深化：</b>仅当用户点名（最多 5 项），不再自动扩全书</li>
    </ul>
  </div>
"""
    if "v1.1 交付冻结" in html and "id=\"doc-audit\"" in html:
        # replace existing freeze note if re-run
        html = re.sub(
            r'<div class="callout danger"><div class="label">v1\.1 交付冻结.*?</div>\s*',
            freeze_note,
            html,
            count=1,
            flags=re.S,
        )
        return html
    m = re.search(r'(<section class="block" id="doc-audit"[^>]*>.*?</h2>)', html, re.S)
    if m:
        html = html[: m.end()] + "\n" + freeze_note + html[m.end() :]
    return html


def patch_ency_fm_hub_koujue(html: str) -> str:
    html = html.replace(
        "门禁口诀：无源码不进门，无案例不进门，无全链路不进门，无锚点证据不算PASS。",
        "v1.1 口诀：Rocket 与 PolarDB 认金标；其它 FULLMAP 先当骨架地图；假全PASS已撤销。见 #delivery-status。",
    )
    html = html.replace(
        "审计口诀：点得开锚点，数得清案例，找得到源码路径，才叫PASS。",
        "审计口诀：金标看 #delivery-status 三块；点得开不等于全 PASS。",
    )
    return html


def ensure_gold_ok(html: str) -> None:
    need = [
        'id="s-ddd-agg"',
        'id="s-ddd-agg-uniq"',
        'id="s-ddd-agg-load"',
        'id="ency-fm-rocket"',
        'id="ency-fm-rocket-storage"',
        'id="ency-fm-polardb"',
        'id="ency-fm-polardb-cn"',
        'id="ency-fm-polardb-dn"',
        'id="ency-fm-polardb-gms"',
        'id="ency-fm-polardb-cdc"',
        'id="delivery-status"',
    ]
    missing = [n for n in need if n not in html]
    if missing:
        raise SystemExit(f"gold/freeze anchors missing: {missing}")


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    html = inject_delivery_status(html)
    html = patch_hero(html)
    html = rewrite_ency_audit(html)
    html = downgrade_hard_gate_labels(html)
    html = add_skeleton_banners(html)
    html = patch_doc_audit(html)
    html = patch_ency_fm_hub_koujue(html)
    ensure_gold_ok(html)

    INDEX.write_text(html, encoding="utf-8")
    shutil.copyfile(INDEX, MIRROR)
    h1 = hashlib.md5(INDEX.read_bytes()).hexdigest()
    h2 = hashlib.md5(MIRROR.read_bytes()).hexdigest()
    assert h1 == h2

    # README one-liner
    readme = ROOT / "README.md"
    if readme.exists():
        t = readme.read_text(encoding="utf-8")
        line = "| **交付冻结 v1.1** | `#delivery-status` | https://junjiewq.github.io/java-senior-playbook/#delivery-status |\n"
        if "#delivery-status" not in t:
            t = t.replace(
                "| **全书去水审计** | `#doc-audit` |",
                line + "| **全书去水审计** | `#doc-audit` |",
                1,
            )
            readme.write_text(t, encoding="utf-8")

    print("FREEZE_OK", INDEX.stat().st_size, h1)
    print("delivery-status", html.count('id="delivery-status"'))
    print("skeleton banners", html.count("骨架·待深化"))
    print("fake PASS in ency-audit rows:", len(re.findall(r"<td>PASS</td>", html[html.find("ency-audit"):html.find("ency-audit")+8000] if "ency-audit" in html else "")))


if __name__ == "__main__":
    main()
