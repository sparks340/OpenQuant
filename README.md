# OpenQuant

OpenQuant 已按“应用层 + 领域层 + 引擎层 + 适配层 + 基础设施层”的目标架构完成一次目录级重构。

## 新架构总览

- `apps/api_service`: 统一 HTTP 接入层（仅做鉴权、校验、编排）。
- `apps/research_worker`: 因子计算、回测分析等研究类异步执行器。
- `apps/trading_worker`: 调仓、下单、订单/持仓/账户同步执行器。
- `apps/scheduler_service`: 定时调度服务（行情同步、因子刷新、维护任务）。
- `apps/llm_service`: LLM 助手服务，独立部署、独立限流。
- `apps/web_app`: 前端源码与页面骨架。

## 包结构

- `packages/core`: 配置、日志、枚举、异常、通用模型。
- `packages/domain`: `research/strategy/trading/platform` 四个子域。
- `packages/datastore`: Mongo/Redis、Repository、UoW。
- `packages/datahub`: 数据接入、清洗、标准化与落库。
- `packages/factor_engine`: 因子校验、解析、执行和算子。
- `packages/analysis_engine`: 回测分析指标、图表和报告。
- `packages/portfolio_engine`: 仓位生成与订单意图构建。
- `packages/risk_engine`: 下单前统一风控规则。
- `packages/trading_engine`: 交易执行主流程编排。
- `packages/broker_adapters`: 模拟与实盘券商适配。
- `packages/task_engine`: 任务投递、状态流转、日志追踪。
- `packages/sdk`: 对外脚本/策略调用 SDK。

## 运行示例

```bash
uvicorn apps.api_service.api_service.main:app --reload
python -m apps.research_worker.research_worker.main
python -m apps.trading_worker.trading_worker.main
```

## 说明

当前提交重点是**目录与模块边界重构**，多数模块仍为占位实现，后续将按文档逐步补齐业务逻辑。


## 迭代执行顺序（最新）

详细执行顺序见 `docs/workflow.md`，按以下顺序推进：
`core -> domain -> datastore -> datahub -> factor_engine -> analysis_engine -> api_service -> task_engine+research_worker -> portfolio_engine -> risk_engine -> simulator -> trading_engine+trading_worker -> real broker -> llm+web`。

MVP 闭环目标：数据入库 → 因子创建/运行 → 回测报告 → 调仓计划 → 模拟下单 → 订单/持仓/账户查询。
