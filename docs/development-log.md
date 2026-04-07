# Development Log

## 2026-04-07（重构后工作流重设计）

### 背景

上一版提交完成了目录重排，但存在两个问题：
1. 占位模块多、落地路径不清晰；
2. 没有按“最小闭环”组织推进顺序。

因此本次对交付流程做了**重新设计与完整记录**。

### 本次变更

- 重写 `docs/workflow.md`，改为严格分阶段顺序：
  `core -> domain -> datastore -> datahub -> factor_engine -> analysis_engine -> api_service -> task_engine+research_worker -> portfolio_engine -> risk_engine -> broker_adapters/simulator -> trading_engine+trading_worker -> 真实券商 -> llm+web`。
- 将 `MVP 最小闭环` 明确为 7 个可验收步骤：
  数据入库、创建因子、运行因子、生成回测报告、生成调仓计划、模拟下单、查询订单/持仓/账户。
- 增加每阶段统一记录模板，确保后续提交可以审计与回放。

### 当前阶段状态盘点

| 阶段 | 状态 | 说明 |
|---|---|---|
| core | 进行中 | 目录存在，待补全 settings/logging/exception 细节实现 |
| domain | 未开始 | 仅骨架，缺实体不变量和规则测试 |
| datastore | 未开始 | 需完成 repository + UoW 可用实现 |
| datahub | 未开始 | 需完成数据同步与清洗最小链路 |
| factor_engine | 未开始 | 需先完成最小算子和执行器 |
| analysis_engine | 未开始 | 需完成最小指标和报告产物 |
| api_service | 进行中 | 仅 health + root，业务路由未实现 |
| task_engine + research_worker | 未开始 | 任务流转未落地 |
| portfolio_engine | 未开始 | 仓位与订单意图未实现 |
| risk_engine | 未开始 | 风控规则未实现 |
| broker simulator | 未开始 | 模拟撮合未实现 |
| trading_engine + trading_worker | 未开始 | 交易主流程未实现 |
| 真实券商 | 未开始 | 依赖模拟链路稳定后接入 |
| llm + web | 未开始 | 放在最后收口 |

### 下一步执行计划（按优先级）

1. 完成 `core` 可用实现（配置、日志、异常、基础模型）并补单测。
2. 落地 `domain + datastore` 最小可用版本（因子定义/版本/运行记录仓储）。
3. 打通 `datahub -> factor_engine -> analysis_engine` 的研究链路。
4. 通过 `task_engine + research_worker` 异步化研究任务。
5. 完成 `portfolio/risk/simulator/trading`，跑通 MVP 闭环。

### 风险与约束

- 当前仓库仍以骨架为主，业务功能未可用。
- 需要优先控制“跨层直接依赖”风险，避免重新耦合为大模块。
- 建议每个 phase 都以可执行测试和示例脚本作为退出条件。

---

## 历史记录（保留）

### 2026-04-07（Phase 1 初始骨架）

- 建立 `apps/`、`packages/`、`docs/`、`tests/` 结构
- 初始化服务骨架和若干基础包
- 完成最初版架构说明与工作流文档
