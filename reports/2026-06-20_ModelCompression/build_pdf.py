from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from string import Template

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-20"
CONCEPT_CN = "模型压缩"
CONCEPT_EN = "Model Compression"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_ANALOGY = "chatgpt_model_compression_analogy.png"
FIG_WORKFLOW = "chatgpt_model_compression_workflow.png"


WHY = [
    "今天我们先从一个很现实的问题开始：为什么很多大模型很聪明，却很难直接放进手机、汽车、家用设备或普通公司的服务器里？原因不是它们不会回答，而是它们太大、太贵、太耗电。",
    "一个大模型就像一座巨大的图书馆。它里面有很多有用知识，也有大量重复、相近、使用频率很低的部分。如果每次回答问题都要搬动整座图书馆，当然慢，也当然贵。",
    "模型压缩要解决的，就是让模型在尽量保留能力的前提下变小、变快、变省。它不是把模型随便砍掉一块，而是像高级整理师一样，判断哪些能力必须保留，哪些冗余可以减少，哪些计算可以换一种更轻的方式表达。",
    "这件事改变了 AI 的落地方式。没有压缩，大模型更像云端机房里的重型设备；有了压缩，AI 才更可能进入手机助手、车载系统、企业私有部署、离线客服、边缘设备和实时应用。",
]

ANALOGY = [
    "想象你要出门旅行一个月。第一次收拾行李时，你把所有东西都塞进一个巨大的箱子：五双鞋、十件外套、三套充电器、很多也许用得上的小物件。箱子确实什么都有，但太重，拖起来很慢，托运也很贵。",
    "后来你请来一位很会整理的人。她不会简单地把东西扔掉，而是先问：哪些东西每天都要用？哪些东西功能重复？哪些可以换成更轻的版本？哪些可以到了当地再找替代品？整理之后，箱子变小了，但旅行仍然顺利。",
    "模型压缩也是这样。原始大模型像那个超重行李箱，里面装满了参数、计算和能力。压缩方法像整理策略：剪枝删掉不太重要的连接，量化把精度换成更省空间的表示，蒸馏让小模型学习大模型的做题方式，低秩分解把复杂矩阵拆成更轻的组合。",
    "真正的目标不是“越小越好”，而是“变小以后仍然够好用”。如果压缩到最后模型回答质量大幅下降，就像旅行箱轻了，但护照、药品、充电器都被扔掉了，那就失败了。",
]

MECHANISM = [
    ("先评估原始模型", "工程师会先测量模型大小、显存占用、生成速度、准确率和典型任务表现。没有这些基准，就不知道压缩后到底是进步还是退步。"),
    ("找到冗余部分", "大模型里并不是每个参数都同样重要。有些连接长期影响很小，有些层可以近似替代，有些数字精度远高于实际需要。"),
    ("选择压缩策略", "常见策略包括剪枝、量化、蒸馏、低秩分解和结构替换。不同策略像不同整理工具，适合解决不同类型的臃肿。"),
    ("重新训练或校准", "很多压缩不是一剪了之。模型变小后，通常还要用数据进行微调、校准或蒸馏训练，让它重新适应新的身体。"),
    ("测试真实任务", "压缩后的模型必须回到真实场景里测试，例如客服问答、摘要、代码补全、设备识别。只看一个排行榜分数往往不够。"),
    ("部署并持续监控", "模型上线后还要看延迟、成本、错误率、用户体验和异常案例。如果效果下降超过可接受范围，就要回滚或重新压缩。"),
]

METHODS = [
    ("剪枝 Pruning", "专业解释：移除对输出影响较小的权重、连接、神经元或注意力头。", "白话解释：像把很少用、占地方的行李拿出来，但保留关键物品。"),
    ("量化 Quantization", "专业解释：用更低位数表示模型权重或激活值，例如从 32 位浮点数降到 8 位或 4 位。", "白话解释：像把高清大图压成清晰够用的小图，体积小很多。"),
    ("知识蒸馏 Distillation", "专业解释：让小模型学习大模型的输出分布、推理习惯或中间表示。", "白话解释：像名师带学生，让学生学会老师解题的套路。"),
    ("低秩分解 Low-rank Factorization", "专业解释：把大型矩阵近似拆成几个更小矩阵的乘积，减少参数和计算。", "白话解释：像把一张复杂大表拆成几张更简单的小表，还能拼出接近的结果。"),
    ("稀疏化 Sparsity", "专业解释：让模型中的大量权重变为零或可跳过，从而减少实际计算。", "白话解释：像地图上很多小路平时不走，导航就不必每次都检查它们。"),
    ("结构化压缩 Structured Compression", "专业解释：按通道、层、模块等结构单位压缩，方便硬件真正加速。", "白话解释：不是零碎地删几颗螺丝，而是直接换成更轻的模块。"),
]

