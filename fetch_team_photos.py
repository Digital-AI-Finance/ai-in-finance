"""
Fetch Team Photos - Download profile photos from people.utwente.nl.

Searches for team members mentioned in the site and downloads their
profile photos from the UT people directory.
"""

import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class TeamPhotoFetcher:
    """Fetch team member photos from people.utwente.nl."""

    def __init__(self, content_dir: str = "content", output_dir: str = "static/images/team"):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Known team member URLs from crawl report
        self.team_urls = [
            "https://people.utwente.nl/joerg.osterrieder",
            "https://people.utwente.nl/r.effing",
            "https://people.utwente.nl/j.huellmann",
            "https://people.utwente.nl/a.trivella",
            "https://people.utwente.nl/m.r.k.mes",
            "https://people.utwente.nl/x.huang",
            "https://people.utwente.nl/c.kolb",
            "https://people.utwente.nl/r.guizzardi",
            "https://people.utwente.nl/e.svetlova",
            "https://people.utwente.nl/p.khrennikova",
            "https://people.utwente.nl/f.s.bernard",
            "https://people.utwente.nl/mathis.jander",
            "https://people.utwente.nl/j.vanhillegersberg",
            "https://people.utwente.nl/mohamed.faid",
            "https://people.utwente.nl/m.r.machado",
            "https://people.utwente.nl/armin.sadighi",
            "https://people.utwente.nl/w.j.a.vanheeswijk",
            "https://people.utwente.nl/manuele.massei",
        ]

        self.downloaded = []
        self.failed = []

    def fetch_profile_photo(self, profile_url: str) -> tuple[str, bytes] | None:
        """Fetch profile photo from a people.utwente.nl page."""
        try:
            response = self.session.get(profile_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for profile photo - typically in div.profile-photo or similar
            photo_img = None

            # Try various selectors for profile photos
            selectors = [
                'img.profile-image',
                'img.photo',
                '.profile-photo img',
                '.staff-photo img',
                '.person-image img',
                'figure.profile img',
                '.card-image img',
                'img[src*="photo"]',
                'img[src*="profile"]',
            ]

            for selector in selectors:
                imgs = soup.select(selector)
                for img in imgs:
                    src = img.get('src') or img.get('data-src')
                    if src and 'placeholder' not in src.lower():
                        photo_img = src
                        break
                if photo_img:
                    break

            # If still not found, look for any image in the main content
            if not photo_img:
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    # Skip icons, logos, etc.
                    if src and any(x in src.lower() for x in ['staff', 'photo', 'profile', 'people', 'employee']):
                        if 'placeholder' not in src.lower() and 'icon' not in src.lower():
                            photo_img = src
                            break

            if photo_img:
                # Make absolute URL
                photo_url = urljoin(profile_url, photo_img)

                # Download the image
                img_response = self.session.get(photo_url, timeout=30)
                img_response.raise_for_status()

                return photo_url, img_response.content

            return None

        except Exception as e:
            print(f"    Error: {e}")
            return None

    def extract_name_from_url(self, url: str) -> str:
        """Extract person's name from profile URL."""
        # URL format: https://people.utwente.nl/firstname.lastname
        name = url.split('/')[-1]
        # Convert to filename-friendly format
        name = name.replace('.', '_')
        return name

    def fetch_all_photos(self):
        """Fetch photos for all team members."""
        print("=" * 60)
        print("FETCH TEAM PHOTOS")
        print("=" * 60)
        print(f"Output directory: {self.output_dir.absolute()}")
        print(f"Team members: {len(self.team_urls)}")
        print()

        for i, url in enumerate(self.team_urls, 1):
            name = self.extract_name_from_url(url)
            print(f"[{i}/{len(self.team_urls)}] {name}...")

            result = self.fetch_profile_photo(url)

            if result:
                photo_url, photo_data = result

                # Determine file extension
                ext = '.jpg'
                if '.png' in photo_url.lower():
                    ext = '.png'
                elif '.webp' in photo_url.lower():
                    ext = '.webp'

                # Save photo
                photo_path = self.output_dir / f"{name}{ext}"
                photo_path.write_bytes(photo_data)

                self.downloaded.append({
                    'name': name,
                    'url': url,
                    'photo_url': photo_url,
                    'local_path': str(photo_path)
                })
                print(f"    Downloaded: {photo_path.name}")
            else:
                self.failed.append({'name': name, 'url': url})
                print(f"    No photo found")

            time.sleep(0.5)  # Rate limiting

        self.generate_report()

    def generate_report(self):
        """Generate summary report."""
        print("\n" + "-" * 60)
        print("SUMMARY")
        print("-" * 60)
        print(f"Downloaded: {len(self.downloaded)}")
        print(f"Failed:     {len(self.failed)}")

        if self.downloaded:
            print("\nDownloaded photos:")
            for item in self.downloaded:
                print(f"  - {item['name']}")

        if self.failed:
            print("\nNo photo found for:")
            for item in self.failed:
                print(f"  - {item['name']} ({item['url']})")

        print("\n" + "=" * 60)

        # Generate markdown snippet for team page
        if self.downloaded:
            print("\nMarkdown snippet for team photos:")
            print("-" * 40)
            for item in self.downloaded:
                rel_path = Path(item['local_path']).relative_to(Path('static'))
                print(f'![{item["name"]}]({rel_path})')


def main():
    """Main entry point."""
    fetcher = TeamPhotoFetcher()
    fetcher.fetch_all_photos()


if __name__ == "__main__":
    main()
