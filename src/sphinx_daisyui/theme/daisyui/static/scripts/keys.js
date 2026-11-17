/* Keyboard shortcuts: one place to ask whether the reader is typing, and one to bind a key. */
(function () {
  "use strict";

  window.sphinxDaisyui = window.sphinxDaisyui || {};

  /* True while the reader is in a field, so a shortcut leaves their typing alone. */
  function isTyping() {
    const el = document.activeElement;
    if (!el) return false;
    return el.matches("input, textarea, select") || el.isContentEditable;
  }

  /* Run a handler when a key is pressed, unless Alt, Ctrl or Meta is held. */
  function on(key, handler) {
    document.addEventListener("keydown", (event) => {
      if (event.key !== key || event.altKey || event.ctrlKey || event.metaKey) return;
      handler(event);
    });
  }

  window.sphinxDaisyui.keys = { isTyping: isTyping, on: on };
})();
