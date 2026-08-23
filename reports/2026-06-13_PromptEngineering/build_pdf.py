from __future__ import annotations

from html import escape
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-13"
CONCEPT_CN = "提示词工程"
CONCEPT_EN = "Prompt Engineering"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
FIG_TASK = ROOT / "chatgpt_prompt_task_brief.png"
FIG_FLOW = ROOT / "chatgpt_prompt_iteration_flow.png"


WHY = [
    "提示词工程重要，不是因为它能让人背会几句“神奇口令”，而是因为大模型把很多软件的入口从按钮、菜单、表单，变成了自然语言。你怎么描述任务，AI 就怎么理解任务；你不给背景，它只能猜；你不说标准，它就不知道什么算好。",
    "同一个模型，面对“帮我写一份方案”和“面向高中生，用三个生活类比解释 RAG，800 字，最后给 3 个复习问题”，输出质量会完全不同。差别不在模型是否突然变聪明，而在任务是否被说清楚。",
    "当 AI 进入客服、办公、搜索、编程和 Agent 工作流时，提示词就像一份任务合同。它规定目标、角色、资料、边界、输出格式和检查标准。理解提示词工程，等于理解普通人如何把 AI 从“会聊天”变成“能帮忙做事”。",
]

ANALOGY = [
    "想象你让一位新来的实习生帮你做一份竞品分析。如果你只说“做个分析”，他可能不知道分析谁、给谁看、要多长、要不要表格、重点是价格还是功能。最后做出来的东西不一定差，但很可能不合你的用。",
    "更好的布置方式是：你告诉他目标是给产品经理做决策参考；竞品是 A、B、C；重点比较功能、价格、用户评价；输出成一页表格加三条建议；如果资料不足，先列出需要补充的问题。",
    "提示词工程就是这种“清楚布置任务”的能力。AI 不是真的读心，它是在根据你给出的语言线索预测下一步该怎么做。线索越完整，输出越稳定；标准越清楚，修改越省力。",
]

MECHANISM = [
    ("先说目标", "不要只说“写一个东西”，而要说清楚要解决什么问题、给谁使用、成功标准是什么。"),
    ("补充背景", "告诉 AI 任务场景、已有资料、读者水平、行业限制和你已经尝试过的方法。"),
    ("指定角色", "角色不是装饰，而是帮助模型选择语气、知识范围和判断角度，例如老师、审稿人、产品经理、客服主管。"),
    ("约束输出", "明确长度、结构、格式、语言风格、是否需要表格、是否要引用来源、哪些内容不能出现。"),
    ("给出例子", "一两个示例能让 AI 更快理解你要的风格，像给学生看标准答案和扣分点。"),
    ("建立反馈闭环", "让 AI 自检遗漏、歧义和不确定点，再根据你的反馈迭代，而不是指望第一次就完美。"),
]

TERMS = [
    ("Prompt", "专业解释：输入给模型的任务指令、上下文和约束集合。", "白话解释：你对 AI 说的“任务说明书”。"),
    ("System Prompt", "专业解释：系统层面的高优先级规则，用来设定模型身份、边界和行为要求。", "白话解释：像课堂纪律或公司制度，告诉 AI 哪些底线不能越过。"),
    ("User Prompt", "专业解释：用户在一次对话中提出的具体问题或任务请求。", "白话解释：你这一轮真正想让 AI 帮你做的事。"),
    ("Few-shot 示例", "专业解释：在提示词中提供少量输入输出样例，引导模型模仿目标格式或风格。", "白话解释：先给 AI 看几份标准答案，它就更容易照着做。"),
    ("结构化输出", "专业解释：要求模型按表格、JSON、清单、章节等固定格式返回结果。", "白话解释：别让 AI 随便聊，要求它把结果装进规定好的盒子里。"),
    ("Prompt Injection", "专业解释：恶意或无关文本试图覆盖原有指令、诱导模型泄露信息或执行错误操作。", "白话解释：有人把“忽略前面规则”藏进资料里，试图骗 AI 跑偏。"),
    ("上下文窗口", "专业解释：模型一次能读取和利用的文本容量范围。", "白话解释：AI 的临时工作台，东西放太多会挤、会漏、会抓不住重点。"),
]

