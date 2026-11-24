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

// Project filters
(() => {
  const buttons = document.querySelectorAll(".filter");
  const rows = document.querySelectorAll("#project-list > li");
  buttons.forEach((b) =>
    b.addEventListener("click", () => {
      buttons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      const f = b.dataset.filter;
      rows.forEach((r) => { r.hidden = f !== "all" && r.dataset.cat !== f; });
    })
  );
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
