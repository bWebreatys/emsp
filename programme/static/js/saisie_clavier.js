/* EMSP — Ergonomie de saisie clavier (V1.99.4)
 * 100% hors-ligne, sans dependance, charte respectee.
 *
 * Lot A — TOUCHE UNIQUE sur les champs liste courts a valeurs fixes :
 *   <select data-saisie="touche"> (rendu par module.html, classe par
 *   metier.champs_saisie). Une frappe = un choix, insensible casse/accents :
 *     - 1 seul libelle commence par la touche -> selectionne + focus au champ suivant.
 *     - plusieurs libelles partagent l'initiale (collision) -> CYCLE entre eux a
 *       chaque frappe, sans avancer le focus tant que l'ambiguite n'est pas levee.
 *   Exemple : R -> Recette (+focus suivant) ; D -> Depense.
 *
 * Lot B — AUTOCOMPLETE "code - intitule" sur les referentiels longs :
 *   <select data-saisie="auto">. Au chargement, le <select> natif est masque et
 *   remplace par un champ texte + une liste flottante filtrable :
 *     - filtre sur le code OU l'intitule (insensible casse/accents) ; "commence par"
 *       en tete, puis "contient".
 *     - navigation fleches haut/bas ; Entree/Tab valide + focus au champ suivant ;
 *       Echap ferme ; clic valide.
 *     - seul le CODE (option.value) est enregistre ; le <select> natif pilote la
 *       valeur postee, donc valide_saisie et l'ecriture Excel sont inchanges.
 *   FILET DE SECURITE : sans JS, le <select> natif reste visible et fonctionnel.
 *   Le panneau flottant est attache au body (echappe a l'overflow de .saisie-grid).
 *
 * Le script est inerte si aucun champ data-saisie n'est present.
 */
