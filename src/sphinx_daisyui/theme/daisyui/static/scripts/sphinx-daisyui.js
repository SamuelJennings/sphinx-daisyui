/* sphinx-daisyui: theme choice, navigation, page contents, search and the version switcher. */
(function () {
  "use strict";
  const root = document.documentElement;
  const body = document.body;
  const $ = (sel, el = document) => el.querySelector(sel);
  const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));
  const darkQuery = matchMedia("(prefers-color-scheme: dark)");

  /* ---------------------------------------------------------------- */
  /* Theme: a mode (system, light, dark) or one named daisyUI theme.   */
  /* ---------------------------------------------------------------- */

  function settleMode() {
    // A named theme decides light or dark itself, through its color-scheme.
    const scheme = getComputedStyle(root).colorScheme || "";
    root.dataset.mode = scheme.includes("dark") ? "dark" : "light";
  }

  function applyMode(mode) {
    const dark = mode === "dark" || (mode === "auto" && darkQuery.matches);
    root.dataset.theme = dark ? root.dataset.darkTheme : root.dataset.lightTheme;
    root.dataset.mode = dark ? "dark" : "light";
    root.dataset.modeChoice = mode;
    localStorage.setItem("daisy-mode", mode);
    localStorage.removeItem("daisy-theme");
    markChoice();
  }

  function applyTheme(name) {
    root.dataset.theme = name;
    root.dataset.modeChoice = "theme";
    localStorage.setItem("daisy-theme", name);
    settleMode();
    markChoice();
  }

  function markChoice() {
    const choice = root.dataset.modeChoice;
    $$("[data-daisy-set-mode]").forEach((b) => b.classList.toggle("menu-active", choice === b.dataset.daisySetMode));
    $$("[data-daisy-set-theme]").forEach((b) =>
      b.classList.toggle("menu-active", choice === "theme" && b.dataset.daisySetTheme === root.dataset.theme)
    );
  }

  $$("[data-daisy-set-mode]").forEach((b) => b.addEventListener("click", () => { applyMode(b.dataset.daisySetMode); blurMenu(); }));
  $$("[data-daisy-set-theme]").forEach((b) => b.addEventListener("click", () => { applyTheme(b.dataset.daisySetTheme); }));
  darkQuery.addEventListener("change", () => { if (root.dataset.modeChoice === "auto") applyMode("auto"); });
  if (root.dataset.modeChoice === "theme") settleMode();
  markChoice();

  function blurMenu() {
    if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
  }

  /* ---------------------------------------------------------------- */
  /* Sidebar navigation                                                */
  /* ---------------------------------------------------------------- */

  $$(".daisy-nav-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const list = button.closest("li").querySelector(":scope > ul");
      const open = button.getAttribute("aria-expanded") !== "true";
      button.setAttribute("aria-expanded", String(open));
      if (list) list.hidden = !open;
    });
  });

  const active = $(".daisy-nav .menu-active");
  const scroller = $(".daisy-sidebar-scroll");
  if (active && scroller) {
    const box = scroller.getBoundingClientRect();
    const at = active.getBoundingClientRect();
    if (at.bottom > box.bottom - 40 || at.top < box.top) scroller.scrollTop += at.top - box.top - box.height / 3;
  }

  const drawer = $("#daisy-drawer");
  $$(".daisy-area-primary a").forEach((a) => a.addEventListener("click", () => { if (drawer) drawer.checked = false; }));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && drawer && drawer.checked) drawer.checked = false; });

  /* ---------------------------------------------------------------- */
  /* On this page: the heading being read is marked as you scroll.     */
  /* ---------------------------------------------------------------- */

  const tocLinks = $$(".daisy-secondary .daisy-toc-link");
  $$(".daisy-toc-mobile a").forEach((a) => a.addEventListener("click", () => { a.closest("details").open = false; }));
  if (tocLinks.length && "IntersectionObserver" in window) {
    const byId = new Map();
    tocLinks.forEach((a) => {
      const id = decodeURIComponent((a.getAttribute("href") || "").replace(/^#/, ""));
      const target = id && document.getElementById(id);
      if (target) byId.set(target, a);
    });
    const visible = new Set();
    const mark = () => {
      let current = null;
      const targets = Array.from(byId.keys());
      for (const t of targets) {
        if (t.getBoundingClientRect().top < 120) current = t;
      }
      // At the foot of the page the last heading is the one being read, even if it never reached the top.
      if (innerHeight + scrollY >= document.documentElement.scrollHeight - 4) current = targets[targets.length - 1];
      tocLinks.forEach((a) => a.classList.remove("daisy-toc-current"));
      const link = current && byId.get(current);
      if (link) link.classList.add("daisy-toc-current");
    };
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((e) => (e.isIntersecting ? visible.add(e.target) : visible.delete(e.target)));
      mark();
    }, { rootMargin: "-64px 0px -60% 0px" });
    byId.forEach((_, t) => observer.observe(t));
    addEventListener("scroll", () => requestAnimationFrame(mark), { passive: true });
    mark();
  }

  /* ---------------------------------------------------------------- */
  /* Back to top: offered when the reader scrolls up, far down a page. */
  /* ---------------------------------------------------------------- */

  const topButton = $(".daisy-back-to-top");
  if (topButton) {
    let last = scrollY;
    addEventListener("scroll", () => {
      const y = scrollY;
      topButton.hidden = !(y < last && y > 600);
      last = y;
    }, { passive: true });
    topButton.addEventListener("click", () => { scrollTo({ top: 0, behavior: "smooth" }); $("#main-content").focus({ preventScroll: true }); topButton.hidden = true; });
  }

  /* ---------------------------------------------------------------- */
  /* Arrow keys move to the previous and next page, when switched on. */
  /* ---------------------------------------------------------------- */

  if (body.hasAttribute("data-daisy-keys")) {
    document.addEventListener("keydown", (e) => {
      if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
      if (/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) return;
      const rel = e.key === "ArrowLeft" ? "prev" : e.key === "ArrowRight" ? "next" : null;
      const link = rel && $(`.daisy-prev-next a[rel="${rel}"]`);
      if (link) location.href = link.href;
    });
  }

  /* ---------------------------------------------------------------- */
  /* Announcement fetched from a URL, as pydata-sphinx-theme allows.   */
  /* ---------------------------------------------------------------- */

  const banner = $("[data-daisy-announcement-body]");
  if (banner) {
    fetch(banner.closest("[data-daisy-announcement]").dataset.daisyAnnouncement)
      .then((r) => (r.ok ? r.text() : ""))
      .then((html) => { if (html.trim()) banner.innerHTML = html; else banner.closest(".daisy-announcement").remove(); })
      .catch(() => banner.closest(".daisy-announcement").remove());
  }

  /* ---------------------------------------------------------------- */
  /* Paths                                                             */
  /* ---------------------------------------------------------------- */

  const contentRoot = body.dataset.daisyRoot || "./";
  const builder = body.dataset.daisyBuilder;
  const linkSuffix = body.dataset.daisyLinkSuffix || ".html";
  function pageUrl(docname, anchor) {
    let path;
    if (builder === "dirhtml") path = docname === "index" ? "" : docname.replace(/(^|\/)index$/, "$1") + (docname.endsWith("index") ? "" : "/");
    else path = docname + linkSuffix;
    return contentRoot + path + (anchor ? "#" + anchor : "");
  }

  /* ---------------------------------------------------------------- */
  /* Version switcher, reading pydata-sphinx-theme's switcher.json.    */
  /* ---------------------------------------------------------------- */

  $$(".daisy-version").forEach((box) => {
    const list = $("[data-daisy-version-list]", box);
    const label = $("[data-daisy-version-label]", box);
    const match = box.dataset.versionMatch;
    let url = box.dataset.jsonUrl;
    if (!/^(https?:)?\/\//.test(url) && !url.startsWith("/")) url = contentRoot + url;
    fetch(url).then((r) => r.json()).then((versions) => {
      versions.forEach((v) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        const current = v.version === match;
        a.href = v.url;
        a.textContent = v.name || v.version;
        if (current) { a.classList.add("menu-active"); a.setAttribute("aria-current", "true"); label.textContent = v.name || v.version; }
        if (v.preferred) {
          const badge = document.createElement("span");
          badge.className = "badge badge-sm badge-success badge-soft";
          badge.textContent = "stable";
          a.append(badge);
        }
        a.addEventListener("click", (e) => {
          // Open the same page in the chosen version when it has one, else its home page.
          e.preventDefault();
          const page = pageUrl(body.dataset.daisyPage).slice(contentRoot.length);
          const target = v.url.replace(/\/?$/, "/") + page;
          fetch(target, { method: "HEAD" }).then((r) => { location.href = r.ok ? target : v.url; }).catch(() => { location.href = v.url; });
        });
        li.append(a);
        list.append(li);
      });
    }).catch(() => box.remove());
  });

  /* ---------------------------------------------------------------- */
  /* Search: results as you type, from Sphinx's own search index.      */
  /* ---------------------------------------------------------------- */

  const dialog = $("#daisy-search");
  if (!dialog) return;
  const input = $(".daisy-search-input", dialog);
  const results = $(".daisy-search-results", dialog);
  const status = $(".daisy-search-status", dialog);
  const isMac = /Mac|iPhone|iPad/.test(navigator.platform);
  if (isMac) $$("[data-daisy-mod]").forEach((k) => (k.textContent = "⌘"));
  let index = null;
  let loading = null;
  let chosen = -1;

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (!loading) {
      loading = fetch(contentRoot + "searchindex.js")
        .then((r) => r.text())
        .then((text) => {
          const json = text.slice(text.indexOf("(") + 1, text.lastIndexOf(")"));
          index = JSON.parse(json);
          return index;
        });
    }
    return loading;
  }

  function openSearch() {
    if (dialog.open) return;
    dialog.showModal();
    input.select();
    loadIndex().then(() => { if (input.value) run(); }).catch(() => { status.textContent = "Search isn't available on this copy of the documentation."; });
  }

  $$(".daisy-search-open").forEach((b) => b.addEventListener("click", openSearch));
  $$("[data-daisy-search-close]").forEach((b) => b.addEventListener("click", () => dialog.close()));
  document.addEventListener("keydown", (e) => {
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName) || document.activeElement.isContentEditable;
    if ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey)) { e.preventDefault(); openSearch(); }
    else if (e.key === "/" && !typing && !dialog.open) { e.preventDefault(); openSearch(); }
  });

  const escapeHtml = (s) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  function highlight(text, words) {
    let html = escapeHtml(text);
    words.forEach((w) => {
      if (w.length < 2) return;
      html = html.replace(new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>");
    });
    return html;
  }

  function stems(word) {
    // A light stemmer, close enough to Sphinx's Porter stems for matching as you type.
    const out = new Set([word]);
    for (const end of ["ing", "ed", "es", "s", "ation", "ions", "ion", "ly"]) {
      if (word.length > end.length + 2 && word.endsWith(end)) out.add(word.slice(0, -end.length));
    }
    return Array.from(out);
  }

  function lookup(table, word, exactScore, prefixScore, scores) {
    for (const s of stems(word)) {
      const hit = table[s];
      if (hit !== undefined) [].concat(hit).forEach((doc) => (scores[doc] = (scores[doc] || 0) + exactScore));
    }
    if (word.length >= 3) {
      for (const key in table) {
        if (key !== word && key.startsWith(word)) [].concat(table[key]).forEach((doc) => (scores[doc] = (scores[doc] || 0) + prefixScore));
      }
    }
  }

  function search(query) {
    const words = query.toLowerCase().split(/[^\p{L}\p{N}_.]+/u).filter(Boolean);
    if (!words.length) return [];
    const perWord = words.map((w) => {
      const scores = {};
      lookup(index.titleterms, w, 15, 6, scores);
      lookup(index.terms, w, 5, 2, scores);
      return scores;
    });
    // Every word must appear somewhere on a page.
    const pages = {};
    Object.keys(perWord[0]).forEach((doc) => {
      if (perWord.every((s) => s[doc])) pages[doc] = perWord.reduce((n, s) => n + s[doc], 0);
    });
    const items = [];
    const q = query.toLowerCase().trim();
    // Section titles that contain the whole query, linked to their heading.
    for (const [title, places] of Object.entries(index.alltitles || {})) {
      const t = title.toLowerCase();
      if (!words.every((w) => t.includes(w))) continue;
      places.forEach(([doc, anchor]) => {
        items.push({ kind: anchor ? "section" : "page", doc, anchor, title, page: index.titles[doc], score: (t === q ? 60 : t.startsWith(q) ? 45 : 35) + (pages[doc] || 0) / 10 });
      });
    }
    // API objects: functions, classes, options.
    const objnames = index.objnames || {};
    for (const [prefix, entries] of Object.entries(index.objects || {})) {
      for (const [doc, typeIndex, , anchor, name] of entries.map((e) => [e[0], e[1], e[2], e[3], e[4]])) {
        const full = (prefix ? prefix + "." : "") + name;
        const lower = full.toLowerCase();
        if (!words.every((w) => lower.includes(w))) continue;
        const kind = (objnames[typeIndex] || [])[2] || "object";
        let target = anchor === "" ? full : anchor === "-" ? (objnames[typeIndex] || [])[1] + "-" + full : anchor;
        items.push({ kind: "api", label: kind, doc, anchor: target, title: full, page: index.titles[doc], score: (lower.endsWith(q) ? 55 : 40) });
      }
    }
    // Pages whose text holds every word.
    const listed = new Set(items.filter((i) => i.kind === "page").map((i) => i.doc));
    Object.entries(pages).forEach(([doc, score]) => {
      if (!listed.has(Number(doc))) items.push({ kind: "page", doc: Number(doc), title: index.titles[doc], score: score });
    });
    items.sort((a, b) => b.score - a.score);
    const seen = new Set();
    return items.filter((i) => {
      const key = i.doc + "#" + (i.anchor || "");
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    }).slice(0, 30).map((i) => ({ ...i, words }));
  }

  function render(items) {
    results.innerHTML = "";
    chosen = -1;
    if (!input.value.trim()) { status.hidden = false; status.textContent = "Type to search pages, sections and API names."; return; }
    if (!items.length) { status.hidden = false; status.innerHTML = "Nothing matches <strong>" + escapeHtml(input.value) + "</strong>."; return; }
    status.hidden = true;
    items.forEach((item, n) => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = pageUrl(index.docnames[item.doc], item.anchor);
      a.id = "daisy-search-option-" + n;
      a.setAttribute("role", "option");
      a.className = "flex items-start gap-3 py-2";
      const iconName = item.kind === "api" ? "file-code" : item.kind === "section" ? "list" : "book-open";
      const kindLabel = item.kind === "api" ? item.label : item.kind === "section" ? "Section" : "Page";
      a.innerHTML =
        '<span class="badge badge-sm badge-ghost mt-0.5 w-16 shrink-0 justify-center capitalize">' + escapeHtml(kindLabel) + "</span>" +
        '<span class="min-w-0"><span class="block truncate font-medium">' + highlight(item.title, item.words) + "</span>" +
        (item.kind !== "page" && item.page ? '<span class="block truncate text-xs opacity-60">' + escapeHtml(item.page.replace(/<[^>]+>/g, "")) + "</span>" : "") +
        "</span>";
      a.addEventListener("click", () => dialog.close());
      li.append(a);
      results.append(li);
    });
  }

  function run() {
    if (!index) return;
    render(search(input.value));
  }

  function choose(n) {
    const options = $$("a[role=option]", results);
    if (!options.length) return;
    chosen = (n + options.length) % options.length;
    options.forEach((o, i) => o.classList.toggle("menu-active", i === chosen));
    options[chosen].scrollIntoView({ block: "nearest" });
    input.setAttribute("aria-activedescendant", options[chosen].id);
  }

  let timer;
  input.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(() => loadIndex().then(run), 60); });
  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); choose(chosen + 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); choose(chosen - 1); }
    else if (e.key === "Enter" && chosen >= 0) {
      e.preventDefault();
      const option = $$("a[role=option]", results)[chosen];
      dialog.close();
      location.href = option.href;
    }
  });
})();
