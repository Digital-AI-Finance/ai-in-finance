---
layout: default
title: "AI in Finance"
description: "University of Twente and ING Bank collaboration on Artificial Intelligence in Finance"
image: /images/project-image.jpg
---

<!-- Schema.org Structured Data - Customize for your project -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ResearchProject",
  "name": "AI in Finance",
  "description": "University of Twente and ING Bank collaboration on Artificial Intelligence in Finance",
  "url": "https://Digital-AI-Finance.github.io/ai-in-finance/",
  "funder": {
    "@type": "Organization",
    "name": "ING Bank / KickStart AI",
    "url": "https://www.ing.com"
  },
  "funding": {
    "@type": "MonetaryGrant",
    "identifier": "ING-UT Collaboration",
    "amount": {
      "@type": "MonetaryAmount",
      "value": 6000000,
      "currency": "EUR"
    }
  },
  "member": [
    {
      "@type": "Person",
      "name": "Prof. Dr. Jos van Hillegersberg",
      "jobTitle": "Principal Investigator",
      "affiliation": "University of Twente"
    }
  ],
  "startDate": "2021-06-01",
  "endDate": "2026-06-01"
}
</script>

<!-- Mobile Menu Toggle -->
<button class="mobile-menu-toggle" onclick="toggleMobileMenu()" aria-label="Toggle navigation menu">
  <span class="hamburger-icon"></span>
</button>

<nav class="sidebar-nav" id="sidebarNav">
  <div class="sidebar-header">
    <div class="sidebar-title">AI in Finance</div>
    <div class="sidebar-subtitle">UT-ING Collaboration</div>
  </div>
  <!-- Search Box -->
  <div class="search-container">
    <input type="text" id="searchInput" placeholder="Search..." onkeyup="performSearch(this.value)">
    <div id="searchResults" class="search-results"></div>
  </div>
  <ul>
    <li><a href="#home">Home</a></li>
    <li><a href="#team">Team</a></li>
    <li><a href="#research">Research</a></li>
    <li><a href="#publications">Publications</a></li>
    <li><a href="#analytics">Analytics</a></li>
    <div class="nav-section">Resources</div>
    <li><a href="#resources">Datasets & Code</a></li>
    <li><a href="#news">News</a></li>
    <li><a href="#events">Events</a></li>
    <div class="nav-section">Network</div>
    <li><a href="#collaborations">Collaborations</a></li>
    <li><a href="#funding">Funding</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
  <!-- Dark Mode Toggle -->
  <div class="theme-toggle-container">
    <button class="theme-toggle" onclick="toggleDarkMode()" aria-label="Toggle dark mode">
      <span class="theme-icon">&#9790;</span> Dark Mode
    </button>
  </div>
</nav>

<nav class="nav-container">
  <ul class="nav-menu">
    <li><a href="#home">Home</a></li>
    <li><a href="#team">Team</a></li>
    <li><a href="#research">Research</a></li>
    <li><a href="#publications">Publications</a></li>
    <li><a href="#analytics">Analytics</a></li>
    <li><a href="#resources">Resources</a></li>
    <li><a href="#news">News</a></li>
    <li><a href="#events">Events</a></li>
    <li><a href="#collaborations">Collaborations</a></li>
    <li><a href="#funding">Funding</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
</nav>

<section id="home">

<div class="logo-banner">
  <img src="assets/images/logos/funder-logo.svg" alt="ING Bank / KickStart AI" loading="lazy">
  <img src="assets/images/logos/institution-logo.svg" alt="University of Twente" loading="lazy">
  <button onclick="toggleDarkMode()" class="btn-theme" aria-label="Toggle dark mode">&#9790;</button>
  <button onclick="window.print()" class="btn-pdf">Print / Save PDF</button>
</div>

<div class="stats-banner">
  <div class="stat-item">
    <span class="stat-number">6M+</span>
    <span class="stat-label">EUR Funding</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{{ site.data.publications | size }}</span>
    <span class="stat-label">Publications</span>
  </div>
  <div class="stat-item" id="totalCitations">
    <span class="stat-number">--</span>
    <span class="stat-label">Total Citations</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">20+</span>
    <span class="stat-label">Collaborations</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">35+</span>
    <span class="stat-label">Researchers</span>
  </div>
