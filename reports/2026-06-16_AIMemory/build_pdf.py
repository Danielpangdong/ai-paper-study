from __future__ import annotations

from html import escape
from pathlib import Path
from string import Template

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-16"
CONCEPT_CN = "AI记忆"
CONCEPT_EN = "AI Memory"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_NOTEBOOK = "chatgpt_ai_memory_notebook.png"
FIG_ARCH = "chatgpt_ai_memory_architecture.png"


WHY = [
    "如果一个 AI 助手每次见到你都像第一次见面，它就很难真正帮你做长期事情。你要反复解释项目背景、个人偏好、格式要求、已经踩过的坑，AI 也容易把旧结论和新目标混在一起。",
    "AI记忆要解决的，是“持续协作”的问题：哪些信息只属于本次对话，哪些信息值得下次继续使用，哪些信息已经过期或需要删除。它让 AI 从一次性回答，走向能参与长期项目的助手。",
    "这个概念对 AI 行业很重要，因为 Agent、AI工作流、多Agent系统、AI客服、个人助理和企业 Copilot 都离不开记忆。没有记忆，系统很难积累经验；记忆设计不好，又会带来隐私、误用和错误放大的风险。",
]

ANALOGY = [
    "想象一个高中生准备期末考试。聪明的学生不会把老师讲过的每一句话都背下来，也不会每次复习都从零开始。他会把重点、错题、解题套路和老师强调的地方写进笔记本。",
    "但笔记本也不是越厚越好。如果把无关闲聊、临时猜测、已经过期的信息都写进去，复习时反而会被干扰。好的笔记要会筛选、分类、标日期，还要定期改正。",
    "AI记忆也是这样。它不是“模型突然拥有了人类记忆”，而是一个被设计出来的外部记录系统：把有长期价值的信息保存成结构化记录，在未来相关任务中检索出来，再和当前上下文一起使用。",
]

MECHANISM = [
    ("看到当前上下文", "AI 先读取本次对话、用户目标、可用工具和当前任务。这就像桌面上摊开的材料，只在本次工作中最直接可见。"),
    ("提取候选记忆", "系统从对话里识别可能值得保存的信息，例如事实、偏好、长期目标、限制条件、常用格式和做事步骤。"),
    ("按规则筛选写入", "不是所有内容都该记。系统要判断信息是否稳定、是否有复用价值、是否敏感、是否需要用户允许，以及是否已有更准确版本。"),
    ("结构化保存", "合格信息会变成记忆卡片，带上类型、来源、时间、置信度、权限和标签。这样以后才能知道它从哪里来、该不该用。"),
    ("在新任务中检索", "当用户提出新问题时，系统不会把所有记忆都塞进回答，而是只找与当前目标相关、仍然有效、允许使用的记录。"),
    ("融合后生成回答", "AI 把当前上下文、检索到的记忆、外部资料和工具结果放在一起，生成更贴合用户和任务的输出。"),
    ("更新与纠错", "如果用户说“我现在不住那里了”或“这个偏好改了”，系统要能合并、覆盖或标记冲突，避免旧记忆继续误导。"),
    ("遗忘与权限控制", "记忆必须能删除、过期和降权。真正可靠的 AI 记忆，不是记得最多，而是知道什么该记、什么时候该忘、谁有权使用。"),
]

TERMS = [
    ("Context Window 上下文窗口", "专业解释：模型在一次生成时能够直接读取的输入范围。", "白话解释：本次对话桌面上摊开的材料，离开桌面就不一定还在。"),
    ("Persistent Memory 持久记忆", "专业解释：跨会话保存、可在未来任务中再次读取的外部记录。", "白话解释：AI 的项目笔记本，不是临时草稿纸。"),
    ("Episodic Memory 情景记忆", "专业解释：记录曾经发生的交互、事件、决策和结果。", "白话解释：像日记，记得“上次我们做过什么”。"),
    ("Semantic Memory 语义记忆", "专业解释：保存较稳定的知识、偏好、身份信息和长期约束。", "白话解释：像通讯录和偏好表，记得“你通常喜欢什么”。"),
    ("Procedural Memory 程序记忆", "专业解释：保存完成某类任务的方法、步骤和工作流。", "白话解释：像操作手册，记得“这件事应该怎么做”。"),
    ("Write Policy 写入策略", "专业解释：决定哪些信息可以写入记忆、如何保存、是否需要权限的规则。", "白话解释：笔记本的收录标准，不是什么都抄。"),
    ("Retriever 检索器", "专业解释：根据当前任务从记忆库中找出相关记录的组件。", "白话解释：帮 AI 翻笔记的人，只找有用页。"),
    ("Forgetting 遗忘机制", "专业解释：删除、过期、降权或覆盖不再可靠的信息。", "白话解释：清理旧笔记，免得旧答案继续带偏。"),
]

