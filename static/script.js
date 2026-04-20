/* Small UX helpers — no framework */
(function () {
  const prefersReduced =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Focus first invalid field on failed native validation (optional enhancement)
  const form = document.getElementById("trip-form");
  if (form && !prefersReduced) {
    form.addEventListener("submit", function () {
      window.requestAnimationFrame(function () {
        const invalid = form.querySelector(":invalid");
        if (invalid && typeof invalid.focus === "function") {
          invalid.focus({ preventScroll: true });
        }
      });
    });
  }
})();
