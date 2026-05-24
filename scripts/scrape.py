#!/usr/bin/env python3
"""
GitHub Treasure Repo Scraper
Uses GitHub API + Curated Lists for comprehensive 2026 data
"""

import json
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Quality thresholds
MIN_STARS = 500
MIN_FORKS = 5

# Curated awesome lists
AWESOME_LISTS = [
    {"name": "awesome-python", "url": "https://raw.githubusercontent.com/vinta/awesome-python/main/README.md"},
    {"name": "awesome-go", "url": "https://raw.githubusercontent.com/avelino/awesome-go/main/README.md"},
    {"name": "awesome-javascript", "url": "https://raw.githubusercontent.com/sorrycc/awesome-javascript/main/README.md"},
    {"name": "awesome-rust", "url": "https://raw.githubusercontent.com/rust-unofficial/awesome-rust/main/README.md"},
    {"name": "awesome-java", "url": "https://raw.githubusercontent.com/akullpp/awesome-java/main/README.md"},
    {"name": "awesome-cpp", "url": "https://raw.githubusercontent.com/fffaraz/awesome-cpp/main/README.md"},
    {"name": "awesome-typescript", "url": "https://raw.githubusercontent.com/semlinker/awesome-typescript/main/README.md"},
    {"name": "awesome-swift", "url": "https://raw.githubusercontent.com/matteocrippa/awesome-swift/main/README.md"},
]

LANGUAGES = [
    "python", "javascript", "typescript", "go", "rust", "java",
    "cpp", "c", "ruby", "swift", "kotlin", "dart", "csharp"
]


def parse_awesome_list(content):
    """Parse awesome list markdown to extract repo URLs"""
    import re
    repos = []

    # Match GitHub URLs in the format github.com/owner/repo or owner/repo
    patterns = [
        r'github\.com/([a-zA-Z0-9-_]+)/([a-zA-Z0-9-_.]+)',
        r'^#\s+\[([^\]]+)\]\(https://github\.com/([a-zA-Z0-9-_]+)/([a-zA-Z0-9-_.]+)\)',
        r'\*\*\[([^\]]+)\]\(https://github\.com/([a-zA-Z0-9-_]+)/([a-zA-Z0-9-_.]+)\)',
    ]

    for line in content.split('\n'):
        line = line.strip()
        for pattern in patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                if len(match) >= 3:
                    owner, repo = match[1], match[2].rstrip('/')
                    if 'awesome-' not in repo.lower():
                        repos.append(f"{owner}/{repo}")

    return list(set(repos))[:50]  # Limit per list


