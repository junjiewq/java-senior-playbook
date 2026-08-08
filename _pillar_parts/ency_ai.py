# -*- coding: utf-8 -*-
"""AI 百科（全且深）— 与 T-AI-Stack 交叉不灌水"""
from ency_factory import sec, deep
from helpers import plain, qa, koujue, reflect


def build() -> str:
    parts = []
    parts.append(sec(
        "ency-ai", "ENCY-AI · AI百科总图", "ENCY-AI", "AI 百科总图（交叉前序）",
        deep(
            plain_txt="人话：前序 <a href='#t-ai-stack'>T-AI-Stack</a>/<a href='#t-ai-x'>T-AI-X</a>/<a href='#t-as'>T-AS</a> 已钉生产红线；本百科补训练推理微调与评测/向量/合规深条目，并给标准流程图。",
            biz="提效客服/研发，禁止直改账务。",
            impl="RAG+工具+HITL；评测门禁；私有化边界。",
            principle="概率系统+确定性状态机协作。",
            substance="幻觉资损=0；工具白名单；评测回归绿。",
            mermaid_id="diag-ency-ai-map",
            mermaid_code="""flowchart TB
  Life[训练/微调/推理] --> RAG[RAG]
  RAG --> Agent[Agent循环]
  Agent --> MCP[MCP/Skills]
  Agent --> Eval[评测闭环]
  Vec[向量库] --> RAG
  Priv[私有化安全] --> Life
  Priv --> Agent
""",
            today_html="<ul><li>交叉阅读前序专章；本附录不重复灌水，只加深。</li></ul>",
            reflect_id="ency-ai-hub-r1",
            koujue_txt="AI 口诀：检索有据，工具白名单，人审改账，评测门禁。",
            spine_pos="AI 副驾挂售后/优惠/复盘，不挂资金写入。",
            serves="人效",
            back="T-AI-* → 本百科",
        ),
    ))
    topics = [
        ("ency-ai-life", "ENCY-AI · 训练推理微调", "ENCY-AI-LIFE", "训练 / 推理 / 微调", {
            "plain_txt": "比喻：训练是办学校，微调是上岗前集训，推理是每天上班答问。",
            "biz": "领域话术更贴；成本可控。",
            "impl": "优先 RAG；不够再 SFT/LoRA；推理限流与缓存。",
            "principle": "预训练泛化；对齐；量化；批推理。",
            "substance": "质量/成本/延迟三角。",
            "mermaid_id": "diag-ency-ai-life",
            "mermaid_code": """flowchart LR
  Pre[预训练] --> SFT[微调SFT/LoRA]
  SFT --> Align[对齐]
  Align --> Serve[推理服务]
  Serve --> Cache[缓存/限流]
""",
            "today_html": "<ul><li>售后话术：先 RAG 再考虑微调。</li></ul>",
            "qas": [("【选型】一定要微调吗？", ["多数中厂 RAG+提示够用；微调要数据与评测预算。", "立项。", "跟风训。", "评测驱动。", "「先检索再微调。」"], "ency-ai-life-q1")],
            "reflect_id": "ency-ai-life-r1",
            "koujue_txt": "生命周期口诀：检索优先，微调有数，推理控本。",
            "floor_title": "LoRA",
            "structure": "低秩适配权重；基座冻结。",
            "source_path": "训练脚本→导出→推理加载 adapter。",
            "online": "遗忘通用能力；版本未钉扎。",
            "verify": "评测集回归。",
        }),
        ("ency-ai-rag", "ENCY-AI · RAG深潜", "ENCY-AI-RAG", "RAG：分块 / 检索 / 生成 / 引用", {
            "plain_txt": "交叉 <a href='#t-rag'>T-RAG</a>：百科给出标准流程图与售后案例加深。",
            "biz": "客服/售后答得有据，少幻觉。",
            "impl": "分块策略；混合检索；强制引用；更新管道。",
            "principle": "向量召回+词法；重排；上下文窗口。",
            "substance": "引用率；投诉幻觉率。",
            "mermaid_id": "diag-ency-ai-rag",
            "mermaid_code": """flowchart TD
  Doc[制度/FAQ/工单] --> Chunk[分块]
  Chunk --> Emb[Embedding]
  Emb --> Vec[(向量库)]
  Q[用户问] --> Ret[检索TopK]
  Vec --> Ret
  Ret --> Rerank[重排]
  Rerank --> LLM[生成+强制引用]
  LLM --> Ans[回答]
""",
            "today_html": "<ul><li>售后政策变更要重索引。</li><li>无检索命中则拒答。</li></ul>",
            "qas": [("【幻觉】模型编造退款时效？", ["无引用拒答；命中政策块；评测集加对抗题。", "客服。", "加温度。", "强制引用。", "「无据不答。」"], "ency-ai-rag-q1")],
            "reflect_id": "ency-ai-rag-r1",
            "koujue_txt": "RAG 口诀：分块有重叠，检索要混合，回答强制引。",
            "floor_title": "分块",
            "structure": "段落/标题层级；重叠；元数据过滤。",
            "source_path": "ingest→embed→upsert；query→search→prompt。",
            "online": "旧政策块未删导致错答。",
            "verify": "文档版本戳；抽检。",
        }),
        ("ency-ai-agent", "ENCY-AI · Agent循环", "ENCY-AI-AGENT", "Agent：规划 · 工具循环 · HITL", {
            "plain_txt": "交叉 <a href='#t-agents'>T-Agents</a>：标准工具循环图 + 禁止改账。",
            "biz": "助理起草与查询；人确认才驱状态机。",
            "impl": "ReAct 循环；工具白名单；审计。",
            "principle": "观察-思考-行动；终止条件；权限。",
            "substance": "越权工具调用=0。",
            "mermaid_id": "diag-ency-ai-agent",
            "mermaid_code": """flowchart TD
  U[用户意图] --> Plan[规划]
  Plan --> Act[选择工具]
  Act --> Tool[执行MCP/API]
  Tool --> Obs[观察结果]
  Obs --> Decide{够了?}
  Decide -->|否| Plan
  Decide -->|是| Draft[草稿]
  Draft --> HITL{人审?}
  HITL -->|资损| Human[人工确认]
  Human --> SM[状态机执行]
  HITL -->|只读| Out[直接回复]
""",
            "today_html": "<ul><li>退款工具仅「申请单草稿」；执行在人审后。</li></ul>",
            "ban_note": True,
            "qas": [("【红线】Agent 能否直接调退款 API？", ["否。只许草稿+HITL。", "安全。", "为了快。", "白名单。", "「AI 草稿，状态机记账。」"], "ency-ai-agent-q1")],
            "reflect_id": "ency-ai-agent-r1",
            "koujue_txt": "Agent 口诀：工具可观察，写账必须人。",
            "extra_html": '  <div class="callout danger"><div class="label">禁止清单</div>禁止 Agent 直连退款/改库存/改分摊；禁止无审计工具。</div>\n',
        }),
        ("ency-ai-mcp", "ENCY-AI · MCP与Skills", "ENCY-AI-MCP", "MCP / Skills 百科条目", {
            "plain_txt": "交叉 <a href='#t-mcp'>T-MCP</a>/<a href='#t-skills'>T-Skills</a>：条目化边界与威胁。",
            "biz": "工具暴露可控；技能沉淀可复用。",
            "impl": "MCP 鉴权；Skills 触发条件；最小权限。",
            "principle": "协议层工具；技能=流程+知识包。",
            "substance": "提示注入失败；技能无冲突。",
            "mermaid_id": "diag-ency-ai-mcp",
            "mermaid_code": """flowchart LR
  Agent --> MCP[MCP Server]
  MCP --> T1[只读查单]
  MCP --> T2[开草稿工单]
  Skills[Skills包] --> Agent
""",
            "today_html": "<ul><li>生产 MCP 禁文件系统乱写。</li><li>Skills 勿塞整本百科。</li></ul>",
            "qas": [("【注入】用户让模型忽略政策？", ["系统提示+工具层鉴权+输出过滤。", "安全。", "只靠提示。", "纵深。", "「提示不是墙。」"], "ency-ai-mcp-q1")],
            "reflect_id": "ency-ai-mcp-r1",
            "koujue_txt": "MCP/Skills 口诀：最小权限，技能要短，注入当敌。",
        }),
        ("ency-ai-eval", "ENCY-AI · 评测闭环", "ENCY-AI-EVAL", "评测闭环：集 · 指标 · 门禁 · 回归", {
            "plain_txt": "比喻：评测集是科目二考场——模型换版本先考过再上路。",
            "biz": "防「新版本更会胡说」。",
            "impl": "金标集；自动指标+人工抽检；CI 门禁。",
            "principle": "任务指标：准确/引用/拒答；安全指标：越权。",
            "substance": "回归绿才能发。",
            "mermaid_id": "diag-ency-ai-eval",
            "mermaid_code": """flowchart TD
  Change[提示/模型/索引变更] --> Eval[跑评测集]
  Eval --> Pass{门禁}
  Pass -->|是| Deploy[灰度]
  Pass -->|否| Fix[修复]
  Fix --> Eval
  Deploy --> Sample[线上抽检]
  Sample --> Eval
""",
            "today_html": "<ul><li>售后政策题+对抗注入题必收录。</li></ul>",
            "qas": [("【门禁】没有金标怎么办？", ["先人工抽 100 题固化；再迭代。", "起步。", "不测上线。", "最小集。", "「先有考场。」"], "ency-ai-eval-q1")],
            "reflect_id": "ency-ai-eval-r1",
            "koujue_txt": "评测口诀：有集有门禁，变更必回归。",
        }),
        ("ency-ai-vec", "ENCY-AI · 向量库", "ENCY-AI-VEC", "向量库 / Embedding", {
            "plain_txt": "比喻：Embedding 把句子变成坐标；向量库是会「附近搜索」的地图。",
            "biz": "检索延迟与召回支撑 RAG。",
            "impl": "选型（Milvus/Qdrant/pgvector 等）；维度一致；过滤元数据。",
            "principle": "ANN；度量余弦/点积；过滤+向量。",
            "substance": "召回率；P99。",
            "mermaid_id": "diag-ency-ai-vec",
            "mermaid_code": """flowchart TD
  Text[文本] --> Model[Embedding模型]
  Model --> Upsert[写入向量库]
  Query --> Model2[同模型]
  Model2 --> ANN[ANN检索]
  Upsert --> ANN
""",
            "today_html": "<ul><li>模型变更要全量重嵌。</li></ul>",
            "qas": [("【坑】混用不同 Embedding？", ["空间不一致召回崩。", "RAG。", "省事混用。", "版本钉扎。", "「同模同维。」"], "ency-ai-vec-q1")],
            "reflect_id": "ency-ai-vec-r1",
            "koujue_txt": "向量口诀：同模同维，元数据过滤，变更重嵌。",
            "floor_title": "ANN",
            "structure": "HNSW/IVF 等索引；召回-精度权衡。",
            "source_path": "embed→index→search。",
            "online": "过滤过严空结果导致胡编。",
            "verify": "空结果拒答率。",
        }),
        ("ency-ai-mm", "ENCY-AI · 多模态", "ENCY-AI-MM", "多模态边界（图/音/文档）", {
            "plain_txt": "人话：多模态能看图识包裹破损，但不等于能自动判责退款。",
            "biz": "质检辅助；票据识别；仍需人审定责。",
            "impl": "OCR/多模态模型作特征；结论进工单草稿。",
            "principle": "模态对齐难；幻觉在图像描述也存在。",
            "substance": "误检率；人工复核占比。",
            "mermaid_id": "diag-ency-ai-mm",
            "mermaid_code": """flowchart TD
  Img[破损图] --> MM[多模态理解]
  MM --> Draft[质检意见草稿]
  Draft --> Human[质检员确认]
  Human --> AS[售后状态机]
""",
            "today_html": "<ul><li>图像结论禁止直接驱动退款。</li></ul>",
            "qas": [("【边界】拍图即退？", ["否。辅助证据链。", "售后。", "全自动。", "HITL。", "「图是证据不是判决。」"], "ency-ai-mm-q1")],
            "reflect_id": "ency-ai-mm-r1",
            "koujue_txt": "多模态口诀：能描述，慎判决，必人审。",
        }),
        ("ency-ai-priv", "ENCY-AI · 私有化与AgentScope", "ENCY-AI-PRIV", "私有化 · 数据安全 · AgentScope 补条", {
            "plain_txt": "交叉 <a href='#t-as'>T-AS</a>/<a href='#t-as-deep'>T-AS+</a>：补私有化与同类对照百科条。",
            "biz": "订单/用户数据不出境或不出域；审计合规。",
            "impl": "私有模型/网关；脱敏；工具审计；AgentScope 嵌入边界。",
            "principle": "数据分级；提示中的 PII；供应链模型风险。",
            "substance": "泄露事件=0；审计可回放。",
            "mermaid_id": "diag-ency-ai-priv",
            "mermaid_code": """flowchart TD
  Data[订单数据] --> Gate[脱敏/网关]
  Gate --> PrivLLM[私有推理]
  Gate --> Cloud{是否上云?}
  Cloud -->|否| Local[本地]
  Cloud -->|是| Contract[合同+脱敏字段]
  AS[AgentScope] --> Tools[白名单工具]
  Tools --> Audit[审计日志]
""",
            "extra_html": """  <h4>AgentScope 与同类（百科条）</h4>
  <table>
    <thead><tr><th>框架</th><th>特点</th><th>交易嵌入建议</th></tr></thead>
    <tbody>
      <tr><td><b>AgentScope</b></td><td>多智能体消息/管线，阿里生态</td><td>售后助理编排；写账 HITL</td></tr>
      <tr><td>LangGraph 等</td><td>图状态机强</td><td>复杂流程可视化；同样白名单</td></tr>
      <tr><td>自研编排</td><td>可控</td><td>中厂常见；成本在维护</td></tr>
    </tbody>
  </table>
""",
            "today_html": "<ul><li>生产提示禁塞完整身份证/卡号。</li><li>AgentScope 只挂只读+草稿工具。</li></ul>",
            "qas": [("【合规】能否把订单库给公有 LLM？", ["默认否；要脱敏+法务；优先私有。", "安全。", "图方便。", "分级。", "「数据分级再说模型。」"], "ency-ai-priv-q1")],
            "reflect_id": "ency-ai-priv-r1",
            "koujue_txt": "私有化口诀：分级脱敏，框架只是壳，红线看工具。",
        }),
    ]
    for sid, toc, sys_id, title, kw in topics:
        kw.pop("ban_note", None)
        kw.setdefault("spine_pos", "AI 副驾挂主线，不改账。")
        kw.setdefault("serves", "客服/售后/研发提效")
        kw.setdefault("back", "T-AI-* → 本叶")
        parts.append(sec(sid, toc, sys_id, title, deep(**kw)))
    parts.append(sec(
        "ency-ai-drill", "ENCY-AI · 综合题", "ENCY-AI-DRILL", "AI 百科综合演练",
        plain("串起 RAG→Agent→评测→私有化。")
        + qa("【综合】售后政策变更后如何上线新助手？",
            ["重索引→评测集含新政策→门禁→灰度→抽检；Agent 仍 HITL。",
             "发布。", "改提示直接全量。", "评测门禁。", "「政策变更=数据+评测。」"],
            "ency-ai-drill-q1")
        + reflect("ency-ai-drill-r1"),
    ))
    return "\n".join(parts)
