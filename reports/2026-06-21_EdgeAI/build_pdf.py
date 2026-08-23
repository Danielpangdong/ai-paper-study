from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from string import Template

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-21"
CONCEPT_CN = "边缘AI"
CONCEPT_EN = "Edge AI"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_ANALOGY = "chatgpt_edge_ai_analogy.png"
FIG_WORKFLOW = "chatgpt_edge_ai_workflow.png"


WHY = [
    "先想一个很普通的问题：为什么手机相册能马上识别照片里的人和宠物？为什么汽车看到行人要立刻刹车，不能先把视频传到远方服务器再等结果？这背后就是边缘AI要解决的问题。",
    "过去很多AI像住在云端机房里的专家。你把数据发过去，它计算完再把答案发回来。这个方式很强大，但在网络慢、隐私敏感、现场反应必须很快的时候，就会出现麻烦。",
    "边缘AI的核心思想，是把一部分智能放到离现场更近的地方：手机、摄像头、汽车、工厂设备、路由器、边缘服务器。它不是让所有事情都离开云端，而是让需要立刻判断的事情先在本地完成。",
    "这件事正在改变AI落地方式。AI不再只是网页里的聊天框，也可以变成仓库里的视觉质检、车里的安全提醒、医院设备旁的初步识别、手机上的离线助手和工厂现场的异常预警。",
]

ANALOGY = [
    "想象一座城市里只有一个中央大厨房。它厨师多、设备全，可以做复杂大餐。但如果全城每个人买早餐、热牛奶、切水果都要送到中央大厨房处理，路上会排队，配送会变慢，很多小事也没必要这么折腾。",
    "于是城市里出现了很多就近小厨房。小厨房不负责研发新菜谱，也不负责做最复杂的大餐，但它能快速完成日常小任务：加热、切配、简单烹饪、应急供餐。真正复杂的问题，再送回中央大厨房。",
    "边缘AI就像这些就近小厨房。手机、摄像头、汽车和工厂设备在现场先做快速判断：这是不是人脸？这条生产线有没有异常？这辆车前方是不是有障碍物？只在需要更强能力、全局学习或长期保存时，才把摘要或结果传回云端。",
    "所以边缘AI的关键不是“把云端干掉”，而是分工：现场小厨房负责快、近、隐私和稳定；中央大厨房负责强算力、大规模训练、复杂分析和模型更新。",
]

MECHANISM = [
    ("现场产生数据", "摄像头、麦克风、传感器、手机、汽车或机器设备不断产生数据。边缘AI首先关心的是：这些数据是不是必须马上处理？"),
    ("在本地做预处理", "设备会先过滤无用信息，例如裁剪画面、降噪、提取关键片段、压缩数据。这样不用把全部原始数据都传出去。"),
    ("小模型就近推理", "一个适合设备运行的模型在本地判断结果。它通常经过量化、压缩或蒸馏，目标是够快、够省电、够稳定。"),
    ("立即触发现实动作", "如果识别到风险，系统可以马上行动：刹车、报警、拒绝开门、停机、提示用户。这里的等待时间越短越好。"),
    ("只上传必要信息", "系统不一定上传完整视频、完整语音或全部传感器数据，而是上传摘要、异常片段、统计结果或用户允许的数据。"),
    ("云端训练再下发", "云端仍然负责大规模训练、统一评估、复杂推理和模型升级。更新后的模型再下发到设备，形成端云协同。"),
]

TERMS = [
    ("边缘设备 Edge Device", "专业解释：靠近数据产生现场并能执行计算的设备。", "白话解释：就在你身边干活的小机器，比如手机、摄像头、汽车芯片。"),
    ("边缘网关 Edge Gateway", "专业解释：连接多个现场设备并承担汇总、过滤或本地计算的节点。", "白话解释：像小区门口的值班室，先集中处理附近的信息。"),
    ("云端 Cloud", "专业解释：远程数据中心提供的大规模计算、存储和训练能力。", "白话解释：远处的大机房，算力强，但来回传输要时间。"),
    ("设备端推理 On-device Inference", "专业解释：模型直接在设备上运行并给出预测结果。", "白话解释：不用每次问远方服务器，设备自己先判断。"),
    ("延迟 Latency", "专业解释：从输入发生到系统给出响应之间的时间。", "白话解释：你等答案或动作发生要多久。"),
    ("带宽 Bandwidth", "专业解释：单位时间内网络能够传输的数据量。", "白话解释：像马路宽度，视频车流太大就会堵。"),
    ("隐私 Privacy", "专业解释：个人或敏感数据被收集、传输、使用和保存时的保护要求。", "白话解释：有些数据最好不要离开本地。"),
    ("离线可用 Offline Availability", "专业解释：系统在无网络或弱网络下仍能完成关键功能。", "白话解释：没网时也能做一些重要判断。"),
    ("模型更新 Model Update", "专业解释：将新训练或修正后的模型版本部署到设备上。", "白话解释：给设备里的AI换一个更聪明的新版本。"),
    ("端云协同 Edge-cloud Collaboration", "专业解释：设备端、边缘节点和云端按任务特点分工合作。", "白话解释：小事就近办，大事回总部办。"),
]

