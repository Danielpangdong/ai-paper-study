from __future__ import annotations

import base64
from pathlib import Path
from textwrap import dedent

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "AI-Daily-Paper-AI-Chemist-2026-06-24-embedded.html"
EMAIL_BODY = ROOT / "email-body.html"
EMAIL_SUBJECT = ROOT / "email_subject.txt"
SOURCES = ROOT / "sources.md"
RUN_SUMMARY = ROOT / "run_summary.md"
HERO = ROOT / "ai-chemist-hero.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size, index=1 if bold else 0)
        except Exception:
            continue
    return ImageFont.load_default()


def make_hero() -> None:
    width, height = 1600, 900
    img = Image.new("RGB", (width, height), "#101518")
    draw = ImageDraw.Draw(img)

    for y in range(height):
        shade = int(18 + 22 * y / height)
        draw.line([(0, y), (width, y)], fill=(shade, shade + 5, shade + 8))

    # Restrained lab-grid background.
    for x in range(0, width, 80):
        draw.line((x, 0, x, height), fill=(28, 40, 44), width=1)
    for y in range(0, height, 80):
        draw.line((0, y, width, y), fill=(28, 40, 44), width=1)

    title_f = font(58, True)
    sub_f = font(30)
    small_f = font(22)
    label_f = font(25, True)

    draw.text((84, 86), "AI 化学家", fill="#f5f2ea", font=title_f)
    draw.text((88, 166), "从读论文到跑实验的科研闭环", fill="#b8d8d6", font=sub_f)
    draw.text((88, 220), "GPT-5.4 + Maria Lab 在 10,080 次实验中找到 TEMPO 方案", fill="#d5ded9", font=small_f)

    steps = [
        ("读文献", "#d7b56d"),
        ("提假设", "#83c5be"),
        ("排实验", "#8db8e8"),
        ("跑实验", "#d58a75"),
        ("读数据", "#a7c77a"),
        ("再优化", "#d7b56d"),
    ]
    x0, y0 = 110, 360
    w, h = 160, 74
    for i, (text, color) in enumerate(steps):
        x = x0 + i * 228
        draw.rounded_rectangle((x, y0, x + w, y0 + h), radius=14, fill="#f3f0e8", outline=color, width=4)
        tw = draw.textlength(text, font=label_f)
        draw.text((x + (w - tw) / 2, y0 + 22), text, fill="#16252a", font=label_f)
        if i < len(steps) - 1:
            ax = x + w + 16
            ay = y0 + h / 2
            draw.line((ax, ay, ax + 48, ay), fill="#d7b56d", width=5)
            draw.polygon([(ax + 48, ay), (ax + 30, ay - 12), (ax + 30, ay + 12)], fill="#d7b56d")

    # Yield card.
    draw.rounded_rectangle((1020, 560, 1488, 780), radius=26, fill="#f3f0e8", outline="#83c5be", width=4)
    draw.text((1060, 600), "平均产率", fill="#253334", font=font(30, True))
    draw.text((1060, 658), "16.6% → 25.2%", fill="#0d5f5a", font=font(58, True))
    draw.text((1060, 733), ">30% 反应占比翻倍以上", fill="#57676a", font=font(24))

    # Molecule-like ring motif.
    cx, cy = 760, 660
    pts = []
    for i in range(6):
        import math

        a = math.pi / 6 + i * math.pi / 3
        pts.append((cx + 120 * math.cos(a), cy + 120 * math.sin(a)))
    draw.line(pts + [pts[0]], fill="#83c5be", width=6)
    for px, py in pts:
        draw.ellipse((px - 14, py - 14, px + 14, py + 14), fill="#f3f0e8", outline="#83c5be", width=4)
    draw.text((cx - 48, cy - 18), "TEMPO", fill="#f3f0e8", font=font(28, True))

    HERO.parent.mkdir(parents=True, exist_ok=True)
    img.save(HERO, format="PNG", optimize=True)


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


make_hero()
hero_data = b64(HERO)

subject = "【AI每日论文精选】AI开始真正参与科学实验了？"

