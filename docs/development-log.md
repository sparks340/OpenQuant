# Development Log

> 目标：记录 OpenQuant 按 `docs/workflow.md` 推进的阶段进展，保证每次提交可追溯。

## 当前快照（截至 2026-04-08）

| 阶段 | 状态 | 备注 |
|---|---|---|
| core | 进行中 | 基础配置/日志/异常/模型已完成最小实现，后续继续细化 |
| domain | 已完成 | research/strategy/trading/platform 四子域实体、值对象、领域服务已形成最小闭环并具备纯领域测试覆盖 |
| datastore | 已完成 | Mongo/Redis 客户端管理、Repository 与 UoW 已补齐，含 CRUD+查询 integration tests |
| datahub | 已完成 | 已落地 CSV/Tushare(Stub) 适配、清洗与标准化入库链路，含 integration tests |
| factor_engine | 已完成 | 已实现公式校验/执行与最小算子集（RANK/DELAY/TS_MEAN），含可复现单测 |
| analysis_engine | 未开始 | 待补最小指标与报告产物 |
| api_service | 进行中 | 目前仅 health/root，业务路由待实现 |
| task_engine + research_worker | 未开始 | 任务流转未落地 |
| portfolio_engine | 未开始 | 仓位与订单意图未实现 |
| risk_engine | 未开始 | 风控规则未实现 |
| broker simulator | 未开始 | 模拟撮合未实现 |
| trading_engine + trading_worker | 未开始 | 交易主流程未实现 |
| 真实券商 | 未开始 | 依赖模拟链路稳定后接入 |
| llm + web | 未开始 | 最后收口 |

## 下一步（按优先级）

1. 进入 `analysis_engine` 阶段：补齐最小指标与报告产物。
2. 通过 `task_engine + research_worker` 异步化研究任务。
3. 完成 `portfolio/risk/simulator/trading`，跑通 MVP 闭环。

## 风险与约束

- 仓库当前仍以骨架为主，业务功能尚未完全可用。
- 需严格控制跨层直接依赖，避免再次耦合为大模块。
- 建议每个 Phase 以“可执行测试 + 示例脚本”作为退出条件。

## 历史 Review 风险台账（截至 2026-04-08）

> 目的：集中记录历次评审中识别的风险点，避免分散在对话中丢失。

1. **Domain 建模深度风险（Phase B）**
   - 当前不少实体/服务仍为 MVP 级最小实现，字段语义与边界规则可能在后续阶段继续收敛。
   - `task_type`、`TaskLogLevel` 等字符串/枚举存在跨系统映射风险，后续接入外部服务时需统一映射表。
   - `sequence` 仅校验正数，跨进程并发时的单调递增约束尚未在持久层保证。

2. **Datastore 落地风险（Phase C）**
   - 当前 Mongo/Redis 客户端为 in-memory 实现，与真实后端在索引行为、查询性能、事务语义上存在差异。
   - `MongoUnitOfWork` 回滚基于 snapshot/restore，适用于本地测试，不等价于真实数据库事务。
   - 进入真实持久层时需重点验证 repository 边界不被业务层绕过（禁止裸查询回流到业务代码）。

3. **Datahub 数据质量风险（Phase D）**
   - `TushareDataAdapter` 仍是 stub，真实接入前缺少鉴权、限流、失败重试与监控。
   - 清洗规则当前主要覆盖 symbol/date/数值标准化，尚未系统覆盖停牌、复权、缺失交易日等边界场景。

4. **Factor Engine 扩展风险（Phase E）**
   - 公式解析器目前仅支持 MVP 单层表达式，复杂嵌套表达式与错误定位能力不足。
   - `python_executor` 仅提供最小校验，尚未具备真正沙箱执行的资源限制与安全隔离。
   - 算子集目前仅 `RANK/DELAY/TS_MEAN`，后续扩展需保证兼容性与回归测试稳定性。

---

## 变更记录（按时间倒序）

### 2026-04-08｜Phase E 完成：factor_engine 校验/执行/算子最小闭环

