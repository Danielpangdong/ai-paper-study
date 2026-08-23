from __future__ import annotations

from html import escape
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-14"
CONCEPT_CN = "AI工作流"
CONCEPT_EN = "AI Workflow"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_KITCHEN = ROOT / "chatgpt_ai_workflow_kitchen.png"
FIG_ARCH = ROOT / "chatgpt_ai_workflow_architecture.png"


WHY = [
    "很多人第一次用大模型，会以为 AI 产品就是一个聊天框：输入问题，等待回答。可是真正进入工作场景后，人们很快会发现：一次回答再聪明，也很难直接变成稳定的业务结果。",
    "比如写周报、处理客户投诉、生成合同初稿、分析销售数据、整理会议纪要，这些任务都不是“说一句话就结束”。它们需要资料、步骤、工具、检查、人工确认和后续记录。AI工作流要解决的，就是把这些环节串起来。",
    "它改变了 AI 的使用方式：从“我问 AI 一个问题”，升级为“我设计一套流程，让 AI 在正确的时间做正确的事，并且每一步都能被检查”。这也是企业里 AI 能否真正落地的分水岭。",
]

ANALOGY = [
    "想象一家外卖厨房。顾客下单后，不是某个厨师凭灵感变出一份餐，而是一套流程开始运转：系统接单，后厨备菜，厨师烹饪，打包员核对，骑手配送，平台记录评价。",
    "如果只看最后那盒饭，你可能以为关键是“厨师厉害”。但一家店能稳定出餐，靠的是流程：谁负责看订单，谁负责查库存，哪一步检查辣度，哪一步确认地址，出了问题怎样追踪。",
    "AI工作流也是这样。大模型像一个很会处理语言和信息的厨师，但它要稳定服务真实工作，就需要订单、资料、工具、质检和日志。没有流程，AI 可能偶尔惊艳；有了流程，AI 才更可能持续可靠。",
]

MECHANISM = [
    ("触发任务", "工作流先要知道什么时候开始：用户点击按钮、每天定时运行、客户发来邮件，或业务系统出现新事件。"),
    ("收集上下文", "把模型需要的资料准备好，例如文件、数据库记录、知识库片段、历史对话和业务规则。"),
    ("拆解步骤", "把大任务拆成小步骤：先理解需求，再检索资料，再生成草稿，再检查格式，最后交付结果。"),
    ("调用工具", "模型不只靠“脑内回答”，还可以调用搜索、代码、表格、API、邮件、数据库等外部能力。"),
    ("设置检查点", "关键步骤要被规则检查：权限是否允许、格式是否正确、事实是否有出处、成本是否超标、安全风险是否过高。"),
    ("人工介入", "高风险决策不要全自动。人可以在批准、修改、拒绝和补充信息的位置进入流程。"),
    ("交付结果", "结果可以是一份报告、一封邮件、一个工单、一条通知，或对业务系统的一次更新。"),
    ("记录改进", "把输入、输出、失败原因和修改意见记下来，用于复盘、评估和优化下一版流程。"),
]

TERMS = [
    ("Workflow 工作流", "专业解释：由触发条件、步骤、工具、检查和输出组成的任务执行流程。", "白话解释：把一件事拆成固定步骤，让它能反复稳定地完成。"),
    ("Trigger 触发器", "专业解释：启动工作流的事件或条件。", "白话解释：像闹钟或订单铃声，告诉系统“现在该开始了”。"),
    ("Context 上下文", "专业解释：模型执行任务时可用的资料、规则、历史记录和当前状态。", "白话解释：给 AI 放到桌上的参考材料。"),
    ("Tool 工具", "专业解释：模型可调用的外部能力，例如搜索、代码执行、数据库查询或邮件发送。", "白话解释：AI 的计算器、资料库、电话和办事窗口。"),
    ("State 状态", "专业解释：工作流运行过程中保存的进度、变量和中间结果。", "白话解释：流程的小本子，记录现在做到哪一步。"),
    ("Guardrail 护栏", "专业解释：限制模型行为、检查风险和阻止错误操作的规则或系统。", "白话解释：流程里的刹车和红线。"),
    ("Human-in-the-loop 人在回路中", "专业解释：在关键环节加入人工审核、批准或修正。", "白话解释：重要决定别让 AI 单独拍板，人要能接管。"),
    ("Evaluation 评估", "专业解释：用指标、样例和人工判断衡量工作流输出质量。", "白话解释：不是感觉“还行”，而是定期看它到底做得好不好。"),
]

