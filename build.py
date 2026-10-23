"""Build the static version of the website for GitHub Pages.

Turns every page in app.py into a plain HTML file inside _site/, then copies
over only the files in static/ that those pages actually use. Anything in
static/ that no page links to stays out of the public site.

Run it with:  python build.py
GitHub Actions runs it automatically on every push to master.
"""
import re
import shutil
from html import escape
from pathlib import Path

from app import app

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
STATIC = ROOT / "static"

# Finds paths like "/static/uofm.png" or "./static/style.css"
STATIC_REF = re.compile(r"""static/([^"'()\s?#]+)""")

REDIRECT_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Redirecting</title>
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
</head>
<body><p>Redirecting to <a href="{url}">{url}</a></p></body>
</html>
"""


def output_name(path):
    """'/' becomes 'index.html', '/projects' becomes 'projects.html'."""
    return (path.strip("/") or "index") + ".html"


def build_pages():
    client = app.test_client()
    paths = sorted(
        rule.rule
        for rule in app.url_map.iter_rules()
        if rule.endpoint != "static" and not rule.arguments and "GET" in rule.methods
    )
    for path in paths:
        response = client.get(path)
        target = OUT / output_name(path)
        if response.status_code == 200:
            target.write_bytes(response.data)
        elif 300 <= response.status_code < 400:
            # GitHub Pages can't send real redirects, so write a page that forwards instead
            target.write_text(REDIRECT_PAGE.format(url=escape(response.location)), encoding="utf-8")
        else:
            raise SystemExit(f"{path} returned {response.status_code}, stopping the build")
        print(f"  {path:<12} -> {target.relative_to(ROOT)}")


def copy_used_static_files():
    seen = set()
    to_scan = [page.read_text(encoding="utf-8") for page in OUT.glob("*.html")]
    while to_scan:
        for ref in STATIC_REF.findall(to_scan.pop()):
            if ref in seen:
                continue
            seen.add(ref)
            source = STATIC / ref
            if not source.is_file():
                print(f"  warning: a page links to static/{ref}, but that file doesn't exist")
                continue
            dest = OUT / "static" / ref
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            print(f"  static/{ref}")
            if source.suffix == ".css":
                # Stylesheets can point at more files, like background images
                to_scan.append(source.read_text(encoding="utf-8"))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    print("Pages:")
    build_pages()
    print("Static files:")
    copy_used_static_files()
    print(f"Done. The site is in {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
