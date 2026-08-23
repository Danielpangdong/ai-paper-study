from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from string import Template

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-18"
CONCEPT_CN = "模型量化"
CONCEPT_EN = "Quantization"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_COMPRESS = "chatgpt_quantization_compress.png"
FIG_WORKFLOW = "chatgpt_quantization_workflow.png"


WHY = [
    "大模型很聪明，但也很“重”：它需要大量显存、计算和电力。模型量化解决的核心问题，是让模型在尽量少损失能力的前提下，用更小的数字、更少的空间和更快的计算完成推理。",
    "如果说训练大模型像建造一座很复杂的工厂，那么推理就是让这座工厂每天不断接单生产。真正决定 AI 能不能大规模进入手机、电脑、客服系统和企业流程的，不只是模型有多强，还包括它是否跑得起、够不够快、成本是否可承受。",
    "量化之所以重要，是因为它把“高性能 AI”从昂贵机房往更广泛的设备和场景里推。手机端 AI、离线助手、低成本客服、边缘摄像头、企业私有化部署，都离不开更小、更快、更便宜的模型。"
]

ANALOGY = [
    "想象你要出门旅行。原来你把所有东西都塞进一个巨大的行李箱：厚外套、正装、五双鞋、完整洗漱包。这样当然最稳妥，但行李太重，搬运慢，还可能超重。",
    "后来你发现，很多东西并不需要“满配”。牙膏不用带一整管，洗发水可以装进小瓶，鞋子只带最常用的两双。你牺牲了一点点选择余地，却换来了轻便、快速和低成本。",
    "模型量化也是类似思路。大模型内部有海量参数，这些参数原本常用很精细的数字保存，比如 32 位浮点数。量化会把它们换成更短、更省空间的数字，比如 8 位或 4 位整数。数字变粗糙了一点，但如果设计得好，模型的大部分能力仍然保留下来。",
    "关键不是“随便变小”，而是“聪明地变小”。就像收拾行李时要知道什么能缩、什么不能丢，量化也要判断哪些参数可以低精度表示，哪些地方需要更谨慎，最后还要检查模型回答是否明显变差。"
]

MECHANISM = [
    ("原始模型：先有一个大而精细的版本", "模型参数像一张巨大的调音台，每个旋钮都有很细的刻度。32 位或 16 位数字能表示很细微的变化，但也占空间、耗显存。"),
    ("观察范围：看看数字通常落在哪里", "量化前要先了解参数或激活值的大致范围。就像给考试分数画刻度尺：如果大多数分数在 60 到 100 之间，就不需要为 10000 分预留刻度。"),
    ("重新刻度：用更短的数字表示近似值", "量化会把连续的精细数字映射到有限的格子里。原来可以有很多小数位，现在可能只保留 256 个等级，甚至 16 个等级。"),
    ("替换计算：用低精度数字做推理", "模型回答问题时，很多乘法和加法可以用更小的数据格式完成。显存占用变少，数据搬运更快，硬件也更容易加速。"),
    ("校准与补偿：减少“变小”带来的偏差", "有些量化方法会用少量样本校准刻度，或保留少数敏感部分的高精度，避免模型在关键任务上突然变笨。"),
    ("质量检查：确认省成本没有省掉能力", "最后要用真实任务测试：回答是否稳定、推理是否变快、幻觉是否增加、数学和代码能力是否下降。合格后才能部署。")
]

