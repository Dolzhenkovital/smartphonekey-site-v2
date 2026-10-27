/** @odoo-module ignore **/
/* SmartphoneKey website 2.0: the setup guide, on the home page and /find-your-setup.
 *
 * Evaluates the same rules the server uses (serialised into
 * #spk-setup-rules by setup_guide.rules_for_script) so the result appears in
 * place. Without this script the forms submit as GET and the server renders
 * the same result. Only enum choices ever reach the URL or analytics; nothing
 * is sent anywhere and nothing is stored in the browser.
 */
(function () {
    "use strict";

    var source = document.getElementById("spk-setup-rules");
    if (!source) {
        return;
    }
    var data = JSON.parse(source.textContent);

    function track(event, detail) {
        // Analytics only receives enum values, and only if a consented loader set dataLayer up.
        if (Array.isArray(window.dataLayer)) {
            window.dataLayer.push(Object.assign({event: event}, detail));
        }
    }

    // --- Home: two choices, frozen copy ------------------------------------
    var home = document.querySelector("[data-spk-home-setup]");
    if (home) {
        var output = home.querySelector("output");
        var update = function () {
            var site = home.elements.site.value;
            var connection = home.elements.connection.value;
            output.textContent = data.home.connection[connection] + " " + data.home.site[site];
        };
        home.addEventListener("change", update);
        update();
    }

    // --- The full guide ----------------------------------------------------
    var form = document.querySelector("[data-spk-setup-guide]");
    if (!form) {
        return;
    }
    var result = document.querySelector("[data-spk-setup-result]");
    // The server renders both states: the empty message (with its own contact link) and the body, one of them hidden.
    var empty = result.querySelector("[data-spk-result-empty]");
    var body = result.querySelector("[data-spk-result-body]");
    var summary = result.querySelector("[data-spk-result-summary]");
    var advice = result.querySelector("[data-spk-result-advice]");
    var items = result.querySelector("[data-spk-result-items]");
    var links = result.querySelector("[data-spk-result-links]");
    var contact = result.querySelector("[data-spk-result-contact]");
    var reset = form.querySelector("[data-spk-setup-reset]");
    var single = ["role", "sites", "doors", "connection"];

    function selection() {
        var chosen = {};
        single.forEach(function (name) {
            var input = form.querySelector("input[name='" + name + "']:checked");
            if (input) {
                chosen[name] = input.value;
            }
        });
        var interests = Array.prototype.map.call(form.querySelectorAll("input[name='interests']:checked"), function (input) {
            return input.value;
        });
        if (interests.length) {
            chosen.interests = interests;
        }
        return chosen;
    }

    function matches(rule, chosen) {
        return Object.keys(rule.when).every(function (field) {
            var values = rule.when[field];
            if (field === "interests") {
                return (chosen.interests || []).some(function (key) { return values.indexOf(key) !== -1; });
            }
            return values.indexOf(chosen[field]) !== -1;
        });
    }

    function query(chosen, withInterest) {
        var params = new URLSearchParams();
        if (withInterest) {
            params.append("interest", "project");
        }
        single.forEach(function (name) {
            if (chosen[name]) {
                params.append(name, chosen[name]);
            }
        });
        (chosen.interests || []).forEach(function (key) { params.append("interests", key); });
        return params.toString();
    }

    function fill(list, entries, render) {
        list.textContent = "";
        entries.forEach(function (entry) {
            var li = document.createElement("li");
            render(li, entry);
            list.appendChild(li);
        });
    }

    function contactHref(chosen) {
        // Keep the link's own origin and base path (the static preview lives in a subfolder).
        var url = new URL(contact.getAttribute("href"), window.location.href);
        url.search = query(chosen, true);
        return url.pathname + url.search;
    }

    function show(chosen) {
        empty.hidden = !!chosen.connection;
        body.hidden = !chosen.connection;
        if (!chosen.connection) {
            return false;
        }
        var texts = [];
        var seen = {};
        var related = [];
        data.rules.forEach(function (rule) {
            if (matches(rule, chosen)) {
                texts.push(rule.item);
                rule.links.forEach(function (key) {
                    if (!seen[key]) {
                        seen[key] = true;
                        related.push(data.links[key]);
                    }
                });
            }
        });
        // The summary: one chip per answer, in the order of the form.
        var answers = Array.prototype.map.call(form.querySelectorAll("input:checked"), function (input) {
            return input.nextElementSibling ? input.nextElementSibling.textContent.trim() : "";
        }).filter(Boolean);
        fill(summary, answers, function (li, text) {
            li.className = "chip";
            li.textContent = text;
        });
        advice.textContent = data.advice[chosen.connection];
        fill(items, texts, function (li, text) { li.textContent = text; });
        fill(links, related, function (li, link) {
            var anchor = document.createElement("a");
            anchor.textContent = link[0];
            anchor.href = link[1];
            li.appendChild(anchor);
        });
        contact.setAttribute("href", contactHref(chosen));
        return true;
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        var chosen = selection();
        var shown = show(chosen);
        var params = query(chosen, false);
        window.history.replaceState(null, "", window.location.pathname + (params ? "?" + params : ""));
        result.focus();
        if (shown) {
            track("setup_completed", {
                role: chosen.role || "",
                sites: chosen.sites || "",
                doors: chosen.doors || "",
                connection: chosen.connection,
                interests: (chosen.interests || []).join(","),
            });
        }
    });

    // "Change answers" (a link to the form) puts the focus on the first answer already given.
    result.querySelectorAll("a[href='#guide-form-title']").forEach(function (link) {
        link.addEventListener("click", function () {
            var first = form.querySelector("input:checked") || form.querySelector("input");
            if (first) {
                window.setTimeout(function () { first.focus(); }, 0);
            }
        });
    });

    reset.addEventListener("click", function (event) {
        event.preventDefault();
        form.reset();
        form.querySelectorAll("input").forEach(function (input) { input.checked = false; });
        show({});
        contact.setAttribute("href", contactHref({}));
        window.history.replaceState(null, "", window.location.pathname);
        form.querySelector("input").focus();
    });
})();
