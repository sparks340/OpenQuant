# OpenQuant

`OpenQuant` 是一个模块化的量化平台项目，目标是逐步落地以下能力：

- 数据接入与清洗
- 因子研究与回测分析
- 策略生成与调仓计划
- 仿真交易与实盘交易
- 风控、任务调度、前端和 LLM 助手

## 当前阶段

当前仓库已经完成第一阶段基础工程搭建：

- 建立 `apps/`、`packages/`、`docs/`、`tests/` 结构
- 初始化 `apps/api`、`apps/research`、`apps/trading`、`apps/scheduler`、`apps/llm`
- 建立核心配置、日志、基础模型和任务分发占位模块
- 补充架构文档、工作流文档和开发记录

## 服务目录

- `apps/api`
- `apps/research`
- `apps/trading`
- `apps/scheduler`
- `apps/llm`

## 目录约定

- `apps/`: 可独立运行的服务入口
- `packages/`: 领域能力与基础模块
- `docs/`: 架构、工作流、开发记录
- `tests/`: 单元测试和集成测试

## 启动开发环境

1. 创建虚拟环境并安装依赖
2. 复制 `.env.example` 为 `.env`
3. 启动 MongoDB 和 Redis
4. 运行 API 服务

```bash
uvicorn apps.api.api.main:app --reload
```

## 项目文档

- `docs/workflow.md`
- `docs/development-log.md`
- `docs/architecture.md`
- `docs/github-upload.md`

## 上传到自己的 GitHub

建议统一使用下面这套命名：

- 本地目录名：`openquant`
- GitHub 仓库名：`openquant` 或 `OpenQuant`
- 项目展示名：`OpenQuant`
- Python 项目名：`openquant`

首次提交可以使用：

```bash
git add .
git commit -m "Initialize OpenQuant platform scaffold"
git remote add origin https://github.com/<your-name>/openquant.git
git branch -M main
git push -u origin main
```
