const BRANDS = {
  aviation: { name: "GatesPort Aviation", stem: "gates-port-logo" },
  cargo: { name: "GatesPort Cargo", stem: "gates-port-cargo-logo" },
  catering: { name: "GatesPort Catering", stem: "gates-port-catering-logo" },
  vip: { name: "GatesPort VIP", stem: "gates-port-vip-logo" },
};

const COLOURS = {
  burgundy: { label: "Burgundy", hex: "#48151D", ground: "cream" },
  gold: { label: "Antique gold", hex: "#B39567", ground: "burgundy" },
  cream: { label: "Warm cream", hex: "#F0E5D2", ground: "espresso" },
  black: { label: "Black", hex: "#111111", ground: "gold" },
  white: { label: "White", hex: "#FFFFFF", ground: "black" },
};

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

const live = $("#live");
const stage = $("#stage");
const stageImg = $("#stage-img");
const tabs = $$(".gate-tab");
const swatches = $$(".swatch");
const isRtl = () => document.documentElement.dir === "rtl";

const state = { brand: "aviation", colour: "gold" };
const timers = new WeakMap();

const logoFile = (brand, colour, ext) => `assets/logos/${BRANDS[brand].stem}-${colour}.${ext}`;

/* ---------- Feedback ---------- */

function announce(message) {
  live.textContent = "";
  requestAnimationFrame(() => {
    live.textContent = message;
  });
}

// A control shows its own result: the label swaps and settles back.
function flash(control, label, outcome = "done") {
  const labelNode = $("span", control) || control;
  if (!timers.has(control)) control.dataset.original = labelNode.textContent;
  clearTimeout(timers.get(control));
  labelNode.textContent = label;
  control.dataset.state = outcome;
  timers.set(
    control,
    setTimeout(() => {
      labelNode.textContent = control.dataset.original;
      delete control.dataset.state;
      timers.delete(control);
    }, 1800),
  );
}

async function copyText(value) {
  try {
    await navigator.clipboard.writeText(value);
    return true;
  } catch {
    const input = document.createElement("textarea");
    input.value = value;
    input.setAttribute("readonly", "");
    input.style.position = "fixed";
    input.style.opacity = "0";
    document.body.appendChild(input);
    input.select();
    const ok = document.execCommand("copy");
    input.remove();
    return ok;
  }
}

function copyImageFallback(source) {
  const selection = window.getSelection();
  const range = document.createRange();
  const container = document.createElement("div");
  const image = document.createElement("img");

  container.contentEditable = "true";
  container.style.position = "fixed";
  container.style.left = "-10000px";
  image.src = new URL(source, window.location.href).href;
  container.appendChild(image);
  document.body.appendChild(container);
  range.selectNode(image);
  selection.removeAllRanges();
  selection.addRange(range);
  const copied = document.execCommand("copy");
  selection.removeAllRanges();
  container.remove();
  return copied;
}

async function copyLogo(button) {
  const source = button.dataset.copyImage;
  const label = button.dataset.copyLabel || "Logo";
  button.disabled = true;

  try {
    if (navigator.clipboard?.write && window.ClipboardItem) {
      const response = await fetch(source);
      if (!response.ok) throw new Error("Logo could not be loaded");
      const blob = await response.blob();
      const pngBlob = blob.type === "image/png" ? blob : new Blob([blob], { type: "image/png" });
      await navigator.clipboard.write([new ClipboardItem({ "image/png": pngBlob })]);
    } else if (!copyImageFallback(source)) {
      throw new Error("Image clipboard is unavailable");
    }
    flash(button, "Copied");
    announce(`${label} copied. Ready to paste.`);
  } catch {
    flash(button, "Use PNG", "fail");
    announce("Image copy is unavailable here. Use Download PNG instead.");
  } finally {
    button.disabled = false;
  }
}

document.addEventListener("click", async (event) => {
  const logoButton = event.target.closest("[data-copy-image]");
  if (logoButton) return copyLogo(logoButton);

  const colourButton = event.target.closest("[data-copy]");
  if (colourButton) {
    const value = colourButton.dataset.copy;
    const ok = await copyText(value);
    colourButton.dataset.state = ok ? "done" : "fail";
    announce(ok ? `Copied ${value}` : `Could not copy ${value}`);
    clearTimeout(timers.get(colourButton));
    timers.set(colourButton, setTimeout(() => delete colourButton.dataset.state, 1800));
    return;
  }

  const pick = event.target.closest("[data-pick]");
  if (pick) {
    event.preventDefault();
    select(pick.dataset.pick, "gold", { focus: false });
    $("#logos").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }
});

