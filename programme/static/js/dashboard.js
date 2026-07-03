/* Tableau de bord EMSP — graphiques selectionnables (Chart.js, hors-ligne). */
(function () {
  "use strict";
  var BLEU = "#1F4E79";
  var PALETTE = ["#1F4E79", "#3A7CB8", "#6FA8D6", "#2E7D32", "#C0392B",
                 "#E08E0B", "#7E57C2", "#00897B", "#5D6D7E", "#AF601A"];

  var DEMO = {
    kpis: { etudiants: 554, actifs: 512, diplomes: 28, taux_presence: 86.4,
            recettes: 18750000, depenses: 14320000, solde: 4430000, heures: 1860, enseignants: 41, reste_du: 5260000 },
    graphiques: {
      filieres: { labels: ["Soins infirmiers", "Soins obstetricaux", "Aides soignants", "Sage-femme", "Laboratoire"],
                  valeurs: [188, 142, 96, 84, 44] },
      statuts: { labels: ["Actif", "Diplome", "Abandonne", "Radie"], valeurs: [512, 28, 9, 5] },
      finances: { labels: ["Inscriptions", "Scolarite", "Examens", "Partenaires", "Locations"],
                  series: [
                    { nom: "Recettes", valeurs: [6200000, 7400000, 1850000, 2900000, 400000] },
                    { nom: "Depenses", valeurs: [0, 9100000, 1200000, 3600000, 420000] }
                  ] },
      presence: { labels: ["10h", "12h", "15h", "17h"], valeurs: [91, 88, 84, 79] },
      heures: { labels: ["E-001", "E-014", "E-022", "E-031", "E-040"], valeurs: [420, 360, 295, 410, 375] },
      reste_du_filiere: { labels: ["Soins infirmiers", "Soins obstetricaux", "Aides soignants", "Sage-femme", "Laboratoire"],
                  valeurs: [2100000, 1450000, 900000, 540000, 270000] }
    }
  };

  var STATE = {}; // par chart : {type, data, hidden:Set, chart}

  function fmt(n) {
    if (typeof n !== "number") return n;
    return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  }

  function normalise(id, g) {
    // -> {labels, datasets:[{label,data}]}
    if (!g) return { labels: [], datasets: [] };
    if (g.series) {
      return { labels: g.labels, datasets: g.series.map(function (s) { return { label: s.nom, data: s.valeurs }; }) };
    }
    var titre = (window.CHART_DEFS.find(function (c) { return c.id === id; }) || {}).titre || id;
    return { labels: g.labels, datasets: [{ label: titre, data: g.valeurs }] };
  }

  function couleurs(n, alpha) {
    var out = [];
    for (var i = 0; i < n; i++) {
      var c = PALETTE[i % PALETTE.length];
      out.push(alpha ? hexA(c, alpha) : c);
    }
    return out;
  }
  function hexA(hex, a) {
    var r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
    return "rgba(" + r + "," + g + "," + b + "," + a + ")";
  }

  function construitChips(id) {
    var st = STATE[id];
    var box = document.getElementById("chips_" + id);
    box.innerHTML = "";
    st.data.labels.forEach(function (lab, i) {
      var on = !st.hidden.has(i);
      var chip = document.createElement("label");
      chip.className = "chip" + (on ? "" : " off");
      chip.innerHTML = '<input type="checkbox" ' + (on ? "checked" : "") + '> ' +
        '<span style="width:9px;height:9px;border-radius:50%;display:inline-block;background:' + PALETTE[i % PALETTE.length] + '"></span>' +
        '<span>' + lab + "</span>";
      chip.querySelector("input").addEventListener("change", function (e) {
        if (e.target.checked) st.hidden.delete(i); else st.hidden.add(i);
        chip.classList.toggle("off", !e.target.checked);
        dessine(id);
      });
      box.appendChild(chip);
    });
  }

  function donneesFiltrees(id) {
    var st = STATE[id];
    var labels = [], idx = [];
    st.data.labels.forEach(function (l, i) { if (!st.hidden.has(i)) { labels.push(l); idx.push(i); } });
    var ds = st.data.datasets.map(function (d) {
      return { label: d.label, data: idx.map(function (i) { return d.data[i]; }) };
    });
    return { labels: labels, datasets: ds };
  }

  function dessine(id) {
    var st = STATE[id];
    var f = donneesFiltrees(id);
    var type = st.type;
    var datasets;
    if (type === "pie") {
      var d0 = f.datasets[0] || { data: [] };
      datasets = [{ data: d0.data, backgroundColor: couleurs(f.labels.length, 0.85), borderColor: "#fff", borderWidth: 2 }];
    } else if (type === "radar") {
      datasets = f.datasets.map(function (d, k) {
        var c = PALETTE[k % PALETTE.length];
        return { label: d.label, data: d.data, borderColor: c, backgroundColor: hexA(c, 0.18), pointBackgroundColor: c };
      });
    } else { // bar
      datasets = f.datasets.map(function (d, k) {
        return { label: d.label, data: d.data,
                 backgroundColor: f.datasets.length > 1 ? hexA(PALETTE[k % PALETTE.length], 0.85) : couleurs(f.labels.length, 0.85),
                 borderRadius: 5, borderSkipped: false };
      });
    }
    var opts = {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: (type === "pie") || f.datasets.length > 1, position: "bottom",
                  labels: { font: { family: "Calibri", size: 13 } } },
        tooltip: { callbacks: { label: function (ctx) {
          var v = (type === "pie") ? ctx.parsed : ctx.parsed.y;
          if (v === undefined || v === null) v = ctx.parsed;
          return (ctx.dataset.label ? ctx.dataset.label + " : " : "") + fmt(v);
        } } }
      },
      scales: (type === "pie") ? {} :
              (type === "radar") ? { r: { ticks: { font: { family: "Calibri" } } } } :
              { x: { ticks: { font: { family: "Calibri" } } }, y: { beginAtZero: true, ticks: { font: { family: "Calibri" } } } }
    };
    if (st.chart) st.chart.destroy();
    st.chart = new Chart(document.getElementById("cv_" + id), { type: type, data: { labels: f.labels, datasets: datasets }, options: opts });
  }

  function chargeKpis(k) {
    document.querySelectorAll("#kpis .v[data-k]").forEach(function (el) {
      var key = el.getAttribute("data-k");
      var v = k[key];
      el.textContent = (key === "taux_presence") ? v : fmt(v);
    });
  }

  function applique(payload) {
    chargeKpis(payload.kpis);
    window.CHART_DEFS.forEach(function (c) {
      STATE[c.id] = STATE[c.id] || { type: c.defaut, hidden: new Set() };
      STATE[c.id].data = normalise(c.id, payload.graphiques[c.id]);
      // garder les indices encore valides
      var max = STATE[c.id].data.labels.length;
      STATE[c.id].hidden = new Set(Array.from(STATE[c.id].hidden).filter(function (i) { return i < max; }));
      construitChips(c.id);
      dessine(c.id);
    });
  }

  function brancheControles() {
    document.querySelectorAll(".chart-card").forEach(function (card) {
      var id = card.getAttribute("data-chart");
      card.querySelectorAll(".types button").forEach(function (b) {
        b.addEventListener("click", function () {
          card.querySelectorAll(".types button").forEach(function (x) { x.classList.remove("on"); });
          b.classList.add("on");
          STATE[id].type = b.getAttribute("data-type");
          dessine(id);
        });
      });
      card.querySelectorAll(".stitle a[data-all]").forEach(function (a) {
        a.addEventListener("click", function () {
          var tout = a.getAttribute("data-all") === "1";
          STATE[id].hidden = new Set();
          if (!tout) STATE[id].data.labels.forEach(function (_, i) { STATE[id].hidden.add(i); });
          construitChips(id);
          dessine(id);
        });
      });
    });
    document.getElementById("demo").addEventListener("change", function (e) {
      if (e.target.checked) applique(DEMO); else charge();
    });
  }

  function charge() {
    fetch(window.API_URL).then(function (r) { return r.json(); })
      .then(function (d) {
        var vide = d.kpis.etudiants === 0 && d.kpis.recettes === 0;
        applique(d);
        if (vide) {
          // bascule auto en demo pour visualiser, en cochant le bouton
          var dm = document.getElementById("demo");
          if (dm && !dm.checked) { dm.checked = true; applique(DEMO); }
        }
      })
      .catch(function () { applique(DEMO); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    brancheControles();
    charge();
  });
})();