CASE = [
    "一个真实应用案例是智能摄像头的安全识别。摄像头每天会看到大量画面，如果每一帧都上传到云端，不仅占带宽，还可能带来隐私问题；如果网络不稳定，警报还可能延迟。",
    "边缘AI的做法是让摄像头或本地网关先运行一个视觉模型。它在现场判断画面里是否有人、是否有异常闯入、是否出现危险动作。大多数普通画面可以直接丢弃或只保存简短记录。",
    "当模型发现异常时，系统可以马上亮灯、报警、通知值班人员，或只上传关键片段给云端复核。云端再用更强模型做复杂分析，并把改进后的模型版本下发到摄像头。",
    "这个例子说明了边缘AI的现实价值：不是为了炫技，而是让AI在现场更快反应、减少数据传输、降低云端成本，并让敏感原始数据少离开本地。",
]

MISTAKES = [
    ("误区一：边缘AI就是不用云端。", "不是。边缘AI更准确的说法是端云分工：现场负责快速判断，云端负责训练、复杂分析和更新。"),
    ("误区二：只要模型在手机上跑，就是边缘AI做得好。", "不一定。还要看速度、耗电、发热、准确率、异常情况和用户是否真的受益。"),
    ("误区三：边缘AI一定比云端更便宜。", "不一定。设备芯片、维护、模型更新和现场管理也有成本。便宜与否取决于规模和场景。"),
    ("误区四：边缘AI天然保护隐私。", "也不一定。它能减少原始数据上传，但本地存储、权限、加密和日志管理仍然很重要。"),
    ("误区五：边缘AI只能跑很弱的小模型。", "不完全对。设备端模型通常更小，但经过量化、压缩和硬件加速后，可以完成很多高价值任务。"),
    ("误区六：网络越快，边缘AI越没用。", "不对。即使网络很快，自动驾驶、工业控制、医疗设备等场景仍然需要本地即时反应。"),
    ("误区七：边缘AI只和硬件有关。", "不是。它同时涉及模型压缩、数据治理、软件更新、权限管理、监控和产品设计。"),
    ("误区八：所有任务都应该放到边缘。", "不对。需要全局知识、长时间推理、大规模训练或跨用户学习的任务，仍然适合云端。"),
]

SUMMARY = [
    "边缘AI的本质，是把一部分智能放到离数据和用户更近的地方。",
    "它最适合需要快速反应、隐私敏感、网络不稳定或传输成本高的场景。",
    "真正成熟的边缘AI不是反云端，而是端云协同：小事就近办，大事回云端办。",
]

QUIZ = [
    "为什么自动驾驶或工厂安全预警不能完全依赖云端返回结果？请用“延迟”解释。",
    "边缘AI能减少隐私风险，但为什么不能说它天然安全？还需要哪些保护？",
    "如果你要设计一个手机离线翻译功能，哪些部分适合放在设备端，哪些部分适合留给云端？",
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
      <h1>边缘AI<br><span>Edge AI</span></h1>
      <p class="subtitle">为什么 AI 不总在云端，而要跑到手机、汽车和摄像头旁边？</p>
      <div class="core">核心一句话：边缘AI的本质，是把需要快速、隐私和稳定响应的智能，放到离数据产生现场更近的地方。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>它解决什么？</b><p>解决云端往返太慢、数据传输太多、隐私压力太大、弱网场景不稳定的问题。</p></div>
        <div class="cover-card"><b>它改变什么？</b><p>让 AI 从网页和机房，走进手机、汽车、工厂、摄像头和本地设备。</p></div>
        <div class="cover-card"><b>今天怎么学？</b><p>用“就近小厨房”的类比，看懂设备端、边缘网关和云端如何分工。</p></div>
      </div>
      <nav aria-label="目录">
        ${toc}
      </nav>
    </div>
  </header>

  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">边缘AI解释的是：为什么真实世界里的AI，不能永远等云端服务器慢慢回答。</p>
      ${why}
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：就近小厨房</h2>
      ${analogy}
      <figure>
        <img src="${fig_analogy}" alt="边缘AI类比图：现场设备、就近小厨房和中央大厨房分工">
        <figcaption>图解：边缘AI像就近小厨房，负责快速、隐私、低传输的现场判断；云端像中央大厨房，负责复杂任务和全局更新。</figcaption>
      </figure>
      <div class="callout">最关键的直觉：边缘AI不是反云端，而是把“必须马上办的小事”放在现场，把“大事和长期学习”交给云端。</div>
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：从现场数据到端云协同</h2>
      <p class="lead">边缘AI不是一个单独按钮，而是一条从数据产生、就近推理、现场行动到云端更新的链路。</p>
      <figure>
        <img src="${fig_workflow}" alt="边缘AI工作流：现场数据、本地预处理、设备端推理、立即行动、上传摘要、云端更新">
        <figcaption>图解：边缘AI把关键判断前移到现场，再把必要信息交给云端做更强分析和模型升级。</figcaption>
      </figure>
      <div class="steps">
        ${steps}
      </div>
      <div class="note">注意：边缘AI通常需要模型压缩、量化、蒸馏、芯片加速和监控系统一起配合，不是把一个超大模型硬塞进设备就结束。</div>
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
      <h2>5. 一个真实应用案例：智能摄像头的现场识别</h2>
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
        "【AI每日深度科普】边缘AI：为什么 AI 要跑到你身边？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        """今天的主题是 边缘AI（Edge AI）。

它解释了一个非常现实的问题：
为什么很多 AI 不能永远等云端回答，而必须在手机、汽车、摄像头、工厂设备旁边先做判断。

附件内容将用“就近小厨房”的生活化方式解释：
边缘AI如何在速度、隐私、网络稳定性和云端能力之间做分工；
以及为什么成熟的AI产品往往不是纯云端，也不是纯本地，而是端云协同。

适合：非技术读者、AI初学者、产品经理、投资研究者和关注 AI 落地场景的人阅读。""",
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
