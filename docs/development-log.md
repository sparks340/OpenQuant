# Development Log

## 2026-04-07

### Phase 1 Started

- 建立 `apps/`、`packages/`、`docs/`、`tests/` 结构
- 初始化服务骨架
- 初始化 `core`、`domain`、`datastore`、`task_engine`、`sdk`
- 添加 `pyproject.toml`、`.env.example`、`.gitignore`
- 添加架构文档、工作流文档和开发记录
- 统一项目名称为 `OpenQuant`
- 将服务目录收敛为短名：`apps/api`、`apps/research`、`apps/trading`、`apps/scheduler`、`apps/llm`
- 清理文档中的中文乱码
- 补充 GitHub 上传说明

### Phase 1 Outcome

仓库已经具备继续迭代的基础工程结构，后续阶段将按工作流持续推进。

### Workflow Check

- 按 `docs/workflow.md` 的 Phase 1 清单复核：目录结构、服务骨架、配置日志、开发记录均已落地。
- 校验测试入口：修正 `pytest` 直跑时的模块导入路径，确保 `pytest -q` 与 `python -m pytest -q` 都可执行。
- 当前状态：Phase 1 可视为完成；Phase 2~5 仍未开始（暂无对应领域实现与数据/交易能力代码）。