</div>

> A strategic 5-year partnership (2021-2026) between the **University of Twente** and **ING Bank** advancing artificial intelligence applications in the financial sector. Our research focuses on machine learning for risk management, explainable AI, privacy-preserving methods, and practical AI deployment in banking operations.

> *"The collaboration between ING and UT has proven to be highly beneficial for all partners involved, significantly expanding ING's access to a highly educated talent base."* - **Leon Dusee, COO Risk Department, ING**

</section>

---

<section id="team">

<h2>Our Team</h2>

<em>Our team combines academic expertise from the University of Twente with industry practitioners from ING Bank, creating a unique blend of research and real-world application.</em>

<div class="team-grid">
{% for member in site.data.team %}
<div class="team-card" itemscope itemtype="https://schema.org/Person">
  <img src="{{ member.image }}" alt="{{ member.name }}" loading="lazy" itemprop="image">
  <span class="role-badge">{{ member.role }}</span>
  <h4 itemprop="name">{{ member.name }}</h4>
  <p class="institution" itemprop="affiliation">{{ member.institution }}{% if member.institution2 %}<br>{{ member.institution2 }}{% endif %}</p>
  <p class="bio" itemprop="description">{{ member.bio }}</p>
  <div class="profile-links">
    {% if member.orcid %}<a href="https://orcid.org/{{ member.orcid }}" target="_blank" rel="noopener" title="ORCID" class="orcid-link external-link"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png" alt="ORCID" loading="lazy"> ORCID</a>{% endif %}
    {% if member.google_scholar %}<a href="{{ member.google_scholar }}" target="_blank" rel="noopener" title="Google Scholar" class="external-link">Scholar</a>{% endif %}
    {% if member.linkedin %}<a href="{{ member.linkedin }}" target="_blank" rel="noopener" title="LinkedIn" class="external-link">LinkedIn</a>{% endif %}
    {% if member.website %}<a href="{{ member.website }}" target="_blank" rel="noopener" title="Website" class="external-link">Web</a>{% endif %}
  </div>
</div>
{% endfor %}
</div>

</section>

---

<section id="research">

<h2>Research Project</h2>

<h3>Background</h3>

The financial industry is undergoing rapid transformation driven by artificial intelligence and data science. Banks face increasing pressure to leverage AI for risk management, customer service, and operational efficiency while ensuring regulatory compliance and ethical AI deployment.

The ING-UT collaboration brings together academic research excellence with industry expertise to address these challenges through joint research projects, MSc thesis supervision, and knowledge exchange.

<h3>Rationale</h3>

The partnership addresses a critical talent gap in AI and finance. By combining UT's academic strengths in AI, data science, and information systems with ING's practical expertise in banking operations, risk management, and regulatory compliance, we create valuable synergies that benefit both institutions and the broader financial sector.

<h3>Objectives</h3>

**Research Objectives:**
- Develop machine learning methods for credit risk assessment and early warning systems
- Create explainable AI models that meet regulatory requirements
- Advance privacy-preserving techniques including federated learning and synthetic data generation
- Build practical AI applications for banking operations

**Educational Objectives:**
- Train MSc students through thesis projects at ING
- Develop curriculum in AI and Finance
- Foster knowledge exchange between academia and industry

<h3>Methods</h3>

Our research combines rigorous academic methodology with practical industry validation:

- **Machine Learning**: Deep learning, ensemble methods, meta-labeling techniques
- **Explainable AI**: SHAP, LIME, inherently interpretable models
- **Privacy-Preserving ML**: Federated learning, differential privacy, synthetic data
- **NLP**: Large language models for document analysis and information extraction
- **Network Analysis**: Graph-based risk modeling and client relationship analysis

<h3>Expected Impact</h3>

**Academic Impact:**
- 50+ peer-reviewed publications in top AI and finance journals
- Multiple PhD defenses and MSc thesis completions
- Active participation in leading conferences (ICAIF, NeurIPS, AAAI)

**Industry Impact:**
- Direct implementation of research findings in ING's banking operations
- Training programs for ING practitioners
- Open-source tools and methodologies for the broader community

</section>

---

<section id="publications">

