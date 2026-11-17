// Run with: npm run themes (npm run build runs it too)
// Writes src/sphinx_daisyui/themes.json from daisyUI's own list of themes, the one
// `themes: all` compiles into the stylesheet, in daisyUI's order.
import fs from "node:fs";
import order from "daisyui/functions/themeOrder.js";

fs.writeFileSync("src/sphinx_daisyui/themes.json", JSON.stringify(order) + "\n");
console.log(order.length, "themes");
