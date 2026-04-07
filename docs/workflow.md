# Workflow

> OpenQuant 迭代工作流（重排版）

## 0. 目标

本工作流用于把当前“目录骨架”推进为可运行的端到端交易研究平台。

- **先做最小闭环（MVP）**：
  1) 数据入库
  2) 创建因子
  3) 运行因子
  4) 生成回测报告
  5) 由因子结果生成调仓计划
  6) 用模拟券商下单
  7) 查看订单/持仓/账户
- **再做增强能力**：真实券商适配、LLM、完整前端。

## 1. 分阶段顺序（必须按序）

### Phase A: core

**范围**
- `packages/core`

**交付**
- Settings 基类（环境切分、配置加载）
- Logger/Audit 工具
- 基础异常体系（base/domain/infra）
- 通用模型与枚举

**验收**
- 单测覆盖配置读取、日志格式与异常基类
- 所有其他包仅依赖 core 的公共接口

---

### Phase B: domain

**范围**
- `packages/domain`

**交付**
- research/strategy/trading/platform 四子域实体、值对象、领域服务
- 状态流转约束（如订单状态、任务状态）

**验收**
- 纯领域单测（不依赖数据库/HTTP）
- 关键业务规则有明确不变量（invariant）校验

---

### Phase C: datastore

**范围**
- `packages/datastore`

**交付**
- Mongo/Redis 客户端管理
- Repository 接口与实现
- Unit of Work
- 索引初始化脚本

**验收**
- integration test 覆盖 repository CRUD + 查询
- 禁止业务层直接写裸 Mongo 查询

---

### Phase D: datahub

**范围**
- `packages/datahub`

**交付**
- 数据源适配器（先 CSV/Tushare，其他可 stub）
- 行情/标的/基础因子清洗
- 标准化后落库

**验收**
- `sync_*` 服务可将样例数据写入 datastore
- 数据字段映射和时间/代码格式统一

---

### Phase E: factor_engine

**范围**
- `packages/factor_engine`

**交付**
- 公式模式与 Python 模式校验/执行
- 最小算子集（RANK/DELAY/TS_MEAN）
- 因子结果统一模型（factor_frame）

**验收**
- 单测覆盖表达式校验与执行
- 输入行情 -> 输出因子值（可复现）

---

### Phase F: analysis_engine

**范围**
- `packages/analysis_engine`

**交付**
- 去极值、标准化、分组收益、IC
- 最小报告构造（json）

**验收**
- 因子值 + 行情 -> 报告产出成功
- 指标计算有 deterministic 测试

---

### Phase G: api_service

**范围**
- `apps/api_service`

**交付**
- 因子创建/运行、报告查询、交易查询 API
- 统一响应模型与错误码

**验收**
- OpenAPI 可访问
- API 层不做核心业务计算，只做编排

---

### Phase H: task_engine + research_worker

**范围**
- `packages/task_engine`
- `apps/research_worker`

**交付**
- 任务投递、消费、状态追踪、分段日志
- 因子计算与回测任务异步化

**验收**
- 提交任务后可观测状态流转（PENDING/RUNNING/SUCCEEDED/FAILED）

---

### Phase I: portfolio_engine

**范围**
- `packages/portfolio_engine`

**交付**
- 因子分数 -> 目标仓位
- 目标仓位 -> 订单意图

**验收**
- 给定资金规模与信号，输出稳定可解释的调仓计划

---

### Phase J: risk_engine

**范围**
- `packages/risk_engine`

**交付**
- 最小风控规则：单票上限、现金保留、黑名单

**验收**
- 每条订单意图均有风控判定结果

---

### Phase K: broker_adapters/simulator

**范围**
- `packages/broker_adapters/simulator.py`

**交付**
- 模拟撮合、订单状态推进、持仓/账户更新

**验收**
- 可跑通“下单->成交->账户与持仓变化”

---

### Phase L: trading_engine + trading_worker

**范围**
- `packages/trading_engine`
- `apps/trading_worker`

**交付**
- 交易执行主流程：接收订单意图 -> 风控 -> 券商路由 -> 状态回写
- 定时同步账户/订单/成交

**验收**
- MVP 闭环可完整跑通

---

### Phase M: 真实券商适配

**范围**
- `packages/broker_adapters/xtquant_broker.py`（先）
- 其他真实券商后续扩展

**交付**
- 与统一接口兼容的真实下单/查询

**验收**
- 在仿真与实盘之间可平滑切换

---

### Phase N: llm_service + 完整前端

**范围**
- `apps/llm_service`
- `apps/web_app`

**交付**
- 助手路由、提示词管理、会话落库
- 因子编辑/报告/交易看板完整页面

**验收**
- 前后端联调通过，关键用户路径可演示

## 2. MVP 最小闭环 Definition of Done

满足以下 7 步即视为 MVP 完成：
1. 数据入库成功（可查询）
2. 可创建因子定义与版本
3. 可触发并完成一次因子运行
4. 可生成并查询回测报告
5. 可生成调仓计划
6. 可通过模拟券商完成下单/成交
7. 可查询订单、持仓、账户结果

## 3. 每阶段统一记录规范

每完成一个 phase，必须同步更新 `docs/development-log.md`，固定包含：
- 目标与范围
- 代码变更清单（模块级）
- 测试与结果
- 风险与遗留问题
- 下一阶段输入条件
