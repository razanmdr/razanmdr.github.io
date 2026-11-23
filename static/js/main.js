// Theme toggle
(() => {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;
  btn.addEventListener("click", () => {
    const root = document.documentElement;
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
  });
})();

// Project filters
(() => {
  const buttons = document.querySelectorAll(".filter");
  const cards = document.querySelectorAll("#project-grid .card");
  buttons.forEach((b) =>
    b.addEventListener("click", () => {
      buttons.forEach((x) => x.classList.toggle("active", x === b));
      const f = b.dataset.filter;
      cards.forEach((c) => c.classList.toggle("hidden", f !== "all" && c.dataset.cat !== f));
    })
  );
})();

// Guided tour
(() => {
  const steps = window.TOUR;
  const box = document.getElementById("tour");
  const start = document.getElementById("tour-start");
  if (!steps || !box || !start) return;
  const $ = (id) => document.getElementById(id);
  let i = 0, focused = null;

  function show() {
    const s = steps[i];
    const el = document.querySelector(s.target);
    if (focused) focused.classList.remove("tour-focus");
    if (el) {
      el.classList.add("tour-focus");
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      focused = el;
    }
    $("tour-count").textContent = `Schritt ${i + 1} von ${steps.length}`;
    $("tour-title").textContent = s.title;
    $("tour-text").textContent = s.text;
    $("tour-prev").disabled = i === 0;
    $("tour-next").textContent = i === steps.length - 1 ? "Fertig" : "Weiter";
  }
  function close() {
    box.hidden = true;
    if (focused) focused.classList.remove("tour-focus");
  }
  start.addEventListener("click", () => { i = 0; box.hidden = false; show(); });
  $("tour-next").addEventListener("click", () => (i < steps.length - 1 ? (i++, show()) : close()));
  $("tour-prev").addEventListener("click", () => { if (i > 0) { i--; show(); } });
  $("tour-close").addEventListener("click", close);
  document.addEventListener("keydown", (e) => {
    if (box.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") $("tour-next").click();
    if (e.key === "ArrowLeft") $("tour-prev").click();
  });
})();
