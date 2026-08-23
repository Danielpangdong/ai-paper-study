from __future__ import annotations

import html
import textwrap
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
DATE = "2026-07-09"
CONCEPT = "Logits与Softmax（模型打分与概率）"
HTML = BASE / f"{DATE}_{CONCEPT}.html"
PDF = BASE / f"{DATE}_{CONCEPT}.pdf"
PREVIEW = BASE / "html_preview.png"
EMAIL_SUBJECT = BASE / "email_subject.txt"
EMAIL_BODY = BASE / "email_body.txt"
SOURCES_MD = BASE / "sources.md"


SECTIONS = [
    (
        "why",
        "为什么这个概念重要？",
        """
        大模型回答问题时，并不是先在脑子里写好整篇文章，再一次性吐出来。它更像一边写一边选：先看已经出现的文字，然后判断“下一个小片段最可能是什么”。这个小片段可以是一个字、一个词，或者一个词的一部分。

        问题是，模型一开始拿到的并不是百分比，而是一堆原始分数。比如它觉得“天气”很合适，给 2.10 分；觉得“很好”也可以，给 0.85 分；觉得“苹果”不太合适，给 -1.20 分。这些原始分数就叫 Logits。

        Softmax 的作用，是把这些草稿分换成一张真正能用来抽样的概率表。理解它，你就能看懂很多 AI 产品背后的旋钮：Temperature 在改分数差距，Top-p 在切概率范围，logit bias 在给某些词加分或扣分。昨天我们讲 Top-p，今天补上它前面的源头：概率到底是从哪里来的。
        """,
    ),
    (
        "analogy",
        "一个直观类比：老师把草稿分换成百分比",
        """
        想象语文老师让全班补完一句话：“今天的____”。同学们交上来很多答案：天气、作业、比赛、苹果。老师先凭直觉给每个答案打草稿分：天气 3 分，很好 2 分，下雨 1 分，苹果 0 分。

        这时还不能直接说“天气有 3% 的概率”。因为 3 分只是一个相对分数，不是百分比。老师还需要把所有分数统一换算：谁更高，谁就占更大的选择份额；但低分答案也不一定完全没有机会。

        Softmax 就像这个换算器。它把“谁更适合”的草稿分，变成“每个答案被选中的概率”。如果最高分只高一点点，概率可能只是略高；如果最高分明显领先，它的概率会被放大很多。
        """,
    ),
    (
        "principle",
        "工作原理：Logits 和 Softmax 怎么配合？",
        """
        第一步，模型读完上下文。比如你输入“今天的___”，模型会在自己的词表里查看许多候选 token：天气、很好、下雨、苹果等等。

        第二步，模型给每个候选 token 打原始分。这个分数就是 Logits。它可以是正数、负数，也不需要加起来等于 1。你可以把它理解为“模型对每个候选词的偏好强度”。

        第三步，Softmax 把这些原始分换成概率。它做两件事：先让高分更突出，再把所有候选的份额统一压到 100%。这样模型才有一张可以抽样的概率表。

        第四步，生成系统根据概率选择下一个 token。如果是保守设置，可能总选最高概率；如果是采样设置，就会按概率抽。选完一个 token 后，模型会把新文字接到上下文后面，再重新打分、重新 Softmax、重新选择下一步。

        所以，AI 不是“整段话一次想完”，而是在一连串极快的选择中，把原始分数不断换成概率，再把概率变成文字。
        """,
    ),
    (
        "terms",
        "关键术语解释",
        "",
    ),
    (
        "case",
        "一个真实应用案例：ChatGPT 为什么能写出不同风格？",
        """
        假设你问 AI：“帮我写一条给客户的道歉短信。”模型生成到“非常抱歉给您带来____”时，下一步可能有很多候选：不便、困扰、麻烦、损失、快乐。

        模型会先给这些候选打 Logits。像“不便”“困扰”这种更符合上下文的词，原始分会更高；像“快乐”这种明显不合适的词，原始分会很低。Softmax 再把这些分数变成概率。

        如果产品希望客服回复稳定、礼貌、少冒险，就会让最高概率词更容易被选中。如果产品在做广告文案或故事创作，就可能允许更宽的概率选择，让一些不那么常规的词也有机会出现。

        这就是为什么同一个模型，在“严肃客服”“创意写作”“代码补全”里会表现出不同风格。不是模型人格突然变了，而是下一个 token 的打分、概率换算和采样规则一起塑造了输出。
        """,
    ),
    (
        "misconceptions",
        "常见误区",
        """
        误区一：Logits 本身就是概率。不对。Logits 是原始分数，可以为负，也不需要加起来等于 100%。

        误区二：Softmax 会让 AI 理解事实。不对。Softmax 只是换算概率，不负责查证事实，也不会凭空增加知识。

        误区三：概率最高的词一定会被选中。不一定。采样模式下，高概率只是更容易被抽到，不代表每次必选。

        误区四：某个词概率 70%，就说明这句话有 70% 真实。不对。这里的概率是“下一个 token 的生成概率”，不是事实可信度。

        误区五：模型先规划好完整答案，再填字。不准确。大多数文本生成是在每一步重新计算候选词分数，逐步写出来的。
        """,
    ),
    (
        "summary",
        "总结：3句话讲清核心认知",
        "",
    ),
    (
        "questions",
        "复习问题",
        "",
    ),
]


