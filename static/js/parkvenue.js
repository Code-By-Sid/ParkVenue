/* ParkVenue — parkvenue.js
   Shared interactions: scroll reveal, animated counters, navbar state,
   menu dropdowns, password visibility toggles, toasts. */

(function () {
    "use strict";

    /* ---- Scroll reveal ---- */
    function initReveal() {
        var els = document.querySelectorAll(".reveal");
        if (!els.length) return;
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.classList.add("visible");
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.12 });
        els.forEach(function (el) { io.observe(el); });
    }

    /* ---- Animated number counters (data-count attr) ---- */
    function initCounters() {
        var counters = document.querySelectorAll("[data-count]");
        if (!counters.length) return;
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var el = entry.target;
                var target = parseInt(el.getAttribute("data-count"), 10) || 0;
                var suffix = el.getAttribute("data-suffix") || "";
                var duration = 1600;
                var start = null;
                function step(ts) {
                    if (!start) start = ts;
                    var p = Math.min((ts - start) / duration, 1);
                    var eased = 1 - Math.pow(1 - p, 3);
                    el.textContent = Math.round(target * eased).toLocaleString() + suffix;
                    if (p < 1) requestAnimationFrame(step);
                }
                requestAnimationFrame(step);
                io.unobserve(el);
            });
        }, { threshold: 0.4 });
        counters.forEach(function (el) { io.observe(el); });
    }

    /* ---- Navbar shadow on scroll ---- */
    function initNav() {
        var nav = document.querySelector(".site-nav");
        if (!nav) return;
        function onScroll() {
            nav.classList.toggle("scrolled", window.scrollY > 12);
        }
        window.addEventListener("scroll", onScroll, { passive: true });
        onScroll();
    }

    /* ---- Menu dropdown toggle (works for any .menu-icon) ---- */
    window.toggleMenu = function (event) {
        if (event) event.stopPropagation();
        var menu = event && event.currentTarget
            ? event.currentTarget.querySelector(".menu-dropdown")
            : document.querySelector(".menu-dropdown");
        if (menu) menu.classList.toggle("show");
    };
    document.addEventListener("click", function (event) {
        if (!event.target.closest(".menu-icon")) {
            document.querySelectorAll(".menu-dropdown.show").forEach(function (d) {
                d.classList.remove("show");
            });
        }
    });

    /* ---- Password visibility toggles ---- */
    function initPasswordToggles() {
        document.querySelectorAll(".toggle-pass").forEach(function (btn) {
            btn.addEventListener("click", function () {
                var input = btn.closest(".field").querySelector("input");
                if (!input) return;
                var showing = input.type === "text";
                input.type = showing ? "password" : "text";
                btn.className = "toggle-pass bx " + (showing ? "bx-hide" : "bx-show");
            });
        });
    }

    /* ---- Toast helper ---- */
    window.pvToast = function (message, icon) {
        var t = document.createElement("div");
        t.className = "toast";
        t.innerHTML = '<i class=\'bx ' + (icon || "bx-check-circle") + '\'></i><span></span>';
        t.querySelector("span").textContent = message;
        document.body.appendChild(t);
        requestAnimationFrame(function () { t.classList.add("show"); });
        setTimeout(function () {
            t.classList.remove("show");
            setTimeout(function () { t.remove(); }, 500);
        }, 3200);
    };

    /* ---- Subtle parallax on hero visual ---- */
    function initParallax() {
        var visual = document.querySelector(".hero-visual");
        if (!visual || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
        window.addEventListener("mousemove", function (e) {
            var x = (e.clientX / window.innerWidth - 0.5) * 14;
            var y = (e.clientY / window.innerHeight - 0.5) * 10;
            visual.style.transform = "translate(" + x + "px," + y + "px)";
        }, { passive: true });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initReveal();
        initCounters();
        initNav();
        initPasswordToggles();
        initParallax();
    });
})();