TERMS = [
    ("Precision 精度", "专业解释：数值表示的细致程度，常见格式包括 FP32、FP16、INT8、INT4。", "白话解释：刻度尺有多细；刻度越细越精确，但也越占空间。"),
    ("FP32 / FP16", "专业解释：32 位或 16 位浮点数格式，常用于训练和高精度计算。", "白话解释：比较精细的数字写法，像带很多小数位的测量结果。"),
    ("INT8 / INT4", "专业解释：8 位或 4 位整数格式，常用于低精度推理和模型压缩。", "白话解释：更短的数字标签，省地方，但刻度更粗。"),
    ("Weights 权重", "专业解释：模型学习得到的参数，决定输入信息如何影响输出。", "白话解释：模型脑子里无数个小旋钮，控制它怎么判断和生成。"),
    ("Activation 激活值", "专业解释：模型在处理输入时，中间层产生的临时数值。", "白话解释：模型思考过程中临时写在草稿纸上的数字。"),
    ("Calibration 校准", "专业解释：用代表性样本确定量化比例和零点，降低低精度表示带来的误差。", "白话解释：先试几道典型题，调整刻度尺怎么画更合适。"),
    ("Scale / Zero Point", "专业解释：把高精度数值映射到低精度整数时使用的缩放比例和偏移量。", "白话解释：告诉模型“一个小格代表多少”，以及“零点放在哪里”。"),
    ("PTQ 后训练量化", "专业解释：模型训练完成后，不重新训练或只用少量校准数据进行量化。", "白话解释：成品模型不大改，直接做瘦身和适配。"),
    ("QAT 量化感知训练", "专业解释：训练阶段就模拟量化误差，让模型提前适应低精度环境。", "白话解释：训练时就让学生习惯用粗一点的尺子做题。"),
    ("Accuracy Drop 精度下降", "专业解释：量化后模型在评测或真实任务上的表现损失。", "白话解释：行李变轻了，但不能把护照和药也丢了。")
]

CASE = [
    "一个真实应用是手机端 AI 助手。假设一个语言模型原本需要很大的显存，只能在云端服务器上运行。用户每问一句话，都要把请求发到远端，再等服务器回答。这会带来成本、延迟和隐私问题。",
    "量化后，模型体积可能显著缩小，推理时需要搬运的数据也变少。这样一部分能力就有机会放到本地设备上运行：例如离线总结、语音指令理解、照片内容问答、个人笔记搜索等。用户感觉到的是“更快、更省电、弱网也能用”，背后则是数值格式和硬件效率的改变。",
    "企业部署也是同理。一个客服系统如果每天要处理几十万次咨询，推理成本会迅速放大。量化模型可以在同样硬件上承载更多请求，或者用更少机器完成同样任务。对公司来说，这不是一个小优化，而是决定 AI 产品能不能长期运营的经济问题。",
    "但量化不是越狠越好。比如医疗建议、法律审查、复杂数学、代码生成等场景，对细节更敏感。工程团队通常会比较不同量化方案，在速度、显存、成本和准确率之间做取舍。"
]

MISTAKES = [
    ("误区一：量化就是把模型简单压缩成 zip。", "不是。压缩包只是减少存储体积；量化会改变模型推理时使用的数字格式，影响计算过程。"),
    ("误区二：位数越低越先进。", "不一定。4 位可能更省，但也更容易损失能力。关键要看任务、硬件、校准方法和质量测试结果。"),
    ("误区三：量化后模型一定变笨很多。", "不一定。很多模型在合理量化后损失很小，尤其是通用问答和简单任务；但高难推理任务可能更敏感。"),
    ("误区四：量化能让模型学到新知识。", "不能。量化主要是让已有模型更轻、更快，不是训练新能力。想增加知识或风格，通常需要微调、RAG 或重新训练。"),
    ("误区五：量化只影响模型文件大小。", "它还影响显存占用、带宽、推理速度、功耗、硬件兼容性和部署成本。"),
    ("误区六：所有层都可以同样量化。", "有些层或少数参数对结果很敏感，工程上常用混合精度，让关键部位保留更高精度。"),
    ("误区七：量化后的速度一定更快。", "不一定。速度还取决于硬件是否支持低精度计算、推理框架是否优化、瓶颈是不是内存搬运。"),
    ("误区八：评测分数不掉就代表真实可用。", "还要看真实用户场景、长文本、边界问题、稳定性和错误类型。平均分不掉，不代表每个关键问题都安全。")
]