**本次变更**
- 先补测试：新增 `tests/unit/factor_engine/test_phase_e_factor_engine.py`，覆盖表达式校验、非法表达式拦截、`RANK/DELAY/TS_MEAN` 执行结果一致性。
- 补实现：完成 `FactorFrame/ValidationResult` 模型、`formula_parser`、`FormulaValidator`、`FormulaExecutor` 与 `FactorExecutorService`。
- 补实现：完成最小算子集 `RANK/DELAY/TS_MEAN`，并补齐 `python_executor` 最小校验与运行时上下文模型。
- 保持输出可复现：同一输入行情可稳定得到同一 `factor_frame`。

**阶段影响**
- Phase E 退出条件满足：表达式校验与执行具备单测覆盖，输入行情可产出可复现因子值。下一步进入 Phase F（analysis_engine）。

### 2026-04-08｜Phase D 完成：datahub 适配/清洗/入库最小链路

**本次变更**
- 先补测试：新增 `tests/integration/datahub/test_phase_d_datahub.py`，覆盖行情、标的、基础因子三条同步链路的清洗与落库行为。
- 补实现：完成 `CSVDataAdapter` 与 `TushareDataAdapter(stub)`，统一通过 `DataSourceAdapter` 协议输出原始行数据。
- 补实现：完成 `market/instrument/base_factor` cleaner 与 `symbol_mapper/trading_calendar` 工具，统一代码、日期、数值格式。
- 补实现：完成 `sync_market_data/sync_instruments/sync_base_factors` 服务，并补齐 `InMemoryInstrumentRepository` 作为标的入库承载。

**阶段影响**
- Phase D 退出条件满足：`sync_*` 服务可将样例数据清洗后写入 datastore，字段映射与代码/日期格式统一。下一步进入 Phase E（factor_engine）。

### 2026-04-08｜Phase C 完成：datastore 客户端/仓储/UoW 与集成测试闭环

**本次变更**
- 先补测试：新增 `tests/integration/datastore/test_datastore_phase_c.py`，覆盖 Mongo/Redis 客户端基本操作、索引初始化、repository CRUD+查询、UoW 异常回滚。
- 补实现：完成 `mongo.client/collections/indexes` 与 `redis.client` 最小可用实现，支持后续 datahub/task_engine 接入。
- 补实现：完成 `factor/task/market_data` repository in-memory 实现，并增强 `strategy/trading` repository snapshot/restore 能力。
- 补实现：扩展 `MongoUnitOfWork` 聚合 `factor/strategy/trading/task` 仓储，支持进入上下文时快照、异常路径回滚。

**阶段影响**
- Phase C 退出条件满足：repository CRUD+查询具备 integration test 覆盖，业务层可通过 repository/UoW 访问持久层边界。下一步进入 Phase D（datahub）。

### 2026-04-08｜Phase B 完成：domain 四子域最小闭环达成

**本次变更**
- 先补测试：新增 `tests/unit/domain/test_phase_b_entities_and_services.py`，覆盖 research/strategy/trading/platform 新增实体与服务的关键不变量与迁移规则。
- 补实现：清理 domain 中剩余 placeholder，补齐 platform（`User/ChatSession/TaskService`）、research（`FactorVersion/FactorValue/AnalysisReport` 与 domain services）、strategy（`StrategyDefinition/StrategyVersion/SignalService`）、trading（`Account/Position/Trade/BrokerConnection` 与 domain services）最小实现。
- 对齐状态约束：补齐 `StrategyVersion`、`BrokerConnection` 迁移规则与错误路径，保证领域层状态机可测试。
- 纯领域测试全量通过，形成不依赖数据库/HTTP 的可回归基线。

**阶段影响**
- Phase B 退出条件满足：domain 四子域具备实体/值对象/领域服务与关键不变量，且测试可执行。下一步可进入 Phase C（datastore）收敛。

### 2026-04-08｜Phase B 跟进：platform 任务日志实体不变量

**本次变更**
- 先补测试：新增 `tests/unit/domain/test_task_log.py`，覆盖日志级别规范化、创建时间默认值、身份/消息非空与序号正数约束。
- 补实现：新增 `TaskLogLevel(INFO/WARNING/ERROR)` 与 `TaskLog` 实体，实现 `task_id/message` 非空、`sequence>0`、`created_at` UTC 默认写入。
- 通过纯领域测试回归，确保 platform 子域日志对象可被后续 task_engine 直接复用。

