# razanmdr.github.io

Portfolio von Mochammad Dary Razan – statische Seite, generiert mit Python + Jinja2, gehostet auf GitHub Pages.

## Struktur

```
content/site.yaml       Profil, Stats, Erfahrung, Skills, Zertifikate, Lab, Tour
content/projects.yaml   Alle Projekte (featured + case -> eigene Case-Study-Seite)
templates/              Jinja2-Templates (Startseite, Case Study, Lebenslauf, 404)
static/                 CSS + JS (Filter, Theme-Toggle, Guided Tour)
build.py                Generator -> _site/
```

## Lokal bauen

```bash
pip install -r requirements.txt
python build.py --serve      # http://localhost:8000
```

## Deploy

1. Repo `razanmdr.github.io` anlegen und diesen Ordner pushen (Branch `main`).
2. Settings → Pages → Source: **GitHub Actions**.
3. Jeder Push baut und deployt automatisch; zusätzlich wöchentlicher Rebuild für die GitHub-Stats.

Das bestehende Repo `razanmdr/playground` bleibt unter `/playground/` erreichbar.

## Inhalte ändern

- Neues Projekt: Eintrag in `content/projects.yaml`. Mit `featured: true` erscheint es oben, mit einem `case:`-Block bekommt es eine eigene Seite.
- Kennzahl auf der Karte: `metric: {value: "...", label: "..."}`.
- Ablaufdiagramm: `flow: [Schritt 1, Schritt 2, ...]`.

## Später

- AI-Q&A-Widget ("Frag mich" + Job-Fit-Check) über einen Cloudflare Worker als Proxy, damit kein API-Key im Frontend liegt.
- Englische Version.
