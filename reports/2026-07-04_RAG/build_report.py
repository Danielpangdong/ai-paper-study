from __future__ import annotations

from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
HTML = BASE / "2026-07-04_RAG（检索增强生成）.html"
PDF = BASE / "2026-07-04_RAG（检索增强生成）.pdf"
PREVIEW = BASE / "html_preview.png"
EMAIL_SUBJECT = BASE / "email_subject.txt"
EMAIL_BODY = BASE / "email_body.txt"
SOURCES = BASE / "sources.md"

FONT_REGULAR = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def wrap_zh(text: str, width: int) -> list[str]:
    lines: list[str] = []
    for piece in text.split("\n"):
        if not piece:
            lines.append("")
            continue
        current = ""
        for char in piece:
            current += char
            if len(current) >= width:
                lines.append(current)
                current = ""
        if current:
            lines.append(current)
    return lines


def rounded_label(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str = "",
    *,
    fill: tuple[int, int, int, int] = (255, 255, 255, 238),
    outline: tuple[int, int, int, int] = (15, 118, 110, 175),
    title_color: tuple[int, int, int] = (15, 23, 42),
    body_color: tuple[int, int, int] = (71, 85, 105),
    radius: int = 16,
    title_size: int = 25,
    body_size: int = 19,
    wrap: int = 13,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=3)
    draw.text((x1 + 18, y1 + 12), title, fill=title_color, font=font(title_size, True))
    y = y1 + 48
    for line in wrap_zh(body, wrap)[:4]:
        draw.text((x1 + 18, y), line, fill=body_color, font=font(body_size))
        y += body_size + 7