<h2>Scientific Publications</h2>

<em>Auto-updated from <a href="https://openalex.org" target="_blank" rel="noopener" class="external-link">OpenAlex.org</a> - {{ site.data.publications | size }} publications</em>

<!-- Citation Metrics Summary -->
<div class="citation-metrics" id="citationMetrics">
  <div class="metric-card">
    <span class="metric-value" id="metricTotalPubs">{{ site.data.publications | size }}</span>
    <span class="metric-label">Publications</span>
  </div>
  <div class="metric-card">
    <span class="metric-value" id="metricTotalCitations">--</span>
    <span class="metric-label">Total Citations</span>
  </div>
  <div class="metric-card">
    <span class="metric-value" id="metricAvgCitations">--</span>
    <span class="metric-label">Avg. Citations</span>
  </div>
  <div class="metric-card">
    <span class="metric-value" id="metricOpenAccess">--</span>
    <span class="metric-label">Open Access</span>
  </div>
</div>

<!-- Publication Filters - Customize topic options for your research area -->
<div class="pub-filters">
  <div class="filter-group">
    <label for="yearFilter">Year:</label>
    <select id="yearFilter" onchange="filterPublications()">
      <option value="all">All Years</option>
    </select>
  </div>
  <div class="filter-group">
    <label for="topicFilter">Topic:</label>
    <select id="topicFilter" onchange="filterPublications()">
      <option value="all">All Topics</option>
      <option value="topic1">Machine Learning</option>
      <option value="topic2">Risk Management</option>
      <option value="topic3">Explainable AI</option>
    </select>
  </div>
  <div class="filter-group">
    <label for="accessFilter">Access:</label>
    <select id="accessFilter" onchange="filterPublications()">
      <option value="all">All</option>
      <option value="open">Open Access</option>
    </select>
  </div>
  <button onclick="resetFilters()" class="btn-reset">Reset</button>
</div>

<div class="pub-actions">
  <button onclick="downloadAllBibtex()" class="btn-download">Download All BibTeX (.bib)</button>
</div>

<div class="publication-list" id="publicationList">
{% for pub in site.data.publications %}
<div class="pub-item" data-year="{{ pub.year }}" data-title="{{ pub.title | downcase }}" data-open="{{ pub.open_access }}">
  <div class="pub-title">{{ pub.title }}</div>
  <div class="pub-meta">{{ pub.authors }} ({{ pub.year }}) - <em>{{ pub.journal }}</em></div>
  <div class="pub-badges">
    {% if pub.doi %}<a href="https://doi.org/{{ pub.doi }}" class="doi-link external-link" target="_blank" rel="noopener">DOI</a>{% endif %}
    {% if pub.citations > 0 %}<span class="citations-badge">{{ pub.citations }} citations</span>{% endif %}
    {% if pub.open_access %}<span class="oa-badge">Open Access</span>{% endif %}
    <button onclick="copyBibtex({{ forloop.index0 }})" data-bibtex-index="{{ forloop.index0 }}" class="btn-bibtex">BibTeX</button>
    {% if pub.abstract and pub.abstract != "" %}<button onclick="toggleAbstract({{ forloop.index0 }})" data-abstract-btn="{{ forloop.index0 }}" class="btn-abstract">Show Abstract</button>{% endif %}
  </div>
  {% if pub.abstract and pub.abstract != "" %}
  <div class="pub-abstract" data-abstract-index="{{ forloop.index0 }}" style="display: none;">{{ pub.abstract }}</div>
  {% endif %}
</div>
{% endfor %}
</div>

<script>
  publicationsData = {{ site.data.publications | jsonify }};
</script>

</section>

---

<section id="analytics">

<h2>Research Analytics</h2>

<div class="analytics-section">
  <div class="chart-container">
    <h3>Publications by Year</h3>
    <canvas id="pubsChart"></canvas>
  </div>
  <div class="chart-container">
    <h3>Co-authorship Network</h3>
    <div id="networkGraph"></div>
  </div>
</div>

<h3>Project Timeline</h3>