(function () {
  "use strict";

  // Minuscule sans accents, pour comparer les initiales (e accent = e).
  function norm(s) {
    return (s == null ? "" : String(s))
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  }

  // Controles reellement atteignables au clavier dans un formulaire (ordre DOM),
  // hors champs caches/desactives/masques. Sert a deplacer le focus.
  function focusables(form) {
    return Array.prototype.filter.call(
      form.querySelectorAll("input, select, textarea, button"),
      function (el) {
        return !el.disabled && el.type !== "hidden" && el.offsetParent !== null;
      }
    );
  }

  function focusSuivant(el) {
    var form = el.form || el.closest("form");
    if (!form) return;
    var f = focusables(form);
    var i = f.indexOf(el);
    if (i >= 0 && i + 1 < f.length) {
      var n = f[i + 1];
      n.focus();
      if (typeof n.select === "function") { try { n.select(); } catch (e) {} }
    }
  }

  function onKey(e) {
    // Laisser passer les combinaisons et les touches de navigation/edition
    // (Tab, Entree, fleches, Echap, Suppr... ont une longueur de cle > 1).
    if (e.ctrlKey || e.altKey || e.metaKey) return;
    if (!e.key || e.key.length !== 1) return;
    var k = norm(e.key);
    if (!k.trim()) return; // espace ignore

    var sel = e.currentTarget;
    var opts = Array.prototype.filter.call(sel.options, function (o) {
      return o.value !== "";
    });
    var matchs = opts.filter(function (o) {
      return norm(o.textContent).charAt(0) === k;
    });

    // On prend la main sur le comportement natif pour rester deterministe.
    e.preventDefault();
    if (matchs.length === 0) return;

    if (matchs.length === 1) {
      sel.value = matchs[0].value;
      sel.dispatchEvent(new Event("change", { bubbles: true }));
      focusSuivant(sel);
      return;
    }

    // Collision : cycle parmi les libelles de meme initiale, focus inchange.
    var cur = sel.value, idx = -1;
    for (var j = 0; j < matchs.length; j++) {
      if (matchs[j].value === cur) { idx = j; break; }
    }
    var suivant = matchs[(idx + 1) % matchs.length];
    sel.value = suivant.value;
    sel.dispatchEvent(new Event("change", { bubbles: true }));
  }

  // ------------------------------------------------------------------
  // Lot B — autocomplete "code - intitule" sur select[data-saisie="auto"]
  // ------------------------------------------------------------------

  var STYLE_B =
    ".emsp-ac-wrap{position:relative;display:inline-block}" +
    ".emsp-ac-pane{position:absolute;z-index:1000;max-height:248px;overflow-y:auto;" +
      "background:#fff;border:1px solid var(--bord,#cbd5e1);border-radius:8px;" +
      "box-shadow:0 6px 18px rgba(31,78,121,.16)}" +
    ".emsp-ac-pane[hidden]{display:none}" +
    ".emsp-ac-item{display:flex;gap:10px;padding:7px 10px;cursor:pointer;white-space:nowrap}" +
    ".emsp-ac-item+.emsp-ac-item{border-top:1px solid #eef2f7}" +
    ".emsp-ac-code{font-family:Consolas,'Courier New',monospace;font-size:13px;" +
      "color:#1F4E79;min-width:46px}" +
    ".emsp-ac-lib{font-size:14px;color:#1f2937}" +
    ".emsp-ac-item.active{background:#1F4E79}" +
    ".emsp-ac-item.active .emsp-ac-code,.emsp-ac-item.active .emsp-ac-lib{color:#fff}" +
    ".emsp-ac-empty{padding:8px 10px;color:#6b7280;font-size:13px}";

  function injectStyleB() {
    if (document.getElementById("emsp-ac-style")) return;
    var s = document.createElement("style");
    s.id = "emsp-ac-style";
    s.textContent = STYLE_B;
    document.head.appendChild(s);
  }

  // "6061 - Achats..." -> {code:"6061", lib:"Achats..."} ; sinon {code:"", lib:label}.
  // Separateur : tiret simple OU cadratin entoure d'espaces (cf. LISTES_ONGLET_VALLABEL).
  function splitCodeLib(label) {
    var parts = String(label).split(/\s+[\u2014-]\s+/);
    if (parts.length >= 2) return { code: parts[0], lib: parts.slice(1).join(" \u2014 ") };
    return { code: "", lib: String(label) };
  }

  function makeAuto(sel) {
    if (sel.__saisieAuto) return;
    sel.__saisieAuto = true;
    injectStyleB();

    var options = Array.prototype.filter.call(sel.options, function (o) {
      return o.value !== "";
    }).map(function (o) {
      return { value: o.value, label: (o.textContent || "").trim() };
    });

    var wrap = document.createElement("span");
    wrap.className = "emsp-ac-wrap";
    var input = document.createElement("input");
    input.type = "text";
    input.autocomplete = "off";
    input.setAttribute("role", "combobox");
    input.setAttribute("aria-autocomplete", "list");
    input.setAttribute("aria-label", "Recherche par code ou intitule");
    wrap.appendChild(input);
    sel.style.display = "none";
    sel.parentNode.insertBefore(wrap, sel.nextSibling);

    var pane = document.createElement("div");
    pane.className = "emsp-ac-pane";
    pane.hidden = true;
    document.body.appendChild(pane);

    var filtered = [], active = -1, open = false;

    function resync() {
      var cur = sel.value, hit = null;
      for (var i = 0; i < options.length; i++) {
        if (options[i].value === cur) { hit = options[i]; break; }
      }
      input.value = hit ? hit.label : "";
    }
    resync();

    function place() {
      var r = input.getBoundingClientRect();
      pane.style.left = (r.left + window.scrollX) + "px";
      pane.style.top = (r.bottom + window.scrollY + 4) + "px";
      pane.style.minWidth = r.width + "px";
    }

    function render() {
      pane.innerHTML = "";
      if (filtered.length === 0) {
        var e = document.createElement("div");
        e.className = "emsp-ac-empty";
        e.textContent = "Aucune correspondance";
        pane.appendChild(e);
        return;
      }
      filtered.forEach(function (o, i) {
        var cl = splitCodeLib(o.label);
        var it = document.createElement("div");
        it.className = "emsp-ac-item" + (i === active ? " active" : "");
        if (cl.code) {
          var c = document.createElement("span");
          c.className = "emsp-ac-code";
          c.textContent = cl.code;
          it.appendChild(c);
        }
        var l = document.createElement("span");
        l.className = "emsp-ac-lib";
        l.textContent = cl.lib;
        it.appendChild(l);
        // mousedown (avant blur) pour valider sans perdre le clic.
        it.addEventListener("mousedown", function (ev) {
          ev.preventDefault();
          choisir(o);
          focusSuivant(input);
        });
        pane.appendChild(it);
      });
      var act = pane.querySelector(".emsp-ac-item.active");
      if (act && act.scrollIntoView) act.scrollIntoView({ block: "nearest" });
    }

    function filtre() {
      var q = norm(input.value);
      if (!q) {
        filtered = options.slice(0, 50);
      } else {
        var deb = [], ct = [];
        options.forEach(function (o) {
          var p = norm(o.label).indexOf(q);
          if (p === 0) deb.push(o); else if (p > 0) ct.push(o);
        });
        filtered = deb.concat(ct).slice(0, 50);
      }
      active = filtered.length ? 0 : -1;
    }

    function ouvrir() {
      open = true; pane.hidden = false; place(); render();
      window.addEventListener("scroll", place, true);
      window.addEventListener("resize", place);
    }
    function fermer() {
      open = false; pane.hidden = true;
      window.removeEventListener("scroll", place, true);
      window.removeEventListener("resize", place);
      // Texte vide -> champ remis a "non renseigne" ; sinon resync (pas de fantome).
      if (input.value.trim() === "") {
        if (sel.value !== "") { sel.value = ""; sel.dispatchEvent(new Event("change", { bubbles: true })); }
      } else {
        resync();
      }
    }
    function choisir(o) {
      sel.value = o.value;
      sel.dispatchEvent(new Event("change", { bubbles: true }));
      input.value = o.label;
      fermer();
    }

    input.addEventListener("focus", function () { filtre(); ouvrir(); });
    input.addEventListener("input", function () {
      filtre();
      if (!open) ouvrir(); else { place(); render(); }
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        if (!open) { filtre(); ouvrir(); }
        else { active = Math.min(active + 1, filtered.length - 1); render(); }
        e.preventDefault();
      } else if (e.key === "ArrowUp") {
        if (open) { active = Math.max(active - 1, 0); render(); }
        e.preventDefault();
      } else if (e.key === "Enter") {
        if (open && active >= 0) { choisir(filtered[active]); focusSuivant(input); }
        e.preventDefault();
      } else if (e.key === "Tab") {
        if (open && active >= 0) choisir(filtered[active]); // laisse Tab avancer le focus
      } else if (e.key === "Escape") {
        if (open) { fermer(); e.preventDefault(); }
      }
    });
    input.addEventListener("blur", function () {
      setTimeout(function () { if (open) fermer(); }, 120);
    });
  }

  function init() {
    var sels = document.querySelectorAll('select[data-saisie="touche"]');
    Array.prototype.forEach.call(sels, function (sel) {
      if (sel.__saisieTouche) return; // idempotent (re-init sans doublon)
      sel.__saisieTouche = true;
      sel.addEventListener("keydown", onKey);
    });
    var autos = document.querySelectorAll('select[data-saisie="auto"]');
    Array.prototype.forEach.call(autos, makeAuto);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
  // Expose une re-initialisation pour les formulaires regeneres dynamiquement.
  window.EMSP_saisieClavierInit = init;
})();
