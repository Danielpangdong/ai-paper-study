from __future__ import annotations

import html
import textwrap
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
DATE = "2026-07-11"
CONCEPT = "Logprobs（对数概率）"
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
        大模型并不是先想好整篇答案，再把它打印出来。它是在每一个位置都问一次：“在已经出现这些字之后，下一小块文字最可能是什么？”这个小块叫 token，可能是一个字、一个词，或一个词的一部分。

        每一步，模型都会给候选 token 一张概率表。可是一句话往往有几十步：如果直接把每一步的概率连乘，数字会迅速小到几乎看不见，也很难比较两句不同答案。Logprobs（对数概率）把每一步的概率换成一种可以相加的记账分数：概率越高，分数越接近 0；概率越低，分数越负。

        这不是一个只属于工程师的“后台数字”。它让开发者看见模型在何处犹豫、比较多个候选答案、给低把握的分类交给人工复核，也可以给 RAG 问答增加“检索材料是否足够”的一道闸门。理解 Logprobs，才能正确理解 AI 的“把握”是什么，又不是什么。
        """,
    ),
    (
        "analogy",
        "一个直观类比：把路线选择记成“可累加的里程”",
        """
        想象你和朋友要从学校走到图书馆。每个路口都有几条路：一条是大家最常走的主路，另一条是绕一点的小路，还有一条会通向施工围挡。你每经过一个路口，都会给选中的路记一笔“顺路程度”。

        如果把每一步的“走对概率”直接相乘，走十个路口后会得到一个很小的小数；既难读，也不方便比较两条路线。于是你们改用一种记账法：把每一步概率取自然对数。原来需要相乘的概率，变成了可以相加的分数；整条路线的总分就是每个路口分数的和。

        Logprobs 就是这本“路线账”。它不说“这条路在现实中一定安全”，只说“在模型已经看到的上下文里，这一步有多符合它学到的语言模式”。总分更接近 0 的句子，表示模型把它看作相对更顺、更像会接着出现的文字。
        """,
    ),
    (
        "principle",
        "工作原理：从下一词概率到整句分数",
        """
        第一步：模型读上下文。比如看到“今天北京的天气很”，它会为下一 token 准备候选：好、热、冷、糟等。这里的概率永远是“在已经出现的文字条件下”的概率，不是脱离语境的词典频率。

        第二步：模型把原始偏好换成概率。上一讲的 Logits 是原始打分，Softmax 把它们换成总和为 1 的概率分布。假设“好”的概率是 0.60，那么它的 logprob 是 log(0.60)≈−0.51；“冷”的概率若为 0.15，logprob 约为 −1.90。两者都为负，是正常的：0 到 1 之间的概率取自然对数，本来就不大于 0。

        第三步：模型选择一个 token，并记录这一笔 logprob。新 token 被接到句子末尾后，模型重新看新的上下文，再为下一步计算新的概率和 logprob。它不会只在第一步算一次。

        第四步：把每一步的 logprob 相加，得到整段文字的序列分数。概率相乘会变成对数相加，这是 Logprobs 最实用的原因。比较不同长度的答案时，通常还要看平均每 token 的 logprob，或使用专门的长度处理；不能只盯着总分。

        第五步：有些 API 会返回 top_logprobs，也就是每一步最靠前的若干候选与它们的 logprob。它像让你看到模型当时还认真考虑过哪些“岔路”。但可返回的数量、模型和端点各不相同，产品实现时必须查当前文档。
        """,
    ),
    ("terms", "关键术语解释", ""),
    (
        "case",
        "一个真实应用案例：给企业知识库问答加一道“先别硬答”的闸门",
        """
        假设一家公司的 AI 客服使用 RAG：先从制度库检索几段材料，再回答“报销凭证要保存多久？”最危险的情况不是它回答“不知道”，而是材料里没有答案，它却写出一个听起来很像真的年限。

        产品团队可以要求模型在正式回答前，只输出 True 或 False： “给出的材料是否足够支持回答？”然后读取这一个分类 token 的 logprob，以及最可能的替代选项。如果模型对 True 的相对把握不够高，就不让它自由作答，而是提示“资料不足，请转人工或补充检索”。

        OpenAI 的官方示例展示了这种“检索上下文是否足够”的自评估思路；同一类信号也可用于文章标签、自动补全和候选答案排序。真正可靠的系统不会把 Logprobs 当判决书：它会把阈值放在离线评测、人工抽检和可追溯来源之后，用它决定何时放行、何时复核。
        """,
    ),
    (
        "misconceptions",
        "常见误区",
        """
        误区一：logprob 高，就是事实是真的。不对。它描述模型在当前上下文下对下一个 token 的生成倾向，不是对外部世界真假的证明。

        误区二：−0.2 比 −2.0 更差。不对。在同一套条件下，−0.2 更接近 0，代表概率更高；0 对应 100% 概率。

        误区三：把一整句的 logprob 相加，就能公平比较任何句子。不完整。长句有更多项相加，往往自然得到更低的总分；比较不同长度候选时，要看平均分或采用长度校正。

        误区四：只要设置一个阈值，就能消灭幻觉。不对。研究发现模型的概率可能并不校准：它给得很有把握，仍可能错。阈值需要用真实业务数据验证，并和检索、规则、人工复核配合。

        误区五：所有模型和 API 都能返回同样的 Logprobs。不对。是否支持、返回哪种 token 信息、top 候选数上限，都取决于具体模型与接口版本。
        """,
    ),
    ("summary", "总结：3句话讲清核心认知", ""),
    ("questions", "复习问题", ""),
]


TERMS = [
    ("Token", "模型处理和生成文本的基本小单位，可以是字、词或词的一部分。", "AI 不是一整句一整句写，而是一小块一小块接着写。"),
    ("条件概率", "在既有上下文条件下，下一个 token 出现的概率。", "同一个“好”字，放在不同前半句后，机会完全不同。"),
    ("Logprob", "某个 token 条件概率的自然对数，即 log(p)。", "把“这一步有多像会出现”记成方便加总的分数。"),
    ("Top logprobs", "某个位置若干最可能候选 token 及其对数概率。", "像看到模型在路口还认真比较了哪些岔路。"),
    ("序列分数", "一段输出中各 token logprob 的和。", "把一整句话每一步的记账分加起来。"),
    ("平均 logprob", "序列分数除以 token 数，常用于缓解长度差异。", "比较长短不同句子时，看每一步平均顺不顺。"),
    ("Perplexity / 困惑度", "由平均负 logprob 指数化得到的语言模型不确定性指标。", "模型越拿不准，像面对的可选岔路越多，困惑度通常越高。"),
    ("Logits 与 Softmax", "Logits 是概率化前的原始分；Softmax 将其转换为概率分布。", "先打草稿分，再换成百分比；Logprobs 则记下百分比的对数。"),
    ("校准（Calibration）", "模型的置信度与实际正确率是否匹配的性质。", "说九成把握时，长期看能不能真的九成正确。"),
]


SUMMARY_POINTS = [
    "Logprobs 是每一步生成概率的对数：数值越接近 0，在该上下文下越可能；它让长文本的概率连乘变成分数相加。",
    "它能帮助排序、阈值分流、看候选词和诊断模型犹豫，但它衡量的是生成倾向，不是事实真相。",
    "把它用于真实产品时，应做长度处理、离线校准和人工复核，并与检索证据一起决定是否让答案放行。",
]


QUESTIONS = [
    "为什么整句的概率直接相乘会不方便？Logprobs 怎样把这个问题改写成“可加”的问题？",
    "两个 logprob 分别是 −0.3 和 −2.1。在相同上下文与设置下，哪个 token 更可能出现？为什么？",
    "企业知识库问答中，为什么即使模型对“材料足够”给出很高 logprob，仍应保留来源核验或人工复核？",
]


SOURCES = [
    ("OpenAI Cookbook: Using logprobs", "https://developers.openai.com/cookbook/examples/using_logprobs"),
    ("Hugging Face Transformers: Generation", "https://huggingface.co/docs/transformers/main_classes/text_generation"),
    ("Jurafsky & Martin: Speech and Language Processing", "https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf"),
    ("Lovering et al. (2024): Are Language Model Logits Calibrated?", "https://arxiv.org/abs/2410.16007"),
    ("Kauf et al. (2024): Log Probabilities and Semantic Plausibility", "https://arxiv.org/abs/2403.14859"),
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
              <img src="assets/logprobs_probability_to_sum.png" alt="Logprobs 将候选词概率转换成可相加分数的中文图解">
              <figcaption>图解 1：把每一步的概率取自然对数，原来的“连乘”就变成可加的序列分数。</figcaption>
            </figure>
            """
        elif sid == "principle":
            content = """
            <figure>
              <img src="assets/logprobs_sequence_score.png" alt="从逐词概率到整句 Logprobs 分数的中文流程图">
              <figcaption>图解 2：模型每生成一个 token 都重新估计下一步；逐步 logprob 加总后可比较候选句的相对可能性。</figcaption>
            </figure>
            """ + paragraph_html(body) + """
            <div class="steps">
              <div><b>1. 看上下文</b><span>读取已输入和已生成的 token。</span></div>
              <div><b>2. 得到概率</b><span>Logits 经 Softmax 变成候选 token 的概率。</span></div>
              <div><b>3. 记 Logprob</b><span>选中 token 的概率取 log，记为一笔分数。</span></div>
              <div><b>4. 加总与比较</b><span>叠加各步分数，并对长度差异做处理。</span></div>
            </div>
            <div class="note">读数小窍门：p=1 时 log(p)=0；p 越接近 0，log(p) 越负。因此同一条件下，−0.1 比 −3.0 更可能。</div>
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
            content = '<ul class="mistakes">' + "\n".join(items) + "</ul>"
        elif sid == "summary":
            content = '<div class="summary-grid">' + "\n".join(
                f"<div><b>{i + 1}</b><span>{html.escape(point)}</span></div>" for i, point in enumerate(SUMMARY_POINTS)
            ) + "</div>"
        elif sid == "questions":
            content = '<ol class="questions">' + "\n".join(f"<li>{html.escape(q)}</li>" for q in QUESTIONS) + "</ol>"
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
    :root {{ --navy:#10233f; --ink:#26364a; --muted:#64758c; --line:#dce6f0; --paper:#f5f8fb; --teal:#0d9689; --blue:#2166d9; --amber:#d88319; }}
    * {{ box-sizing:border-box; }} html {{ scroll-behavior:smooth; }}
    body {{ margin:0; color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif; background:#fff; line-height:1.8; }}
    .page {{ width:min(1080px,calc(100% - 44px)); margin:0 auto; }}
    .hero {{ min-height:760px; padding:82px 0 52px; background:radial-gradient(circle at 83% 10%,#ddecff 0,transparent 30%),linear-gradient(180deg,#f7faff 0%,#fff 88%); border-bottom:1px solid var(--line); }}
    .eyebrow {{ display:inline-flex; align-items:center; gap:10px; font-size:14px; color:var(--muted); border:1px solid var(--line); border-radius:999px; padding:8px 14px; background:rgba(255,255,255,.82); }}
    h1 {{ font-size:clamp(48px,7.4vw,90px); line-height:1.05; margin:40px 0 22px; color:var(--navy); letter-spacing:0; }}
    h1 span {{ display:block; color:var(--teal); font-size:.46em; margin-top:17px; }}
    .subtitle {{ font-size:29px; color:#415873; margin:0 0 28px; max-width:930px; }}
    .core {{ display:block; max-width:940px; background:var(--navy); color:#fff; border-radius:10px; padding:24px 28px; font-size:24px; line-height:1.58; box-shadow:0 14px 32px rgba(16,35,63,.13); }}
    .hero-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:42px; }}
    .hero-grid div {{ border:1px solid var(--line); border-radius:10px; padding:18px; background:rgba(255,255,255,.82); min-height:126px; }}
    .hero-grid b {{ display:block; color:var(--navy); margin-bottom:7px; }}
    .toc {{ position:sticky; top:0; z-index:2; background:rgba(255,255,255,.94); backdrop-filter:blur(16px); border-bottom:1px solid var(--line); }}
    .toc .page {{ display:flex; gap:10px; overflow-x:auto; padding:14px 0; }}
    .toc a {{ white-space:nowrap; color:var(--muted); text-decoration:none; border:1px solid var(--line); border-radius:999px; padding:7px 12px; font-size:14px; background:#fff; }}
    section {{ padding:58px 0; border-bottom:1px solid var(--line); }} h2 {{ color:var(--navy); font-size:34px; line-height:1.25; margin:0 0 22px; }} p {{ font-size:19px; margin:0 0 18px; }}
    figure {{ margin:34px 0; }} img {{ display:block; width:100%; border-radius:10px; border:1px solid var(--line); background:#fff; }} figcaption {{ color:var(--muted); font-size:15px; margin-top:10px; }}
    .steps {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:28px; }} .steps div,.summary-grid div {{ border:1px solid var(--line); border-radius:10px; padding:18px; background:#fbfdff; }}
    .steps b {{ display:block; color:var(--teal); margin-bottom:6px; }} .steps span {{ color:var(--muted); font-size:15px; line-height:1.55; }}
    .note {{ margin-top:20px; padding:17px 18px; border-radius:10px; background:#edf8f7; border:1px solid #bfe5df; color:#235e55; font-size:16px; }}
    table {{ width:100%; border-collapse:collapse; overflow:hidden; border:1px solid var(--line); border-radius:10px; font-size:16px; }} th,td {{ text-align:left; vertical-align:top; padding:15px 16px; border-bottom:1px solid var(--line); }} th {{ color:var(--navy); background:#f5f8fb; width:23%; }} thead th {{ background:var(--navy); color:#fff; }}
    .mistakes {{ list-style:none; padding:0; margin:0; display:grid; gap:12px; }} .mistakes li {{ border-left:5px solid var(--amber); background:#fff9ef; border-radius:9px; padding:16px 18px; }} .mistakes strong {{ display:block; color:#6a4210; margin-bottom:4px; }}
    .summary-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; font-size:18px; }} .summary-grid b {{ display:inline-flex; width:32px; height:32px; align-items:center; justify-content:center; border-radius:50%; background:var(--teal); color:#fff; margin-bottom:12px; }} .summary-grid span {{ display:block; }}
    .questions {{ font-size:19px; padding-left:26px; }} .questions li {{ margin-bottom:14px; padding-left:6px; }}
    .sources {{ background:#f6f8fb; padding:48px 0 64px; color:var(--muted); }} .sources h2 {{ font-size:26px; }} .sources a {{ color:var(--blue); }}
    @page {{ size:A4; margin:0; }} @media print {{ body {{ background:#fff; }} .toc {{ position:static; }} section {{ break-inside:avoid; padding:36px 0; }} .hero {{ min-height:680px; }} img {{ max-height:520px; object-fit:contain; }} }}
    @media (max-width:760px) {{ .page {{ width:min(100% - 28px,1080px); }} .hero {{ padding-top:56px; min-height:auto; }} .subtitle {{ font-size:22px; }} .core {{ font-size:19px; }} .hero-grid,.steps,.summary-grid {{ grid-template-columns:1fr; }} h2 {{ font-size:28px; }} p {{ font-size:17px; }} table {{ font-size:14px; }} th,td {{ padding:12px; }} }}
  </style>
</head>
<body>
  <header class="hero"><div class="page">
    <div class="eyebrow">AI 每日深度科普 · {DATE} · 生成式 AI 基础认知</div>
    <h1>Logprobs<span>AI 怎样给每一步“把握”记账？</span></h1>
    <p class="subtitle">从单个 token 到完整句子，读懂模型的“相对可能性”如何被记录、比较和正确使用。</p>
    <div class="core">核心一句话：Logprobs 把每一步的生成概率变成能相加的分数，用来比较候选答案在模型眼中相对“顺不顺”。</div>
    <div class="hero-grid"><div><b>它解决什么</b><span>把一长串小概率的连乘，变成稳定、可比较的加法记账。</span></div><div><b>它连接什么</b><span>承接 Logits、Softmax、Temperature、Top-p 与 Top-k，解释生成链路的“分数记录”。</span></div><div><b>它不是什么</b><span>它不是事实验证器；高把握仍需要外部证据、评测与人工复核。</span></div></div>
  </div></header>
  <nav class="toc"><div class="page">{toc}</div></nav>
  <main class="page">{''.join(section_blocks)}</main>
  <footer class="sources"><div class="page"><h2>参考来源</h2><ul>{source_links}</ul></div></footer>
</body></html>\n"""


