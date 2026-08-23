from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from string import Template

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-19"
CONCEPT_CN = "推测解码"
CONCEPT_EN = "Speculative Decoding"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_ANALOGY = "chatgpt_speculative_decoding_analogy.png"
FIG_WORKFLOW = "chatgpt_speculative_decoding_workflow.png"


WHY = [
    "很多人以为大模型回答慢，是因为它“思考得久”。这只说对了一半。大模型生成文字时，通常像一个人打字：先写第一个词，再根据前面的内容写第二个词，然后继续写第三个词。每多生成一个词，都要让庞大的模型再跑一轮。",
    "这就是推理阶段的一个核心瓶颈：模型不是一次把整段答案吐出来，而是一小步一小步地往前走。即使有 KV Cache、模型量化、GPU 加速，长答案仍然会被“一个词一等待”的节奏拖慢。",
    "推测解码要解决的，就是这个等待问题。它让一个更小、更快的模型先猜出一串候选词，再让真正的大模型一次性检查这串词。猜对的部分就整批收下，猜错的地方再回退修正。这样，大模型不用每个词都单独等一轮。",
    "它重要的地方不只是让聊天机器人回复更快。AI 搜索、代码助手、客服系统、翻译、会议纪要、企业知识库问答，只要需要大模型快速生成长文本，就都关心这个问题。速度提升意味着用户少等、服务器少跑、GPU 成本下降。"
]

ANALOGY = [
    "想象一位语文老师每天要批改很多作文。最稳妥的做法是：学生每写一个字，老师就检查一次。这样当然最准确，但效率极低。老师的大部分时间都花在等待和重复确认上。",
    "后来老师安排了一个助教。助教很快，但水平略低。每次学生提出一个问题，助教先根据上下文写出接下来几个词，像一份“草稿”。老师不再一个词一个词地从零写，而是快速检查这份草稿：前面几处如果都对，就一次性盖章通过；从第一个不对的地方开始，老师亲自改写。",
    "这就是推测解码的直觉。小模型像助教，负责快速写草稿；大模型像老师，负责最终把关。真正的答案仍然由大模型决定，只是它不必每一步都从头慢慢生成。",
    "关键点在于：助教不是乱猜。它通常是一个和大模型风格接近、但更小更快的模型。遇到“今天天气很好”“下面分三点说明”这类容易预测的句子时，助教可能一连猜对好几个词；遇到复杂推理、精确数字、创造性表达时，它就更容易猜错，大模型会及时接管。"
]

MECHANISM = [
    ("先有一个目标模型", "目标模型就是我们真正信任的大模型。它决定最终答案的质量和风格，就像作文老师拥有最后批改权。"),
    ("准备一个草稿模型", "草稿模型更小、更快，能力弱一些，但足够擅长猜常见的下一步。它的任务不是替代大模型，而是先提出候选词。"),
    ("草稿模型连续猜多个词", "普通解码一次只让大模型生成一个词；推测解码先让草稿模型连续写出一小串候选词，例如 4 个、8 个或更多。"),
    ("大模型并行检查这串词", "大模型拿着已有上下文和候选词序列，一次前向计算就能检查多个位置：第一个词是否合理，第二个词在第一个词成立后是否合理，依次往后看。"),
    ("接受最长的正确前缀", "如果前几个候选词都符合大模型的判断，就把这段前缀一次性加入答案。通过的词越多，节省的大模型轮数越多。"),
    ("从第一个分歧点继续", "一旦某个候选词不被大模型接受，就在这个位置回退。经典算法会用大模型的概率分布补上正确下一词，再进入下一轮草稿与验证。"),
    ("用接受率决定是否划算", "如果草稿模型经常猜对，推测解码会明显加速；如果经常猜错，小模型的草稿成本反而可能抵消收益。"),
    ("保持质量靠大模型把关", "经典的推测解码可以在概率意义上保持与目标模型相同的输出分布。工程实现如果做近似，则必须用评测确认质量没有被速度牺牲掉。")
]

