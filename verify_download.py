"""
Verify that all content from ai-in-finance.eu was downloaded.
Compares original site structure with downloaded files.
"""

import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class DownloadVerifier:
    """Verify completeness of website download."""

    def __init__(self, base_url: str, raw_dir: str = "raw_site"):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.raw_dir = Path(raw_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Track results
        self.original_pages = set()
        self.downloaded_pages = set()
        self.original_assets = set()
        self.downloaded_assets = set()
        self.missing_pages = set()
        self.missing_assets = set()

    def crawl_original_site(self, url: str = None, visited: set = None):
        """Recursively crawl original site to find all pages."""
        if url is None:
            url = self.base_url
        if visited is None:
            visited = set()

        # Normalize URL
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
        if not normalized:
            normalized = f"{parsed.scheme}://{parsed.netloc}"

        if normalized in visited:
            return
        visited.add(normalized)

        # Only process internal URLs
        if parsed.netloc != self.domain:
            return

        print(f"  Checking: {url}")
        self.original_pages.add(normalized)

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all internal links
            for a in soup.find_all('a', href=True):
                href = a.get('href')
                if href and not href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                    full_url = urljoin(url, href)
                    parsed_link = urlparse(full_url)

                    # Only follow internal links
                    if parsed_link.netloc == self.domain:
                        # Skip asset files
                        if not any(parsed_link.path.lower().endswith(ext)
                                   for ext in ['.pdf', '.jpg', '.png', '.gif', '.svg',
                                              '.css', '.js', '.zip', '.doc', '.docx']):
                            self.crawl_original_site(full_url, visited)

            # Find all assets
            # Images
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src:
                    asset_url = urljoin(url, src)
                    if urlparse(asset_url).netloc == self.domain:
                        self.original_assets.add(asset_url)

            # CSS
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href:
                    asset_url = urljoin(url, href)
                    self.original_assets.add(asset_url)

            # JS
            for script in soup.find_all('script', src=True):
                src = script.get('src')
                if src:
                    asset_url = urljoin(url, src)
                    if urlparse(asset_url).netloc == self.domain:
                        self.original_assets.add(asset_url)

        except Exception as e:
            print(f"    Error: {e}")

    def scan_downloaded_files(self):
        """Scan downloaded files in raw_site directory."""
        # Count HTML files
        for html_file in self.raw_dir.rglob('*.html'):
            # Convert file path back to URL
            rel_path = html_file.relative_to(self.raw_dir)
            parts = list(rel_path.parts)

            # Remove index.html from path
            if parts[-1] == 'index.html':
                parts = parts[:-1]

            if parts:
                url_path = '/'.join(parts)
                url = f"{self.base_url}/{url_path}"
            else:
                url = self.base_url

            self.downloaded_pages.add(url.rstrip('/'))

        # Count asset files
        asset_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico',
                          '.avif', '.css', '.js', '.mjs', '.woff', '.woff2', '.ttf', '.eot'}
        for asset_file in self.raw_dir.rglob('*'):
            if asset_file.is_file() and asset_file.suffix.lower() in asset_extensions:
                self.downloaded_assets.add(str(asset_file))

    def compare_results(self):
        """Compare original and downloaded content."""
        # Find missing pages
        for page in self.original_pages:
            normalized = page.rstrip('/')
            found = False
            for downloaded in self.downloaded_pages:
                if normalized == downloaded.rstrip('/'):
                    found = True
                    break
            if not found:
                self.missing_pages.add(page)

    def generate_report(self):
        """Generate verification report."""
        print("\n" + "=" * 70)
        print("DOWNLOAD VERIFICATION REPORT")
        print("=" * 70)

        print(f"\nOriginal Site: {self.base_url}")
        print(f"Download Dir:  {self.raw_dir.absolute()}")

        print("\n--- PAGES ---")
        print(f"Original pages found:   {len(self.original_pages)}")
        print(f"Downloaded pages:       {len(self.downloaded_pages)}")

        if self.missing_pages:
            print(f"\nMISSING PAGES ({len(self.missing_pages)}):")
            for page in sorted(self.missing_pages):
                print(f"  - {page}")
        else:
            print("\n[OK] All pages downloaded!")

        print("\n--- ASSETS ---")
        print(f"Original assets found:  {len(self.original_assets)}")
        print(f"Downloaded assets:      {len(self.downloaded_assets)}")

        print("\n--- DOWNLOADED FILES SUMMARY ---")

        # Count by type
        html_count = len(list(self.raw_dir.rglob('*.html')))
        image_count = len([f for f in self.raw_dir.rglob('*')
                          if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico', '.avif'}])
        css_count = len(list(self.raw_dir.rglob('*.css')))
        js_count = len(list(self.raw_dir.rglob('*.js'))) + len(list(self.raw_dir.rglob('*.mjs')))
        font_count = len([f for f in self.raw_dir.rglob('*')
                         if f.suffix.lower() in {'.woff', '.woff2', '.ttf', '.eot', '.otf'}])

        print(f"  HTML pages:    {html_count}")
        print(f"  Images:        {image_count}")
        print(f"  CSS files:     {css_count}")
        print(f"  JS files:      {js_count}")
        print(f"  Font files:    {font_count}")

        total_size = sum(f.stat().st_size for f in self.raw_dir.rglob('*') if f.is_file())
        print(f"\nTotal download size: {total_size / (1024*1024):.2f} MB")

        print("\n--- DOWNLOADED PAGES LIST ---")
        for i, page in enumerate(sorted(self.downloaded_pages), 1):
            print(f"  {i:2}. {page}")

        print("\n" + "=" * 70)

        # Summary verdict
        if not self.missing_pages:
            print("VERDICT: COMPLETE - All pages from the original site were downloaded")
        else:
            print(f"VERDICT: INCOMPLETE - {len(self.missing_pages)} pages missing")

        print("=" * 70)

    def verify(self):
        """Run complete verification."""
        print("Starting verification...")
        print("\n1. Crawling original site to find all pages...")
        self.crawl_original_site()

        print("\n2. Scanning downloaded files...")
        self.scan_downloaded_files()

        print("\n3. Comparing results...")
        self.compare_results()

        print("\n4. Generating report...")
        self.generate_report()


def main():
    """Main entry point."""
    verifier = DownloadVerifier(
        base_url="https://www.ai-in-finance.eu/",
        raw_dir="raw_site"
    )
    verifier.verify()


if __name__ == "__main__":
    main()
