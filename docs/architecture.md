# OpenQuant Architecture

## 分层原则

1. **接入层（apps）**：只负责协议接入、参数校验、鉴权、调用应用服务。
2. **领域层（packages/domain）**：沉淀业务语义与领域规则，不依赖 Web/DB 细节。
3. **能力层（engines）**：因子、分析、组合、风控、交易等能力模块化。
4. **适配层（adapters）**：数据源、券商接口隔离。
5. **基础设施层（core/datastore/task）**：配置、日志、数据访问、任务编排。

## 服务边界

- `api_service`：统一 API 网关。
- `research_worker`：研究计算执行器。
- `trading_worker`：交易执行器。
- `scheduler_service`：定时任务调度器。
- `llm_service`：助手服务。
- `web_app`：前端应用。

## 关键约束

- API 不承载核心计算。
- 业务代码不得散写数据库查询，统一走 repository。
- 订单发往券商前必须通过 `risk_engine`。
- 研究输出（因子/信号）经 `portfolio_engine` 转换为交易意图。

## 现状

本次重构完成目录结构与占位模块搭建，为后续逐模块填充实现提供稳定边界。
