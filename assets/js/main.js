// =============================================================================
// MAIN JAVASCRIPT - Research Project Website
// =============================================================================
// This file handles all interactive functionality for the research project site
// Publication data will be injected by Jekyll from _data/publications.json

let publicationsData = [];
let searchIndex = null;

// =============================================================================
// BIBTEX FUNCTIONALITY
// =============================================================================

// Generate BibTeX citation for a publication
function generateBibtex(pub) {
  const key = pub.openalex_id || 'pub' + Math.random().toString(36).substr(2, 9);
  const authors = pub.authors ? pub.authors.replace(/, et al\./g, ' and others').replace(/, /g, ' and ') : '';
  const type = pub.type === 'article' ? 'article' : 'misc';

  return `@${type}{${key},
  title = {${pub.title || ''}},
  author = {${authors}},
  journal = {${pub.journal || ''}},
  year = {${pub.year || ''}},
  doi = {${pub.doi || ''}}
}`;
}

// Copy single BibTeX entry to clipboard
function copyBibtex(index) {
  if (publicationsData[index]) {
    const bibtex = generateBibtex(publicationsData[index]);
    navigator.clipboard.writeText(bibtex).then(() => {
      const btn = document.querySelector(`[data-bibtex-index="${index}"]`);
      if (btn) {
        const original = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = original; }, 1500);
      }
    });
  }
}

// Download all BibTeX entries as a .bib file
function downloadAllBibtex() {
  const allBibtex = publicationsData.map(generateBibtex).join('\n\n');
  const blob = new Blob([allBibtex], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'publications.bib';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// =============================================================================
// ABSTRACT TOGGLE
// =============================================================================

function toggleAbstract(index) {
  const abstract = document.querySelector(`[data-abstract-index="${index}"]`);
  const btn = document.querySelector(`[data-abstract-btn="${index}"]`);
  if (abstract && btn) {
    const isHidden = abstract.style.display === 'none' || !abstract.style.display;
    abstract.style.display = isHidden ? 'block' : 'none';
    btn.textContent = isHidden ? 'Hide Abstract' : 'Show Abstract';
  }
}

// =============================================================================
// DARK MODE
// =============================================================================

function toggleDarkMode() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);

  // Update button icons
  const themeIcons = document.querySelectorAll('.theme-icon');
  themeIcons.forEach(icon => {
    icon.innerHTML = newTheme === 'dark' ? '&#9788;' : '&#9790;';
  });

  const themeToggle = document.querySelector('.theme-toggle');
  if (themeToggle) {
    themeToggle.innerHTML = newTheme === 'dark'
      ? '<span class="theme-icon">&#9788;</span> Light Mode'
      : '<span class="theme-icon">&#9790;</span> Dark Mode';
  }
}

function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    if (savedTheme === 'dark') {
      const themeToggle = document.querySelector('.theme-toggle');
      if (themeToggle) {
        themeToggle.innerHTML = '<span class="theme-icon">&#9788;</span> Light Mode';
      }
    }
  }
}

// =============================================================================
// MOBILE MENU
// =============================================================================

function toggleMobileMenu() {
  const sidebar = document.getElementById('sidebarNav');
  const toggleBtn = document.querySelector('.mobile-menu-toggle');

  if (sidebar && toggleBtn) {
    sidebar.classList.toggle('mobile-active');
    toggleBtn.classList.toggle('active');
  }
}

function initMobileMenuClose() {
  const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
  sidebarLinks.forEach(link => {
    link.addEventListener('click', () => {
      const sidebar = document.getElementById('sidebarNav');
      const toggleBtn = document.querySelector('.mobile-menu-toggle');
      if (sidebar && toggleBtn && window.innerWidth < 1024) {
        sidebar.classList.remove('mobile-active');
        toggleBtn.classList.remove('active');
      }
    });
  });
}

function closeSidebarOnMobile() {
  if (window.innerWidth < 1024) {
    const sidebar = document.getElementById('sidebarNav');
    const toggleBtn = document.querySelector('.mobile-menu-toggle');
    if (sidebar) sidebar.classList.remove('mobile-active');
    if (toggleBtn) toggleBtn.classList.remove('active');
  }
}

// =============================================================================
// BACK TO TOP BUTTON
// =============================================================================

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

function initBackToTop() {
  const backToTopBtn = document.getElementById('backToTop');
  if (backToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    });
  }
}

// =============================================================================
// PUBLICATION FILTERS
// =============================================================================

function initPublicationFilters() {
  const yearSelect = document.getElementById('yearFilter');
  if (!yearSelect || !publicationsData.length) return;

  // Populate year filter from publication data
  const years = [...new Set(publicationsData.map(p => p.year).filter(Boolean))].sort((a, b) => b - a);
  years.forEach(year => {
    const option = document.createElement('option');
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
  });
}

function filterPublications() {
  const yearFilter = document.getElementById('yearFilter')?.value || 'all';
  const topicFilter = document.getElementById('topicFilter')?.value || 'all';
  const accessFilter = document.getElementById('accessFilter')?.value || 'all';

  const pubItems = document.querySelectorAll('.pub-item');

  pubItems.forEach(item => {
    const year = item.dataset.year;
    const title = (item.dataset.title || '').toLowerCase();
    const isOpen = item.dataset.open === 'true';

    let show = true;

    // Year filter
    if (yearFilter !== 'all' && year !== yearFilter) {
      show = false;
    }

    // Topic filter - customize keywords for your research area
    if (topicFilter !== 'all') {
      const topicKeywords = {
        // Add your research topics and keywords here
        'topic1': ['keyword1', 'keyword2', 'keyword3'],
        'topic2': ['keyword4', 'keyword5'],
        'topic3': ['keyword6', 'keyword7', 'keyword8']
      };
      const keywords = topicKeywords[topicFilter] || [];
      if (!keywords.some(kw => title.includes(kw))) {
        show = false;
      }
    }

    // Access filter
    if (accessFilter === 'open' && !isOpen) {
      show = false;
    }

    item.classList.toggle('hidden', !show);
  });
}

