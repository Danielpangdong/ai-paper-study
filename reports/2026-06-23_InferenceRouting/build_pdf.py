from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from string import Template

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-23"
CONCEPT_CN = "推理路由"
CONCEPT_EN = "Inference Routing"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_ANALOGY = "chatgpt_inference_routing_analogy.png"
FIG_WORKFLOW = "chatgpt_inference_routing_workflow.png"


WHY = [
    "你打开一个 AI 助手时，背后可能不止一个模型在工作。有的问题很简单，比如翻译一句话；有的问题很复杂，比如分析一份合同；有的问题需要查资料，有的问题涉及图片、语音或隐私安全。",
    "如果每个问题都交给最大、最贵、最慢的模型处理，就像医院里每个病人都直接去找顶级专家。结果是专家被挤爆，简单问题也要排队，成本还会高到产品难以长期运行。",
    "推理路由要解决的，就是 AI 服务的分诊问题：来了一个请求，系统先判断它是什么任务、难不难、急不急、有没有风险，然后把它送到最合适的路线。",
    "这个概念很重要，因为今天的 AI 产品已经不是单个模型的演示，而是一套服务系统。真正好用的 AI，需要在正确率、速度、成本和安全之间做实时取舍。",
    "理解推理路由以后，你会更容易看懂为什么有些 AI 回复很快，有些会先检索资料，有些会调用工具，有些会升级到更强模型，也会理解为什么企业部署 AI 时不能只问“模型多大”。",
]


ANALOGY = [
    "把 AI 服务想象成一家大型医院。医院门口每天来很多人：有人只是轻微感冒，有人需要拍片，有人要看专科，有人情况紧急。医院不会让所有人直接冲进同一个专家诊室。",
    "更合理的流程是先分诊。分诊台会问：你哪里不舒服？症状严重吗？是不是急诊？需要检查吗？然后把人安排到普通门诊、专科医生、检验科、急诊，或者让护士先处理简单问题。",
    "推理路由就是 AI 系统里的“智能分诊台”。用户的问题进来后，路由器先看任务类型和难度，再决定交给小模型、大模型、RAG 检索、工具调用、多模态模型，或者在高风险时交给人工兜底。",
    "关键不是“永远用最强模型”，而是“把正确的问题交给正确的能力”。简单问题让小模型快速回答，复杂问题让大模型深度处理，需要事实依据的问题先去知识库查证，需要操作的问题调用工具。",
    "这样做的好处很直观：普通问题不用排队等专家，复杂问题也不会被简单问题挤占资源；用户感觉更快，企业成本更低，系统整体也更稳。",
]


MECHANISM = [
    ("接收请求", "用户输入问题、文件、图片或语音。系统先把它转成机器能处理的请求，并记录来源、长度、权限和实时负载。"),
    ("识别任务", "系统判断这是翻译、总结、代码、问答、图片理解、数据查询，还是需要执行动作。就像分诊台先问清楚“你到底来解决什么问题”。"),
    ("估算难度", "路由器会判断问题是否简单、是否需要长推理、是否需要最新资料、是否可能出错。简单问题可以走快车道，难题才升级到更强路线。"),
    ("检查约束", "系统会同时看延迟要求、成本预算、隐私等级、安全风险和用户权限。有些问题能快答，有些问题必须更谨慎。"),
    ("选择路线", "路由器把请求送到小模型、大模型、RAG 检索、工具调用、多模态模型或人工兜底。路线可以是一条，也可以是几条组合。"),
    ("执行与合并", "被选中的模型或工具开始工作。系统可能先检索资料，再让模型组织答案；也可能让小模型先尝试，大模型负责复核。"),
    ("返回结果", "答案返回给用户。对用户来说只是一次对话；对系统来说，背后可能已经完成了分诊、检索、模型选择和安全检查。"),
    ("监控反馈", "系统持续记录质量、速度、成本、失败率和安全事件。表现不好的路线会被调整，就像医院会根据拥堵情况重新安排窗口。"),
]


