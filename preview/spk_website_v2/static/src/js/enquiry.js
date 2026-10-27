/** @odoo-module ignore **/
/* SmartphoneKey website 2.0: the contact form.
 *
 * The form works as an ordinary POST. This script checks the required fields
 * in place, sends the same form asking for JSON, and shows "received" only
 * when the server answers that the lead exists. On any failure the values
 * stay in the form, nothing is copied to the URL, storage or analytics, and
 * the same submission ID is reused so a retry cannot create a second lead.
 */
(function () {
    "use strict";

    var form = document.querySelector("[data-spk-enquiry]");
    if (!form) {
        return;
    }
    var preview = form.hasAttribute("data-preview");
    var summary = form.querySelector("[data-spk-error-summary]");
    var submit = form.querySelector("[data-spk-submit]");
    var status = form.querySelector("[data-spk-status]");
    var success = document.querySelector("[data-spk-success]");
    var aside = document.querySelector(".contact-aside");
    var idleLabel = submit.textContent;
    var pending = false;
    var reported = {};
    // Every message comes from the page, in the visitor's language.
    var text = {};
    form.querySelectorAll("[data-spk-messages] [data-key]").forEach(function (node) {
        text[node.getAttribute("data-key")] = node.textContent.trim();
    });
    var sendError = text.send;
    var messages = {name: text.name, email: text.email, enquiry_type: text.enquiry_type};
    var formMessages = {conflict: text.conflict, preview: text.preview};

    // Prefill from enum query parameters when the server could not (the static preview).
    var params = new URLSearchParams(window.location.search);
    var interestMap = {visitor: ["project", "visitors"], automation: ["project", "automation"], technical: ["compatibility"]};
    if (params.get("interest") && !form.elements.enquiry_type.value) {
        var mapped = interestMap[params.get("interest")] || [params.get("interest")];
        setChoice("enquiry_type", mapped[0]);
        if (mapped[1]) {
            params.append("interests", mapped[1]);
        }
    }
    ["role", "sites", "doors", "connection"].forEach(function (name) {
        if (params.get(name) && !form.elements[name].value) {
            setChoice(name, params.get(name));
        }
    });
    params.getAll("interests").forEach(function (key) {
        var box = form.querySelector("input[name='interests'][value='" + CSS.escape(key) + "']");
        if (box) {
            box.checked = true;
        }
    });

    function setChoice(name, value) {
        var select = form.elements[name];
        if (select && Array.prototype.some.call(select.options, function (option) { return option.value === value; })) {
            select.value = value;
        }
    }

    if (preview) {
        // Without this script the preview's button stays disabled; with it, the checks can be tried.
        submit.disabled = false;
    }
    if (!summary.hidden) {
        // The server sent the form back with errors (a submission without this script).
        summary.focus();
    }

    function fieldBox(name) {
        return form.querySelector("#field-" + name).closest(".field");
    }

    function clearErrors() {
        form.querySelectorAll(".field[data-invalid]").forEach(function (box) {
            box.removeAttribute("data-invalid");
            var error = box.querySelector(".field-error");
            if (error) {
                error.remove();
            }
            var input = box.querySelector("input, select, textarea");
            input.removeAttribute("aria-invalid");
            var described = (input.getAttribute("aria-describedby") || "").split(" ").filter(function (id) {
                return id && id.indexOf("-error") === -1;
            });
            if (described.length) {
                input.setAttribute("aria-describedby", described.join(" "));
            } else {
                input.removeAttribute("aria-describedby");
            }
        });
        summary.hidden = true;
        summary.textContent = "";
    }

    function showErrors(title, errors) {
        var list = document.createElement("ul");
        Object.keys(errors).forEach(function (name) {
            var field = form.querySelector("#field-" + name);
            if (!field) {
                return;
            }
            var box = fieldBox(name);
            var error = document.createElement("p");
            error.className = "field-error";
            error.id = "field-" + name + "-error";
            error.textContent = errors[name];
            box.setAttribute("data-invalid", "1");
            box.querySelector("label").insertAdjacentElement("afterend", error);
            var input = box.querySelector("input, select, textarea");
            input.setAttribute("aria-invalid", "true");
            input.setAttribute("aria-describedby", ((input.getAttribute("aria-describedby") || "") + " " + error.id).trim());
            var item = document.createElement("li");
            var link = document.createElement("a");
            link.href = "#field-" + name;
            link.textContent = errors[name];
            item.appendChild(link);
            list.appendChild(item);
        });
        var heading = document.createElement("p");
        heading.className = "error-title";
        heading.textContent = title;
        summary.appendChild(heading);
        if (list.children.length) {
            summary.appendChild(list);
        }
        summary.hidden = false;
        summary.focus();
    }

    function localErrors() {
        var errors = {};
        var name = form.elements.name.value.trim();
        if (name.length < 2 || name.length > 120) {
            errors.name = messages.name;
        }
        var email = form.elements.email.value.trim();
        if (!/^[^\s@,]+@[^\s@,]+\.[^\s@,]+$/.test(email) || email.length > 254) {
            errors.email = messages.email;
        }
        if (!form.elements.enquiry_type.value) {
            errors.enquiry_type = messages.enquiry_type;
        }
        return errors;
    }

    function setPending(on) {
        pending = on;
        submit.disabled = on;
        submit.textContent = on ? text.pending : idleLabel;
        status.textContent = on ? text.pending : "";
    }

    function received(answer) {
        var id = form.elements.submission_id.value;
        if (!reported[id] && Array.isArray(window.dataLayer)) {
            // Enum and page only: never a name, address or the message text.
            window.dataLayer.push({
                event: "enquiry_submitted",
                enquiry_type: form.elements.enquiry_type.value,
                source_path: form.elements.source_path.value,
                duplicate: answer.status === "duplicate",
            });
        }
        reported[id] = true;
        form.hidden = true;
        if (aside) {
            aside.hidden = true;
        }
        success.hidden = false;
        success.focus();
    }

    var booking = success.querySelector("[data-spk-booking]");
    if (booking) {
        booking.addEventListener("click", function () {
            if (Array.isArray(window.dataLayer)) {
                window.dataLayer.push({event: "booking_link_opened", link: "booking"});
            }
        });
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        if (pending) {
            return;
        }
        clearErrors();
        var errors = localErrors();
        if (Object.keys(errors).length) {
            showErrors(text.check, errors);
            return;
        }
        if (preview) {
            showErrors(formMessages.preview, {});
            return;
        }
        setPending(true);
        var controller = window.AbortController ? new AbortController() : null;
        var timer = controller ? window.setTimeout(function () { controller.abort(); }, 20000) : null;
        window.fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: {Accept: "application/json"},
            credentials: "same-origin",
            signal: controller ? controller.signal : undefined,
        }).then(function (response) {
            return response.json().catch(function () {
                return {ok: false, error: "send"};
            });
        }).then(function (answer) {
            window.clearTimeout(timer);
            setPending(false);
            if (answer.ok) {
                received(answer);
                return;
            }
            if (answer.error === "invalid" && answer.fields) {
                var fields = answer.fields;
                var title = fields.form || text.check;
                delete fields.form;
                showErrors(title, fields);
                return;
            }
            showErrors(formMessages[answer.error] || sendError, {});
        }).catch(function () {
            window.clearTimeout(timer);
            setPending(false);
            showErrors(sendError, {});
        });
    });
})();
