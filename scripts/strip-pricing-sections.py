#!/usr/bin/env python3
"""
strip-pricing-sections.py

Post-processor for assembled SMB Team Growth Audit HTML reports.
Takes one or more HTML file paths as CLI arguments and removes pricing-related
sections in place. Used by audit-pipeline.yml when suppress_pricing=true.

Sections removed:
  1. Executive summary pricing: div.exec-block containing a
     div.exec-block-title with text "Recommended Investment"
  2. Within div#recommendation's next sibling div.content-wrap:
     - All div.package-block elements
     - All div.investment-grid elements
     Kept: div.closing-statement-block, div.dbm-subheader,
           div.scorecard-label, div.outcome-grid, div.personal-closing

Usage:
  python3 scripts/strip-pricing-sections.py <file1.html> [file2.html ...]
"""

import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 is not installed. Run: pip install beautifulsoup4")
    sys.exit(1)


def strip_pricing(html_path: str) -> None:
    path = Path(html_path)
    if not path.exists():
        print(f"  [SKIP] File not found: {html_path}")
        return

    content = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")
    removed = []

    # ------------------------------------------------------------------
    # 1. Executive summary pricing block
    #    Find div.exec-block that contains a div.exec-block-title with
    #    the text "Recommended Investment" and remove the entire exec-block.
    # ------------------------------------------------------------------
    for exec_block in soup.find_all("div", class_="exec-block"):
        title_el = exec_block.find("div", class_="exec-block-title")
        if title_el and "Recommended Investment" in title_el.get_text():
            exec_block.decompose()
            removed.append("exec-block (Recommended Investment)")

    # ------------------------------------------------------------------
    # 2. Section 11 pricing elements inside div#recommendation's
    #    next sibling div.content-wrap
    # ------------------------------------------------------------------
    recommendation_div = soup.find("div", id="recommendation")
    if recommendation_div:
        # Walk forward siblings to find the next div.content-wrap
        content_wrap = None
        for sibling in recommendation_div.next_siblings:
            if hasattr(sibling, "name") and sibling.name == "div":
                classes = sibling.get("class", [])
                if "content-wrap" in classes:
                    content_wrap = sibling
                    break

        if content_wrap:
            # Remove all div.package-block elements
            for el in content_wrap.find_all("div", class_="package-block"):
                el.decompose()
                removed.append("package-block")

            # Remove all div.investment-grid elements
            for el in content_wrap.find_all("div", class_="investment-grid"):
                el.decompose()
                removed.append("investment-grid")

    # ------------------------------------------------------------------
    # Write back if anything was removed
    # ------------------------------------------------------------------
    if removed:
        path.write_text(str(soup), encoding="utf-8")
        print(f"  [MODIFIED] {html_path}")
        for item in removed:
            print(f"    Removed: {item}")
    else:
        print(f"  [UNCHANGED] {html_path} — no pricing sections found")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 strip-pricing-sections.py <file1.html> [file2.html ...]")
        sys.exit(1)

    files = sys.argv[1:]
    print(f"strip-pricing-sections.py: processing {len(files)} file(s)\n")

    for html_path in files:
        strip_pricing(html_path)

    print("\nDone.")
    sys.exit(0)


if __name__ == "__main__":
    main()