TERMS = [
    ("推理 Inference", "专业解释：训练完成的模型根据输入生成输出的过程。", "白话解释：AI 正式回答你问题的那一刻。"),
    ("路由 Routing", "专业解释：根据规则、模型判断或系统状态，把请求分配到不同处理路径。", "白话解释：给每个问题安排最合适的去处。"),
    ("路由器 Router", "专业解释：负责判断请求类型、难度、风险并选择处理资源的模块。", "白话解释：AI 服务里的分诊台或调度员。"),
    ("小模型 Small Model", "专业解释：参数规模较小、运行更快、成本更低的模型。", "白话解释：处理日常小事的快手助手。"),
    ("大模型 Large Model", "专业解释：能力更强但计算成本和响应时间通常更高的模型。", "白话解释：更像专家医生，适合复杂问题。"),
    ("RAG 检索增强生成", "专业解释：模型回答前先从外部知识库检索相关资料，再基于资料生成答案。", "白话解释：让 AI 开卷答题，先翻资料再回答。"),
    ("工具调用 Tool Calling", "专业解释：模型按需要调用外部函数、数据库、计算器、搜索或业务系统。", "白话解释：AI 不只说话，还能去查表、算数、下指令。"),
    ("多模态模型 Multimodal Model", "专业解释：能同时处理文字、图片、语音、视频等多种输入的模型。", "白话解释：不只会读文字，还能看图、听声音。"),
    ("延迟 Latency", "专业解释：从请求发出到用户看到结果所花的时间。", "白话解释：你等 AI 回答要等多久。"),
    ("成本 Cost", "专业解释：一次请求消耗的算力、模型调用费用、存储和网络资源。", "白话解释：AI 回答一次到底花多少钱。"),
    ("质量评估 Quality Evaluation", "专业解释：用规则、模型或人工判断答案是否正确、有用、安全。", "白话解释：检查 AI 有没有答对、有没有乱说。"),
    ("人工兜底 Human Fallback", "专业解释：当风险或不确定性过高时，把任务转交给人类处理。", "白话解释：AI 拿不准时，请真人接手。"),
]


CASE = [
    "一个真实应用案例是企业 AI 客服。用户可能会问三类问题：第一类是“订单到哪里了”，第二类是“帮我改收货地址”，第三类是“我收到的商品有安全隐患，怎么处理”。",
    "如果所有问题都交给最强大模型，系统会很贵也很慢。更合理的做法是：订单查询走工具调用，直接查物流系统；常见政策问题走小模型或知识库；涉及投诉、安全、法律或高金额赔付的问题升级到大模型，并可能交给人工复核。",
    "在这个过程中，推理路由像一个安静的后台调度员。它先识别用户意图，再判断风险和权限，然后决定是否查数据库、是否检索知识库、是否调用大模型、是否需要人工接管。",
    "用户看到的是“客服很快给了准确答案”。企业看到的是另一个结果：简单问题自动化处理，复杂问题得到更好关注，客服成本下降，风险问题不会被随便交给一个不合适的模型。",
    "AI 搜索、代码助手、办公助手、医疗预问诊、金融投研助手也有类似逻辑。越是复杂的 AI 产品，越不可能只靠一个模型硬扛所有请求。",
]


MISTAKES = [
    ("误区一：推理路由就是随机选择一个模型。", "不是。好的路由会依据任务类型、难度、成本、延迟、安全和历史效果做选择，而不是随便分配。"),
    ("误区二：永远用最大模型就最好。", "不一定。最大模型更贵、更慢，也未必适合每个任务。简单问题用小模型常常更快、更稳定。"),
    ("误区三：小模型一定回答得差。", "不一定。对格式固定、范围明确、重复性高的任务，小模型可能已经足够好，而且响应更快。"),
    ("误区四：推理路由等于负载均衡。", "不完全是。负载均衡主要看机器忙不忙；推理路由还要看问题该由谁处理、需要什么能力、风险有多高。"),
    ("误区五：RAG、工具调用和路由是同一回事。", "不是。RAG 和工具调用是可选路线；推理路由决定什么时候该走这些路线。"),
    ("误区六：路由越复杂越高级。", "不一定。路线太多会增加错误、延迟和维护成本。好系统要清楚、可解释、能监控。"),
    ("误区七：推理路由只关心省钱。", "省钱只是一个目标。真正的路由还要兼顾正确率、用户体验、隐私、安全和业务责任。"),
    ("误区八：路由策略一旦写好就不用改。", "不会。模型能力、用户问题、业务规则和成本都会变化，路由策略需要持续评估和更新。"),
]


