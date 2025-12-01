"""
AI in Finance Website Scraper
Downloads entire website with all pages, images, CSS, JS, and assets.
"""

import os
import re
import time
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup


class WebsiteScraper:
    """Recursive website scraper with asset downloading."""

    def __init__(self, base_url: str, output_dir: str = "raw_site"):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Track visited URLs to avoid duplicates
        self.visited_pages = set()
        self.downloaded_assets = set()

        # Rate limiting
        self.request_delay = 0.5  # seconds between requests
        self.last_request_time = 0

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Stats
        self.stats = {
            'pages': 0,
            'images': 0,
            'css': 0,
            'js': 0,
            'fonts': 0,
            'other': 0,
            'errors': 0
        }

    def _rate_limit(self):
        """Implement polite rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self.last_request_time = time.time()

    def _normalize_url(self, url: str) -> str:
        """Normalize URL for comparison."""
        parsed = urlparse(url)
        # Remove fragment and trailing slash
        path = parsed.path.rstrip('/')
        if not path:
            path = '/'
        return f"{parsed.scheme}://{parsed.netloc}{path}"

    def _is_internal_url(self, url: str) -> bool:
        """Check if URL is internal to the site."""
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''

    def _url_to_filepath(self, url: str, is_page: bool = False) -> Path:
        """Convert URL to local file path."""
        parsed = urlparse(url)
        path = unquote(parsed.path)

        if not path or path == '/':
            path = '/index.html'
        elif is_page and not path.endswith('.html'):
            # Add index.html for directory-like URLs
            if path.endswith('/'):
                path = f"{path}index.html"
            else:
                path = f"{path}/index.html"

        # Remove leading slash and create path
        clean_path = path.lstrip('/')
        return self.output_dir / clean_path

    def _download_file(self, url: str, filepath: Path) -> bool:
        """Download a file and save it."""
        try:
            self._rate_limit()
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Create parent directories
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(filepath, 'wb') as f:
                f.write(response.content)

            return True
        except Exception as e:
            print(f"  Error downloading {url}: {e}")
            self.stats['errors'] += 1
            return False

    def _extract_urls_from_css(self, css_content: str, base_url: str) -> list:
        """Extract URLs from CSS content (fonts, images)."""
        urls = []
        # Match url(...) patterns
        pattern = r'url\(["\']?([^"\')\s]+)["\']?\)'
        for match in re.finditer(pattern, css_content):
            url = match.group(1)
            if not url.startswith('data:'):  # Skip data URIs
                full_url = urljoin(base_url, url)
                urls.append(full_url)
        return urls

    def _get_asset_type(self, url: str) -> str:
        """Determine asset type from URL."""
        path = urlparse(url).path.lower()
        if any(path.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico']):
            return 'images'
        elif path.endswith('.css'):
            return 'css'
        elif path.endswith('.js'):
            return 'js'
        elif any(path.endswith(ext) for ext in ['.woff', '.woff2', '.ttf', '.eot', '.otf']):
            return 'fonts'
        else:
            return 'other'

    def _download_asset(self, url: str) -> bool:
        """Download an asset (image, CSS, JS, font)."""
        if url in self.downloaded_assets:
            return True

        self.downloaded_assets.add(url)
        filepath = self._url_to_filepath(url)

        asset_type = self._get_asset_type(url)
        print(f"  Downloading {asset_type}: {url}")

        if self._download_file(url, filepath):
            self.stats[asset_type] += 1

            # If CSS, also download referenced assets (fonts, images)
            if asset_type == 'css':
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        css_content = f.read()
                    for ref_url in self._extract_urls_from_css(css_content, url):
                        if self._is_internal_url(ref_url) or 'fonts' in ref_url.lower():
                            self._download_asset(ref_url)
                except Exception as e:
                    print(f"  Error parsing CSS {url}: {e}")

            return True
        return False

    def scrape_page(self, url: str) -> list:
        """Scrape a single page and return found internal links."""
        normalized_url = self._normalize_url(url)
        if normalized_url in self.visited_pages:
            return []

        self.visited_pages.add(normalized_url)
        print(f"\nScraping page: {url}")

        try:
            self._rate_limit()
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Save HTML
            filepath = self._url_to_filepath(url, is_page=True)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)

            self.stats['pages'] += 1
            print(f"  Saved to: {filepath}")

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Download assets
            # Images
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src:
                    asset_url = urljoin(url, src)
                    if self._is_internal_url(asset_url):
                        self._download_asset(asset_url)

            # CSS
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href:
                    asset_url = urljoin(url, href)
                    self._download_asset(asset_url)

            # JavaScript
            for script in soup.find_all('script', src=True):
                src = script.get('src')
                if src:
                    asset_url = urljoin(url, src)
                    if self._is_internal_url(asset_url):
                        self._download_asset(asset_url)

            # Background images in style attributes
            for elem in soup.find_all(style=True):
                style = elem.get('style', '')
                for match in re.finditer(r'url\(["\']?([^"\')\s]+)["\']?\)', style):
                    asset_url = urljoin(url, match.group(1))
                    if self._is_internal_url(asset_url):
                        self._download_asset(asset_url)

            # Inline style tags
            for style in soup.find_all('style'):
                if style.string:
                    for ref_url in self._extract_urls_from_css(style.string, url):
                        if self._is_internal_url(ref_url):
                            self._download_asset(ref_url)

            # Find internal links
            internal_links = []
            for a in soup.find_all('a', href=True):
                href = a.get('href')
                if href and not href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                    full_url = urljoin(url, href)
                    if self._is_internal_url(full_url):
                        parsed = urlparse(full_url)
                        # Only follow pages, not assets
                        if not any(parsed.path.lower().endswith(ext)
                                   for ext in ['.pdf', '.jpg', '.png', '.gif', '.svg',
                                              '.css', '.js', '.zip', '.doc', '.docx']):
                            internal_links.append(full_url)

            return internal_links

        except Exception as e:
            print(f"  Error scraping {url}: {e}")
            self.stats['errors'] += 1
            return []

    def scrape_all(self):
        """Recursively scrape entire website."""
        print(f"Starting scrape of {self.base_url}")
        print(f"Output directory: {self.output_dir.absolute()}")
        print("=" * 60)

        # Start with base URL
        urls_to_visit = [self.base_url]

        while urls_to_visit:
            url = urls_to_visit.pop(0)
            new_links = self.scrape_page(url)

            # Add new links that haven't been visited
            for link in new_links:
                normalized = self._normalize_url(link)
                if normalized not in self.visited_pages and link not in urls_to_visit:
                    urls_to_visit.append(link)

        print("\n" + "=" * 60)
        print("SCRAPE COMPLETE")
        print("=" * 60)
        print(f"Pages downloaded:  {self.stats['pages']}")
        print(f"Images downloaded: {self.stats['images']}")
        print(f"CSS files:         {self.stats['css']}")
        print(f"JS files:          {self.stats['js']}")
        print(f"Font files:        {self.stats['fonts']}")
        print(f"Other files:       {self.stats['other']}")
        print(f"Errors:            {self.stats['errors']}")
        print(f"\nFiles saved to: {self.output_dir.absolute()}")


def main():
    """Main entry point."""
    scraper = WebsiteScraper(
        base_url="https://www.ai-in-finance.eu/",
        output_dir="raw_site"
    )
    scraper.scrape_all()


if __name__ == "__main__":
    main()
