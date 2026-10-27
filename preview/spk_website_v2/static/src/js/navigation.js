/** @odoo-module ignore **/
/* SmartphoneKey website 2.0: header menus.
 *
 * The menus are <details> disclosures, so they open by click and keyboard and
 * work without this script. It adds: one menu open at a time, Escape closes
 * and returns focus to the trigger, a click outside closes, and the mobile
 * menu closes after a link is followed.
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

    menus.forEach(function (menu) {
        menu.addEventListener("toggle", function () {
            if (menu.open) {
                closeAll(menu);
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

    document.addEventListener("click", function (event) {
        menus.forEach(function (menu) {
            if (menu.open && !menu.contains(event.target)) {
                menu.open = false;
            }
        });
    });
})();
