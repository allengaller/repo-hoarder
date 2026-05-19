# GitHub Treasure Repo

## 项目概述

自动抓取 GitHub Trending 优质项目的工具，通过专业评分体系筛选宝藏 repo。

## 评分算法

```
综合得分 = Stars + (Fork数/Stars数 × 1000) + 今日增长 × 时间权重
```

- 时间权重: daily=30, weekly=4, monthly=1
- 质量门槛: stars ≥ 1000, forks ≥ 10

## 爬虫逻辑

1. 遍历 3 种时间维度 (daily/weekly/monthly)
2. 遍历 14 种语言 (Python, JS, TS, Go, Rust, Java, C++, C, Ruby, Swift, Kotlin, Dart, C#)
3. 每次请求间隔 1 秒，避免触发限流
4. 去重并按综合评分排序
5. 输出到 data/repos.json

## Web UI

- 读取 data/repos.json 展示
- 支持按语言筛选、按 stars/forks/score 排序
- 搜索支持 repo 名称和描述

## GitHub Actions

- 触发条件: 每月 1 日 + workflow_dispatch
- 运行脚本: python scripts/scrape.py
- 自动提交更新到 data/repos.json