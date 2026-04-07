# Development Log

> 目标：记录 OpenQuant 按 `docs/workflow.md` 推进的阶段进展，保证每次提交可追溯。

## 当前快照（截至 2026-04-07）

| 阶段 | 状态 | 备注 |
|---|---|---|
| core | 进行中 | 基础配置/日志/异常/模型已完成最小实现，后续继续细化 |
| domain | 未开始 | 待补实体不变量与纯领域测试 |
| datastore | 未开始 | 待补 repository + UoW 可用实现 |
| datahub | 未开始 | 待打通数据同步与清洗最小链路 |
| factor_engine | 未开始 | 待补最小算子与执行器 |
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

1. 启动 `domain` 阶段：先补 research/trading 核心实体不变量测试。
2. 并行设计 `datastore` repository 接口契约，确保不向业务层泄漏查询细节。
3. 打通 `datahub -> factor_engine -> analysis_engine` 的研究链路。
4. 通过 `task_engine + research_worker` 异步化研究任务。
5. 完成 `portfolio/risk/simulator/trading`，跑通 MVP 闭环。

## 风险与约束

- 仓库当前仍以骨架为主，业务功能尚未完全可用。
- 需严格控制跨层直接依赖，避免再次耦合为大模块。
- 建议每个 Phase 以“可执行测试 + 示例脚本”作为退出条件。

---

## 变更记录（按时间倒序）

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
