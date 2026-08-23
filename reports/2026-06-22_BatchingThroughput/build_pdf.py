from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from string import Template

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-22"
CONCEPT_CN = "批处理与吞吐量"
CONCEPT_EN = "Batching and Throughput"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_ANALOGY = "chatgpt_batching_analogy.png"
FIG_WORKFLOW = "chatgpt_batching_workflow.png"


WHY = [
    "先想一个日常场景：晚上八点，几百万人同时打开 AI 助手。有的人问一句话，有的人上传一段长文，有的人让 AI 写代码。服务器如果像小摊老板一样“来一个人就单独开火做一次”，很快就会又慢又贵。",
    "批处理与吞吐量要解决的，就是 AI 服务的规模问题：怎样让同一块 GPU 在同一段时间里服务更多请求，同时又不让用户等得太久。",
    "这不是一个边角料概念。它直接决定了 AI 产品能不能在高峰期稳定运行、每次回答的成本有多高、企业能不能把大模型真正用到客服、办公、搜索、编程和数据分析里。",
    "理解它之后，你会明白：AI 的体验不只取决于模型聪不聪明，还取决于背后的交通调度。一个好模型，如果排队、分组和算力利用做得不好，也会像高速路收费站堵车一样让人焦躁。",
]

ANALOGY = [
    "想象一家很忙的餐厅。中午高峰时，顾客不断下单：有人点牛肉面，有人点盖饭，有人点蒸饺。如果厨师每接一单就单独洗锅、开火、备料、出餐，厨房会被大量重复动作拖慢。",
    "更聪明的做法是：服务员先把订单放进队列，厨房在很短时间内把相似订单凑成一批。比如三碗牛肉面一起煮，两份盖饭一起炒，一笼蒸饺一起蒸。每个顾客的餐仍然分开送回，但厨房一次动作服务了更多人。",
    "AI 服务里的批处理也是这个意思。用户请求进入队列后，调度器会在极短时间内把多个请求组成一个“微批次”，让 GPU 一次并行计算。GPU 特别擅长同时处理大量矩阵运算，就像大厨房的大灶台适合一次做多份。",
    "但餐厅也不能为了凑满一锅，让第一个顾客等半小时。所以批处理的真正难点不是“批越大越好”，而是在低延迟和高吞吐之间找到平衡点：既让用户感觉快，又让算力不空转。",
]

MECHANISM = [
    ("请求进入队列", "用户的问题、文档或图片请求先进入服务队列。系统会记录它们的到达时间、长度、优先级和预计计算量。"),
    ("调度器短暂等待", "调度器不会无限等，而是在几毫秒到几十毫秒的窗口里观察新请求。它像餐厅前台，决定哪些订单适合一起处理。"),
    ("组成微批次", "多个请求被打包成一个 micro-batch。短请求和长请求可能被分到不同批次，避免一个特别长的请求拖慢所有人。"),
    ("GPU 并行计算", "GPU 一次处理整批请求里的矩阵运算。对 GPU 来说，一次算一份常常不够“吃饱”，一批一起算才能提高利用率。"),
    ("解码时持续重组", "生成文字时，有的回答很快结束，有的还在继续。连续批处理会不断把结束的位置腾出来，让新请求插入，减少空位浪费。"),
    ("拆分结果返回", "批次只是计算时的临时组合。计算完后，系统会把每个用户的结果拆开，按原来的请求分别返回。"),
    ("监控并调参", "工程团队会监控延迟、吞吐、错误率、GPU 利用率和成本，再调整最大批大小、等待时间和优先级策略。"),
]