CASE = [
    "一个真实常见的场景是：运营团队用 AI 写一封活动复盘邮件。差提示词是“写一封复盘邮件”。AI 可能写得流畅，但重点泛泛，缺少数据，也不知道收件人关心什么。",
    "更好的提示词会写清楚：收件人是部门负责人；活动目标是拉新；输入数据包括曝光、点击、转化、成本；邮件要先给结论，再列三条证据，最后给下周行动建议；语气专业克制；如果数据不足，先标注“不确定”。",
    "这样做的效果不是让 AI 变成专家，而是让它更像一个有任务边界的助理。它知道该从哪些信息里提炼结论，也知道输出要方便人直接转发、修改或决策。",
]

MISTAKES = [
    ("误区一：提示词工程就是背固定模板。", "模板只能帮你起步，真正重要的是理解任务、读者、证据和标准。不同场景需要不同提示词。"),
    ("误区二：提示词越长越好。", "不一定。过长、混乱、互相矛盾的提示词会增加噪声。好提示词应该信息充分，但结构清楚。"),
    ("误区三：提示词能弥补所有知识缺口。", "不能。如果模型没有可靠资料，或任务需要实时数据、专业审批、法律判断，提示词再漂亮也不能替代证据和流程。"),
    ("误区四：让 AI “一步一步思考”就一定正确。", "要求模型列出可检查的推理提纲有帮助，但流畅解释不等于真实正确。关键仍然是证据、自检和人类复核。"),
    ("误区五：把敏感信息塞进提示词没关系。", "不对。提示词可能进入日志、工具调用或第三方系统。商业机密、个人隐私和账号凭证都不应随意输入。"),
    ("误区六：AI 越强，提示词工程越没用。", "模型越强，越能处理复杂任务，但复杂协作仍然需要目标、权限、资料、边界和验收标准。"),
]

SUMMARY = [
    "提示词工程的本质，不是咒语，而是把任务、背景、标准和反馈闭环说清楚。",
    "好提示词像一份任务委托书：让 AI 知道要做什么、凭什么做、做到什么程度才算好。",
    "普通人掌握提示词工程，就能把 AI 从“会聊天的工具”变成“能参与工作的助理”。",
]