CASE = [
    "一个真实应用是“自动生成客户投诉处理摘要”。差的做法是把客户原文直接丢给 AI，让它写一段总结。这样看似省事，但很容易漏掉订单号、赔付规则、历史沟通和风险等级。",
    "更可靠的 AI 工作流会这样运行：客服系统收到投诉后触发流程；系统读取订单信息、物流轨迹、历史工单和公司政策；模型先提取客户诉求，再判断问题类型；然后调用知识库查找处理规则；生成客服回复草稿；检查是否承诺了超权限赔付；最后由人工客服确认发送。",
    "这套流程的价值不是让 AI 替代所有客服，而是让客服少做重复整理，多做判断和沟通。客户得到更快回应，公司也能追踪每一步为什么这样处理。",
]

MISTAKES = [
    ("误区一：AI工作流就是把几个提示词连起来。", "提示词只是其中一部分。真正的工作流还包括资料输入、工具调用、权限控制、检查点、日志和人工审核。"),
    ("误区二：工作流越自动化越先进。", "不一定。涉及钱、法律、医疗、安全和客户承诺的步骤，常常需要人工确认。好工作流不是全自动，而是把自动化放在合适的位置。"),
    ("误区三：有了 Agent，就不需要工作流。", "Agent 更像会自己规划的执行者，工作流更像可审计的流程设计。真实系统通常需要两者结合，而不是互相替代。"),
    ("误区四：一次跑通就说明流程可靠。", "演示成功不等于生产可靠。必须看异常情况、边界输入、权限失败、成本波动和长期质量。"),
    ("误区五：工作流能消除 AI 幻觉。", "不能完全消除，但可以通过检索证据、事实核查、引用来源和人工审核来降低风险。"),
    ("误区六：所有任务都该做成复杂工作流。", "简单问题直接聊天就够了。只有重复、高价值、需要追踪或需要协作的任务，才值得流程化。"),
]

SUMMARY = [
    "AI工作流的本质，是把 AI 能力放进可重复、可检查、可改进的任务流程。",
    "它让 AI 从“会回答问题”变成“能参与完成工作”，关键环节包括资料、工具、检查、人工确认和日志。",
    "普通人理解 AI工作流，就能更清楚地判断：哪些任务适合自动化，哪些步骤必须保留人的判断。",
]

QUIZ = [
    "为什么一家外卖店不能只靠“厨师很厉害”来保证稳定出餐？这个类比对应 AI工作流里的哪些环节？",
    "如果要设计一个“自动生成会议纪要并发给参会人”的 AI工作流，你会设置哪些输入、工具、检查点和人工确认环节？",
    "为什么说 AI工作流不是越自动越好？请举一个需要人工审核的高风险场景说明。",
]


def p(items: list[str]) -> str:
    return "\n".join(f"<p>{escape(item)}</p>" for item in items)