def annotate_exam() -> None:
    img = Image.open(ASSETS / "rag_exam_base.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.rounded_rectangle((34, 26, 1638, 108), radius=22, fill=(255, 255, 255, 236), outline=(37, 99, 235, 120), width=2)
    draw.text((74, 45), "RAG：让大模型像“开卷考试”一样先查资料再回答", fill=(13, 31, 45), font=font(38, True))
    draw.text((74, 92), "核心直觉：模型不是凭空背答案，而是先把相关资料摆到桌上，再组织成回答。", fill=(71, 85, 105), font=font(22))

    top_labels = [
        ((60, 134, 392, 204), "1 用户提问", "问题先被写成一张“考题卡”。"),
        ((505, 134, 842, 204), "2 检索资料", "像老师翻教材，找最相关页。"),
        ((945, 134, 1272, 204), "3 取出证据", "只把相关片段交给模型。"),
        ((1372, 134, 1628, 204), "4 生成答案", "引用资料，用人话讲清楚。"),
    ]
    for box, title, body in top_labels:
        rounded_label(draw, box, title, body, title_size=23, body_size=17, wrap=12)

    bottom_labels = [
        ((58, 756, 378, 868), "普通聊天", "只靠模型记忆，遇到私有资料或新信息容易答空。"),
        ((452, 756, 860, 868), "RAG 像开卷考试", "允许翻指定资料，但仍要会理解问题、组织答案。"),
        ((928, 756, 1258, 868), "资料越准越好", "检索错了，后面的回答很难正确。"),
        ((1320, 756, 1620, 868), "答案要可追溯", "最好给出处、时间、权限范围。"),
    ]
    colors = [(37, 99, 235, 160), (15, 118, 110, 170), (217, 119, 6, 170), (22, 163, 74, 160)]
    for (box, title, body), color in zip(bottom_labels, colors):
        rounded_label(draw, box, title, body, outline=color, title_size=24, body_size=18, wrap=14)

    rounded_label(
        draw,
        (710, 356, 1038, 470),
        "最关键的动作",
        "把“可能有用的资料”放进上下文窗口，模型才能基于资料回答。",
        fill=(247, 253, 252, 240),
        outline=(15, 118, 110, 190),
        title_size=27,
        body_size=20,
        wrap=15,
    )
    rounded_label(
        draw,
        (1184, 416, 1538, 526),
        "不是自动正确",
        "RAG 降低幻觉风险，但不替代核对、权限和评估。",
        fill=(255, 255, 255, 240),
        outline=(217, 119, 6, 185),
        title_size=26,
        body_size=20,
        wrap=15,
    )

    out = ASSETS / "rag_open_book_labeled.png"
    Image.alpha_composite(img, overlay).convert("RGB").save(out, quality=94)


def annotate_pipeline() -> None:
    img = Image.open(ASSETS / "rag_pipeline_base.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.rounded_rectangle((38, 34, 1630, 126), radius=20, fill=(255, 255, 255, 238), outline=(37, 99, 235, 120), width=2)
    draw.text((76, 54), "RAG 工程流程：资料入库 → 找回证据 → 生成回答", fill=(13, 31, 45), font=font(38, True))
    draw.text((76, 100), "真正的难点不只在大模型，而在资料质量、检索排序、权限控制和答案核验。", fill=(71, 85, 105), font=font(22))

    stage_boxes = [
        ((50, 766, 260, 866), "资料源", "文档、网页、手册、问答。"),
        ((300, 766, 520, 866), "切块", "长文档拆成可检索小片段。"),
        ((548, 766, 770, 866), "向量化", "每个片段变成意义坐标。"),
        ((788, 760, 1080, 878), "索引/权限", "存入向量库，也要记录来源、时间和访问权限。"),
        ((1120, 766, 1340, 866), "召回排序", "找出最相关的几段证据。"),
        ((1378, 766, 1624, 866), "回答生成", "把证据塞进上下文，再让模型组织语言。"),
    ]
    outlines = [
        (37, 99, 235, 165),
        (22, 163, 74, 165),
        (14, 165, 233, 165),
        (15, 118, 110, 180),
        (217, 119, 6, 180),
        (37, 99, 235, 165),
    ]
    for (box, title, body), outline in zip(stage_boxes, outlines):
        rounded_label(draw, box, title, body, outline=outline, title_size=23, body_size=17, wrap=11)

    small_labels = [
        ((48, 210, 240, 252), "1 原始知识"),
        ((320, 210, 500, 252), "2 文档切片"),
        ((568, 210, 742, 252), "3 语义坐标"),
        ((824, 210, 1030, 252), "4 向量数据库"),
        ((1142, 210, 1298, 252), "5 相关证据"),
        ((1392, 210, 1608, 252), "6 带依据回答"),
    ]
    for box, text in small_labels:
        rounded_label(draw, box, text, "", fill=(255, 255, 255, 230), outline=(100, 116, 139, 120), title_size=20, radius=14)

    rounded_label(
        draw,
        (782, 620, 1048, 714),
        "生产系统要多一道门",
        "谁能看？资料新不新？来源可不可信？",
        outline=(15, 118, 110, 190),
        title_size=22,
        body_size=17,
        wrap=12,
    )
    rounded_label(
        draw,
        (1108, 565, 1360, 660),
        "召回不是越多越好",
        "塞太多无关资料，会挤占上下文，也会干扰模型。",
        outline=(217, 119, 6, 180),
        title_size=22,
        body_size=17,
        wrap=12,
    )

    out = ASSETS / "rag_pipeline_labeled.png"
    Image.alpha_composite(img, overlay).convert("RGB").save(out, quality=94)


SECTIONS = [
    {
        "id": "why",
        "title": "为什么这个概念重要？",
        "body": """
<p>大模型很会组织语言，但它有一个天然限制：它并不会自动知道你公司的内部制度、今天刚更新的政策、某个客户的最新订单状态，也不一定能准确记住训练资料里的每个细节。</p>
<p>RAG 解决的就是这个问题：在回答之前，先从外部资料库里找出相关内容，再把这些内容交给大模型，让它基于资料回答。它像给模型配了一个“可查资料的书包”。</p>
<div class="insight"><b>行业为什么离不开它：</b>企业知识库、AI搜索、客服助手、投研问答、法律/医疗辅助、内部办公 Copilot，都需要模型回答“我自己的资料”和“最新资料”，这正是 RAG 的核心场景。</div>
<p>它改变了 AI 产品的边界。没有 RAG，很多应用只能像一个会聊天的百科全书；有了 RAG，模型才更像一个能读公司资料、查证据、给出处的工作助手。</p>
""",
    },
    {
        "id": "analogy",
        "title": "一个直观类比：开卷考试",
        "body": """
<p>想象你参加一场考试。闭卷考试时，你只能靠记忆答题；如果题目问到一本新教材里的内容，你很可能答错或编一段看起来很像答案的话。</p>
<p>RAG 更像开卷考试。老师允许你带教材，但有两个条件：第一，你要先翻到正确页；第二，你要读懂材料，而不是把整本书全抄上去。RAG 里的“检索”负责翻到相关页，“生成”负责把材料整理成自然语言答案。</p>
<p>所以，RAG 的关键不是让模型“变得全知”，而是让它在回答前先看到可信资料。资料找对了，答案才有基础；资料找错了，模型再会说话也可能把错资料讲得很流畅。</p>
""",
        "image": "assets/rag_open_book_labeled.png",
        "caption": "图解 1：RAG 像开卷考试。先找资料，再基于资料回答，而不是只靠模型记忆。",
    },
    {
        "id": "how",
        "title": "工作原理（深入浅出）",
        "body": """
<div class="steps">
  <div><span>1</span><b>资料入库</b><p>把文档、网页、手册、FAQ 放进系统。长文档通常先切成小块，方便精确检索。</p></div>
  <div><span>2</span><b>变成可搜索的索引</b><p>每个资料块可以做关键词索引，也可以用 Embedding 变成向量，存入向量数据库。</p></div>
  <div><span>3</span><b>用户提问时先检索</b><p>系统把问题也变成查询，找出最相关的几段资料，而不是把所有资料都塞给模型。</p></div>
  <div><span>4</span><b>把证据交给模型</b><p>相关资料被放进上下文窗口，模型根据这些证据组织答案，最好同时给出处。</p></div>
</div>
<p>这里有一个常见误会：RAG 并不等于“让模型联网”。RAG 可以用公开网页，也可以只用企业内部文档；它的本质是“先检索，再生成”。检索的数据从哪里来，是另一个工程选择。</p>
<p>真正的生产系统还要处理更多细节：资料是不是最新？用户有没有权限看？相似度最高的结果是否真的有用？答案有没有引用错误？这些问题决定了一个 RAG 系统是“演示好看”，还是“工作中可靠”。</p>
""",
        "image": "assets/rag_pipeline_labeled.png",
        "caption": "图解 2：RAG 的工程流程。资料先入库并建立索引，提问时召回证据，再交给大模型生成回答。",
    },
    {
        "id": "terms",
        "title": "关键术语解释",
        "body": """
<table>
  <thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead>
  <tbody>
    <tr><td>RAG</td><td>Retrieval-Augmented Generation，检索增强生成。</td><td>先查资料，再让 AI 写答案。</td></tr>
    <tr><td>Retrieval</td><td>从知识库、搜索索引或数据库中召回相关内容。</td><td>像在教材里翻到可能有答案的页。</td></tr>
    <tr><td>Generation</td><td>大模型根据问题和检索内容生成自然语言回复。</td><td>把资料读懂后，用人话讲出来。</td></tr>
    <tr><td>Chunk</td><td>把长文档切成较小、可单独检索的片段。</td><td>把一本书拆成一张张知识卡片。</td></tr>
    <tr><td>Embedding</td><td>把文本等内容转换成向量表示，用于语义相似度检索。</td><td>给每段资料做“意思坐标”。</td></tr>
    <tr><td>Vector Database</td><td>专门存储和快速检索向量的数据库。</td><td>按“意思相近”找资料的图书馆。</td></tr>
    <tr><td>Context Window</td><td>模型一次能看到的输入范围。</td><td>模型桌面上能摊开的资料面积有限。</td></tr>
    <tr><td>Grounding</td><td>让模型输出基于外部事实来源，而不只依赖参数记忆。</td><td>把答案“钉”在资料上，减少乱编。</td></tr>
  </tbody>
</table>
""",
    },
    {
        "id": "case",
        "title": "一个真实应用案例",
        "body": """
<p>假设一个企业客服助手要回答：“我的订单显示到达中转场后两天没有变化，下一步怎么办？”</p>
<p>如果只靠大模型记忆，它可能给出一段泛泛的安慰话。但 RAG 系统会先去知识库里找：中转异常处理规则、延误判定标准、客户告知话术、人工工单触发条件。它可能找到几段真正相关的内部资料，再把它们交给模型。</p>
<p>然后模型生成回答：先说明可能原因，再告诉用户可以等待多久、如何查询、什么情况需要转人工。更好的系统还会显示引用来源，比如“依据：中转异常处理规范，第 3.2 条，更新时间 2026-06-15”。</p>
<div class="insight"><b>一句话看懂价值：</b>RAG 让 AI 客服不只是“会说话”，而是能围绕企业自己的资料回答，且有机会把答案追溯到来源。</div>
""",
    },
    {
        "id": "myths",
        "title": "常见误区（非常重要）",
        "body": """
<div class="myths">
  <div><b>误区一：RAG 就是联网搜索。</b><p>不是。联网搜索只是资料来源之一。RAG 也可以完全基于企业内部文档、数据库或离线知识库。</p></div>
  <div><b>误区二：用了 RAG 就不会幻觉。</b><p>不是。RAG 能降低模型凭空编造的概率，但如果检索错、资料旧、提示写得差，模型仍然可能误读或编造。</p></div>
  <div><b>误区三：把所有资料都塞给模型最好。</b><p>不是。上下文窗口有限，塞太多无关内容会挤掉重点，也会让模型被噪音干扰。</p></div>
  <div><b>误区四：向量相似度最高就是正确答案。</b><p>不一定。语义相近只代表“可能相关”，还要看来源、时间、权限、上下文和业务规则。</p></div>
  <div><b>误区五：RAG 可以替代数据库查询。</b><p>不能简单替代。订单号、余额、库存这类精确数据，通常需要结构化数据库或工具调用，而不是只靠相似度搜索。</p></div>
  <div><b>误区六：RAG 是一次性工程。</b><p>不是。好系统要持续评估召回率、答案准确率、引用质量、资料更新和用户反馈。</p></div>
</div>
""",
    },
    {
        "id": "summary",
        "title": "总结（3句话）",
        "body": """
<ol class="summary">
  <li>RAG 的本质，是让大模型在回答前先检索外部资料，再基于资料生成答案。</li>
  <li>它把 Embedding、向量数据库、搜索索引和大模型连接起来，是企业 AI 应用落地的关键桥梁。</li>
  <li>RAG 能减少“凭空编”，但不能自动保证正确；资料质量、检索质量、权限控制和答案核验同样重要。</li>
</ol>
""",
    },
    {
        "id": "quiz",
        "title": "复习问题（必须）",
        "body": """
<div class="quiz">
  <p><b>1.</b> 为什么说 RAG 像“开卷考试”，而不是让模型“突然变聪明”？</p>
  <p><b>2.</b> 如果一个 RAG 系统总是召回不相关资料，最终答案会出现什么问题？你会优先检查哪几个环节？</p>
  <p><b>3.</b> 为什么订单号、库存数量、账户余额这类精确问题，通常不能只靠向量检索来回答？</p>
</div>
""",
    },
]


SOURCES_LIST = [
    ("Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "https://arxiv.org/abs/2005.11401"),
    ("OpenAI Cookbook: Question answering using embeddings-based search", "https://developers.openai.com/cookbook/examples/question_answering_using_embeddings"),
    ("OpenAI Cookbook: Retrieval augmented generation using Elasticsearch and OpenAI", "https://developers.openai.com/cookbook/examples/vector_databases/elasticsearch/elasticsearch-retrieval-augmented-generation"),
    ("Microsoft Learn: RAG and Generative AI - Azure AI Search", "https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview"),
    ("Microsoft Learn: Retrieval augmented generation and indexes", "https://learn.microsoft.com/en-us/azure/foundry/concepts/retrieval-augmented-generation"),
    ("Google Cloud: What is Retrieval-Augmented Generation?", "https://cloud.google.com/use-cases/retrieval-augmented-generation"),
]


def render_toc() -> str:
    return "\n".join(
        f'<a href="#{section["id"]}"><span>{idx:02d}</span>{escape(section["title"])}</a>'
        for idx, section in enumerate(SECTIONS, 1)
    )


def render_sections() -> str:
    chunks = []
    for idx, section in enumerate(SECTIONS, 1):
        image = ""
        if "image" in section:
            image = f"""
<figure>
  <img src="{escape(section["image"])}" alt="{escape(section["caption"])}">
  <figcaption>{escape(section["caption"])}</figcaption>
</figure>
"""
        chunks.append(
            f"""
<section id="{section["id"]}">
  <div class="section-head">
    <div class="section-kicker">Part {idx:02d}</div>
    <h2>{escape(section["title"])}</h2>
  </div>
  {section["body"]}
  {image}
</section>
"""
        )
    return "\n".join(chunks)


def render_sources() -> str:
    return "\n".join(
        f'<li><a href="{escape(url)}">{escape(label)}</a></li>' for label, url in SOURCES_LIST
    )


def write_html() -> None:
    css = """
:root {
  --ink: #111827;
  --muted: #64748b;
  --line: #dbe3ec;
  --paper: #fbfcfd;
  --teal: #0f766e;
  --blue: #2563eb;
  --amber: #d97706;
  --green: #15803d;
  --coral: #e4572e;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: #edf2f7;
  color: var(--ink);
  font-family: "STHeiti", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  line-height: 1.72;
  letter-spacing: 0;
}
a { color: var(--blue); text-decoration: none; }
.page {
  width: min(1060px, 100%);
  margin: 0 auto;
  background: var(--paper);
  box-shadow: 0 28px 80px rgba(15, 23, 42, .12);
}
.hero {
  min-height: 880px;
  padding: 74px 78px 54px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(115deg, rgba(15, 118, 110, .12), transparent 34%),
    linear-gradient(35deg, rgba(217, 119, 6, .16), transparent 42%),
    #fbfcfd;
}
.hero:after {
  content: "";
  position: absolute;
  inset: auto -110px -210px auto;
  width: 560px;
  height: 560px;
  border: 1px solid rgba(15, 118, 110, .24);
  border-radius: 50%;
}
.meta {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  color: var(--muted);
  font-size: 15px;
  text-transform: uppercase;
}
.meta span {
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 4px 12px;
  background: rgba(255, 255, 255, .62);
}
h1 {
  margin: 88px 0 18px;
  font-size: 72px;
  line-height: 1.04;
  letter-spacing: 0;
}
.subtitle {
  max-width: 760px;
  margin: 0;
  color: #334155;
  font-size: 28px;
  line-height: 1.38;
}
.one-line {
  width: min(800px, 100%);
  margin-top: 52px;
  padding: 24px 28px;
  border-left: 6px solid var(--teal);
  background: #ffffff;
  box-shadow: 0 16px 36px rgba(15, 23, 42, .08);
  font-size: 24px;
  line-height: 1.55;
}
.hero-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-top: 66px;
  position: relative;
  z-index: 1;
}
.hero-grid div {
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, .72);
  padding: 18px;
  min-height: 126px;
}
.hero-grid b { display: block; font-size: 18px; margin-bottom: 8px; }
.hero-grid p { margin: 0; color: var(--muted); font-size: 15px; line-height: 1.55; }
.toc {
  padding: 52px 78px;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  background: #fff;
}
.toc h2 { margin: 0 0 24px; font-size: 34px; }
.toc-links {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px 18px;
}
.toc a {
  display: flex;
  gap: 14px;
  align-items: center;
  min-height: 56px;
  padding: 12px 16px;
  border: 1px solid var(--line);
  color: var(--ink);
  background: #fbfdff;
}
.toc a span {
  color: var(--teal);
  font-weight: 700;
  font-size: 14px;
}
section {
  padding: 58px 78px;
  border-bottom: 1px solid var(--line);
}
.section-head {
  break-inside: avoid;
  break-after: avoid;
}
.section-kicker {
  color: var(--teal);
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 8px;
}
h2 {
  margin: 0 0 24px;
  font-size: 38px;
  line-height: 1.22;
  letter-spacing: 0;
}
p { margin: 0 0 18px; font-size: 19px; }
.insight {
  margin: 24px 0;
  padding: 22px 24px;
  border: 1px solid rgba(15, 118, 110, .28);
  border-left: 6px solid var(--teal);
  background: #f3fbfa;
  font-size: 19px;
}
figure {
  margin: 34px 0 0;
  padding: 0;
}
figure img {
  display: block;
  width: 100%;
  border: 1px solid var(--line);
  background: #fff;
}
figcaption {
  margin-top: 10px;
  color: var(--muted);
  font-size: 15px;
}
.steps {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin: 8px 0 28px;
}
.steps div {
  min-height: 176px;
  border: 1px solid var(--line);
  background: #fff;
  padding: 20px;
}
.steps span {
  display: inline-grid;
  place-items: center;
  width: 34px;
  height: 34px;
  margin-bottom: 12px;
  border-radius: 50%;
  background: var(--teal);
  color: white;
  font-weight: 800;
}
.steps b { display: block; font-size: 20px; margin-bottom: 8px; }
.steps p { margin: 0; font-size: 16px; color: #475569; line-height: 1.6; }
table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  font-size: 16px;
}
th, td {
  padding: 14px 16px;
  border: 1px solid var(--line);
  vertical-align: top;
}
th { background: #eef7f6; text-align: left; color: #0f3f3b; }
td:first-child { font-weight: 800; width: 18%; }
.myths {
  display: grid;
  gap: 14px;
}
.myths div {
  border: 1px solid var(--line);
  background: #fff;
  padding: 18px 20px;
}
.myths b { color: #b45309; font-size: 18px; }
.myths p { margin: 8px 0 0; font-size: 17px; color: #475569; }
.summary {
  margin: 0;
  padding-left: 26px;
}
.summary li {
  margin: 0 0 18px;
  font-size: 22px;
  line-height: 1.58;
}
.quiz {
  display: grid;
  gap: 14px;
}
.quiz p {
  margin: 0;
  padding: 18px 20px;
  border: 1px solid var(--line);
  background: #fff;
}
.knowledge-map {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 24px 0 0;
}
.knowledge-map span {
  border: 1px solid var(--line);
  background: #fff;
  padding: 9px 12px;
  color: #334155;
  font-size: 15px;
}
.sources {
  padding: 48px 78px 70px;
  color: #475569;
  font-size: 15px;
}
.sources h2 { font-size: 26px; margin-bottom: 16px; color: var(--ink); }
.sources ul { margin: 0; padding-left: 22px; }
.sources li { margin: 8px 0; }
@page { size: A4; margin: 0; }
@media print {
  body { background: white; }
  .page { width: 100%; box-shadow: none; }
  .hero { min-height: 296mm; page-break-after: always; }
  h2 { break-after: avoid; }
  figure, table, .steps, .insight, .quiz p, .myths div { break-inside: avoid; }
  a { color: var(--blue); }
}
@media (max-width: 760px) {
  .hero, .toc, section, .sources { padding-left: 24px; padding-right: 24px; }
  h1 { font-size: 46px; }
  .subtitle { font-size: 22px; }
  .hero-grid, .toc-links, .steps { grid-template-columns: 1fr; }
}
"""
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>RAG（检索增强生成）｜AI每日深度科普</title>
  <style>{css}</style>
</head>
<body>
<main class="page">
  <header class="hero">
    <div class="meta"><span>AI每日深度科普</span><span>2026-07-04</span><span>今日概念</span></div>
    <div>
      <h1>RAG<br>检索增强生成</h1>
      <p class="subtitle">为什么真正有用的 AI，往往要先“查资料”再回答？</p>
      <div class="one-line"><b>核心一句话：</b>RAG 的本质，是让大模型像开卷考试一样，先检索可信资料，再基于资料生成答案。</div>
      <div class="knowledge-map">
        <span>知识地图：Embedding → RAG → 向量数据库 → Agent 工具使用</span>
        <span>今天承接：上一期的“意思坐标”如何变成可用问答系统</span>
      </div>
    </div>
    <div class="hero-grid">
      <div><b>它解决什么</b><p>模型不知道私有资料、最新资料时，先把相关证据找出来。</p></div>
      <div><b>它连接什么</b><p>Embedding、向量数据库、搜索索引、上下文窗口和大模型。</p></div>
      <div><b>今天要记住</b><p>RAG 能降低幻觉风险，但不能自动保证答案正确。</p></div>
    </div>
  </header>
  <nav class="toc">
    <h2>目录</h2>
    <div class="toc-links">{render_toc()}</div>
  </nav>
  {render_sections()}
  <footer class="sources">
    <h2>主要参考来源</h2>
    <ul>
      {render_sources()}
    </ul>
  </footer>
</main>
</body>
</html>
"""
    HTML.write_text(html, encoding="utf-8")


def write_sidecars() -> None:
    EMAIL_SUBJECT.write_text("【AI每日深度科普】RAG：为什么真正有用的AI要先查资料再回答？\n", encoding="utf-8")
    EMAIL_BODY.write_text(
        """今天的主题是 RAG（检索增强生成）。

这是理解企业知识库、AI搜索、客服助手和内部 Copilot 的核心概念。

附件会用“开卷考试”的方式解释：
为什么大模型需要先检索资料，再基于证据生成答案。

适合非技术读者、AI初学者、产品经理、知识库/客服/运营团队阅读。
""",
        encoding="utf-8",
    )
    source_lines = "\n".join(f"- {label} — {url}" for label, url in SOURCES_LIST)
    SOURCES.write_text(
        f"""# Sources

{source_lines}

Image generation note:

- Two clean diagram bases were generated with the built-in ChatGPT image generation tool under `/Users/mac/.codex/generated_images/019f2a6d-4a44-7073-b85d-800ed0b783e9/`.
- Final Chinese labels were added locally with PIL to ensure text accuracy and readable Chinese typography.
""",
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


def render_pdf() -> None:
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
    annotate_exam()
    annotate_pipeline()
    write_html()
    write_sidecars()
    render_pdf()
    print(HTML)
    print(PDF)


if __name__ == "__main__":
    main()
