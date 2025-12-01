"""
Convert scraped HTML to Hugo markdown files.
Extracts content from UT website HTML and creates Hugo-compatible markdown.
"""

import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
import html2text


class HugoConverter:
    """Convert scraped HTML to Hugo markdown."""

    def __init__(self, raw_dir: str = "raw_site", hugo_dir: str = "hugo_site"):
        self.raw_dir = Path(raw_dir)
        self.hugo_dir = Path(hugo_dir)
        self.content_dir = self.hugo_dir / "content"
        self.static_dir = self.hugo_dir / "static"

        # HTML to Markdown converter
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.body_width = 0  # No line wrapping

        # Stats
        self.stats = {
            'pages': 0,
            'images': 0,
            'errors': 0
        }

    def setup_directories(self):
        """Create Hugo directory structure."""
        dirs = [
            self.hugo_dir,
            self.content_dir,
            self.static_dir,
            self.static_dir / "images",
            self.static_dir / "css",
            self.static_dir / "js",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title from HTML."""
        # Try meta title
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Remove " | University of Twente" suffix
            title = re.sub(r'\s*\|\s*University of Twente.*$', '', title)
            return title

        # Try h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)

        return "Untitled"

    def extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description from meta tag."""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta:
            return meta.get('content', '')

        # Try first paragraph
        first_p = soup.find('p')
        if first_p:
            text = first_p.get_text(strip=True)[:200]
            return text

        return ""

    def extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content area from HTML."""
        # Try to find main content container
        # UT sites use specific classes
        content_selectors = [
            'main',
            '.content',
            '.main-content',
            'article',
            '.article-content',
            '#content',
            '.page-content',
        ]

        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                # Remove navigation, header, footer
                for tag in content.find_all(['nav', 'header', 'footer', 'script', 'style']):
                    tag.decompose()
                return content

        # Fallback: try body
        body = soup.find('body')
        if body:
            for tag in body.find_all(['nav', 'header', 'footer', 'script', 'style', 'head']):
                tag.decompose()
            return body

        return soup

    def fix_image_paths(self, content: str, page_path: Path) -> str:
        """Fix image paths to point to Hugo static folder."""
        # Pattern to match image paths
        patterns = [
            (r'!\[([^\]]*)\]\((/[^\)]+)\)', r'![\1](/images\2)'),  # Markdown
            (r'src="(/[^"]+)"', r'src="/images\1"'),  # HTML src
            (r"src='(/[^']+)'", r"src='/images\1'"),  # HTML src single quotes
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        return content

    def html_to_markdown(self, html_content: str) -> str:
        """Convert HTML content to Markdown."""
        try:
            markdown = self.h2t.handle(html_content)
            # Clean up excessive whitespace
            markdown = re.sub(r'\n{3,}', '\n\n', markdown)
            return markdown.strip()
        except Exception as e:
            print(f"  Error converting HTML: {e}")
            return html_content

    def create_front_matter(self, title: str, description: str, weight: int = 1) -> str:
        """Create Hugo front matter in YAML format."""
        # Escape quotes in title and description
        title = title.replace('"', '\\"')
        description = description.replace('"', '\\"')

        front_matter = f'''---
title: "{title}"
description: "{description}"
weight: {weight}
draft: false
---

'''
        return front_matter

    def convert_page(self, html_path: Path) -> bool:
        """Convert a single HTML page to Hugo markdown."""
        try:
            # Read HTML
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract metadata
            title = self.extract_title(soup)
            description = self.extract_description(soup)

            # Extract main content
            main_content = self.extract_main_content(soup)
            if main_content:
                content_html = str(main_content)
            else:
                content_html = html_content

            # Convert to Markdown
            markdown_content = self.html_to_markdown(content_html)

            # Fix image paths
            markdown_content = self.fix_image_paths(markdown_content, html_path)

            # Create front matter
            front_matter = self.create_front_matter(title, description)

            # Determine output path
            rel_path = html_path.relative_to(self.raw_dir)
            # Convert path: raw_site/Our-People/index.html -> content/our-people/_index.md
            parts = list(rel_path.parts)

            # Handle index.html
            if parts[-1] == 'index.html':
                parts[-1] = '_index.md'
            else:
                parts[-1] = parts[-1].replace('.html', '.md')

            # Lowercase paths
            parts = [p.lower() for p in parts]

            output_path = self.content_dir.joinpath(*parts)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write markdown file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(front_matter)
                f.write(markdown_content)

            print(f"  Converted: {html_path.name} -> {output_path.relative_to(self.hugo_dir)}")
            self.stats['pages'] += 1
            return True

        except Exception as e:
            print(f"  Error converting {html_path}: {e}")
            self.stats['errors'] += 1
            return False

    def copy_assets(self):
        """Copy images and other assets to Hugo static folder."""
        print("\nCopying assets...")

        # Image extensions
        image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico', '.avif'}
        css_exts = {'.css'}
        js_exts = {'.js', '.mjs'}
        font_exts = {'.woff', '.woff2', '.ttf', '.eot', '.otf'}

        for file_path in self.raw_dir.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower()

                if ext in image_exts:
                    dest = self.static_dir / "images" / file_path.relative_to(self.raw_dir)
                elif ext in css_exts:
                    dest = self.static_dir / "css" / file_path.name
                elif ext in js_exts:
                    dest = self.static_dir / "js" / file_path.name
                elif ext in font_exts:
                    dest = self.static_dir / "fonts" / file_path.name
                else:
                    continue

                dest.parent.mkdir(parents=True, exist_ok=True)

                if not dest.exists():
                    shutil.copy2(file_path, dest)
                    self.stats['images'] += 1

        print(f"  Copied {self.stats['images']} assets")

    def convert_all(self):
        """Convert all HTML files to Hugo markdown."""
        print(f"Converting HTML to Hugo markdown...")
        print(f"Source: {self.raw_dir.absolute()}")
        print(f"Output: {self.hugo_dir.absolute()}")
        print("=" * 60)

        # Setup directories
        self.setup_directories()

        # Find all HTML files
        html_files = list(self.raw_dir.rglob('*.html'))
        print(f"\nFound {len(html_files)} HTML files")

        # Convert each file
        for html_path in html_files:
            # Skip certain files
            if '.wh' in str(html_path) or '.publisher' in str(html_path):
                continue
            self.convert_page(html_path)

        # Copy assets
        self.copy_assets()

        print("\n" + "=" * 60)
        print("CONVERSION COMPLETE")
        print("=" * 60)
        print(f"Pages converted: {self.stats['pages']}")
        print(f"Assets copied:   {self.stats['images']}")
        print(f"Errors:          {self.stats['errors']}")
        print(f"\nOutput: {self.hugo_dir.absolute()}")


def main():
    """Main entry point."""
    converter = HugoConverter(
        raw_dir="raw_site",
        hugo_dir="hugo_site"
    )
    converter.convert_all()


if __name__ == "__main__":
    main()