function resetFilters() {
  const yearFilter = document.getElementById('yearFilter');
  const topicFilter = document.getElementById('topicFilter');
  const accessFilter = document.getElementById('accessFilter');

  if (yearFilter) yearFilter.value = 'all';
  if (topicFilter) topicFilter.value = 'all';
  if (accessFilter) accessFilter.value = 'all';

  filterPublications();
}

// =============================================================================
// CITATION METRICS
// =============================================================================

function updateCitationMetrics() {
  if (!publicationsData.length) return;

  const totalCitations = publicationsData.reduce((sum, p) => sum + (p.citations || 0), 0);
  const avgCitations = (totalCitations / publicationsData.length).toFixed(1);
  const openAccessCount = publicationsData.filter(p => p.open_access).length;

  // Update stats banner
  const totalCitationsEl = document.querySelector('#totalCitations .stat-number');
  if (totalCitationsEl) {
    totalCitationsEl.textContent = totalCitations.toLocaleString();
  }

  // Update metric cards
  const metricTotalCitations = document.getElementById('metricTotalCitations');
  const metricAvgCitations = document.getElementById('metricAvgCitations');
  const metricOpenAccess = document.getElementById('metricOpenAccess');

  if (metricTotalCitations) metricTotalCitations.textContent = totalCitations.toLocaleString();
  if (metricAvgCitations) metricAvgCitations.textContent = avgCitations;
  if (metricOpenAccess) metricOpenAccess.textContent = openAccessCount;
}

// =============================================================================
// SEARCH FUNCTIONALITY (using Lunr.js)
// =============================================================================

function initSearch() {
  if (typeof lunr === 'undefined') return;

  // Build search index from site sections and publications
  const searchData = [];

  // Add site sections - customize these for your project
  const sections = [
    { id: 'home', title: 'Home', content: 'project overview research objectives' },
    { id: 'team', title: 'Team', content: 'researchers investigators members' },
    { id: 'research', title: 'Research', content: 'methods objectives goals' },
    { id: 'publications', title: 'Publications', content: 'papers journals DOI citations' },
    { id: 'resources', title: 'Resources', content: 'datasets code data' },
    { id: 'news', title: 'News', content: 'updates announcements' },
    { id: 'events', title: 'Events', content: 'conferences presentations workshops' },
    { id: 'collaborations', title: 'Collaborations', content: 'partners universities' },
    { id: 'funding', title: 'Funding', content: 'grants money sponsors' },
    { id: 'contact', title: 'Contact', content: 'email address form' }
  ];

  // Add publications to search index
  publicationsData.forEach((pub, idx) => {
    searchData.push({
      id: `pub-${idx}`,
      title: pub.title || '',
      content: `${pub.authors || ''} ${pub.journal || ''} ${pub.year || ''}`,
      section: 'publications'
    });
  });

  sections.forEach(s => searchData.push({ ...s, section: s.id }));

  searchIndex = lunr(function() {
    this.ref('id');
    this.field('title', { boost: 10 });
    this.field('content');

    searchData.forEach(doc => {
      this.add(doc);
    });
  });

  // Store data for results display
  window.searchData = searchData;
}

function performSearch(query) {
  const resultsContainer = document.getElementById('searchResults');
  if (!resultsContainer || !searchIndex || !query.trim()) {
    if (resultsContainer) resultsContainer.innerHTML = '';
    return;
  }

  try {
    const results = searchIndex.search(query + '*');

    if (results.length === 0) {
      resultsContainer.innerHTML = '<div class="search-result-item">No results found</div>';
      return;
    }

    const html = results.slice(0, 5).map(result => {
      const item = window.searchData.find(d => d.id === result.ref);
      if (!item) return '';

      const href = item.id.startsWith('pub-') ? '#publications' : `#${item.id}`;
      const sectionLabel = item.section.charAt(0).toUpperCase() + item.section.slice(1);

      return `
        <a href="${href}" class="search-result-item" onclick="closeSidebarOnMobile()">
          <div class="result-title">${item.title}</div>
          <div class="result-section">${sectionLabel}</div>
        </a>
      `;
    }).join('');

    resultsContainer.innerHTML = html;
  } catch (e) {
    resultsContainer.innerHTML = '';
  }
}

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
  // Initialize theme from localStorage
  initTheme();

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Highlight active navigation on scroll
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-menu a');
  const sidebarLinks = document.querySelectorAll('.sidebar-nav a');

  function highlightNav() {
    let scrollPos = window.scrollY + 100;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
        sidebarLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', highlightNav);
  highlightNav();

  // Add scroll shadow to nav
  const navContainer = document.querySelector('.nav-container');
  if (navContainer) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        navContainer.classList.add('scrolled');
      } else {
        navContainer.classList.remove('scrolled');
      }
    });
  }

  // Initialize features
  initMobileMenuClose();
  initBackToTop();

  // Wait for publicationsData to be set by Jekyll
  setTimeout(() => {
    initPublicationFilters();
    updateCitationMetrics();
    initSearch();
  }, 100);
});