SUMMARY = [
    "模型量化的本质，是用更短、更省空间的数字近似表示模型里的大量参数和中间计算。",
    "它让大模型推理更省显存、更快、更便宜，是 AI 从实验室走向手机、企业和边缘设备的重要工程基础。",
    "量化不是免费午餐：真正可靠的量化，需要在成本收益和能力损失之间做测试、校准和取舍。"
]

QUIZ = [
    "为什么把 32 位数字变成 4 位数字可能让模型更快？请从“显存”和“数据搬运”两个角度解释。",
    "如果一个客服模型量化后回答速度快了 2 倍，但投诉率上升，你会检查哪些环节？",
    "请用“旅行行李箱”的类比解释：为什么量化不是简单地把东西越删越好？"
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
        radial-gradient(circle at 88% 18%, rgba(15, 139, 141, .14), transparent 24%),
        linear-gradient(90deg, rgba(18, 56, 114, .10), transparent 42%),
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
      <h1>模型量化<br><span>Quantization</span></h1>
      <p class="subtitle">为什么大模型可以变小、变快、变便宜，却还能大体保持聪明？</p>
      <div class="core">核心一句话：模型量化的本质，是把模型里的精细大数字，聪明地换成更短、更省空间的小数字。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>它解决什么？</b><p>降低显存、算力和部署成本，让模型更容易进入真实设备与业务系统。</p></div>
        <div class="cover-card"><b>它改变什么？</b><p>AI 不再只能依赖昂贵服务器，也能靠更轻的模型走向本地和边缘场景。</p></div>
        <div class="cover-card"><b>今天怎么学？</b><p>用“旅行行李箱”和“重新画刻度尺”的类比，看懂量化的收益与代价。</p></div>
      </div>
      <nav aria-label="目录">
        $toc
      </nav>
    </div>
  </header>

  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">AI 能不能普及，不只取决于模型是否聪明，还取决于它是否跑得起、够不够快、成本是否可控。</p>
      $why
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：把超重行李箱收拾成随身箱</h2>
      $analogy
      <figure>
        <img src="$fig_compress" alt="模型量化把32位数字变成8位或4位数字，使模型更省显存、推理更快、更容易部署">
        <figcaption>图解：量化不是随便删东西，而是把原来很精细的数字，映射成更短、更适合推理的数字格式。</figcaption>
      </figure>
      <div class="note">一句话判断：量化不是让模型“变小就完事”，而是在“省成本”和“保能力”之间寻找可接受的平衡点。</div>
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：重新画一把更粗但更省的刻度尺</h2>
      <p class="lead">模型量化的核心动作，是把高精度数值映射到低精度格子里，再检查这种近似是否仍然够用。</p>
      <div class="steps">
        $mechanism
      </div>
      <figure>
        <img src="$fig_workflow" alt="模型量化工作流：原始模型、量化校准、低精度推理、质量检查">
        <figcaption>图解：一个可靠的量化流程通常包括观察数值范围、校准刻度、低精度推理和质量检查。</figcaption>
      </figure>
      <div class="callout">最关键的直觉：量化省下来的不只是硬盘空间，更是推理时显存带宽、计算时间和硬件成本。</div>
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
      <h2>5. 一个真实应用案例：手机端 AI 与企业客服</h2>
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
        fig_compress=image_data_uri(FIG_COMPRESS),
        fig_workflow=image_data_uri(FIG_WORKFLOW),
    )


def write_email_files() -> None:
    (ROOT / "email_subject.txt").write_text(
        "【AI每日深度科普】模型量化：为什么大模型可以变小、变快、变便宜？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        "\n".join(
            [
                "今天的主题是 模型量化（Quantization）。",
                "",
                "它解释的是：为什么大模型可以从昂贵服务器走向手机、本地电脑、企业私有化和边缘设备。",
                "",
                "附件用“旅行行李箱”和“重新画刻度尺”的生活化类比，讲清楚 32位、8位、4位、校准、低精度推理，以及量化为什么能让 AI 更省显存、更快、更便宜。",
                "",
                "适合：非技术读者、AI初学者、产品经理、投资研究者和正在关注 AI 部署成本的人阅读。",
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
