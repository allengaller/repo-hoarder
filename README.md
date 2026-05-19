# GitHub Treasure Repo

全自动抓取 GitHub Trending 优质项目的开源工具，通过专业评分体系筛选宝藏 repo。

## 核心特性

- **多维度采集**: daily / weekly / monthly 三种时间维度 × 14 种主流语言
- **专业评分**: Stars + Fork率 + 增长加速度 综合评分
- **质量门槛**: stars ≥ 1000, forks ≥ 10
- **自动更新**: 每月 1 日 GitHub Actions 自动抓取 + 支持手动触发
- **Web UI**: 深色主题卡片展示，支持搜索/筛选/排序

## 评分标准

```
综合得分 = Stars + (Fork数/Stars数 × 1000) + 今日增长 × 时间权重

时间权重: daily=30, weekly=4, monthly=1
```

## 项目结构

```
repo-hoarder/
├── scripts/
│   └── scrape.py          # 爬虫脚本
├── data/
│   └── repos.json         # 抓取的数据
├── web/
│   ├── index.html         # 主页面
│   ├── styles.css         # 样式
│   └── app.js             # 前端逻辑
├── .github/
│   └── workflows/
│       └── monthly-scrape.yml  # GitHub Actions
├── requirements.txt       # Python 依赖
└── README.md
```

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 抓取数据（全量）
python3 scripts/scrape.py

# 快速抓取（仅当日 trending）
python3 scripts/scrape.py --quick

# 预览 Web UI
cd web && python3 -m http.server 8000
```

## 技术栈

- **Python 3**: requests + BeautifulSoup
- **前端**: 纯 HTML/CSS/JS（零依赖）
- **CI/CD**: GitHub Actions

## 数据示例

| 排名 | Repo | Stars | Forks | 评分 |
|------|------|-------|-------|------|
| 1 | flutter/flutter | 176k | 30k | 176,527 |
| 2 | ollama/ollama | 172k | 16k | 171,771 |
| 3 | NousResearch/hermes-agent | 156k | 25k | 155,963 |

## License

MIT