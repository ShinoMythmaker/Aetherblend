// Point download buttons at the newest release zip; the static href is the fallback.
const downloads = document.querySelectorAll("[data-latest-zip]");
if (downloads.length) {
  fetch("https://api.github.com/repos/ShinoMythmaker/Aetherblend/releases/latest")
    .then((response) => (response.ok ? response.json() : Promise.reject()))
    .then((release) => {
      const zip = release.assets.find((asset) => asset.name.endsWith(".zip"));
      if (!zip) return;
      downloads.forEach((link) => {
        // Keep the ?repository=... query so Blender still knows which repository the zip belongs to.
        const query = link.href.includes("?") ? link.href.slice(link.href.indexOf("?")) : "";
        link.href = zip.browser_download_url + query;
      });
    })
    .catch(() => {});
}

const button = document.querySelector(".menu-btn");
if (button) {
  button.addEventListener("click", () => document.body.classList.toggle("nav-open"));
  document.querySelectorAll(".sidebar a").forEach((link) =>
    link.addEventListener("click", () => document.body.classList.remove("nav-open")),
  );
}

document.querySelectorAll("pre").forEach((pre) => {
  const snippet = pre.closest(".codehilite") || pre;
  const block = document.createElement("div");
  block.className = "code-block";
  snippet.before(block);
  block.append(snippet);

  const copy = document.createElement("button");
  copy.type = "button";
  copy.className = "code-copy";
  copy.textContent = "Copy";
  copy.setAttribute("aria-label", "Copy code to clipboard");

  const status = document.createElement("p");
  status.className = "code-copy-status";
  status.setAttribute("role", "status");
  status.hidden = true;
  block.append(copy, status);

  let resetTimer;
  copy.addEventListener("click", async () => {
    clearTimeout(resetTimer);
    copy.disabled = true;
    copy.textContent = "Copy";
    status.hidden = true;
    try {
      if (!navigator.clipboard?.writeText) {
        throw new Error("Clipboard access is unavailable in this browser or context.");
      }
      await navigator.clipboard.writeText(pre.textContent);
      copy.textContent = "Copied!";
      status.textContent = "Code copied to clipboard.";
      resetTimer = setTimeout(() => { copy.textContent = "Copy"; }, 2000);
    } catch (error) {
      console.error("[AetherBlend] Could not copy code to the clipboard.", error);
      copy.textContent = "Copy failed";
      status.textContent = "Could not access the clipboard. Select the code and copy it manually.";
    } finally {
      copy.disabled = false;
      status.hidden = false;
    }
  });
});
