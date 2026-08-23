from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from string import Template

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-24"
CONCEPT_CN = "AI芯片"
CONCEPT_EN = "AI Chips"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_ANALOGY = "chatgpt_ai_chips_analogy.png"
FIG_WORKFLOW = "chatgpt_ai_chips_workflow.png"


WHY = [
    "过去我们讨论 AI 时，常常只盯着模型：参数有多少、回答聪不聪明、能不能写代码。但真正让大模型跑起来的，还有一个更底层的问题：这么多计算，到底由谁来做？",
    "AI芯片要解决的，就是大模型的算力问题。一个大模型读一句话、生成一个词，背后都要做海量重复计算，尤其是矩阵乘法。普通 CPU 很灵活，但它像一个全能办公室主任；面对成千上万件相似小任务时，专门的并行计算芯片更高效。",
    "这就是为什么 AI 产业离不开芯片：它决定训练一个模型要花多久，用户等待回答要多久，企业服务一次请求要多少钱，手机能不能在本地离线运行 AI 功能，甚至决定数据中心要消耗多少电。",
    "理解 AI芯片之后，你会明白：AI 不是飘在云上的魔法。它最终会落到非常现实的物理世界里：硅片、显存、带宽、散热、电费和供应链。",
]

ANALOGY = [
    "想象一家大型餐厅。餐厅里有三类角色：店长、很多普通厨师、还有专门做某一道菜的老师傅。",
    "CPU 像店长。它什么都能管：接电话、排班、处理投诉、安排采购。它灵活，但如果让它同时切一万根胡萝卜，就会很慢。",
    "GPU 像一排厨师一起切菜。每个人做的动作差不多，但可以同时做。AI 里大量计算正是这种“相似动作重复很多次”的任务，所以 GPU 特别适合。",
    "NPU、TPU 或其他 AI 加速器，则像专门为 AI 设计的流水线。它们不一定像 CPU 那样什么都能做，但在矩阵乘法、张量计算、低精度计算和能效上更专精。",
    "最重要的直觉是：AI芯片不是越贵越神奇，而是越能把合适的计算交给合适的硬件。店长负责调度，大厨房负责并行，专用厨师负责高频菜品，这家餐厅才跑得快、成本低。",
]

MECHANISM = [
    ("用户输入变成数字", "AI 不能直接理解汉字。系统会先把一句话切成 token，再把 token 转成向量，也就是一串数字。"),
    ("模型做大量矩阵乘法", "大模型的很多核心步骤，本质上是在做矩阵和向量之间的计算。你可以把它想成把很多数字表格按规则反复相乘、相加。"),
    ("芯片把计算并行排队", "AI芯片的优势，是把大量相似小计算排成整齐队列，让很多计算单元同时开工，而不是一个接一个慢慢算。"),
    ("显存保存中间结果", "模型权重、用户上下文、KV Cache 和中间结果都要放在显存或片上缓存里。空间不够，速度就会被拖慢。"),
    ("带宽决定搬运速度", "芯片不仅要会算，还要能快速把数据搬进搬出。很多时候慢的不是算，而是数字在内存和计算单元之间来回搬运。"),
    ("能耗和散热限制规模", "算得越多，耗电和发热越大。数据中心关心电费和散热，手机关心续航和温度，所以能效是 AI芯片的核心指标。"),
    ("软件决定硬件能不能吃饱", "同一块芯片，如果编译器、推理框架、批处理、量化和调度做得不好，性能也发挥不出来。AI芯片从来不是单独工作的。"),
]

