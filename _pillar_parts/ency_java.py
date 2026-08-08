# -*- coding: utf-8 -*-
"""Java 技术百科（极全极深）"""
from ency_factory import sec, deep
from helpers import plain, qa, koujue, reflect


def build() -> str:
    parts = []
    parts.append(sec(
        "ency-j", "ENCY-J · Java百科总图", "ENCY-J", "Java 技术百科总图",
        deep(
            plain_txt="人话：Java 百科从语言语义一路凿到 Netty/Spring/测试安全——每节问：支付回调线程在这层会怎么死。",
            biz="服务稳定承载下单/支付/售后流量。",
            impl="并发模型+内存+IO+框架生命周期对齐容器。",
            principle="JMM/GC/集合/IO 事件循环是底板；框架是底板之上的约定。",
            substance="P99、错误率、泄漏、拒单可解释。",
            mermaid_id="diag-ency-j-map",
            mermaid_code="""flowchart TB
  Lang[语言语义] --> Conc[并发JUC]
  Conc --> JVM[JVM/GC]
  JVM --> Col[集合]
  Col --> IO[IO/NIO/Netty]
  IO --> FW[Spring/ORM]
  FW --> QA[测试/安全/性能]
""",
            today_html="<ul><li>与 <a href='#t-found-x'>T-Found-X</a> 交叉：本百科补集合/IO/SPI/测试/安全等未写透处。</li></ul>",
            reflect_id="ency-j-hub-r1",
            koujue_txt="Java 口诀：语义清楚，并发可控，内存可见，IO 不堵。",
            spine_pos="Java 底板服务正逆向工程实现。",
            serves="支付/售后 Pod",
            back="T1/T-Found-X → 本百科",
        ),
    ))

    topics = [
        ("ency-j-lang", "ENCY-J · 语言语义", "ENCY-J-LANG", "语言：类型 / 泛型 / 异常契约 / equals", {
            "plain_txt": "比喻：equals/hashCode 是身份证规则；泛型是安检口贴纸——运行时大多擦掉。",
            "biz": "领域对象比较与集合去重正确，避免订单 Set 丢元素。",
            "impl": "值对象正确实现 equals/hashCode；受检异常别滥用；Optional 边界清晰。",
            "principle": "类型擦除；桥接方法；字符串不可变与常量池。",
            "substance": "集合去重 bug=0；序列化兼容。",
            "floor_title": "equals 契约与擦除",
            "structure": "自反对称传递一致；参与 hash 的字段必须稳定。",
            "source_path": "HashMap 用 hash→equals；记录类/ Lombok 生成要审字段。",
            "online": "可变字段进 hash→丢桶；订单号用 == 比较。",
            "verify": "单测契约；SpotBugs。",
            "mermaid_id": "diag-ency-j-lang",
            "mermaid_code": """flowchart TD
  Put[放入HashMap] --> Hash[hashCode]
  Hash --> Eq[equals判等]
  Eq --> Bucket[同桶链/树]
""",
            "today_html": "<ul><li>订单 ID 用唯一键字符串/Long，禁可变实体当键。</li></ul>",
            "qas": [("【坑】实体当 HashMap key 被改字段？", ["丢元素/脏读。用不可变 ID。", "缓存。", "可变 key。", "ID 键。", "「键不可变。」"], "ency-j-lang-q1")],
            "reflect_id": "ency-j-lang-r1",
            "koujue_txt": "语言口诀：契约先守，键不可变。",
        }),
        ("ency-j-juc", "ENCY-J · 并发加深", "ENCY-J-JUC", "并发：JMM / AQS / 池 / 无锁", {
            "plain_txt": "交叉 <a href='#t-found-juc'>T-Found-JUC</a>：这里加厚 happens-before 与常见订单坑。",
            "biz": "回调并发不错账；池打满可观测。",
            "impl": "有界池+舱壁；volatile/最终发布；少用全局锁包 IO。",
            "principle": "JMM：工作内存/主内存；hb 规则；AQS CLH；CHM 扩容。",
            "substance": "双扣=0；拒绝策略打点。",
            "hc": "大促回调。",
            "floor_title": "happens-before 与发布",
            "structure": "监视器锁/volatile/线程 start/join 等 hb；安全发布用 final 或锁。",
            "source_path": "AQS acquireQueued；TPE execute；Unsafe CAS。",
            "online": "懒启单例无锁导致 NPE；无界池 OOM。",
            "verify": "jstack；池指标。",
            "mermaid_id": "diag-ency-j-juc",
            "mermaid_code": """flowchart TD
  T1[线程写] -->|hb| Unlock[解锁]
  Unlock -->|hb| Lock[他线程加锁]
  Lock --> T2[读到新值]
""",
            "today_html": "<ul><li>支付回调池独立；禁 CachedThreadPool。</li></ul>",
            "qas": [("【原理】为何 synchronized 能见性？", ["解锁 hb 加锁；刷新工作内存。", "并发。", "只背互斥。", "讲 hb。", "「锁不只互斥还有可见。」"], "ency-j-juc-q1")],
            "reflect_id": "ency-j-juc-r1",
            "koujue_txt": "并发口诀：hb 可见，池有界，锁不加 IO。",
        }),
        ("ency-j-jvm", "ENCY-J · JVM加深", "ENCY-J-JVM", "JVM：内存 / GC / 诊断", {
            "plain_txt": "交叉 <a href='#t-found-jvm'>T-Found-JVM</a>：补诊断路径与直接内存。",
            "biz": "支付 Pod 不停顿到用户可感；OOMKill=0。",
            "impl": "G1+容器百分比；GC 日志；NMT；heap dump 流程。",
            "principle": "分代/Region；Safepoint；直接内存与堆分离。",
            "substance": "GC Pause P99；重启次数。",
            "floor_title": "诊断工具链",
            "structure": "jstat/jcmd/jmap/jstack/async-profiler。",
            "source_path": "GC 日志分析 Pause；dump 用 MAT/JOL。",
            "online": "导出 Excel 打爆同进程支付。",
            "verify": "GC 与成功率同屏。",
            "mermaid_id": "diag-ency-j-jvm",
            "mermaid_code": """flowchart TD
  Alloc[分配] --> Eden
  Eden --> Sur[Survivor]
  Sur --> Old
  Old --> GC[混合/Full]
  GC --> SP[Safepoint停顿]
""",
            "today_html": "<ul><li>大对象作业隔离进程。</li></ul>",
            "qas": [("【OOM】堆不满被 Kill？", ["Direct/Metaspace/线程栈。", "容器。", "只加 Xmx。", "NMT。", "「Kill 看 cgroup。」"], "ency-j-jvm-q1")],
            "reflect_id": "ency-j-jvm-r1",
            "koujue_txt": "JVM 口诀：日志先开，堆非堆分清。",
        }),
        ("ency-j-col", "ENCY-J · 集合源码", "ENCY-J-COL", "集合：HashMap / List / CHM / 迭代", {
            "plain_txt": "比喻：HashMap 是很多抽屉；冲突拉链/树化；扩容要搬抽屉。",
            "biz": "本地缓存与去重结构在售后并发下正确。",
            "impl": "合适结构；并发用 CHM；迭代时防 CME。",
            "principle": "扰动 hash；树化阈值；fail-fast vs weakly-consistent。",
            "substance": "CME/丢数据=0。",
            "floor_title": "HashMap putVal",
            "structure": "数组+链表/红黑树；扩容 rehash；阈值 loadFactor。",
            "source_path": "HashMap.putVal/treeifyBin/resize；CHM.putVal/transfer。",
            "online": "多线程普通 HashMap 死循环/丢数据（历史）；今仍可能丢。",
            "verify": "并发单测；size 监控。",
            "mermaid_id": "diag-ency-j-col",
            "mermaid_code": """flowchart TD
  Put[put] --> Idx[计算下标]
  Idx --> Empty{空?}
  Empty -->|是| Place[放入]
  Empty -->|否| Coll[链/树]
  Place --> Resize{超阈值?}
  Resize -->|是| Grow[扩容迁移]
""",
            "today_html": "<ul><li>共享 Map 用 CHM；迭代用 keySet 视图小心删除。</li></ul>",
            "qas": [("【源码】为何树化？", ["防哈希攻击退化 O(n)。", "安全。", "只背红黑树。", "讲阈值。", "「树化抗碰撞。」"], "ency-j-col-q1")],
            "reflect_id": "ency-j-col-r1",
            "koujue_txt": "集合口诀：单线程 HashMap，并发 CHM，迭代防 CME。",
        }),
        ("ency-j-io", "ENCY-J · IO/NIO/Netty", "ENCY-J-IO", "IO / NIO / Netty 事件驱动", {
            "plain_txt": "比喻：BIO 一客一侍者；NIO 一个侍者盯很多铃；Netty 把铃系统工程化。",
            "biz": "网关/RPC/MQ 客户端别堵死支付线程。",
            "impl": "业务线程与 EventLoop 分离；禁在 EventLoop 重计算。",
            "principle": "Selector；Channel；Pipeline；池化 ByteBuf。",
            "substance": "连接泄漏=0；入站延迟。",
            "floor_title": "Netty Pipeline",
            "structure": "Boss 接连 Worker 读写；Handler 链入站出站。",
            "source_path": "NioEventLoop.run；AbstractChannel；ByteBuf 引用计数。",
            "online": "ByteBuf 泄漏；在 EventLoop 调外部 HTTP。",
            "verify": "ResourceLeakDetector；EventLoop 延迟。",
            "mermaid_id": "diag-ency-j-io",
            "mermaid_code": """flowchart LR
  Boss[Boss EventLoop] --> Worker[Worker]
  Worker --> Pipe[Pipeline Handlers]
  Pipe --> Biz[业务线程池]
""",
            "today_html": "<ul><li>RPC 超时&lt;Tomcat 线程等待；Direct 内存限额。</li></ul>",
            "qas": [("【泄漏】Netty 直接内存涨？", ["未 release ByteBuf；查 leak 日志。", "网关。", "只加堆。", "引用计数。", "「Buf 要放生。」"], "ency-j-io-q1")],
            "reflect_id": "ency-j-io-r1",
            "koujue_txt": "IO 口诀：EventLoop 要轻，业务丢池里。",
        }),
        ("ency-j-cl", "ENCY-J · 类加载", "ENCY-J-CL", "类加载 / 双亲委派 / 热部署边界", {
            "plain_txt": "比喻：双亲委派像「先问老师傅有没有这门手艺」——避免核心类被替换。",
            "biz": "插件/SPI 不污染主干；版本冲突可定位。",
            "impl": "理解 classpath；排依赖；禁随意自定义打破委派除非 OSGi/插件框架。",
            "principle": "加载-链接-初始化；委派模型；线程上下文类加载器 SPI 例外。",
            "substance": "NoClassDef/冲突可解释。",
            "floor_title": "双亲委派",
            "structure": "Bootstrap→Ext/Platform→App；findClass。",
            "source_path": "ClassLoader.loadClass；ServiceLoader。",
            "online": "fat jar 依赖冲突；热部署 Metaspace 胀。",
            "verify": "jcmd VM.classloaders；依赖树。",
            "mermaid_id": "diag-ency-j-cl",
            "mermaid_code": """flowchart TD
  App[AppCL] -->|委派| Plat[Platform]
  Plat --> Boot[Bootstrap]
  Boot -->|无| Plat2[尝试加载]
  Plat2 --> App2[App加载]
""",
            "today_html": "<ul><li>订单服务禁热部署生产；SPI 用 ServiceLoader 规范。</li></ul>",
            "qas": [("【冲突】两个日志实现？", ["排依赖+桥接；统一 slf4j。", "启动。", "都留下来。", "dependency:tree。", "「日志只留一家。」"], "ency-j-cl-q1")],
            "reflect_id": "ency-j-cl-r1",
            "koujue_txt": "类加载口诀：委派保核心，冲突看树。",
        }),
        ("ency-j-spi", "ENCY-J · SPI扩展", "ENCY-J-SPI", "SPI 与扩展点（JDK / Spring / Dubbo 思维）", {
            "plain_txt": "人话：SPI 是「定义插座，别人插实现」——支付渠道适配器就靠它。",
            "biz": "新渠道/新物流不改核心编译。",
            "impl": "接口+META-INF/services 或 Spring factories；策略注入。",
            "principle": "开放封闭；服务发现；类加载 TCCL。",
            "substance": "扩展上线无改核。",
            "mermaid_id": "diag-ency-j-spi",
            "mermaid_code": """flowchart TD
  API[扩展接口] --> Loader[ServiceLoader/Spring]
  Loader --> ImplA[渠道A]
  Loader --> ImplB[渠道B]
  Core[核心流程] --> API
""",
            "today_html": "<ul><li>支付渠道路由用策略+SPI；配置开关。</li></ul>",
            "qas": [("【设计】如何加新支付渠道？", ["实现接口+注册+路由配置；核心编排不动。", "支付。", "改 if-else 核心。", "SPI。", "「插座式加渠道。」"], "ency-j-spi-q1")],
            "reflect_id": "ency-j-spi-r1",
            "koujue_txt": "SPI 口诀：接口稳定，实现可插拔。",
        }),
        ("ency-j-log", "ENCY-J · 异常与日志", "ENCY-J-LOG", "异常体系与结构化日志", {
            "plain_txt": "比喻：异常是火警，日志是黑匣子；级别乱喊会狼来了。",
            "biz": "线上可定位资损与超时；审计可追溯。",
            "impl": "业务异常 vs 系统异常；JSON 日志+traceId；敏感脱敏。",
            "principle": "异常成本；吞异常危险；MDC 传递。",
            "substance": "MTTR；日志量成本。",
            "mermaid_id": "diag-ency-j-log",
            "mermaid_code": """flowchart TD
  Req[请求] --> MDC[注入traceId]
  MDC --> Biz[业务]
  Biz -->|业务错| Warn[warn+错误码]
  Biz -->|系统错| Err[error+栈]
""",
            "today_html": "<ul><li>支付回调日志含 trade_no；禁打卡号明文。</li></ul>",
            "qas": [("【坑】catch Exception 空？", ["丢根因。至少打 error+指标。", "线上。", "吞。", "统一处理。", "「别空 catch。」"], "ency-j-log-q1")],
            "reflect_id": "ency-j-log-r1",
            "koujue_txt": "日志口诀：有 trace，分级别，敏脱敏。",
        }),
        ("ency-j-jdk", "ENCY-J · JDK新特性", "ENCY-J-JDK", "JDK 新特性实用（8→21）", {
            "plain_txt": "人话：新特性不是追新潮——Stream/Optional/Record/虚拟线程看订单场景值不值。",
            "biz": "提效可读；虚拟线程慎用于已有池模型。",
            "impl": "常用：Optional 边界、Record DTO、Switch 模式、Text block SQL。",
            "principle": "虚拟线程：多阻塞友好；别和 synchronized 钉死载体线程。",
            "substance": "可读性/性能收益可测。",
            "mermaid_id": "diag-ency-j-jdk",
            "mermaid_code": """flowchart LR
  J8[Stream/Optional] --> J11[HTTP Client]
  J11 --> J17[Record/Sealed]
  J17 --> J21[VirtualThread]
""",
            "today_html": "<ul><li>支付回调别贸然全体虚拟线程；先压测。</li></ul>",
            "qas": [("【虚拟线程】适合支付回调吗？", ["若大量阻塞 IO 可试；与老线程池混用要隔离评估。", "并发。", "一键替换。", "压测。", "「先测再换。」"], "ency-j-jdk-q1")],
            "reflect_id": "ency-j-jdk-r1",
            "koujue_txt": "JDK 口诀：实用优先，虚拟线程先压测。",
        }),
        ("ency-j-jdbc", "ENCY-J · JDBC连接池", "ENCY-J-JDBC", "JDBC 与连接池（Hikari）", {
            "plain_txt": "比喻：连接池是出租柜台——租完要还，不还就假性打满。",
            "biz": "支付库连接不打满；泄漏可发现。",
            "impl": "Hikari 尺寸公式；leakDetection；超时。",
            "principle": "连接=会话；池耗尽=线程等待。",
            "substance": "获取连接 P99；泄漏告警。",
            "floor_title": "池耗尽链路",
            "structure": "getConnection 阻塞→业务线程堆积→Tomcat 打满。",
            "source_path": "HikariPool.getConnection；JDBC 事务 autoCommit。",
            "online": "未关 ResultSet/连接；长事务占连接。",
            "verify": "Hikari 指标 active/pending。",
            "mermaid_id": "diag-ency-j-jdbc",
            "mermaid_code": """flowchart TD
  Req[请求] --> Borrow[借连接]
  Borrow --> SQL[执行]
  SQL --> Return[归还]
  Borrow --> Wait[池满等待]
""",
            "conf_title": "Hikari 起步",
            "conf_code": "spring.datasource.hikari.maximum-pool-size=20\nspring.datasource.hikari.leak-detection-threshold=20000",
            "today_html": "<ul><li>短事务；try-with-resources。</li></ul>",
            "qas": [("【打满】active=max pending 飙升？", ["查慢 SQL/泄漏/下游锁。", "支付库。", "盲目加池。", "先找占连者。", "「池是镜子不是药。」"], "ency-j-jdbc-q1")],
            "reflect_id": "ency-j-jdbc-r1",
            "koujue_txt": "连接池口诀：借还成对，池大小跟数据库能力。",
        }),
        ("ency-j-orm", "ENCY-J · MyBatis/JPA", "ENCY-J-ORM", "MyBatis / JPA 本质与坑", {
            "plain_txt": "比喻：MyBatis 是「SQL 仍在你手」；JPA 是「对象世界映射」——订单复杂查询别迷信一种。",
            "biz": "订单读写正确；N+1 不拖垮列表。",
            "impl": "写用明确 SQL/Repository；读复杂走自定义查询或 CQRS。",
            "principle": "一级缓存/会话；脏检查；延迟加载陷阱。",
            "substance": "N+1 消除；更新行数校验。",
            "mermaid_id": "diag-ency-j-orm",
            "mermaid_code": """flowchart TD
  App[应用] --> MB[MyBatis Mapper]
  App --> JPA[EntityManager]
  MB --> SQL[可控SQL]
  JPA --> Gen[生成SQL/脏检查]
""",
            "today_html": "<ul><li>支付更新用条件 SQL 校验 rowcount。</li><li>列表禁懒加载风暴。</li></ul>",
            "qas": [("【N+1】售后列表慢？", ["改 join/fetch 或一次查明细。", "列表。", "开懒加载。", "批查。", "「列表先看 SQL 条数。」"], "ency-j-orm-q1")],
            "reflect_id": "ency-j-orm-r1",
            "koujue_txt": "ORM 口诀：写要可控，读防 N+1。",
        }),
        ("ency-j-spring", "ENCY-J · Spring全家桶", "ENCY-J-SPRING", "Spring：IoC / AOP / 事务 / Boot / Cloud 底板", {
            "plain_txt": "交叉 T2：这里掀事务代理与循环依赖、配置刷新边界。",
            "biz": "事务边界正确；配置变更不误伤支付。",
            "impl": "声明式事务理解代理；自调用失效；Cloud 组件按需。",
            "principle": "三级缓存解循环；Bean 生命周期；AOP 链。",
            "substance": "事务失效事故=0。",
            "floor_title": "事务代理失效",
            "structure": "同类自调用不走代理；private/final 难代理。",
            "source_path": "AnnotationTransactionAttributeSource；AbstractPlatformTransactionManager。",
            "online": "售后服务自调用导致未开事务双写。",
            "verify": "集成测试断言回滚。",
            "mermaid_id": "diag-ency-j-spring",
            "mermaid_code": """flowchart TD
  Ctrl[Controller] --> Proxy[事务代理]
  Proxy --> Svc[Service]
  Svc -->|自调用| Svc
  note1[自调用绕过代理]:::n
  classDef n fill:#333,color:#fff
""",
            "today_html": "<ul><li>事务方法拆到另一 Bean；只读事务标 clear。</li></ul>",
            "qas": [("【失效】@Transactional 不回滚？", ["查自调用/异常类型/传播。", "资损。", "怪数据库。", "测回滚。", "「先怀疑代理。」"], "ency-j-spring-q1")],
            "reflect_id": "ency-j-spring-r1",
            "koujue_txt": "Spring 口诀：事务看代理，配置看刷新面。",
        }),
        ("ency-j-test", "ENCY-J · 测试", "ENCY-J-TEST", "测试：JUnit5 / Mockito / Testcontainers", {
            "plain_txt": "人话：单测钉逻辑，容器测钉协议——支付幂等必须有自动化。",
            "biz": "防回归资损；重构敢动。",
            "impl": "金字塔；关键路径 Testcontainers MySQL/Redis/MQ。",
            "principle": "测试替身；契约测试；时间可注入。",
            "substance": "关键用例覆盖；CI 红灯即停。",
            "mermaid_id": "diag-ency-j-test",
            "mermaid_code": """flowchart TD
  Unit[单测纯逻辑] --> Slice[切片Web/Data]
  Slice --> IT[Testcontainers集成]
  IT --> CI[流水线门禁]
""",
            "today_html": "<ul><li>支付幂等、分摊、售后状态机必有 IT。</li></ul>",
            "qas": [("【测】如何测回调重复？", ["同 trade_no 打两次断言一次履约。", "支付。", "只测快乐路径。", "重复用例。", "「重复回调必测。」"], "ency-j-test-q1")],
            "reflect_id": "ency-j-test-r1",
            "koujue_txt": "测试口诀：关键路径容器化，重复与失败都要测。",
        }),
        ("ency-j-sec", "ENCY-J · 安全JWT/OAuth2", "ENCY-J-SEC", "安全：JWT / OAuth2 / 网关鉴权落地", {
            "plain_txt": "比喻：JWT 是盖章通行证；OAuth2 是「谁授权你拿什么章」。",
            "biz": "越权=0；代币泄露可吊销/短 TTL。",
            "impl": "网关验签；服务内鉴权注解；刷新令牌轮转。",
            "principle": "JWT 无状态 vs 黑名单；scope/audience；PKCE。",
            "substance": "越权扫描；代币泄露响应。",
            "mermaid_id": "diag-ency-j-sec",
            "mermaid_code": """sequenceDiagram
  participant C as 客户端
  participant G as 网关
  participant A as 授权服务器
  participant S as 订单服务
  C->>A: 登录/授权
  A-->>C: Access Token
  C->>G: 请求+JWT
  G->>S: 验签后转发
""",
            "today_html": "<ul><li>订单接口强制 userId 与资源归属校验。</li><li>管理端与用户端 audience 分离。</li></ul>",
            "qas": [("【越权】只改 orderId 看别人单？", ["服务端归属校验；禁信客户端 userId。", "安全。", "只验登录。", "IDOR 防护。", "「登录≠授权。」"], "ency-j-sec-q1")],
            "reflect_id": "ency-j-sec-r1",
            "koujue_txt": "安全口诀：验签+鉴权+归属，三者缺一不可。",
        }),
        ("ency-j-perf", "ENCY-J · 性能工程", "ENCY-J-PERF", "性能：压测 / 火焰图 / 容量", {
            "plain_txt": "交叉 T13：百科强调「指标-瓶颈-改动-回归」闭环。",
            "biz": "大促容量有数；瓶颈可解释。",
            "impl": "压测模型；火焰图；Little's Law 估线程。",
            "principle": "先度量再优化；避免过早优化。",
            "substance": "目标 QPS/P99 达标；回归基线。",
            "mermaid_id": "diag-ency-j-perf",
            "mermaid_code": """flowchart TD
  Goal[目标SLO] --> Load[压测]
  Load --> Prof[剖析火焰图]
  Prof --> Fix[优化]
  Fix --> Load
""",
            "today_html": "<ul><li>支付链路单独压；含回调与 DB。</li></ul>",
            "qas": [("【容量】如何估回调线程？", ["QPS×RT≈并发；加冗余与拒绝对策。", "大促。", "拍脑袋。", "Little's Law。", "「并发=QPS×RT。」"], "ency-j-perf-q1")],
            "reflect_id": "ency-j-perf-r1",
            "koujue_txt": "性能口诀：先测后改，改完再测。",
        }),
    ]
    for sid, toc, sys_id, title, kw in topics:
        kw.setdefault("spine_pos", "Java 底板挂支付/售后服务实现。")
        kw.setdefault("serves", "交易工程")
        kw.setdefault("back", "T-Found-X / T1/T2 → 本叶")
        parts.append(sec(sid, toc, sys_id, title, deep(**kw)))
    return "\n".join(parts)
