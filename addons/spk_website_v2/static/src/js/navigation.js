/** @odoo-module ignore **/
/* SmartphoneKey website 2.0: header menus.
 *
 * The four navigation menus, the language menu in the utility row and the
 * mobile menu are <details> disclosures, so they open by click and keyboard and
 * work without this script. It adds: one menu open at a time (across all three
 * kinds), Escape closes and returns focus to the trigger, a click outside
 * closes, a menu closes after a link inside it is followed, and everything
 * closes when the window crosses the mobile breakpoint. While the mobile menu is
 * open the page behind it does not scroll (class spk-menu-open on <html>, and the
 * panel starts where the header ends).
 */
(function () {
    "use strict";

    var menus = Array.prototype.slice.call(document.querySelectorAll("[data-spk-menu], [data-spk-mobile-menu]"));
    if (!menus.length) {
        return;
    }

    function closeAll(except) {
        menus.forEach(function (menu) {
            if (menu !== except && menu.open) {
                menu.open = false;
            }
        });
    }

    var root = document.documentElement;
    var header = document.querySelector(".site-header");

    function syncMobileMenu(menu) {
        if (menu.open) {
            if (header) {
                root.style.setProperty("--spk-menu-top", Math.max(0, Math.round(header.getBoundingClientRect().bottom)) + "px");
            }
            root.classList.add("spk-menu-open");
        } else {
            root.classList.remove("spk-menu-open");
            root.style.removeProperty("--spk-menu-top");
        }
    }

    menus.forEach(function (menu) {
        menu.addEventListener("toggle", function () {
            if (menu.open) {
                closeAll(menu);
            }
            if (menu.hasAttribute("data-spk-mobile-menu")) {
                syncMobileMenu(menu);
            }
        });
        menu.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                menu.open = false;
            });
        });
    });

    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") {
            return;
        }
        menus.forEach(function (menu) {
            if (menu.open) {
                menu.open = false;
                menu.querySelector("summary").focus();
            }
        });
    });

    // The desktop menus and the mobile menu never show together; start clean when the layout switches.
    if (window.matchMedia) {
        var mobile = window.matchMedia("(max-width: 960px)");
        var wasMobile = mobile.matches;
        var onLayoutChange = function () {
            if (mobile.matches !== wasMobile) {
                wasMobile = mobile.matches;
                closeAll(null);
            }
        };
        if (mobile.addEventListener) {
            mobile.addEventListener("change", onLayoutChange);
        } else if (mobile.addListener) {
            mobile.addListener(onLayoutChange);
        }
    }

    document.addEventListener("click", function (event) {
        menus.forEach(function (menu) {
            if (menu.open && !menu.contains(event.target)) {
                menu.open = false;
            }
        });
    });
})();