TERMS = [
    ("CPU", "专业解释：通用中央处理器，擅长复杂控制逻辑和多样化任务。", "白话解释：全能店长，什么都能管，但不适合海量重复劳动。"),
    ("GPU", "专业解释：图形处理器，拥有大量并行计算单元，适合矩阵和张量运算。", "白话解释：很多厨师同时做类似动作，适合 AI 的大批量计算。"),
    ("TPU", "专业解释：面向机器学习工作负载设计的专用张量处理器。", "白话解释：专门为 AI 菜谱改造过的流水线。"),
    ("NPU", "专业解释：面向神经网络推理的专用处理单元，常见于手机、电脑和边缘设备。", "白话解释：设备里专门跑 AI 小任务的省电助手。"),
    ("AI加速器", "专业解释：用于加速 AI 训练或推理的硬件统称，包括 GPU、TPU、NPU 和其他 ASIC。", "白话解释：所有“让 AI 算得更快”的专用硬件大类。"),
    ("矩阵乘法", "专业解释：线性代数中的核心运算，是神经网络大量计算的基础。", "白话解释：把成片数字表格按规则批量相乘、相加。"),
    ("张量 Tensor", "专业解释：多维数组，是深度学习框架表达数据和参数的基本结构。", "白话解释：不只是表格，还可能是很多层叠在一起的数字盒子。"),
    ("显存 VRAM/HBM", "专业解释：靠近加速器的高速内存，用来存放模型权重和中间数据。", "白话解释：大厨房旁边的备菜台，越大越快越不容易卡住。"),
    ("内存带宽", "专业解释：单位时间内芯片和内存之间能传输多少数据。", "白话解释：备菜台到灶台之间的传送带有多宽。"),
    ("算力 FLOPS/TOPS", "专业解释：芯片每秒可完成的浮点或整数运算次数。", "白话解释：这家厨房理论上一秒能切、炒、装盘多少次。"),
    ("能效", "专业解释：单位能耗下完成的计算量，常用于衡量 AI硬件效率。", "白话解释：花同样电费，谁能多做几份菜。"),
    ("推理 Inference", "专业解释：已经训练好的模型根据输入生成输出的过程。", "白话解释：AI 正式给用户回答问题的时刻。"),
]

CASE = [
    "一个真实应用案例，是手机里的本地 AI 功能。比如语音转文字、照片增强、实时翻译、键盘预测和部分离线助手功能。它们不能每次都把数据传到云端，因为那会带来延迟、流量、隐私和断网问题。",
    "这时设备里的 NPU 就很重要。它可以在本地处理适合自己的神经网络任务：图片里的物体识别、音频特征提取、短文本理解、低功耗推理。对用户来说，只是相机更智能、输入法更懂你；对设备来说，是把 AI 计算交给更省电的专用硬件。",
    "另一个案例是云端 AI 助手。用户提问看似只有一句话，背后却可能需要 GPU 或其他 AI 加速器加载大模型、处理上下文、执行矩阵计算、维护 KV Cache，再把 token 一个个生成出来。前面讲过的批处理、推理路由、量化、模型压缩，最终都要和芯片能力配合。",
    "所以 AI芯片不是单纯的硬件新闻。它直接影响 AI 产品能不能更便宜、更快、更稳定地服务更多人。",
]

MISTAKES = [
    ("误区一：AI芯片越贵，模型就一定越聪明。", "不一定。芯片提供计算能力，但模型能力还取决于数据、结构、训练方法、对齐和产品设计。好厨房不等于自动有好菜谱。"),
    ("误区二：CPU 已经过时了。", "没有。CPU 仍然负责操作系统、调度、数据预处理、网络通信和很多控制逻辑。AI 系统通常是 CPU 与加速器协同。"),
    ("误区三：GPU、TPU、NPU 都是一回事。", "它们都能加速 AI，但定位不同。GPU 更通用、更灵活；TPU/NPU 往往更专用，可能在特定任务上更省电或更高效。"),
    ("误区四：只要算力够，AI 就没有瓶颈。", "不对。显存容量、内存带宽、网络通信、散热、电力和软件调度都会成为瓶颈。"),
    ("误区五：AI芯片只和训练有关。", "不是。训练需要大量算力，推理同样重要。真正面向大众的 AI 产品，每天要处理海量推理请求。"),
    ("误区六：本地 AI 一定比云端 AI 弱。", "不一定。小模型、本地 NPU 和隐私场景结合后，很多任务在本地更快、更稳、更省钱。复杂任务仍可交给云端大模型。"),
    ("误区七：算力指标越大，实际体验越好。", "不一定。理论算力像厨房最大产能，真实体验还要看模型大小、批处理、内存带宽、软件优化和网络延迟。"),
    ("误区八：AI芯片只是工程师才需要懂的细节。", "值得普通人理解。它解释了为什么 AI 产品有价格差异、为什么会排队、为什么手机能离线 AI、为什么科技公司争夺算力。"),
]

SUMMARY = [
    "AI芯片的本质，是把大模型需要的大量重复计算变成更快、更省电的专业流水线。",
    "CPU、GPU、TPU、NPU 不是谁取代谁，而是在灵活性、并行能力和能效之间分工合作。",
    "AI 的真实瓶颈不只在模型，还在算力、显存、带宽、能耗和软件调度共同组成的系统。",
]