SUMMARY = [
    "推理路由的本质，是给每个 AI 请求做智能分诊，把问题送到最合适的模型、工具或人工路径。",
    "它让 AI 产品在正确率、速度、成本和安全之间做实时取舍，而不是所有问题都用同一个大模型硬答。",
    "成熟的 AI 系统不只是“一个聪明模型”，更是一套能判断、调度、监控和纠错的服务网络。",
]


QUIZ = [
    "为什么医院分诊台的类比能帮助理解推理路由？请举一个“简单问题”和一个“需要专家处理的问题”。",
    "如果一个企业客服系统为了省钱，把太多问题都交给小模型，可能会出现什么风险？",
    "RAG、工具调用、大模型、小模型都可以是路线。你会怎样为“查询订单物流”和“分析合同风险”分别设计路线？",
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
      --ink: #111827;
      --muted: #475569;
      --quiet: #64748b;
      --line: #d7e0ea;
      --paper: #ffffff;
      --soft: #f8fafc;
      --blue: #123872;
      --teal: #0f766e;
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
      <h1>推理路由<br><span>Inference Routing</span></h1>
      <p class="subtitle">为什么 AI 服务需要一个“智能分诊台”？</p>
      <div class="core">核心一句话：推理路由的本质，是让 AI 先判断问题该走哪条路，再把它交给最合适的模型、工具或人工处理。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>它解决什么？</b><p>解决所有请求都挤向同一个大模型，导致慢、贵、风险高的问题。</p></div>
        <div class="cover-card"><b>它改变什么？</b><p>让 AI 产品从“一个模型回答所有事”变成“多种能力协同服务”。</p></div>
        <div class="cover-card"><b>今天怎么学？</b><p>用医院分诊台的直觉，看懂模型选择、工具调用和风险兜底。</p></div>
      </div>
      <nav aria-label="目录">
        ${toc}
      </nav>
    </div>
  </header>

  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">推理路由解释的是：一个成熟 AI 产品为什么不能只靠一个大模型回答所有问题。</p>
      ${why}
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：医院里的智能分诊台</h2>
      ${analogy}
      <figure>
        <img src="${fig_analogy}" alt="推理路由类比图：AI服务像智能分诊台，把不同请求送往小模型、大模型、工具或RAG检索">
        <figcaption>图解：推理路由像分诊台，不是每个问题都派最贵的模型，而是按任务选择最合适的路线。</figcaption>
      </figure>
      <div class="callout">最关键的直觉：推理路由不是降低 AI 能力，而是让不同能力各司其职。</div>
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：从问题进入系统到路线选择</h2>
      <p class="lead">推理路由通常不是一个单独按钮，而是一套实时判断流程：识别任务、估算难度、检查约束、选择路线、监控反馈。</p>
      <figure>
        <img src="${fig_workflow}" alt="推理路由工作流：输入请求、识别任务、估算难度与风险、选择路线、返回答案、监控反馈">
        <figcaption>图解：路由器在正确率、速度、成本和安全之间做取舍，把请求送到合适的模型或工具。</figcaption>
      </figure>
      <div class="steps">
        ${steps}
      </div>
      <div class="note">注意：好的路由不是“越省越好”，也不是“越强越好”。它要让简单问题快，复杂问题准，高风险问题稳。</div>
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
      <h2>5. 一个真实应用案例：企业 AI 客服</h2>
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
        "【AI每日深度科普】推理路由：为什么 AI 服务需要一个“智能分诊台”？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        """今天的主题是 推理路由（Inference Routing）。

它解释了一个非常关键的问题：
为什么成熟的 AI 产品不能所有请求都交给同一个大模型，而要先判断任务类型、难度、风险、速度和成本，再选择合适路线。

附件内容将用生活化方式解释：
推理路由如何像医院分诊台一样工作；
它怎样在小模型、大模型、RAG、工具调用和人工兜底之间做选择；
以及为什么它是企业级 AI 服务走向稳定、低成本和可控风险的关键能力。

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
