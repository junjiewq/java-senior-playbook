#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pretty UTF-8 TXT export from playbook index.html (local only)."""
from __future__ import annotations

import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT / "index.html"
OUT_PATH = ROOT / "高级Java外包-系统学习技术白皮书.txt"
W = 72  # target display width (CJK-aware wrap)


def dw(s: str) -> int:
    n = 0
    for ch in s:
        o = ord(ch)
        n += 2 if (o >= 0x1100 and (
            o <= 0x115F or 0x2E80 <= o <= 0xA4CF or 0xAC00 <= o <= 0xD7A3
            or 0xF900 <= o <= 0xFAFF or 0xFE10 <= o <= 0xFE6F
            or 0xFF00 <= o <= 0xFF60 or 0xFFE0 <= o <= 0xFFE6
            or 0x20000 <= o <= 0x3FFFD
        )) or (0x4E00 <= o <= 0x9FFF) or (0x3000 <= o <= 0x303F) else 1
    return n


def pad(s: str, width: int) -> str:
    return s + " " * max(0, width - dw(s))


def wrap(text: str, width: int = W, indent: str = "") -> list[str]:
    text = re.sub(r"[ \t]+", " ", text.strip())
    if not text:
        return []
    lines, cur = [], indent
    for ch in text:
        trial = cur + ch
        if dw(trial) > width and cur.strip():
            lines.append(cur.rstrip())
            cur = indent + ch.lstrip() if ch != " " else indent
        else:
            cur = trial
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def box(title: str, body_lines: list[str], width: int = W) -> list[str]:
    inner = width - 2
    title = title.strip()
    head = f"┌─ {title} " + "─" * max(1, inner - dw(title) - 3) + "┐"
    out = [head]
    for ln in body_lines:
        chunks = wrap(ln, inner - 2, "") if dw(ln) > inner - 2 else [ln]
        for c in chunks:
            out.append("│ " + pad(c, inner - 2) + " │")
    out.append("└" + "─" * inner + "┘")
    return out


def banner_h1(title: str) -> list[str]:
    bar = "═" * W
    t = title.strip()
    return ["", bar, pad(f"  {t}", W), bar, ""]


def banner_h2(title: str) -> list[str]:
    bar = "─" * W
    return ["", bar, f"「{title.strip()}」", bar, ""]


def banner_h3(title: str) -> list[str]:
    return ["", f"▸ {title.strip()}", "·" * min(W, max(24, dw(title) + 4)), ""]