QUIZ = [
    "为什么“帮我写一篇 AI 文章”通常比“面向高中生，用三个生活类比解释 RAG，800 字，最后给 3 个复习题”效果差？",
    "如果你要让 AI 帮你写一份部门周报，你会在提示词里补充哪四类信息？请按目标、背景、格式、检查标准来回答。",
    "为什么提示词工程不能替代事实核查、隐私保护和人工审批？请举一个高风险场景说明。",
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
      --ink: #101827;
      --muted: #475569;
      --quiet: #64748b;
      --line: #dbe3ef;
      --paper: #ffffff;
      --soft: #f7fafc;
      --navy: #0f2f6b;
      --teal: #0f8b8d;
      --green: #2f8f4e;
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
      text-transform: uppercase;
    }}
    h1 {{
      max-width: 960px;
      margin: 18px 0 14px;
      color: var(--ink);
      font-size: clamp(44px, 7vw, 84px);
      line-height: 1.04;
      letter-spacing: 0;
    }}
    h1 span {{ color: var(--navy); }}
    .subtitle {{
      max-width: 880px;
      margin: 0;
      color: var(--muted);
      font-size: clamp(22px, 3.4vw, 34px);
      line-height: 1.35;
      font-weight: 600;
    }}
    .core {{
      max-width: 920px;
      margin-top: 28px;
      padding: 18px 22px;
      border: 1px solid #a7f3d0;
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
    .cover-card b {{ display: block; color: var(--navy); font-size: 20px; margin-bottom: 8px; }}
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
      color: var(--navy);
      font-weight: 700;
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
    h3 {{ margin: 0 0 6px; color: var(--navy); font-size: 21px; line-height: 1.3; }}
    p {{ margin: 12px 0; font-size: 18px; }}
    .lead {{ color: var(--muted); font-size: 20px; font-weight: 650; }}
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
      min-height: 128px;
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
      background: var(--navy);
      color: white;
      font-weight: 900;
    }}
    .step-card p {{ margin: 0; color: var(--muted); font-size: 16px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 15.5px; }}
    th, td {{ border: 1px solid var(--line); padding: 12px; vertical-align: top; }}
    th {{ width: 16%; background: #f8fafc; color: var(--navy); text-align: left; }}
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
      color: var(--navy);
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
      <p class="subtitle">为什么会提问的人，能让 AI 少跑偏、多产出可用结果？</p>
      <div class="core">核心一句话：提示词工程的本质，不是背咒语，而是把任务、背景、标准和反馈说清楚。</div>
      <div class="cover-grid">
        <div class="cover-card"><b>面向普通人</b><p>它解释的是我们每天怎样与大模型协作，而不是工程师才懂的内部代码。</p></div>
        <div class="cover-card"><b>连接前序知识</b><p>它把上下文窗口、Agent、RAG 和对齐，落到一次具体任务里。</p></div>
        <div class="cover-card"><b>直接影响结果</b><p>同一个模型，任务说明越清楚，输出越稳定、越容易复用。</p></div>
      </div>
      <nav>{toc_html}</nav>
    </div>
  </header>
  <main>
    <section id="why">
      <h2>1. 为什么这个概念重要？</h2>
      <p class="lead">提示词工程是普通人与大模型协作的第一层“操作系统”。</p>
      {p(WHY)}
    </section>

    <section id="analogy">
      <h2>2. 一个直观类比：给实习生布置任务</h2>
      <figure>
        <img src="{FIG_TASK.name}" alt="提示词像给AI的任务委托书">
        <figcaption>好提示词不是“神奇话术”，而是一份清楚的任务委托书：目标、背景、约束和检查标准都要说清楚。</figcaption>
      </figure>
      {p(ANALOGY)}
    </section>

    <section id="mechanism">
      <h2>3. 工作原理：好提示词怎样让 AI 更稳定？</h2>
      <figure>
        <img src="{FIG_FLOW.name}" alt="提示词从模糊问题到高质量输出的迭代流程">
        <figcaption>从模糊问题到可用结果，关键不是一句万能模板，而是持续补足目标、背景、格式和检查标准。</figcaption>
      </figure>
      <div class="steps">{mechanism_cards()}</div>
      <div class="note">判断一条提示词是否合格，可以问：AI 是否知道“给谁看、做什么、用什么资料、按什么格式、怎样算好”？</div>
    </section>

    <section id="terms">
      <h2>4. 关键术语解释</h2>
      <table>
        <thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead>
        <tbody>{term_rows()}</tbody>
      </table>
    </section>

    <section id="case">
      <h2>5. 一个真实应用案例：让 AI 写活动复盘邮件</h2>
      {p(CASE)}
      <div class="note">现实价值：提示词把“我想要一份好结果”的愿望，翻译成 AI 能执行、团队能检查的任务说明。</div>
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
        browser.close()


def build() -> None:
    missing = [path for path in (FIG_TASK, FIG_FLOW) if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing expected figure(s): " + ", ".join(str(p) for p in missing))

    html_path = ROOT / HTML_NAME
    pdf_path = ROOT / PDF_NAME
    html_path.write_text(build_html(), encoding="utf-8")
    render_pdf(html_path, pdf_path)

    (ROOT / "email_subject.txt").write_text(
        "【AI每日深度科普】提示词工程：为什么会提问的人更会用 AI？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        "\n".join(
            [
                "今天的主题是 Prompt Engineering（提示词工程）。",
                "",
                "它是普通人真正用好大模型的入口：不是背咒语，而是把任务、背景、标准和反馈闭环说清楚。",
                "",
                "附件内容将用“给实习生布置任务”的生活化类比解释：",
                "为什么同一个 AI，面对不同提示词会输出完全不同质量的结果。",
                "",
                "适合：非技术读者、AI 初学者、产品经理、运营、知识工作者阅读。",
            ]
        ),
        encoding="utf-8",
    )

    print(pdf_path)
    print(html_path)
    print(FIG_TASK)
    print(FIG_FLOW)


if __name__ == "__main__":
    build()
