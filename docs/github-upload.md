# GitHub Upload Guide

## Goal

把当前仓库作为你自己的 `OpenQuant` 项目上传到个人 GitHub。

## Recommended Naming

- Local folder: `openquant`
- GitHub repository: `openquant`
- Project display name: `OpenQuant`
- Python package name: `openquant`

## Recommended First Commit

建议第一次提交使用：

```bash
git add .
git commit -m "Initialize OpenQuant platform scaffold"
```

## Connect Your Own Remote

如果你已经在 GitHub 创建了自己的空仓库，可以这样连接：

```bash
git remote add origin https://github.com/<your-name>/openquant.git
git branch -M main
git push -u origin main
```

## Suggested Repository Description

可以在 GitHub 仓库简介里使用这段：

> OpenQuant is a modular quant research, backtesting, simulation, and live trading platform.

## Suggested Topics

- quant
- trading
- backtesting
- factor-research
- algorithmic-trading
- fastapi
- python