def write_text_assets() -> None:
    EMAIL_SUBJECT.write_text("【AI每日深度科普】Logprobs：AI 怎样给每一步“把握”记账？\n", encoding="utf-8")
    EMAIL_BODY.write_text(
        """今天的主题是 Logprobs（对数概率）。

它是理解大模型“把握度”最容易被误解、也最有用的底层概念之一：模型为每个生成 token 记下一笔分数，让整句话能够被排序、比较和分流。

附件将用路线选择和逐词生成的图解，讲清：
为什么概率要取对数、Logprobs 如何帮助 AI 产品知道何时该转人工，以及为什么“高把握”不等于“事实正确”。

适合：
非技术读者、AI初学者、产品经理、业务负责人、投资研究者阅读。\n""",
        encoding="utf-8",
    )
    SOURCES_MD.write_text("# Sources\n\n" + "\n".join(f"- {name}\n  {url}" for name, url in SOURCES) + "\n", encoding="utf-8")


def launch_chromium(playwright):
    candidates = [None, "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium"]
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
            page.pdf(path=str(PDF), format="A4", print_background=True, prefer_css_page_size=True, margin={"top":"0","right":"0","bottom":"0","left":"0"})
            page.screenshot(path=str(PREVIEW), full_page=True)
        finally:
            browser.close()


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name in ["logprobs_probability_to_sum.png", "logprobs_sequence_score.png"]:
        if not (ASSETS / name).exists():
            raise FileNotFoundError(f"Missing generated image asset: {ASSETS / name}")
    HTML.write_text(render_html(), encoding="utf-8")
    write_text_assets()
    build_pdf()
    print(PDF)


if __name__ == "__main__":
    main()
