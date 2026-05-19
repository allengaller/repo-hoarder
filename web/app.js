const DATA_URL = '../data/repos.json';

let allRepos = [];
let languages = new Set();

// Language SVG icons (minimal, geometric)
const LANG_ICONS = {
  'Python': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2C6.48 2 6 4.24 6 6v2h6v1H5.5C3.02 9 2 10.02 2 12.5v1C2 15.98 3.02 17 5.5 17H6v2c0 1.76.48 4 6 4s6-2.24 6-4v-2h.5c2.48 0 3.5-1.02 3.5-3.5v-1c0-2.48-1.02-3.5-3.5-3.5H18V6c0-1.76-.48-4-6-4zm-2 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm5 4H9c-.55 0-1-.45-1-1s.45-1 1-1h6c.55 0 1 .45 1 1s-.45 1-1 1z"/></svg>`,
  'JavaScript': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 10l2 2 4-4"/></svg>`,
  'TypeScript': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 17V9h2.5c1.5 0 2.5.83 2.5 2.5s-1 2.5-2.5 2.5H9"/></svg>`,
  'Go': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`,
  'Rust': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><path d="M12 8v4l3 3"/></svg>`,
  'Java': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 3h8l-1 9H9L8 3z"/><path d="M7 12c0-2 1.5-4 5-4s5 2 5 4-1.5 4-5 4-5-2-5-4z"/><path d="M9 21h6l-1-8h-4L9 21z"/></svg>`,
  'C++': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2l-9 4.5v9L12 20l9-4.5v-9L12 2z"/><path d="M12 22V10"/><path d="M20 7.5L12 10 4 7.5"/></svg>`,
  'C': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 8h-4V6H8c-2.21 0-4 1.79-4 4v8c0 2.21 1.79 4 4 4h6v-2h-6c-1.1 0-2-.9-2-2v-2h2v-2h4v2h2V8z"/></svg>`,
  'C#': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L4 6v6c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V6l-8-4z"/></svg>`,
  'Ruby': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L3 7v10l9 5 9-5V7l-9-5z"/><path d="M12 22V12"/><path d="M3 7l9 5 9-5"/></svg>`,
  'PHP': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><ellipse cx="12" cy="12" rx="9" ry="5"/><path d="M4 10V8c0-2 1.5-3 4-3h8c2.5 0 4 1 4 3v2"/><path d="M4 14v2c0 2 1.5 3 4 3h8c2.5 0 4-1 4-3v-2"/></svg>`,
  'Swift': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4l8 16L20 4"/><path d="M4 4h16"/></svg>`,
  'Kotlin': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 4c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6 2.69-6 6-6z"/></svg>`,
  'Dart': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 20l7-16L19 4"/><path d="M5 20h14L12 12"/></svg>`,
  'Jupyter Notebook': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 7h4v4H7z"/><path d="M13 7h4"/><path d="M13 11h4"/><path d="M7 15h10"/></svg>`,
  'HTML': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 3l2 18 6-3 6 3 2-18H4z"/><path d="M8 8h8l-.5 5.5L12 15l-3.5-1.5L8 8z"/></svg>`,
  'CSS': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 3l2 18 6-3 6 3 2-18H4z"/><path d="M8 9l1 7 3-1.5 2 2.5H8"/></svg>`,
  'Shell': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 17l6-6-6-6"/><path d="M12 19h8"/></svg>`,
  'Unknown': `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="12" r="4"/></svg>`
};

// Theme management
function initTheme() {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (prefersDark ? 'dark' : 'light');
  document.body.dataset.theme = theme;
}

function toggleTheme() {
  const current = document.body.dataset.theme;
  const next = current === 'dark' ? 'light' : 'dark';
  document.body.dataset.theme = next;
  localStorage.setItem('theme', next);
}

// Load repos
async function loadRepos() {
  const grid = document.getElementById('repoGrid');

  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error('Data file not found');
    const data = await response.json();

    allRepos = data.repos || [];

    // Update stats
    document.getElementById('repoCount').textContent = allRepos.length;
    document.getElementById('totalStars').textContent = fmtNum(
      allRepos.reduce((s, r) => s + r.stars, 0)
    );
    document.getElementById('langCount').textContent = new Set(allRepos.map(r => r.language)).size;
    document.getElementById('lastUpdated').textContent = fmtDate(data.fetched_at);

    extractLanguages();
    populateLanguageFilter();
    updateRangeMaxValues();
    renderRepos(allRepos);
    applyStagger();

  } catch (error) {
    grid.innerHTML = `
      <div class="loading">
        <span style="color: var(--text-muted); font-size: 0.9rem;">无法加载数据，请先运行 scripts/scrape.py</span>
      </div>
    `;
  }
}

function extractLanguages() {
  languages = new Set(allRepos.map(r => r.language).filter(Boolean));
}

function populateLanguageFilter() {
  const select = document.getElementById('languageFilter');
  select.innerHTML = '<option value="">全部</option>';

  Array.from(languages).sort().forEach(lang => {
    const opt = document.createElement('option');
    opt.value = lang;
    opt.textContent = `${lang} (${allRepos.filter(r => r.language === lang).length})`;
    select.appendChild(opt);
  });
}

