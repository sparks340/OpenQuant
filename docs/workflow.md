# Workflow

> Workflow for `OpenQuant`

## Delivery Workflow

### Phase 1: Foundation

- 建立目录结构
- 建立基础配置与日志
- 建立服务入口骨架
- 建立开发记录机制

### Phase 2: Domain

- 定义因子、任务、报告、策略、订单、持仓等领域对象
- 收口所有状态枚举与基础模型

### Phase 3: Data

- 接入数据源
- 清洗行情与基础因子
- 建立统一仓储接口

### Phase 4: Research

- 实现因子引擎
- 实现分析引擎
- 接入研究任务 Worker

### Phase 5: Strategy and Trading

- 实现信号和组合层
- 接入仿真交易
- 接入实盘交易
- 加入风控和监控

## Change Rule

每一阶段都必须完成以下动作：

1. 更新 `docs/development-log.md`
2. 在代码中写清楚模块边界注释
3. 不跳过测试入口和健康检查
4. 每次变更都尽量保持仓库可运行