TERMS = [
    ("参数 Parameter", "专业解释：模型训练后保存下来的数字权重，决定模型如何处理输入。", "白话解释：像模型脑子里的经验刻度。"),
    ("权重 Weight", "专业解释：神经网络连接上的数值，用来表示某个信号的重要程度。", "白话解释：像老师批改时给不同线索打的分量。"),
    ("显存 VRAM", "专业解释：GPU 上用于存放模型、缓存和计算中间结果的高速内存。", "白话解释：像工作台，台面越小，越放不下大模型。"),
    ("延迟 Latency", "专业解释：从用户发出请求到收到响应之间的等待时间。", "白话解释：你问 AI 以后要等多久。"),
    ("吞吐量 Throughput", "专业解释：系统单位时间内能处理的请求数或生成的 token 数。", "白话解释：同一批机器一小时能服务多少人。"),
    ("精度 Precision", "专业解释：数字表示的细致程度，例如 32 位、16 位、8 位、4 位。", "白话解释：像尺子的刻度，刻度越细越精确，但也更占空间。"),
    ("校准 Calibration", "专业解释：压缩后用少量数据调整量化范围或模型行为，减少误差。", "白话解释：像换了新秤以后重新调零。"),
    ("微调 Fine-tuning", "专业解释：在特定数据上继续训练模型，让它适应目标任务。", "白话解释：像学生学完通识课后，再做专项训练。"),
    ("边缘设备 Edge Device", "专业解释：靠近用户或现场运行计算的设备，例如手机、摄像头、车载芯片。", "白话解释：不是把问题都送到云端，而是在你身边的小机器上处理。"),
    ("质量退化 Quality Degradation", "专业解释：压缩后模型在准确率、稳定性、推理能力或安全性上的下降。", "白话解释：箱子轻了，但关键东西丢了。"),
]

CASE = [
    "一个真实应用案例是手机里的 AI 助手。用户希望它能离线总结通知、识别图片、改写短句、回答简单问题。如果每次都把请求发到云端，可能有网络延迟、隐私风险和服务器成本。",
    "但完整大模型通常放不进手机芯片和内存。于是工程团队会先选择一个能力合适的模型，再使用量化减少存储和计算，用蒸馏训练更小版本，用剪枝或结构化压缩去掉不重要模块，最后在真实手机上测试耗电、发热、响应速度和回答质量。",
    "如果压缩做得好，用户看到的是更快的本地 AI：不联网也能做一些任务，隐私数据不用离开设备，电量消耗可控。公司看到的是更低的云端成本和更稳定的体验。",
    "如果压缩做得不好，问题也很明显：模型可能更容易答错、漏掉重要信息、在少数场景里突然失灵。所以模型压缩永远不是只看文件大小，而是要看真实任务是否仍然可靠。",
]

MISTAKES = [
    ("误区一：模型压缩就是把模型随便删小。", "不是。真正的压缩要保留关键能力，并通过测试证明变小以后仍然可用。"),
    ("误区二：压缩后的模型一定更差。", "不一定。适度压缩有时几乎不影响体验，甚至因为部署更快、更稳定而让产品更好用。"),
    ("误区三：模型越小越好。", "不对。太小可能丢掉推理能力、语言能力或安全边界。目标是合适大小，不是最小大小。"),
    ("误区四：量化等于全部模型压缩。", "量化只是压缩方法之一。剪枝、蒸馏、低秩分解、稀疏化也很常见。"),
    ("误区五：压缩只适合手机。", "不是。云端服务也需要压缩，因为它直接影响 GPU 成本、吞吐量、延迟和能耗。"),
    ("误区六：只要排行榜分数没掉就安全。", "不够。真实应用还要看长文本、边界问题、安全回答、少数语言、行业术语和异常输入。"),
    ("误区七：压缩可以让模型学会新知识。", "一般不会。压缩主要是让已有能力更轻量；新增知识通常依赖训练、检索或工具系统。"),
    ("误区八：压缩一次就结束。", "不是。模型、硬件、任务和用户需求都会变化，压缩方案也要持续评估和迭代。"),
]

