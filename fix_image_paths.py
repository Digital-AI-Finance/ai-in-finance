"""
Fix Image Paths - Convert absolute paths to relative for Hugo.

Problem: Markdown uses absolute paths like /images/... which don't work
on GitHub Pages subdirectory deployment (/ai-in-finance/).

Solution: Remove leading slash to make paths relative, letting Hugo
process them correctly with baseURL.
"""

import re
from pathlib import Path


def fix_image_paths(content_dir: str = "content"):
    """Fix image paths in all markdown files."""
    content_path = Path(content_dir)
    files_modified = 0
    images_fixed = 0

    print("=" * 60)
    print("FIX IMAGE PATHS")
    print("=" * 60)

    # Pattern to match markdown images with absolute paths
    # Matches: ![alt text](/images/...) or ![](/images/...)
    img_pattern = re.compile(r'!\[([^\]]*)\]\(/images/([^)]+)\)')

    # Pattern for HTML img tags with absolute src
    html_img_pattern = re.compile(r'<img([^>]*)\ssrc="/images/([^"]+)"([^>]*)>')

    # Pattern to remove CMS placeholder tokens like #replace=...
    placeholder_pattern = re.compile(r'#replace=[a-zA-Z0-9+/=]+')

    for md_file in sorted(content_path.rglob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
            original = content
            file_fixes = 0

            # Fix markdown image paths: /images/... -> images/...
            def fix_md_img(match):
                nonlocal file_fixes
                alt = match.group(1)
                path = match.group(2)
                # Remove CMS placeholder tokens
                path = placeholder_pattern.sub('', path)
                file_fixes += 1
                return f'![{alt}](images/{path})'

            content = img_pattern.sub(fix_md_img, content)

            # Fix HTML img src paths
            def fix_html_img(match):
                nonlocal file_fixes
                before = match.group(1)
                path = match.group(2)
                after = match.group(3)
                # Remove CMS placeholder tokens
                path = placeholder_pattern.sub('', path)
                file_fixes += 1
                return f'<img{before} src="images/{path}"{after}>'

            content = html_img_pattern.sub(fix_html_img, content)

            # Also fix any remaining standalone image references
            # Pattern: src="/images/..." or href="/images/..."
            attr_pattern = re.compile(r'(src|href)="/images/([^"]+)"')

            def fix_attr(match):
                nonlocal file_fixes
                attr = match.group(1)
                path = match.group(2)
                path = placeholder_pattern.sub('', path)
                file_fixes += 1
                return f'{attr}="images/{path}"'

            content = attr_pattern.sub(fix_attr, content)

            if content != original:
                md_file.write_text(content, encoding="utf-8")
                files_modified += 1
                images_fixed += file_fixes
                print(f"  Fixed {file_fixes} images in: {md_file.relative_to(content_path)}")

        except Exception as e:
            print(f"  Error processing {md_file}: {e}")

    print("\n" + "-" * 60)
    print(f"SUMMARY: Fixed {images_fixed} image paths in {files_modified} files")
    print("=" * 60)

    return files_modified, images_fixed


def main():
    """Main entry point."""
    fix_image_paths()


if __name__ == "__main__":
    main()
