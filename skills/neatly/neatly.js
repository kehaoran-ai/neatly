/* ==========================================================================
   Neatly · neatly.js  (optional, ~4 KB, no dependencies)
   Lives in a <script> in <head>; it waits for the page to load. It handles:
     - charts:    <svg class="nt-chart" data-chart="line|bars" data-series='[[..],[..]]' data-labels='[..]'>
                  <svg class="nt-spark" data-spark='[..]'>
     - copy:      <button class="nt-copy" data-copy="#id-of-pre">Copy</button>
     - contents:  <nav data-toc> with links to #section ids; the current one gets aria-current
     - switches:  <div class="nt-seg"><button aria-pressed="true">..</button>..</div>
     - slides:    body.nt-deck with section.nt-slide children
     - try a colour:  open the page with ?accent=ff5a1f
   https://github.com/kehaoran-ai/neatly · MIT
   ========================================================================== */
(function () {
  var NS = "http://www.w3.org/2000/svg";
  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function parse(v, fallback) { try { return JSON.parse(v); } catch (e) { return fallback; } }
  function fmt(v) { return v >= 1000 ? (v / 1000).toFixed(v >= 10000 ? 0 : 1).replace(/\.0$/, "") + "k" : String(v); }

  /* ---- try a colour: ?accent=ff5a1f ---- */
  var a = new URLSearchParams(location.search).get("accent");
  if (a && /^[0-9a-f]{3,8}$/i.test(a)) document.documentElement.style.setProperty("--nt-accent", "#" + a);

  function init() {
    /* ---- line / area / bars ----
       Drawn at the element's real pixel width so labels stay 11px; redrawn on resize. */
    function niceStep(raw) {
      var p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p;
      return (m <= 1.2 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p;
    }
    function draw(svg) {
      var kind = svg.dataset.chart || "line";
      var series = parse(svg.dataset.series, []);
      if (!series.length) return;
      if (typeof series[0] === "number") series = [series];
      var labels = parse(svg.dataset.labels, []);
      var unit = svg.dataset.unit || "";
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var W = Math.max(280, Math.round(svg.clientWidth || svg.getBoundingClientRect().width || 640));
      var H = +(svg.dataset.height || 240), L = 40, R = 12, T = 12, B = labels.length ? 28 : 8;
      // On a slide, never run past the bottom of the slide body.
      var body = svg.closest(".nt-slide-body");
      if (body && body.offsetParent) {
        var sc = body.getBoundingClientRect().height / body.offsetHeight || 1;
        var room = (body.getBoundingClientRect().bottom - svg.getBoundingClientRect().top) / sc - 8;
        if (room > 120) H = Math.min(H, Math.floor(room));
      }
      svg.setAttribute("viewBox", "0 0 " + W + " " + H);
      svg.setAttribute("height", H);
      svg.setAttribute("role", "img");
      var all = [].concat.apply([], series), mx = Math.max.apply(null, all);
      var stepV = niceStep(mx / 4 || 1), top = stepV * Math.ceil(mx * 1.04 / stepV);
      var n = series[0].length, iw = W - L - R, ih = H - T - B;
      var x = function (i) { return kind === "bars" ? L + iw * (i + 0.5) / n : L + (n === 1 ? iw / 2 : iw * i / (n - 1)); };
      var y = function (v) { return T + ih - ih * v / top; };
      for (var gv = 0; gv <= top + 1e-9; gv += stepV) {
        var gy = y(gv);
        el("line", { x1: L, x2: W - R, y1: gy, y2: gy, class: "axis" }, svg);
        el("text", { x: L - 10, y: gy + 4, "text-anchor": "end", class: "tick" }, svg).textContent = fmt(+gv.toFixed(2)) + unit;
      }
      // Empty strings in data-labels mean "no label here": the author already chose which to show.
      var maxLabels = Math.max(2, Math.floor(iw / 70)), named = labels.filter(Boolean).length;
      var step = named < labels.length && named <= maxLabels ? 1 : Math.ceil(labels.length / maxLabels);
      labels.forEach(function (lb, i) {
        if (!lb || (i % step && i !== labels.length - 1)) return;
        var anchor = kind === "bars" ? "middle" : i === 0 ? "start" : i === labels.length - 1 ? "end" : "middle";
        el("text", { x: x(i), y: H - 8, "text-anchor": anchor, class: "tick" }, svg).textContent = lb;
      });
      var hi = +(svg.dataset.accent || 0);
      if (kind === "bars") {
        var bw = Math.min(32, iw / n * 0.58), hl = parse(svg.dataset.highlight, [n - 1]);
        series[0].forEach(function (v, i) {
          el("rect", { x: x(i) - bw / 2, y: y(v), width: bw, height: Math.max(1, y(0) - y(v)), rx: 3, class: "bar" + (hl.indexOf(i) > -1 ? " is-accent" : "") }, svg);
        });
        return;
      }
      var s = series[hi];
      var d = s.map(function (v, i) { return (i ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1); }).join(" ");
      if (svg.dataset.area !== "false") el("path", { d: d + " L" + x(n - 1) + " " + y(0) + " L" + x(0) + " " + y(0) + " Z", class: "area" }, svg);
      series.forEach(function (o, si) {
        if (si === hi) return;
        el("path", { d: o.map(function (v, i) { return (i ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1); }).join(" "), class: "series is-faint" }, svg);
      });
      el("path", { d: d, class: "series is-accent" }, svg);
      el("circle", { cx: x(n - 1), cy: y(s[n - 1]), r: 4, class: "dot" }, svg);
    }
    var charts = [].slice.call(document.querySelectorAll("svg.nt-chart"));
    charts.forEach(draw);
    var rt;
    window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { charts.forEach(draw); }, 120); });

    /* ---- sparkline ---- */
    document.querySelectorAll("svg.nt-spark").forEach(function (svg) {
      var s = parse(svg.dataset.spark, []);
      if (s.length < 2) return;
      var W = 120, H = 28, mn = Math.min.apply(null, s), mx = Math.max.apply(null, s), r = mx - mn || 1;
      svg.setAttribute("viewBox", "0 0 " + W + " " + H);
      svg.setAttribute("preserveAspectRatio", "none");
      var d = s.map(function (v, i) { return (i ? "L" : "M") + (W * i / (s.length - 1)).toFixed(1) + " " + (H - 2 - (H - 4) * (v - mn) / r).toFixed(1); }).join(" ");
      if (svg.classList.contains("is-accent")) el("path", { d: d + " L" + W + " " + H + " L0 " + H + " Z", class: "area" }, svg);
      el("path", { d: d, class: "series" + (svg.classList.contains("is-accent") ? " is-accent" : "") }, svg);
    });

    /* ---- deck: arrows / space / click to move, #3 deep links, scales to fit ---- */
    var deck = document.querySelector(".nt-deck");
    if (deck) {
      var slides = [].slice.call(deck.querySelectorAll(".nt-slide")), cur = 0;
      var bar = document.createElement("div"); bar.className = "nt-progress nt-noprint"; document.body.appendChild(bar);
      function fit() { var de = document.documentElement, sc = Math.min(de.clientWidth / 1360, de.clientHeight / 780); document.documentElement.style.setProperty("--nt-scale", Math.min(sc, 1.6).toFixed(3)); }
      function go(i) {
        cur = Math.max(0, Math.min(slides.length - 1, i));
        slides.forEach(function (s, k) { s.classList.toggle("is-active", k === cur); });
        bar.style.width = (100 * (cur + 1) / slides.length) + "%";
        slides[cur].querySelectorAll("svg.nt-chart").forEach(draw);
        history.replaceState(null, "", "#" + (cur + 1));
      }
      slides.forEach(function (s, k) {
        var n = s.querySelector(".nt-slide-foot .nt-num");
        if (n) n.textContent = String(k + 1).padStart(2, "0") + " / " + String(slides.length).padStart(2, "0");
      });
      addEventListener("keydown", function (e) {
        if (["ArrowRight", "PageDown", " ", "Enter"].indexOf(e.key) > -1) { e.preventDefault(); go(cur + 1); }
        else if (["ArrowLeft", "PageUp", "Backspace"].indexOf(e.key) > -1) { e.preventDefault(); go(cur - 1); }
        else if (e.key === "Home") go(0);
        else if (e.key === "End") go(slides.length - 1);
      });
      deck.addEventListener("click", function (e) { if (e.target.closest("a, button")) return; go(cur + (e.clientX > innerWidth / 3 ? 1 : -1)); });
      addEventListener("resize", fit);
      fit(); go((parseInt(location.hash.slice(1), 10) || 1) - 1);
    }

    /* ---- copy buttons ---- */
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest(".nt-copy");
      if (!b) return;
      var src = document.querySelector(b.dataset.copy);
      if (!src) return;
      navigator.clipboard && navigator.clipboard.writeText(src.innerText.replace(/^\$ /gm, "")).then(function () {
        var t = b.textContent; b.textContent = "Copied"; setTimeout(function () { b.textContent = t; }, 1400);
      });
    });

    /* ---- segmented control: one pressed button per group ---- */
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest(".nt-seg button");
      if (!b) return;
      b.parentNode.querySelectorAll("button").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
    });

    /* ---- contents: highlight the last section whose heading has passed the top third ---- */
    var toc = document.querySelector("[data-toc]");
    if (toc) {
      var items = [].slice.call(toc.querySelectorAll('a[href^="#"]')).map(function (l) {
        return { link: l, target: document.getElementById(l.getAttribute("href").slice(1)) };
      }).filter(function (it) { return it.target; });
      var ticking = false;
      function mark() {
        ticking = false;
        var line = innerHeight * 0.3, cur = items[0];
        items.forEach(function (it) { if (it.target.getBoundingClientRect().top <= line) cur = it; });
        if (innerHeight + scrollY >= document.documentElement.scrollHeight - 4) cur = items[items.length - 1];
        items.forEach(function (it) { if (it === cur) it.link.setAttribute("aria-current", "true"); else it.link.removeAttribute("aria-current"); });
      }
      if (items.length) {
        addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(mark); } }, { passive: true });
        mark();
      }
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
