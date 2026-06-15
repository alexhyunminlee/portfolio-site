/* ============================================================
   Parallax scroll effect on the hero section
   ============================================================ */
(function () {
  const hero = document.getElementById("hero");
  if (!hero) return;

  let rafId = null;

  window.addEventListener(
    "scroll",
    () => {
      if (rafId) return;
      rafId = requestAnimationFrame(() => {
        const scrollY = window.scrollY;
        // Shift the hero content upward at 30% of scroll speed
        hero.style.transform = `translateY(${scrollY * 0.3}px)`;
        hero.style.opacity = Math.max(0, 1 - scrollY / 400);
        rafId = null;
      });
    },
    { passive: true }
  );
})();

/* ============================================================
   Active nav link highlighting based on current pathname
   ============================================================ */
(function () {
  const path = window.location.pathname;

  document.querySelectorAll(".nav-link").forEach((link) => {
    const href = link.getAttribute("href");
    const isActive = href === path || (href !== "/" && path.startsWith(href));

    if (isActive) {
      link.classList.add("text-white");
      link.classList.remove("text-gray-400");
    }
  });
})();
