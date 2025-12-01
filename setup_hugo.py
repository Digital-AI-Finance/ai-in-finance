"""
Setup Hugo project structure with theme and configuration.
"""

import os
import subprocess
from pathlib import Path


class HugoSetup:
    """Setup Hugo project with theme and config."""

    def __init__(self, hugo_dir: str = "hugo_site"):
        self.hugo_dir = Path(hugo_dir)
        self.themes_dir = self.hugo_dir / "themes"
        self.layouts_dir = self.hugo_dir / "layouts"

    def create_config(self):
        """Create Hugo configuration file."""
        config_content = '''# Hugo configuration for AI in Finance website
baseURL = "https://digital-ai-finance.github.io/ai-in-finance/"
languageCode = "en-us"
title = "AI in Finance - UT & ING Collaboration"
theme = "PaperMod"

# Enable emoji support
enableEmoji = true

# Build settings
buildDrafts = false
buildFuture = false
buildExpired = false

# Output formats
[outputs]
  home = ["HTML", "RSS"]
  page = ["HTML"]
  section = ["HTML", "RSS"]

# Menu configuration
[menu]
  [[menu.main]]
    name = "Home"
    url = "/"
    weight = 1
  [[menu.main]]
    name = "Our People"
    url = "/our-people/"
    weight = 2
  [[menu.main]]
    name = "Research"
    url = "/ing-ut-collaboration/research/"
    weight = 3
  [[menu.main]]
    name = "Education"
    url = "/ing-ut-collaboration/education/"
    weight = 4
  [[menu.main]]
    name = "Output & Impact"
    url = "/ing-ut-collaboration/output-and-impact/"
    weight = 5

# Theme parameters
[params]
  # Site description
  description = "The ING-UT AI in Finance collaboration focuses on advanced AI applications in data handling, risk management, and business operations within the finance sector."

  # Show reading time
  ShowReadingTime = false

  # Show share buttons
  ShowShareButtons = false

  # Show breadcrumbs
  ShowBreadCrumbs = true

  # Show table of contents
  ShowToc = false

  # Enable search
  fuseOpts = { threshold = 0.3 }

  # Home info mode
  [params.homeInfoParams]
    Title = "AI in Finance"
    Content = "A collaboration between University of Twente and ING focusing on personalized financial services with AI."

  # Social icons
  [[params.socialIcons]]
    name = "github"
    url = "https://github.com/Digital-AI-Finance"

  # Assets
  [params.assets]
    favicon = "/images/favicon.ico"

  # Cover image
  [params.cover]
    hidden = false
    hiddenInList = false

# Markup configuration
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
  [markup.highlight]
    style = "monokai"
'''

        config_path = self.hugo_dir / "config.toml"
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"Created config: {config_path}")

    def create_github_workflow(self):
        """Create GitHub Actions workflow for Hugo deployment."""
        workflow_dir = self.hugo_dir / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)

        workflow_content = '''# GitHub Actions workflow for Hugo deployment
name: Deploy Hugo site to Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.120.4
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \\
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4

      - name: Install Node.js dependencies
        run: "[[ -f package-lock.json || -f npm-shrinkwrap.json ]] && npm ci || true"

      - name: Build with Hugo
        env:
          HUGO_ENVIRONMENT: production
          HUGO_ENV: production
        run: |
          hugo \\
            --gc \\
            --minify \\
            --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v3
'''

        workflow_path = workflow_dir / "hugo.yml"
        with open(workflow_path, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        print(f"Created workflow: {workflow_path}")

    def create_custom_layouts(self):
        """Create custom layouts for better styling."""
        # Create layouts directory
        partials_dir = self.layouts_dir / "partials"
        partials_dir.mkdir(parents=True, exist_ok=True)

        # Custom head partial for additional styles
        head_content = '''<!-- Custom head additions -->
<style>
  /* Custom styles for AI in Finance */
  :root {
    --primary-color: #001e50;  /* UT Blue */
    --secondary-color: #ff6600;  /* ING Orange */
  }

  .logo-container {
    display: flex;
    gap: 2rem;
    align-items: center;
    flex-wrap: wrap;
    margin: 2rem 0;
  }

  .logo-container img {
    max-height: 60px;
    width: auto;
  }

  .team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }

  .team-member {
    text-align: center;
    padding: 1rem;
    border-radius: 8px;
    background: var(--entry);
  }

  .team-member img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
  }

  .stats-container {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    justify-content: center;
    margin: 2rem 0;
  }

  .stat-item {
    text-align: center;
    padding: 1.5rem;
    background: var(--entry);
    border-radius: 8px;
    min-width: 150px;
  }

  .stat-number {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--secondary);
  }
</style>
'''

        head_path = partials_dir / "extend_head.html"
        with open(head_path, 'w', encoding='utf-8') as f:
            f.write(head_content)
        print(f"Created custom head: {head_path}")

    def install_theme(self):
        """Install PaperMod theme as git submodule."""
        self.themes_dir.mkdir(parents=True, exist_ok=True)

        # Create .gitmodules file
        gitmodules_content = '''[submodule "themes/PaperMod"]
    path = themes/PaperMod
    url = https://github.com/adityatelange/hugo-PaperMod.git
'''
        gitmodules_path = self.hugo_dir / ".gitmodules"
        with open(gitmodules_path, 'w', encoding='utf-8') as f:
            f.write(gitmodules_content)

        print(f"Created .gitmodules: {gitmodules_path}")
        print("NOTE: Run 'git submodule update --init --recursive' to install theme")

        # Try to clone theme directly
        theme_path = self.themes_dir / "PaperMod"
        if not theme_path.exists():
            try:
                subprocess.run([
                    'git', 'clone', '--depth=1',
                    'https://github.com/adityatelange/hugo-PaperMod.git',
                    str(theme_path)
                ], check=True, capture_output=True)
                print(f"Cloned PaperMod theme to: {theme_path}")
            except Exception as e:
                print(f"Could not clone theme: {e}")
                print("Please run: git clone https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod")

    def create_gitignore(self):
        """Create .gitignore file."""
        gitignore_content = '''# Hugo build output
public/
resources/

# OS files
.DS_Store
Thumbs.db

# Editor files
*.swp
*.swo
*~

# IDE
.idea/
.vscode/

# Python
__pycache__/
*.py[cod]
*.pyo

# Raw scraped site (optional - comment out if you want to include)
# raw_site/
'''
        gitignore_path = self.hugo_dir / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print(f"Created .gitignore: {gitignore_path}")

    def create_readme(self):
        """Create README.md file."""
        readme_content = '''# AI in Finance Website

This is the Hugo-based website for the AI in Finance collaboration between University of Twente and ING.

## Overview

The ING-UT AI in Finance collaboration focuses on advanced AI applications in:
- Data handling
- Risk management
- Business operations within the finance sector

## Local Development

1. Install Hugo (extended version): https://gohugo.io/installation/

2. Clone with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/Digital-AI-Finance/ai-in-finance.git
   ```

3. Start development server:
   ```bash
   cd ai-in-finance
   hugo server -D
   ```

4. Open http://localhost:1313

## Deployment

The site is automatically deployed to GitHub Pages when pushing to the `main` branch.

Live site: https://digital-ai-finance.github.io/ai-in-finance/

## Team

- **University of Twente**: 11 professors and researchers
- **ING**: 22+ team members
- **Students**: 9 MSc students, 1 PhD candidate

## Links

- [Original site](https://www.ai-in-finance.eu/)
- [Digital Finance MSCA](https://www.digital-finance-msca.com/)
- [KickStart AI](https://www.kickstartai.nl/)
'''
        readme_path = self.hugo_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"Created README: {readme_path}")

    def setup_all(self):
        """Run complete Hugo setup."""
        print("Setting up Hugo project...")
        print("=" * 60)

        # Create directories
        self.hugo_dir.mkdir(parents=True, exist_ok=True)

        # Create all configurations
        self.create_config()
        self.create_github_workflow()
        self.create_custom_layouts()
        self.create_gitignore()
        self.create_readme()
        self.install_theme()

        print("\n" + "=" * 60)
        print("HUGO SETUP COMPLETE")
        print("=" * 60)
        print(f"\nProject directory: {self.hugo_dir.absolute()}")
        print("\nNext steps:")
        print("1. cd hugo_site")
        print("2. git init")
        print("3. hugo server -D  (to test locally)")
        print("4. git add . && git commit -m 'Initial Hugo site'")
        print("5. git push to GitHub")


def main():
    """Main entry point."""
    setup = HugoSetup(hugo_dir="hugo_site")
    setup.setup_all()


if __name__ == "__main__":
    main()
