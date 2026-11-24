// Thesis console: switch the language of the tool description
(() => {
  const out = document.getElementById("schema-desc");
  if (!out) return;
  const desc = {
    de: "Sucht Produkte im Katalog nach Kategorie und Preis.",
    en: "Searches the product catalog by category and price.",
  };
  const buttons = document.querySelectorAll(".toggle button");
  buttons.forEach((b) =>
    b.addEventListener("click", () => {
      buttons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      out.innerHTML = '<span class="k">search_products</span>: "' + desc[b.dataset.lang] + '"';
    })
  );
})();

// Project list: show the first rows, filter by area, reveal all on request
(() => {
  const buttons = document.querySelectorAll(".filter");
  const rows = [...document.querySelectorAll("#project-list > li")];
  const more = document.getElementById("show-all");
  const LIMIT = window.matchMedia("(max-width: 640px)").matches ? 4 : 8;
  let expanded = false, filter = "all";
  const render = () => {
    let shown = 0;
    rows.forEach((r) => {
      const match = filter === "all" || r.dataset.cat === filter;
      const visible = match && (expanded || filter !== "all" || shown < LIMIT);
      r.hidden = !visible;
      if (visible) shown++;
    });
    if (more) more.hidden = expanded || filter !== "all" || rows.length <= LIMIT;
  };
  buttons.forEach((b) =>
    b.addEventListener("click", () => {
      buttons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      filter = b.dataset.filter;
      render();
    })
  );
  if (more) more.addEventListener("click", () => { expanded = true; render(); rows[LIMIT] && rows[LIMIT].querySelector("a, h4").focus?.(); });
  render();
})();

// Mobile menu
(() => {
  const btn = document.getElementById("menu-toggle");
  const nav = document.getElementById("nav-links");
  if (!btn || !nav) return;
  const setOpen = (open) => {
    nav.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", String(open));
    btn.textContent = open ? "Schließen" : "Menü";
  };
  btn.addEventListener("click", () => setOpen(!nav.classList.contains("open")));
  nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setOpen(false)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("open")) { setOpen(false); btn.focus(); }
  });
})();

// Career ruler: on narrow screens start at the most recent years
(() => {
  const sc = document.querySelector(".ruler-scroll");
  if (sc && sc.scrollWidth > sc.clientWidth) sc.scrollLeft = sc.scrollWidth;
})();

// Career list on phones: tasks fold out per role
document.querySelectorAll(".tasks-btn").forEach((b) =>
  b.addEventListener("click", () => {
    const li = b.closest("li");
    const open = li.classList.toggle("open");
    b.setAttribute("aria-expanded", String(open));
    b.textContent = open ? "Aufgaben ausblenden" : "Aufgaben anzeigen";
  })
);