QUIZ = [
    "为什么说 CPU 像店长、GPU 像并行厨房、NPU/TPU 像 AI 专用厨师？这个类比各自有什么局限？",
    "如果一个 AI 产品回答很慢，你会从算力、显存、带宽、网络和调度里优先检查哪些因素？为什么？",
    "为什么手机里的本地 AI 功能更看重能效，而云端大模型服务更看重吞吐、显存和集群调度？",
]

SOURCES = [
    ("Google Cloud TPU documentation", "https://cloud.google.com/tpu/docs/intro-to-tpu"),
    ("NVIDIA Tensor Cores overview", "https://www.nvidia.com/en-us/data-center/tensor-cores/"),
    ("MLCommons MLPerf Inference", "https://mlcommons.org/benchmarks/inference-datacenter/"),
    ("Apple Machine Learning research overview", "https://machinelearning.apple.com/"),
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


def source_items() -> str:
    return "\n".join(
        f'<li><a href="{escape(url)}">{escape(title)}</a></li>' for title, url in SOURCES
    )


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
      background: linear-gradient(180deg, #ffffff 0%, #f7fbff 58%, #eefbf7 100%);
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
    .sources a {
      color: var(--blue);
      text-decoration: none;
      border-bottom: 1px solid #bfdbfe;
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
      <h1>AI芯片<br><span>AI Chips</span></h1>
      <p class="subtitle">为什么算力成了 AI 时代的新电力？</p>
      <div class="core">核心一句话：AI芯片的本质，是把大模型需要的大量重复计算变成更快、更省电的专业流水线。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>它解决什么？</b><p>解决大模型计算量巨大、普通硬件效率不够、推理成本过高的问题。</p></div>
        <div class="cover-card"><b>它改变什么？</b><p>让 AI 从实验室模型，变成能在云端、手机和边缘设备上运行的产品。</p></div>
        <div class="cover-card"><b>今天怎么学？</b><p>用餐厅分工的直觉，看懂 CPU、GPU、NPU/TPU 的不同角色。</p></div>
      </div>
      <nav aria-label="目录">
        ${toc}
      </nav>
    </div>
  </header>

  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">AI芯片解释的是：为什么大模型不只是“算法问题”，也是一场真实世界里的算力、能耗和供应链问题。</p>
      ${why}
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：大型餐厅里的分工</h2>
      ${analogy}
      <figure>
        <img src="${fig_analogy}" alt="AI芯片类比图：CPU像全能总管，GPU像并行大厨房，NPU/TPU像AI专用厨师">
        <figcaption>图解：AI 系统不是只靠一种芯片，而是把灵活调度、并行计算和专用加速组合起来。</figcaption>
      </figure>
      <div class="callout">最关键的直觉：芯片不是“越强越万能”，而是“越适合某类计算，就越快、越省电”。</div>
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：从一句问题到芯片计算</h2>
      <p class="lead">大模型看似在“理解语言”，但在芯片眼里，它主要是在搬运数字、做矩阵运算、保存中间结果。</p>
      <figure>
        <img src="${fig_workflow}" alt="AI芯片工作流程图：用户问题、Token化、矩阵乘法、芯片并行计算、内存读写、输出答案">
        <figcaption>图解：一次 AI 回答背后，是 token、矩阵乘法、并行计算、内存读写和结果生成的流水线。</figcaption>
      </figure>
      <div class="steps">
        ${steps}
      </div>
      <div class="note">注意：AI芯片的“快”并不只来自算得快，还来自数据搬得快、存得下、散得出热、软件能调度得好。</div>
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
      <h2>5. 一个真实应用案例：手机本地 AI 与云端 AI 助手</h2>
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

    <section class="sources" id="sources">
      <h2>参考资料</h2>
      <p class="lead">以下资料用于校准 TPU、Tensor Core、推理评测和设备端机器学习等基础表述。</p>
      <ul>
        ${sources}
      </ul>
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
        sources=source_items(),
    )


def write_text_files() -> None:
    (ROOT / "email_subject.txt").write_text(
        "【AI每日深度科普】AI芯片：为什么算力成了 AI 时代的新电力？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        """今天的主题是 AI芯片（AI Chips）。

它解释了一个非常底层但关键的问题：
为什么大模型不只是算法突破，也离不开 GPU、TPU、NPU、显存、带宽、能耗和软件调度。

附件内容将用生活化方式解释：
CPU、GPU、NPU/TPU 分别像什么；
为什么矩阵乘法是 AI 计算的核心；
以及为什么算力、显存、带宽和能效正在决定 AI 产品的成本与体验。

适合：非技术读者、AI初学者、产品经理、投资研究者和关注 AI 产业基础设施的人阅读。""",
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


if __name__ == "__main__":
    main()
