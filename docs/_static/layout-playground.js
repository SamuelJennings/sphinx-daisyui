/* The layout playground: type a layout code and the mock-up redraws with it.
   The rules are the layout code's own. The documentation build reads them from
   sphinx_daisyui.layout and writes them into the page as #layout-rules, so this
   script holds no copy of them. */
(function () {
  "use strict";
  const box = document.querySelector("[data-layout-playground]");
  const source = document.getElementById("layout-rules");
  if (!box || !source) return;

  const RULES = JSON.parse(source.textContent);
  const LABELS = {
    header: "Header",
    primary: "Primary sidebar",
    main: "Page",
    secondary: "Secondary sidebar",
    footer: "Footer",
  };
  const ROWS = ["top", "middle", "bottom"];
  const ORDINAL = ["first", "second", "third"];
  const LETTERS = Object.fromEntries(
    Object.entries(RULES.areas).map(([letter, area]) => [letter, `${letter} (${LABELS[area].toLowerCase()})`])
  );

  const input = box.querySelector(".lp-code");
  const message = box.querySelector(".lp-msg");
  const grid = box.querySelector(".lp-grid");
  const chips = box.querySelector(".lp-chips");
  const explain = box.querySelector(".lp-explain");
  const snippet = box.querySelector(".lp-snippet code");
  const address = box.querySelector(".lp-address");

  const letterCount = RULES.positions.length;
  // One position per letter, with a space after each group of three.
  const SLOTS = RULES.positions.flatMap((taken, i) => (i && i % 3 === 0 ? [" ", taken] : [taken]));

  function listChoices(taken) {
    return [...taken].map((letter) => LETTERS[letter]).join(" or ");
  }

  function rulesSentence() {
    const rows = ROWS.map((row, r) => {
      const taken = RULES.positions.slice(r * 3, r * 3 + 3);
      return `the ${row} row is ${taken.map((t) => [...t].join(" or ")).join(", then ")}`;
    });
    return `Three groups of three letters: ${rows.join("; ")}.`;
  }

  // The key a code has in the rules: lower case except where case changes the layout.
  function lookup(raw) {
    const letters = raw.replace(/\s+/g, "");
    if (letters.length !== letterCount) return null;
    const key = [...letters]
      .map((letter, i) => (RULES.case.includes(i) ? letter : letter.toLowerCase()))
      .map((letter, i) => (i && i % 3 === 0 ? " " + letter : letter))
      .join("");
    const facts = RULES.layouts[key];
    if (!facts) return null;
    const code = [...letters].map((letter, i) => (i && i % 3 === 0 ? " " + letter : letter)).join("");
    return { code, rows: code.split(" "), lower: code.toLowerCase().split(" "), ...facts };
  }

  function describe(p) {
    const [top, , bottom] = p.lower;
    return [
      ["header", `${LABELS.header}: ${p.header_fixed ? "stays at the top as you scroll" : "scrolls away with the page"}. ` +
        (top[0] === "h" ? "It runs across above the primary sidebar" : "It starts beside the primary sidebar") +
        (top[2] === "h" ? " and above the secondary one." : ", and the secondary sidebar reaches the top beside it.")],
      ["primary", `${LABELS.primary}: ${p.primary_fixed ? "stays beside the page and scrolls on its own" : "scrolls with the page"}. ` +
        (top[0] === "l" ? "It reaches the top with the logo at its head" : "It starts under the header") +
        (bottom[0] === "l" ? " and runs to the bottom." : ", and the footer runs under it.")],
      ["main", `${LABELS.main}: always the centre.`],
      ["secondary", `${LABELS.secondary}: ${p.secondary_fixed ? "stays beside the page" : "scrolls with the page"}. ` +
        (top[2] === "r" ? "It reaches the top" : "It starts under the header") +
        (bottom[2] === "r" ? " and runs to the bottom." : ", and the footer runs under it.")],
      ["footer", `${LABELS.footer}: ${p.footer_fixed ? "stays at the bottom of the window" : "sits at the end of the page"}.`],
    ];
  }

  function render(p) {
    grid.style.setProperty("--lp-areas", box.dataset.screen === "xl" ? p.wide : p.medium);
    grid.style.setProperty("--lp-primary-top", p.primary_below_header ? "var(--lp-header)" : "0px");
    grid.style.setProperty("--lp-secondary-top", p.secondary_below_header ? "var(--lp-header)" : "0px");
    for (const area of ["header", "primary", "secondary", "footer"]) {
      grid.toggleAttribute(`data-${area}-fixed`, p[`${area}_fixed`]);
      box.querySelector(`[data-pin="${area}"]`).hidden = !p[`${area}_fixed`];
    }

    chips.replaceChildren();
    p.rows.forEach((row, r) => {
      if (r) chips.append(Object.assign(document.createElement("span"), { className: "lp-gap" }));
      for (const letter of row) {
        const fixed = letter !== letter.toLowerCase();
        const chip = document.createElement("span");
        chip.className = "lp-chip" + (fixed ? " is-fixed" : "");
        chip.dataset.area = RULES.areas[letter.toLowerCase()];
        chip.textContent = letter;
        chip.title = LABELS[chip.dataset.area] + (fixed ? ", stays in place" : "");
        chips.append(chip);
      }
    });

    explain.replaceChildren();
    for (const [area, text] of describe(p)) {
      const item = document.createElement("li");
      item.dataset.area = area;
      const dot = Object.assign(document.createElement("span"), { className: "lp-dot" });
      const words = document.createElement("span");
      words.textContent = text;
      item.append(dot, words);
      explain.append(item);
    }

    snippet.textContent = `html_theme_options = {"layout": "${p.code}"}`;
    address.textContent = `docs.example.org  ·  layout = "${p.code}"`;
    box.querySelectorAll("[data-code]").forEach((button) => {
      const on = button.dataset.code === p.code;
      button.classList.toggle("btn-primary", on);
      button.setAttribute("aria-pressed", String(on));
    });
  }

  let current = lookup(input.value);
  let refused = false;

  function update() {
    const p = lookup(input.value);
    if (!p) {
      // An unfinished code is fine while it is being typed: the mock-up keeps the last one.
      if (input.value.replace(/\s+/g, "").length < letterCount) {
        input.classList.remove("input-error");
        if (!refused) message.textContent = "";
        return;
      }
      input.classList.add("input-error");
      input.setAttribute("aria-invalid", "true");
      message.textContent = rulesSentence();
      return;
    }
    input.classList.remove("input-error");
    input.removeAttribute("aria-invalid");
    if (!refused) message.textContent = "";
    current = p;
    render(p);
  }

  /* Only what a layout code can hold gets into the field. Each position takes only
     its own letters, a space is added after each group of three, and anything else
     is refused with a sentence saying what that position takes. */
  function tidy(value) {
    const letters = value.replace(/\s+/g, "");
    let out = (letters.match(/.{1,3}/g) || []).join(" ");
    if (/\s$/.test(value) && letters.length && letters.length % 3 === 0 && letters.length < letterCount) out += " ";
    return out;
  }

  function firstWrong(value) {
    for (let i = 0; i < value.length; i++) {
      if (i >= SLOTS.length || !SLOTS[i].includes(value[i].toLowerCase())) return i;
    }
    return -1;
  }

  function refusal(index, character) {
    if (index >= SLOTS.length) return `A layout code is ${letterCount} letters, in three groups of three.`;
    const slot = index - Math.floor(index / 4);
    return `"${character}" can't go there. The ${ORDINAL[slot % 3]} letter of the ${ROWS[Math.floor(slot / 3)]} row is ${listChoices(SLOTS[index])}, in either case.`;
  }

  function choose(code) {
    input.value = accepted = code;
    refused = false;
    update();
  }

  input.maxLength = SLOTS.length;
  input.pattern = SLOTS.map((taken) => (taken === " " ? " " : `[${[...taken].map((l) => l + l.toUpperCase()).join("")}]`)).join("");
  input.title = rulesSentence();

  let accepted = input.value;
  input.addEventListener("input", () => {
    const tidied = tidy(input.value);
    const wrong = firstWrong(tidied);
    if (wrong !== -1) {
      input.value = accepted;
      message.textContent = refusal(wrong, tidied[wrong]);
      refused = true;
      return;
    }
    refused = false;
    if (tidied !== input.value) input.value = tidied;
    accepted = input.value;
    update();
  });
  box.querySelectorAll("[data-code]").forEach((button) =>
    button.addEventListener("click", () => choose(button.dataset.code))
  );
  box.querySelectorAll("[data-screen-choice]").forEach((button) =>
    button.addEventListener("click", () => {
      box.dataset.screen = button.dataset.screenChoice;
      box.querySelectorAll("[data-screen-choice]").forEach((other) => {
        other.classList.toggle("btn-primary", other === button);
        other.setAttribute("aria-pressed", String(other === button));
      });
      if (current) render(current);
    })
  );
  box.querySelector(".lp-form").addEventListener("submit", (event) => event.preventDefault());
  update();
})();
