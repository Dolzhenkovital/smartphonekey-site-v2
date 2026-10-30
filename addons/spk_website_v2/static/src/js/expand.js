/** @odoo-module ignore **/
/* SmartphoneKey website 2.0: the expanded view of a product screenshot.
 *
 * A link marked data-spk-expand points at the full-size image, so without this
 * script it simply opens the image. With it, the link opens a modal <dialog>
 * with the same image, its alt text and a close button: Escape closes it (the
 * browser's own dialog behaviour), so does the close button and a click on the
 * backdrop, and focus returns to the link that opened it. Wide screenshots keep
 * a readable width inside the dialog and scroll sideways on a narrow screen
 * instead of shrinking into illegible text.
 */
(function () {
    "use strict";

    var links = Array.prototype.slice.call(document.querySelectorAll("a[data-spk-expand]"));
    if (!links.length || typeof HTMLDialogElement !== "function") {
        return;
    }

    var dialog = document.createElement("dialog");
    dialog.className = "expand-dialog";
    dialog.setAttribute("aria-label", links[0].getAttribute("data-spk-expand-dialog-label") || links[0].textContent.trim());
    dialog.innerHTML =
        '<div class="expand-inner">' +
        '<div class="expand-bar"><p class="expand-caption"></p>' +
        '<button type="button" class="button-outline expand-close">' +
        (links[0].getAttribute("data-spk-expand-close") || "Close") + "</button></div>" +
        '<div class="expand-scroll"><img alt=""/></div></div>';
    document.body.appendChild(dialog);

    var image = dialog.querySelector("img");
    var caption = dialog.querySelector(".expand-caption");
    var closeButton = dialog.querySelector(".expand-close");
    var opener = null;

    function open(link) {
        opener = link;
        image.src = link.getAttribute("href");
        image.alt = link.getAttribute("data-spk-expand-alt") || "";
        image.width = parseInt(link.getAttribute("data-spk-expand-width"), 10) || 0;
        image.height = parseInt(link.getAttribute("data-spk-expand-height"), 10) || 0;
        caption.textContent = link.getAttribute("data-spk-expand-alt") || "";
        dialog.showModal();
        closeButton.focus();
    }

    links.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            open(link);
        });
    });
    closeButton.addEventListener("click", function () {
        dialog.close();
    });
    dialog.addEventListener("click", function (event) {
        // The backdrop is the dialog element itself; its content is the inner box.
        if (event.target === dialog) {
            dialog.close();
        }
    });
    dialog.addEventListener("close", function () {
        image.removeAttribute("src");
        if (opener) {
            opener.focus();
            opener = null;
        }
    });
})();
