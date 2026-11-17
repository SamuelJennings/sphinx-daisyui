/* The layout playground: type a layout code and the mock-up redraws with it.
   The rules are the theme's own (sphinx_daisyui.parse_layout), written again here
   so the page needs no build. */
(function () {
  "use strict";
  const box = document.querySelector("[data-layout-playground]");
  if (!box) return;

  const NAMES = { h: "header", l: "primary", p: "main", r: "secondary", f: "footer" };
  const LABELS = { header: "Header", primary: "Left sidebar", main: "Page", secondary: "Right sidebar", footer: "Footer" };
  const SHAPE = /^[hl]h[hr] lpr [fl]f[fr]$/;
  const input = box.querySelector(".lp-code");
  const message = box.querySelector(".lp-msg");
  const grid = box.querySelector(".lp-grid");
  const chips = box.querySelector(".lp-chips");
  const explain = box.querySelector(".lp-explain");
  const snippet = box.querySelector(".lp-snippet code");
  const address = box.querySelector(".lp-address");

  function parse(raw) {
    const code = raw.trim().split(/\s+/).join(" ");
    if (!SHAPE.test(code.toLowerCase())) return null;
    const rows = code.split(" ");
    const lower = rows.map((r) => r.toLowerCase());
    const narrow = lower.map((row) => [...row].map((c, i) => (c === "r" ? row[i - 1] : c)).join(""));
    const areas = (g) => g.map((row) => '"' + [...row].map((c) => NAMES[c]).join(" ") + '"').join(" ");
    const headerFixed = rows[0][1] === "H";
    return {
      code, rows, lower,
      wide: areas(lower),
      medium: areas(narrow),
      headerFixed,
      primaryFixed: rows[1][0] === "L",
      secondaryFixed: rows[1][2] === "R",
      footerFixed: rows[2][1] === "F",
      primaryTop: headerFixed && lower[0][0] === "h",
      secondaryTop: headerFixed && lower[0][2] === "h",
    };
  }

  function describe(p) {
    const [top, , bottom] = p.lower;
    return [
      ["header", `Header: ${p.headerFixed ? "stays at the top as you scroll" : "scrolls away with the page"}. ` +
        (top[0] === "h" ? "It runs across above the left sidebar" : "It starts beside the left sidebar") +
        (top[2] === "h" ? " and above the right one." : ", and the right sidebar reaches the top beside it.")],
      ["primary", `Left sidebar: ${p.primaryFixed ? "stays beside the page and scrolls on its own" : "scrolls with the page"}. ` +
        (top[0] === "l" ? "It reaches the top with the logo at its head" : "It starts under the header") +
        (bottom[0] === "l" ? " and runs to the bottom." : ", and the footer runs under it.")],
      ["main", "Page: always the centre."],
      ["secondary", `Right sidebar: ${p.secondaryFixed ? "stays beside the page" : "scrolls with the page"}. ` +
        (top[2] === "r" ? "It reaches the top" : "It starts under the header") +
        (bottom[2] === "r" ? " and runs to the bottom." : ", and the footer runs under it.")],
      ["footer", `Footer: ${p.footerFixed ? "stays at the bottom of the window" : "sits at the end of the page"}.`],
    ];
  }

  function render(p) {
    const screen = box.dataset.screen;
    grid.style.setProperty("--lp-areas", screen === "xl" ? p.wide : p.medium);
    grid.style.setProperty("--lp-primary-top", p.primaryTop ? "var(--lp-header)" : "0px");
    grid.style.setProperty("--lp-secondary-top", p.secondaryTop ? "var(--lp-header)" : "0px");
    grid.toggleAttribute("data-header-fixed", p.headerFixed);
    grid.toggleAttribute("data-primary-fixed", p.primaryFixed);
    grid.toggleAttribute("data-secondary-fixed", p.secondaryFixed);
    grid.toggleAttribute("data-footer-fixed", p.footerFixed);
    box.querySelector('[data-pin="header"]').hidden = !p.headerFixed;
    box.querySelector('[data-pin="primary"]').hidden = !p.primaryFixed;
    box.querySelector('[data-pin="secondary"]').hidden = !p.secondaryFixed;
    box.querySelector('[data-pin="footer"]').hidden = !p.footerFixed;

    chips.innerHTML = "";
    p.rows.forEach((row, r) => {
      if (r) chips.append(Object.assign(document.createElement("span"), { className: "lp-gap" }));
      [...row].forEach((c) => {
        const chip = document.createElement("span");
        chip.className = "lp-chip" + (c !== c.toLowerCase() ? " is-fixed" : "");
        chip.dataset.area = NAMES[c.toLowerCase()];
        chip.textContent = c;
        chip.title = LABELS[chip.dataset.area] + (c !== c.toLowerCase() ? ", stays in place" : "");
        chips.append(chip);
      });
    });

    explain.innerHTML = "";
    describe(p).forEach(([area, text]) => {
      const li = document.createElement("li");
      li.dataset.area = area;
      li.innerHTML = '<span class="lp-dot"></span><span></span>';
      li.lastChild.textContent = text;
      explain.append(li);
    });

    snippet.textContent = `html_theme_options = {"layout": "${p.code}"}`;
    address.textContent = `docs.example.org  ·  layout = "${p.code}"`;
    box.querySelectorAll("[data-code]").forEach((b) => {
      const on = b.dataset.code === p.code;
      b.classList.toggle("btn-primary", on);
      b.setAttribute("aria-pressed", String(on));
    });
  }

  let current = parse(input.value);
  function update() {
    const p = parse(input.value);
    if (!p) {
      // An unfinished code is fine while it's being typed: the mock-up keeps the last one.
      if (input.value.replace(/\s+/g, "").length < 9) {
        input.classList.remove("input-error");
        if (!message.classList.contains("is-refusal")) message.textContent = "";
        return;
      }
      input.classList.add("input-error");
      input.setAttribute("aria-invalid", "true");
      message.textContent =
        "Three groups of three letters: the top row is h or l, then h, then h or r. The middle row is l, p, r. The bottom row is f or l, then f, then f or r.";
      return;
    }
    input.classList.remove("input-error");
    input.removeAttribute("aria-invalid");
    if (!message.classList.contains("is-refusal")) message.textContent = "";
    current = p;
    render(p);
  }

  /* Only what a layout code can hold gets into the field. Each position takes
     only its own letters, a space is added after each group of three, and
     anything else is refused with a sentence saying what that position takes. */
  const SLOTS = ["hl", "h", "hr", " ", "l", "p", "r", " ", "fl", "f", "fr"];
  const ROWS = ["top", "middle", "bottom"];
  const ORDINAL = ["first", "second", "third"];
  const NAMED = { h: "h (header)", l: "l (left sidebar)", p: "p (page)", r: "r (right sidebar)", f: "f (footer)" };

  function tidy(value) {
    const letters = value.replace(/\s+/g, "");
    const groups = letters.match(/.{1,3}/g) || [];
    let out = groups.join(" ");
    if (/\s$/.test(value) && letters.length % 3 === 0 && letters.length && letters.length < 9) out += " ";
    return out;
  }

  function firstWrong(value) {
    for (let i = 0; i < value.length; i++) {
      if (i >= SLOTS.length || !SLOTS[i].includes(value[i].toLowerCase())) return i;
    }
    return -1;
  }

  function refusal(index, ch) {
    if (index >= SLOTS.length) return "A layout code is nine letters, in three groups of three.";
    const slot = index - Math.floor(index / 4);
    const row = ROWS[Math.floor(slot / 3)];
    const allowed = [...SLOTS[index]].map((c) => NAMED[c]).join(" or ");
    return `"${ch}" can't go there. The ${ORDINAL[slot % 3]} letter of the ${row} row is ${allowed}, in either case.`;
  }

  let accepted = input.value;
  input.addEventListener("input", () => {
    const tidied = tidy(input.value);
    const wrong = firstWrong(tidied);
    if (wrong !== -1) {
      input.value = accepted;
      message.textContent = refusal(wrong, tidied[wrong]);
      message.classList.add("is-refusal");
      return;
    }
    message.classList.remove("is-refusal");
    if (tidied !== input.value) input.value = tidied;
    accepted = input.value;
    update();
  });
  box.querySelectorAll("[data-code]").forEach((b) =>
    b.addEventListener("click", () => { input.value = accepted = b.dataset.code; message.classList.remove("is-refusal"); update(); })
  );
  box.querySelectorAll("[data-screen-choice]").forEach((b) =>
    b.addEventListener("click", () => {
      box.dataset.screen = b.dataset.screenChoice;
      box.querySelectorAll("[data-screen-choice]").forEach((o) => {
        o.classList.toggle("btn-primary", o === b);
        o.setAttribute("aria-pressed", String(o === b));
      });
      if (current) render(current);
    })
  );
  box.querySelector(".lp-form").addEventListener("submit", (e) => e.preventDefault());
  update();
})();
