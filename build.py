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


def asset_version():
    """Hash of CSS/JS so browsers fetch new assets after each deploy."""
    import hashlib
    h = hashlib.md5()
    for f in sorted((ROOT / "static").rglob("*.*")):
        if f.suffix in (".css", ".js"):
            h.update(f.read_bytes())
    return h.hexdigest()[:8]


def career_timeline(experience):
    """Bars for the to-scale career chart, in months from January of the first year."""
    def month(s):
        m, y = s.strip().split(".")
        return int(y) * 12 + int(m) - 1

    spans = []
    for e in experience:
        start, end = (month(part) for part in e["period"].replace("–", "-").split("-"))
        role = e["role"].lower()
        spans.append({"from": start, "to": end + 1,
                      "qa": any(w in role for w in ("test", "qa", "quality"))})
    first = min(s["from"] for s in spans) // 12
    last = (max(s["to"] for s in spans) - 1) // 12
    origin = first * 12
    return {
        "years": list(range(first, last + 1)),
        "total": (last - first + 1) * 12,
        "spans": [{"start": s["from"] - origin, "length": s["to"] - s["from"], "qa": s["qa"]} for s in spans],
    }


def build():
    site = load("site.yaml")
    projects = load("projects.yaml")
    for p in projects:
        p["category_label"] = CATEGORIES[p["category"]]
        # Typesetting: a colon in titles and a comma in prose instead of a spaced dash
        p["title"] = p["title"].replace(" – ", ": ")
        p["summary"] = p["summary"].replace(" – ", ", ")
        for k, val in (p.get("case") or {}).items():
            if isinstance(val, str) and k != "example":
                p["case"][k] = val.replace(" – ", ", ")

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
    featured = [p for p in projects if p.get("featured")]
    zahl = {1: "Eine", 2: "Zwei", 3: "Drei", 4: "Vier", 5: "Fünf", 6: "Sechs", 7: "Sieben",
            8: "Acht", 9: "Neun", 10: "Zehn", 11: "Elf", 12: "Zwölf"}.get(len(featured), str(len(featured)))
    for step in site["tour"]:
        step["text"] = step["text"].replace("{featured}", zahl)
    ctx = dict(
        site=site,
        person=site["person"],
        projects=projects,
        featured=featured,
        categories=CATEGORIES,
        timeline=career_timeline(site["experience"]),
        tour_json=json.dumps(site["tour"], ensure_ascii=False),
        asset_v=asset_version(),
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
