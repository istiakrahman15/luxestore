/* LuxeStore — vanilla JS interactions (no frameworks, no external deps) */
(function () {
  "use strict";

  /* ---------- Dark / Light theme toggle ---------- */
  const root = document.documentElement;
  const THEME_KEY = "luxestore-theme";
  const toggleBtn = document.getElementById("theme-toggle");

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (toggleBtn) {
      const icon = toggleBtn.querySelector("i");
      if (icon) {
        icon.className = theme === "dark" ? "bi bi-moon-stars" : "bi bi-sun";
      }
    }
  }

  const savedTheme =
    localStorage.getItem(THEME_KEY) ||
    (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
  applyTheme(savedTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
      const current = root.getAttribute("data-theme");
      const next = current === "dark" ? "light" : "dark";
      applyTheme(next);
      localStorage.setItem(THEME_KEY, next);
    });
  }

  /* ---------- Scroll-to-top button ---------- */
  const scrollBtn = document.getElementById("scroll-top-btn");
  if (scrollBtn) {
    window.addEventListener("scroll", function () {
      scrollBtn.classList.toggle("visible", window.scrollY > 480);
    });
    scrollBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- Scroll reveal ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  }

  /* ---------- Navbar background on scroll ---------- */
  const navbar = document.querySelector(".navbar-luxe");
  if (navbar) {
    window.addEventListener("scroll", function () {
      navbar.classList.toggle("scrolled", window.scrollY > 8);
    });
  }

  /* ---------- Newsletter form (UI only, no backend) ---------- */
  const newsletterForm = document.getElementById("newsletter-form");
  if (newsletterForm) {
    newsletterForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const feedback = document.getElementById("newsletter-feedback");
      const input = document.getElementById("newsletter-email");
      if (feedback) {
        feedback.textContent = "Thanks — this is a UI-only demo, so nothing was actually sent.";
        feedback.classList.remove("d-none");
      }
      if (input) input.value = "";
    });
  }
})();