**阶段影响**
- platform 子域除 `TaskRecord` 外新增可执行日志实体，任务追踪在 domain 层形成“状态 + 事件”双模型基础。

### 2026-04-08｜Phase B 修正：TaskRecord 构造语义与身份字段约束

**本次变更**
- 先补测试：新增 `TaskRecord` 创建时间自动生成与身份字段非空校验测试（TDD），用于约束任务记录初始语义。
- 补实现：`TaskRecord.created_at` 调整为构造时默认写入 UTC 时间，避免记录在首次迁移前缺失创建时间。
- 补实现：新增 `task_id/task_type` 非空校验，不允许空白标识进入领域模型。
- 保持生命周期不变量与迁移规则不变，继续通过纯领域单测回归。

**阶段影响**
- platform 子域任务实体从“可迁移”提升到“可审计（创建时间稳定）+ 可识别（身份字段必填）”，为后续 task_engine 任务追踪提供更稳输入。

### 2026-04-08｜Phase B 跟进：platform 任务生命周期不变量

**本次变更**
- 完成 `platform.task_record` 生命周期模型，补齐状态迁移约束（PENDING/RUNNING/SUCCESS/FAILED）与时间戳字段一致性校验。
- 约束失败态必须显式提供 `error_message`，成功态禁止携带错误信息，避免任务结果语义不清。
- 新增 `tests/unit/domain/test_task_record.py`，覆盖合法迁移、非法跳转与失败原因必填等规则。

**阶段影响**
- platform 子域开始具备可执行任务状态约束，可作为后续 `task_engine + research_worker` 状态机的领域基座。

### 2026-04-07｜Phase C 启动：repository 契约与 UoW 参考实现

**本次变更**
- 新增 `StrategyRepository/TradingRepository` 抽象契约与 `InMemory` 参考实现，用于约束业务层访问边界。
- 新增 `MongoUnitOfWork` 最小实现，提供 `strategy_repository`、`trading_repository` 聚合访问与 commit/rollback 生命周期。
- 新增 `tests/unit/datastore/test_repository_contracts.py`，覆盖 repository round-trip 与 UoW 提交行为。

**阶段影响**
- `datastore` 阶段进入“进行中”，已具备可测试的 repository + UoW 契约骨架，为后续 Mongo/Redis 真正接入铺路。

### 2026-04-07｜Phase B 扩展：strategy 信号到调仓计划服务

**本次变更**
- 完成 `Signal` 与 `TargetPosition` 实体最小实现，补齐标的标准化与分数/权重约束。
- 完成 `RebalanceService.build_plan`：支持按分数筛选正向信号、Top-N 截断与单票上限约束；新增迭代分配逻辑，确保上限约束在最终目标权重中仍然成立。
- 新增 `tests/unit/domain/test_rebalance_service.py`，覆盖正向建仓、无正信号拒绝、分数范围约束与单票上限生效。

**阶段影响**
- strategy 子域具备首个可执行 domain service，可直接支撑后续 `portfolio_engine` 输入生成。

### 2026-04-07｜Phase B 扩展：value object 首批落地

**本次变更**
- 完成 research 子域值对象：`FactorCode`（代码非空校验）与 `BacktestConfig`（日期区间与资金约束）。
- 完成 trading 子域值对象：`Money`（币种一致性与加减法约束）与 `OrderRequest`（下单参数与标的标准化）。
- 新增 `tests/unit/domain/test_value_objects.py`，覆盖构造校验与核心运算约束。

**阶段影响**
- 领域层开始具备“实体 + 值对象”双维约束能力，为后续 domain service 编排提供稳定输入边界。

### 2026-04-07｜Phase B 加固：失败原因显式化与调仓目标规范化

**本次变更**
- 将 `OrderStatus/OrderSide/FactorRunStatus` 提取到 `packages/core/core/enums`，避免在 domain 实体内重复定义。
- `FactorRun.transition_to(FAILED)` 调整为必须显式提供 `error_message`，禁止默认兜底文案，避免故障根因丢失。
- `RebalancePlan` 新增目标代码标准化（统一大写）与“权重必须为正数”约束，避免零权重噪音目标进入下游流程。
- 扩展纯领域单测，覆盖上述规则的正反场景。

