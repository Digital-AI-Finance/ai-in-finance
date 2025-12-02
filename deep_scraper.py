"""
Deep Scraper - Unlimited Depth Website Crawler
Downloads ALL pages from ai-in-finance.eu with no depth limit.
Also follows external links to team profiles (people.utwente.nl).
"""

import hashlib
import json
import re
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup


class DeepScraper:
    """Unlimited depth web scraper for ai-in-finance.eu."""

    def __init__(self, base_url: str, output_dir: str = "raw_site_new"):
        self.base_url = base_url.rstrip('/')
        self.primary_domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Allowed domains to crawl
        self.allowed_domains = {
            self.primary_domain,
            'www.ai-in-finance.eu',
            'ai-in-finance.eu',
        }

        # External domains to also download (team profiles, etc.)
        self.external_domains = {
            'people.utwente.nl',
        }

        # Session setup
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

        # Tracking
        self.visited_urls = set()
        self.discovered_urls = set()
        self.downloaded_pages = []
        self.downloaded_assets = []
        self.external_links = []
        self.failed_urls = []

        # Rate limiting
        self.request_delay = 0.5  # seconds between requests

        # Asset extensions
        self.asset_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico', '.avif',
            '.css', '.js', '.mjs',
            '.woff', '.woff2', '.ttf', '.eot', '.otf',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.rar', '.7z',
            '.mp4', '.webm', '.mp3', '.wav',
        }

    def is_internal_url(self, url: str) -> bool:
        """Check if URL is internal to allowed domains."""
        parsed = urlparse(url)
        return parsed.netloc in self.allowed_domains or parsed.netloc == ''

    def is_external_profile(self, url: str) -> bool:
        """Check if URL is an external profile we want to capture."""
        parsed = urlparse(url)
        return parsed.netloc in self.external_domains

    def is_asset_url(self, url: str) -> bool:
        """Check if URL points to an asset file."""
        parsed = urlparse(url)
        path_lower = parsed.path.lower()
        return any(path_lower.endswith(ext) for ext in self.asset_extensions)

    def normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication."""
        parsed = urlparse(url)
        # Remove fragment
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        # Remove trailing slash for consistency (except root)
        if normalized.endswith('/') and len(parsed.path) > 1:
            normalized = normalized.rstrip('/')
        return normalized

    def url_to_filepath(self, url: str, is_asset: bool = False) -> Path:
        """Convert URL to local file path."""
        parsed = urlparse(url)
        path = unquote(parsed.path).strip('/')

        if not path:
            path = 'index.html'
        elif not is_asset and not path.endswith('.html'):
            path = f"{path}/index.html"

        # Handle external domains
        if parsed.netloc and parsed.netloc != self.primary_domain:
            path = f"_external/{parsed.netloc}/{path}"

        return self.output_dir / path

    def download_page(self, url: str) -> tuple[str, BeautifulSoup] | None:
        """Download a page and return its content and parsed HTML."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            content_type = response.headers.get('content-type', '')
            if 'text/html' not in content_type.lower():
                return None

            return response.text, BeautifulSoup(response.text, 'html.parser')

        except Exception as e:
            print(f"    [ERROR] {url}: {e}")
            self.failed_urls.append({'url': url, 'error': str(e)})
            return None

    def download_asset(self, url: str) -> bool:
        """Download an asset file."""
        try:
            response = self.session.get(url, timeout=60, stream=True)
            response.raise_for_status()

            filepath = self.url_to_filepath(url, is_asset=True)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True

        except Exception as e:
            print(f"    [ERROR] Asset {url}: {e}")
            return False

    def save_page(self, url: str, content: str):
        """Save HTML page to file."""
        filepath = self.url_to_filepath(url)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')

    def extract_links(self, url: str, soup: BeautifulSoup) -> tuple[set, set]:
        """Extract internal links and assets from a page."""
        links = set()
        assets = set()

        # Extract all links
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                continue

            full_url = urljoin(url, href)
            normalized = self.normalize_url(full_url)

            if self.is_asset_url(full_url):
                assets.add(full_url)
            elif self.is_internal_url(full_url):
                links.add(normalized)
            elif self.is_external_profile(full_url):
                self.external_links.append(full_url)

        # Extract images
        for img in soup.find_all(['img', 'source']):
            for attr in ['src', 'data-src', 'srcset']:
                src = img.get(attr, '')
                if src:
                    # Handle srcset
                    if ',' in src:
                        for part in src.split(','):
                            src_url = part.strip().split()[0]
                            if src_url:
                                assets.add(urljoin(url, src_url))
                    else:
                        assets.add(urljoin(url, src))

        # Extract CSS
        for link in soup.find_all('link'):
            href = link.get('href', '')
            if href:
                assets.add(urljoin(url, href))

        # Extract JS
        for script in soup.find_all('script', src=True):
            src = script.get('src', '')
            if src:
                assets.add(urljoin(url, src))

        # Extract video/audio
        for media in soup.find_all(['video', 'audio']):
            src = media.get('src', '')
            if src:
                assets.add(urljoin(url, src))
            poster = media.get('poster', '')
            if poster:
                assets.add(urljoin(url, poster))

        # Extract from inline styles
        style_pattern = re.compile(r'url\([\'"]?([^\'")]+)[\'"]?\)')
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            for match in style_pattern.findall(style):
                if not match.startswith('data:'):
                    assets.add(urljoin(url, match))

        # Extract from style tags
        for style in soup.find_all('style'):
            if style.string:
                for match in style_pattern.findall(style.string):
                    if not match.startswith('data:'):
                        assets.add(urljoin(url, match))

        return links, assets

    def crawl(self):
        """Perform BFS crawl with unlimited depth."""
        print("=" * 70)
        print("DEEP SCRAPER - Unlimited Depth Crawler")
        print("=" * 70)
        print(f"Base URL: {self.base_url}")
        print(f"Output:   {self.output_dir.absolute()}")
        print("=" * 70)

        # Queue for BFS - (url, depth)
        queue = deque([(self.base_url, 0)])
        all_assets = set()

        print("\n[1/3] Crawling pages (unlimited depth)...")

        while queue:
            url, depth = queue.popleft()
            normalized = self.normalize_url(url)

            if normalized in self.visited_urls:
                continue

            self.visited_urls.add(normalized)
            self.discovered_urls.add(normalized)

            print(f"  [{len(self.downloaded_pages)+1}] Depth {depth}: {url}")

            result = self.download_page(url)
            if result is None:
                continue

            content, soup = result

            # Save page
            self.save_page(url, content)
            self.downloaded_pages.append({
                'url': url,
                'depth': depth,
                'filepath': str(self.url_to_filepath(url))
            })

            # Extract links and assets
            links, assets = self.extract_links(url, soup)
            all_assets.update(assets)

            # Add new links to queue
            for link in links:
                if link not in self.visited_urls:
                    queue.append((link, depth + 1))

            time.sleep(self.request_delay)

        print(f"\n  Total pages discovered: {len(self.downloaded_pages)}")

        # Download assets
        print(f"\n[2/3] Downloading assets ({len(all_assets)} found)...")
        downloaded_count = 0
        for i, asset_url in enumerate(sorted(all_assets), 1):
            if self.is_internal_url(asset_url):
                print(f"  [{i}/{len(all_assets)}] {asset_url[:80]}...")
                if self.download_asset(asset_url):
                    self.downloaded_assets.append(asset_url)
                    downloaded_count += 1
                time.sleep(self.request_delay / 2)

        print(f"  Downloaded: {downloaded_count} assets")

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate detailed crawl report."""
        print("\n[3/3] Generating report...")

        report = {
            'base_url': self.base_url,
            'total_pages': len(self.downloaded_pages),
            'total_assets': len(self.downloaded_assets),
            'failed_urls': len(self.failed_urls),
            'external_links': list(set(self.external_links)),
            'pages': self.downloaded_pages,
            'assets': self.downloaded_assets,
            'failed': self.failed_urls,
        }

        # Save JSON report
        report_path = self.output_dir / '_crawl_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # Print summary
        print("\n" + "=" * 70)
        print("CRAWL COMPLETE")
        print("=" * 70)
        print(f"Pages downloaded:    {len(self.downloaded_pages)}")
        print(f"Assets downloaded:   {len(self.downloaded_assets)}")
        print(f"Failed URLs:         {len(self.failed_urls)}")
        print(f"External links:      {len(set(self.external_links))}")

        # Group pages by depth
        depth_counts = {}
        for page in self.downloaded_pages:
            d = page['depth']
            depth_counts[d] = depth_counts.get(d, 0) + 1

        print("\nPages by depth:")
        for depth in sorted(depth_counts.keys()):
            print(f"  Depth {depth}: {depth_counts[depth]} pages")

        # List all pages
        print("\nDownloaded pages:")
        for i, page in enumerate(sorted(self.downloaded_pages, key=lambda x: x['url']), 1):
            print(f"  {i:3}. {page['url']}")

        # List external links found
        if self.external_links:
            print(f"\nExternal profile links found ({len(set(self.external_links))}):")
            for link in sorted(set(self.external_links))[:20]:
                print(f"  - {link}")
            if len(set(self.external_links)) > 20:
                print(f"  ... and {len(set(self.external_links)) - 20} more")

        if self.failed_urls:
            print("\nFailed URLs:")
            for fail in self.failed_urls:
                print(f"  - {fail['url']}: {fail['error']}")

        print(f"\nReport saved: {report_path}")
        print("=" * 70)


def compare_with_existing(new_dir: str = "raw_site_new", old_dir: str = "raw_site"):
    """Compare new crawl with existing download."""
    new_path = Path(new_dir)
    old_path = Path(old_dir)

    if not old_path.exists():
        print("No existing download to compare.")
        return

    print("\n" + "=" * 70)
    print("COMPARISON: New vs Existing Download")
    print("=" * 70)

    # Count files
    new_html = set(f.relative_to(new_path) for f in new_path.rglob('*.html'))
    old_html = set(f.relative_to(old_path) for f in old_path.rglob('*.html'))

    new_only = new_html - old_html
    old_only = old_html - new_html

    print(f"New download:      {len(new_html)} HTML files")
    print(f"Existing download: {len(old_html)} HTML files")

    if new_only:
        print(f"\nNEW pages found ({len(new_only)}):")
        for f in sorted(new_only):
            print(f"  + {f}")

    if old_only:
        print(f"\nPages in old but not new ({len(old_only)}):")
        for f in sorted(old_only):
            print(f"  - {f}")

    if not new_only and not old_only:
        print("\nNo differences in page structure.")

    print("=" * 70)


def main():
    """Main entry point."""
    scraper = DeepScraper(
        base_url="https://www.ai-in-finance.eu/",
        output_dir="raw_site_new"
    )
    scraper.crawl()

    # Compare with existing
    compare_with_existing()


if __name__ == "__main__":
    main()