TERMS = [
    ("Token 词元", "专业解释：模型生成和读取文本的基本单位，可以是字、词、词的一部分或符号。", "白话解释：AI 打字时不是按整句话输出，而是一小块一小块往外吐。"),
    ("Autoregressive Decoding 自回归解码", "专业解释：每一步都基于已经生成的内容预测下一个 token。", "白话解释：像接龙，前面写了什么，会决定后面能接什么。"),
    ("Target Model 目标模型", "专业解释：最终负责输出质量和概率分布的大模型。", "白话解释：真正有最后决定权的老师。"),
    ("Draft Model 草稿模型", "专业解释：更小更快、用于提前生成候选 token 的辅助模型。", "白话解释：先快速写草稿的助教。"),
    ("Candidate Tokens 候选词序列", "专业解释：草稿模型连续预测出来、等待目标模型验证的一串 token。", "白话解释：助教先写好的一小段草稿。"),
    ("Verification 验证", "专业解释：目标模型对候选 token 的多个位置进行检查，决定接受或拒绝。", "白话解释：老师快速批改草稿，看前面哪些词可以直接收下。"),
    ("Accepted Prefix 接受前缀", "专业解释：候选序列中从开头起连续被目标模型接受的部分。", "白话解释：草稿前面连续正确的一段，可以直接并入答案。"),
    ("Rejection Sampling 拒绝采样", "专业解释：通过接受或拒绝候选样本，使最终采样符合目标分布的一类方法。", "白话解释：猜得合理就收下，不合理就按大模型的规则重来。"),
    ("Acceptance Rate 接受率", "专业解释：候选 token 被目标模型接受的比例，是推测解码是否加速的关键指标。", "白话解释：助教草稿有多少能被老师直接盖章。"),
    ("Latency 延迟", "专业解释：用户发出请求到看到答案之间的等待时间。", "白话解释：你问完以后，要等多久才开始看到有用回答。"),
    ("Throughput 吞吐量", "专业解释：系统单位时间内能处理的请求或生成的 token 数。", "白话解释：同一批机器一小时能服务多少人。"),
    ("KV Cache 键值缓存", "专业解释：保存注意力计算中的历史键值，避免每一步重复计算全部上下文。", "白话解释：把前面已经算过的阅读笔记留下来，后面不用重读整篇文章。")
]

CASE = [
    "一个真实应用场景是 AI 编程助手。用户让模型生成一段 Python 函数，前半部分往往很有规律：函数名、参数、注释、常见循环、错误处理模板。草稿模型可以很快预测这些常见片段。",
    "随后，大模型一次性检查草稿模型写出的多个 token。如果它发现“def”“return”“for”等常见结构都合理，就直接接受一段；如果遇到关键逻辑、边界条件或变量名不一致的地方，就从分歧点接管生成。",
    "用户感受到的是：代码一行一行出现得更快，等待时间更短。平台感受到的是：同样一批 GPU 可以服务更多请求。对企业来说，这会影响成本结构；对产品来说，这会影响用户是否愿意持续使用。",
    "但推测解码不是所有时候都一样有效。写样板代码、常见客服回复、格式化摘要时，草稿模型更容易猜对，收益更高；做复杂数学证明、长链推理、非常开放的创意写作时，候选词更难预测，接受率会下降。"
]

MISTAKES = [
    ("误区一：推测解码就是让小模型替代大模型。", "不是。小模型只负责先写草稿，最终是否接受仍由大模型把关。"),
    ("误区二：它会让模型变聪明。", "不会。它主要解决生成速度和成本问题，不会凭空增加模型知识或推理能力。"),
    ("误区三：它一定会降低答案质量。", "经典推测解码设计得当时，可以保持目标模型的输出分布；但具体工程实现仍要实测。"),
    ("误区四：它一定能让所有任务都快很多。", "不一定。加速取决于草稿模型成本、候选长度、接受率、硬件调度和实现细节。"),
    ("误区五：草稿越长越好。", "草稿太短，省不了几轮；草稿太长，猜错多、验证和回退成本增加。需要找到合适长度。"),
    ("误区六：推测解码等于多用户批处理。", "不是。批处理是把多个用户请求一起跑；推测解码是在一个用户的生成过程中提前猜一串 token。"),
    ("误区七：只要有小模型就能做。", "草稿模型要和目标模型的输出习惯足够接近，否则接受率低，速度收益会被抵消。"),
    ("误区八：速度提升来自“大模型少思考”。", "更准确地说，是大模型少跑了若干轮逐词等待；它仍然负责验证和决定关键输出。")
]

SUMMARY = [
    "推测解码的本质，是让小而快的模型先写一串草稿，再让大模型一次性检查并接受尽可能长的正确前缀。",
    "它解决的是大模型生成时“一个词一等待”的推理瓶颈，常用于降低延迟、提升吞吐量和节省 GPU 成本。",
    "它不是让模型变聪明，也不是无条件加速；真正收益取决于草稿模型是否常常猜对，以及系统实现是否足够高效。"
]

