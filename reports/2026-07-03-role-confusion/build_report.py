from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HERO = ROOT / "role-confusion-hero.png"
OUT = ROOT / "AI-Daily-Paper-Role-Confusion-2026-07-03.html"
SUBJECT = ROOT / "email_subject.txt"
BODY = ROOT / "email_body.txt"


def image_data_uri(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


hero_uri = image_data_uri(HERO)

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>AI每日论文精选｜Prompt Injection as Role Confusion</title>
  <style>
    :root {{
      --bg:#f4f6f8;
      --paper:#ffffff;
      --ink:#15181d;
      --muted:#626b77;
      --line:#dde3ea;
      --accent:#0b6bcb;
      --accent2:#b54628;
      --accent3:#0b7a53;
      --soft:#edf5ff;
      --soft2:#fff4ee;
      --dark:#101820;
      --shadow:0 18px 50px rgba(24,35,52,.10);
    }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{
      margin:0;
      background:linear-gradient(180deg,#f7f9fb 0%,#eef2f6 100%);
      color:var(--ink);
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Arial,sans-serif;
      line-height:1.74;
      letter-spacing:0;
    }}
    a {{ color:var(--accent); text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    .wrap {{ max-width:1100px; margin:0 auto; padding:28px 18px 70px; }}
    .hero {{
      overflow:hidden;
      border-radius:8px;
      background:var(--dark);
      color:#fff;
      box-shadow:var(--shadow);
      border:1px solid rgba(10,20,32,.1);
    }}
    .hero-img {{
      min-height:395px;
      display:grid;
      align-items:end;
      padding:54px 44px;
      background-image:linear-gradient(90deg,rgba(5,12,20,.92),rgba(5,12,20,.68),rgba(5,12,20,.18)),url("{hero_uri}");
      background-size:cover;
      background-position:center;
    }}
    .eyebrow {{
      display:inline-block;
      width:fit-content;
      border:1px solid rgba(255,255,255,.36);
      border-radius:999px;
      padding:4px 10px;
      color:rgba(255,255,255,.88);
      font-size:12px;
      font-weight:750;
      text-transform:uppercase;
    }}
    h1 {{
      margin:18px 0 12px;
      max-width:840px;
      font-size:clamp(36px,6vw,70px);
      line-height:1.03;
      letter-spacing:0;
    }}
    .subtitle {{ max-width:800px; margin:0; color:rgba(255,255,255,.87); font-size:18px; }}
    .meta-grid {{
      display:grid;
      grid-template-columns:repeat(4,minmax(0,1fr));
      gap:1px;
      background:rgba(255,255,255,.14);
      border-top:1px solid rgba(255,255,255,.16);
    }}
    .meta-cell {{ padding:18px; background:rgba(8,18,28,.86); }}
    .meta-cell b {{ display:block; color:rgba(255,255,255,.55); font-size:12px; margin-bottom:6px; }}
    .meta-cell span {{ font-weight:700; }}
    .section {{
      margin-top:22px;
      padding:28px;
      background:var(--paper);
      border:1px solid var(--line);
      border-radius:8px;
      box-shadow:0 8px 24px rgba(21,31,44,.045);
    }}
    h2 {{ margin:0 0 14px; font-size:28px; line-height:1.24; letter-spacing:0; }}
    h3 {{ margin:20px 0 8px; font-size:18px; }}
    p {{ margin:10px 0; }}
    .lead {{ font-size:19px; color:#2b3139; }}
    .one-line {{
      padding:22px 24px;
      border-left:5px solid var(--accent);
      border-radius:6px;
      background:var(--soft);
      font-size:24px;
      line-height:1.38;
      font-weight:800;
    }}
    .cards {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin-top:16px; }}
    .card {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:16px; }}
    .card b {{ display:block; color:#0f253d; margin-bottom:6px; }}
    .kpi {{ font-size:34px; line-height:1; font-weight:850; color:var(--accent); margin:8px 0 4px; }}
    .risk {{ background:var(--soft2); border-color:#f0c7b7; }}
    .risk b {{ color:var(--accent2); }}
    table {{ width:100%; border-collapse:collapse; margin:16px 0; font-size:14px; background:#fff; border:1px solid var(--line); }}
    th,td {{ padding:11px 10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
    th {{ background:#eef3f8; color:#475363; font-size:12px; text-transform:uppercase; }}
    tr:last-child td {{ border-bottom:0; }}
    .pill {{ display:inline-block; padding:3px 8px; border-radius:999px; background:#e7f1ff; color:#0b5cad; font-size:12px; font-weight:750; }}
    .pill.red {{ background:#fff0e8; color:#ad3f1d; }}
    .pill.green {{ background:#e8f6ef; color:#0b7250; }}
    .note {{ color:var(--muted); font-size:13px; }}
    .diagram {{
      margin:18px 0;
      border:1px solid var(--line);
      border-radius:8px;
      overflow:hidden;
      background:linear-gradient(180deg,#fff,#f8fbff);
    }}
    .diagram svg {{ display:block; width:100%; height:auto; }}
    .bar-row {{ display:grid; grid-template-columns:150px 1fr 64px; gap:12px; align-items:center; margin:10px 0; }}
    .bar-label {{ font-weight:700; font-size:14px; }}
    .bar-track {{ height:18px; background:#e7edf4; border-radius:999px; overflow:hidden; }}
    .bar {{ height:100%; border-radius:999px; background:linear-gradient(90deg,#0b6bcb,#30a1ff); }}
    .bar.red {{ background:linear-gradient(90deg,#b54628,#f47a52); }}
    .bar.green {{ background:linear-gradient(90deg,#0b7a53,#37b987); }}
    .terms {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }}
    .term {{ padding:14px; border:1px solid var(--line); border-radius:8px; background:#fff; }}
    .term strong {{ color:var(--accent); }}
    .source-list li {{ margin:8px 0; }}
    .footer {{ text-align:center; color:var(--muted); font-size:13px; margin-top:30px; }}
    @media (max-width:780px) {{
      .wrap {{ padding:12px 10px 38px; }}
      .hero-img {{ min-height:430px; padding:34px 22px; }}
      h1 {{ font-size:38px; }}
      .subtitle {{ font-size:16px; }}
      .meta-grid,.cards,.terms {{ grid-template-columns:1fr; }}
      .section {{ padding:20px 16px; }}
      table {{ font-size:13px; }}
      th,td {{ padding:9px 8px; }}
      .bar-row {{ grid-template-columns:1fr; gap:5px; }}
    }}
    @media (prefers-color-scheme:dark) {{
      :root {{ --bg:#101418; --paper:#171c21; --ink:#f2f5f8; --muted:#aab2bb; --line:#303943; --soft:#12243a; --soft2:#2a1d18; }}
      body {{ background:#101418; }}
      .lead {{ color:#e7edf4; }}
      .card,.term,table {{ background:#1f252b; }}
      th {{ background:#26303a; color:#d2d9e1; }}
      .diagram {{ background:#171c21; }}
      .bar-track {{ background:#303943; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <header class="hero">
      <div class="hero-img">
        <div>
          <span class="eyebrow">AI Daily Paper · 2026-07-03</span>
          <h1>提示词注入的真正漏洞：AI 分不清“谁在说话”</h1>
          <p class="subtitle">今日精选论文：<i>Prompt Injection as Role Confusion</i>。它把 prompt injection 从“提示词攻防技巧”推进到一个更底层的问题：模型在内部如何判断系统、用户、工具、自己思考之间的边界。</p>
        </div>
      </div>
      <div class="meta-grid">
        <div class="meta-cell"><b>论文</b><span>Prompt Injection as Role Confusion</span></div>
        <div class="meta-cell"><b>作者</b><span>Charles Ye · Jasmine Cui · Dylan Hadfield-Menell</span></div>
        <div class="meta-cell"><b>机构</b><span>Independent · MIT</span></div>
        <div class="meta-cell"><b>平台</b><span>arXiv · ICML 2026</span></div>
      </div>
    </header>

    <section class="section">
      <h2>1. 标题区</h2>
      <table>
        <tr><th>项目</th><th>信息</th></tr>
        <tr><td>英文标题</td><td><b>Prompt Injection as Role Confusion</b></td></tr>
        <tr><td>中文标题</td><td>把提示词注入理解为“角色混淆”</td></tr>
        <tr><td>作者</td><td>Charles Ye, Jasmine Cui, Dylan Hadfield-Menell</td></tr>
        <tr><td>机构</td><td>Charles Ye 与 Jasmine Cui 为独立研究者；Dylan Hadfield-Menell 来自 MIT</td></tr>
        <tr><td>发布时间</td><td>arXiv 初版 2026-02-22；论文 PDF 显示 v6 为 2026-06-27</td></tr>
        <tr><td>会议/平台</td><td>arXiv:2603.12277；项目页标注 accepted to ICML 2026</td></tr>
        <tr><td>论文链接</td><td><a href="https://arxiv.org/abs/2603.12277">https://arxiv.org/abs/2603.12277</a></td></tr>
        <tr><td>项目页</td><td><a href="https://role-confusion.github.io/">https://role-confusion.github.io/</a></td></tr>
      </table>
    </section>

    <section class="section">
      <h2>2. 为什么今天选它？</h2>
      <p class="lead">因为 Agent 时代真正危险的不是“AI 会不会被一句坏话骗到”，而是：AI 是否真的知道哪些文字有权下命令，哪些文字只是网页、邮件、PDF 或工具返回的数据。</p>
      <div class="cards">
        <div class="card"><b>行业意义</b><p>企业正把 LLM 接进邮箱、浏览器、数据库和代码仓库。只要模型把网页里的假命令当成用户授权，Agent 就可能越权。</p></div>
        <div class="card"><b>技术突破</b><p>论文不是再列一个攻击样例，而是设计 role probes，尝试直接读取模型内部“它以为谁在说话”。</p></div>
        <div class="card"><b>长期价值</b><p>它把 prompt injection 从外围过滤问题，推进为模型表征与架构边界问题。这会影响未来 Agent 安全栈怎么设计。</p></div>
      </div>
      <p>我选择它而不是泛泛的安全论文，是因为它给出了一个可迁移的解释框架：今天攻击者伪装成“模型自己的思考”，明天也可能伪装成“用户批准”“系统政策”“工具结果”。如果模型只靠文字风格判断权威来源，所有接入外部世界的 Agent 都会长期处在脆弱状态。</p>
    </section>

    <section class="section">
      <h2>3. 一句话讲透论文</h2>
      <div class="one-line">这篇论文的核心是：大模型看到的是一锅连续文字汤，它不总是按标签分清角色，而是会被“说话的腔调”骗，以为外部攻击文字就是自己的想法或用户的授权。</div>
    </section>

    <section class="section">
      <h2>4. 核心贡献拆解</h2>
      <table>
        <tr><th>贡献</th><th>解决的问题</th><th>为什么更好</th></tr>
        <tr><td><span class="pill">新解释</span></td><td>把 prompt injection 归因为 role confusion：模型按写法而不是来源判断角色。</td><td>过去像是在追每一种骗术；现在开始研究“为什么这些骗术都能骗成”。</td></tr>
        <tr><td><span class="pill">新工具</span></td><td>提出 role probes，测量模型内部把某段 token 当成 user、tool、assistant 还是 think。</td><td>它让安全评估不只看最终回答，还能在模型生成前观察风险状态。</td></tr>
        <tr><td><span class="pill red">新攻击</span></td><td>提出 CoT Forgery：把伪造的思考过程塞进低权限输入，让模型误以为那是自己的推理。</td><td>攻击在多个模型上零样本迁移，说明问题更像结构漏洞，而不是某个模型的偶然失败。</td></tr>
        <tr><td><span class="pill green">新指标</span></td><td>证明内部角色混淆程度能预测攻击成功率。</td><td>这给防御提供了新目标：修正角色感知，而不是只背诵已知攻击模板。</td></tr>
      </table>
    </section>

    <section class="section">
      <h2>5. 工作原理：深入浅出</h2>
      <p>把一个 AI Agent 想成一家银行。系统指令像董事会章程，用户指令像柜台客户，工具输出像外部快递送来的文件。正常银行绝不会因为快递纸箱上写着“我是董事会命令”就转账。但今天的大模型有时会被纸箱上的语气骗到。</p>
      <div class="diagram" aria-label="角色混淆流程图">
        <svg viewBox="0 0 1100 430" role="img">
          <rect width="1100" height="430" fill="#f8fbff"/>
          <text x="40" y="48" font-size="26" font-weight="800" fill="#17212b">从结构化对话到“一锅文字汤”</text>
          <rect x="45" y="85" width="210" height="72" rx="8" fill="#e9f3ff" stroke="#9bc4ee"/>
          <text x="70" y="116" font-size="18" font-weight="700" fill="#0b5cad">系统指令</text>
          <text x="70" y="140" font-size="14" fill="#425466">最高优先级规则</text>
          <rect x="45" y="180" width="210" height="72" rx="8" fill="#e8f6ef" stroke="#8bcfac"/>
          <text x="70" y="211" font-size="18" font-weight="700" fill="#0b7250">用户请求</text>
          <text x="70" y="235" font-size="14" fill="#425466">真正授权通道</text>
          <rect x="45" y="275" width="210" height="72" rx="8" fill="#fff1e8" stroke="#f0b99c"/>
          <text x="70" y="306" font-size="18" font-weight="700" fill="#ad3f1d">网页/工具输出</text>
          <text x="70" y="330" font-size="14" fill="#425466">低权限外部数据</text>
          <path d="M280 216 C350 216 360 216 430 216" stroke="#738294" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          <rect x="455" y="95" width="240" height="250" rx="12" fill="#101820"/>
          <text x="485" y="132" font-size="20" font-weight="800" fill="#fff">模型实际看到</text>
          <text x="485" y="168" font-size="15" fill="#cfd8e3">system ... user ... tool ...</text>
          <text x="485" y="197" font-size="15" fill="#cfd8e3">一整串连续 token</text>
          <text x="485" y="232" font-size="15" fill="#ffb38a">攻击文字模仿“思考腔”</text>
          <text x="485" y="262" font-size="15" fill="#cfd8e3">模型内部开始误判：</text>
          <text x="485" y="292" font-size="17" font-weight="800" fill="#ffdb7a">这像是我自己的推理</text>
          <path d="M720 216 C790 216 802 216 872 216" stroke="#738294" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          <rect x="895" y="115" width="165" height="205" rx="12" fill="#fff" stroke="#dde3ea"/>
          <text x="925" y="158" font-size="20" font-weight="800" fill="#17212b">结果</text>
          <text x="925" y="192" font-size="15" fill="#425466">低权限文本</text>
          <text x="925" y="220" font-size="15" fill="#425466">继承高权限</text>
          <text x="925" y="258" font-size="17" font-weight="800" fill="#b54628">越权执行</text>
          <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#738294"/></marker></defs>
        </svg>
      </div>
      <h3>三步理解</h3>
      <table>
        <tr><th>步骤</th><th>白话解释</th><th>论文里的对应概念</th></tr>
        <tr><td>1. 标签本来是门禁</td><td>系统、用户、工具、助手、思考分别有不同权限。</td><td>Role tags / instruction hierarchy</td></tr>
        <tr><td>2. 模型把门禁当口音</td><td>它不仅看“这段来自哪里”，还看“这段像谁说的”。</td><td>Role perception in latent space</td></tr>
        <tr><td>3. 攻击者模仿高权限口音</td><td>外部文本写得像模型自己的思考，就可能拿到不该有的信任。</td><td>CoT Forgery / style-induced role confusion</td></tr>
      </table>
    </section>

    <section class="section">
      <h2>6. 关键术语解释</h2>
      <div class="terms">
        <div class="term"><strong>Prompt Injection</strong><p><b>专业：</b>攻击者把恶意指令藏在用户输入、网页、邮件或工具输出中，试图覆盖原本指令。</p><p><b>白话：</b>像在快递单里夹一张“老板说马上转账”的假纸条。</p></div>
        <div class="term"><strong>Role Tags</strong><p><b>专业：</b>聊天模板中标记 system、user、assistant、tool 等来源的结构标签。</p><p><b>白话：</b>每段话胸前的工牌，告诉模型它是谁说的。</p></div>
        <div class="term"><strong>Role Confusion</strong><p><b>专业：</b>模型内部表征把低权限文本误识别为高权限角色。</p><p><b>白话：</b>保安看口气不像看证件，把冒牌人员放进了机房。</p></div>
        <div class="term"><strong>CoT Forgery</strong><p><b>专业：</b>伪造 chain-of-thought 风格文本，让模型误以为那是自身推理。</p><p><b>白话：</b>伪造一张“我已经认真想过，可以这么做”的内部审批单。</p></div>
        <div class="term"><strong>Role Probes</strong><p><b>专业：</b>线性探针，用模型激活值预测某个 token 在内部被感知成哪个角色。</p><p><b>白话：</b>给模型脑内装一个测温计，看看它把这段话当成谁。</p></div>
        <div class="term"><strong>Latent Space</strong><p><b>专业：</b>模型内部用于表示意义、风格、角色等信息的高维空间。</p><p><b>白话：</b>模型脑子里的地图；论文发现“角色边界”在这张地图上并不牢固。</p></div>
      </div>
    </section>

    <section class="section">
      <h2>7. 实验结果解读</h2>
      <p class="lead">最重要的不是“攻击成功了”，而是成功率随内部角色感知一起变化。这说明它不是玄学，也不只是某句提示词凑巧有效。</p>
      <div class="cards">
        <div class="card"><b>聊天安全基准</b><div class="kpi">60%</div><p>CoT Forgery 在 StrongREJECT 上达到约 60% 平均攻击成功率，而基线接近 0。</p></div>
        <div class="card"><b>Agent 外泄任务</b><div class="kpi">61%</div><p>在 agent exfiltration 场景中，平均攻击成功率约 61%。</p></div>
        <div class="card"><b>去风格化后</b><div class="kpi">10%</div><p>保留语义但去掉“思考腔调”后，攻击成功率从 61% 降到约 10%。</p></div>
      </div>
      <div class="section" style="margin-top:16px; box-shadow:none;">
        <h3>关键数字怎么读</h3>
        <div class="bar-row"><div class="bar-label">CoT Forgery</div><div class="bar-track"><div class="bar red" style="width:60.5%"></div></div><div>60.5%</div></div>
        <div class="bar-row"><div class="bar-label">去风格化版本</div><div class="bar-track"><div class="bar green" style="width:9.7%"></div></div><div>9.7%</div></div>
        <div class="bar-row"><div class="bar-label">最低混淆分位</div><div class="bar-track"><div class="bar" style="width:2%"></div></div><div>2%</div></div>
        <div class="bar-row"><div class="bar-label">最高混淆分位</div><div class="bar-track"><div class="bar red" style="width:70%"></div></div><div>70%</div></div>
      </div>
      <p>这意味着：安全问题不只出在模型“不够聪明”。恰恰相反，模型很会读风格，于是把风格当成身份。对企业应用来说，单靠把工具输出包在低权限标签里，可能不足以保证安全。</p>
    </section>

    <section class="section">
      <h2>8. 局限性与问题</h2>
      <div class="cards">
        <div class="card risk"><b>模型与时间窗口限制</b><p>部分结果来自 late-2025/frontier 模型与 gpt-oss 系列。论文项目页也提示，今天的闭源前沿模型可能已针对具体攻击做了防御。</p></div>
        <div class="card risk"><b>探针不是最终真相</b><p>Role probes 是有用仪器，但探针能读出相关结构，不等于完全解释所有内部因果机制。</p></div>
        <div class="card risk"><b>防御仍未闭环</b><p>论文更强在诊断与理论，不是给出“一招解决 prompt injection”的工程方案。</p></div>
      </div>
      <p>所以更准确的结论不是“所有模型现在都会被这招打穿”，而是：只要模型没有真正稳固的角色感知，新的伪装方式就会不断出现。</p>
    </section>

    <section class="section">
      <h2>9. 产业影响分析</h2>
      <table>
        <tr><th>对象</th><th>可能受益/受冲击</th><th>应该关注什么</th></tr>
        <tr><td>企业 Agent 平台</td><td>受冲击最大。浏览网页、读邮件、跑 shell、查数据库都会接触不可信文本。</td><td>权限隔离、工具沙箱、审批链、不可由模型单独决定的敏感操作。</td></tr>
        <tr><td>模型厂商</td><td>会受益于新的评测方向：不只看拒答率，还看内部角色边界。</td><td>训练时让角色成为更硬的架构信号，而不是被风格轻易覆盖。</td></tr>
        <tr><td>安全创业公司</td><td>机会增加。传统 WAF 式过滤不够，需要面向 Agent 的上下文权限系统。</td><td>动态风险评分、tool output quarantine、最小权限、审计日志。</td></tr>
        <tr><td>产品经理</td><td>要重新理解“让 AI 自动操作”的边界。</td><td>把 AI 当建议引擎还是执行主体，是产品安全性的关键分水岭。</td></tr>
        <tr><td>投资研究者</td><td>Agent 安全可能成为基础设施赛道，而非边缘插件。</td><td>谁能把角色边界、权限系统、验证回路产品化。</td></tr>
      </table>
      <p>我的判断：这类研究会推动 AI 应用从“提示词工程”走向“权限工程”。未来的可靠 Agent 不会只是更会写 prompt，而是必须拥有像操作系统一样清晰的用户、进程、文件、网络和工具权限边界。</p>
    </section>

    <section class="section">
      <h2>10. 延伸阅读</h2>
      <ul class="source-list">
        <li><a href="https://arxiv.org/abs/2603.12277">原论文：Prompt Injection as Role Confusion</a></li>
        <li><a href="https://role-confusion.github.io/">作者项目页与长文：A Theory of Prompt Injection</a></li>
        <li><a href="https://github.com/role-confusion/prompt-injection-as-role-confusion">代码与 notebook：role-confusion/prompt-injection-as-role-confusion</a></li>
        <li><a href="https://simonwillison.net/2026/Jun/22/prompt-injection-as-role-confusion/">Simon Willison 对论文的评论</a></li>
        <li><a href="https://www.schneier.com/blog/archives/2026/06/interesting-paper-exploring-prompt-injection.html">Bruce Schneier：Interesting Paper Exploring Prompt Injection</a></li>
        <li><a href="https://arxiv.org/abs/2404.13208">相关背景：The Instruction Hierarchy</a></li>
        <li><a href="https://arxiv.org/abs/2605.30521">相关防御：Mock Tool Calls to Quarantine Untrusted Prompt Content</a></li>
      </ul>
    </section>

    <section class="section">
      <h2>11. 引用来源</h2>
      <ul class="source-list">
        <li>Ye, C., Cui, J., Hadfield-Menell, D. <i>Prompt Injection as Role Confusion</i>. arXiv:2603.12277. <a href="https://arxiv.org/abs/2603.12277">arXiv</a></li>
        <li>Role Confusion project page, accepted to ICML 2026. <a href="https://role-confusion.github.io/">role-confusion.github.io</a></li>
        <li>Local PDF text extraction from arXiv v6, used for exact experiment figures and methodology notes.</li>
        <li>Simon Willison, <i>Prompt Injection as Role Confusion</i>, 2026-06-22. <a href="https://simonwillison.net/2026/Jun/22/prompt-injection-as-role-confusion/">simonwillison.net</a></li>
        <li>Bruce Schneier, <i>Interesting Paper Exploring Prompt Injection</i>, 2026-06-25. <a href="https://www.schneier.com/blog/archives/2026/06/interesting-paper-exploring-prompt-injection.html">schneier.com</a></li>
        <li>The Register and Tom's Hardware reports were used only as attention/industry-discussion signals, not as primary technical sources.</li>
      </ul>
      <p class="note">中文图示为基于论文机制重新设计的解释图，不是原论文截图。报告目标是帮助非技术读者理解“为什么重要”，不是复刻论文排版。</p>
    </section>

    <p class="footer">AI每日论文精选 · 2026-07-03 · 面向普通读者、产品经理、创业者和投资研究者的 AI 前沿解释系统</p>
  </main>
</body>
</html>
"""

body = """今天精选的论文是 Prompt Injection as Role Confusion，来自 Charles Ye、Jasmine Cui 与 MIT 的 Dylan Hadfield-Menell，已被项目页标注为 ICML 2026。

它解释了一个非常关键的问题：
为什么 AI Agent 明明有 system/user/tool 等角色标签，却仍可能被网页、邮件或工具输出里的文字诱导越权？

一句话推荐理由：
这篇论文把“提示词注入”从提示技巧问题，推进为模型内部角色感知和 Agent 权限边界问题。

附件为中文深度拆解 HTML 报告，适合非技术读者、产品经理、创业者和投资研究者阅读。"""

OUT.write_text(html, encoding="utf-8")
SUBJECT.write_text("【AI每日论文精选】为什么AI分不清“谁在说话”？\n", encoding="utf-8")
BODY.write_text(body + "\n", encoding="utf-8")
print(OUT)
