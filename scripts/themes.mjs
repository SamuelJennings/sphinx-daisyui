// Run with: npm run themes (npm run build runs it too)
// Writes src/sphinx_daisyui/themes.json from daisyUI's own list of themes, the one
// `themes: all` compiles into the stylesheet, in daisyUI's order. The file is written
// only when the list changes, so the development server, which rebuilds the site when
// a file under src/ changes and runs this script before each build, does not rebuild
// for ever.
import fs from "node:fs";
import order from "daisyui/functions/themeOrder.js";

const path = "src/sphinx_daisyui/themes.json";
const text = JSON.stringify(order) + "\n";
const current = fs.existsSync(path) ? fs.readFileSync(path, "utf8") : "";
if (current !== text) fs.writeFileSync(path, text);
console.log(order.length, "themes");