FLOWCHARTS = {
    "method": """\
【文字流程图】钉拆标选验五步法
图例：▶ 前进  │ 分层  ◆ 决策

  ┌────────┐   ┌────────┐   ┌────────┐
  │ ① 钉   │──▶│ ② 拆   │──▶│ ③ 标   │
  │ 钉问题  │   │ 拆本质  │   │ 标验收  │
  └────────┘   └────────┘   └────┬───┘
                                 ▼
  ┌────────┐   ┌────────┐   ┌────────┐
  │ ⑤ 验   │◀──│ ④ 选   │◀──│ 口径齐 │
  │ 验结果  │   │ 选方案  │   │ 再选型 │
  └────────┘   └────────┘   └────────┘
""",
    "c4": """\
【文字流程图】四段闭环（业务↔技术）
图例：闭环四段，缺一不可

        ┌──────────────────┐
        │ ① 业务本质       │
        │ 怕什么/验收口径   │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ ② 技术实现       │
        │ 怎么干/关键路径  │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ ③ 技术原理       │
        │ 为何稳/底板机制   │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ ④ 业务实质       │
        │ 账过了没/可回滚   │
        └────────┬─────────┘
                 │
                 └──▶ 回①（周复盘）
""",
    "rocket": """\
【文字流程图】RocketMQ 存储/消费链路（金标）
图例：写路径 ▼  读路径 ▶  DLQ ◆

  Producer
     │ send
     ▼
  ┌──────────────┐
  │  Broker      │
  │  CommitLog   │◀── 顺序写盘 / 刷盘 / 复制
  └──────┬───────┘
         │ 建索引
         ▼
  ┌──────────────┐     ┌──────────────┐
  │ ConsumeQueue │────▶│  Consumer    │
  │ (逻辑队列)    │     │  pull/push   │
  └──────────────┘     └──────┬───────┘
                              │ 失败超限
                              ▼
                         ◆ DLQ / 重试主题
""",
    "polardb": """\
【文字流程图】PolarDB-X · CN→DN / CDC
图例：SQL入口 → 分片执行 → 变更外送

  App / JDBC
       │
       ▼
  ┌─────────┐   路由/计划    ┌─────────┐
  │   CN    │──────────────▶│   DN    │
  │ 计算层  │               │ 存储分片 │
  └────┬────┘               └────┬────┘
       │ meta                    │ binlog/redo
       ▼                         ▼
  ┌─────────┐               ┌─────────┐
  │   GMS   │               │   CDC   │──▶ 下游订阅
  │ 元数据  │               │ 变更流  │
  └─────────┘               └─────────┘
""",
    "ddd": """\
【文字流程图】DDD 聚合加载（命令最小图）
图例：好路径 ▶  坏路径 ✗

  命令进入（支付标已付）
       │
       ▼
  ┌────────────────────┐
  │ 按业务键定位聚合根  │
  │ orderNo+token 唯一  │
  └─────────┬──────────┘
            ▼
     ◆ 加载策略？
      /            \\
  ▶ 最小图         ✗ 大图 fetch join
  根+必需边          售后/轨迹一并加载
      │                 │
      ▼                 ▼
  短事务条件更新     事务拖长 / 锁扩散
  version++          P99 崩 / 双单风险
""",
    "aftersale": """\
【文字流程图】拼团/售后并行冲突收敛
图例：并行分支须汇合到唯一售后单

  用户连点申请
       │
       ▼
  ┌──────────────┐
  │ 幂等键/唯一  │──命中──▶ 返回已有单
  └──────┬───────┘
         │ 未命中
         ▼
  ┌──────────────┐
  │ 创建售后聚合    │
  └──────┬───────┘
         ├──────────────┐
         ▼              ▼
    寄修分支        换新预占分支
         │              │
         └──────┬───────┘
                ▼
         质检/回执驱动
                ▼
         退款·分摊·对账
""",
    "agentscope_arch": """\
【文字流程图】AgentScope Studio 生产拓扑
图例：主路径 ▶  旁路虚线 ···

  Studio 三栏 UI
       │ WS /ws/agent
       ▼
  AgentWebSocketHandler ──▶ AgentChatService
       │                         │
       │              enrichWithMemory
       │                         ▼
       │              MemoryRagRouter / PersonalMemoryStore
       │                         │
       │                         ▼
       │                   ReActAgent
       │                    │         │
       │                    ▼         ▼
       │              SwappableModel  Toolkit
       │              (DeepSeek)       │
       │                               ├─ WorkspaceFileTools / SafeCompile
       │                               ├─ PersonalMemoryTools
       │                               └─ WebSearch / ImageTools
       │                    │
       │                    ▼
       │           JsonFileAgentStateStore (.agent-state)
       │
  Edge TTS / ASR ···（不经 ReAct Model）···▶ UI
""",
    "agentscope_react": """\
【文字流程图】ReActAgent 循环（CallExecution）
图例：▶ 前进  ◆ 决策

  [*] seedSystemMsg / RuntimeContext
       │
       ▼
  executeIteration(iter) ──▶ reasoning
       │
       ◆ iter >= maxIters ?
      / \\
  是 /   \\ 否
    ▼     ▼
 summariz  model.stream(+ tools schema)
    │         │
    │    ◆ InterruptControl ?
    │     / \\
    │  取消   继续
    │   ▼      │
    │  [*]  ◆ 含 ToolUseBlock ?
    │        / \\
    │     有 /   \\ 无且结束
    │       ▼     ▼
    │    acting   Done
    │       │
    │  PermissionEngine
    │    / deny     \\ allow
    │   ▼            ▼
    │ 观察拒绝   toolkit.callTools
    │   \\            /
    │    observation 入 context / iter+1
    │              │
    └──────────────┘ → reasoning
  Done → saveStateToSession → [*]
""",
    "agentscope_seq": """\
【文字流程图】请求时序 User ↔ WS ↔ Agent ↔ LLM ↔ Tools
图例：→ 请求  ← 推送  ∥ 循环

  用户 UI
    → AgentWebSocketHandler : chat JSON
    → AgentChatService.streamChat
    → MemoryRagRouter.enrichWithMemory
    → ReActAgent.streamEvents
    ∥ ReAct iter < maxIters
       → OpenAIChatModel.stream
       ← Text / Thinking / ToolCall*Event
       ← WS JSON（token / thinking / tool_start）
       opt tool_call
         → Toolkit.@Tool
         ← ToolResult / tool_end / file_change
    ← AgentResultEvent / message final
  用户 cancel → Disposable.dispose
  （框架另有 agent.interrupt → InterruptControl）
""",
    "agentscope_layers": """\
【文字流程图】Skills / MCP / RAG / AgentScope 分层
图例：上→下装配；红线在 Tool/Permission

  ┌─────────────────────────────┐
  │ RAG：条款/基线/慢SQL指纹/复盘│
  └──────────────┬──────────────┘
                 ▼
  ┌─────────────────────────────┐
  │ Skills：怎么干（SKILL.md）   │
  └──────────────┬──────────────┘
                 ▼
  ┌─────────────────────────────┐
  │ MCP / Toolkit：只读手/白名单 │
  └──────────────┬──────────────┘
                 ▼
  ┌─────────────────────────────┐
  │ AgentScope ReActAgent 循环   │
  └─────────────────────────────┘
""",
    "sql_agents": """\
【文字流程图】SQL 巡检智能体（Skills+MCP+RAG）
图例：CI/周批两条入口

  Git PR diff / 慢日志 TopN
           │
           ▼
     AgentScope ReAct
        │    │    │
        ▼    ▼    ▼
     Skills  MCP  RAG
   (审核/巡检)(只读)(条款ID)
        │
        ▼
  结构化报告 + 变更单草稿
        │
        ▼
   CI 门禁 / 治理看板
""",
    "polar_shared": """\
【文字流程图】PolarDB 共享存储（再钉一次）
图例：计算与存储分离

  App / JDBC
       │
       ▼
  ┌─────────┐     ┌──────────────┐
  │ Primary │────▶│ 共享存储     │
  │  RW     │     │ (分布式文件系统)│
  └────┬────┘     └──────▲───────┘
       │ 复制日志         │
       ▼                  │
  ┌─────────┐             │
  │   RO    │─────────────┘
  │  只读   │  本地缓存页
  └─────────┘
  付后强一致读 → 走 RW / 会话粘滞；RO 有复制延迟
""",
    "xxl_job": """\
【文字流程图】XXL-JOB 调度→执行→回调
图例：Admin 只调度 · Executor 跑业务

  Cron/时间轮
       │
       ▼
  ┌──────────────┐
  │  XXL-Admin   │──路由/写日志──▶ HTTP 派发
  └──────────────┘
                       │
                       ▼
  ┌──────────────┐   ┌──────────────┐
  │  Executor    │──▶│ @XxlJob 业务 │──▶ Polar/对账
  └──────┬───────┘   └──────────────┘
         │ callback
         ▼
     xxl_job_log（失败超限→告警工单；幂等 runId）
""",
    "kafka_appx": """\
【文字流程图】Kafka 生产加厚：Outbox→ISR→消费→DLQ
图例：权威在库 · EOS 不跨系统

  业务写 Polar + Outbox
           │
           ▼
     KafkaProducer（业务 key）
           │ acks=all / ISR
           ▼
     Leader Partition + Followers
           │ fetch ≤ HW
           ▼
     Consumer Group → 幂等表 → 状态机
           │ 失败超限
           ▼
        DLQ / XXL 补数
""",
}