TERMS = [
    ("Token", "模型处理文本的基本单位，可以是字、词或词的一部分。", "AI 写作不是一次写整段，而是一个小块一个小块接下去。"),
    ("Vocabulary / 词表", "模型可以选择的全部 token 集合。", "像一大本候选字词菜单，模型每一步都从里面挑。"),
    ("Logits", "模型在 Softmax 之前给每个候选 token 的原始预测分数。", "像老师先打草稿分，还不是百分比。"),
    ("Softmax", "把一组原始分数转换成总和为 1 的概率分布的函数。", "像把草稿分换成一张总和 100% 的抽奖券表。"),
    ("Probability Distribution / 概率分布", "所有候选 token 的概率组合，总和为 100%。", "每个词有多少张抽奖券，合起来刚好是一整盒彩券。"),
    ("Sampling / 抽样", "按照概率从候选 token 中选择输出。", "高概率更容易中，但低概率也可能被抽到。"),
    ("Temperature", "在 Softmax 前调整分数差距的采样参数。", "像把选择变得更保守或更发散的旋钮。"),
    ("Top-p", "在概率出来后，只保留累计概率达到 p 的核心候选池。", "像昨天讲的，只从靠谱候选圈里抽。"),
    ("Logit bias", "在采样前人为提高或降低特定 token 的 logit。", "像给某些词提前加分或扣分，让它更容易或更难出现。"),
]


SUMMARY_POINTS = [
    "Logits 是模型对每个候选 token 的原始草稿分，Softmax 把它们换成可抽样的概率表。",
    "概率最高不等于一定会选中，也不等于事实一定正确；它只表示生成下一步文字的倾向。",
    "理解 Logits 与 Softmax，就能把 Temperature、Top-p、logit bias 这些生成参数串成一条完整链路。",
]


QUESTIONS = [
    "如果“天气”的 logit 比“苹果”高很多，Softmax 后会发生什么？请用老师打分的类比解释。",
    "为什么“某个词生成概率很高”不等于“这句话一定真实”？",
    "昨天讲的 Top-p 是在概率出来后切候选池。今天的 Logits 与 Softmax 位于它前面还是后面？为什么？",
]


SOURCES = [
    ("OpenAI API Reference: Completions - logit_bias, temperature, top_p", "https://developers.openai.com/api/reference/resources/completions/methods/create"),
    ("Hugging Face Transformers: Generation", "https://huggingface.co/docs/transformers/en/main_classes/text_generation"),
    ("Hugging Face Transformers: Generation utilities and LogitsProcessor", "https://huggingface.co/docs/transformers/en/internal/generation_utils"),
    ("Hugging Face Transformers: Generation strategies", "https://huggingface.co/docs/transformers/en/generation_strategies"),
    ("The Annotated Transformer: softmax in attention", "https://rush-nlp.com/2018/04/01/attention.html"),
]