TERMS = [
    ("请求 Request", "专业解释：一次用户输入触发的模型服务调用。", "白话解释：用户向 AI 点的一份单。"),
    ("延迟 Latency", "专业解释：从请求发出到开始或完成响应所经历的时间。", "白话解释：你等 AI 回答要等多久。"),
    ("吞吐量 Throughput", "专业解释：系统在单位时间内能处理的请求数或 token 数。", "白话解释：这家 AI 餐厅一分钟能服务多少人、做出多少字。"),
    ("批 Batch", "专业解释：被合并在同一次计算中处理的一组样本或请求。", "白话解释：把几份订单临时放在同一个托盘上处理。"),
    ("微批次 Micro-batch", "专业解释：在线推理中为了兼顾等待时间和算力利用而形成的小批量请求。", "白话解释：只等一小会儿，凑够几单就开做。"),
    ("动态批处理 Dynamic Batching", "专业解释：根据实时到达的请求长度、数量和负载动态决定如何组批。", "白话解释：不是固定每十单一锅，而是看现场情况灵活拼单。"),
    ("连续批处理 Continuous Batching", "专业解释：在生成式模型解码过程中持续插入新请求、移除已完成请求的调度方法。", "白话解释：有人吃完离席，就马上安排下一个人坐进来。"),
    ("GPU 利用率 GPU Utilization", "专业解释：GPU 计算资源在运行期间被有效使用的比例。", "白话解释：昂贵的大灶台到底是在忙，还是在空等。"),
    ("SLA 服务承诺", "专业解释：系统对响应时间、可用性或成功率的服务水平要求。", "白话解释：产品承诺用户“最多等多久、能不能稳定用”。"),
    ("Token 吞吐", "专业解释：模型每秒能生成或处理的 token 数量。", "白话解释：AI 每秒能读写多少小文字块。"),
    ("排队时间 Queue Time", "专业解释：请求进入系统后，在被实际计算前等待调度的时间。", "白话解释：你在餐厅门口等叫号的时间。"),
    ("填充 Padding", "专业解释：为了让不同长度输入放入同一批计算而补齐长度的技术。", "白话解释：把长短不一的纸条垫到相同宽度，机器才好整齐处理。"),
]

CASE = [
    "一个真实应用案例是高峰期的 AI 客服。假设一家电商在促销日同时收到十万条咨询：有人问退货，有人问物流，有人要求总结聊天记录。所有请求如果逐个单独跑模型，GPU 会频繁等待，成本会非常高。",
    "更常见的做法是：请求先进入队列，调度器把相似长度和相近优先级的请求组成微批次。GPU 一次并行计算这一批，生成结果后再拆分给不同用户。对用户来说，自己仍然是在和 AI 一对一对话；对系统来说，背后是很多请求一起搭了一趟车。",
    "如果系统发现队列变长，会适当增大批次或调更多 GPU；如果用户开始感觉等待明显变久，就会缩短等待窗口，优先保证交互体验。企业真正关心的不是单次演示有多快，而是高峰期能不能稳定、成本是否可控。",
    "ChatGPT、AI 搜索、代码助手、智能客服和企业知识库问答都需要类似思想。区别只是在不同场景中，延迟和吞吐的权重不同：聊天更重视体感速度，离线文档分析更能接受较大批次。",
]

MISTAKES = [
    ("误区一：批处理会让模型变聪明。", "不会。批处理主要提升服务效率和成本表现，不直接改变模型能力。聪明程度更多来自模型结构、训练数据和对齐方法。"),
    ("误区二：批越大一定越好。", "不一定。批越大，GPU 利用率可能更高，但第一个进队列的人可能等更久。真实系统要在延迟和吞吐之间取平衡。"),
    ("误区三：批处理只发生在训练阶段。", "不是。训练常用 batch，在线推理同样需要 batch，只是推理更在意用户等待时间。"),
    ("误区四：批处理等于把多个用户的问题合并成一个问题。", "不是。请求只是计算时临时打包，结果和上下文仍然要分开管理。"),
    ("误区五：GPU 很快，所以不需要排队调度。", "恰恰相反。GPU 快但贵，若每次只处理很小请求，就像大巴车只坐一个人出发，浪费明显。"),
    ("误区六：流式输出就不能批处理。", "可以。连续批处理能让正在生成的请求和新来的请求共同调度，只是实现更复杂。"),
    ("误区七：吞吐量高就代表用户体验好。", "不一定。后台批量任务可以追求高吞吐，但聊天产品还要看首字响应时间和整体等待感。"),
    ("误区八：批处理只是工程细节，普通人不用懂。", "值得懂。它解释了为什么同一个 AI 产品有时很快、有时排队，也解释了为什么 AI 服务价格会随算力效率下降。"),
]

SUMMARY = [
    "批处理的本质，是把多个零散请求临时凑成一批，让 GPU 一次并行服务更多人。",
    "吞吐量衡量系统单位时间能处理多少工作，但它必须和用户等待时间一起看。",
    "成熟的 AI 服务不是只靠大模型，而是靠模型、GPU、队列、调度器和成本控制共同运转。",
]

