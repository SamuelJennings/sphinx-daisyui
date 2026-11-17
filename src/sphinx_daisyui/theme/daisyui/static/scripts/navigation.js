/* The sidebar navigation: each toggle opens and closes its branch, and the current page's entry is brought into view. */
(function () {
  "use strict";

  /* The stylesheet hides a closed branch's list from its toggle's state. */
  document.querySelectorAll(".daisy-nav-toggle").forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(open));
    });
  });

  /* Scrolling the sidebar alone keeps the page where the reader left it. */
  const scroller = document.querySelector(".daisy-sidebar-scroll");
  const current = document.querySelector('.daisy-nav [aria-current="page"]');
  if (!scroller || !current) return;
  const box = scroller.getBoundingClientRect();
  const entry = current.getBoundingClientRect();
  if (entry.top < box.top || entry.bottom > box.bottom) {
    scroller.scrollTop += entry.top - box.top - box.height / 3;
  }
})();
