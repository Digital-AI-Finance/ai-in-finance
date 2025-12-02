"""
Navigation Generator - Build hierarchical sidebar menu for Hugo site.
Scans content directory and generates collapsible menu configuration.
"""

import json
import re
from pathlib import Path


class NavigationGenerator:
    """Generate Hugo navigation from content structure."""

    def __init__(self, content_dir: str = "content", output_dir: str = "."):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.tree = {}

    def scan_content(self) -> dict:
        """Scan content directory and build tree structure."""
        print("Scanning content directory...")

        tree = {"_pages": [], "_children": {}}

        for md_file in sorted(self.content_dir.rglob("*.md")):
            rel_path = md_file.relative_to(self.content_dir)
            parts = list(rel_path.parts)

            # Extract front matter for title
            title = self.extract_title(md_file)
            url = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"
            if parts[-1] != "_index.md":
                url = "/" + str(rel_path.with_suffix("")).replace("\\", "/")

            # Determine weight/order
            weight = self.extract_weight(md_file)

            page_info = {
                "title": title,
                "url": url,
                "file": str(rel_path),
                "weight": weight,
                "is_index": parts[-1] == "_index.md"
            }

            # Navigate to correct position in tree
            current = tree
            for i, part in enumerate(parts[:-1]):
                if part not in current["_children"]:
                    current["_children"][part] = {"_pages": [], "_children": {}}
                current = current["_children"][part]

            if parts[-1] == "_index.md":
                current["_index"] = page_info
            else:
                current["_pages"].append(page_info)

        self.tree = tree
        return tree

    def extract_title(self, md_file: Path) -> str:
        """Extract title from markdown front matter."""
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            # Look for YAML front matter
            if content.startswith("---"):
                end = content.find("---", 3)
                if end != -1:
                    front_matter = content[3:end]
                    for line in front_matter.split("\n"):
                        if line.strip().startswith("title:"):
                            title = line.split(":", 1)[1].strip()
                            # Remove quotes
                            return title.strip("\"'")

            # Fallback: use filename
            return md_file.stem.replace("-", " ").replace("_", " ").title()
        except Exception:
            return md_file.stem.replace("-", " ").title()

    def extract_weight(self, md_file: Path) -> int:
        """Extract weight from front matter for ordering."""
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            if content.startswith("---"):
                end = content.find("---", 3)
                if end != -1:
                    front_matter = content[3:end]
                    for line in front_matter.split("\n"):
                        if line.strip().startswith("weight:"):
                            return int(line.split(":", 1)[1].strip())
        except Exception:
            pass
        return 999

    def generate_menu_data(self) -> list:
        """Generate menu data structure for Hugo."""
        def build_menu(node, path=""):
            items = []

            # Add section index if exists
            if "_index" in node:
                idx = node["_index"]
                item = {
                    "name": idx["title"],
                    "url": idx["url"],
                    "weight": idx["weight"],
                }
                # If has children, mark as parent
                if node["_children"] or node["_pages"]:
                    item["hasChildren"] = True
                    item["children"] = []

                    # Add child sections
                    for child_name, child_node in sorted(node["_children"].items()):
                        child_items = build_menu(child_node, f"{path}/{child_name}")
                        item["children"].extend(child_items)

                    # Add child pages
                    for page in sorted(node["_pages"], key=lambda x: x["weight"]):
                        item["children"].append({
                            "name": page["title"],
                            "url": page["url"],
                            "weight": page["weight"]
                        })

                items.append(item)
            else:
                # No index, add children directly
                for child_name, child_node in sorted(node["_children"].items()):
                    child_items = build_menu(child_node, f"{path}/{child_name}")
                    items.extend(child_items)

                for page in sorted(node["_pages"], key=lambda x: x["weight"]):
                    items.append({
                        "name": page["title"],
                        "url": page["url"],
                        "weight": page["weight"]
                    })

            return items

        return build_menu(self.tree)

    def generate_hugo_menu_config(self) -> str:
        """Generate Hugo menu configuration (TOML format)."""
        menu_data = self.generate_menu_data()

        lines = ["# Auto-generated menu configuration", ""]

        def add_menu_items(items, parent_id=None, level=0):
            for i, item in enumerate(items):
                identifier = item["url"].strip("/").replace("/", "-") or "home"

                lines.append("[[menu.main]]")
                lines.append(f'  identifier = "{identifier}"')
                lines.append(f'  name = "{item["name"]}"')
                lines.append(f'  url = "{item["url"]}"')
                lines.append(f'  weight = {item.get("weight", i + 1)}')
                if parent_id:
                    lines.append(f'  parent = "{parent_id}"')
                lines.append("")

                if "children" in item:
                    add_menu_items(item["children"], identifier, level + 1)

        add_menu_items(menu_data)
        return "\n".join(lines)

    def generate_sidebar_partial(self) -> str:
        """Generate Hugo sidebar partial template."""
        return '''{{/* Collapsible Sidebar Navigation */}}
<nav class="sidebar-nav">
  {{ $currentPage := . }}
  {{ range .Site.Menus.sidebar }}
    {{ template "menu-tree" (dict "menu" . "currentPage" $currentPage "level" 0) }}
  {{ end }}
</nav>

{{ define "menu-tree" }}
  {{ $menu := .menu }}
  {{ $currentPage := .currentPage }}
  {{ $level := .level }}
  {{ $isActive := or ($currentPage.IsMenuCurrent "sidebar" $menu) ($currentPage.HasMenuCurrent "sidebar" $menu) }}
  {{ $hasChildren := $menu.HasChildren }}

  <div class="nav-item level-{{ $level }}{{ if $isActive }} active{{ end }}">
    {{ if $hasChildren }}
      <details{{ if $isActive }} open{{ end }}>
        <summary>
          <a href="{{ $menu.URL }}">{{ $menu.Name }}</a>
          <span class="toggle-icon"></span>
        </summary>
        <div class="nav-children">
          {{ range $menu.Children }}
            {{ template "menu-tree" (dict "menu" . "currentPage" $currentPage "level" (add $level 1)) }}
          {{ end }}
        </div>
      </details>
    {{ else }}
      <a href="{{ $menu.URL }}"{{ if $isActive }} class="current"{{ end }}>{{ $menu.Name }}</a>
    {{ end }}
  </div>
{{ end }}
'''

    def generate_sidebar_css(self) -> str:
        """Generate CSS for collapsible sidebar."""
        return '''/* Collapsible Sidebar Navigation */
.sidebar-nav {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.5;
}

.nav-item {
  margin: 0;
}

.nav-item a {
  display: block;
  padding: 8px 12px;
  color: #333;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-item a:hover {
  background-color: #f0f0f0;
}

.nav-item.active > a,
.nav-item.active > details > summary > a {
  color: #0066cc;
  font-weight: 500;
}

.nav-item a.current {
  background-color: #e8f4fc;
  color: #0066cc;
}

/* Nested levels */
.nav-item.level-1 { padding-left: 16px; }
.nav-item.level-2 { padding-left: 32px; }
.nav-item.level-3 { padding-left: 48px; }
.nav-item.level-4 { padding-left: 64px; }

/* Details/Summary styling */
details {
  margin: 0;
}

details > summary {
  display: flex;
  align-items: center;
  cursor: pointer;
  list-style: none;
}

details > summary::-webkit-details-marker {
  display: none;
}

details > summary > a {
  flex-grow: 1;
}

.toggle-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
}

.toggle-icon::before {
  content: "+";
  font-weight: bold;
  color: #666;
}

details[open] > summary .toggle-icon::before {
  content: "-";
}

.nav-children {
  margin-top: 4px;
  padding-left: 8px;
  border-left: 2px solid #e0e0e0;
  margin-left: 12px;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .sidebar-nav {
    padding: 16px;
  }

  .nav-item a {
    padding: 12px;
  }
}
'''

    def generate_sidebar_layout(self) -> str:
        """Generate Hugo layout with sidebar."""
        return '''{{ define "main" }}
<div class="content-wrapper">
  <aside class="sidebar">
    {{ partial "sidebar.html" . }}
  </aside>
  <main class="main-content">
    <article>
      <h1>{{ .Title }}</h1>
      {{ .Content }}
    </article>
  </main>
</div>
{{ end }}
'''

    def generate_menu_yaml(self) -> str:
        """Generate menu data as YAML for Hugo data directory."""
        menu_data = self.generate_menu_data()

        def to_yaml(items, indent=0):
            lines = []
            prefix = "  " * indent
            for item in items:
                lines.append(f"{prefix}- name: \"{item['name']}\"")
                lines.append(f"{prefix}  url: \"{item['url']}\"")
                lines.append(f"{prefix}  weight: {item.get('weight', 999)}")
                if "children" in item and item["children"]:
                    lines.append(f"{prefix}  children:")
                    lines.extend(to_yaml(item["children"], indent + 2))
            return lines

        return "menu:\n" + "\n".join(to_yaml(menu_data, 1))

    def generate(self):
        """Generate all navigation files."""
        print("=" * 60)
        print("NAVIGATION GENERATOR")
        print("=" * 60)

        # Scan content
        self.scan_content()

        # Count pages
        def count_pages(node):
            count = len(node["_pages"])
            if "_index" in node:
                count += 1
            for child in node["_children"].values():
                count += count_pages(child)
            return count

        total_pages = count_pages(self.tree)
        print(f"Found {total_pages} pages")

        # Generate menu data
        menu_data = self.generate_menu_data()
        print(f"Generated menu with {len(menu_data)} top-level items")

        # Save menu YAML
        data_dir = self.output_dir / "data"
        data_dir.mkdir(exist_ok=True)
        menu_yaml = self.generate_menu_yaml()
        (data_dir / "menu.yaml").write_text(menu_yaml, encoding="utf-8")
        print(f"Saved: data/menu.yaml")

        # Save sidebar partial
        partials_dir = self.output_dir / "layouts" / "partials"
        partials_dir.mkdir(parents=True, exist_ok=True)
        (partials_dir / "sidebar.html").write_text(
            self.generate_sidebar_partial(), encoding="utf-8"
        )
        print(f"Saved: layouts/partials/sidebar.html")

        # Save sidebar CSS
        css_dir = self.output_dir / "static" / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        (css_dir / "sidebar.css").write_text(
            self.generate_sidebar_css(), encoding="utf-8"
        )
        print(f"Saved: static/css/sidebar.css")

        # Save layout with sidebar
        layouts_dir = self.output_dir / "layouts" / "_default"
        layouts_dir.mkdir(parents=True, exist_ok=True)
        (layouts_dir / "single-with-sidebar.html").write_text(
            self.generate_sidebar_layout(), encoding="utf-8"
        )
        print(f"Saved: layouts/_default/single-with-sidebar.html")

        # Generate and print menu config for reference
        print("\n" + "-" * 60)
        print("Generated Menu Structure:")
        print("-" * 60)

        def print_menu(items, indent=0):
            for item in items:
                prefix = "  " * indent
                print(f"{prefix}- {item['name']}")
                if "children" in item:
                    print_menu(item["children"], indent + 1)

        print_menu(menu_data)

        print("\n" + "=" * 60)
        print("NAVIGATION GENERATION COMPLETE")
        print("=" * 60)
        print("\nTo use the sidebar, add to your layout:")
        print('  <link rel="stylesheet" href="/css/sidebar.css">')
        print('  {{ partial "sidebar.html" . }}')


def main():
    """Main entry point."""
    generator = NavigationGenerator(
        content_dir="content",
        output_dir="."
    )
    generator.generate()


if __name__ == "__main__":
    main()