SUMMARY = [
    "模型压缩的本质，是在尽量保留能力的前提下，让模型变小、变快、变省。",
    "它常用剪枝、量化、蒸馏、低秩分解等方法，不是简单删除，而是有目标地减少冗余。",
    "压缩成功的标准不是文件最小，而是在真实场景里仍然够准确、够稳定、够便宜、够快。",
]

QUIZ = [
    "为什么说模型压缩更像“整理行李箱”，而不是“把东西越扔越多”？",
    "请比较模型量化和知识蒸馏：它们都能让模型变小，但思路有什么不同？",
    "如果一个压缩模型在排行榜上分数还不错，但手机上经常发热、回答慢，你会从哪些角度重新评估它？",
]


def image_data_uri(name: str) -> str:
    data = (ROOT / name).read_bytes()
    return f"data:image/png;base64,{base64.b64encode(data).decode('ascii')}"


def paras(items: list[str]) -> str:
    return "\n".join(f"<p>{escape(item)}</p>" for item in items)


def step_cards() -> str:
    cards: list[str] = []
    for idx, (title, body) in enumerate(MECHANISM, 1):
        cards.append(
            f"""
            <article class="step-card">
              <div class="step-num">{idx}</div>
              <div>
                <h3>{escape(title)}</h3>
                <p>{escape(body)}</p>
              </div>
            </article>
            """
        )
    return "\n".join(cards)


def method_cards() -> str:
    cards: list[str] = []
    for name, pro, plain in METHODS:
        cards.append(
            f"""
            <article class="method-card">
              <h3>{escape(name)}</h3>
              <p><strong>专业解释：</strong>{escape(pro.removeprefix("专业解释："))}</p>
              <p><strong>白话解释：</strong>{escape(plain.removeprefix("白话解释："))}</p>
            </article>
            """
        )
    return "\n".join(cards)


def term_rows() -> str:
    return "\n".join(
        f"<tr><th>{escape(term)}</th><td>{escape(pro)}</td><td>{escape(plain)}</td></tr>"
        for term, pro, plain in TERMS
    )


def mistake_items() -> str:
    return "\n".join(
        f"<li><strong>{escape(title)}</strong><span>{escape(body)}</span></li>"
        for title, body in MISTAKES
    )


def numbered(items: list[str]) -> str:
    return "\n".join(f"<li>{escape(item)}</li>" for item in items)