CASE = [
    "一个真实应用是“企业 AI 客服”。客户上个月投诉过配送延迟，这个月又来询问同类订单。如果 AI 完全没有记忆，它只能处理眼前这句话；如果把过去的工单、处理承诺、客户偏好和当前政策结合起来，它就能更快理解背景。",
    "但这不是让 AI 把客户所有话都永远记住。靠谱的做法是：把关键事实写成受权限保护的记录，例如订单号、问题类型、处理状态、承诺时间和客户明确表达的偏好；在新工单出现时，只检索相关记录；当问题解决或政策更新后，记忆也要同步更新。",
    "同样的逻辑也适用于个人 AI 助理。它可以记住你写报告偏好先给摘要、常用受众是非技术读者、某个项目要保留中文术语表。但它不应该把一次闲聊、临时情绪或敏感信息无规则地写入长期记忆。",
]

MISTAKES = [
    ("误区一：AI记忆就是模型训练时学到的知识。", "不是。训练知识像教科书，更新慢且不针对某个用户；AI记忆更像应用层笔记，可以围绕用户、项目和任务动态维护。"),
    ("误区二：上下文窗口越长，就不需要记忆。", "上下文窗口是本次可见材料，长上下文能放更多东西，但不能自动判断什么值得长期保存、何时更新、谁能使用。"),
    ("误区三：记得越多，AI 就越聪明。", "记忆太多会增加噪声、成本和隐私风险。好记忆追求相关、准确、可追溯，而不是无限堆积。"),
    ("误区四：写进记忆的内容一定是真的。", "记忆只是记录，不是事实证明。它需要来源、时间、置信度和纠错机制，否则错误会被反复引用并放大。"),
    ("误区五：AI记忆可以替代 RAG 或搜索。", "不能。RAG 更像查外部资料库，AI记忆更像保存与用户或任务相关的经验。两者经常配合，但作用不同。"),
    ("误区六：个性化记忆一定越强越好。", "个性化要有边界。医疗、财务、身份、家庭等敏感信息需要更严格的权限、最小化保存和可删除能力。"),
    ("误区七：AI 有长期记忆，就等于有人的自我意识。", "长期记忆只是工程能力，不代表模型拥有人的体验、身份或真正的连续自我。不要把产品功能误认为生命特征。"),
]

SUMMARY = [
    "AI记忆的本质，是把有长期价值的信息按规则保存、检索、更新和遗忘，让 AI 能参与持续任务。",
    "它和上下文窗口、RAG、模型训练知识都不同：上下文是本次桌面，RAG 是查资料，记忆是保存可复用经验。",
    "可靠的 AI 记忆不是“什么都记”，而是有写入标准、来源记录、权限控制、纠错机制和遗忘能力。",
]

