# GitHub Treasure Repo

全自动聚合 GitHub 优质项目的开源工具，整合 Awesome 榜单 + API 搜索 + Trending 多源数据。

## 核心特性

- **多源聚合**: Awesome Lists + GitHub API + Trending HTML
- **专业评分**: Stars + Fork率 + 增长加速度 综合评分
- **多维度筛选**: 语言 / Stars / Forks / 评分范围筛选
- **暗夜/白天模式**: 一键切换，本地存储记忆
- **自动更新**: 每月 1 日 GitHub Actions 自动抓取 + 支持手动触发

## 数据来源

| 来源 | 描述 |
|------|------|
| **Awesome Lists** | vinta/awesome-python, avelino/awesome-go 等经典列表 |
| **GitHub API** | 2026 年创建的热门项目搜索 |
| **Trending** | 当日/周/月热门项目 |

## 评分标准

```
综合得分 = Stars + Forks + (Fork数/Stars数 × 1000) + 今日增长 × 10
```

## 项目结构

```
repo-hoarder/
├── scripts/
│   └── scrape.py          # 多源聚合爬虫
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

# 抓取数据（多源聚合）
python3 scripts/scrape.py

# 预览 Web UI
cd web && python3 -m http.server 8000
```

## 技术栈

- **Python 3**: requests + BeautifulSoup
- **前端**: 纯 HTML/CSS/JS（零依赖）
- **CI/CD**: GitHub Actions

## 数据示例

| 排名 | Repo | 语言 | Stars |
|------|------|------|-------|
| 1 | ultraworkers/claw-code | Rust | 192k |
| 2 | affaan-m/ECC | JavaScript | 187k |
| 3 | NousResearch/hermes-agent | Python | 157k |
| 4 | multica-ai/andrej-karpathy-skills | - | 137k |
| 5 | ggml-org/llama.cpp | C++ | 111k |

## License

MIT