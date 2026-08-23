from base64 import b64encode
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
HERO = OUT_DIR / "hola-hero.png"
HTML = OUT_DIR / "AI-Daily-Paper-HOLA-2026-07-04.html"
EMAIL = OUT_DIR / "email_body.txt"
SOURCES = OUT_DIR / "sources.md"


hero_data = ""
if HERO.exists():
    hero_data = "data:image/png;base64," + b64encode(HERO.read_bytes()).decode("ascii")

html = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI每日论文精选｜HOLA：给线性注意力装上海马体</title>
  <style>
    :root {
      color-scheme: light dark;
      --ink: #152033;
      --muted: #5f6b7d;
      --paper: #fbfcff;
      --panel: #ffffff;
      --line: #dce3ec;
      --blue: #2468d8;
      --green: #0b8f74;
      --red: #c3423f;
      --gold: #b47b18;
      --slate: #25364d;
      --soft: #eef4ff;
      --soft2: #edf8f5;
      --soft3: #fff5df;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
      background: var(--paper);
      color: var(--ink);
      line-height: 1.72;
    }
    a { color: var(--blue); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .wrap { max-width: 1040px; margin: 0 auto; padding: 28px 18px 56px; }
    .hero {
      display: grid;
      grid-template-columns: 1.05fr .95fr;
      gap: 24px;
      align-items: center;
      padding: 34px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: linear-gradient(180deg, #ffffff 0%, #f6f9ff 100%);
    }
    .eyebrow {
      display: inline-flex;
      gap: 8px;
      align-items: center;
      margin-bottom: 14px;
      color: var(--blue);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0;
    }
    h1 {
      margin: 0;
      font-size: 42px;
      line-height: 1.12;
      letter-spacing: 0;
    }
    .subtitle { margin: 18px 0 0; color: var(--muted); font-size: 18px; }
    .hero-img {
      width: 100%;
      border-radius: 8px;
      border: 1px solid var(--line);
      display: block;
      background: #fff;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-top: 18px;
    }
    .meta {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: rgba(255,255,255,.78);
    }
    .meta b { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
    .meta span { display: block; font-size: 14px; font-weight: 700; }
    section { margin-top: 24px; }
    .section {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 24px;
    }
    h2 { margin: 0 0 14px; font-size: 26px; line-height: 1.22; letter-spacing: 0; }
    h3 { margin: 18px 0 8px; font-size: 18px; letter-spacing: 0; }
    p { margin: 9px 0; }
    .lead { font-size: 18px; color: var(--slate); }
    .one-line {
      margin: 16px 0 0;
      padding: 18px;
      border-left: 4px solid var(--blue);
      background: var(--soft);
      border-radius: 8px;
      font-size: 20px;
      font-weight: 800;
    }
    .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 14px; }
    .card {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      background: #fff;
    }
    .card b { display: block; margin-bottom: 7px; font-size: 16px; }
    .kpi { font-size: 36px; line-height: 1; font-weight: 850; color: var(--blue); margin: 6px 0; }
    .tag {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid var(--line);
      font-size: 12px;
      font-weight: 700;
      color: var(--slate);
      background: #f8fafc;
    }
    .tag.green { color: var(--green); background: var(--soft2); }
    .tag.red { color: var(--red); background: #fff0f0; }
    .tag.gold { color: var(--gold); background: var(--soft3); }
    .table-wrap { overflow-x: auto; margin-top: 14px; border: 1px solid var(--line); border-radius: 8px; }
    table { width: 100%; border-collapse: collapse; min-width: 720px; background: #fff; }
    th, td { padding: 12px 14px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
    th { background: #f3f6fb; font-size: 13px; color: var(--muted); }
    tr:last-child td { border-bottom: 0; }
    .diagram {
      margin-top: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdff;
      overflow: hidden;
    }
    .diagram svg { display: block; width: 100%; height: auto; }
    .terms { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
    .term {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fff;
    }
    .term strong { color: var(--blue); }
    .note {
      border-radius: 8px;
      border: 1px solid var(--line);
      padding: 14px 16px;
      margin-top: 12px;
      background: #f8fbff;
    }
    .risk { border-color: #f0c6c4; background: #fff6f5; }
    .why { border-color: #cfe9df; background: #f2fbf7; }
    .bars { margin-top: 12px; }
    .bar-row {
      display: grid;
      grid-template-columns: 150px 1fr 70px;
      gap: 10px;
      align-items: center;
      margin: 10px 0;
      font-size: 14px;
    }
    .track { height: 14px; border-radius: 999px; background: #e8edf5; overflow: hidden; }
    .bar { height: 100%; border-radius: 999px; background: var(--blue); }
    .bar.green { background: var(--green); }
    .bar.gold { background: var(--gold); }
    .bar.red { background: var(--red); }
    ul { padding-left: 20px; margin: 10px 0; }
    li { margin: 6px 0; }
    .footer { color: var(--muted); font-size: 13px; margin-top: 20px; }
    @media (max-width: 820px) {
      .wrap { padding: 14px 12px 36px; }
      .hero { grid-template-columns: 1fr; padding: 22px; }
      h1 { font-size: 32px; }
      .subtitle, .lead { font-size: 16px; }
      .meta-grid, .cards, .terms { grid-template-columns: 1fr; }
      .section { padding: 18px; }
      h2 { font-size: 22px; }
      .bar-row { grid-template-columns: 110px 1fr 52px; }
    }
  </style>
</head>
<body>
  <main class="wrap">
    <header class="hero">
      <div>
        <div class="eyebrow">AI每日论文精选 · 2026-07-04</div>
        <h1>给线性注意力装上海马体：让便宜模型记住真正重要的细节</h1>
        <p class="subtitle">今日精选论文：<i>A Hippocampus for Linear Attention: An Exact Memory for What the Recurrent State Forgets</i>。它讨论的是未来大模型最现实的矛盾之一：我们既想要 Transformer 的精确记忆，又想要线性模型的低成本长上下文。</p>
        <div class="meta-grid">
          <div class="meta"><b>论文</b><span>HOLA</span></div>
          <div class="meta"><b>作者</b><span>Wanyun Cui</span></div>
          <div class="meta"><b>机构</b><span>上海财经大学</span></div>
          <div class="meta"><b>平台</b><span>arXiv · 2026-07-02</span></div>
        </div>
      </div>
      <img class="hero-img" src="__HERO_DATA__" alt="HOLA 记忆系统示意图">
    </header>

    <section class="section">
      <h2>1. 标题区</h2>
      <div class="table-wrap">
        <table>
          <tr><th>项目</th><th>信息</th></tr>
          <tr><td>英文标题</td><td><b>A Hippocampus for Linear Attention: An Exact Memory for What the Recurrent State Forgets</b></td></tr>
          <tr><td>中文标题</td><td>给线性注意力一个“海马体”：为循环状态遗忘的内容建立精确记忆</td></tr>
          <tr><td>作者</td><td>Wanyun Cui</td></tr>
          <tr><td>机构</td><td>Shanghai University of Finance and Economics</td></tr>
          <tr><td>发布时间</td><td>2026-07-02，arXiv:2607.02303v1</td></tr>
          <tr><td>会议/平台</td><td>arXiv cs.AI / cs.CL 预印本</td></tr>
          <tr><td>论文链接</td><td><a href="https://arxiv.org/abs/2607.02303">https://arxiv.org/abs/2607.02303</a></td></tr>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>2. 为什么今天选它？</h2>
      <p class="lead">因为它抓住了大模型工程里一个很硬的成本问题：长上下文越来越重要，但完整 Transformer 注意力会让内存和计算随上下文增长而变贵；线性注意力更省，却容易忘掉很远处的精确事实。</p>
      <div class="cards">
        <div class="card"><span class="tag green">行业意义</span><b>长上下文的成本拐点</b><p>如果模型能用近似固定的内存处理长文本，同时记住关键事实，未来文档助手、代码 Agent、企业知识库会更便宜。</p></div>
        <div class="card"><span class="tag gold">认知突破</span><b>别把所有记忆塞进一个箱子</b><p>论文借鉴人脑互补学习系统：新皮层负责压缩规律，海马体负责一次性精确记住特殊事件。</p></div>
        <div class="card"><span class="tag red">长期价值</span><b>给高效模型补上精确回忆</b><p>它不是追逐更大模型，而是在问：模型自己已经知道哪些信息“不该被压缩”，能不能把这些信息单独保存？</p></div>
      </div>
      <div class="note why"><b>今天的判断：</b>HOLA 值得关注，不是因为它已经证明可以取代 Transformer，而是因为它给“低成本长上下文模型”提供了一个干净的设计原则：压缩记忆负责规律，精确缓存负责意外事实。</div>
    </section>

    <section class="section">
      <h2>3. 一句话讲透论文</h2>
      <div class="one-line">这篇论文是在教便宜的长上下文模型：平时像做笔记一样压缩全文，但遇到“可能会考”的细节，就单独放进一个小抽屉，等需要时精确取出来。</div>
    </section>

    <section class="section">
      <h2>4. 核心贡献拆解</h2>
      <div class="table-wrap">
        <table>
          <tr><th>贡献</th><th>它做了什么</th><th>为什么更好</th></tr>
          <tr><td><span class="tag green">双记忆结构</span></td><td>保留 Gated DeltaNet 的压缩循环状态，再增加一个容量有限的精确 KV 缓存。</td><td>压缩状态负责“整体规律”，缓存负责“不能丢的具体事实”。</td></tr>
          <tr><td><span class="tag gold">惊讶度写入</span></td><td>用 delta-rule 已经计算出的 β · ||e|| 作为缓存淘汰分数。</td><td>不用额外学习一个复杂淘汰器，直接保存“模型刚才最费劲才写进去”的 token。</td></tr>
          <tr><td><span class="tag green">锐化读取</span></td><td>用独立的 RMSNorm-γ 路径读取缓存，让匹配更接近精确检索。</td><td>避免缓存被读成“平均一堆相似信息”，真正发挥精确记忆作用。</td></tr>
          <tr><td><span class="tag red">实验锚点</span></td><td>340M 模型、15B SlimPajama tokens 训练，Wikitext 困惑度 27.32 降到 22.92。</td><td>说明收益不是只在玩具任务上出现，而是在语言建模和长距离检索上同时体现。</td></tr>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>5. 工作原理：深入浅出</h2>
      <p>把模型想象成一个每天处理几千页资料的研究助理。普通线性注意力像一本“不断压缩的会议纪要”：越写越省空间，但早期的具体数字、姓名、代码片段容易被覆盖。HOLA 给它加了一个“考试重点卡盒”：不是保存最近看到的东西，而是保存模型自己觉得最意外、最难压缩的东西。</p>
      <div class="diagram" aria-label="HOLA 工作流程图">
        <svg viewBox="0 0 960 430" role="img">
          <rect width="960" height="430" fill="#fbfdff"/>
          <rect x="42" y="55" width="185" height="78" rx="8" fill="#eef4ff" stroke="#b9c8e8"/>
          <text x="134" y="88" text-anchor="middle" font-size="19" font-weight="700" fill="#152033">输入 token</text>
          <text x="134" y="115" text-anchor="middle" font-size="14" fill="#5f6b7d">文档、代码、对话</text>
          <path d="M230 94 H305" stroke="#6c7a90" stroke-width="3" marker-end="url(#arrow)"/>
          <rect x="312" y="38" width="250" height="116" rx="8" fill="#edf8f5" stroke="#9acdbc"/>
          <text x="437" y="73" text-anchor="middle" font-size="19" font-weight="700" fill="#152033">压缩记忆 State</text>
          <text x="437" y="101" text-anchor="middle" font-size="14" fill="#5f6b7d">像新皮层：总结规律</text>
          <text x="437" y="126" text-anchor="middle" font-size="14" fill="#5f6b7d">省内存，但会覆盖细节</text>
          <path d="M437 156 V222" stroke="#6c7a90" stroke-width="3" marker-end="url(#arrow)"/>
          <rect x="292" y="229" width="290" height="76" rx="8" fill="#fff5df" stroke="#e6c77e"/>
          <text x="437" y="260" text-anchor="middle" font-size="19" font-weight="700" fill="#152033">计算惊讶度 β · ||e||</text>
          <text x="437" y="286" text-anchor="middle" font-size="14" fill="#5f6b7d">这个 token 是否真的改变了记忆？</text>
          <path d="M585 267 H660" stroke="#6c7a90" stroke-width="3" marker-end="url(#arrow)"/>
          <rect x="670" y="214" width="240" height="108" rx="8" fill="#fff0f0" stroke="#e7aaa6"/>
          <text x="790" y="248" text-anchor="middle" font-size="19" font-weight="700" fill="#152033">精确 KV 缓存</text>
          <text x="790" y="276" text-anchor="middle" font-size="14" fill="#5f6b7d">像海马体：保存意外事实</text>
          <text x="790" y="301" text-anchor="middle" font-size="14" fill="#5f6b7d">容量小，但可精确回忆</text>
          <path d="M562 96 H710 Q790 96 790 214" stroke="#2468d8" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
          <path d="M437 305 V358 H790 V322" stroke="#0b8f74" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
          <rect x="337" y="356" width="420" height="46" rx="8" fill="#f3f6fb" stroke="#c9d3e1"/>
          <text x="547" y="386" text-anchor="middle" font-size="18" font-weight="700" fill="#152033">输出 = 压缩理解 + 精确回忆</text>
          <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#6c7a90"/></marker></defs>
        </svg>
      </div>
      <h3>三个步骤</h3>
      <ul>
        <li><b>第一步：所有 token 都进入压缩状态。</b>这保证模型仍然像线性注意力一样便宜，不需要把所有历史 token 都完整保留下来。</li>
        <li><b>第二步：用“写入幅度”判断谁值得单独保存。</b>如果一个 token 让状态发生很大改动，说明它不是普通背景信息，而是可能需要精确记住的事实。</li>
        <li><b>第三步：查询时同时读两个地方。</b>压缩状态给出大方向，精确缓存给出少量高价值事实，最后合成答案。</li>
      </ul>
    </section>

    <section class="section">
      <h2>6. 关键术语解释</h2>
      <div class="terms">
        <div class="term"><strong>Linear Attention</strong><p><b>专业：</b>用固定大小循环状态近似注意力，避免完整 KV cache 随上下文增长。</p><p><b>白话：</b>不是把每页资料都放桌上，而是边读边写一份压缩笔记。</p></div>
        <div class="term"><strong>KV Cache</strong><p><b>专业：</b>保存 key-value 对，供后续 token 通过相似度检索。</p><p><b>白话：</b>像索引卡片：问题像 key，卡片内容像 value。</p></div>
        <div class="term"><strong>Delta Rule</strong><p><b>专业：</b>根据当前状态预测误差更新记忆矩阵。</p><p><b>白话：</b>如果新信息和笔记差很多，就把差异补进去。</p></div>
        <div class="term"><strong>β · ||e||</strong><p><b>专业：</b>写入强度乘以预测残差大小，用作缓存保留分数。</p><p><b>白话：</b>既要“我没想到”，也要“我真的把它写进去了”。</p></div>
        <div class="term"><strong>Perplexity</strong><p><b>专业：</b>语言模型预测下一个 token 的困惑程度，越低越好。</p><p><b>白话：</b>越低说明模型越不“猜瞎了”，语言理解更稳。</p></div>
        <div class="term"><strong>RULER / Needle Recall</strong><p><b>专业：</b>长上下文检索基准，测试模型能否从长文本中找回特定信息。</p><p><b>白话：</b>把一根针藏进一大堆干草里，看模型能不能找回来。</p></div>
      </div>
    </section>

    <section class="section">
      <h2>7. 实验结果解读</h2>
      <div class="cards">
        <div class="card"><b>语言建模</b><div class="kpi">22.92</div><p>Wikitext 困惑度，从同骨架 GDN 的 27.32 降到 22.92，下降 16.1%。</p></div>
        <div class="card"><b>长上下文找针</b><div class="kpi">0.58</div><p>32k S-NIAH-1 召回，GDN 为 0.14，HOLA+recency 为 0.24。</p></div>
        <div class="card"><b>额外参数</b><div class="kpi">&lt;0.004%</div><p>作者报告缓存路径新增可训练标量很少，主要成本是推理时的小缓存。</p></div>
      </div>
      <div class="bars">
        <h3>Wikitext 困惑度：越低越好</h3>
        <div class="bar-row"><span>GDN</span><div class="track"><div class="bar red" style="width: 82%"></div></div><b>27.32</b></div>
        <div class="bar-row"><span>HOLA+recency</span><div class="track"><div class="bar gold" style="width: 75%"></div></div><b>25.04</b></div>
        <div class="bar-row"><span>Transformer++</span><div class="track"><div class="bar" style="width: 81%"></div></div><b>26.88</b></div>
        <div class="bar-row"><span>HOLA</span><div class="track"><div class="bar green" style="width: 69%"></div></div><b>22.92</b></div>
      </div>
      <div class="table-wrap">
        <table>
          <tr><th>实验</th><th>旧方法表现</th><th>HOLA 表现</th><th>这意味着什么</th></tr>
          <tr><td>Wikitext-103</td><td>GDN 27.32；Transformer++ 26.88</td><td>22.92</td><td>在同等规模实验里，压缩模型加精确缓存后，语言建模更稳。</td></tr>
          <tr><td>LAMBADA 困惑度</td><td>GDN 30.95</td><td>30.26</td><td>收益较小，但方向一致。</td></tr>
          <tr><td>FDA 检索</td><td>GDN 11.7</td><td>20.1</td><td>精确抽取能力显著增强，但仍低于完整注意力的 46.1。</td></tr>
          <tr><td>32k 单针召回</td><td>GDN 0.14；最近缓存 0.24</td><td>0.58</td><td>“保存重要信息”比“保存最近信息”更适合远距离找针。</td></tr>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>8. 局限性与问题</h2>
      <div class="note risk"><b>不要过度解读：</b>HOLA 还不是一个可直接替换所有 Transformer 的工业结论。它是一篇很有启发的架构论文，但仍需要更大规模、多 seed、更多真实工作负载验证。</div>
      <ul>
        <li><b>缓存容量仍然有限。</b>论文默认 w=64，并加当前 chunk，作者也承认 32k 召回是 0.58，不是满分。</li>
        <li><b>纯精确抽取仍落后完整注意力。</b>FDA 上 HOLA 从 11.7 提到 20.1，但 full-attention Transformer++ 仍是 46.1。</li>
        <li><b>主要大规模结果是单 seed。</b>作者给出 46M 诊断和跨尺度趋势，但 340M 级别仍需要更强复现实验。</li>
        <li><b>产业落地需要工程验证。</b>真实服务中还要看批处理、KV 管理、长文档分布、推理延迟和硬件 kernel 支持。</li>
      </ul>
    </section>

    <section class="section">
      <h2>9. 产业影响分析</h2>
      <p>如果这条路线成立，受益最大的不是“聊天更会说话”，而是需要长上下文、低成本、精确回忆的系统。</p>
      <div class="table-wrap">
        <table>
          <tr><th>对象</th><th>可能变化</th><th>判断</th></tr>
          <tr><td>企业知识库</td><td>长文档问答可以少依赖昂贵完整注意力，同时保留关键事实。</td><td>中期受益，但还需和 RAG、检索排序结合。</td></tr>
          <tr><td>代码 Agent</td><td>项目级上下文中，少量关键变量、接口、错误栈值得精确缓存。</td><td>很相关，因为代码任务常常输在远处细节。</td></tr>
          <tr><td>端侧模型</td><td>固定或接近固定内存更适合手机、PC、本地设备。</td><td>长期值得看，前提是 kernel 和模型生态跟上。</td></tr>
          <tr><td>模型厂商</td><td>低成本长上下文可能削弱“堆更大 KV cache”的单一路线。</td><td>不是替代，而是多一条效率架构分支。</td></tr>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>10. 延伸阅读</h2>
      <ul>
        <li><a href="https://arxiv.org/abs/2607.02303">原论文：A Hippocampus for Linear Attention</a></li>
        <li><a href="https://arxiv.org/html/2607.02303">arXiv HTML 版本</a></li>
        <li><a href="https://arxiv.org/abs/2402.18668">Simple Linear Attention Language Models Balance the Recall-Throughput Tradeoff</a></li>
        <li><a href="https://arxiv.org/abs/2404.06654">RULER: What is the Real Context Size of Your Long-Context Language Models?</a></li>
        <li><a href="https://arxiv.org/abs/2405.21060">Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality</a></li>
        <li><a href="https://arxiv.org/abs/2410.01201">Gated Delta Networks: Improving Mamba2 with Delta Rule</a></li>
      </ul>
    </section>

    <section class="section">
      <h2>11. 引用来源</h2>
      <ul>
        <li>Wanyun Cui. <i>A Hippocampus for Linear Attention: An Exact Memory for What the Recurrent State Forgets</i>. arXiv:2607.02303v1, 2026-07-02. <a href="https://arxiv.org/abs/2607.02303">arXiv</a></li>
        <li>论文 PDF 与 HTML 正文，本报告已本地抽取用于核验标题、作者、机构、实验设置、表格数据和局限性。</li>
        <li>Hsieh et al. <i>RULER: What is the Real Context Size of Your Long-Context Language Models?</i> arXiv:2404.06654.</li>
        <li>Arora et al. <i>Simple Linear Attention Language Models Balance the Recall-Throughput Tradeoff</i>. ICML 2024 / arXiv:2402.18668.</li>
      </ul>
      <p class="footer">视觉说明：顶部概念图由图像生成工具生成；流程图与数据图为本报告根据论文机制和表格重新绘制，非论文截图。</p>
    </section>
  </main>
</body>
</html>
"""

if not hero_data:
    html = html.replace('<img class="hero-img" src="__HERO_DATA__" alt="HOLA 记忆系统示意图">', "")
else:
    html = html.replace("__HERO_DATA__", hero_data)

HTML.write_text(html, encoding="utf-8")

EMAIL.write_text(
    """今天精选的论文是 A Hippocampus for Linear Attention，来自上海财经大学 Wanyun Cui，2026-07-02 发布在 arXiv。

一句话推荐理由：
它把线性注意力“省钱但容易忘细节”的问题，重新解释成一个双记忆系统问题：压缩状态负责规律，海马体式缓存负责精确事实。

这可能是低成本长上下文模型的重要方向之一，尤其适合未来的企业知识库、代码 Agent 和端侧模型。

附件为中文深度拆解 HTML 报告，适合非技术读者阅读。""",
    encoding="utf-8",
)

SOURCES.write_text(
    """# Sources

- arXiv abstract: https://arxiv.org/abs/2607.02303
- arXiv PDF: https://arxiv.org/pdf/2607.02303
- arXiv HTML: https://arxiv.org/html/2607.02303
- Local PDF text extraction: reports/source_papers/hola-2607.02303.txt
- Generated hero image: reports/2026-07-04-hola/hola-hero.png
""",
    encoding="utf-8",
)

print(HTML)
print(EMAIL)
print(SOURCES)
