const colourButtons = document.querySelectorAll("[data-copy]");
const toast = document.querySelector(".toast");
const toastValue = toast.querySelector("span");
const navLinks = document.querySelectorAll(".desktop-nav a");
const sections = [...document.querySelectorAll("main section[id]")];

let toastTimer;

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

  toastValue.textContent = value;
  toast.classList.add("visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("visible"), 1800);
}

colourButtons.forEach((button) => {
  button.addEventListener("click", () => copyText(button.dataset.copy));
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