email_body = """<!doctype html><html lang="zh-CN"><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',Arial,sans-serif;line-height:1.7;color:#162022">
<p>今天精选的论文是 <b>TEMPO Improves Generality and Decreases Oxidative Deboronation in Chan-Lam Couplings of Primary Sulfonamides</b>。</p>
<p>一句话推荐理由：OpenAI 和 Molecule.one 把 GPT-5.4 接入 Maria 自动化实验平台，让 AI 参与提出假设、设计实验、读取数据和继续优化，最终在真实化学反应中找到一个可验证改进。</p>
<p>这可能是“AI 科学家”从答题系统走向实验闭环的重要信号。附件为中文深度拆解 HTML 报告，适合非技术读者阅读。</p>
</body></html>
"""

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI每日论文精选｜AI开始真正参与科学实验了？</title>
<style>
  :root {{
    color-scheme: light dark;
    --ink:#172225; --muted:#617174; --paper:#f6f5f0; --panel:#fffdf8;
    --line:#d9ded8; --teal:#0d6862; --blue:#2e6384; --gold:#a7772d;
    --rose:#8a4d4d; --dark:#101819; --soft:#e9f1ed;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC","PingFang SC",Arial,sans-serif; background:var(--paper); color:var(--ink); line-height:1.72; letter-spacing:0; }}
  a {{ color:var(--teal); text-decoration:none; }}
  .hero {{ position:relative; min-height:560px; color:white; overflow:hidden; background:#101819; }}
  .hero img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.82; }}
  .hero:after {{ content:""; position:absolute; inset:0; background:linear-gradient(90deg,rgba(12,18,20,.94),rgba(12,18,20,.62) 48%,rgba(12,18,20,.06)); }}
  .hero-inner,.wrap {{ max-width:980px; margin:0 auto; padding-left:18px; padding-right:18px; }}
  .hero-inner {{ position:relative; z-index:1; padding-top:74px; padding-bottom:64px; }}
  .eyebrow {{ display:inline-block; padding:6px 10px; border:1px solid rgba(255,255,255,.28); border-radius:999px; background:rgba(255,255,255,.08); color:#dcebe8; font-size:13px; }}
  h1 {{ margin:22px 0 18px; max-width:800px; font-size:42px; line-height:1.13; letter-spacing:0; }}
  .subtitle {{ max-width:750px; color:#dce5df; font-size:19px; }}
  .hero-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; max-width:820px; margin-top:30px; }}
  .metric {{ padding:14px; border:1px solid rgba(255,255,255,.22); border-radius:8px; background:rgba(255,255,255,.08); }}
  .metric b {{ display:block; font-size:22px; color:white; }}
  .metric span {{ display:block; font-size:12px; color:#c6d6d1; }}
  .wrap {{ padding-bottom:58px; }}
  section {{ margin-top:34px; }}
  h2 {{ margin:0 0 14px; font-size:25px; line-height:1.25; }}
  h3 {{ margin:0 0 9px; font-size:18px; line-height:1.35; }}
  p {{ margin:0 0 14px; }}
  .card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:20px; box-shadow:0 12px 28px rgba(34,44,38,.05); }}
  .grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
  .grid-3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }}
  table {{ width:100%; border-collapse:collapse; background:var(--panel); border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
  th,td {{ padding:12px 13px; border-bottom:1px solid var(--line); vertical-align:top; text-align:left; }}
  th {{ background:#e8f0ed; color:#263334; font-weight:750; }}
  tr:last-child td {{ border-bottom:0; }}
  .tag {{ display:inline-block; margin:0 6px 6px 0; padding:4px 9px; border-radius:999px; background:var(--soft); color:#24524f; font-size:12px; font-weight:750; }}
  .quote {{ border-left:4px solid var(--teal); background:#eef6f3; padding:16px 18px; border-radius:0 8px 8px 0; font-size:20px; font-weight:800; }}
  .diagram {{ width:100%; height:auto; display:block; background:#111b1d; border-radius:8px; border:1px solid #243437; }}
  .note {{ color:var(--muted); font-size:14px; }}
  .warn {{ border-left:4px solid var(--gold); }}
  .risk {{ border-left:4px solid var(--rose); }}
  .source-list li {{ margin-bottom:8px; }}
  .footer {{ margin-top:42px; color:var(--muted); font-size:13px; }}
  @media (max-width:720px) {{
    .hero {{ min-height:650px; }}
    h1 {{ font-size:31px; }}
    .subtitle {{ font-size:17px; }}
    .hero-grid,.grid-2,.grid-3 {{ grid-template-columns:1fr; }}
    th,td {{ display:block; width:100%; }}
    tr {{ display:block; border-bottom:1px solid var(--line); }}
    tr:last-child {{ border-bottom:0; }}
    th {{ border-bottom:0; }}
  }}
</style>
</head>
<body>
<header class="hero">
  <img src="data:image/png;base64,{hero_data}" alt="AI chemist research loop visual">
  <div class="hero-inner">
    <span class="eyebrow">AI每日论文精选 · 2026-06-24</span>
    <h1>AI 开始真正参与科学实验了？</h1>
    <p class="subtitle">今天这篇论文重要，不是因为 AI “懂化学题”了，而是因为它进入了真实科研闭环：读文献、提假设、让自动化实验室跑上万次实验、再根据数据继续优化。</p>
    <div class="hero-grid">
      <div class="metric"><b>10,080</b><span>微升级实验反应</span></div>
      <div class="metric"><b>16.6%→25.2%</b><span>平均估计产率</span></div>
      <div class="metric"><b>11/14</b><span>bench-scale 复验提升</span></div>
      <div class="metric"><b>3 months</b><span>从首个 prompt 到专家分享</span></div>
    </div>
  </div>
</header>

<main class="wrap">
  <section>
    <h2>1. 标题区</h2>
    <table>
      <tr><th>论文</th><td><b>TEMPO Improves Generality and Decreases Oxidative Deboronation in Chan-Lam Couplings of Primary Sulfonamides</b><br>中文可译：TEMPO 提高伯磺酰胺 Chan-Lam 偶联反应的通用性，并减少氧化脱硼副反应</td></tr>
      <tr><th>作者</th><td>Jan Rzymkowski, Shuyuan Zhang, Artur Choluj, Aleksander Szkolka, Mateja Dud, Mateusz Bruno-Kaminski, Jan Busz, Michal Sadowski, Grzegorz Wojciechowski, Jan Kulczycki, Mariusz Gruza, Tadija Radusinovic, Maria Wyrzykowska, Szymon Kapuscinski, Oleksandr Popika, Lukasz Szczupak, Ahmed El-Kishky, Paulina Wach, Pawel Wlodarczyk-Pruszynski, Piotr Byrski, Joe Palermo, Stan Jastrzebski</td></tr>
      <tr><th>机构</th><td>Molecule.one（San Francisco / Warsaw）与 OpenAI（San Francisco）</td></tr>
      <tr><th>发布时间</th><td>OpenAI 发布：2026-06-17；preprint PDF：20 页；平台：OpenAI Research / Molecule.one / OpenAI CDN preprint</td></tr>
      <tr><th>链接</th><td><a href="https://openai.com/index/ai-chemist-improves-reaction/">OpenAI 官方解读</a> · <a href="https://cdn.openai.com/pdf/7136bb75-6d47-4834-8fff-c07c0e06708a/tempo-improves-generality-and-decreases-oxidative-deboronation.pdf">论文 PDF</a> · <a href="https://molecule.one/">Molecule.one 项目页</a></td></tr>
    </table>
  </section>

  <section>
    <h2>2. 为什么今天选它？</h2>
    <div class="grid-2">
      <div class="card">
        <h3>因为它不是“答题”，而是“做实验”</h3>
        <p>很多 AI for Science 论文仍停留在预测、问答、文献总结。这里的 AI 系统进入了湿实验世界：提出研究方向，设计实验矩阵，读取真实仪器数据，再提出下一轮实验。</p>
      </div>
      <div class="card">
        <h3>因为它把“AI 科学家”变得可度量</h3>
        <p>AI 的贡献不再只是一个漂亮段落，而是反应产率、底物覆盖、bench-scale 复验这些硬指标。科学世界最终看证据，不看口才。</p>
      </div>
    </div>
    <div class="card warn" style="margin-top:14px">
      <span class="tag">AI for Science</span><span class="tag">Agentic Lab</span><span class="tag">药物化学</span><span class="tag">高通量实验</span>
      <p>这篇值得长期关注，是因为它指向一个更大的趋势：未来的 AI 产品不只是聊天窗口，而可能是“软件 + 自动化设备 + 专家审核 + 实验数据”的闭环系统。</p>
    </div>
  </section>

  <section>
    <h2>3. 一句话讲透论文</h2>
    <div class="quote">这篇论文本质上是在证明：AI 可以像一个初级科研合作者一样，提出一个可验证的化学假设，并通过自动化实验把它一步步筛出来。</div>
  </section>

  <section>
    <h2>4. 核心贡献拆解</h2>
    <div class="grid-3">
      <div class="card"><h3>提出一个反应改进</h3><p>针对伯磺酰胺与芳基硼酸的 Chan-Lam 偶联，系统发现 TEMPO 能提高目标 C-N 成键，并减少硼酸降解副反应。</p></div>
      <div class="card"><h3>用大规模实验验证</h3><p>两轮微升级高通量实验共 10,080 次，覆盖氧化剂、铜源、碱、溶剂、温度、底物结构等变量。</p></div>
      <div class="card"><h3>形成 AI 科研闭环</h3><p>GPT-5.4 负责提出和排序想法，Maria AI/Lab 把方案变成实验，结构化结果再反馈给模型提出下一步。</p></div>
    </div>
  </section>

  <section>
    <h2>5. 工作原理：AI 像“研究小组”一样工作</h2>
    <div class="card">
      <svg class="diagram" viewBox="0 0 980 390" role="img" aria-label="AI chemist workflow">
        <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#d4b15f"/></marker></defs>
        <rect x="0" y="0" width="980" height="390" fill="#111b1d"/>
        <text x="42" y="48" fill="#f2eee6" font-size="26" font-weight="700">从“会答题”到“会循环做研究”</text>
        <g fill="#f1eee6" stroke="#83c5be" stroke-width="3">
          <rect x="48" y="96" width="150" height="70" rx="10"/><rect x="250" y="96" width="150" height="70" rx="10"/><rect x="452" y="96" width="150" height="70" rx="10"/><rect x="654" y="96" width="150" height="70" rx="10"/>
        </g>
        <text x="83" y="139" fill="#18282b" font-size="22" font-weight="700">读文献</text>
        <text x="285" y="139" fill="#18282b" font-size="22" font-weight="700">提假设</text>
        <text x="487" y="139" fill="#18282b" font-size="22" font-weight="700">排实验</text>
        <text x="690" y="139" fill="#18282b" font-size="22" font-weight="700">跑实验</text>
        <line x1="205" y1="131" x2="242" y2="131" stroke="#d4b15f" stroke-width="4" marker-end="url(#arrow)"/>
        <line x1="407" y1="131" x2="444" y2="131" stroke="#d4b15f" stroke-width="4" marker-end="url(#arrow)"/>
        <line x1="609" y1="131" x2="646" y2="131" stroke="#d4b15f" stroke-width="4" marker-end="url(#arrow)"/>
        <line x1="730" y1="176" x2="730" y2="230" stroke="#d4b15f" stroke-width="4" marker-end="url(#arrow)"/>
        <g fill="#203234" stroke="#6e8782" stroke-width="2">
          <rect x="570" y="246" width="320" height="88" rx="12"/>
        </g>
        <text x="602" y="282" fill="#f2eee6" font-size="21" font-weight="700">实验数据回流</text>
        <text x="602" y="313" fill="#c6d6d1" font-size="17">产率、副产物、底物范围、失败样本</text>
        <path d="M570 292 C420 345 255 325 202 174" fill="none" stroke="#d4b15f" stroke-width="4" marker-end="url(#arrow)"/>
        <text x="62" y="245" fill="#c8d7d2" font-size="18">像人类课题组：不是一次回答完，而是根据实验结果继续收窄问题。</text>
      </svg>
      <p class="note">高中生版类比：普通 AI 像“考试会做题的学生”；这个系统更像“有实验室的学生”。它不是只写答案，而是把想法拿去试，试完看数据，再改方案。</p>
    </div>
  </section>

  <section>
    <h2>6. 关键术语解释</h2>
    <table>
      <tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr>
      <tr><td>Chan-Lam coupling</td><td>一种铜催化的交叉偶联反应，可形成 C-N、C-O、C-S 等键。</td><td>像把两个化学零件用铜催化剂接起来，常用于做药物分子。</td></tr>
      <tr><td>Primary sulfonamide</td><td>含 R-SO2NH2 结构的官能团，在药物化学中常见但反应性偏弱。</td><td>一种药物里常见的“把手”，有价值但不好加工。</td></tr>
      <tr><td>TEMPO</td><td>稳定的氮氧自由基氧化剂，可调节铜氧化还原过程。</td><td>像温和的交通协管员，让反应更走正路，少跑偏。</td></tr>
      <tr><td>HTE</td><td>High-throughput experimentation，高通量实验。</td><td>一次不只试几个配方，而是像批量测评一样同时试上千个配方。</td></tr>
      <tr><td>Yield</td><td>目标产物产率，表示起始物有多少变成了想要的产品。</td><td>做菜时最后真正做成功的比例。</td></tr>
      <tr><td>Deboronation</td><td>硼酸底物失去硼相关基团的降解副反应。</td><td>原料还没来得及组装，就先坏掉了。</td></tr>
    </table>
  </section>

  <section>
    <h2>7. 实验结果解读</h2>
    <table>
      <tr><th>指标</th><th>无氧化剂 / 基线</th><th>TEMPO 优化后</th><th>这意味着什么</th></tr>
      <tr><td>平均估计产率</td><td>16.6%</td><td>25.2%</td><td>不是小样本偶然提升，而是在大矩阵中整体抬高。</td></tr>
      <tr><td>>30% 产率反应占比</td><td>15.6%</td><td>37.5%</td><td>“可用”的反应组合明显变多，底物范围更宽。</td></tr>
      <tr><td>底物层面改善</td><td>历史上伯磺酰胺 Chan-Lam 难做</td><td>88% 芳基硼酸、83% 磺酰胺测试中改善</td><td>说明它不是只对单个幸运样本有效。</td></tr>
      <tr><td>人工 bench-scale 复验</td><td>微升级筛选可能有假阳性</td><td>14 对代表性底物中 11 对提升，多数超过两倍</td><td>结果从自动化小体积实验走向真实实验台验证。</td></tr>
    </table>
    <p class="note">关键点：25.2% 不是“高到可以直接工业生产”的神奇产率，而是对一个难反应的系统性改进。真正重要的是流程：AI 提出可被实验检验的假设，并在真实数据中找到了方向。</p>
  </section>

  <section>
    <h2>8. 局限性与问题</h2>
    <div class="grid-2">
      <div class="card risk"><h3>还不是完全自主科学家</h3><p>人类仍写 steering/grading prompts，筛选高分方案，修正部分实验计划，参与实验操作，并进行 bench-scale 复验。</p></div>
      <div class="card risk"><h3>泛化还没证明</h3><p>论文聚焦一个具体反应家族。它不等于证明 AI 可以独立解决所有有机化学问题，也不等于能直接迁移到生产规模。</p></div>
      <div class="card risk"><h3>依赖昂贵实验基础设施</h3><p>Maria Lab 这样的高通量自动化平台并不是普通实验室标配。真正落地需要设备、数据标准、试剂供应和安全流程。</p></div>
      <div class="card risk"><h3>安全和双用途风险存在</h3><p>化学能力既能服务药物和材料，也可能被滥用。OpenAI 强调本项目限定在合法药物化学问题，并保留人类控制。</p></div>
    </div>
  </section>

  <section>
    <h2>9. 产业影响分析</h2>
    <div class="card">
      <h3>谁会受益？</h3>
      <p>药物发现公司、CRO、自动化实验室、化学数据平台、AI for Science 基础设施公司都会受益。最直接的价值是：更快地找到“值得继续做”的反应条件，而不是让博士生一周一周手动试错。</p>
      <h3>谁会被冲击？</h3>
      <p>只靠人工经验和低通量筛选的传统流程会承压。未来竞争力可能来自“模型能力 + 自动化实验 + 私有实验数据 + 专家审核”的组合，而不只是单个模型。</p>
      <h3>它会改变 AI 竞争格局吗？</h3>
      <p>会给一个方向：大模型公司不只卖 API，还可能嵌入到科学工作流。对投资人和产品经理来说，重点不是“AI 会不会替代科学家”，而是“谁能把 AI 接到真实测量系统里”。</p>
    </div>
  </section>

  <section>
    <h2>10. 延伸阅读</h2>
    <ul class="source-list">
      <li><a href="https://cdn.openai.com/pdf/7136bb75-6d47-4834-8fff-c07c0e06708a/tempo-improves-generality-and-decreases-oxidative-deboronation.pdf">论文 PDF：TEMPO Improves Generality...</a></li>
      <li><a href="https://openai.com/index/ai-chemist-improves-reaction/">OpenAI 官方文章：A near-autonomous AI chemist improves a challenging reaction</a></li>
      <li><a href="https://molecule.one/">Molecule.one：Maria AI / Lab / Data 平台说明</a></li>
      <li><a href="https://openai.com/index/introducing-life-sci-bench/">OpenAI LifeSciBench：真实生命科学任务 benchmark</a></li>
      <li><a href="https://arxiv.org/pdf/2510.10645">Trustworthy Retrosynthesis: Mitigating Hallucinations with Reaction Plausibility Filtering and Retrieval-Augmented Scoring</a></li>
    </ul>
  </section>

  <section>
    <h2>11. 引用来源</h2>
    <table>
      <tr><th>来源</th><th>本报告使用方式</th></tr>
      <tr><td>OpenAI 官方研究文章，2026-06-17</td><td>核对发布时间、近自主工作流、10,080 次实验、两轮实验、3 个月周期、关键结果和局限性表述。</td></tr>
      <tr><td>OpenAI/Molecule.one preprint PDF</td><td>核对正式论文标题、作者机构、摘要、实验规模、产率、复验结果、4-hydroxy-TEMPO、氧化脱硼机制假设。</td></tr>
      <tr><td>Molecule.one 官方页面</td><td>核对 Maria AI/Lab/Data 平台定位、双方合作、preprint 链接及反应示意。</td></tr>
      <tr><td>OpenAI LifeSciBench</td><td>作为背景资料，说明真实科研任务评测为何从“单题问答”转向复杂研究工作流。</td></tr>
    </table>
  </section>

  <p class="footer">生成时间：2026-06-24 Asia/Shanghai。本文为中文解读，不构成化学实验建议；所有具体反应条件以原论文和补充材料为准。</p>
</main>
</body>
</html>
"""

sources = dedent(
    """\
    # Sources

    - OpenAI article: https://openai.com/index/ai-chemist-improves-reaction/
    - Preprint PDF: https://cdn.openai.com/pdf/7136bb75-6d47-4834-8fff-c07c0e06708a/tempo-improves-generality-and-decreases-oxidative-deboronation.pdf
    - Molecule.one official page: https://molecule.one/
    - OpenAI LifeSciBench: https://openai.com/index/introducing-life-sci-bench/
    - Related paper: https://arxiv.org/pdf/2510.10645

    Key checked facts:
    - OpenAI article date: 2026-06-17.
    - Paper title: TEMPO Improves Generality and Decreases Oxidative Deboronation in Chan-Lam Couplings of Primary Sulfonamides.
    - Authors and affiliations checked from PDF text.
    - HTE campaign: 10,080 microscale reactions across two campaigns.
    - Optimized condition: 2 eq TEMPO and 20 mol% Cu(OAc)2 in paper abstract.
    - Mean estimated product yield: 16.6% to 25.2%.
    - Share of reactions exceeding 30% yield: 15.6% to 37.5%.
    - Bench-scale validation: 11 of 14 representative substrate pairs improved; majority over twofold.
    - OpenAI article states this is near-autonomous, not fully autonomous, with human steering, review, corrections, operations, and validation.
    """
)

run_summary = dedent(
    """\
    # Run Summary

    - Automation: AI每日论文博客精选
    - Automation ID: ai
    - Run date: 2026-06-24 Asia/Shanghai
    - Selected paper: TEMPO Improves Generality and Decreases Oxidative Deboronation in Chan-Lam Couplings of Primary Sulfonamides
    - Authors: Jan Rzymkowski, Shuyuan Zhang, Artur Choluj, Aleksander Szkolka, Mateja Dud, Mateusz Bruno-Kaminski, Jan Busz, Michal Sadowski, Grzegorz Wojciechowski, Jan Kulczycki, Mariusz Gruza, Tadija Radusinovic, Maria Wyrzykowska, Szymon Kapuscinski, Oleksandr Popika, Lukasz Szczupak, Ahmed El-Kishky, Paulina Wach, Pawel Wlodarczyk-Pruszynski, Piotr Byrski, Joe Palermo, Stan Jastrzebski
    - Institution: Molecule.one and OpenAI
    - Why selected: concrete AI-for-science wet-lab loop where GPT-5.4 and Maria AI/Lab proposed, tested, analyzed, and refined a medicinal-chemistry reaction improvement, with 10,080 HTE reactions and bench-scale validation.
    - Recently avoided: SkillOpt, Arbor, Sumi, DiffusionGemma, ToolPrivBench, MiniMax Sparse Attention, ABC-Bench, SWITCH latent reasoning.
    - Sources checked: OpenAI article, preprint PDF, Molecule.one page, OpenAI LifeSciBench, related retrosynthesis paper.
    - Artifact: `/Users/mac/Desktop/AI论文解读/reports/2026-06-24-ai-chemist/AI-Daily-Paper-AI-Chemist-2026-06-24-embedded.html`
    - Email subject: `【AI每日论文精选】AI开始真正参与科学实验了？`
    """
)

REPORT.write_text(html, encoding="utf-8")
EMAIL_BODY.write_text(email_body, encoding="utf-8")
EMAIL_SUBJECT.write_text(subject + "\n", encoding="utf-8")
SOURCES.write_text(sources, encoding="utf-8")
RUN_SUMMARY.write_text(run_summary, encoding="utf-8")