def build_html() -> str:
    toc = [
        ("why", "为什么重要"),
        ("analogy", "直观类比"),
        ("mechanism", "工作原理"),
        ("terms", "关键术语"),
        ("case", "真实案例"),
        ("mistakes", "常见误区"),
        ("summary", "3句话总结"),
        ("quiz", "复习问题"),
    ]
    toc_html = "\n".join(f'<a href="#{slug}">{label}</a>' for slug, label in toc)
    template = Template(
        """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${date}_${concept_full}</title>
  <style>
    :root {
      --ink: #101827;
      --muted: #475569;
      --quiet: #64748b;
      --line: #d7e0ea;
      --paper: #ffffff;
      --soft: #f8fafc;
      --blue: #123872;
      --teal: #0f8b8d;
      --green: #237a57;
      --amber: #a16207;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: #eef3f8;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      line-height: 1.76;
    }
    .cover {
      min-height: 100vh;
      padding: 58px 26px 42px;
      background: linear-gradient(180deg, #ffffff 0%, #f6fbff 56%, #edf7f6 100%);
      border-bottom: 1px solid var(--line);
    }
    .wrap { max-width: 1080px; margin: 0 auto; }
    .eyebrow {
      color: var(--teal);
      font-size: 15px;
      font-weight: 820;
      letter-spacing: 0;
    }
    h1 {
      max-width: 980px;
      margin: 18px 0 14px;
      color: var(--ink);
      font-size: clamp(42px, 6vw, 74px);
      line-height: 1.08;
      letter-spacing: 0;
    }
    h1 span { color: var(--blue); }
    .subtitle {
      max-width: 920px;
      margin: 0;
      color: var(--muted);
      font-size: clamp(22px, 3vw, 32px);
      line-height: 1.35;
      font-weight: 680;
    }
    .core {
      max-width: 980px;
      margin-top: 28px;
      padding: 18px 22px;
      border: 1px solid #99f6e4;
      border-left: 8px solid var(--teal);
      border-radius: 8px;
      background: #f0fdfa;
      color: #0f766e;
      font-size: 20px;
      font-weight: 820;
    }
    .cover-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-top: 34px;
    }
    .cover-card {
      min-height: 150px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,.92);
      padding: 18px;
    }
    .cover-card b {
      display: block;
      color: var(--blue);
      font-size: 20px;
      margin-bottom: 8px;
    }
    .cover-card p {
      margin: 0;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.65;
    }
    nav {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 10px;
      margin-top: 30px;
    }
    nav a {
      display: block;
      padding: 10px 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      color: var(--blue);
      font-weight: 760;
      text-decoration: none;
    }
    main { padding: 34px 26px 80px; }
    section {
      max-width: 1080px;
      margin: 0 auto 28px;
      padding: 30px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--paper);
    }
    h2 {
      margin: 0 0 16px;
      color: var(--ink);
      font-size: 32px;
      line-height: 1.25;
      letter-spacing: 0;
    }
    h3 {
      margin: 0 0 6px;
      color: var(--blue);
      font-size: 20px;
      line-height: 1.3;
      letter-spacing: 0;
    }
    p { margin: 12px 0; font-size: 18px; }
    .lead {
      color: var(--muted);
      font-size: 20px;
      font-weight: 700;
    }
    figure { margin: 20px 0 8px; break-inside: avoid; }
    img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
    }
    figcaption {
      margin-top: 8px;
      color: var(--quiet);
      font-size: 14px;
    }
    .steps {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 18px;
    }
    .step-card {
      display: grid;
      grid-template-columns: 50px 1fr;
      gap: 14px;
      min-height: 138px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdff;
      break-inside: avoid;
    }
    .step-num {
      display: grid;
      place-items: center;
      width: 42px;
      height: 42px;
      border-radius: 8px;
      background: var(--blue);
      color: white;
      font-weight: 900;
    }
    .step-card p {
      margin: 0;
      color: var(--muted);
      font-size: 16px;
    }
    .method-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 18px;
    }
    .method-card {
      min-height: 142px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fafc;
      break-inside: avoid;
    }
    .method-card p {
      margin: 7px 0 0;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.58;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      font-size: 15.5px;
    }
    th, td {
      border: 1px solid var(--line);
      padding: 12px;
      vertical-align: top;
    }
    th {
      width: 22%;
      background: #f8fafc;
      color: var(--blue);
      text-align: left;
    }
    ul, ol { padding-left: 24px; }
    li {
      margin: 10px 0;
      font-size: 18px;
    }
    .mistakes {
      list-style: none;
      padding: 0;
      margin: 8px 0 0;
    }
    .mistakes li {
      border: 1px solid var(--line);
      border-left: 6px solid var(--amber);
      border-radius: 8px;
      padding: 13px 16px;
      background: #fffaf0;
      break-inside: avoid;
    }
    .mistakes strong {
      display: block;
      color: #92400e;
      margin-bottom: 4px;
    }
    .mistakes span { color: var(--muted); }
    .note {
      margin-top: 18px;
      padding: 16px 18px;
      border: 1px solid #bfdbfe;
      border-radius: 8px;
      background: #eff6ff;
      color: var(--blue);
      font-size: 18px;
      font-weight: 760;
    }
    .summary-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
    }
    .summary-card {
      min-height: 172px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fafc;
      font-size: 17px;
      font-weight: 730;
    }
    .callout {
      margin: 18px 0 0;
      padding: 16px 18px;
      border: 1px solid #bbf7d0;
      border-radius: 8px;
      background: #f0fdf4;
      color: #166534;
      font-size: 18px;
      font-weight: 760;
    }
    footer {
      max-width: 1080px;
      margin: 0 auto;
      padding: 8px 30px 34px;
      color: var(--quiet);
      font-size: 14px;
    }
    @page { size: A4; margin: 15mm 13mm 17mm; }
    @media print {
      body { background: #fff; }
      .cover {
        min-height: 238mm;
        padding: 0;
        border-bottom: 0;
        break-after: page;
      }
      .cover .wrap { padding-top: 8mm; }
      h1 { font-size: 50px; margin: 12px 0 10px; }
      .subtitle { font-size: 21px; line-height: 1.32; }
      .core { margin-top: 16px; padding: 12px 16px; }
      .cover-grid { gap: 9px; margin-top: 16px; }
      .cover-card { min-height: 88px; padding: 12px; }
      .cover-card b { font-size: 16px; margin-bottom: 4px; }
      nav {
        grid-template-columns: repeat(4, 1fr);
        gap: 7px;
        margin-top: 14px;
      }
      main { padding: 0; }
      section {
        max-width: none;
        margin: 0 0 10mm;
        padding: 0;
        border: 0;
        border-radius: 0;
        break-inside: avoid;
      }
      .steps, .method-grid { grid-template-columns: repeat(2, 1fr); }
      .step-card { min-height: 116px; }
      .method-card { min-height: 120px; }
      p, li { font-size: 14.5px; line-height: 1.65; }
      h2 { font-size: 24px; }
      h3 { font-size: 17px; }
      table { font-size: 12px; }
      th, td { padding: 8px; }
      .summary-card { min-height: 128px; font-size: 13px; }
      .cover-card p { font-size: 13px; }
      .core { font-size: 17px; }
      nav a { font-size: 13px; padding: 7px 10px; }
      .callout, .note { font-size: 14px; }
      footer { display: none; }
    }
    @media (max-width: 760px) {
      .cover-grid, .steps, .method-grid, .summary-grid { grid-template-columns: 1fr; }
      section { padding: 22px; }
      main { padding: 24px 16px 56px; }
      .cover { padding: 44px 18px 32px; }
    }
  </style>
</head>
<body>
  <header class="cover">
    <div class="wrap">
      <div class="eyebrow">AI每日深度科普 · ${date}</div>
      <h1>模型压缩<br><span>Model Compression</span></h1>
      <p class="subtitle">为什么 AI 可以“瘦身”以后，跑进手机、汽车和普通服务器？</p>
      <div class="core">核心一句话：模型压缩的本质，是在尽量保留能力的前提下，减少模型的体积、计算和运行成本。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>它解决什么？</b><p>解决大模型太大、太贵、太耗电，难以广泛部署的问题。</p></div>
        <div class="cover-card"><b>它改变什么？</b><p>让 AI 从云端重型设备，走向手机、车载、企业本地和边缘设备。</p></div>
        <div class="cover-card"><b>今天怎么学？</b><p>用“整理行李箱”的类比，看懂剪枝、量化、蒸馏和工程取舍。</p></div>
      </div>
      <nav aria-label="目录">
        ${toc}
      </nav>
    </div>
  </header>

  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">模型压缩解释的是：AI 如何从“机房里的庞然大物”，变成可以被真实产品反复调用的能力。</p>
      ${why}
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：整理行李箱</h2>
      ${analogy}
      <figure>
        <img src="${fig_analogy}" alt="模型压缩类比：原始大模型像超重行李箱，通过剪枝、量化、蒸馏变成更小模型">
        <figcaption>图解：压缩不是粗暴扔东西，而是保留关键能力、减少重复和冗余，让模型更轻但仍然好用。</figcaption>
      </figure>
      <div class="note">一句话判断：压缩成功不是“最小”，而是“足够小，同时仍然可靠”。</div>
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：模型怎样被聪明瘦身？</h2>
      <p class="lead">压缩是一套工程流程，不是一个按钮。它先测量，再减少冗余，最后回到真实任务里验证。</p>
      <div class="steps">
        ${steps}
      </div>
      <figure>
        <img src="${fig_workflow}" alt="模型压缩工作流程：评估原始模型、找到冗余部分、选择压缩策略、重新测试效果、部署到真实场景">
        <figcaption>图解：模型压缩要在体积、速度、成本、准确率之间取平衡。</figcaption>
      </figure>
      <div class="callout">最关键的直觉：模型压缩不是牺牲一切换小体积，而是在真实场景里找到可接受的平衡点。</div>
      <div class="method-grid">
        ${methods}
      </div>
    </section>

    <section id="terms">
      <h2>4. 关键术语解释</h2>
      <table>
        <thead>
          <tr><th>术语</th><th>一句专业解释</th><th>一句白话解释</th></tr>
        </thead>
        <tbody>
          ${terms}
        </tbody>
      </table>
    </section>

    <section id="case">
      <h2>5. 一个真实应用案例：手机里的 AI 助手</h2>
      ${case}
    </section>

    <section id="mistakes">
      <h2>6. 常见误区</h2>
      <ul class="mistakes">
        ${mistakes}
      </ul>
    </section>

    <section id="summary">
      <h2>7. 3句话总结</h2>
      <div class="summary-grid">
        <div class="summary-card">1. ${summary_1}</div>
        <div class="summary-card">2. ${summary_2}</div>
        <div class="summary-card">3. ${summary_3}</div>
      </div>
    </section>

    <section id="quiz">
      <h2>8. 复习问题</h2>
      <ol>
        ${quiz}
      </ol>
    </section>
  </main>

  <footer>© 2026 AI每日深度科普 · 本文面向非技术读者，用生活化方式解释 AI 核心概念。</footer>
</body>
</html>
"""
    )
    return template.substitute(
        date=DATE,
        concept_full=escape(CONCEPT_FULL),
        toc=toc_html,
        why=paras(WHY),
        analogy=paras(ANALOGY),
        steps=step_cards(),
        methods=method_cards(),
        terms=term_rows(),
        case=paras(CASE),
        mistakes=mistake_items(),
        summary_1=escape(SUMMARY[0]),
        summary_2=escape(SUMMARY[1]),
        summary_3=escape(SUMMARY[2]),
        quiz=numbered(QUIZ),
        fig_analogy=image_data_uri(FIG_ANALOGY),
        fig_workflow=image_data_uri(FIG_WORKFLOW),
    )