/* ---------- Picker ---------- */

function select(brand, colour, { focus = true } = {}) {
  const changed = brand !== state.brand || colour !== state.colour;
  state.brand = brand;
  state.colour = colour;

  const b = BRANDS[brand];
  const c = COLOURS[colour];
  const png = logoFile(brand, colour, "png");
  const svg = logoFile(brand, colour, "svg");

  tabs.forEach((tab) => {
    const active = tab.dataset.brand === brand;
    tab.setAttribute("aria-selected", String(active));
    tab.tabIndex = active ? 0 : -1;
    if (active && focus) tab.focus();
  });
  $("#picker-panel").setAttribute("aria-labelledby", `tab-${brand}`);

  swatches.forEach((swatch) => {
    const active = swatch.dataset.colour === colour;
    swatch.setAttribute("aria-checked", String(active));
    swatch.tabIndex = active ? 0 : -1;
    $("img", swatch).src = logoFile(brand, swatch.dataset.colour, "png");
    if (active && focus && document.activeElement?.closest(".swatches")) swatch.focus();
  });

  const paint = () => {
    stage.dataset.ground = c.ground;
    stageImg.src = png;
    stageImg.alt = `${b.name} logo in ${c.label.toLowerCase()}`;
    stage.classList.remove("is-swapping");
  };

  if (changed && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    stage.classList.add("is-swapping");
    setTimeout(paint, 180);
  } else {
    paint();
  }

  $("#stage-meta").textContent = `${b.name} · ${c.label} · ${c.hex}`;
  $("#take-name").textContent = b.name;
  $("#take-colour").innerHTML = `${c.label} <span>${c.hex}</span>`;
  $("#take-file").textContent = `${b.stem}-${colour}`;
  $("#take-png").href = png;
  $("#take-svg").href = svg;

  const copy = $("#take-copy");
  copy.dataset.copyImage = png;
  copy.dataset.copyLabel = `${b.name} ${c.label.toLowerCase()} logo`;
}

function moveSelection(items, current, event, activate) {
  const forward = isRtl() ? ["ArrowLeft", "ArrowDown"] : ["ArrowRight", "ArrowDown"];
  const backward = isRtl() ? ["ArrowRight", "ArrowUp"] : ["ArrowLeft", "ArrowUp"];
  let next = items.indexOf(current);
  if (forward.includes(event.key)) next = (next + 1) % items.length;
  else if (backward.includes(event.key)) next = (next - 1 + items.length) % items.length;
  else if (event.key === "Home") next = 0;
  else if (event.key === "End") next = items.length - 1;
  else return;
  event.preventDefault();
  activate(items[next]);
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => select(tab.dataset.brand, state.colour, { focus: false }));
  tab.addEventListener("keydown", (event) =>
    moveSelection(tabs, tab, event, (next) => select(next.dataset.brand, state.colour)),
  );
});

swatches.forEach((swatch) => {
  swatch.addEventListener("click", () => select(state.brand, swatch.dataset.colour, { focus: false }));
  swatch.addEventListener("keydown", (event) =>
    moveSelection(swatches, swatch, event, (next) => {
      select(state.brand, next.dataset.colour, { focus: false });
      next.focus();
    }),
  );
});

/* ---------- Wayfinding: current section and progress ---------- */

const navLinks = $$(".deck-nav a");
const sections = $$("main section[id]");

const spy = new IntersectionObserver(
  (entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    navLinks.forEach((link) => {
      if (link.getAttribute("href") === `#${visible.target.id}`) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
  },
  { rootMargin: "-30% 0px -55%", threshold: [0, 0.2, 0.6] },
);
sections.forEach((section) => spy.observe(section));

const root = document.documentElement;
let ticking = false;
function updateProgress() {
  const max = root.scrollHeight - innerHeight;
  root.style.setProperty("--progress", max > 0 ? Math.min(scrollY / max, 1).toFixed(4) : "0");
  ticking = false;
}
addEventListener(
  "scroll",
  () => {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(updateProgress);
    }
  },
  { passive: true },
);
updateProgress();
