/* ============================================================
   AI 论文学习站 · 首页逻辑
   ============================================================ */
(function () {
  "use strict";
  const D = window.PAPERS;
  const papers = D.papers;
  const stats = D.stats;

  const TYPE_CLS = { "每日精读": "ct-daily", "概念精讲": "ct-concept", "论文精选": "ct-pick", "深度精读": "ct-deep" };
  const ORG_COLORS = {
    "Anthropic": "#d97757", "OpenAI": "#10a37f", "DeepMind": "#5b9dff",
    "Meta": "#0a7cff", "Google": "#fbbc05", "MiniMax": "#22d3ee",
    "NVIDIA": "#76b900", "阿里 Qwen": "#e0442e", "学术/AI前沿": "#a78bfa",
    "其他": "#8b9ac4",
  };
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));

  /* ---------------- 状态 ---------------- */
  const state = { q: "", type: "全部", org: "全部", tags: new Set(), view: "grid" };

  /* ---------------- 统计 ---------------- */
  function renderStats() {
    const s = [
      [stats.total, "总文章"],
      [stats.daily, "每日精读"],
      [stats.concept, "概念精讲"],
      [stats.picks, "论文精选"],
      [stats.orgs.length, "机构/来源"],
      [span(stats.first, stats.last), "时间跨度"],
    ];
    document.getElementById("stats").innerHTML = s.map(([n, l]) =>
      `<div class="stat"><div class="n">${esc(n)}</div><div class="l">${esc(l)}</div></div>`).join("");
    document.getElementById("footTotal").textContent = stats.total;
  }
  function span(a, b) {
    if (!a || !b) return "—";
    const s = (x) => x.slice(0, 7).replace("-", ".");
    return s(a) + " ~ " + s(b);
  }

  /* ---------------- 筛选 chips ---------------- */
  function chip(label, key, active, cnt) {
    return `<button class="chip${active ? " on" : ""}" data-key="${esc(key)}">${esc(label)}<span class="cnt">${cnt}</span></button>`;
  }
  function renderChips() {
    const count = (fn) => papers.filter(fn).length;
    const tAll = papers.length;
    const types = ["每日精读", "概念精讲", "论文精选", "深度精读"];
    document.getElementById("typeChips").innerHTML =
      '<span class="clabel">类型</span>' +
      chip("全部", "type|全部", state.type === "全部", tAll) +
      types.map((t) => chip(t, "type|" + t, state.type === t, count((p) => p.type === t))).join("");

    const orgs = stats.orgs.map((o) => [o, count((p) => p.org === o)]).filter(([, c]) => c > 0);
    document.getElementById("orgChips").innerHTML =
      '<span class="clabel">机构</span>' +
      chip("全部", "org|全部", state.org === "全部", tAll) +
      orgs.map(([o, c]) => chip(o, "org|" + o, state.org === o, c)).join("");

    const tagCnt = {};
    papers.forEach((p) => p.tags.forEach((t) => (tagCnt[t] = (tagCnt[t] || 0) + 1)));
    const tags = Object.entries(tagCnt).sort((a, b) => b[1] - a[1]).slice(0, 14);
    document.getElementById("tagChips").innerHTML =
      '<span class="clabel">主题</span>' +
      chip("全部", "tag|__all__", state.tags.size === 0, tAll) +
      tags.map(([t, c]) => chip(t, "tag|" + t, state.tags.has(t), c)).join("");
  }

  /* ---------------- 过滤 ---------------- */
  function filtered() {
    const q = state.q.trim().toLowerCase();
    return papers.filter((p) => {
      if (state.type !== "全部" && p.type !== state.type) return false;
      if (state.org !== "全部" && p.org !== state.org) return false;
      if (state.tags.size && !p.tags.some((t) => state.tags.has(t))) return false;
      if (q) {
        const hay = (p.title + " " + p.summary + " " + p.tags.join(" ") + " " + p.org).toLowerCase();
        if (!q.split(/\s+/).every((w) => hay.includes(w))) return false;
      }
      return true;
    });
  }

  /* ---------------- 卡片 ---------------- */
  function card(p) {
    const c = ORG_COLORS[p.org] || "#8b9ac4";
    return `<article class="card" data-file="${esc(p.file)}" tabindex="0"
      style="--ac:${c}">
      <div class="top">
        <span class="cdate">${esc(p.date)}</span>
        <span class="corg"><i class="odot" style="background:${c};box-shadow:0 0 8px ${c}"></i>${esc(p.org)}</span>
        <span class="ctype ${TYPE_CLS[p.type] || "ct-deep"}">${esc(p.type)}</span>
      </div>
      <h3>${esc(p.title)}</h3>
      <p class="sum">${esc(p.summary || "（本篇暂无摘要，点开阅读全文）")}</p>
      <div class="foot">
        ${p.tags.map((t) => `<span class="tag">#${esc(t)}</span>`).join("")}
        <span class="mins">☕ ${p.minutes} 分钟</span>
        <span class="read">开始精读 →</span>
      </div>
    </article>`;
  }

  function openPaper(p) {
    location.href = "reader.html?f=" + encodeURIComponent(p.file);
  }

  function renderGrid(list) {
    const g = document.getElementById("grid");
    g.innerHTML = list.length
      ? list.map(card).join("")
      : `<div class="empty"><div class="big">🔭</div>没有找到匹配的文章，换个关键词试试？</div>`;
    g.querySelectorAll(".card").forEach((el) => {
      const p = papers.find((x) => x.file === el.dataset.file);
      el.addEventListener("click", () => openPaper(p));
      el.addEventListener("keydown", (e) => { if (e.key === "Enter") openPaper(p); });
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        el.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100) + "%");
        el.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100) + "%");
      });
    });
  }

  /* ---------------- 时间线 ---------------- */
  function renderTL(list) {
    const months = {};
    [...list].sort((a, b) => (a.date < b.date ? 1 : -1)).forEach((p) => {
      const k = p.date.slice(0, 7);
      (months[k] = months[k] || []).push(p);
    });
    const MO = ["", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"];
    document.getElementById("timeline").innerHTML = Object.entries(months).map(([k, arr]) => {
      const [y, m] = k.split("-");
      return `<div class="tl-month"><span class="mdot">·</span>
        <div class="mt">${y} 年 ${MO[+m]}<span>${arr.length} 篇</span></div>
        ${arr.map((p) => {
          const c = ORG_COLORS[p.org] || "#8b9ac4";
          return `<div class="tl-item" data-file="${esc(p.file)}">
            <div class="d">${p.date.slice(5)}</div>
            <div class="t">${esc(p.title)}</div>
            <div class="m">${esc(p.summary || "")}</div>
            <div class="b"><span class="tag" style="color:${c}">${esc(p.type)}</span><span class="tag">#${esc(p.org)}</span></div>
          </div>`;
        }).join("")}
      </div>`;
    }).join("");
    document.querySelectorAll(".tl-item").forEach((el) => {
      el.addEventListener("click", () => {
        const p = papers.find((x) => x.file === el.dataset.file);
        if (p) openPaper(p);
      });
    });
  }

  /* ---------------- 渲染总入口 ---------------- */
  function render() {
    const list = filtered();
    document.getElementById("resCount").textContent = list.length;
    const active = [state.type !== "全部" ? state.type : "", state.org !== "全部" ? state.org : "", [...state.tags].join("/")].filter(Boolean);
    document.getElementById("resInfo").textContent = active.length ? "筛选：" + active.join(" · ") : "";
    renderGrid(list);
    renderTL(list);
  }

  /* ---------------- 视图切换 ---------------- */
  function setView(v) {
    state.view = v;
    const grid = document.getElementById("grid");
    const tl = document.getElementById("timeline");
    grid.style.display = v === "grid" ? "grid" : "none";
    tl.classList.toggle("on", v === "timeline");
    document.getElementById("btnGrid").classList.toggle("on", v === "grid");
    document.getElementById("btnTL").classList.toggle("on", v === "timeline");
    document.getElementById("navGrid").classList.toggle("active", v === "grid");
    document.getElementById("navTimeline").classList.toggle("active", v === "timeline");
  }

  /* ---------------- 事件 ---------------- */
  function bind() {
    document.addEventListener("click", (e) => {
      const chipEl = e.target.closest(".chip");
      if (chipEl) {
        const [kind, key] = chipEl.dataset.key.split("|");
        if (kind === "type") state.type = key;
        else if (kind === "org") state.org = key;
        else if (kind === "tag") {
          if (key === "__all__") state.tags.clear();
          else state.tags.has(key) ? state.tags.delete(key) : state.tags.add(key);
        }
        renderChips(); render();
      }
      if (e.target.closest("#btnGrid")) setView("grid");
      if (e.target.closest("#btnTL")) setView("timeline");
      if (e.target.closest("#navGrid")) setView("grid");
      if (e.target.closest("#navTimeline")) setView("timeline");
      if (e.target.closest("#btnClear")) {
        state.q = ""; state.type = "全部"; state.org = "全部"; state.tags.clear();
        document.getElementById("search").value = "";
        renderChips(); render();
      }
      if (e.target.closest("#btnRandom")) {
        const list = filtered();
        if (list.length) openPaper(list[Math.floor(Math.random() * list.length)]);
      }
    });
    let t;
    document.getElementById("search").addEventListener("input", (e) => {
      clearTimeout(t); t = setTimeout(() => { state.q = e.target.value; render(); }, 120);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "/" && document.activeElement !== document.getElementById("search")) {
        e.preventDefault(); document.getElementById("search").focus();
      }
      if (e.key === "Escape") { document.getElementById("search").blur(); }
    });
  }

  /* ---------------- 星野背景 ---------------- */
  function stars() {
    const cv = document.getElementById("stars"), ctx = cv.getContext("2d");
    let W, H, pts = [], meteors = [];
    function size() {
      W = cv.width = innerWidth; H = cv.height = innerHeight;
      const n = Math.min(240, Math.floor((W * H) / 6500));
      pts = Array.from({ length: n }, () => ({
        x: Math.random() * W, y: Math.random() * H,
        r: Math.random() * 1.4 + .25, a: Math.random(),
        tw: Math.random() * .02 + .004, hue: Math.random() < .2 ? 210 : (Math.random() < .5 ? 0 : 265),
      }));
    }
    function tick() {
      ctx.clearRect(0, 0, W, H);
      for (const p of pts) {
        p.a += p.tw;
        const alpha = .25 + Math.abs(Math.sin(p.a)) * .75;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 7);
        ctx.fillStyle = `hsla(${p.hue},80%,85%,${alpha})`; ctx.fill();
      }
      if (Math.random() < .012) meteors.push({ x: Math.random() * W * .7, y: -20, vx: 6 + Math.random() * 5, vy: 3.2 + Math.random() * 2.6, life: 1 });
      meteors = meteors.filter((m) => m.life > 0);
      for (const m of meteors) {
        m.x += m.vx; m.y += m.vy; m.life -= .018;
        ctx.strokeStyle = `rgba(180,215,255,${m.life * .85})`; ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.moveTo(m.x, m.y);
        ctx.lineTo(m.x - m.vx * 7, m.y - m.vy * 7); ctx.stroke();
      }
      requestAnimationFrame(tick);
    }
    addEventListener("resize", size);
    size(); tick();
  }

  /* ---------------- 启动 ---------------- */
  renderStats(); renderChips(); render(); setView("grid"); bind(); stars();
})();
