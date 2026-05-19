#!/usr/bin/env python3
"""
GitHub Treasure Repo Scraper
Uses GitHub API for accurate 2026 data
"""

import json
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Quality thresholds
MIN_STARS = 500
MIN_FORKS = 5

# Languages to search
LANGUAGES = [
    "python", "javascript", "typescript", "go", "rust", "java",
    "cpp", "c", "ruby", "swift", "kotlin", "dart", "csharp"
]


def search_github_repos(query, min_stars=1000, per_page=30):
    """Search GitHub repos using API"""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{query} created:2026-01-01..2026-12-31 stars:>={min_stars}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
        "page": 1
    }
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        if resp.status_code == 403:
            print(f"    Rate limited, waiting...")
            time.sleep(5)
            return []
        resp.raise_for_status()
        return resp.json().get("items", [])
    except Exception as e:
        print(f"    Error: {e}")
        return []


def fetch_trending_via_html():
    """Fetch from HTML as fallback"""
    url = "https://github.com/trending"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select("article.Box-row")
    repos = []

    for article in articles:
        try:
            h2 = article.select_one("h2")
            if not h2:
                continue
            h2_text = h2.get_text(strip=True)
            parts = h2_text.split("/")
            if len(parts) < 2:
                continue

            owner = parts[0].strip()
            repo_name = parts[1].strip()
            full_name = f"{owner}/{repo_name}"

            desc_elem = article.select_one("p.col-9")
            description = desc_elem.get_text(strip=True) if desc_elem else ""

            stars = forks = 0
            for a in article.select("a"):
                href = a.get("href", "")
                text = a.get_text(strip=True)
                if "/stargazers" in href:
                    stars = parse_num(text)
                elif "/forks" in href:
                    forks = parse_num(text)

            lang_elem = article.select_one("span[itemprop='programmingLanguage']")
            lang = lang_elem.get_text(strip=True) if lang_elem else "Unknown"

            star_span = article.select_one("span.d-inline-block.float-sm-right")
            today_stars = parse_num(star_span.get_text(strip=True)) if star_span else 0

            repos.append({
                "name": full_name,
                "url": f"https://github.com/{full_name}",
                "description": description,
                "stars": stars,
                "forks": forks,
                "language": lang,
                "today_stars": today_stars,
                "score": stars + forks,
                "fetched_at": datetime.now().isoformat()
            })
        except Exception:
            continue

    return repos


def parse_num(text):
    """Parse number like 1.2k, 3.4M"""
    text = text.replace(",", "").replace(" ", "")
    for suffix, mult in {"k": 1_000, "m": 1_000_000}.items():
        if suffix in text.lower():
            try:
                return int(float(text.lower().replace(suffix, "")) * mult)
            except ValueError:
                return 0
    try:
        return int(text)
    except ValueError:
        return 0


def fetch_all_2026_repos():
    """Main fetch function using GitHub API"""
    print("🏆 Fetching 2026 GitHub Treasure Repos via API")
    print("=" * 50)

    all_repos = []
    seen = set()

    # Search trending/agent related (most active in 2026)
    print("\n[1/4] Fetching Agent & AI repos...")
    queries = [
        "agent skills",
        "claude-code",
        "AI framework",
        "LLM inference",
    ]
    for q in queries:
        print(f"  Query: {q}")
        repos = search_github_repos(q, min_stars=500)
        for r in repos:
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                all_repos.append(format_api_repo(r))
        time.sleep(0.5)

    # Fetch by language
    print("\n[2/4] Fetching by language...")
    for lang in LANGUAGES[:8]:  # Top 8 languages
        print(f"  {lang}...")
        repos = search_github_repos(f"language:{lang}", min_stars=1000)
        for r in repos:
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                all_repos.append(format_api_repo(r))
        time.sleep(0.5)

    # Fallback to HTML scraping
    print("\n[3/4] Fetching from GitHub Trending...")
    html_repos = fetch_trending_via_html()
    for r in html_repos:
        if r["name"] not in seen:
            seen.add(r["name"])
            all_repos.append(r)

    # Remove duplicates and sort
    print(f"\n[4/4] Processing {len(all_repos)} repos...")
    unique = {}
    for repo in all_repos:
        name = repo["name"]
        if name not in unique or repo["stars"] > unique[name]["stars"]:
            unique[name] = repo

    result = list(unique.values())
    result.sort(key=lambda x: x["score"], reverse=True)

    # Calculate proper score
    for repo in result:
        fork_ratio = repo["forks"] / repo["stars"] if repo["stars"] > 0 else 0
        repo["score"] = round(repo["stars"] + repo["forks"] + fork_ratio * 1000 + repo.get("today_stars", 0) * 10, 2)

    return result


def format_api_repo(r):
    """Format GitHub API repo to our schema"""
    return {
        "name": r["full_name"],
        "url": r["html_url"],
        "description": r.get("description") or "暂无描述",
        "stars": r["stargazers_count"],
        "forks": r["forks_count"],
        "language": r.get("language") or "Unknown",
        "today_stars": 0,
        "score": r["stargazers_count"],
        "fetched_at": datetime.now().isoformat()
    }


def main():
    print("Starting fetch at", datetime.now().isoformat())

    repos = fetch_all_2026_repos()

    # Re-sort after score calculation
    repos.sort(key=lambda x: x["score"], reverse=True)

    output = {
        "fetched_at": datetime.now().isoformat(),
        "total": len(repos),
        "source": "github_api + trending_html",
        "criteria": {"min_stars": MIN_STARS, "min_forks": MIN_FORKS},
        "repos": repos
    }

    with open("data/repos.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved {len(repos)} repos to data/repos.json")

    print("\n🏆 Top 10:")
    for i, repo in enumerate(repos[:10], 1):
        print(f"  {i:2}. {repo['name']:<45} ⭐{repo['stars']:>8,} 评分:{repo['score']:>10,.0f}")


if __name__ == "__main__":
    main()