function updateRangeMaxValues() {
  const maxStars = Math.max(...allRepos.map(r => r.stars), 50000);
  const maxForks = Math.max(...allRepos.map(r => r.forks), 5000);
  const maxScore = Math.max(...allRepos.map(r => r.score), 200000);

  document.getElementById('starsRange').max = Math.ceil(maxStars / 1000) * 1000;
  document.getElementById('forksRange').max = Math.ceil(maxForks / 100) * 100;
  document.getElementById('scoreRange').max = Math.ceil(maxScore / 5000) * 5000;
}

function renderRepos(repos) {
  const grid = document.getElementById('repoGrid');

  if (repos.length === 0) {
    grid.innerHTML = `
      <div class="loading">
        <span style="color: var(--text-muted);">没有找到符合条件的项目</span>
      </div>
    `;
    return;
  }

  grid.innerHTML = repos.map((repo, i) => createCard(repo, i)).join('');
}

function createCard(repo, index) {
  const [author, name] = repo.name.split('/');
  const icon = LANG_ICONS[repo.language] || LANG_ICONS['Unknown'];

  return `
    <article class="repo-card" style="animation-delay: ${index * 0.025}s">
      <div class="card-header">
        <div class="card-icon">${icon}</div>
        <div class="card-info">
          <h3 class="card-name">
            <a href="${repo.url}" target="_blank" rel="noopener">${esc(name)}</a>
          </h3>
          <span class="card-author">${esc(author)}</span>
        </div>
      </div>
      <p class="card-desc">${esc(repo.description || '暂无描述')}</p>
      <div class="card-stats">
        <span class="card-stat stars">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          ${fmtNum(repo.stars)}
        </span>
        <span class="card-stat">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/>
            <path d="M18 6v6c0 2-2 4-6 6-4-2-6-4-6-6V6"/>
          </svg>
          ${fmtNum(repo.forks)}
        </span>
        ${repo.language && repo.language !== 'Unknown' ? `
          <span class="card-stat lang">${repo.language}</span>
        ` : ''}
        ${repo.today_stars > 0 ? `
          <span class="card-stat" style="color: var(--text-muted)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
              <polyline points="17 6 23 6 23 12"/>
            </svg>
            +${fmtNum(repo.today_stars)}
          </span>
        ` : ''}
        <span class="card-stat score">🏆 ${fmtNum(repo.score)}</span>
      </div>
    </article>
  `;
}

function applyStagger() {
  document.querySelectorAll('.repo-card').forEach((card, i) => {
    card.style.animationDelay = `${i * 0.02}s`;
  });
}

function esc(text) {
  const d = document.createElement('div');
  d.textContent = text;
  return d.innerHTML;
}

function fmtNum(num) {
  if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M';
  if (num >= 1_000) return (num / 1_000).toFixed(1) + 'k';
  return num.toString();
}

function fmtDate(str) {
  if (!str) return '-';
  const d = new Date(str);
  return d.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function filterAndSort() {
  const search = document.getElementById('searchInput').value.toLowerCase();
  const lang = document.getElementById('languageFilter').value;
  const sort = document.getElementById('sortFilter').value;
  const minStars = parseInt(document.getElementById('starsRange').value) || 0;
  const minForks = parseInt(document.getElementById('forksRange').value) || 0;
  const minScore = parseInt(document.getElementById('scoreRange').value) || 0;

  let f = allRepos.filter(r => {
    if (search && !r.name.toLowerCase().includes(search) && !r.description?.toLowerCase().includes(search)) return false;
    if (lang && r.language !== lang) return false;
    if (r.stars < minStars) return false;
    if (r.forks < minForks) return false;
    if (r.score < minScore) return false;
    return true;
  });

  f.sort((a, b) => {
    switch (sort) {
      case 'stars': return b.stars - a.stars;
      case 'forks': return b.forks - a.forks;
      case 'today': return b.today_stars - a.today_stars;
      case 'score': return b.score - a.score;
      default: return 0;
    }
  });

  renderRepos(f);
  applyStagger();
}

function updateRangeDisplay(rangeId, valId) {
  document.getElementById(valId).textContent = fmtNum(parseInt(document.getElementById(rangeId).value));
}

function resetFilters() {
  document.getElementById('searchInput').value = '';
  document.getElementById('languageFilter').value = '';
  document.getElementById('sortFilter').value = 'score';
  document.getElementById('starsRange').value = 0;
  document.getElementById('forksRange').value = 0;
  document.getElementById('scoreRange').value = 0;
  document.getElementById('starsValue').textContent = '0';
  document.getElementById('forksValue').textContent = '0';
  document.getElementById('scoreValue').textContent = '0';
  filterAndSort();
}

function debounce(fn, d) {
  let t;
  return function(...a) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, a), d);
  };
}

// Event listeners
document.getElementById('themeToggle').addEventListener('click', toggleTheme);
document.getElementById('searchInput').addEventListener('input', debounce(filterAndSort, 200));
document.getElementById('languageFilter').addEventListener('change', filterAndSort);
document.getElementById('sortFilter').addEventListener('change', filterAndSort);

['starsRange', 'forksRange', 'scoreRange'].forEach(id => {
  const rangeId = id;
  const valId = id.replace('Range', 'Value');
  document.getElementById(rangeId).addEventListener('input', () => {
    updateRangeDisplay(rangeId, valId);
    filterAndSort();
  });
});

document.getElementById('resetFilters').addEventListener('click', resetFilters);

// Init
initTheme();
loadRepos();