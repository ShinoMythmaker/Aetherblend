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
