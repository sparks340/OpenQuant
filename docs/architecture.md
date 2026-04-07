# Architecture

> Project Name: `OpenQuant`

## Goal

`OpenQuant` 按“研究域”和“交易域”分离的方式构建，避免把因子、回测、策略、交易、风控全部堆在一个服务里。

## Service Layer

- `apps/api`: 对外提供 API
- `apps/research`: 执行因子与回测任务
- `apps/trading`: 执行调仓、下单和同步任务
- `apps/scheduler`: 调度定时任务
- `apps/llm`: 提供因子和交易助手能力

## Package Layer

- `core`: 配置、日志、基础模型、枚举
- `domain`: 领域对象和领域规则
- `datastore`: 仓储与数据访问
- `task_engine`: 统一任务分发与跟踪
- `sdk`: 外部脚本调用入口

## Delivery Strategy

项目按阶段推进：

1. 基础工程与目录搭建
2. 领域模型与仓储接口
3. 数据接入
4. 因子引擎
5. 分析引擎
6. 研究 API 与异步任务
7. 策略、组合、仿真交易
8. 实盘交易、风控与监控
