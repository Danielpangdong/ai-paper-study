from __future__ import annotations

import base64
import html.parser as html_parser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "AI-Daily-Paper-PairCoder-2026-07-05.html"
EMAIL_BODY = ROOT / "email_body.txt"
EMAIL_SUBJECT = ROOT / "email_subject.txt"
SOURCES = ROOT / "sources.md"
HERO = ROOT / "paircoder-hero.png"


def data_uri(path: Path) -> str:
    raw = path.read_bytes()
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


hero_uri = data_uri(HERO)

subject = "【AI每日论文精选】AI写代码不只会聊天，开始会交付可验证产物"

email_body = """今天精选的论文是 PairCoder++。

它研究的不是“让模型多说几句推理过程”，而是让两个 AI 像结对程序员一样工作：一个写代码，一个拿编译器、运行结果、渲染图或仿真器证据来审查。

这篇论文重要的地方在于：很多未来的 AI 产物都会先以代码形式出现，比如图表、网页、3D 场景、CAD 模型和芯片设计。PairCoder++ 给出了一个清晰信号：AI Agent 的下一步，不是更会聊天，而是更会被工具链验证、修复并交付。

附件为中文深度拆解 HTML 报告，适合非技术读者阅读。
"""

sources_md = """# Sources

- arXiv abstract: https://arxiv.org/abs/2607.01883
- arXiv HTML: https://arxiv.org/html/2607.01883
- Project page: https://yisuanwang.github.io/PairCoder/
- GitHub repository: https://github.com/yisuanwang/PairCoder
- Original PairCoder ACL 2026 Findings page: https://aclanthology.org/2026.findings-acl.149/

Local copies:

- /Users/mac/Desktop/AI论文解读/reports/source_papers/paircoder-2607.01883.html
- /Users/mac/Desktop/AI论文解读/reports/source_papers/paircoder-2607.01883.pdf
- /Users/mac/Desktop/AI论文解读/reports/source_papers/paircoder-2607.01883.txt
- /Users/mac/Desktop/AI论文解读/reports/source_papers/paircoder-project.html
- /Users/mac/Desktop/AI论文解读/reports/source_papers/paircoder-github-readme.md
"""