QUIZ = [
    "为什么“上下文窗口很长”仍然不能完全替代 AI 记忆？请用“本次桌面”和“长期笔记本”的类比解释。",
    "如果一个 AI 助手把一次临时偏好永久保存，未来可能造成什么问题？你会给它设计什么写入规则？",
    "在企业 AI 客服场景中，哪些信息适合写入长期记忆？哪些信息应该只留在本次工单里，或不应该保存？",
]


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
      --ink: #111827;
      --muted: #4b5563;
      --quiet: #64748b;
      --line: #d7e0ea;
      --paper: #ffffff;
      --soft: #f7fafc;
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
      background:
        linear-gradient(90deg, rgba(15,139,141,.09), transparent 34%),
        linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
      border-bottom: 1px solid var(--line);
      padding: 62px 26px 42px;
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
      font-size: clamp(42px, 6.2vw, 78px);
      line-height: 1.05;
      letter-spacing: 0;
    }
    h1 span { color: var(--blue); }
    .subtitle {
      max-width: 920px;
      margin: 0;
      color: var(--muted);
      font-size: clamp(22px, 3vw, 32px);
      line-height: 1.35;
      font-weight: 650;
    }
    .core {
      max-width: 960px;
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
      min-height: 148px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,.88);
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
      min-height: 134px;
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
      .step-card { min-height: 116px; }
      p, li { font-size: 14.5px; line-height: 1.65; }
      h2 { font-size: 24px; }
      h3 { font-size: 17px; }
      table { font-size: 12px; }
      th, td { padding: 8px; }
      .summary-card { min-height: 130px; font-size: 13px; }
      .cover-card p { font-size: 13px; }
      .core { font-size: 17px; }
      nav a { font-size: 13px; padding: 7px 10px; }
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
      <div class="eyebrow">AI每日深度科普 · 2026-06-16</div>
      <h1>AI记忆<br><span>AI Memory</span></h1>
      <p class="subtitle">为什么AI不能只靠本次对话，也需要会整理、会更新、会遗忘的“笔记本”？</p>
      <div class="core">核心一句话：AI记忆的本质，是把有长期价值的信息按规则保存、检索、更新和遗忘，让 AI 能参与持续任务。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>它解决什么？</b><p>AI 每次从零开始的问题，让长期项目、个人偏好和业务状态能被延续。</p></div>
        <div class="cover-card"><b>它改变什么？</b><p>AI 从一次性聊天工具，变成能积累上下文和经验的协作助手。</p></div>
        <div class="cover-card"><b>今天怎么学？</b><p>用“学生笔记本”理解写入、检索、更新和遗忘。</p></div>
      </div>
      <nav aria-label="目录">
        $toc
      </nav>
    </div>
  </header>

  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">真正有用的 AI 助手，不只是会回答这一次，还要能在下一次继续理解你正在做什么。</p>
      $why
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：AI 需要一本会整理的笔记本</h2>
      $analogy
      <figure>
        <img src="$fig_notebook" alt="AI记忆像学生笔记本，把一次经历变成可复用记录">
        <figcaption>图解：AI记忆不是魔法般的人类记忆，而是有筛选、写入、检索、更新规则的外部记录系统。</figcaption>
      </figure>
      <div class="note">判断 AI 记忆是否可靠，可以先问四个问题：记住什么？谁允许？什么时候用？错了怎么改？</div>
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：从本次对话到长期可用经验</h2>
      <p class="lead">AI记忆系统通常包含两个方向：把有价值的信息写进去，在未来相关任务中再找出来。</p>
      <div class="steps">
        $mechanism
      </div>
      <figure>
        <img src="$fig_arch" alt="AI记忆系统从用户输入到长期记忆库再到检索使用的架构图">
        <figcaption>图解：好的 AI 记忆系统要同时处理写入规则、检索规则、维护规则和权限边界，避免无关记忆干扰当前任务。</figcaption>
      </figure>
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
      <h2>5. 一个真实应用案例：企业 AI 客服与个人助理</h2>
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
        fig_notebook=FIG_NOTEBOOK,
        fig_arch=FIG_ARCH,
    )


def write_email_files() -> None:
    (ROOT / "email_subject.txt").write_text(
        "【AI每日深度科普】AI记忆：为什么AI不能只靠本次对话？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        "\n".join(
            [
                "今天的主题是 AI记忆（AI Memory）。",
                "",
                "它解释的是：为什么真正有用的 AI 助手不能每次都从零开始，也不能什么都永久记住，而需要一套会筛选、会检索、会更新、会遗忘的记忆系统。",
                "",
                "附件用“学生笔记本”和“企业 AI 客服”两个类比，讲清楚 AI 记忆如何工作、它和上下文窗口/RAG有什么区别，以及常见误区在哪里。",
                "",
                "适合：非技术读者、AI初学者、产品经理、投资研究者和正在思考 AI Agent 落地的人阅读。",
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