def write_email_files() -> None:
    (ROOT / "email_subject.txt").write_text(
        "【AI每日深度科普】模型压缩：为什么 AI 可以被聪明瘦身？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        "\n".join(
            [
                "今天的主题是 模型压缩（Model Compression）。",
                "",
                "这是大模型从实验室和云端机房走向手机、车载设备、企业私有部署和边缘场景的关键工程能力之一。",
                "",
                "附件内容将用“整理行李箱”的生活化方式解释：",
                "为什么压缩不是简单删小，而是在体积、速度、成本、准确率之间做平衡；",
                "以及剪枝、量化、蒸馏、低秩分解分别在解决什么问题。",
                "",
                "适合：非技术读者、AI初学者、产品经理、投资研究者和关注 AI 落地成本的人阅读。",
            ]
        ),
        encoding="utf-8",
    )


def render_pdf() -> None:
    html_path = ROOT / HTML_NAME
    pdf_path = ROOT / PDF_NAME
    html_path.write_text(build_html(), encoding="utf-8")
    write_email_files()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1600}, device_scale_factor=1)
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.screenshot(path=str(ROOT / "html_preview.png"), full_page=False)
        scroll_height = page.evaluate("document.documentElement.scrollHeight")
        y = max(0, min(int(scroll_height * 0.43), max(0, int(scroll_height) - 1600)))
        page.evaluate("(scrollY) => window.scrollTo(0, scrollY)", y)
        page.wait_for_timeout(250)
        page.screenshot(path=str(ROOT / "html_midpage_preview.png"), full_page=False)
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "15mm", "right": "13mm", "bottom": "17mm", "left": "13mm"},
            prefer_css_page_size=True,
        )
        browser.close()


if __name__ == "__main__":
    render_pdf()