QUIZ = [
    "为什么餐厅“拼单一起做”的类比能帮助理解 AI 批处理？它和用户一对一聊天是否矛盾？",
    "如果一个 AI 系统吞吐量很高，但用户抱怨等待时间变长，你认为问题可能出在哪里？",
    "聊天助手、离线文档批量总结、自动客服高峰期，这三个场景的批大小策略应该一样吗？为什么？",
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
      background: linear-gradient(180deg, #ffffff 0%, #f7fbff 58%, #edf7f6 100%);
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
      .steps { grid-template-columns: repeat(2, 1fr); }
      .step-card { min-height: 116px; }
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
      .cover-grid, .steps, .summary-grid { grid-template-columns: 1fr; }
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
      <h1>批处理与吞吐量<br><span>Batching and Throughput</span></h1>
      <p class="subtitle">为什么 AI 服务要学会“拼车”，而不是每个请求单独出发？</p>
      <div class="core">核心一句话：批处理的本质，是把多个零散请求临时凑成一批，让昂贵的 GPU 一次并行服务更多人。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>它解决什么？</b><p>解决高峰期请求太多、GPU 空转浪费、单次服务成本过高的问题。</p></div>
        <div class="cover-card"><b>它改变什么？</b><p>让 AI 产品从“能演示”走向“能大规模稳定服务”。</p></div>
        <div class="cover-card"><b>今天怎么学？</b><p>用餐厅拼单和大巴拼车的直觉，看懂延迟与吞吐的平衡。</p></div>
      </div>
      <nav aria-label="目录">
        ${toc}
      </nav>
    </div>
  </header>

  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">批处理与吞吐量解释的是：为什么 AI 服务背后需要排队、拼单和调度，而不只是“大模型回答问题”。</p>
      ${why}
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：餐厅拼单出餐</h2>
      ${analogy}
      <figure>
        <img src="${fig_analogy}" alt="批处理类比图：把零散订单凑成一批，一起出餐，提升吞吐量">
        <figcaption>图解：餐厅不会每份订单都单独开一口锅；AI 服务也会把多个请求临时打包，让算力更高效。</figcaption>
      </figure>
      <div class="callout">最关键的直觉：批处理不是牺牲用户，而是在“不让人等太久”的前提下，让同一块算力一次服务更多请求。</div>
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：从请求队列到 GPU 并行计算</h2>
      <p class="lead">AI 服务里的批处理，本质是一套实时交通调度系统：排队、分组、并行计算、拆分返回。</p>
      <figure>
        <img src="${fig_workflow}" alt="AI服务批处理流水线：请求队列、调度器、微批次、GPU并行计算、结果返回">
        <figcaption>图解：调度器把请求组成微批次，让 GPU 一次处理更多工作；同时必须控制等待时间。</figcaption>
      </figure>
      <div class="steps">
        ${steps}
      </div>
      <div class="note">注意：真正难的是实时平衡。批太小，GPU 吃不饱；批太大，用户等太久。好的系统会按负载动态调整。</div>
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
      <h2>5. 一个真实应用案例：促销日的 AI 客服</h2>
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
        <div class="summary-card">1. ${summary1}</div>
        <div class="summary-card">2. ${summary2}</div>
        <div class="summary-card">3. ${summary3}</div>
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
        concept_full=CONCEPT_FULL,
        toc=toc_html,
        why=paras(WHY),
        analogy=paras(ANALOGY),
        fig_analogy=image_data_uri(FIG_ANALOGY),
        fig_workflow=image_data_uri(FIG_WORKFLOW),
        steps=step_cards(),
        terms=term_rows(),
        case=paras(CASE),
        mistakes=mistake_items(),
        summary1=escape(SUMMARY[0]),
        summary2=escape(SUMMARY[1]),
        summary3=escape(SUMMARY[2]),
        quiz=numbered(QUIZ),
    )


def write_text_files() -> None:
    (ROOT / "email_subject.txt").write_text(
        "【AI每日深度科普】批处理与吞吐量：为什么 AI 服务要学会“拼车”？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        """今天的主题是 批处理与吞吐量（Batching and Throughput）。

它解释了一个非常现实的问题：
为什么 AI 服务在高峰期不能每个请求都单独计算，而要像餐厅拼单、出行拼车一样，把多个请求临时凑成一批。

附件内容将用生活化方式解释：
批处理如何提升 GPU 利用率、降低服务成本；
吞吐量为什么不能脱离延迟单独看；
以及为什么成熟的 AI 产品背后一定有队列、调度器和实时平衡。

适合：非技术读者、AI初学者、产品经理、投资研究者和关注 AI 工程落地的人阅读。""",
        encoding="utf-8",
    )


def main() -> None:
    html = build_html()
    html_path = ROOT / HTML_NAME
    pdf_path = ROOT / PDF_NAME
    html_path.write_text(html, encoding="utf-8")
    write_text_files()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1600}, device_scale_factor=1)
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
        )
        page.screenshot(path=str(ROOT / "html_preview.png"), full_page=True)
        browser.close()

    print(f"Wrote {html_path}")
    print(f"Wrote {pdf_path}")


if __name__ == "__main__":
    main()
