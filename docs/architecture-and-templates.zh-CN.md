# OpenQuant 架构与模板说明（中文）

## 1. 项目整体架构（分层）

OpenQuant 当前采用「应用层 + 领域层 + 能力层 + 适配层 + 基础设施层」的分层思路：

- 应用层（`apps/*`）负责接入协议、参数校验、鉴权与编排，不承载核心计算。
- 领域层（`packages/domain`）负责业务语义与规则。
- 能力层（若干 `*_engine`）负责因子、分析、组合、风控、交易等计算能力。
- 适配层（adapters）负责外部数据源与券商接口隔离。
- 基础设施层（`core/datastore/task`）负责配置、日志、数据访问与任务编排。

## 2. 应用层（apps）服务职责

- `api_service`：统一 HTTP 网关。
- `research_worker`：研究类异步执行（因子计算、回测）。
- `trading_worker`：交易执行与账户/订单/持仓同步。
- `scheduler_service`：定时任务编排（行情同步、策略再平衡、维护）。
- `llm_service`：LLM 助手服务。
- `web_app`：前端页面承载层。

## 3. 包（packages）能力分工

- `core`：配置、日志、通用异常、枚举与基础模型。
- `factor_engine`：因子校验、解析、执行与算子。
- `analysis_engine`：回测指标与报告生成。
- `trading_engine`：交易执行主流程编排。
- `task_engine`：任务投递、消费与状态追踪。
- `sdk`：对外脚本调用接口。

> 说明：仓库文档中还规划了 `portfolio_engine`、`risk_engine`、`broker_adapters` 等能力边界，作为后续迭代重点。

## 4. 关键架构约束（重要）

- API 层不做核心计算。
- 业务层不直接散写数据库查询，应走 repository。
- 下单前必须经过 `risk_engine`。
- 研究产出需先经 `portfolio_engine` 转为交易意图。

## 5. “模板”现状与功能定位

当前仓库是“目录边界优先”的重构阶段，许多模块仍是占位模板（placeholder），模板主要用于提前固定职责边界，便于后续并行开发。

### 5.1 前端页面模板（`apps/web_app/src/pages/*.tsx`）

以下页面文件目前为空模板（待填充），但按命名可对应未来功能：

- `FactorList.tsx`：因子列表与筛选。
- `FactorEditor.tsx`：因子创建/编辑（公式或 Python）。
- `AnalysisReport.tsx`：回测与分析报告展示。
- `StrategyList.tsx`：策略列表、状态与版本管理。
- `TradingDashboard.tsx`：交易总览看板（账户、风险、执行状态）。
- `Orders.tsx`：订单列表与状态跟踪。
- `Positions.tsx`：持仓查询与结构展示。
- `ChatAssistant.tsx`：LLM 助手交互页面。

### 5.2 调度模板（`scheduler_service/schedules/*.py`）

目前 `base_factor.py`、`market_data.py`、`strategy_rebalance.py`、`maintenance.py` 都是 placeholder。

- `base_factor.py`：预期承载“基础因子刷新/重算”调度。
- `market_data.py`：预期承载“行情拉取与入库”调度。
- `strategy_rebalance.py`：预期承载“策略定时再平衡与调仓触发”。
- `maintenance.py`：预期承载“系统维护类任务”（如清理、归档、健康巡检）。

### 5.3 API 路由模板（`api_service/routers/*.py`）

除 `health.py` 外，多数路由仍为 placeholder：

- `factors.py`：因子创建、运行、查询。
- `analysis.py`：分析任务提交与报告读取。
- `trading.py`：交易执行、订单/持仓/账户查询。
- `strategies.py`：策略 CRUD 与状态管理。
- `tasks.py`：异步任务状态查询。
- `data.py`：数据同步/查询入口。
- `chat.py`：LLM 助手会话入口。
- `auth.py`：鉴权认证。

## 6. 当前成熟度判断

- 该项目目前“架构边界清晰、业务实现待补齐”。
- 已有可运行最小入口（如 API 根路由和健康检查）。
- 研发主线是按 `docs/workflow.md` 的 Phase A~N 顺序逐步把模板填充为可运行模块，最终闭环到“研究 -> 调仓 -> 模拟下单 -> 查询结果”。