<div class="timeline">
  <div class="timeline-item">
    <span class="timeline-date">June 2022</span>
    <div class="timeline-content">
      <strong>Partnership Launch</strong>
      <p>ING and UT sign 5-year collaboration agreement at FinanceCom 2022</p>
    </div>
  </div>
  <div class="timeline-item">
    <span class="timeline-date">March 2024</span>
    <div class="timeline-content">
      <strong>MSCA Digital Finance</strong>
      <p>Launch of EUR 3.8M Horizon Europe doctoral network with 17 PhD positions</p>
    </div>
  </div>
  <div class="timeline-item">
    <span class="timeline-date">2025-2026</span>
    <div class="timeline-content">
      <strong>Scaling Impact</strong>
      <p>Expanding research collaborations and industry implementation</p>
    </div>
  </div>
  <!-- Add more timeline items as needed -->
</div>

</section>

---

<section id="resources">

<h2>Datasets & Code</h2>

<em>Research materials and code repositories from our project</em>

<div class="resource-grid">
  <div class="resource-card">
    <h4>ING Thesis Projects</h4>
    <p>MSc thesis opportunities at ING in AI and finance applications</p>
    <div class="resource-links">
      <a href="#resources" class="resource-link external-link" target="_blank" rel="noopener">View Theses</a>
    </div>
  </div>
  <div class="resource-card">
    <h4>Course Materials</h4>
    <p>Educational resources on AI in Finance topics</p>
    <div class="resource-links">
      <a href="#resources" class="resource-link external-link" target="_blank" rel="noopener">Learn More</a>
    </div>
  </div>
  <div class="resource-card">
    <h4>Publications Data (JSON)</h4>
    <p>Auto-updated publication metadata from OpenAlex API</p>
    <div class="resource-links">
      <a href="https://github.com/Digital-AI-Finance/ai-in-finance/blob/main/_data/publications.json" class="resource-link external-link" target="_blank" rel="noopener">View JSON</a>
      <button onclick="downloadAllBibtex()" class="resource-link">Download BibTeX</button>
    </div>
  </div>
  <div class="resource-card">
    <h4>Project Documentation</h4>
    <p>Wiki with detailed methodology, results, and supplementary materials</p>
    <div class="resource-links">
      <a href="https://github.com/Digital-AI-Finance/ai-in-finance/wiki" class="resource-link external-link" target="_blank" rel="noopener">Project Wiki</a>
    </div>
  </div>
</div>

</section>

---

<section id="news">

<h2>News & Updates</h2>

<p class="rss-link"><a href="{{ site.baseurl }}/feed.xml" class="external-link" target="_blank" rel="noopener">Subscribe via RSS</a></p>

<div class="news-list">
{% for item in site.data.news %}
<div class="news-item" itemscope itemtype="https://schema.org/NewsArticle">
  <span class="news-date" itemprop="datePublished">{{ item.date }}</span>
  <div class="news-content">
    <strong itemprop="headline">{{ item.title }}</strong>
    <p itemprop="description">{{ item.description }}</p>
  </div>
</div>
{% endfor %}
</div>

</section>

---

<section id="events">

<h2>Academic Events</h2>

<em>We regularly organize training events, workshops, and conference sessions bringing together researchers and practitioners in AI and finance.</em>

<!-- Add event image if available -->
<!-- <img src="images/event-photo.jpg" alt="Event Name" class="event-image" loading="lazy"> -->

<h3>MSCA Digital Finance Training Week 2025</h3>

The Marie Curie doctoral network organizes intensive training weeks for PhD candidates. The February 2025 training at University of Twente focuses on **Reinforcement Learning in Digital Finance**.

**Date:** February 17-21, 2025
**Location:** University of Twente, Enschede, Netherlands
**Topics:** Deep RL, trading strategies, risk management optimization

<h3>Conference Presentations</h3>

<table>
  <thead>
    <tr><th>Event</th><th>Date</th><th>Location</th><th>Contribution</th></tr>
  </thead>
  <tbody>
    <tr><td><strong>MSCA Mid-Term Meeting</strong></td><td>Nov 2024</td><td>Online/Hybrid</td><td>Progress review, all PhD candidates</td></tr>
    <tr><td><strong>ING-UT Workshop</strong></td><td>Jun 2024</td><td>ING Amsterdam</td><td>Data Analytics & Quantitative Models</td></tr>
    <!-- Add more events as needed -->
  </tbody>
