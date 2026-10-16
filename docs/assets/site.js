const button = document.querySelector(".menu-btn");
if (button) {
  button.addEventListener("click", () => document.body.classList.toggle("nav-open"));
  document.querySelectorAll(".sidebar a").forEach((link) =>
    link.addEventListener("click", () => document.body.classList.remove("nav-open")),
  );
}
