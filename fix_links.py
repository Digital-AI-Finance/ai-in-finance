"""Fix all broken links in markdown files."""
import re
from pathlib import Path

content_dir = Path("content")
total_fixes = 0

for md in content_dir.rglob("*.md"):
    text = md.read_text(encoding='utf-8')
    original = text

    # 1. Convert external ai-in-finance.eu links to relative
    text = re.sub(r'\]\(https?://(?:www\.)?ai-in-finance\.eu/([^)]*)\)', r'](/\1)', text)

    # 2. Remove broken placeholder images
    text = re.sub(r'!\[[^\]]*\]\(images/\.publisher/[^)]+\)\n?', '', text)

    # 3. Convert absolute internal links: ](/path) stays as is (Hugo handles it)

    if text != original:
        # Count changes
        c1 = len(re.findall(r'ai-in-finance\.eu', original)) - len(re.findall(r'ai-in-finance\.eu', text))
        c2 = original.count('.publisher/') - text.count('.publisher/')
        total_fixes += c1 + c2
        md.write_text(text, encoding='utf-8')
        print(f"Fixed: {md.relative_to(content_dir)}")

print(f"\nTotal fixes: {total_fixes}")
