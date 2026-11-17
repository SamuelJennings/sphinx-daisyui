// Collect the SVG icons the theme draws into one JSON file the Python side reads.
// Interface icons come from Lucide (ISC), brand icons from Simple Icons (CC0).
import fs from "node:fs";
import * as si from "simple-icons";
const lucide = ["search","sun","moon","sun-moon","menu","x","chevron-right","chevron-down","pencil","file-code","arrow-up","arrow-left","arrow-right","external-link","palette","list","copy","check","link","book-open","history","languages","megaphone","square-arrow-out-up-right"];
const brands = {github:"siGithub",gitlab:"siGitlab",bitbucket:"siBitbucket","x-twitter":"siX",mastodon:"siMastodon",discord:"siDiscord",pypi:"siPypi",python:"siPython",youtube:"siYoutube",discourse:"siDiscourse",stackoverflow:"siStackoverflow",readthedocs:"siReadthedocs",bluesky:"siBluesky",matrix:"siMatrix",zulip:"siZulip",condaforge:"siCondaforge",docker:"siDocker",npm:"siNpm",anaconda:"siAnaconda",codeberg:"siCodeberg",orcid:"siOrcid",zenodo:"siZenodo",jupyter:"siJupyter"};
const out = {};
for (const name of lucide) {
  let svg = fs.readFileSync(`node_modules/lucide-static/icons/${name}.svg`, "utf8");
  svg = svg.replace(/<!--[\s\S]*?-->/g, "").replace(/\s*class="[^"]*"/, "").replace(/\s+width="24"\s+height="24"/, "").replace(/\n\s*/g, " ").trim();
  out[name] = svg;
}
for (const [name, key] of Object.entries(brands)) {
  const icon = si[key];
  if (!icon) { console.error("missing brand", name); continue; }
  out[name] = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="${icon.path}"/></svg>`;
}
fs.writeFileSync("src/sphinx_daisyui/icons.json", JSON.stringify(out, null, 0));
console.log(Object.keys(out).length, "icons");