</table>

</section>

---

<section id="collaborations">

<h2>Collaborations</h2>

<table>
  <thead>
    <tr><th>Institution</th><th>Contact</th><th>Activities</th></tr>
  </thead>
  <tbody>
    <tr><td><strong>ING Bank</strong></td><td>Leon Dusee (COO Risk)</td><td>Joint research, MSc supervision, knowledge exchange</td></tr>
    <tr><td><strong>KickStart AI</strong></td><td>National AI Initiative</td><td>AI education, talent development, innovation</td></tr>
    <!-- Add more collaborations as needed -->
  </tbody>
</table>

<h3>Research Networks</h3>

We actively participate in major European research networks:

**MSCA Digital Finance** - Marie Curie Industrial Doctoral Network with 17 PhD candidates across 18 European institutions including ECB and BIS.

**COST FinAI (CA19130)** - Pan-European network connecting 360 researchers from 51 countries working on fintech and AI in finance.

**SNSF Projects** - Swiss National Science Foundation funded research on narrative finance and network-based credit risk modeling.

</section>

---

<section id="funding">

<h2>Third-Party Funds</h2>

<em>Our research is supported by major funding from industry partnerships and European research programs.</em>

{% for fund in site.data.funding %}
<div class="funding-card">
  <h3>{{ fund.title }}</h3>
  <span class="funding-amount">{{ fund.amount }}</span>
  <dl class="funding-details">
    <dt>Grant Number</dt>
    <dd>{{ fund.grant_number }}</dd>
    <dt>Grant Period</dt>
    <dd>{{ fund.period }}</dd>
    <dt>Institution</dt>
    <dd>{{ fund.institution }}</dd>
    <dt>Team</dt>
    <dd>{{ fund.team }}</dd>
  </dl>
</div>
{% endfor %}

<div class="text-center mt-2">
  <h3>Total Funding Secured: EUR 6M+</h3>
</div>

</section>

---

<section id="contact">

<h2>Contact Us</h2>

<div class="contact-section">

<!-- Replace with your Formspree endpoint or other form handler -->
<form class="contact-form" action="https://formspree.io/f/xyzgqwkl" method="POST">
  <div class="form-group">
    <label for="name">Your Name</label>
    <input type="text" id="name" name="name" required placeholder="Enter your full name">
  </div>
  <div class="form-group">
    <label for="email">Email Address</label>
    <input type="email" id="email" name="email" required placeholder="Enter your email">
  </div>
  <div class="form-group">
    <label for="subject">Subject</label>
    <input type="text" id="subject" name="subject" required placeholder="What is this regarding?">
  </div>
  <div class="form-group">
    <label for="message">Message</label>
    <textarea id="message" name="message" required placeholder="Your message..."></textarea>
  </div>
  <button type="submit">Send Message</button>
</form>

<div class="text-center mt-2">
  <p><strong>Principal Investigator:</strong> Prof. Dr. Jos van Hillegersberg</p>
  <p><strong>Institution:</strong> University of Twente</p>
  <p><strong>Address:</strong> University of Twente, Faculty of BMS, Drienerlolaan 5, 7522 NB Enschede, Netherlands</p>
</div>

</div>

</section>

---

<footer class="site-footer">
  <div class="footer-content">
    <div>
      <p>&copy; 2025 Digital-AI-Finance</p>
      <p>AI in Finance - University of Twente & ING Bank Collaboration</p>
    </div>
    <div class="footer-links">
      <a href="https://github.com/Digital-AI-Finance/ai-in-finance" target="_blank" rel="noopener" class="external-link">GitHub</a>
      <a href="https://github.com/Digital-AI-Finance/ai-in-finance/wiki" target="_blank" rel="noopener" class="external-link">Wiki</a>
      <a href="{{ site.baseurl }}/feed.xml" target="_blank" rel="noopener">RSS Feed</a>
    </div>
  </div>
</footer>

<!-- Back to Top Button -->
<button id="backToTop" class="back-to-top" onclick="scrollToTop()" aria-label="Back to top">
  &#8593;
</button>

<!-- External Libraries -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.9/lunr.min.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/visualizations.js"></script>