html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI每日论文精选｜PairCoder++：让 AI 交付可验证产物</title>
  <style>
    :root {{
      color-scheme: light dark;
      --ink: #162033;
      --muted: #647084;
      --paper: #f7f9fc;
      --panel: #ffffff;
      --line: #dbe3ef;
      --blue: #2563d8;
      --green: #087f68;
      --gold: #a66f14;
      --red: #c3423f;
      --slate: #24354d;
      --soft-blue: #eef4ff;
      --soft-green: #edf8f5;
      --soft-gold: #fff5df;
      --soft-red: #fff0f0;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
      background: var(--paper);
      color: var(--ink);
      line-height: 1.72;
    }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .wrap {{ max-width: 1060px; margin: 0 auto; padding: 28px 18px 56px; }}
    .hero {{
      display: grid;
      grid-template-columns: 1.02fr .98fr;
      gap: 24px;
      align-items: center;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 32px;
      background: linear-gradient(180deg, #fff 0%, #f3f7fd 100%);
    }}
    .eyebrow {{ color: var(--blue); font-size: 13px; font-weight: 800; margin-bottom: 12px; }}
    h1 {{ margin: 0; font-size: 40px; line-height: 1.14; letter-spacing: 0; }}
    .subtitle {{ margin: 16px 0 0; color: var(--muted); font-size: 18px; }}
    .hero-img {{ width: 100%; border: 1px solid var(--line); border-radius: 8px; display: block; background: #fff; }}
    .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 18px; }}
    .meta {{ border: 1px solid var(--line); border-radius: 8px; padding: 12px; background: rgba(255,255,255,.78); }}
    .meta b {{ display: block; color: var(--muted); font-size: 12px; margin-bottom: 4px; }}
    .meta span {{ display: block; font-size: 14px; font-weight: 750; }}
    section {{ margin-top: 22px; }}
    .section {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 24px;
    }}
    h2 {{ margin: 0 0 14px; font-size: 26px; line-height: 1.22; letter-spacing: 0; }}
    h3 {{ margin: 22px 0 8px; font-size: 18px; }}
    p {{ margin: 0 0 12px; }}
    .lead {{ font-size: 19px; color: #263852; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      background: #fff;
    }}
    .card.blue {{ background: var(--soft-blue); }}
    .card.green {{ background: var(--soft-green); }}
    .card.gold {{ background: var(--soft-gold); }}
    .card.red {{ background: var(--soft-red); }}
    .label {{ font-size: 12px; font-weight: 800; color: var(--muted); text-transform: uppercase; }}
    .big {{ font-size: 28px; font-weight: 850; line-height: 1.1; margin: 6px 0; }}
    .tagline {{
      display: block;
      margin: 14px 0;
      padding: 16px 18px;
      border-left: 4px solid var(--blue);
      background: var(--soft-blue);
      font-size: 20px;
      font-weight: 800;
    }}
    table {{ width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 14px; }}
    th, td {{ border: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top; }}
    th {{ background: #f3f6fb; color: var(--slate); }}
    .note {{ color: var(--muted); font-size: 13px; }}
    .pill {{ display: inline-block; border-radius: 999px; border: 1px solid var(--line); padding: 3px 9px; font-size: 12px; font-weight: 750; background: #fff; margin: 2px 4px 2px 0; }}
    .viz {{ width: 100%; overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; background: #fff; padding: 10px; margin: 14px 0; }}
    .barrow {{ display: grid; grid-template-columns: 150px 1fr 86px; gap: 10px; align-items: center; margin: 10px 0; }}
    .bartrack {{ height: 12px; border-radius: 999px; background: #e9eef6; overflow: hidden; }}
    .bar {{ height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--blue), var(--green)); }}
    .refs li {{ margin-bottom: 8px; }}
    @media (max-width: 760px) {{
      .hero, .grid-3, .grid-2, .meta-grid {{ grid-template-columns: 1fr; }}
      .hero {{ padding: 20px; }}
      h1 {{ font-size: 30px; }}
      .barrow {{ grid-template-columns: 1fr; }}
      table {{ font-size: 13px; }}
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --ink:#e8eef8; --muted:#aab6c8; --paper:#101722; --panel:#151f2d; --line:#2b3b52; --soft-blue:#172846; --soft-green:#132b28; --soft-gold:#2d2415; --soft-red:#321c1e; }}
      .hero, .card, th, .meta, .viz {{ background:#151f2d; }}
      .hero-img {{ background:#fff; }}
    }}
  </style>
</head>
<body>
<main class="wrap">
  <section class="hero">
    <div>
      <div class="eyebrow">AI每日论文精选 · 2026-07-05</div>
      <h1>PairCoder++：AI 写代码的下一步，是交付可验证产物</h1>
      <p class="subtitle">不是让模型“多想一会儿”，而是让两个 AI 像结对程序员一样：一个写，一个拿真实工具链证据审查，直到代码能运行、能渲染、能通过测试。</p>
      <div class="meta-grid">
        <div class="meta"><b>论文</b><span>PairCoder++</span></div>
        <div class="meta"><b>平台</b><span>arXiv / ACL 2026 Findings</span></div>
        <div class="meta"><b>日期</b><span>2026-07-02</span></div>
        <div class="meta"><b>主题</b><span>Agent · 代码生成 · 可验证产物</span></div>
      </div>
    </div>
    <img class="hero-img" src="{hero_uri}" alt="PairCoder++ two-agent verification workflow infographic">
  </section>

  <section class="section" id="paper-info">
    <h2>1. 标题区</h2>
    <table>
      <tr><th>英文标题</th><td>PairCoder++: Pair Programming as a Universal Paradigm for Verified Code-Driven Multimodal and Structured-Artifact Generation</td></tr>
      <tr><th>中文标题</th><td>PairCoder++：把结对编程变成可验证代码驱动多模态与结构化产物生成的通用范式</td></tr>
      <tr><th>作者</th><td>Junhao Chen, Xiang Li, Mingjin Chen, Boran Zhang, Henghaofan Zhang, Yibin Xu, Yuehan Cui, Fangsheng Weng, Fei Ma, Qi Tian, Ruqi Huang, Hao Zhao</td></tr>
      <tr><th>机构</th><td>Tsinghua University, Peking University, The Hong Kong Polytechnic University, USTC, UESTC, Tongji University, Tianjin University, Guangming Lab, BAAI 等</td></tr>
      <tr><th>发布时间</th><td>arXiv v1: 2026-07-02 08:36 UTC；论文页面标注 Accepted by ACL 2026</td></tr>
      <tr><th>链接</th><td><a href="https://arxiv.org/abs/2607.01883">arXiv</a> · <a href="https://yisuanwang.github.io/PairCoder/">Project Page</a> · <a href="https://github.com/yisuanwang/PairCoder">GitHub</a></td></tr>
    </table>
  </section>

  <section class="section" id="why">
    <h2>2. 为什么今天选它？</h2>
    <p class="lead">因为它抓住了 AI Agent 从“会聊天”走向“会交付”的关键门槛：产物必须能被真实世界的工具检查。</p>
    <div class="grid-3">
      <div class="card blue"><div class="label">行业意义</div><div class="big">从答案到产物</div><p>未来很多 AI 输出不是一句话，而是一段可运行代码：图表、网页、CAD、3D、芯片逻辑。PairCoder++ 研究的正是这类“用代码表示的产物”。</p></div>
      <div class="card green"><div class="label">技术突破</div><div class="big">审查有证据</div><p>Navigator 不是凭感觉挑刺，而是看编译错误、测试结果、渲染图或仿真器反馈。它必须指出具体错误，否则返回 <b>[NOERROR]</b>。</p></div>
      <div class="card gold"><div class="label">长期价值</div><div class="big">Agent 工程范式</div><p>这不是某个模型的小技巧，而是一种可迁移流程：只要任务有可靠检查器，就可以把单次生成变成“生成-验证-修复”的闭环。</p></div>
    </div>
  </section>

  <section class="section" id="one-sentence">
    <h2>3. 一句话讲透论文</h2>
    <span class="tagline">PairCoder++ 本质上是在让 AI 像一对严谨的程序员：一个负责把想法写成代码，另一个拿真实运行证据检查它，直到产物真的站得住。</span>
    <p>如果说普通聊天机器人像“口头回答问题”，PairCoder++ 更像“交作业前先跑一遍测试”。这一步看似朴素，却是 AI 真正进入生产流程的核心。</p>
  </section>

  <section class="section" id="contributions">
    <h2>4. 核心贡献拆解</h2>
    <div class="grid-2">
      <div class="card"><h3>提出了什么</h3><p>一个 Driver + Navigator 的双 Agent 框架。Driver 写代码，Navigator 基于工具链证据审查；如果发现问题，角色切换，发现问题的人接手修复。</p></div>
      <div class="card"><h3>解决什么问题</h3><p>单次生成很脆：代码看起来像对的，但可能不能运行、图表变形、3D 模型空壳、硬件逻辑不通过仿真。PairCoder++ 把“看起来对”改成“被工具证明基本可用”。</p></div>
      <div class="card"><h3>与旧方法区别</h3><p>旧方法常让模型自我反思或多 Agent 互相讨论，但证据弱。这里的审查来自编译器、渲染器、测试器、仿真器，像老师看作业时直接运行代码。</p></div>
      <div class="card"><h3>为什么更好</h3><p>它能利用外部世界给出的硬反馈。模型不知道哪里坏，工具知道；模型擅长修，工具擅长判。两者合起来，才接近“能交付”。</p></div>
    </div>
  </section>

  <section class="section" id="mechanism">
    <h2>5. 工作原理：像一间有验收环节的小型工作室</h2>
    <p>可以把 PairCoder++ 想成一个小团队：Driver 是执行者，先做出第一版；工具链是质检机器，负责发现硬错误；Navigator 是审稿人，只能根据质检证据给意见；如果问题很具体，Navigator 直接坐到键盘前修。</p>
    <div class="viz">
      <svg viewBox="0 0 1000 330" width="100%" role="img" aria-label="PairCoder workflow">
        <defs>
          <linearGradient id="g" x1="0" x2="1"><stop stop-color="#2563d8"/><stop offset="1" stop-color="#087f68"/></linearGradient>
          <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#556579"/></marker>
        </defs>
        <rect x="20" y="42" width="155" height="80" rx="8" fill="#eef4ff" stroke="#c9d8f2"/>
        <text x="98" y="75" text-anchor="middle" font-size="21" font-weight="700" fill="#162033">任务需求</text>
        <text x="98" y="102" text-anchor="middle" font-size="14" fill="#647084">图表 / 网页 / 3D / 硬件</text>
        <rect x="245" y="30" width="170" height="105" rx="8" fill="#fff" stroke="#dbe3ef"/>
        <text x="330" y="70" text-anchor="middle" font-size="24" font-weight="800" fill="#2563d8">Driver</text>
        <text x="330" y="101" text-anchor="middle" font-size="15" fill="#647084">写出候选代码</text>
        <rect x="500" y="30" width="185" height="105" rx="8" fill="#edf8f5" stroke="#c3e1da"/>
        <text x="592" y="65" text-anchor="middle" font-size="23" font-weight="800" fill="#087f68">工具链验证</text>
        <text x="592" y="96" text-anchor="middle" font-size="14" fill="#647084">编译 / 运行 / 渲染 / 仿真</text>
        <rect x="760" y="30" width="190" height="105" rx="8" fill="#fff5df" stroke="#ead5a9"/>
        <text x="855" y="65" text-anchor="middle" font-size="24" font-weight="800" fill="#a66f14">Navigator</text>
        <text x="855" y="96" text-anchor="middle" font-size="14" fill="#647084">基于证据审查</text>
        <path d="M175 82 L240 82" stroke="#556579" stroke-width="3" marker-end="url(#arrow)"/>
        <path d="M415 82 L494 82" stroke="#556579" stroke-width="3" marker-end="url(#arrow)"/>
        <path d="M685 82 L754 82" stroke="#556579" stroke-width="3" marker-end="url(#arrow)"/>
        <path d="M855 139 C855 235 330 235 330 143" fill="none" stroke="#556579" stroke-width="3" marker-end="url(#arrow)"/>
        <text x="592" y="225" text-anchor="middle" font-size="17" font-weight="700" fill="#162033">发现具体错误：请求修复并切换角色</text>
        <path d="M855 139 C900 175 910 220 910 262 L910 280 L760 280" fill="none" stroke="url(#g)" stroke-width="4" marker-end="url(#arrow)"/>
        <rect x="560" y="250" width="200" height="55" rx="8" fill="#eef4ff" stroke="#c9d8f2"/>
        <text x="660" y="283" text-anchor="middle" font-size="19" font-weight="800" fill="#162033">[NOERROR] 后交付</text>
      </svg>
    </div>
    <ol>
      <li>给定一个任务，比如“根据数据画一张图”或“生成一个 Blender 3D 场景”。</li>
      <li>Driver 先写出一版代码。</li>
      <li>系统运行真实工具：编译、执行、渲染、测试或仿真。</li>
      <li>Navigator 查看证据，必须给出具体错误；如果没有具体错误，就接受。</li>
      <li>如果有错误，角色切换，审查者变成修复者，进入下一轮。</li>
    </ol>
  </section>

  <section class="section" id="terms">
    <h2>6. 关键术语解释</h2>
    <table>
      <tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr>
      <tr><td>Agent</td><td>能调用工具、观察反馈并多步完成任务的模型流程。</td><td>不是只回答一句话，而是能干活、看结果、继续改的人。</td></tr>
      <tr><td>Artifact</td><td>由代码生成的结构化或多模态产物，如图表、SVG、CAD、3D 场景、网页、Verilog。</td><td>AI 最后交出来的“东西”，不是聊天记录。</td></tr>
      <tr><td>Toolchain</td><td>编译器、解释器、渲染器、模拟器、测试框架等外部工具集合。</td><td>检查作业的机器：能跑就跑，不能跑就报错。</td></tr>
      <tr><td>Oracle</td><td>能判断候选输出好坏的验证信号。</td><td>裁判。裁判越靠谱，AI 越知道往哪改。</td></tr>
      <tr><td>[NOERROR]</td><td>Navigator 无法指出具体错误时必须返回的接受标记。</td><td>别没事找事。已经可用，就别继续乱改。</td></tr>
      <tr><td>Token cost</td><td>模型输入输出 token 消耗，近似对应推理成本。</td><td>多请两个 AI 轮流检查，质量更高，但账单也更高。</td></tr>
    </table>
  </section>

  <section class="section" id="results">
    <h2>7. 实验结果解读</h2>
    <p>论文在 17 个公开基准、7 个模型、3 家模型供应商上测试。最值得看的不是“平均涨了多少”，而是它在哪些任务上明显有效：凡是有强工具链反馈、且原模型还有犯错空间的地方，收益最明显。</p>
    <table>
      <tr><th>任务</th><th>指标</th><th>单模型</th><th>PairCoder</th><th>普通人怎么理解</th></tr>
      <tr><td>DaTikZ</td><td>有效渲染率</td><td>0.717</td><td><b>0.967</b></td><td>科学图示从“经常画不出来”接近“基本能画出来”。</td></tr>
      <tr><td>Plot2Code</td><td>执行率</td><td>0.962</td><td><b>0.977</b></td><td>本来就不错，PairCoder 继续把边缘错误补掉。</td></tr>
      <tr><td>GenCAD-Code</td><td>执行率 / Chamfer ↓</td><td>0.867 / 0.259</td><td><b>0.983 / 0.155</b></td><td>CAD 模型更常成功生成，几何误差也更小。</td></tr>
      <tr><td>3DCodeBench</td><td>Blender 可执行率</td><td>0.433</td><td><b>0.783</b></td><td>3D 场景从“经常空跑或报错”变成“多数能真正生成”。</td></tr>
      <tr><td>StarVector</td><td>渲染率</td><td>0.900</td><td><b>1.000</b></td><td>向量图生成更稳定，至少不容易交出坏文件。</td></tr>
    </table>
    <div class="viz" aria-label="Result bars">
      <div class="barrow"><strong>DaTikZ 有效渲染</strong><div class="bartrack"><div class="bar" style="width:96.7%"></div></div><span>0.967</span></div>
      <div class="barrow"><strong>GenCAD 执行</strong><div class="bartrack"><div class="bar" style="width:98.3%"></div></div><span>0.983</span></div>
      <div class="barrow"><strong>3DCodeBench 执行</strong><div class="bartrack"><div class="bar" style="width:78.3%"></div></div><span>0.783</span></div>
      <div class="barrow"><strong>StarVector 渲染</strong><div class="bartrack"><div class="bar" style="width:100%"></div></div><span>1.000</span></div>
    </div>
    <p class="note">代价也很明确：论文报告 PairCoder 相比单次生成约为 2.9 到 9.2 倍 token 成本，整体约 7 倍。也就是说，它不是免费午餐，而是“用更多推理回合换更可靠交付”。</p>
  </section>

  <section class="section" id="limitations">
    <h2>8. 局限性与问题</h2>
    <div class="grid-2">
      <div class="card red"><h3>成本更高</h3><p>2.9-9.2 倍 token 成本会限制低价值任务。适合用在“交付失败很贵”的场景，比如报表、工程图、前端页面、硬件逻辑。</p></div>
      <div class="card red"><h3>依赖好裁判</h3><p>如果工具链只能判断“能不能跑”，却不能判断“是否好看、是否符合用户真实意图”，PairCoder 的收益会减弱。</p></div>
      <div class="card red"><h3>安全边界复杂</h3><p>既然要运行模型写出的代码，就必须有沙箱、权限控制、依赖隔离和审计日志，否则会把代码执行风险带进生产系统。</p></div>
      <div class="card red"><h3>不是通用智能</h3><p>它提升的是“可验证任务”的可靠性，不等于模型真正理解设计美学、产品目标或隐含业务约束。</p></div>
    </div>
  </section>

  <section class="section" id="industry">
    <h2>9. 产业影响分析</h2>
    <p>这篇论文对产品和投资的信号很直接：AI Agent 真正值钱的地方，往往不是“说得像专家”，而是“能进入带验收标准的工作流”。</p>
    <table>
      <tr><th>谁受益</th><th>可能变化</th></tr>
      <tr><td>AI 编程工具</td><td>从补全代码升级为“生成、运行、修复、交付 PR 或页面”的闭环。</td></tr>
      <tr><td>数据分析与 BI</td><td>图表和报告可以先由 AI 写代码，再用渲染与数据检查避免错误图。</td></tr>
      <tr><td>工业设计 / CAD / 3D 内容</td><td>只要能把设计表达为代码并用工具验证，就可能被 Agent 工作流加速。</td></tr>
      <tr><td>芯片与硬件设计</td><td>Verilog/RTL 这类天然有仿真器的领域，适合“AI 生成 + 工具验证”。</td></tr>
      <tr><td>创业公司</td><td>机会在于把特定行业的 oracle 做深：医学、法律、金融、工程都需要自己的裁判。</td></tr>
    </table>
    <p><b>竞争格局判断：</b>模型能力仍重要，但工具链、验证器、沙箱和行业基准会变成新的护城河。谁能把“外部世界的硬反馈”接进 Agent，谁就更接近生产级 AI。</p>
  </section>

  <section class="section" id="reading">
    <h2>10. 延伸阅读</h2>
    <ul class="refs">
      <li><a href="https://arxiv.org/abs/2607.01883">PairCoder++ arXiv 页面</a>：论文摘要、PDF、HTML 与提交记录。</li>
      <li><a href="https://yisuanwang.github.io/PairCoder/">PairCoder++ 项目页</a>：交互式结果表、方法图和跨模型案例。</li>
      <li><a href="https://github.com/yisuanwang/PairCoder">PairCoder GitHub 仓库</a>：代码、复现实验目录、README 与许可证。</li>
      <li><a href="https://aclanthology.org/2026.findings-acl.149/">原始 PairCoder ACL 2026 Findings</a>：更聚焦传统代码生成的双 Agent 结对编程版本。</li>
      <li>相关方向：Tool-augmented agents、self-refinement、program synthesis、visual artifact generation、hardware code generation。</li>
    </ul>
  </section>

  <section class="section" id="citations">
    <h2>11. 引用来源</h2>
    <ol class="refs">
      <li>arXiv: PairCoder++，提交日期、作者、摘要、ACL 2026 接收信息、实验摘要和 DOI 信息。<a href="https://arxiv.org/abs/2607.01883">https://arxiv.org/abs/2607.01883</a></li>
      <li>项目页：机构、核心指标、方法三组件、完整多模态结果表和图示。<a href="https://yisuanwang.github.io/PairCoder/">https://yisuanwang.github.io/PairCoder/</a></li>
      <li>GitHub 仓库：README、复现目录、实现范围、许可和 PairCoder / PairCoder++ 区分。<a href="https://github.com/yisuanwang/PairCoder">https://github.com/yisuanwang/PairCoder</a></li>
      <li>本地保存材料：PDF、HTML、纯文本、项目页和 README 已保存到 <code>/Users/mac/Desktop/AI论文解读/reports/source_papers/</code>。</li>
    </ol>
  </section>
</main>
</body>
</html>
"""


class Validator(html_parser.HTMLParser):
    pass


REPORT.write_text(html, encoding="utf-8")
EMAIL_BODY.write_text(email_body, encoding="utf-8")
EMAIL_SUBJECT.write_text(subject + "\n", encoding="utf-8")
SOURCES.write_text(sources_md, encoding="utf-8")
Validator().feed(html)

section_count = html.count("<section")
table_count = html.count("<table")
svg_count = html.count("<svg")
if section_count < 11 or table_count < 4 or svg_count < 1:
    raise SystemExit(f"Validation failed: sections={section_count}, tables={table_count}, svg={svg_count}")
if "<script" in html.lower():
    raise SystemExit("Validation failed: script tag found")

print(f"Wrote {REPORT}")
print(f"sections={section_count} tables={table_count} svg={svg_count} bytes={REPORT.stat().st_size}")