def mechanism_cards() -> str:
    return "\n".join(
        f"""
        <article class="step-card">
          <div class="step-num">{idx:02d}</div>
          <div>
            <h3>{escape(title)}</h3>
            <p>{escape(body)}</p>
          </div>
        </article>
        """
        for idx, (title, body) in enumerate(MECHANISM, 1)
    )


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
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{DATE}_{escape(CONCEPT_FULL)}</title>
  <style>
    :root {{
      --ink: #111827;
      --muted: #4b5563;
      --quiet: #64748b;
      --line: #d7e0ea;
      --paper: #ffffff;
      --soft: #f7fafc;
      --blue: #0f3b7a;
      --teal: #0f8b8d;
      --green: #24865a;
      --amber: #d97706;
      --red: #c2410c;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background: #edf2f7;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
    }}
    .cover {{
      background: var(--paper);
      border-bottom: 1px solid var(--line);
      padding: 64px 26px 44px;
    }}
    .wrap {{ max-width: 1080px; margin: 0 auto; }}
    .eyebrow {{
      color: var(--teal);
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 0;
    }}
    h1 {{
      max-width: 980px;
      margin: 18px 0 14px;
      color: var(--ink);
      font-size: clamp(44px, 7vw, 84px);
      line-height: 1.04;
      letter-spacing: 0;
    }}
    h1 span {{ color: var(--blue); }}
    .subtitle {{
      max-width: 900px;
      margin: 0;
      color: var(--muted);
      font-size: clamp(22px, 3.3vw, 34px);
      line-height: 1.35;
      font-weight: 650;
    }}
    .core {{
      max-width: 940px;
      margin-top: 28px;
      padding: 18px 22px;
      border: 1px solid #99f6e4;
      border-left: 8px solid var(--teal);
      border-radius: 8px;
      background: #f0fdfa;
      color: #0f766e;
      font-size: 20px;
      font-weight: 800;
    }}
    .cover-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-top: 34px;
    }}
    .cover-card {{
      min-height: 146px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--soft);
      padding: 18px;
    }}
    .cover-card b {{ display: block; color: var(--blue); font-size: 20px; margin-bottom: 8px; }}
    .cover-card p {{ margin: 0; color: var(--muted); font-size: 16px; line-height: 1.65; }}
    nav {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 10px;
      margin-top: 30px;
    }}
    nav a {{
      display: block;
      padding: 10px 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      color: var(--blue);
      font-weight: 750;
      text-decoration: none;
    }}
    main {{ padding: 34px 26px 80px; }}
    section {{
      max-width: 1080px;
      margin: 0 auto 28px;
      padding: 30px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--paper);
    }}
    h2 {{
      margin: 0 0 16px;
      color: var(--ink);
      font-size: 32px;
      line-height: 1.25;
      letter-spacing: 0;
    }}
    h3 {{ margin: 0 0 6px; color: var(--blue); font-size: 21px; line-height: 1.3; }}
    p {{ margin: 12px 0; font-size: 18px; }}
    .lead {{ color: var(--muted); font-size: 20px; font-weight: 680; }}
    figure {{ margin: 20px 0 8px; }}
    img {{
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: white;
    }}
    figcaption {{ margin-top: 8px; color: var(--quiet); font-size: 14px; }}
    .steps {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 20px;
    }}
    .step-card {{
      display: grid;
      grid-template-columns: 54px 1fr;
      gap: 14px;
      min-height: 126px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdff;
      break-inside: avoid;
    }}
    .step-num {{
      display: grid;
      place-items: center;
      width: 46px;
      height: 46px;
      border-radius: 8px;
      background: var(--blue);
      color: white;
      font-weight: 900;
    }}
    .step-card p {{ margin: 0; color: var(--muted); font-size: 16px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 15.5px; }}
    th, td {{ border: 1px solid var(--line); padding: 12px; vertical-align: top; }}
    th {{ width: 22%; background: #f8fafc; color: var(--blue); text-align: left; }}
    ul, ol {{ padding-left: 24px; }}
    li {{ margin: 10px 0; font-size: 18px; }}
    .mistakes {{ list-style: none; padding: 0; margin: 8px 0 0; }}
    .mistakes li {{
      border: 1px solid var(--line);
      border-left: 6px solid var(--amber);
      border-radius: 8px;
      padding: 13px 16px;
      background: #fffaf0;
      break-inside: avoid;
    }}
    .mistakes strong {{ display: block; color: #9a3412; margin-bottom: 4px; }}
    .mistakes span {{ color: var(--muted); }}
    .note {{
      margin-top: 18px;
      padding: 16px 18px;
      border: 1px solid #bfdbfe;
      border-radius: 8px;
      background: #eff6ff;
      color: var(--blue);
      font-size: 18px;
      font-weight: 750;
    }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
    }}
    .summary-card {{
      min-height: 170px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fafc;
      font-size: 17px;
      font-weight: 700;
    }}
    footer {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 8px 30px 34px;
      color: var(--quiet);
      font-size: 14px;
    }}
    @page {{ size: A4; margin: 15mm 13mm 17mm; }}
    @media print {{
      body {{ background: #fff; }}
      .cover {{
        min-height: 238mm;
        padding: 0;
        border-bottom: 0;
        break-after: page;
      }}
      .cover .wrap {{ padding-top: 8mm; }}
      main {{ padding: 0; }}
      section {{
        max-width: none;
        margin: 0 0 10mm;
        padding: 0;
        border: 0;
        border-radius: 0;
      }}
      nav {{ break-inside: avoid; }}
      .cover-grid, .steps, .summary-grid {{ break-inside: avoid; }}
      h2 {{ break-after: avoid; }}
      figure, table, .step-card, .mistakes li, .summary-card {{ break-inside: avoid; }}
      a {{ color: inherit; }}
    }}
    @media (max-width: 760px) {{
      .cover-grid, .steps, .summary-grid {{ grid-template-columns: 1fr; }}
      section {{ padding: 22px; }}
    }}
  </style>
</head>
<body>
  <header class="cover">
    <div class="wrap">
      <div class="eyebrow">AI每日深度科普 · {DATE}</div>
      <h1>{escape(CONCEPT_CN)}<br><span>{escape(CONCEPT_EN)}</span></h1>
      <p class="subtitle">为什么 AI 真正落地，靠的不是一次神奇回答，而是一套可复用流程？</p>
      <div class="core">核心一句话：AI工作流的本质，是把 AI 能力放进可重复、可检查、可改进的任务流程。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>从聊天到做事</b><p>它解释 AI 如何从一次回答，变成能持续参与办公、客服、分析和运营的流程。</p></div>
        <div class="cover-card"><b>连接前序知识</b><p>它把提示词、RAG、Function Calling、Agent、护栏和评估串成一个系统。</p></div>
        <div class="cover-card"><b>决定落地质量</b><p>企业级 AI 不是只看模型多强，还要看流程是否可控、可查、可改。</p></div>
      </div>
      <nav>{toc_html}</nav>
    </div>
  </header>
  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">AI工作流是把“模型能力”变成“可靠工作结果”的桥。</p>
      {p(WHY)}
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：外卖厨房流水线</h2>
      <figure>
        <img src="{FIG_KITCHEN.name}" alt="AI工作流像外卖厨房流水线">
        <figcaption>外卖厨房能稳定出餐，不只靠厨师，而靠接单、分工、加工、质检、配送和复盘。AI工作流也是同样的逻辑。</figcaption>
      </figure>
      {p(ANALOGY)}
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：一套 AI 工作流怎样运转？</h2>
      <figure>
        <img src="{FIG_ARCH.name}" alt="AI工作流的真实运行结构">
        <figcaption>从触发器到交付结果，AI工作流把模型、资料、工具、检查和日志连接成一条可追踪链路。</figcaption>
      </figure>
      <div class="steps">{mechanism_cards()}</div>
      <div class="note">判断一个任务是否适合做成 AI工作流，可以问：它是否重复发生、资料是否明确、结果是否需要检查、失败是否有成本？</div>
    </section>

    <section id="terms">
      <h2>4. 关键术语解释</h2>
      <table>
        <thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead>
        <tbody>{term_rows()}</tbody>
      </table>
    </section>

    <section id="case">
      <h2>5. 一个真实应用案例：客户投诉处理摘要</h2>
      {p(CASE)}
      <div class="note">现实价值：AI工作流把“让 AI 帮客服整理一下”升级成一套能追踪、能审核、能持续改进的服务流程。</div>
    </section>

    <section id="mistakes">
      <h2>6. 常见误区</h2>
      <ul class="mistakes">{mistake_items()}</ul>
    </section>

    <section id="summary">
      <h2>7. 3句话总结</h2>
      <div class="summary-grid">
        <div class="summary-card">1. {escape(SUMMARY[0])}</div>
        <div class="summary-card">2. {escape(SUMMARY[1])}</div>
        <div class="summary-card">3. {escape(SUMMARY[2])}</div>
      </div>
    </section>

    <section id="quiz">
      <h2>8. 复习问题</h2>
      <ol>{numbered(QUIZ)}</ol>
    </section>
  </main>
  <footer>{DATE} · {escape(CONCEPT_FULL)} · AI每日深度科普</footer>
</body>
</html>
"""


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1800}, device_scale_factor=1)
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True)
        page.screenshot(path=str(ROOT / "html_preview.png"), full_page=False)
        page.evaluate("window.scrollTo({ top: 1900, behavior: 'instant' })")
        page.wait_for_timeout(200)
        page.screenshot(path=str(ROOT / "html_midpage_preview.png"), full_page=False)
        browser.close()


def build() -> None:
    missing = [path for path in (FIG_KITCHEN, FIG_ARCH) if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing expected figure(s): " + ", ".join(str(p) for p in missing))

    html_path = ROOT / HTML_NAME
    pdf_path = ROOT / PDF_NAME
    html_path.write_text(build_html(), encoding="utf-8")
    render_pdf(html_path, pdf_path)

    (ROOT / "email_subject.txt").write_text(
        "【AI每日深度科普】AI工作流：为什么 AI 落地靠流程，而不是一次回答？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        "\n".join(
            [
                "今天的主题是 AI Workflow（AI工作流）。",
                "",
                "它是把大模型从“会聊天”变成“能稳定参与工作”的关键概念：触发任务、准备资料、调用工具、设置检查点、交付结果，并持续复盘改进。",
                "",
                "附件内容将用“外卖厨房流水线”的生活化类比解释：",
                "为什么真实 AI 落地靠可复用流程，而不是一次神奇回答。",
                "",
                "适合：非技术读者、AI 初学者、产品经理、运营、客服管理者、知识工作者阅读。",
            ]
        ),
        encoding="utf-8",
    )

    print(pdf_path)
    print(html_path)
    print(FIG_KITCHEN)
    print(FIG_ARCH)


if __name__ == "__main__":
    build()