**阶段影响**
- 研究与策略子域在错误可观测性和输入标准化方面更一致，可减少后续编排层分支处理复杂度。

### 2026-04-07｜Phase B 加固：构造态一致性校验

**本次变更**
- 为 `Order` 增加构造态一致性校验：`SUBMITTED/FILLED` 状态必须具备 `submitted_at`，`FILLED` 必须具备 `filled_at` 且时间先后合法。
- 为 `FactorRun` 增加构造态一致性校验：运行/结束态必须具备起止时间，`FAILED` 必须包含错误信息，`SUCCEEDED` 禁止携带错误信息。
- 扩展单测覆盖构造态非法输入（通过 `InvariantViolationError` 校验），并保持状态迁移单测通过。

**阶段影响**
- 领域对象在“构造时”和“迁移时”均具备约束，降低脏数据绕过迁移方法直接入模的风险。

### 2026-04-07｜Phase B 修正：订单状态迁移原子性

**本次变更**
- 修复 `Order.transition_to` 中 `FILLED` 校验时机，先校验 `submitted_at` 再写入状态，避免异常时状态被提前污染。
- 新增单测验证非法 `SUBMITTED -> FILLED`（缺少 `submitted_at`）时，订单状态保持不变。

**阶段影响**
- 领域实体状态迁移具备更好的原子性，减少异常路径下的数据不一致风险。

### 2026-04-07｜Phase B 跟进：统一领域异常与约束细化

**本次变更**
- 将 `order/factor_run/rebalance_plan` 的不变量报错统一为 `InvariantViolationError`，避免使用通用 `ValueError`。
- 增加 `rebalance_plan` 空目标校验，要求调仓计划至少包含一个标的。
- 增加 `factor_run` 非法状态跳转测试与 `rebalance_plan` 空目标测试，强化规则覆盖。

**阶段影响**
- 领域规则错误类型与跨层错误码语义对齐，便于 API 层后续统一映射。

### 2026-04-07｜Phase B 启动：domain 首批不变量落地

**本次变更**
- 为 `trading.order` 增加最小生命周期模型与状态迁移约束（PENDING/SUBMITTED/FILLED/CANCELED/REJECTED）。
- 为 `research.factor_run` 增加执行状态约束（PENDING/RUNNING/SUCCEEDED/FAILED）与时间戳管理。
- 为 `strategy.rebalance_plan` 增加调仓权重不变量校验（单票非负、总权重不超过 1.0）。
- 新增 `tests/unit/domain/test_domain_invariants.py`，覆盖上述领域规则，保持纯领域测试（不依赖数据库/HTTP）。

**阶段影响**
- `domain` 阶段进入“进行中”，已具备首批可执行不变量示例，后续补齐更多实体和值对象。

### 2026-04-07｜Phase A 执行：core 最小可用实现

**本次变更**
- 完成 `packages/core` 基础异常体系：`OpenQuantError` + `Domain/Infra` 分层异常及结构化序列化。
- 完成日志基础设施增强：统一日志格式、避免重复 handler、新增审计事件 `emit_audit_event`。
- 完成配置基础能力增强：`Settings` 增加环境枚举限制与 `get_settings()` 单例缓存。
- 增加 `CoreModel` 作为跨包统一基础模型配置。
- 新增 core 单元测试，覆盖配置读取、日志工厂行为、异常序列化。

**阶段影响**
- `core` 进入“最小可用”阶段，可支撑后续模块接入。

### 2026-04-07｜工作流重设计

**背景**
- 需要把工程直接拉回到“最小闭环优先”的交付节奏。
- 需要统一阶段记录格式，确保每次提交都可审计、可回放。

**本次变更**
- 重写 `docs/workflow.md`，明确 Phase A~N 严格顺序。
- 将 MVP 闭环明确为 7 步：数据入库、创建因子、运行因子、生成报告、生成调仓计划、模拟下单、查询结果。
- 增加每阶段统一记录模板，支持后续审计与回放。