def fetch_github_repo_details(owner, repo):
    """Fetch repo details from GitHub API"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 403:
            return None
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None


def fetch_awesome_lists():
    """Fetch repos from curated awesome lists via GitHub API"""
    print("\n[1/5] Fetching from curated awesome lists...")

    awesome_repos = {}

    # Use GitHub API to get repo contents
    for list_info in AWESOME_LISTS:
        print(f"  📚 {list_info['name']}...", end=" ")

        # Try GitHub API instead of raw content
        try:
            owner_repo = list_info["name"]
            url = f"https://api.github.com/repos/{owner_repo}"
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

            if resp.status_code == 200:
                data = resp.json()
                # This is the awesome list repo itself - get its stars
                stars = data.get("stargazers_count", 0)
                if stars >= MIN_STARS:
                    awesome_repos[owner_repo] = {
                        "name": owner_repo,
                        "url": data.get("html_url", f"https://github.com/{owner_repo}"),
                        "description": data.get("description", ""),
                        "stars": stars,
                        "forks": data.get("forks_count", 0),
                        "language": data.get("language") or "Markdown",
                        "today_stars": 0,
                        "score": stars,
                        "fetched_at": datetime.now().isoformat(),
                        "source": "awesome_list"
                    }
                print(f"⭐{stars:,}")
            else:
                print(f"failed ({resp.status_code})")
        except Exception as e:
            print(f"error")

        time.sleep(0.3)

    print(f"  ✅ Collected {len(awesome_repos)} repos from awesome lists")
    return awesome_repos


def search_github_repos(query, min_stars=1000, per_page=30):
    """Search GitHub repos using API"""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{query} created:2026-01-01..2026-12-31 stars:>={min_stars}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        if resp.status_code == 403:
            print("    Rate limited")
            time.sleep(5)
            return []
        resp.raise_for_status()
        return resp.json().get("items", [])
    except Exception as e:
        print(f"    Error: {e}")
        return []


def fetch_from_api():
    """Fetch repos via GitHub API"""
    print("\n[2/5] Fetching 2026 repos via API...")
    api_repos = {}
    seen = set()

    # Agent/AI related queries
    queries = ["agent skills", "claude-code", "AI framework", "LLM inference", "RAG"]
    for q in queries:
        print(f"  Query: {q}...", end=" ")
        repos = search_github_repos(q, min_stars=500)
        print(f"found {len(repos)}")
        for r in repos:
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                api_repos[r["full_name"]] = format_api_repo(r)
        time.sleep(0.5)

    # By language
    for lang in LANGUAGES[:6]:
        print(f"  {lang}...", end=" ")
        repos = search_github_repos(f"language:{lang}", min_stars=2000)
        print(f"found {len(repos)}")
        for r in repos:
            if r["full_name"] not in seen:
                seen.add(r["full_name"])
                api_repos[r["full_name"]] = format_api_repo(r)
        time.sleep(1)

    print(f"  ✅ Collected {len(api_repos)} repos from API")
    return api_repos


def fetch_trending_html():
    """Fetch from GitHub Trending HTML"""
    print("\n[3/5] Fetching from GitHub Trending...")
    from bs4 import BeautifulSoup

    url = "https://github.com/trending"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

    trending_repos = {}

    for since in ["daily", "weekly", "monthly"]:
        try:
            resp = requests.get(url, params={"since": since}, headers=headers, timeout=30)
            soup = BeautifulSoup(resp.text, "html.parser")

            for article in soup.select("article.Box-row"):
                try:
                    h2 = article.select_one("h2")
                    if not h2:
                        continue

                    h2_text = h2.get_text(strip=True)
                    parts = h2_text.split("/")
                    if len(parts) < 2:
                        continue

                    full_name = f"{parts[0].strip()}/{parts[1].strip()}"

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

                    trending_repos[full_name] = {
                        "name": full_name,
                        "url": f"https://github.com/{full_name}",
                        "description": description,
                        "stars": stars,
                        "forks": forks,
                        "language": lang,
                        "today_stars": today_stars,
                        "score": stars,
                        "fetched_at": datetime.now().isoformat()
                    }
                except Exception:
                    continue

            time.sleep(1)
        except Exception as e:
            print(f"    Error fetching {since}: {e}")

    print(f"  ✅ Collected {len(trending_repos)} repos from Trending")
    return trending_repos


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
        "fetched_at": datetime.now().isoformat(),
        "source": "github_api"
    }


def calculate_score(repo):
    """Calculate treasure score"""
    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)
    today = repo.get("today_stars", 0)
    fork_ratio = forks / stars if stars > 0 else 0
    return round(stars + forks + fork_ratio * 1000 + today * 10, 2)


def merge_and_sort(all_repos):
    """Merge all sources and sort by score"""
    print(f"\n[4/5] Processing {len(all_repos)} total repos...")

    # Deduplicate by name, keeping highest score
    unique = {}
    for repo in all_repos.values():
        name = repo["name"]
        repo["score"] = calculate_score(repo)
        if name not in unique or repo["stars"] > unique[name]["stars"]:
            unique[name] = repo

    result = list(unique.values())
    result.sort(key=lambda x: x["score"], reverse=True)

    print(f"  ✅ {len(result)} unique repos after deduplication")
    return result


def save_results(repos):
    """Save to JSON file"""
    print(f"\n[5/5] Saving results...")

    output = {
        "fetched_at": datetime.now().isoformat(),
        "total": len(repos),
        "sources": ["awesome_lists", "github_api", "trending_html"],
        "criteria": {
            "min_stars": MIN_STARS,
            "min_forks": MIN_FORKS,
            "awesome_lists": [l["name"] for l in AWESOME_LISTS]
        },
        "repos": repos
    }

    with open("data/repos.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  ✅ Saved to data/repos.json")
    return output


def print_top_repos(repos):
    """Print top 15 repos"""
    print("\n🏆 Top 15 Treasure Repos:")
    for i, repo in enumerate(repos[:15], 1):
        source_icon = "📚" if repo.get("source") == "awesome_list" else "🔍"
        print(f"  {i:2}. {source_icon} {repo['name']:<45} ⭐{repo['stars']:>7,}  评分:{repo['score']:>10,.0f}")
        print(f"      {repo['language']:<12} | {repo['description'][:50]}...")


def main():
    print("=" * 60)
    print("🏆 GitHub Treasure Repo Scraper")
    print("   Sources: Awesome Lists + GitHub API + Trending")
    print("=" * 60)
    print(f"\nStarted at {datetime.now().isoformat()}")

    # Fetch from all sources
    awesome_repos = fetch_awesome_lists()
    api_repos = fetch_from_api()
    trending_repos = fetch_trending_html()

    # Merge all repos
    all_repos = {}
    all_repos.update(awesome_repos)
    all_repos.update(api_repos)
    all_repos.update(trending_repos)

    # Process and save
    repos = merge_and_sort(all_repos)
    output = save_results(repos)

    # Print summary
    print_top_repos(repos)

    # Stats
    lang_count = len(set(r["language"] for r in repos))
    total_stars = sum(r["stars"] for r in repos)
    print(f"\n📊 Stats:")
    print(f"   Total repos: {len(repos)}")
    print(f"   Total stars: {total_stars:,}")
    print(f"   Languages: {lang_count}")


if __name__ == "__main__":
    main()