def paragraph_html(text: str) -> str:
    parts = [p.strip() for p in textwrap.dedent(text).strip().split("\n\n") if p.strip()]
    return "\n".join(f"<p>{html.escape(part)}</p>" for part in parts)


def render_html() -> str:
    toc = "\n".join(f'<a href="#{sid}">{i + 1}. {html.escape(title)}</a>' for i, (sid, title, _) in enumerate(SECTIONS))
    section_blocks: list[str] = []

    for sid, title, body in SECTIONS:
        if sid == "analogy":
            content = paragraph_html(body) + """
            <figure>
              <img src="assets/logits_to_softmax.png" alt="Logits 到 Softmax 的中文流程图">
              <figcaption>图解：模型先给候选词打原始分，再由 Softmax 换算为总和 100% 的概率。</figcaption>
            </figure>
            """
        elif sid == "principle":
            content = """
            <figure>
              <img src="assets/softmax_score_to_probability.png" alt="Softmax 把相对分数变成概率倾向的图解">
              <figcaption>图解：Softmax 会让高分更突出，但低分候选仍可能保留一点机会。</figcaption>
            </figure>
            """ + paragraph_html(body) + """
            <div class="steps">
              <div><b>1. 看上下文</b><span>读到目前已经生成或输入的文字。</span></div>
              <div><b>2. 打草稿分</b><span>给词表里的候选 token 打 Logits。</span></div>
              <div><b>3. 换成概率</b><span>Softmax 把分数换成总和 100% 的概率。</span></div>
              <div><b>4. 选择输出</b><span>按规则选下一个 token，然后重复。</span></div>
            </div>
            <div class="note">小提醒：这里的 Softmax 也出现在注意力机制里，用来把“关注分数”换成“关注权重”。今天我们重点讲它在文本生成下一 token 时的作用。</div>
            """
        elif sid == "terms":
            rows = "\n".join(
                f"<tr><th>{html.escape(term)}</th><td>{html.escape(pro)}</td><td>{html.escape(plain)}</td></tr>"
                for term, pro, plain in TERMS
            )
            content = f"""
            <table>
              <thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
            """
        elif sid == "misconceptions":
            items = []
            for line in [p.strip() for p in textwrap.dedent(body).strip().split("\n\n") if p.strip()]:
                head, rest = line.split("。", 1)
                items.append(f"<li><strong>{html.escape(head)}。</strong><span>{html.escape(rest.strip())}</span></li>")
            content = "<ul class=\"mistakes\">" + "\n".join(items) + "</ul>"
        elif sid == "summary":
            content = "<div class=\"summary-grid\">" + "\n".join(
                f"<div><b>{i + 1}</b><span>{html.escape(point)}</span></div>" for i, point in enumerate(SUMMARY_POINTS)
            ) + "</div>"
        elif sid == "questions":
            content = "<ol class=\"questions\">" + "\n".join(f"<li>{html.escape(q)}</li>" for q in QUESTIONS) + "</ol>"
        else:
            content = paragraph_html(body)
        section_blocks.append(f'<section id="{sid}"><h2>{html.escape(title)}</h2>{content}</section>')

    source_links = "\n".join(f'<li><a href="{url}">{html.escape(name)}</a></li>' for name, url in SOURCES)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{DATE}_{CONCEPT}</title>
  <style>
    :root {{
      --navy: #132238;
      --ink: #273246;
      --muted: #647389;
      --line: #dce5ee;
      --paper: #f5f8fb;
      --teal: #149e8c;
      --blue: #2d6cdf;
      --amber: #d98924;
      --green: #2d9d68;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: #ffffff;
      line-height: 1.78;
      letter-spacing: 0;
    }}
    .page {{
      width: min(1080px, calc(100% - 44px));
      margin: 0 auto;
    }}
    .hero {{
      min-height: 760px;
      padding: 82px 0 50px;
      background: linear-gradient(180deg, #f7fafc 0%, #ffffff 88%);
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      display: inline-flex;
      gap: 10px;
      align-items: center;
      font-size: 14px;
      color: var(--muted);
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 8px 14px;
      background: rgba(255,255,255,.82);
    }}
    h1 {{
      font-size: clamp(48px, 7.4vw, 90px);
      line-height: 1.05;
      margin: 40px 0 22px;
      color: var(--navy);
      letter-spacing: 0;
    }}
    h1 span {{
      display: block;
      color: var(--teal);
      font-size: .46em;
      margin-top: 17px;
    }}
    .subtitle {{
      font-size: 29px;
      color: #41536b;
      margin: 0 0 28px;
      max-width: 930px;
    }}
    .core {{
      display: block;
      max-width: 940px;
      background: var(--navy);
      color: #ffffff;
      border-radius: 8px;
      padding: 24px 28px;
      font-size: 24px;
      line-height: 1.58;
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 14px;
      margin-top: 42px;
    }}
    .hero-grid div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px 18px 16px;
      background: rgba(255,255,255,.78);
      min-height: 126px;
    }}
    .hero-grid b {{
      display: block;
      color: var(--navy);
      margin-bottom: 7px;
    }}
    .toc {{
      position: sticky;
      top: 0;
      z-index: 2;
      background: rgba(255,255,255,.94);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--line);
    }}
    .toc .page {{
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding: 14px 0;
    }}
    .toc a {{
      white-space: nowrap;
      color: var(--muted);
      text-decoration: none;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 7px 12px;
      font-size: 14px;
      background: #ffffff;
    }}
    section {{
      padding: 58px 0;
      border-bottom: 1px solid var(--line);
    }}
    h2 {{
      color: var(--navy);
      font-size: 34px;
      line-height: 1.25;
      margin: 0 0 22px;
      letter-spacing: 0;
    }}
    p {{
      font-size: 19px;
      margin: 0 0 18px;
    }}
    figure {{
      margin: 34px 0;
      padding: 0;
    }}
    img {{
      display: block;
      width: 100%;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: #fff;
    }}
    figcaption {{
      color: var(--muted);
      font-size: 15px;
      margin-top: 10px;
    }}
    .steps {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-top: 28px;
    }}
    .steps div, .summary-grid div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      background: #fbfdff;
    }}
    .steps b {{
      display: block;
      color: var(--teal);
      margin-bottom: 6px;
    }}
    .steps span {{
      color: var(--muted);
      font-size: 15px;
      line-height: 1.55;
    }}
    .note {{
      margin-top: 20px;
      padding: 17px 18px;
      border-radius: 8px;
      background: #f2fbf9;
      border: 1px solid #c9e8e1;
      color: #245f56;
      font-size: 16px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 8px;
      font-size: 16px;
    }}
    th, td {{
      text-align: left;
      vertical-align: top;
      padding: 15px 16px;
      border-bottom: 1px solid var(--line);
    }}
    th {{
      color: var(--navy);
      background: #f5f8fb;
      width: 23%;
    }}
    thead th {{
      background: var(--navy);
      color: #ffffff;
    }}
    .mistakes {{
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      gap: 12px;
    }}
    .mistakes li {{
      border-left: 5px solid var(--amber);
      background: #fff9ef;
      border-radius: 8px;
      padding: 16px 18px;
    }}
    .mistakes strong {{
      display: block;
      color: #6b4311;
      margin-bottom: 4px;
    }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      font-size: 18px;
    }}
    .summary-grid b {{
      display: inline-flex;
      width: 32px;
      height: 32px;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      background: var(--teal);
      color: #fff;
      margin-bottom: 12px;
    }}
    .summary-grid span {{
      display: block;
    }}
    .questions {{
      font-size: 19px;
      padding-left: 26px;
    }}
    .questions li {{
      margin-bottom: 14px;
      padding-left: 6px;
    }}
    .sources {{
      background: #f6f8fb;
      padding: 48px 0 64px;
      color: var(--muted);
    }}
    .sources h2 {{
      font-size: 26px;
    }}
    .sources a {{
      color: var(--blue);
    }}
    @page {{
      size: A4;
      margin: 0;
    }}
    @media print {{
      body {{ background: #fff; }}
      .toc {{ position: static; }}
      section {{ break-inside: avoid; padding: 36px 0; }}
      .hero {{ min-height: 680px; }}
      img {{ max-height: 520px; object-fit: contain; }}
    }}
    @media (max-width: 760px) {{
      .page {{ width: min(100% - 28px, 1080px); }}
      .hero {{ padding-top: 56px; min-height: auto; }}
      .subtitle {{ font-size: 22px; }}
      .core {{ font-size: 19px; }}
      .hero-grid, .steps, .summary-grid {{ grid-template-columns: 1fr; }}
      h2 {{ font-size: 28px; }}
      p {{ font-size: 17px; }}
      table {{ font-size: 14px; }}
      th, td {{ padding: 12px; }}
    }}
  </style>
</head>
<body>
  <header class="hero">
    <div class="page">
      <div class="eyebrow">AI 每日深度科普 · {DATE} · 生成式 AI 基础认知</div>
      <h1>Logits 与 Softmax<span>AI 如何把“感觉”变成概率？</span></h1>
      <p class="subtitle">从“草稿分”理解大模型每一步如何选下一个词。</p>
      <div class="core">核心一句话：Logits 是模型给候选词的原始草稿分，Softmax 是把草稿分换成可抽样概率表的换算器。</div>
      <div class="hero-grid">
        <div><b>它解决什么</b><span>把一堆不能直接比较的原始分，变成总和 100% 的选择概率。</span></div>
        <div><b>它连接什么</b><span>连接昨天的 Top-p、前天的 Temperature，以及模型每一步生成。</span></div>
        <div><b>它不是什么</b><span>不是事实检查器，也不是让模型突然“更懂”的魔法。</span></div>
      </div>
    </div>
  </header>
  <nav class="toc"><div class="page">{toc}</div></nav>
  <main class="page">
    {''.join(section_blocks)}
  </main>
  <footer class="sources">
    <div class="page">
      <h2>参考来源</h2>
      <ul>{source_links}</ul>
    </div>
  </footer>
</body>
</html>
"""


def write_text_assets() -> None:
    EMAIL_SUBJECT.write_text(
        "【AI每日深度科普】Logits 与 Softmax：AI 如何把“感觉”变成概率？\n",
        encoding="utf-8",
    )
    EMAIL_BODY.write_text(
        """今天的主题是 Logits 与 Softmax。

这是理解大模型“为什么会这样回答”的基础概念：模型先给候选词打原始分，再把这些分数换成可以抽样的概率。

附件内容将用“老师打草稿分”和“概率换算器”的类比，讲清楚：
Logits、Softmax、Temperature、Top-p 之间到底是什么关系。

适合：
非技术读者、AI初学者、产品经理、业务负责人、投资研究者阅读。
""",
        encoding="utf-8",
    )
    SOURCES_MD.write_text(
        "# Sources\n\n" + "\n".join(f"- {name}\n  {url}" for name, url in SOURCES) + "\n",
        encoding="utf-8",
    )


def launch_chromium(playwright):
    candidates = [
        None,
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    last_error: Exception | None = None
    for executable_path in candidates:
        try:
            kwargs = {"headless": True}
            if executable_path and Path(executable_path).exists():
                kwargs["executable_path"] = executable_path
            elif executable_path:
                continue
            return playwright.chromium.launch(**kwargs)
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not launch Chromium/Chrome: {last_error}")


def build_pdf() -> None:
    with sync_playwright() as p:
        browser = launch_chromium(p)
        try:
            page = browser.new_page(viewport={"width": 1240, "height": 1754}, device_scale_factor=1)
            page.goto(HTML.as_uri(), wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(PDF),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            page.screenshot(path=str(PREVIEW), full_page=True)
        finally:
            browser.close()


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name in ["logits_to_softmax.png", "softmax_score_to_probability.png"]:
        path = ASSETS / name
        if not path.exists():
            raise FileNotFoundError(f"Missing generated image asset: {path}")
    HTML.write_text(render_html(), encoding="utf-8")
    write_text_assets()
    build_pdf()
    print(PDF)


if __name__ == "__main__":
    main()