QUIZ = [
    "为什么普通大模型生成长答案时会慢？请用“一个词一等待”的角度解释。",
    "如果草稿模型连续猜 8 个词，但大模型只接受前 2 个词，这一轮为什么仍然可能收益有限？",
    "请比较昨天的“模型量化”和今天的“推测解码”：它们都能让 AI 更快，但分别是在解决什么不同问题？"
]


def image_data_uri(name: str) -> str:
    data = (ROOT / name).read_bytes()
    return f"data:image/png;base64,{base64.b64encode(data).decode('ascii')}"


def paras(items: list[str]) -> str:
    return "\n".join(f"<p>{escape(item)}</p>" for item in items)


def mechanism_cards() -> str:
    cards: list[str] = []
    for idx, (title, body) in enumerate(MECHANISM, 1):
        cards.append(
            f"""
            <article class="step-card">
              <div class="step-num">{idx:02d}</div>
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
      --green: #23845c;
      --amber: #b7791f;
      --red: #c2410c;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: #eef3f8;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
    }
    .cover {
      min-height: 100vh;
      background:
        radial-gradient(circle at 86% 16%, rgba(15, 139, 141, .13), transparent 24%),
        linear-gradient(90deg, rgba(18, 56, 114, .10), transparent 44%),
        linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
      border-bottom: 1px solid var(--line);
      padding: 56px 26px 42px;
    }
    .wrap { max-width: 1080px; margin: 0 auto; }
    .eyebrow {
      color: var(--teal);
      font-size: 15px;
      font-weight: 800;
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
      max-width: 940px;
      margin: 0;
      color: var(--muted);
      font-size: clamp(22px, 3vw, 32px);
      line-height: 1.35;
      font-weight: 650;
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
      font-weight: 800;
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
      background: rgba(255,255,255,.90);
      padding: 18px;
    }
    .cover-card b { display: block; color: var(--blue); font-size: 20px; margin-bottom: 8px; }
    .cover-card p { margin: 0; color: var(--muted); font-size: 16px; line-height: 1.65; }
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
      font-weight: 750;
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
    h3 { margin: 0 0 6px; color: var(--blue); font-size: 21px; line-height: 1.3; }
    p { margin: 12px 0; font-size: 18px; }
    .lead { color: var(--muted); font-size: 20px; font-weight: 680; }
    figure { margin: 20px 0 8px; break-inside: avoid; }
    img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
    }
    figcaption { margin-top: 8px; color: var(--quiet); font-size: 14px; }
    .steps {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 20px;
    }
    .step-card {
      display: grid;
      grid-template-columns: 54px 1fr;
      gap: 14px;
      min-height: 140px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdff;
      break-inside: avoid;
    }
    .step-num {
      display: grid;
      place-items: center;
      width: 46px;
      height: 46px;
      border-radius: 8px;
      background: var(--blue);
      color: white;
      font-weight: 900;
    }
    .step-card p { margin: 0; color: var(--muted); font-size: 16px; }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 15.5px; }
    th, td { border: 1px solid var(--line); padding: 12px; vertical-align: top; }
    th { width: 22%; background: #f8fafc; color: var(--blue); text-align: left; }
    ul, ol { padding-left: 24px; }
    li { margin: 10px 0; font-size: 18px; }
    .mistakes { list-style: none; padding: 0; margin: 8px 0 0; }
    .mistakes li {
      border: 1px solid var(--line);
      border-left: 6px solid var(--amber);
      border-radius: 8px;
      padding: 13px 16px;
      background: #fffaf0;
      break-inside: avoid;
    }
    .mistakes strong { display: block; color: #92400e; margin-bottom: 4px; }
    .mistakes span { color: var(--muted); }
    .note {
      margin-top: 18px;
      padding: 16px 18px;
      border: 1px solid #bfdbfe;
      border-radius: 8px;
      background: #eff6ff;
      color: var(--blue);
      font-size: 18px;
      font-weight: 750;
    }
    .summary-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
    }
    .summary-card {
      min-height: 178px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fafc;
      font-size: 17px;
      font-weight: 700;
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
      .step-card { min-height: 118px; }
      p, li { font-size: 14.5px; line-height: 1.65; }
      h2 { font-size: 24px; }
      h3 { font-size: 17px; }
      table { font-size: 12px; }
      th, td { padding: 8px; }
      .summary-card { min-height: 132px; font-size: 13px; }
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
      <h1>推测解码<br><span>Speculative Decoding</span></h1>
      <p class="subtitle">为什么 AI 可以“先猜一串，再一次性检查”，从而更快生成答案？</p>
      <div class="core">核心一句话：推测解码的本质，是让小模型先写草稿，再让大模型批量验收，减少大模型一个词一个词等待的轮数。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>它解决什么？</b><p>解决大模型生成长答案时“逐词等待”的推理瓶颈。</p></div>
        <div class="cover-card"><b>它改变什么？</b><p>让聊天、代码、搜索和客服系统更低延迟、更高吞吐、更省 GPU。</p></div>
        <div class="cover-card"><b>今天怎么学？</b><p>用“学生先写，老师检查”的类比，看懂草稿、验证、接受和回退。</p></div>
      </div>
      <nav aria-label="目录">
        $toc
      </nav>
    </div>
  </header>

  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">推测解码解释的是：为什么不改变大模型本身，也能让它更快回答。</p>
      $why
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：学生先写，老师检查</h2>
      $analogy
      <figure>
        <img src="$fig_analogy" alt="推测解码类比：小模型先写草稿，大模型快速检查，通过则一次收下多个词，不通过则回退重写">
        <figcaption>图解：小模型像快速助教，大模型像最终老师。速度提升来自“大模型少等几轮”，不是来自放弃检查。</figcaption>
      </figure>
      <div class="note">一句话判断：推测解码不是“让小模型回答”，而是“让小模型先猜，大模型批改”。</div>
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：一批词一起验</h2>
      <p class="lead">真正的技巧在于：草稿模型提前生成多个候选词，目标模型一次计算验证多个位置。</p>
      <div class="steps">
        $mechanism
      </div>
      <figure>
        <img src="$fig_workflow" alt="推测解码工作流：草稿模型生成候选词序列，目标模型并行验证，接受前缀，从分歧点继续">
        <figcaption>图解：普通解码像“一个词一等”；推测解码像“先写一批，再一起验”。</figcaption>
      </figure>
      <div class="callout">最关键的直觉：如果草稿模型经常猜对，大模型一次验证就能换来多个 token 的进展。</div>
    </section>

    <section id="terms">
      <h2>4. 关键术语解释</h2>
      <table>
        <thead>
          <tr><th>术语</th><th>一句专业解释</th><th>一句白话解释</th></tr>
        </thead>
        <tbody>
          $terms
        </tbody>
      </table>
    </section>

    <section id="case">
      <h2>5. 一个真实应用案例：AI 编程助手</h2>
      $case
    </section>

    <section id="mistakes">
      <h2>6. 常见误区</h2>
      <ul class="mistakes">
        $mistakes
      </ul>
    </section>

    <section id="summary">
      <h2>7. 3句话总结</h2>
      <div class="summary-grid">
        <div class="summary-card">1. $summary_1</div>
        <div class="summary-card">2. $summary_2</div>
        <div class="summary-card">3. $summary_3</div>
      </div>
    </section>

    <section id="quiz">
      <h2>8. 复习问题</h2>
      <ol>
        $quiz
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
        mechanism=mechanism_cards(),
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
        "【AI每日深度科普】推测解码：为什么 AI 可以更快生成答案？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        "\n".join(
            [
                "今天的主题是 推测解码（Speculative Decoding）。",
                "",
                "它解释的是：为什么大模型可以通过“小模型先写草稿、大模型快速检查”的方式，减少一个词一个词等待的推理时间。",
                "",
                "附件用“学生先写，老师检查”的生活化类比，讲清楚草稿模型、目标模型、候选词、并行验证、接受前缀、回退重写，以及它和昨天“模型量化”的区别。",
                "",
                "适合：非技术读者、AI初学者、产品经理、投资研究者和正在关注 AI 推理成本的人阅读。",
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
        y = max(0, min(int(scroll_height * 0.42), max(0, int(scroll_height) - 1600)))
        page.evaluate("(scrollY) => window.scrollTo(0, scrollY)", y)
        page.wait_for_timeout(250)
        page.screenshot(path=str(ROOT / "html_midpage_preview.png"), full_page=False)
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()


if __name__ == "__main__":
    render_pdf()
