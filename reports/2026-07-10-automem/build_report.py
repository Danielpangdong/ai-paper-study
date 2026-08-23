from __future__ import annotations

import base64
from pathlib import Path
from string import Template

BASE = Path(__file__).resolve().parent
COVER = BASE / "automem-cover.jpg"
REPORT = BASE / "AI-Daily-Paper-AutoMem-2026-07-10.html"
EMAIL_BODY = BASE / "email-body.md"
SOURCES = BASE / "sources.md"

cover_data = "data:image/jpeg;base64," + base64.b64encode(COVER.read_bytes()).decode("ascii")

html = Template(r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI每日论文精选：AutoMem - 把记忆变成 AI Agent 可训练的能力</title>
  <style>
    :root {
      color-scheme: light dark;
      --ink: #111827;
      --muted: #667085;
      --soft: #f5f7fb;
      --line: #d9e0ea;
      --card: #ffffff;
      --brand: #0f766e;
      --brand-2: #2563eb;
      --accent: #f59e0b;
      --danger: #b42318;
      --dark: #0b1220;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: #eef2f6;
      color: var(--ink);
      line-height: 1.72;
    }
    a { color: #0b63ce; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .page { max-width: 1040px; margin: 0 auto; background: #fff; box-shadow: 0 20px 80px rgba(15, 23, 42, .12); }
    .hero {
      position: relative;
      min-height: 520px;
      padding: 42px 38px;
      color: #fff;
      display: flex;
      align-items: flex-end;
      overflow: hidden;
      background: #07111f;
    }
    .hero img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .72; }
    .hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(7,17,31,.15), rgba(7,17,31,.92)); }
    .hero-content { position: relative; z-index: 1; max-width: 820px; }
    .eyebrow { display: inline-flex; gap: 8px; align-items: center; padding: 6px 10px; border: 1px solid rgba(255,255,255,.35); border-radius: 999px; background: rgba(255,255,255,.1); font-size: 13px; letter-spacing: 0; }
    h1 { margin: 18px 0 12px; font-size: 44px; line-height: 1.12; letter-spacing: 0; }
    .subtitle { font-size: 21px; max-width: 760px; color: rgba(255,255,255,.9); margin: 0 0 22px; }
    .meta-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 20px; }
    .meta { border: 1px solid rgba(255,255,255,.22); background: rgba(255,255,255,.11); border-radius: 8px; padding: 10px 12px; backdrop-filter: blur(8px); }
    .meta b { display: block; color: #fff; font-size: 13px; }
    .meta span { color: rgba(255,255,255,.84); font-size: 13px; }
    main { padding: 34px 38px 52px; }
    section { margin: 34px 0; }
    h2 { font-size: 26px; line-height: 1.25; margin: 0 0 16px; letter-spacing: 0; }
    h3 { font-size: 18px; margin: 22px 0 8px; }
    p { margin: 0 0 14px; }
    .lead { font-size: 19px; line-height: 1.75; color: #243044; }
    .grid { display: grid; gap: 16px; }
    .grid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .card { border: 1px solid var(--line); border-radius: 8px; background: var(--card); padding: 18px; }
    .card.soft { background: var(--soft); }
    .card.dark { background: #0e1728; color: #e5edf8; border-color: #1e2d47; }
    .card h3 { margin-top: 0; }
    .tag { display: inline-block; font-size: 12px; font-weight: 700; color: #0f766e; background: #dff7f3; border-radius: 999px; padding: 4px 9px; margin-bottom: 10px; }
    .quote { border-left: 4px solid var(--brand); padding: 14px 18px; background: #f0fbf9; border-radius: 0 8px 8px 0; font-size: 20px; font-weight: 700; }
    table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 14px; }
    th, td { border: 1px solid #d7dee8; padding: 10px 12px; vertical-align: top; }
    th { background: #eef4fb; text-align: left; }
    tr.highlight td { background: #f0fbf9; font-weight: 700; }
    .note { font-size: 13px; color: var(--muted); }
    .warn { border-left: 4px solid var(--danger); background: #fff6f4; }
    .figure { margin: 18px 0; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; }
    .figure-title { padding: 12px 16px; background: #0e1728; color: #fff; font-weight: 700; }
    .figure-body { padding: 16px; overflow-x: auto; }
    .caption { padding: 0 16px 16px; color: var(--muted); font-size: 13px; }
    svg { max-width: 100%; height: auto; }
    .term { display: grid; grid-template-columns: 160px 1fr 1fr; gap: 0; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; margin-bottom: 10px; }
    .term > div { padding: 12px; border-right: 1px solid var(--line); }
    .term > div:last-child { border-right: 0; }
    .term .name { background: #0e1728; color: #fff; font-weight: 700; }
    .small { font-size: 13px; color: var(--muted); }
    .footer { padding: 26px 38px; background: #0b1220; color: #cbd5e1; font-size: 13px; }
    @media (max-width: 760px) {
      .hero { min-height: 560px; padding: 28px 22px; }
      h1 { font-size: 32px; }
      .subtitle { font-size: 18px; }
      main { padding: 26px 22px 40px; }
      .meta-grid, .grid.two, .grid.three { grid-template-columns: 1fr; }
      .term { grid-template-columns: 1fr; }
      .term > div { border-right: 0; border-bottom: 1px solid var(--line); }
      .term > div:last-child { border-bottom: 0; }
      table { font-size: 13px; }
      th, td { padding: 8px; }
    }
  </style>
</head>
<body>
<div class="page">
  <header class="hero">
    <img src="$cover_data" alt="AI agent organizing memory files">
    <div class="hero-content">
      <div class="eyebrow">AI每日论文精选 · 2026-07-10 · Agent Memory</div>
      <h1>AutoMem：把“会记东西”变成 AI Agent 可以训练的能力</h1>
      <p class="subtitle">一篇来自 Stanford 的论文提醒我们：未来 agent 的差距，可能不只来自模型有多大，而来自它是否真的会做笔记、会查笔记、会整理自己的经验。</p>
      <div class="meta-grid">
        <div class="meta"><b>论文</b><span>AutoMem: Automated Learning of Memory as a Cognitive Skill</span></div>
        <div class="meta"><b>作者</b><span>Shengguang Wu, Hao Zhu, Yuhui Zhang, Xiaohan Wang, Serena Yeung-Levy</span></div>
        <div class="meta"><b>机构</b><span>Stanford University</span></div>
        <div class="meta"><b>平台</b><span>arXiv:2607.01224v1 · 2026-07-01</span></div>
      </div>
    </div>
  </header>

  <main>
    <section>
      <div class="grid two">
        <div class="card soft">
          <span class="tag">论文信息卡</span>
          <p><b>论文链接：</b><a href="https://arxiv.org/abs/2607.01224">https://arxiv.org/abs/2607.01224</a></p>
          <p><b>项目页：</b><a href="https://autolearnmem.github.io/">https://autolearnmem.github.io/</a></p>
          <p><b>代码：</b><a href="https://github.com/autoLearnMem/AutoMem">autoLearnMem/AutoMem</a></p>
          <p><b>评测任务：</b>Crafter、MiniHack、NetHack，都是长时间、多步骤、需要记录地图/物品/策略的游戏环境。</p>
        </div>
        <div class="card dark">
          <span class="tag">一句话讲透论文</span>
          <p class="lead">AutoMem 不是给 AI 装一个更大的“记事本”，而是训练 AI 学会像靠谱助理一样：什么值得记、什么时候查、怎样整理。</p>
        </div>
      </div>
    </section>

    <section>
      <h2>为什么今天选它？</h2>
      <p class="lead">过去一年，agent 的讨论很容易陷入两个方向：更大的上下文窗口，或者更复杂的工具调用。AutoMem 的价值在于它换了一个角度：真正长时间工作的 agent，不只是“看得更多”，而是要学会管理自己的经验。</p>
      <div class="grid three">
        <div class="card">
          <h3>1. 认知突破</h3>
          <p>论文借用了 cognitive science 里的 <b>metamemory</b>：人类不只是有记忆，还会判断“这件事要不要记、要怎么记”。这给 agent 记忆研究提供了更清楚的框架。</p>
        </div>
        <div class="card">
          <h3>2. 工程突破</h3>
          <p>它把文件读写、搜索、追加这些记忆操作，放进 agent 的动作空间里。也就是说，查资料和走一步棋一样，都是模型可选择、可追踪、可优化的动作。</p>
        </div>
        <div class="card">
          <h3>3. 产业含义</h3>
          <p>如果记忆管理能单独训练，小模型在长任务上的短板可能被明显补上。对企业 agent、代码 agent、个人助理、游戏 NPC 都很关键。</p>
        </div>
      </div>
    </section>

    <section>
      <h2>核心贡献拆解</h2>
      <table>
        <thead>
          <tr><th>问题</th><th>旧方法常见做法</th><th>AutoMem 的做法</th><th>为什么更好</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>长任务会遗忘</td>
            <td>把最近若干步塞进上下文，或用固定摘要/向量库。</td>
            <td>让 agent 自己决定读、写、查、整理记忆文件。</td>
            <td>记忆不再是外部插件，而是 agent 行为的一部分。</td>
          </tr>
          <tr>
            <td>记忆结构难设计</td>
            <td>工程师手写 prompt、文件格式、检索规则。</td>
            <td>外层循环 #1 让强模型审查完整轨迹，自动修改脚手架。</td>
            <td>像代码审查一样，从失败轨迹里找出“笔记系统”的设计问题。</td>
          </tr>
          <tr>
            <td>模型不会熟练使用记忆</td>
            <td>只改系统提示，期待模型自然学会。</td>
            <td>外层循环 #2 从 agent 自己的好记忆决策中筛数据，训练 memory specialist。</td>
            <td>把“先查再写、少写废话”变成模型内部习惯。</td>
          </tr>
          <tr>
            <td>训练可能损坏任务能力</td>
            <td>直接微调整个 agent。</td>
            <td>只训练专门处理 LOG/PLAN 记忆部分的模型，执行世界动作的模型保持不变。</td>
            <td>把“记忆能力”和“玩游戏/执行任务能力”分开优化，降低副作用。</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section>
      <h2>工作原理：像训练一名会做笔记的实习生</h2>
      <p>可以把 agent 想象成一个新来的实习生，要在复杂迷宫里完成任务。普通做法是不断提醒它：“记得看前面的记录。”AutoMem 更像是在建立一套训练制度：</p>
      <div class="figure">
        <div class="figure-title">图 1：AutoMem 的两层训练循环</div>
        <div class="figure-body">
          <svg viewBox="0 0 980 430" role="img" aria-label="AutoMem workflow diagram">
            <defs>
              <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"></path>
              </marker>
              <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#0f172a" flood-opacity=".12"/>
              </filter>
            </defs>
            <rect x="20" y="24" width="940" height="382" rx="18" fill="#f6f8fb" stroke="#d9e0ea"/>
            <rect x="70" y="150" width="220" height="118" rx="12" fill="#0e1728" filter="url(#shadow)"/>
            <text x="180" y="186" text-anchor="middle" fill="#fff" font-size="20" font-weight="700">内层 Agent</text>
            <text x="180" y="218" text-anchor="middle" fill="#cbd5e1" font-size="14">一边行动，一边管理文件记忆</text>
            <text x="180" y="244" text-anchor="middle" fill="#8ee8dc" font-size="14">READ · SEARCH · APPEND · UPSERT_MAP</text>

            <rect x="384" y="58" width="240" height="118" rx="12" fill="#fff" stroke="#cbd5e1" filter="url(#shadow)"/>
            <text x="504" y="95" text-anchor="middle" fill="#0e1728" font-size="19" font-weight="700">外层循环 #1</text>
            <text x="504" y="125" text-anchor="middle" fill="#475467" font-size="14">强模型审查完整轨迹</text>
            <text x="504" y="150" text-anchor="middle" fill="#0f766e" font-size="14">改 prompt / 文件结构 / 动作词表</text>

            <rect x="384" y="248" width="240" height="118" rx="12" fill="#fff" stroke="#cbd5e1" filter="url(#shadow)"/>
            <text x="504" y="285" text-anchor="middle" fill="#0e1728" font-size="19" font-weight="700">外层循环 #2</text>
            <text x="504" y="315" text-anchor="middle" fill="#475467" font-size="14">挑出好的记忆决策</text>
            <text x="504" y="340" text-anchor="middle" fill="#0f766e" font-size="14">训练 memory specialist</text>

            <rect x="714" y="150" width="200" height="118" rx="12" fill="#ecfeff" stroke="#67e8f9" filter="url(#shadow)"/>
            <text x="814" y="186" text-anchor="middle" fill="#0e1728" font-size="19" font-weight="700">更会记的 Agent</text>
            <text x="814" y="218" text-anchor="middle" fill="#475467" font-size="14">少写废话，先查再写</text>
            <text x="814" y="244" text-anchor="middle" fill="#2563eb" font-size="14">长任务表现提升 2-4 倍</text>

            <path d="M290 190 C330 150 340 118 380 118" fill="none" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow)"/>
            <path d="M624 118 C670 118 686 170 714 190" fill="none" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow)"/>
            <path d="M290 232 C330 282 340 307 380 307" fill="none" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow)"/>
            <path d="M624 307 C670 307 686 245 714 228" fill="none" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow)"/>
            <path d="M180 268 C180 370 810 392 814 270" fill="none" stroke="#f59e0b" stroke-width="3" stroke-dasharray="8 8" marker-end="url(#arrow)"/>
            <text x="490" y="393" text-anchor="middle" fill="#92400e" font-size="14">新的 agent 继续产生轨迹，进入下一轮审查与训练</text>
          </svg>
        </div>
        <div class="caption">白话版：先让高级导师检查“笔记系统设计”哪里错了，再把优秀笔记行为挑出来训练成习惯。</div>
      </div>

      <div class="grid two">
        <div class="card">
          <h3>LOG：这件事值得记吗？</h3>
          <p>每一步结束后，agent 会问自己：刚才发生了什么？有没有新地图、新物品、新危险、新策略？如果值得，就写入或更新记忆文件。</p>
        </div>
        <div class="card">
          <h3>PLAN：行动前要查什么？</h3>
          <p>准备下一步动作前，agent 先搜索已有记忆，像人类出门前查待办、地图、上次会议纪要，而不是凭感觉乱走。</p>
        </div>
      </div>
    </section>

    <section>
      <h2>关键术语解释</h2>
      <div class="term"><div class="name">Metamemory</div><div><b>专业解释：</b>认知科学中关于“人如何监控和调节自己的记忆”的能力。</div><div><b>白话解释：</b>不只是记性好，而是知道什么该记、什么时候该翻笔记。</div></div>
      <div class="term"><div class="name">Scaffold</div><div><b>专业解释：</b>支撑 agent 行为的提示词、代码、文件 schema、动作接口等外部结构。</div><div><b>白话解释：</b>给实习生用的工作手册、表格模板和操作规范。</div></div>
      <div class="term"><div class="name">Memory Specialist</div><div><b>专业解释：</b>专门微调来处理记忆读写与规划咨询的模型组件。</div><div><b>白话解释：</b>一个专职“秘书脑”，负责查笔记、整理笔记，不负责真正走棋。</div></div>
      <div class="term"><div class="name">LoRA</div><div><b>专业解释：</b>低秩适配微调方法，用少量参数改变模型行为。</div><div><b>白话解释：</b>不是重造大脑，而是给模型装一套可替换的小插件。</div></div>
      <div class="term"><div class="name">Long-horizon task</div><div><b>专业解释：</b>需要大量连续步骤、早期决策会影响很久之后结果的任务。</div><div><b>白话解释：</b>不是答一道题，而是玩一局几千步的生存游戏，前面忘了哪里有矿，后面就会迷路。</div></div>
    </section>

    <section>
      <h2>实验结果怎么读？</h2>
      <p>论文用 Qwen2.5-32B-Instruct 做基础模型，只优化“记忆”，不改它执行游戏动作的能力。结果在三个长任务环境里，表现约提升 2-4 倍。</p>
      <table>
        <thead>
          <tr><th>方法 / 模型</th><th>Crafter</th><th>MiniHack</th><th>NetHack</th><th>怎么理解</th></tr>
        </thead>
        <tbody>
          <tr><td>Qwen2.5-32B + 文件记忆 v0</td><td>25.00</td><td>7.50</td><td>0.42</td><td>有笔记本，但还不会好好用。</td></tr>
          <tr><td>+ scaffold optimization</td><td>47.27</td><td>27.50</td><td>1.57</td><td>导师改了笔记系统，地图、规则、检索方式更合理。</td></tr>
          <tr class="highlight"><td>+ memory training</td><td>51.36</td><td>30.00</td><td>1.85</td><td>模型开始内化“先查再写”的习惯。</td></tr>
          <tr><td>Claude Opus 4.5</td><td>49.5</td><td>27.5</td><td>2.0</td><td>在这些任务上，AutoMem 的 32B 开源模型接近前沿闭源系统。</td></tr>
          <tr><td>Qwen2.5-72B</td><td>27.3</td><td>5.0</td><td>0.3</td><td>单纯变大，不一定比“会记忆”更有效。</td></tr>
        </tbody>
      </table>
      <p class="note">指标是 progression rate，论文报告为均值 ± 标准误。NetHack 数值绝对值低，因为环境极难，完整任务可达 10^4-10^5 步。</p>

      <div class="figure">
        <div class="figure-title">图 2：关键结果的直觉化对比</div>
        <div class="figure-body">
          <svg viewBox="0 0 920 330" role="img" aria-label="AutoMem result bars">
            <rect width="920" height="330" fill="#fff"/>
            <line x1="120" y1="270" x2="860" y2="270" stroke="#cbd5e1"/>
            <text x="120" y="295" font-size="13" fill="#667085">0</text>
            <text x="360" y="295" font-size="13" fill="#667085">20</text>
            <text x="600" y="295" font-size="13" fill="#667085">40</text>
            <text x="830" y="295" font-size="13" fill="#667085">60</text>
            <g font-size="15" font-weight="700" fill="#0e1728">
              <text x="40" y="76">Crafter</text>
              <text x="40" y="156">MiniHack</text>
              <text x="40" y="236">NetHack</text>
            </g>
            <g>
              <rect x="120" y="48" width="300" height="22" fill="#94a3b8"/><text x="430" y="66" font-size="13">v0 25.0</text>
              <rect x="120" y="78" width="616" height="22" fill="#0f766e"/><text x="746" y="96" font-size="13">AutoMem 51.36</text>
              <rect x="120" y="128" width="90" height="22" fill="#94a3b8"/><text x="220" y="146" font-size="13">v0 7.5</text>
              <rect x="120" y="158" width="360" height="22" fill="#0f766e"/><text x="490" y="176" font-size="13">AutoMem 30.0</text>
              <rect x="120" y="208" width="5" height="22" fill="#94a3b8"/><text x="136" y="226" font-size="13">v0 0.42</text>
              <rect x="120" y="238" width="22" height="22" fill="#0f766e"/><text x="154" y="256" font-size="13">AutoMem 1.85</text>
            </g>
            <text x="120" y="22" font-size="14" fill="#667085">Progression rate (%)：绿色是完整 AutoMem，灰色是初始文件记忆 agent</text>
          </svg>
        </div>
        <div class="caption">真正要看的不是 NetHack 绝对分数多高，而是“只训练记忆管理”竟然能带来大幅提升。</div>
      </div>

      <div class="card soft">
        <h3>一个很有意思的行为变化</h3>
        <p>训练后的 memory specialist 在 LOG 阶段更少“盲目写入”，更倾向于先搜索已有记忆再决定是否追加。论文报告：Crafter 的写入/搜索比从 0.84 降到 0.39，MiniHack 从 2.89 降到 0.82，NetHack 从 4.66 降到 1.31。</p>
        <p>这就像一个新人从“会议上听到什么都新建一个文档”，进化到“先查旧文档，必要时更新同一份记录”。</p>
      </div>
    </section>

    <section>
      <h2>局限性与风险提示</h2>
      <div class="grid two">
        <div class="card warn">
          <h3>论文自己承认的限制</h3>
          <p>目前记忆是 episodic：每个 episode 开始时文件系统重新开始，尚未证明跨 episode 的长期持久记忆。</p>
          <p>实验仍集中在游戏环境。游戏适合研究长任务记忆，但距离真实企业工作流还有迁移距离。</p>
          <p>三类游戏分别训练了不同 scaffold 和 specialist，一个通用记忆系统是否可跨任务共享仍未知。</p>
        </div>
        <div class="card warn">
          <h3>产业落地风险</h3>
          <p><b>成本：</b>外层循环依赖强模型审查完整轨迹，还要做 LoRA 训练，不是轻量插件。</p>
          <p><b>安全：</b>agent 如果能写长期记忆，也可能把错误、敏感信息或攻击痕迹固化下来。</p>
          <p><b>评测：</b>在游戏里“记得地图”很清楚，在办公、医疗、金融场景里“什么值得记”更难定义。</p>
        </div>
      </div>
    </section>

    <section>
      <h2>产业影响分析</h2>
      <table>
        <thead><tr><th>角色</th><th>可能受益</th><th>可能被冲击</th></tr></thead>
        <tbody>
          <tr><td>Agent 平台</td><td>可以把记忆从“外挂功能”升级成可训练模块，提升长任务可靠性。</td><td>只做简单向量库/聊天记录召回的记忆产品会被重新定义。</td></tr>
          <tr><td>企业 AI 应用</td><td>客户支持、代码维护、销售跟进、研究助理都需要跨天、跨项目记忆。</td><td>需要更严格的数据权限、遗忘机制、审计与回滚。</td></tr>
          <tr><td>开源模型</td><td>论文暗示：在长任务上，记忆训练可能比单纯扩大模型更高杠杆。</td><td>如果需要昂贵 meta-LLM 审查轨迹，小团队复现门槛仍高。</td></tr>
          <tr><td>产品经理</td><td>可以把“记忆”设计成用户可见、可编辑、可验证的产品界面。</td><td>黑箱记忆会造成信任问题：用户不知道 AI 记了什么、为什么这么做。</td></tr>
        </tbody>
      </table>
    </section>

    <section>
      <h2>如果你只记住三件事</h2>
      <div class="quote">第一，agent 的记忆不是一个数据库问题，而是一个行为训练问题。</div>
      <div class="quote">第二，会查、会写、会整理，比“上下文更长”更接近人类工作方式。</div>
      <div class="quote">第三，未来 AI 助理的核心竞争力，可能是它能不能把经验变成可用的工作记忆。</div>
    </section>

    <section>
      <h2>延伸阅读</h2>
      <ul>
        <li>原论文：<a href="https://arxiv.org/abs/2607.01224">AutoMem: Automated Learning of Memory as a Cognitive Skill</a></li>
        <li>项目页：<a href="https://autolearnmem.github.io/">AutoMem project page</a></li>
        <li>代码仓库：<a href="https://github.com/autoLearnMem/AutoMem">autoLearnMem/AutoMem</a></li>
        <li>Hugging Face Papers：<a href="https://huggingface.co/papers/2607.01224">AutoMem paper page</a></li>
        <li>相关方向：BALROG long-horizon agent evaluation；LoRA；RAG；Generative Agents；Self-Compacting Language Model Agents。</li>
      </ul>
    </section>

    <section>
      <h2>引用来源</h2>
      <ol>
        <li>Wu, Shengguang et al. <i>AutoMem: Automated Learning of Memory as a Cognitive Skill</i>. arXiv:2607.01224v1, 2026-07-01.</li>
        <li>AutoMem official project page, Stanford University, retrieved 2026-07-10.</li>
        <li>autoLearnMem/AutoMem GitHub repository README, retrieved 2026-07-10.</li>
        <li>Hugging Face Papers page for arXiv:2607.01224, retrieved 2026-07-10.</li>
        <li>Related paper references cited in AutoMem: BALROG, Crafter, MiniHack, NetHack Learning Environment, LoRA, RAG, Generative Agents.</li>
      </ol>
      <p class="small">本文为中文研究解读，图示为重新设计的解释性图，不是论文原图截图。数值以论文和项目页公开信息为准。</p>
    </section>
  </main>
  <footer class="footer">
    AI每日论文精选 · 本期主题：AutoMem 与可训练的 Agent 记忆 · 生成时间：2026-07-10 Asia/Shanghai
  </footer>
</div>
</body>
</html>
""").substitute(cover_data=cover_data)

REPORT.write_text(html, encoding="utf-8")

EMAIL_BODY.write_text(
    """今天精选的论文来自 Stanford：AutoMem: Automated Learning of Memory as a Cognitive Skill。

一句话推荐理由：
它把“AI 会不会记东西、什么时候查、怎样整理经验”从外挂功能变成可训练能力，可能是长任务 Agent 走向真实生产力的关键一步。

附件为中文深度拆解 HTML 报告，包含核心贡献、机制图、实验结果、局限性与产业影响分析，适合非技术读者阅读。
""",
    encoding="utf-8",
)

SOURCES.write_text(
    """# Sources

- arXiv abstract: https://arxiv.org/abs/2607.01224
- arXiv HTML: https://arxiv.org/html/2607.01224v1
- PDF: https://arxiv.org/pdf/2607.01224
- Project page: https://autolearnmem.github.io/
- GitHub: https://github.com/autoLearnMem/AutoMem
- Hugging Face Papers: https://huggingface.co/papers/2607.01224

Local source files are stored under `reports/2026-07-10-automem/sources/`.
""",
    encoding="utf-8",
)

print(REPORT)
