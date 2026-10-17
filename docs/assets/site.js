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
      resetTimer = setTimeout(() => { copy.textContent = "Copy"; }, 2000);
    } catch (error) {
      console.error("[AetherBlend] Could not copy code to the clipboard.", error);
      copy.textContent = "Copy failed";
      status.textContent = "Could not access the clipboard. Select the code and copy it manually.";
      status.hidden = false;
    } finally {
      copy.disabled = false;
    }
  });
});
