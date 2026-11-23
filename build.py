"""Static site generator: content/*.yaml + templates/*.html -> _site/

Usage:  python build.py            # build into _site/
        python build.py --serve    # build and serve on http://localhost:8000
"""
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
OUT = ROOT / "_site"

CATEGORIES = {
    "de": "Data Engineering & BI",
    "da": "Data Analytics",
    "ml": "Machine Learning",
    "ai": "KI & LLM",
    "ecom": "E-Commerce & Digitalisierung",
}


def load(name):
    with open(ROOT / "content" / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def github_repo_count(user):
    """Public repo count from the GitHub API; None if offline or rate-limited."""
    req = urllib.request.Request(f"https://api.github.com/users/{user}")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.load(r).get("public_repos")
    except Exception as e:  # noqa: BLE001
        print(f"  GitHub API skipped ({e.__class__.__name__}), using fallback")
        return None


def build():
    site = load("site.yaml")
    projects = load("projects.yaml")
    for p in projects:
        p["category_label"] = CATEGORIES[p["category"]]

    repos = github_repo_count(site["github_user"])
    for s in site["stats"]:
        if s.get("key") == "repos" and repos:
            s["value"] = str(repos)
        if s.get("key") == "projects":
            s["value"] = str(len(projects))

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    ctx = dict(
        site=site,
        person=site["person"],
        projects=projects,
        featured=[p for p in projects if p.get("featured")],
        categories=CATEGORIES,
        tour_json=json.dumps(site["tour"], ensure_ascii=False),
    )

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT / "static")

    def render(template, path, **extra):
        target = OUT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        depth = len(Path(path).parts) - 1
        root = extra.pop("root", "../" * depth or "./")
        html = env.get_template(template).render(**ctx, **extra, root=root)
        target.write_text(html, encoding="utf-8")
        print(f"  {path}")

    render("index.html", "index.html")
    render("resume.html", "lebenslauf/index.html")
    for p in projects:
        if p.get("case"):
            render("project.html", f"projects/{p['slug']}/index.html", p=p)
    render("404.html", "404.html", root="/")  # 404 is served at any depth
    (OUT / ".nojekyll").write_text("")
    print(f"Done: {OUT}")


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        import functools
        import http.server

        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=OUT)
        print("Serving on http://localhost:8000")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()
