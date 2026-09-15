const colourButtons = document.querySelectorAll("[data-copy]");
const logoCopyButtons = document.querySelectorAll("[data-copy-image]");
const toast = document.querySelector(".toast");
const toastValue = toast.querySelector("span");
const navLinks = document.querySelectorAll(".desktop-nav a");
const sections = [...document.querySelectorAll("main section[id]")];

let toastTimer;

function showToast(message) {
  toastValue.textContent = message;
  toast.classList.add("visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("visible"), 2400);
}

async function copyText(value) {
  try {
    await navigator.clipboard.writeText(value);
  } catch {
    const input = document.createElement("textarea");
    input.value = value;
    input.setAttribute("readonly", "");
    input.style.position = "fixed";
    input.style.opacity = "0";
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    input.remove();
  }

  showToast(`Copied ${value}`);
}

colourButtons.forEach((button) => {
  button.addEventListener("click", () => copyText(button.dataset.copy));
});

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
  button.setAttribute("aria-busy", "true");

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

    showToast(`${label} copied — ready to paste.`);
  } catch {
    showToast("Image copy is unavailable here. Use Download PNG instead.");
  } finally {
    button.disabled = false;
    button.removeAttribute("aria-busy");
  }
}

logoCopyButtons.forEach((button) => {
  button.addEventListener("click", () => copyLogo(button));
});

const sectionObserver = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (!visible) return;

    navLinks.forEach((link) => {
      const active = link.getAttribute("href") === `#${visible.target.id}`;
      if (active) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
  },
  { rootMargin: "-25% 0px -60%", threshold: [0, 0.2, 0.6] },
);

sections.forEach((section) => sectionObserver.observe(section));
