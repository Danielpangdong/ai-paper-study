from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HERO = ROOT / "orca-hero.png"
OUT = ROOT / "AI-Daily-Paper-Orca-2026-07-02.html"


def image_data_uri(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


html = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>AI每日论文精选｜Orca: The World is in Your Mind</title>
  <style>
    :root {
      --bg: #f5f3ef;
      --paper: #fffefa;
      --ink: #171717;
      --muted: #66645e;
      --line: #ded9cf;
      --accent: #0f766e;
      --accent2: #bc6c25;
      --deep: #10231f;
      --soft: #e9f1ee;
      --warn: #8a3f12;
      --shadow: 0 20px 60px rgba(30, 24, 16, .10);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
      line-height: 1.72;
      letter-spacing: 0;
    }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .wrap { max-width: 1080px; margin: 0 auto; padding: 28px 18px 64px; }
    .hero {
      overflow: hidden;
      border: 1px solid rgba(255,255,255,.5);
      background: #0e1517;
      color: white;
      box-shadow: var(--shadow);
      border-radius: 8px;
    }
    .hero-img {
      min-height: 340px;
      background-image: linear-gradient(90deg, rgba(4,10,12,.88), rgba(4,10,12,.56), rgba(4,10,12,.18)), url("{{HERO_URI}}");
      background-size: cover;
      background-position: center;
      padding: 54px 44px;
      display: grid;
      align-items: end;
    }
    .eyebrow {
      display: inline-block;
      width: fit-content;
      padding: 4px 10px;
      border: 1px solid rgba(255,255,255,.35);
      border-radius: 999px;
      color: rgba(255,255,255,.86);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
    }
    h1 {
      max-width: 790px;
      margin: 18px 0 10px;
      font-size: clamp(36px, 6vw, 72px);
      line-height: 1.02;
      letter-spacing: 0;
    }
    .subtitle { max-width: 760px; color: rgba(255,255,255,.86); font-size: 18px; margin: 0; }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 1px;
      background: rgba(255,255,255,.12);
      border-top: 1px solid rgba(255,255,255,.16);
    }
    .meta-cell { padding: 18px; background: rgba(8,18,19,.84); }
    .meta-cell b { display: block; font-size: 12px; color: rgba(255,255,255,.55); margin-bottom: 6px; }
    .meta-cell span { font-weight: 650; }
    .section { margin-top: 22px; padding: 28px; background: var(--paper); border: 1px solid var(--line); border-radius: 8px; box-shadow: 0 8px 24px rgba(20,18,14,.04); }
    h2 { margin: 0 0 14px; font-size: 28px; line-height: 1.22; letter-spacing: 0; }
    h3 { margin: 20px 0 8px; font-size: 18px; letter-spacing: 0; }
    p { margin: 10px 0; }
    .lead { font-size: 19px; color: #2b2925; }
    .one-line {
      font-size: 24px;
      line-height: 1.35;
      padding: 22px 24px;
      border-left: 5px solid var(--accent);
      background: var(--soft);
      border-radius: 6px;
      font-weight: 750;
    }
    .cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: 16px; }
    .card { border: 1px solid var(--line); border-radius: 8px; padding: 16px; background: #fff; }
    .card b { display: block; margin-bottom: 6px; color: var(--deep); }
    .kpi { font-size: 30px; line-height: 1; font-weight: 800; color: var(--accent); margin: 8px 0 4px; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; background: white; border: 1px solid var(--line); }
    th, td { padding: 11px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
    th { background: #f0eee8; font-size: 12px; text-transform: uppercase; color: #4b4842; }
    tr:last-child td { border-bottom: 0; }
    .note { color: var(--muted); font-size: 13px; }
    .pill { display: inline-block; padding: 3px 8px; border-radius: 999px; background: #e3efeb; color: #12584f; font-size: 12px; font-weight: 700; }
    .diagram {
      margin: 18px 0;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
      background: linear-gradient(180deg, #ffffff, #f7f5ef);
    }
    .diagram svg { display: block; width: 100%; height: auto; }
    .term-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    .term { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 14px; }
    .term strong { color: var(--accent); }
    .risk { border-color: #e0b998; background: #fff7ef; }
    .risk b { color: var(--warn); }
    .source-list li { margin: 8px 0; }
    .footer { color: var(--muted); font-size: 13px; text-align: center; margin-top: 30px; }
    @media (max-width: 760px) {
      .wrap { padding: 12px 10px 36px; }
      .hero-img { min-height: 420px; padding: 34px 22px; }
      h1 { font-size: 39px; }
      .subtitle { font-size: 16px; }
      .meta-grid, .cards, .term-grid { grid-template-columns: 1fr; }
      .section { padding: 20px 16px; }
      table { font-size: 13px; }
      th, td { padding: 9px 8px; }
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #111312;
        --paper: #191c1a;
        --ink: #f3f1eb;
        --muted: #aaa49a;
        --line: #343832;
        --soft: #172520;
      }
      .card, .term, table { background: #20231f; }
      th { background: #272a25; color: #d7d0c3; }
      .lead { color: #e6e1d8; }
      .risk { background: #2a2119; }
      .diagram { background: #1c1f1c; }
    }
  </style>
</head>
<body>
  <main class="wrap">
    <header class="hero">
      <div class="hero-img">
        <div>
          <span class="eyebrow">AI Daily Paper · 2026-07-02</span>
          <h1>Orca：让 AI 不只预测下一个词，而是预测“世界下一步会怎样”</h1>
          <p class="subtitle">今日精选论文：<i>Orca: The World is in Your Mind</i>。它把语言理解、图像预测和机器人动作放进同一个“世界状态”框架里，是通往通用世界基础模型的一次重要探索。</p>
        </div>
      </div>
      <div class="meta-grid">
        <div class="meta-cell"><b>论文</b><span>Orca: The World is in Your Mind</span></div>
        <div class="meta-cell"><b>团队</b><span>Orca Team · BAAI</span></div>
        <div class="meta-cell"><b>时间</b><span>2026-06-29 发布，2026-06-30 v2</span></div>
        <div class="meta-cell"><b>平台</b><span>arXiv cs.CV · HF Papers</span></div>
      </div>
    </header>

    <section class="section">
      <h2>1. 标题区</h2>
      <table>
        <tr><th>项目</th><th>信息</th></tr>
        <tr><td>英文标题</td><td><b>Orca: The World is in Your Mind</b></td></tr>
        <tr><td>中文标题</td><td>Orca：世界就在模型的脑海里</td></tr>
        <tr><td>作者</td><td>Yihao Wang、Yuheng Ji、Mingyu Cao、Yanqing Shen、Runze Xiao 等 57 位作者；署名 Orca Team</td></tr>
        <tr><td>机构</td><td>Beijing Academy of Artificial Intelligence（北京智源人工智能研究院）</td></tr>
        <tr><td>发布时间</td><td>arXiv 首次发布 2026-06-29；v2 更新 2026-06-30</td></tr>
        <tr><td>论文链接</td><td><a href="https://arxiv.org/abs/2606.30534">https://arxiv.org/abs/2606.30534</a></td></tr>
        <tr><td>项目页</td><td><a href="https://orca-wm.github.io/">https://orca-wm.github.io/</a></td></tr>
      </table>
    </section>

    <section class="section">
      <h2>2. 为什么今天选它？</h2>
      <p class="lead">过去几年，AI 的主线是三条分开的路：大语言模型预测下一个词，视频生成模型预测下一帧，机器人模型预测下一个动作。Orca 试图把这三件事合并成一个更大的问题：预测世界的下一个状态。</p>
      <div class="cards">
        <div class="card"><b>行业意义</b><p>如果模型能先形成“世界状态”，再读出文字、图像或动作，那么未来的 Agent 和机器人就不必为每个任务重新造一套脑子。</p></div>
        <div class="card"><b>技术突破</b><p>论文提出 Next-State-Prediction：不是只补一句话、补一帧画面、补一个动作，而是学习“现在发生了什么，接下来可能变成什么”。</p></div>
        <div class="card"><b>长期价值</b><p>这可能是世界模型从“会生成视频”走向“能支撑理解、预测、行动”的关键分界线。</p></div>
      </div>
      <p>我没有选择它仅仅因为新，而是因为它把一个核心判断说清楚了：通用智能也许不该从“语言聊天”定义，而应从“状态建模”定义。对产品经理和投资人来说，这意味着未来的 AI 产品竞争，可能从模型能说什么，转向模型是否真正理解环境变化、能否低成本迁移到新任务。</p>
    </section>

    <section class="section">
      <h2>3. 一句话讲透论文</h2>
      <div class="one-line">Orca 想让 AI 像人一样先在脑中形成“世界模型”，再根据需要把这个内部世界翻译成文字、图片或机器人动作。</div>
    </section>

    <section class="section">
      <h2>4. 核心贡献拆解</h2>
      <table>
        <tr><th>贡献</th><th>它做了什么</th><th>为什么更重要</th></tr>
        <tr>
          <td><span class="pill">新目标</span></td>
          <td>把训练中心从 next-token / next-frame / next-action 转向 next-state prediction。</td>
          <td>像教孩子理解“水杯被推会倒”，而不是只背“水杯”这个词或生成一张水杯图。</td>
        </tr>
        <tr>
          <td><span class="pill">双学习机制</span></td>
          <td>无意识学习从连续视频里学自然变化；有意识学习从事件描述和 VQA 里学有意义的变化。</td>
          <td>前者像每天观察世界，后者像老师解释“为什么这一步发生”。两者合起来才像真正的经验。</td>
        </tr>
        <tr>
          <td><span class="pill">统一潜空间</span></td>
          <td>预训练后冻结 Orca 主干，只训练轻量 readout，把潜空间读成文本、图像或动作。</td>
          <td>这证明“内部世界状态”不是漂亮概念，而是能被不同任务复用的接口。</td>
        </tr>
        <tr>
          <td><span class="pill">大规模数据</span></td>
          <td>构建 125K 小时视频、160M 事件标注和 11.5M VQA 数据；本版只用其中约十分之一视频数据。</td>
          <td>说明这条路线还没吃完数据红利，模型规模和数据规模都有继续扩展空间。</td>
        </tr>
      </table>
    </section>

    <section class="section">
      <h2>5. 工作原理：把“看见”变成“懂得下一步”</h2>
      <p>可以把 Orca 想成一个学开车的新手。普通视频模型像是在练习“下一秒画面是什么”；普通语言模型像是在练习“下一句话是什么”；普通机器人模型像是在练习“下一次方向盘转多少”。Orca 更像是在问：我现在处在什么世界状态？如果前车刹车、路口变灯、行人移动，世界下一步会怎样？</p>
      <div class="diagram">
        <svg viewBox="0 0 980 470" role="img" aria-label="Orca 工作流程图">
          <defs>
            <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#0f766e"/></marker>
            <filter id="shadow"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity=".13"/></filter>
          </defs>
          <rect width="980" height="470" fill="#faf8f2"/>
          <text x="40" y="52" font-size="28" font-weight="800" fill="#16231f">Orca 的核心不是生成，而是先学“世界状态”</text>
          <g filter="url(#shadow)">
            <rect x="55" y="105" width="200" height="92" rx="8" fill="#fff" stroke="#ded9cf"/>
            <text x="82" y="142" font-size="20" font-weight="700" fill="#171717">连续视频</text>
            <text x="82" y="173" font-size="15" fill="#66645e">世界自然怎么变</text>
            <rect x="55" y="235" width="200" height="92" rx="8" fill="#fff" stroke="#ded9cf"/>
            <text x="82" y="272" font-size="20" font-weight="700" fill="#171717">事件 + 语言</text>
            <text x="82" y="303" font-size="15" fill="#66645e">人类说清楚为什么变</text>
          </g>
          <path d="M260 151 C330 151, 350 205, 420 205" stroke="#0f766e" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          <path d="M260 281 C330 281, 350 245, 420 245" stroke="#0f766e" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          <g filter="url(#shadow)">
            <rect x="420" y="135" width="190" height="170" rx="8" fill="#10231f"/>
            <text x="459" y="182" font-size="24" font-weight="800" fill="#fff">世界潜空间</text>
            <text x="452" y="218" font-size="15" fill="#cde5dc">像脑中的沙盘</text>
            <text x="452" y="246" font-size="15" fill="#cde5dc">保存状态、关系、变化</text>
          </g>
          <path d="M615 180 C690 142, 715 125, 770 125" stroke="#0f766e" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          <path d="M615 220 C690 220, 715 220, 770 220" stroke="#0f766e" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          <path d="M615 260 C690 304, 715 335, 770 335" stroke="#0f766e" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          <g filter="url(#shadow)">
            <rect x="770" y="84" width="150" height="82" rx="8" fill="#fff" stroke="#ded9cf"/>
            <text x="805" y="120" font-size="19" font-weight="800" fill="#171717">读成文字</text>
            <text x="798" y="146" font-size="14" fill="#66645e">回答、解释、推理</text>
            <rect x="770" y="179" width="150" height="82" rx="8" fill="#fff" stroke="#ded9cf"/>
            <text x="805" y="215" font-size="19" font-weight="800" fill="#171717">读成图像</text>
            <text x="797" y="241" font-size="14" fill="#66645e">预测交互后的画面</text>
            <rect x="770" y="298" width="150" height="82" rx="8" fill="#fff" stroke="#ded9cf"/>
            <text x="805" y="334" font-size="19" font-weight="800" fill="#171717">读成动作</text>
            <text x="797" y="360" font-size="14" fill="#66645e">控制真实机器人</text>
          </g>
        </svg>
      </div>
      <h3>三个步骤</h3>
      <p><b>第一步：观察。</b>给模型大量真实世界视频，让它学习没有标签的自然变化，比如手靠近杯子、门被推开、物体被遮挡又出现。</p>
      <p><b>第二步：解释。</b>给模型事件描述和问答，让它知道“这不是随机像素变化，而是有人把海绵放下、机器人收回手臂”。</p>
      <p><b>第三步：读出。</b>冻结 Orca 主体，只训练轻量模块，看这个内部世界能否被读成文字、未来图像、机器人动作。结果显示，潜空间越强，三个 readout 越强。</p>
    </section>

    <section class="section">
      <h2>6. 关键术语解释</h2>
      <div class="term-grid">
        <div class="term"><strong>World Model / 世界模型</strong><p>专业解释：对环境状态、动态规律和因果变化的内部表征。白话解释：AI 脑子里的一张可更新地图，不只知道“有什么”，还知道“会怎么变”。</p></div>
        <div class="term"><strong>Latent Space / 潜空间</strong><p>专业解释：模型内部压缩后的向量表征空间。白话解释：不是原始视频或文字，而是模型自己理解后的“脑内草图”。</p></div>
        <div class="term"><strong>Readout / 读出接口</strong><p>专业解释：把同一个内部表征映射到文字、图像、动作等不同输出。白话解释：同一份脑内理解，可以说出来、画出来，也可以变成手的动作。</p></div>
        <div class="term"><strong>OOD / 分布外</strong><p>专业解释：测试环境不同于训练分布。白话解释：不是考原题，而是换了房间、换了物体、换了视角，看模型还能不能懂。</p></div>
        <div class="term"><strong>VQA</strong><p>专业解释：Visual Question Answering，视觉问答监督。白话解释：给模型看图或视频，然后问它问题，逼它把视觉和语言对齐。</p></div>
        <div class="term"><strong>Proprioception / 本体感知</strong><p>专业解释：机器人的关节、末端执行器等自身状态信号。白话解释：机器人知道自己的手在哪里、关节转到什么位置。</p></div>
      </div>
    </section>

    <section class="section">
      <h2>7. 实验结果解读</h2>
      <p>这篇论文的关键不是“Orca 全面 SOTA”，而是证明：一个学到的世界潜空间，确实可以迁移到三种不同输出。</p>
      <table>
        <tr><th>任务</th><th>代表结果</th><th>普通人应该怎么理解</th></tr>
        <tr><td>文本理解</td><td>Orca-4B 在四个文本/视频理解 benchmark 平均 51.8，高于 Qwen3.5-4B 的 46.7。</td><td>它不是单靠语言参数变大，而是通过“状态变化”学习，提升了动态世界理解。</td></tr>
        <tr><td>图像预测</td><td>PRICE-V0.1 平均分 Orca-4B+2B 为 59.8，高于 FLUX.2 [klein] 的 56.1。</td><td>给它一个当前画面和指令，它更能预测真实交互后的结果，减少凭空多出手或物体的情况。</td></tr>
        <tr><td>机器人动作</td><td>总体 Rule-based 分数 Orca 为 32.4，高于 V-JEPA 2.1 的 17.0、Qwen3.5 的 10.5，也略高于 π0.5 的 29.4。</td><td>在只给每个任务 200 条真实机器人轨迹的情况下，世界潜空间能帮动作模块少走弯路。</td></tr>
        <tr><td>训练效率</td><td>H100 上训练吞吐从 StarVLA 管线的 0.66 提升到 2.91 samples/sec/GPU。</td><td>这不是算法概念秀，团队也处理了训练基础设施，否则世界模型路线很难扩展。</td></tr>
      </table>
      <div class="diagram">
        <svg viewBox="0 0 980 420" role="img" aria-label="Orca 结果对比图">
          <rect width="980" height="420" fill="#fbfaf6"/>
          <text x="40" y="48" font-size="26" font-weight="800" fill="#171717">实验结果的真正含义：同一个“脑内世界”能服务三类任务</text>
          <g font-size="15" fill="#3c3832">
            <text x="70" y="105">文本理解平均分</text><text x="70" y="205">图像预测 PRICE</text><text x="70" y="305">动作 Rule-based</text>
          </g>
          <g>
            <rect x="250" y="82" width="290" height="36" fill="#d7d2c8"/><text x="555" y="107" font-size="14" fill="#66645e">Qwen3.5-4B 46.7</text>
            <rect x="250" y="122" width="322" height="36" fill="#0f766e"/><text x="590" y="147" font-size="14" fill="#10231f">Orca-4B 51.8</text>
            <rect x="250" y="182" width="349" height="36" fill="#d7d2c8"/><text x="615" y="207" font-size="14" fill="#66645e">FLUX.2 56.1</text>
            <rect x="250" y="222" width="372" height="36" fill="#0f766e"/><text x="640" y="247" font-size="14" fill="#10231f">Orca 59.8</text>
            <rect x="250" y="282" width="183" height="36" fill="#d7d2c8"/><text x="450" y="307" font-size="14" fill="#66645e">π0.5 29.4</text>
            <rect x="250" y="322" width="202" height="36" fill="#0f766e"/><text x="470" y="347" font-size="14" fill="#10231f">Orca 32.4</text>
          </g>
          <text x="720" y="132" font-size="18" font-weight="800" fill="#10231f">注意</text>
          <text x="720" y="164" font-size="15" fill="#4b4842">这些分数不是终局证明。</text>
          <text x="720" y="192" font-size="15" fill="#4b4842">更重要的是：</text>
          <text x="720" y="220" font-size="15" fill="#4b4842">冻结主干后，轻量接口</text>
          <text x="720" y="248" font-size="15" fill="#4b4842">还能读出多种能力。</text>
        </svg>
      </div>
    </section>

    <section class="section risk">
      <h2>8. 局限性与问题</h2>
      <div class="cards">
        <div class="card risk"><b>还不是完整世界</b><p>Orca 主要学习视觉和语言，缺少声音、触觉、力、光等信号。真实世界很多变化并不只靠眼睛理解。</p></div>
        <div class="card risk"><b>规模仍小</b><p>主要实验在 0.8B 和 4B，论文也承认模型容量不足以吸收更多世界知识和更多模态。</p></div>
        <div class="card risk"><b>评测仍早期</b><p>PRICE-V0.1 和机器人任务有价值，但覆盖范围有限，不能直接推出“通用机器人智能已经解决”。</p></div>
      </div>
      <p>最需要克制的地方是：Orca 证明了方向值得走，但没有证明世界模型已经成熟。它像第一代航海地图：已经能把海岸线画出来，但距离全球精密导航还差卫星、气象、港口、船况等很多信号。</p>
    </section>

    <section class="section">
      <h2>9. 产业影响分析</h2>
      <table>
        <tr><th>对象</th><th>可能受益</th><th>可能被冲击</th></tr>
        <tr><td>机器人公司</td><td>可用大量无动作标签视频提升泛化，再用少量机器人轨迹训练动作接口。</td><td>只依赖昂贵遥操作数据堆规模的路线，成本压力会更大。</td></tr>
        <tr><td>多模态 Agent</td><td>能把“看、想、做”统一到状态变化，适合长任务、桌面操作、工业巡检。</td><td>只会文字规划但缺少环境状态理解的 Agent 会显得脆弱。</td></tr>
        <tr><td>视频生成模型</td><td>从生成好看的片段，升级到预测受约束的真实交互结果。</td><td>纯审美生成模型在物理一致性场景里会被区分出来。</td></tr>
        <tr><td>云厂商与芯片</td><td>世界模型路线继续推高长视频、多模态训练和推理基础设施需求。</td><td>小团队很难直接复刻全量训练，需要靠开源权重、蒸馏或行业数据合作。</td></tr>
      </table>
      <p>如果这条路线继续成立，未来 AI 产品会更像“可迁移的大脑 + 多个专业输出器”。同一个世界潜空间可以接客服文字、仿真图像、工厂机器人、自动驾驶解释器。竞争焦点也会从“谁的单项模型更强”变成“谁的世界状态表征更通用、更便宜、更可靠”。</p>
    </section>

    <section class="section">
      <h2>10. 延伸阅读</h2>
      <ul class="source-list">
        <li>Orca arXiv 论文：<a href="https://arxiv.org/abs/2606.30534">https://arxiv.org/abs/2606.30534</a></li>
        <li>Orca 官方项目页：<a href="https://orca-wm.github.io/">https://orca-wm.github.io/</a></li>
        <li>Hugging Face Papers 页面：<a href="https://huggingface.co/papers/2606.30534">https://huggingface.co/papers/2606.30534</a></li>
        <li>相关方向：Cosmos 3: Omnimodal world models for physical AI</li>
        <li>相关方向：V-JEPA 2.1、π0.5、GR00T N1.7、RFT、VLA-JEPA 等世界模型 / 机器人基础模型工作</li>
      </ul>
    </section>

    <section class="section">
      <h2>11. 引用来源</h2>
      <ol class="source-list">
        <li>arXiv API 与论文 PDF：标题、作者、发布时间、摘要、数据规模、实验表格、局限性。</li>
        <li>Orca 官方项目页：机构、项目入口、论文引用信息。</li>
        <li>Hugging Face Papers：社区论文页与当日候选扫描。</li>
        <li>Papers With Code 搜索：未找到稳定的 Orca 专属条目；本报告未把其作为事实来源。</li>
        <li>Semantic Scholar API：本次返回 429 限流；未作为事实来源。</li>
      </ol>
      <p class="note">本报告没有截图搬运原论文图，而是把论文中的核心流程重新设计成中文解释型图示。封面图由内置图像生成工具生成，机制图和结果图为本报告重构。</p>
    </section>

    <p class="footer">AI每日论文精选 · 面向普通读者、产品经理、创业者和投资研究者的 AI 前沿解释系统</p>
  </main>
</body>
</html>
"""


def main() -> None:
    html_out = html.replace("{{HERO_URI}}", image_data_uri(HERO))
    OUT.write_text(html_out, encoding="utf-8")
    print(OUT)
    print(len(html_out.encode("utf-8")))


if __name__ == "__main__":
    main()