CASE_MARKERS = [
    ("完整业务场景", "1/5 完整业务场景"),
    ("技术落地配置", "2/5 技术落地配置"),
    ("线上真实故障", "3/5 线上真实故障"),
    ("分步优化方案", "4/5 分步优化方案"),
    ("落地效果数据", "5/5 落地效果数据"),
]


def strip_chrome(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<style\b[^>]*>.*?</style>", "", html, flags=re.S | re.I)
    html = re.sub(r'<div class="diag-actions"[^>]*>.*?</div>', "", html, flags=re.S)
    html = re.sub(r'<div class="reflect-tools"[^>]*>.*?</div>', "", html, flags=re.S)
    html = re.sub(r'<div class="reflect-foot"[^>]*>.*?</div>', "", html, flags=re.S)
    return html


class PrettyExport(HTMLParser):
    SKIP = {"script", "style", "svg", "button", "noscript"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.toc: list[tuple[str, str]] = []
        self.skip = 0
        self.in_pre = 0
        self.in_code_fence = False
        self.li_depth = 0
        self.table_rows: list[list[str]] = []
        self.cur_row: list[str] | None = None
        self.cur_cell: list[str] | None = None
        self.in_table = 0
        self.capture_text = True
        self.section_id = ""
        self.pending_label = ""
        self.class_stack: list[str] = []
        self.mermaid_buf: list[str] = []
        self.in_mermaid = 0
        self.reflect_skip_empty = True
        self._injected: set[str] = set()
        self._sys_id_open = False

    def _cls(self) -> str:
        return self.class_stack[-1] if self.class_stack else ""

    def _emit(self, s: str):
        self.parts.append(s)

    def _emit_lines(self, lines: list[str]):
        for ln in lines:
            self.parts.append(ln + "\n")

    def _maybe_inject_flow(self, sec_id: str, toc: str, htext: str):
        key = None
        blob = f"{sec_id} {toc} {htext}".lower()
        if "s-method" in blob or "钉拆标选验" in blob or sec_id == "s-method":
            key = "method"
        elif sec_id in ("s-c4",) or "四段闭环" in blob or "c4" in sec_id:
            key = "c4"
        elif "rocket" in blob or "ency-fm-rocket" in sec_id:
            key = "rocket"
        elif "appx-polar" in sec_id or "polardb 原理" in blob:
            key = "polar_shared"
        elif "polardb" in blob or "ency-fm-polardb" in sec_id:
            key = "polardb"
        elif "ddd-agg" in sec_id or ("聚合" in htext and "加载" in htext):
            key = "ddd"
        elif "拼团" in blob or ("售后" in htext and ("bx" in sec_id or "case" in sec_id)):
            key = "aftersale"
        elif sec_id.startswith("b-x") or "拼团券退" in blob:
            key = "aftersale"
        elif "appx-agentscope" in sec_id or "agentscope 源码" in blob:
            key = "agentscope_arch"
        elif "appx-as-loop" in sec_id or ("reactagent" in blob and "循环" in htext):
            key = "agentscope_react"
        elif "appx-as-seq" in sec_id or ("请求时序" in htext and "ws" in blob):
            key = "agentscope_seq"
        elif "appx-as-skill" in sec_id or ("skills" in blob and "mcp" in blob and "分层" in htext):
            key = "agentscope_layers"
        elif "appx-sql-agents" in sec_id or "sql 方向智能体" in blob:
            key = "sql_agents"
        elif "appx-xxl" in sec_id or "xxl-job" in blob or ("xxl" in blob and "深挖" in blob):
            key = "xxl_job"
        elif "appx-kafka" in sec_id or ("kafka" in blob and ("源码" in blob or "加厚" in blob)):
            key = "kafka_appx"
        if key and key not in self._injected:
            self._injected.add(key)
            self._emit("\n")
            for ln in FLOWCHARTS[key].strip("\n").splitlines():
                self._emit(ln + "\n")
            self._emit("\n")

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        ad = dict(attrs)
        cls = ad.get("class", "")
        self.class_stack.append(cls)
        if tag in self.SKIP or "diag-actions" in cls or "reflect-tools" in cls:
            self.skip += 1
            return
        if self.skip:
            return

        if tag == "section" and "block" in cls.split():
            self.section_id = ad.get("id", "")
            toc = ad.get("data-toc", "")
            if toc:
                self.toc.append((self.section_id, toc))

        if "mermaid" in cls.split():
            self.in_mermaid += 1
            self.mermaid_buf = []
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.cur_cell = []  # reuse as heading buffer
            self.pending_label = f"__h__{tag}"
            return

        # sys-id badges sit inside headings — keep a space after them
        if tag == "span" and "sys-id" in cls.split() and self.pending_label.startswith("__h__"):
            if self.cur_cell is not None:
                self.cur_cell.append("")  # marker; space added on endtag
            self._sys_id_open = True
            return

        if tag == "table":
            self.in_table += 1
            self.table_rows = []
            return
        if self.in_table and tag == "tr":
            self.cur_row = []
            return
        if self.in_table and tag in {"td", "th"}:
            self.cur_cell = []
            return

        if tag == "pre" and "mermaid" not in cls:
            self.in_pre += 1
            self._emit("\n```\n")
            return
        if tag == "br":
            self._emit("\n")
            return
        if tag == "hr":
            self._emit("\n" + ("─" * W) + "\n")
            return
        if tag == "li":
            self.li_depth += 1
            self._emit("\n  • ")
            return
        if tag == "p":
            self._emit("\n")
            return

        if "company-prd" in cls.split():
            self._emit("\n")
            self._emit_lines(banner_h3("【案例 CASE】五段硬门槛"))
            return
        if "callout" in cls.split():
            danger = "danger" in cls.split()
            self.pending_label = "callout-danger" if danger else "callout"
            self.cur_cell = []
            return
        if "koujue" in cls.split():
            self.pending_label = "koujue"
            self.cur_cell = []
            return
        if "reflect" in cls.split():
            self.pending_label = "reflect"
            self.cur_cell = []
            return
        if "label" in cls.split() and self.pending_label in {
            "callout", "callout-danger", "koujue", "reflect"
        }:
            return

    def handle_endtag(self, tag):
        tag = tag.lower()
        cls = self.class_stack.pop() if self.class_stack else ""
        if tag in self.SKIP:
            if self.skip:
                self.skip -= 1
            return
        if self.skip:
            return

        if self.in_mermaid and tag in {"pre", "div"}:
            # close mermaid on pre end preferably
            if tag == "pre" or (tag == "div" and "mermaid" in cls):
                src = "".join(self.mermaid_buf).strip()
                self.in_mermaid = max(0, self.in_mermaid - 1)
                self.mermaid_buf = []
                ascii_flow = self._mermaid_to_ascii(src)
                self._emit("\n【文字流程图】（由 mermaid 转写）\n")
                self._emit("图例：节点顺序按源图箭头近似展开\n")
                for ln in ascii_flow.splitlines():
                    self._emit(ln + "\n")
                self._emit("\n")
                return

        if tag == "span" and "sys-id" in cls.split() and getattr(self, "_sys_id_open", False):
            self._sys_id_open = False
            if self.cur_cell is not None:
                self.cur_cell.append(" ")
            return

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self.pending_label.startswith("__h__"):
            text = "".join(self.cur_cell or []).strip()
            text = re.sub(r"\s+", " ", text)
            self.cur_cell = None
            level = self.pending_label[-2:]
            self.pending_label = ""
            if level == "h1":
                self._emit_lines(banner_h1(text))
            elif level == "h2":
                self._emit_lines(banner_h2(text))
                self._maybe_inject_flow(self.section_id, "", text)
            else:
                self._emit_lines(banner_h3(text))
                # also match h3/h4 anchors via id-less text
                self._maybe_inject_flow(self.section_id, "", text)
                # h3/h4 may carry their own ids in HTML but section_id is parent block
                # inject by heading text for AgentScope subsections
                low = text.lower()
                if "agent 循环" in low or "message → model" in low:
                    self._maybe_inject_flow("appx-as-loop", "", text)
                elif "请求时序" in text:
                    self._maybe_inject_flow("appx-as-seq", "", text)
                elif "skills" in low and "mcp" in low and ("分层" in text or "rag" in low):
                    self._maybe_inject_flow("appx-as-skill-mcp", "", text)
                elif "sql 方向智能体" in low or "sql方向智能体" in low.replace(" ", ""):
                    self._maybe_inject_flow("appx-sql-agents", "", text)
                elif "polardb 原理与规范" in low:
                    self._maybe_inject_flow("appx-polar-deep", "", text)
                elif "xxl-job" in low or ("xxl" in low and "深挖" in text):
                    self._maybe_inject_flow("appx-xxl", "", text)
                elif "kafka" in low and ("源码" in text or "加厚" in text or "用法" in text):
                    self._maybe_inject_flow("appx-kafka-src", "", text)
            return

        if self.in_table and tag in {"td", "th"}:
            cell = re.sub(r"\s+", " ", "".join(self.cur_cell or []).strip())
            if self.cur_row is not None:
                self.cur_row.append(cell)
            self.cur_cell = None
            return
        if self.in_table and tag == "tr":
            if self.cur_row is not None:
                self.table_rows.append(self.cur_row)
            self.cur_row = None
            return
        if tag == "table" and self.in_table:
            self.in_table -= 1
            self._emit("\n")
            self._emit_lines(self._fmt_table(self.table_rows))
            self._emit("\n")
            self.table_rows = []
            return

        if tag == "pre" and self.in_pre:
            self.in_pre -= 1
            self._emit("\n```\n\n")
            return
        if tag == "li":
            self.li_depth = max(0, self.li_depth - 1)
            return
        if tag == "p":
            self._emit("\n")
            return

        if tag == "div" and self.pending_label in {
            "callout", "callout-danger", "koujue", "reflect"
        }:
            # only close when leaving the callout-like root — heuristic: class contains it
            root = self.pending_label
            if root == "callout" and "callout" not in cls:
                return
            if root == "callout-danger" and "callout" not in cls:
                return
            if root == "koujue" and "koujue" not in cls:
                return
            if root == "reflect" and "reflect" not in cls:
                return
            body = re.sub(r"\s+", " ", "".join(self.cur_cell or []).strip())
            self.cur_cell = None
            kind = self.pending_label
            self.pending_label = ""
            if kind == "reflect":
                if not body or len(body) < 4:
                    return
                title = "✎ 反思"
            elif kind == "koujue":
                title = "★ 口诀"
            elif kind == "callout-danger":
                title = "⚠ 警告"
            else:
                title = "◆ 要点"
                if "金标" in body:
                    title = "★ 金标"
                elif "骨架" in body:
                    title = "⚠ 骨架·待深化"
            self._emit("\n")
            self._emit_lines(box(title, [body] if body else [""]))
            self._emit("\n")
            return

        if tag == "div" and "company-prd" in cls:
            # after case block, ensure five markers visible if prose had bold labels
            pass

    def handle_data(self, data):
        if self.skip:
            return
        if self.in_mermaid:
            self.mermaid_buf.append(data)
            return
        if self.cur_cell is not None:
            self.cur_cell.append(data)
            return
        if self.in_pre:
            self._emit(data)
            return
        # rewrite case five-field markers inline
        t = data
        for raw, mark in CASE_MARKERS:
            if raw in t and f"[{mark}]" not in t:
                t = t.replace(f"{raw}：", f"\n  ▸ [{mark}] ", 1)
                t = t.replace(f"{raw}:", f"\n  ▸ [{mark}] ", 1)
        t = re.sub(r"[ \t\f\v]+", " ", t)
        if t.strip():
            self._emit(t)

    def _fmt_table(self, rows: list[list[str]]) -> list[str]:
        if not rows:
            return []
        cols = max(len(r) for r in rows)
        rows = [r + [""] * (cols - len(r)) for r in rows]
        widths = [3] * cols
        for r in rows:
            for i, c in enumerate(r):
                widths[i] = min(28, max(widths[i], dw(c)))
        lines = []
        sep = "┼".join("─" * w for w in widths)
        top = "┌" + "┬".join("─" * w for w in widths) + "┐"
        mid = "├" + sep + "┤"
        bot = "└" + "┴".join("─" * w for w in widths) + "┘"
        lines.append(top)
        for i, r in enumerate(rows):
            cells = [pad(c[:40], widths[j]) for j, c in enumerate(r)]
            lines.append("│" + "│".join(cells) + "│")
            if i == 0:
                lines.append(mid)
        lines.append(bot)
        return lines

    def _mermaid_to_ascii(self, src: str) -> str:
        src = re.sub(r"<br\s*/?>", " / ", src, flags=re.I)
        kind = "flow"
        head = next((ln.strip() for ln in src.splitlines() if ln.strip() and not ln.strip().startswith("%%")), "")
        if head.startswith("sequenceDiagram"):
            kind = "sequence"
        elif head.startswith("stateDiagram"):
            kind = "state"
        elif head.startswith("classDiagram"):
            kind = "class"

        if kind == "sequence":
            return self._mermaid_sequence(src)
        if kind == "state":
            return self._mermaid_state(src)

        nodes: dict[str, str] = {}
        for m in re.finditer(r'([A-Za-z0-9_]+)\[([^\]]+)\]', src):
            nodes[m.group(1)] = re.sub(r"\s+", " ", m.group(2)).strip()
        for m in re.finditer(r'([A-Za-z0-9_]+)\{([^}]+)\}', src):
            nodes.setdefault(m.group(1), re.sub(r"\s+", " ", m.group(2)).strip())
        for m in re.finditer(r'([A-Za-z0-9_]+)\(\[?([^\]\)]+)\]?\)', src):
            nodes.setdefault(m.group(1), re.sub(r"\s+", " ", m.group(2)).strip())
        for m in re.finditer(r'([A-Za-z0-9_]+)\[\(([^)]+)\)\]', src):
            nodes.setdefault(m.group(1), re.sub(r"\s+", " ", m.group(2)).strip())
        # subgraph titles
        for m in re.finditer(r'subgraph\s+([A-Za-z0-9_]+)\[([^\]]+)\]', src):
            nodes.setdefault(m.group(1), m.group(2).strip())

        edges: list[tuple[str, str, str]] = []
        # A -->|label| B   /  A --> B  /  A -.-> B  /  A ==> B
        edge_re = re.compile(
            r'([A-Za-z0-9_]+)\s*'
            r'(?:-\.->|-->|==>|---|-.->|->)\s*'
            r'(?:\|([^|]*)\|)?\s*'
            r'([A-Za-z0-9_]+)'
        )
        for m in edge_re.finditer(src):
            edges.append((m.group(1), (m.group(2) or "").strip(), m.group(3)))

        if not edges and not nodes:
            lines = [
                ln.rstrip()
                for ln in src.splitlines()
                if ln.strip() and not ln.strip().startswith("%%")
                and not re.match(r'^(flowchart|graph|stateDiagram|sequenceDiagram)\b', ln.strip())
            ]
            body = lines[:22]
            return "\n".join(body) if body else "(empty diagram)"

        out: list[str] = []
        # compact vertical chain: prefer unique adjacency list over repeating boxes
        if edges:
            seen: set[tuple[str, str, str]] = set()
            first = True
            for a, lab, b in edges[:28]:
                key = (a, b, lab)
                if key in seen:
                    continue
                seen.add(key)
                la = nodes.get(a, a)[:36]
                lb = nodes.get(b, b)[:36]
                if first:
                    out.append(f"┌─ {la} ─┐")
                    first = False
                else:
                    # if previous target != this source, restate source
                    if not out or la not in out[-1]:
                        out.append(f"┌─ {la} ─┐")
                out.append("│")
                out.append(f"▼{(' ' + lab) if lab else ''}")
                out.append(f"┌─ {lb} ─┐")
                out.append("")
        else:
            for _, v in list(nodes.items())[:18]:
                out.append(f"◆ {v}")
        return "\n".join(out).rstrip()

    def _mermaid_sequence(self, src: str) -> str:
        aliases: dict[str, str] = {}
        for m in re.finditer(
            r'participant\s+([A-Za-z0-9_]+)\s+as\s+(.+)', src
        ):
            aliases[m.group(1)] = m.group(2).strip()
        msgs: list[str] = []
        msg_re = re.compile(
            r'([A-Za-z0-9_]+)\s*(-->>|->>|-->|->)\s*([A-Za-z0-9_]+)\s*:\s*(.+)'
        )
        for ln in src.splitlines():
            s = ln.strip()
            if not s or s.startswith("%%") or s.startswith("sequenceDiagram"):
                continue
            if s.startswith((
                "participant", "Note", "loop", "alt", "opt", "else", "end",
                "rect", "critical", "break",
            )):
                if s.startswith("loop"):
                    msgs.append(f"∥ {s[4:].strip() or 'loop'}")
                elif s.startswith("opt"):
                    msgs.append(f"◇ {s}")
                elif s.startswith("alt"):
                    msgs.append(f"◇ {s}")
                elif s.startswith("Note"):
                    note = re.sub(
                        r'^Note\s+(over|left of|right of)\s+[^:]+:\s*', '', s
                    )
                    msgs.append(f"※ {note[:60]}")
                continue
            m = msg_re.match(s)
            if m:
                a, arr, b, text = m.group(1), m.group(2), m.group(3), m.group(4).strip()
                la = aliases.get(a, a)
                lb = aliases.get(b, b)
                # mermaid A->>B / A-->>B are both A→B (solid vs dashed reply style)
                arrow = "⇢" if arr in ("-->>", "-->") else "→"
                msgs.append(f"{la} {arrow} {lb} : {text[:52]}")
        if not msgs:
            return self._mermaid_fallback_lines(src)
        return "\n".join(msgs[:36])

    def _mermaid_state(self, src: str) -> str:
        trans: list[str] = []
        # [*] --> Foo : label   /  Foo --> Bar : label
        tr_re = re.compile(
            r'(\[\*\]|[A-Za-z0-9_]+)\s*-->\s*(\[\*\]|[A-Za-z0-9_]+)\s*(?::\s*(.+))?'
        )
        for ln in src.splitlines():
            s = ln.strip()
            if not s or s.startswith("%%") or s.startswith("stateDiagram"):
                continue
            m = tr_re.match(s)
            if m:
                a, b, lab = m.group(1), m.group(2), (m.group(3) or "").strip()
                line = f"{a} ──▶ {b}"
                if lab:
                    line += f"  ({lab[:40]})"
                trans.append(line)
        if not trans:
            return self._mermaid_fallback_lines(src)
        out = ["[*] 状态迁移（按源图顺序）", ""]
        out.extend(f"  {t}" for t in trans[:28])
        return "\n".join(out)

    def _mermaid_fallback_lines(self, src: str) -> str:
        lines = [
            ln.rstrip()
            for ln in src.splitlines()
            if ln.strip() and not ln.strip().startswith("%%")
            and not re.match(
                r'^(flowchart|graph|stateDiagram|sequenceDiagram)\b', ln.strip()
            )
        ]
        body = lines[:22]
        return "\n".join(body) if body else "(empty diagram)"


def build_title_page(toc: list[tuple[str, str]]) -> str:
    today = date.today().isoformat()
    lines = []
    lines.append("╔" + "═" * (W - 2) + "╗")
    lines.append("║" + pad("", W - 2) + "║")
    lines.append("║" + pad("  高级 Java · 下单正逆向闭环白皮书", W - 2) + "║")
    lines.append("║" + pad("  系统学习技术白皮书 · 纯文本美观版", W - 2) + "║")
    lines.append("║" + pad("", W - 2) + "║")
    lines.append("║" + pad(f"  版本：v1.1 诚实交付冻结", W - 2) + "║")
    lines.append("║" + pad(f"  日期：{today}", W - 2) + "║")
    lines.append("║" + pad("  编码：UTF-8 · 等宽字体阅读更佳", W - 2) + "║")
    lines.append("╠" + "═" * (W - 2) + "╣")
    for ln in [
        "【交付摘要 delivery-status】",
        "· 金标 3 块：#s-ddd-agg / #ency-fm-rocket / #ency-fm-polardb",
        "· 其余多为骨架可用；速查勿当深度正文",
        "· 行业案例按五段硬门槛：场景/配置/故障/方案/效果",
        "· 深化项由读者点名（最多 5 项）",
    ]:
        lines.append("║" + pad("  " + ln, W - 2) + "║")
    lines.append("╚" + "═" * (W - 2) + "╝")
    lines.append("")
    lines.append("【目录 TOC】")
    lines.append("─" * W)
    for i, (sid, title) in enumerate(toc, 1):
        anchor = f"#{sid}" if sid else ""
        row = f"  {i:02d}. {anchor:<22} {title}"
        # soft trim
        if dw(row) > W:
            row = row[:80]
        lines.append(row)
    lines.append("─" * W)
    lines.append("")
    # front-matter flowcharts
    lines.append(FLOWCHARTS["method"].rstrip())
    lines.append("")
    lines.append(FLOWCHARTS["c4"].rstrip())
    lines.append("")
    lines.append(FLOWCHARTS["rocket"].rstrip())
    lines.append("")
    lines.append(FLOWCHARTS["polardb"].rstrip())
    lines.append("")
    lines.append(FLOWCHARTS["ddd"].rstrip())
    lines.append("")
    lines.append(FLOWCHARTS["aftersale"].rstrip())
    lines.append("")
    lines.append("═" * W)
    lines.append("以下为正文（自 HTML #exportRoot 提取）")
    lines.append("═" * W)
    lines.append("")
    return "\n".join(lines) + "\n"


def postprocess(text: str) -> str:
    # wrap prose lines that are too long, skip fences / boxes / flow lines
    out = []
    in_fence = False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence or ln.startswith((
            "┌", "│", "└", "├", "╠", "╔", "║", "╚", "◆", "▼", "▸", "  ▸",
            "【文字", "图例", "∥", "◇", "※", "[*]",
        )):
            out.append(ln)
            continue
        if ln.startswith(("═", "─", "·", "「", "#")) or (ln.startswith("  ") and ("│" in ln or "──▶" in ln)):
            out.append(ln)
            continue
        # sequence / labeled flow lines: keep intact
        if " → " in ln or " ← " in ln or " ──▶ " in ln:
            out.append(ln)
            continue
        if dw(ln) <= W + 8:
            out.append(ln)
        else:
            out.extend(wrap(ln, W))
    text = "\n".join(out)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n"


def main():
    raw = HTML_PATH.read_text(encoding="utf-8")
    m = re.search(r'<article id="exportRoot">(.*)</article>', raw, re.S)
    if not m:
        print("exportRoot not found", file=sys.stderr)
        sys.exit(1)
    article = strip_chrome(m.group(1))
    parser = PrettyExport()
    parser.feed(article)
    body = "".join(parser.parts)
    # ensure key flowcharts appear even if section match failed
    for k, fc in FLOWCHARTS.items():
        if f"【文字流程图】" in fc.splitlines()[0] and fc.splitlines()[0] not in body:
            # title page already embeds all; body inject may miss — OK
            pass
    title = build_title_page(parser.toc)
    final = postprocess(title + body)
    OUT_PATH.write_text(final, encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    print(f"bytes={OUT_PATH.stat().st_size}")
    print(f"lines={final.count(chr(10))}")
    print(f"toc_entries={len(parser.toc)}")
    print(f"flows_injected={sorted(parser._injected)}")


if __name__ == "__main__":
    main()
