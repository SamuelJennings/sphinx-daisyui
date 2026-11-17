/* The page frame: the scrolled mark, the measured header, the drawer and the moving navbar_end. */
(function () {
  "use strict";

  const shell = document.querySelector(".daisy-layout");
  if (!shell) return;

  /* The header draws its line and shadow once the page has scrolled. */
  function markScrolled() {
    shell.classList.toggle("daisy-scrolled", window.scrollY > 0);
  }
  window.addEventListener("scroll", markScrolled, { passive: true });
  markScrolled();

  /* The header's height, so the sticky sidebars sit below it whatever it holds. */
  const header = shell.querySelector(".daisy-area-header");
  if (header && "ResizeObserver" in window) {
    new ResizeObserver(() => {
      const height = header.getBoundingClientRect().height;
      shell.style.setProperty("--daisy-header-height", height + "px");
    }).observe(header, { box: "border-box" });
  }

  /* Following a link in the navigation closes the drawer, and so does Escape. */
  const drawer = document.getElementById("daisy-drawer");
  document.querySelectorAll(".daisy-area-primary a").forEach((link) => {
    link.addEventListener("click", () => {
      if (drawer) drawer.checked = false;
    });
  });
  if (window.sphinxDaisyui && window.sphinxDaisyui.keys) {
    window.sphinxDaisyui.keys.on("Escape", () => {
      if (drawer && drawer.checked) drawer.checked = false;
    });
  }

  /* Below 40rem the navbar's end items move into the drawer, and back above it. */
  const end = document.querySelector("[data-daisy-navbar-end]");
  const slot = document.querySelector("[data-daisy-navbar-end-slot]");
  if (end && slot) {
    const narrow = window.matchMedia("(width < 40rem)");
    const place = () => {
      const from = narrow.matches ? end : slot;
      const to = narrow.matches ? slot : end;
      while (from.firstChild) to.appendChild(from.firstChild);
    };
    narrow.addEventListener("change", place);
    place();
  }
})();
