# -*- coding: utf-8 -*-
"""B. 云原生 Docker/K8s · 极致落地"""
from anti_water_boost import boost_k8s_workload
from helpers import (
    qa, c4, five, tradeoff, mermaid, spine, essence, company_prd,
    plain, koujue, failbox, runbook, pit, reflect, ban, today, floor,
)


def build() -> str:
    hub = f"""
<section class="block" id="t-k8s-x" data-toc="T-K8s-X · 云原生极致落地总图" data-prio="p0">
  <h2><span class="sys-id">T-K8s-X</span>云原生极致落地：Docker/K8s 服务正逆向交易</h2>
{spine("在 T-K8s 之上加厚：工作负载、支付退款安全发布、配置密钥多环境、配额与节点故障、Mesh 决策、Runbook 与题库。",
       serves="订单/OMS/售后发布与弹性",
       back="T-K8s → 本极致章 → <a href='#x-promo-trinity'>交叉大促</a> / S-Year M10")}
{essence(
    "换版本与打爆时生意不能停、账不能乱：支付回调要接住，退款不能因发布双飞。",
    "验收：发布窗口成功率、回滚 RTO、OOMKill、密钥不进镜像、节点挂了单子不丢。",
    "用 Deployment 语义、探针、资源对齐、金丝雀门禁、配额与疏散演练消灭不确定性。",
    "容器参数与 JVM 对齐；HPA 不是秒杀银弹；Mesh 是可选层不是信仰。",
    "半就绪吃回调、金丝雀无资损门禁、HPA 打爆渠道、节点故障无 PDB。",
)}
{plain("人话：K8s 极致落地=把「发布/扩容/挂节点」三件事做成交易值班剧本，而不是 YAML 收藏夹。")}
{company_prd(
    "大促前 OMS 热修+售后分摊修复；要求可金丝雀、可回滚、可证明节点故障不丢支付回调。",
    "JVM 容器参数；探针；HPA 决策；支付/退款发布清单；Config/Secret；配额；节点演练；Mesh 决策；Runbook。",
    "自研 Operator、多集群联邦、全站 Mesh。",
    "构建→金丝雀→三针门禁→放量；异常 revision 回滚。",
    "OOMKill、探针误杀、渠道被扩容打爆、节点 NotReady。",
    "发布检查单签字；回滚演练；节点故障演练记录；Secret 扫描通过。",
    "30 分钟：支付/退款成功率、Pod 重启、Outbox、GC、线程池。",
)}
  <table>
    <thead><tr><th>子章</th><th>锚点</th><th>一句话</th></tr></thead>
    <tbody>
      <tr><td>工作负载设计</td><td><a href="#t-k8s-x-workload">#t-k8s-x-workload</a></td><td>JVM/探针/HPA 与秒杀</td></tr>
      <tr><td>安全发布清单</td><td><a href="#t-k8s-x-release">#t-k8s-x-release</a></td><td>金丝雀/蓝绿对支付退款</td></tr>
      <tr><td>配置密钥多环境</td><td><a href="#t-k8s-x-ops">#t-k8s-x-ops</a></td><td>配额与节点故障演练</td></tr>
      <tr><td>Service Mesh</td><td><a href="#t-k8s-x-mesh">#t-k8s-x-mesh</a></td><td>中厂何时上何时不上</td></tr>
      <tr><td>清单·Runbook·题</td><td><a href="#t-k8s-x-drills">#t-k8s-x-drills</a></td><td>可执行加厚</td></tr>
    </tbody>
  </table>
{koujue("云原生口诀：探针分生死，内存对齐堆，金丝雀看三针，秒杀慎 HPA，Mesh 默认不上。")}
{floor(
    "kubelet 探针与驱逐",
    "kubelet 按 period 探 liveness/readiness；失败达阈值→杀容器或摘 Endpoint。驱逐按 node pressure（内存/磁盘）删 Pod。",
    "认知路径：API Deployment→ReplicaSet→Pod→kubelet syncPod→probe manager；Service Endpoints 摘除未就绪 Pod。看 <code>kubectl describe pod</code> Events、<code>containerStatuses</code>。",
    "liveness 打 DB→依赖抖则重启风暴→支付回调 503；内存 limit 小于堆+直接内存→OOMKilled。",
    "看：RestartCount、OOMKilled、Readiness 翻转、Endpoints 数量与支付成功率同秒相关。",
)}
{today("""<ul>
<li>支付 Deployment：readiness 只查本进程端口；liveness 别查 DB。</li>
<li><code>preStop: sleep 10</code> + 先失败 readiness，再停 Tomcat。</li>
<li>金丝雀门禁接支付/退款/Outbox 三面板，超阈 <code>kubectl rollout undo</code>。</li>
</ul>""")}
{reflect("k8sx-hub-r1")}
</section>
"""

    workload = f"""
<section class="block" id="t-k8s-x-workload" data-toc="T-K8s-X · 订单链路工作负载" data-prio="p0">
  <h2><span class="sys-id">T-K8s-X</span>订单链路工作负载：JVM · 探针 · HPA · 秒杀</h2>
{spine("不同服务扩缩容节奏不同，禁止一个超级 Deployment 吃所有流量形态。",
       serves="订单回调、OMS 消费、售后出口",
       back="T-K8s 拆单元 → 本页")}
{c4(
    "支付回调要稳接、OMS 要消化波次、售后要控出口——三者资源画像不同。",
    "分 Deployment；JVM Xmx&lt;limit；liveness 轻、readiness 表可接客；HPA 看饱和指标而非只看 CPU。",
    "CPU throttle 制造假死；错误 readiness 造成摘不干净；HPA 放大对下游的打砸。",
    "压测给出副本×池×DB 连接公式；秒杀场景书面决定「扩不扩」。",
    "秒杀尖刺秒级，HPA 分钟级——时间常数不匹配。",
)}
""" + boost_k8s_workload() + f"""
  <h3 id="k8sx-w-jvm">JVM 容器参数对齐（写死习惯）</h3>
  <table>
    <thead><tr><th>项</th><th>建议</th><th>若违背</th></tr></thead>
    <tbody>
      <tr><td>heap</td><td><code>-Xmx</code> ≈ limit 的 50–75%（留 metaspace/direct/线程栈）</td><td>OOMKill 连环</td></tr>
      <tr><td>容器感知</td><td>现代 JDK 认 cgroup；旧版显式 CPU/内存</td><td>GC 线程数离谱</td></tr>
      <tr><td>GC</td><td>G1/ZGC 按延迟目标；大促前固定版本</td><td>发布换 GC 当实验</td></tr>
      <tr><td>优雅停机</td><td><code>preStop</code> sleep + 摘流 + 排水中断</td><td>回调 503 风暴</td></tr>
      <tr><td>连接池</td><td>按 Pod 数反推 DB 最大连接</td><td>扩容打满 DB</td></tr>
    </tbody>
  </table>
  <h3 id="k8sx-w-probe">探针分工</h3>
  <table>
    <thead><tr><th>探针</th><th>检查什么</th><th>禁止</th></tr></thead>
    <tbody>
      <tr><td>liveness</td><td>进程死锁/卡死（轻）</td><td>查 DB/下游</td></tr>
      <tr><td>readiness</td><td>能接客：本地依赖就绪、非排水中</td><td>把远端慢依赖当永久未就绪而无超时</td></tr>
      <tr><td>startup</td><td>慢启动 JVM</td><td>用 liveness 硬杀启动中实例</td></tr>
    </tbody>
  </table>
  <h3 id="k8sx-w-hpa">HPA 与秒杀：该不该 HPA？</h3>
{tradeoff("秒杀/大促弹性", [
    ("活动前预热固定副本", "稳", "尖刺前已知", "资源预留成本", "<b>秒杀默认</b>"),
    ("HPA 按 CPU", "滞后", "慢于秒杀", "低", "仅平峰"),
    ("HPA 按自定义 QPS/队列深度", "较好", "需指标管道", "中", "OMS 消费可"),
    ("KEDA 按 MQ lag", "贴业务", "需运维", "中", "Outbox/MQ 消费者"),
    ("无限 HPA + 无出口限流", "看似弹性", "打爆渠道/DB", "事故", "<b>禁止</b>"),
])}
{plain("人话：秒杀像洪水，HPA 像慢慢拧水龙头。洪水靠水库（预热+限流+削峰队列），不靠拧龙头的手速。")}
{five(
    "秒杀不靠 HPA 救场；支付回调池与 DB 连接有上限模型。",
    "主：预热；支：限流；异：降级；逆：售后出口限流独立。",
    "按 CPU 盲目扩、探针打下游、Xmx=limit。",
    "预热+队列削峰；HPA 只给可扩展且出口受限的服务。",
    "压测证明扩容收益；演练节点杀软。",
)}
{qa("【场景题】售后 HPA 从 5 扩到 40，渠道超时暴增，为什么？",
    ["出口无限制，扩容=放大打砸；渠道限流/熔断应在应用侧，HPA 上限要绑定下游配额。",
     "客服高峰。", "只加 maxReplicas。", "出口限流+maxReplicas 公式。", "「扩容前先问下游配额。」"],
    "k8sx-w-q1")}
{reflect("k8sx-w-r1")}
</section>
"""

    release = f"""
<section class="block" id="t-k8s-x-release" data-toc="T-K8s-X · 支付退款安全发布" data-prio="p0">
  <h2><span class="sys-id">T-K8s-X</span>金丝雀 / 蓝绿：支付与退款安全发布清单</h2>
{spine("资损敏感发布的检查单写死，避免「感觉平稳就全量」。",
       serves="支付回调、退款口径、分摊热修",
       back="T-K8s 发布 → 本页 → S-MS-X 灰度")}
{mermaid("diag-k8sx-release", '''flowchart TD
  Build[镜像tag不可变] --> Canary[金丝雀1%-5%]
  Canary --> Gate{三针门禁}
  Gate -->|支付成功/退款成功/Outbox OK| Ramp[放量]
  Gate -->|资损或错误预算烧| RB[revision回滚+开关关]
  Ramp --> Full[全量]
  Full --> Watch[观察30-60min]
''')}
  <h3 id="k8sx-r-checklist">安全发布清单（支付/退款）</h3>
  <ul class="checklist">
    <li>变更分类：兼容修复 / 口径变更 / schema——口径与 schema 强制金丝雀或 expand/contract</li>
    <li>镜像 tag 不可变；禁止 <code>latest</code> 上生产</li>
    <li>DB 先扩后缩；禁止回滚应用却留下不兼容列用法</li>
    <li>特征开关默认安全；与金丝雀正交（可关逻辑不回滚也可）</li>
    <li>金丝雀门禁：支付成功率、退款成功率、Outbox 年龄、分摊不平衡、5xx、重启</li>
    <li>资损告警 → 自动/一键缩容金丝雀到 0</li>
    <li>排水：readiness=false → preStop → 注册摘除 → 再杀进程</li>
    <li>回调兼容：新旧版本都能处理渠道通知</li>
    <li>回滚演练：本季做过；RTO 写入 Runbook</li>
    <li>发布窗口避开日终对账锁账时段（若有）</li>
  </ul>
{tradeoff("发布策略选择", [
    ("滚动", "兼容前提", "连续", "低", "常规"),
    ("金丝雀", "可控爆炸半径", "稍慢", "中", "<b>支付/退款口径</b>"),
    ("蓝绿", "切换快", "双倍资源", "高", "难兼容大版本"),
])}
{failbox("新旧逻辑各吃 50% 无法对账",
         "分摊算法无版本号，金丝雀与稳定版对同一规则理解不同→财务抽检失败。口径变更必须 ruleVersion 钉扎并写入订单快照。")}
{qa("【场景题】蓝绿切换瞬间退款失败尖刺，如何设计切换？",
    ["先暖连接/缓存；切换用加权或短重叠；确保两端都能处理在途退款；切换后紧盯渠道错误码；异常立即切回。",
     "大版本。", "DNS 一把切无观察。", "清单+演练。", "「切流量前先切信心。」"],
    "k8sx-r-q1")}
{reflect("k8sx-r-r1")}
</section>
"""

    ops = f"""
<section class="block" id="t-k8s-x-ops" data-toc="T-K8s-X · 配置密钥配额演练" data-prio="p0">
  <h2><span class="sys-id">T-K8s-X</span>配置 / 密钥 / 多环境 · 资源配额 · 节点故障演练</h2>
{spine("环境漂移与节点死亡是外包进组高频事故源。", serves="多环境发布与稳定性", back="T-K8s 配置 → 本页")}
  <h3 id="k8sx-ops-env">多环境与密钥</h3>
  <table>
    <thead><tr><th>项</th><th>做法</th><th>禁止</th></tr></thead>
    <tbody>
      <tr><td>ConfigMap</td><td>非机密；版本化；可回滚</td><td>把密钥放进 CM</td></tr>
      <tr><td>Secret/KMS</td><td>支付密钥外置；轮换；审计</td><td>写进镜像/日志</td></tr>
      <tr><td>环境</td><td>dev/stage/prod 隔离账号与桶</td><td>stage 指产库「图方便」</td></tr>
      <tr><td>开关</td><td>大促开关单独面板+权限</td><td>工程师个人改产配置无单</td></tr>
    </tbody>
  </table>
  <h3 id="k8sx-ops-quota">资源配额与噪音邻居</h3>
  <ul>
    <li>Namespace Quota / LimitRange：防某队吃光节点。</li>
    <li>requests≈实际，limits 防暴走；CPU limit 过紧→throttle 假死。</li>
    <li>PDB：支付/OMS 保证最小可用，防同时驱逐。</li>
  </ul>
  <h3 id="k8sx-ops-node">节点故障演练剧本</h3>
{runbook("节点 NotReady / 杀软",
         """<ol>
      <li>选定非全部支付副本所在节点；cordon + drain（尊重 PDB）。</li>
      <li>观察：回调成功率、Pod 重建时间、Outbox、会话粘滞是否误伤。</li>
      <li>验证：新节点调度成功；无脑杀不尊重 PDB 的脚本禁止。</li>
      <li>记录 RTO/RPO 观感；修 affinity/拓扑若过浓。</li>
    </ol>""")}
{pit("drain 不尊重 PDB 或把全部支付副本打到同一节点——演练变事故。")}
{qa("【场景题】stage 用了 prod 支付密钥做联调，如何治理？",
    ["密钥分环境；流水线扫描；最小权限；联调走沙箱渠道；追责审计。",
     "赶工。", "「先上了再换」。", "Secret 策略+准入。", "「沙箱密钥是纪律不是建议。」"],
    "k8sx-ops-q1")}
{reflect("k8sx-ops-r1")}
</section>
"""

    mesh = f"""
<section class="block" id="t-k8s-x-mesh" data-toc="T-K8s-X · Service Mesh决策" data-prio="p0">
  <h2><span class="sys-id">T-K8s-X</span>Service Mesh：中厂何时上 · 何时不上</h2>
{spine("Mesh 解决的是一致性治理与可观测下沉，不是交易业务本身。", back="S-MS-X 中厂对照 → 本页")}
{c4(
    "中厂缺人时，Mesh 的运维税可能高于它消灭的配置漂移税。",
    "默认：网关+SDK 治理（超时重试熔断）+ OTel。出现多语言统一 mTLS/流量治理且有平台编制再评估 Istio/Linkerd。",
    "边车资源与排障复杂度；故障域增加（控制面）。",
    "决策进 ADR：问题、替代、成本、回滚；禁止「大厂有我们也要」。",
    "大促前禁止首次上 Mesh。",
)}
{tradeoff("流量治理落点", [
    ("Spring Cloud / Resilience4j + 网关", "够用", "高", "低", "<b>中厂默认</b>"),
    ("Linkerd 轻量", "mTLS/重试统一", "中", "中", "多语言且编制≥1"),
    ("Istio 全家桶", "强", "看控制面", "高", "有平台组"),
    ("大促当周上 Mesh", "赌博", "未知", "事故", "<b>禁止</b>"),
])}
{ban("<ul><li>无人会排障边车就上全站 Mesh</li><li>用 Mesh 重试掩盖非幂等写</li><li>Mesh 与 SDK 双重重试</li></ul>")}
{qa("【场景题】面试官问「你们为什么不上 Istio」怎么答？",
    ["我们缺的是超时矩阵与幂等纪律，不是边车；上 Mesh 的触发条件是多语言统一治理+编制，现在用网关+SDK 达到同等验收。",
     "架构评审。", "贬低 Mesh。", "给 ADR。", "「先纪律后平台。」"],
    "k8sx-m-q1")}
{reflect("k8sx-m-r1")}
</section>
"""

    drills = f"""
<section class="block" id="t-k8s-x-drills" data-toc="T-K8s-X · 落地清单与题" data-prio="p0">
  <h2><span class="sys-id">T-K8s-X</span>落地清单 · 故障 Runbook · 多题详答</h2>
  <h3 id="k8sx-d-land">落地清单（交易域容器化）</h3>
  <ul class="checklist">
    <li>订单 / OMS / 售后分 Deployment，连接池按副本核算</li>
    <li>JVM 与 memory limit 对齐文档化</li>
    <li>liveness/readiness/startup 三分</li>
    <li>金丝雀门禁接支付/退款/Outbox</li>
    <li>Secret 不进镜像；环境隔离</li>
    <li>PDB + 拓扑分散支付副本</li>
    <li>HPA 上限绑定下游配额；秒杀预热</li>
    <li>节点 drain 演练每季</li>
    <li>Mesh 默认不上并有 ADR</li>
    <li>发布检查单与回滚 RTO 写进值班手册</li>
  </ul>
{runbook("交易链路发布异常 10 分钟",
         """<ol>
      <li>三针：支付成功、退款成功、Outbox 年龄；叠加 5xx/重启。</li>
      <li>超阈 → rollback revision + 关特征开关。</li>
      <li>OOMKill → 对齐 Xmx/limit；临时提 limit。</li>
      <li>503 回调 → 查排水/注册摘除/readiness。</li>
      <li>保留镜像 tag、配置版本、trace、看板截图。</li>
    </ol>""")}

{qa("【题】为何说「readiness 失败应摘流，liveness 失败才杀」？",
    ["未就绪可能是依赖抖动或排水；杀进程会放大雪崩。liveness 仅表示进程不可救。",
     "依赖抖动。", "两探针打同一重检查。", "分探针+超时。", "「摘流可逆，杀进程更贵。」"],
    "k8sx-d-q1")}
{qa("【题】支付服务能不能开 HPA 目标 CPU 30% 激进扩？",
    ["先算 DB 连接与下游配额；激进扩可能先打满 DB。支付更常预热+垂直容量，HPA 温和且有上限。",
     "大促。", "只看 CPU。", "容量模型表。", "「扩展性被最窄依赖决定。」"],
    "k8sx-d-q2")}
{qa("【题】金丝雀已全量，发现分摊 bug，回滚还是正向修复？",
    ["看数据兼容与资损速度：资损中优先回滚+开关；若 schema 已不可逆则正向热修+冻结相关退款人工。",
     "口径变更。", "坚持「向前修复」面子。", "清单预设决策树。", "「钱在流血就回滚。」"],
    "k8sx-d-q3")}
{qa("【题】节点磁盘满导致 Evicted，支付 Pod 没了，如何预防？",
    ["日志落 stdout+采集；emptyDir 限额；磁盘告警；PDB；反亲和。",
     "日志写容器盘。", "加副本不治本。", "演练 Evict。", "「磁盘是隐蔽单点。」"],
    "k8sx-d-q4")}
{qa("【题】用四段讲「交易域上 K8s 的价值」",
    ["C1 怕换版本与打爆时账乱；C2 探针金丝雀配额；C3 爆炸半径与资源对齐；C4 回滚演练与大促成功率。",
     "甲方追问上云。", "堆名词。", "挂回验收句。", "「编排管爆炸半径。」"],
    "k8sx-d-q5")}
{reflect("k8sx-d-r1")}
</section>
"""
    return hub + workload + release + ops + mesh + drills
