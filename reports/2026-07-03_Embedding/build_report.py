from __future__ import annotations

from html import escape
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
HTML = BASE / "2026-07-03_Embedding（向量表示）.html"
PDF = BASE / "2026-07-03_Embedding（向量表示）.pdf"
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
    outline: tuple[int, int, int, int] = (17, 94, 89, 170),
    title_color: tuple[int, int, int] = (18, 31, 44),
    body_color: tuple[int, int, int] = (76, 86, 99),
    radius: int = 18,
    title_size: int = 30,
    body_size: int = 23,
    wrap: int = 18,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=3)
    draw.text((x1 + 20, y1 + 16), title, fill=title_color, font=font(title_size, True))
    y = y1 + 58
    for line in wrap_zh(body, wrap)[:4]:
        draw.text((x1 + 20, y), line, fill=body_color, font=font(body_size))
        y += body_size + 8


def annotate_map() -> None:
    img = Image.open(ASSETS / "embedding_map_base.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.text((72, 48), "Embedding：把“意思”放到一张地图上", fill=(14, 28, 42), font=font(48, True))
    draw.text(
        (72, 112),
        "离得近，通常代表意思接近；离得远，通常代表主题差异更大。",
        fill=(82, 92, 105),
        font=font(28),
    )

    rounded_label(draw, (72, 236, 342, 338), "输入内容", "一句话、一段文档、一张图片，先被模型读懂大概含义。", outline=(20, 184, 166, 180), wrap=13)
    rounded_label(draw, (70, 435, 330, 705), "颜色簇", "每个点是一段内容。\n同一类意思会自然聚在一起，不要求用词完全一样。", outline=(148, 163, 184, 190), title_size=28, body_size=22, wrap=12)

    labels = [
        ((320, 238, 585, 318), "宠物护理", "猫粮、狗毛、洗澡"),
        ((420, 720, 680, 806), "物流服务", "派送、签收、中转"),
        ((762, 848, 1048, 934), "金融公司", "收入、成本、估值"),
        ((1268, 172, 1546, 262), "旅行计划", "酒店、路线、景点"),
        ((1368, 408, 1640, 502), "电子产品", "芯片、手机、电脑"),
        ((1298, 716, 1576, 806), "健康运动", "睡眠、跑步、恢复"),
    ]
    colors = [
        (17, 94, 89, 180),
        (8, 145, 178, 180),
        (101, 163, 13, 180),
        (217, 119, 6, 180),
        (234, 88, 12, 180),
        (37, 99, 235, 180),
    ]
    for (box, title, body), color in zip(labels, colors):
        rounded_label(draw, box, title, body, outline=color, title_size=26, body_size=20, wrap=11)

    rounded_label(
        draw,
        (704, 350, 1010, 470),
        "查询向量",
        "用户问题也会变成一个点，然后去找最近的一群点。",
        fill=(255, 255, 255, 242),
        outline=(31, 41, 55, 190),
        title_size=28,
        body_size=22,
        wrap=14,
    )
    rounded_label(
        draw,
        (560, 82, 1110, 162),
        "关键直觉",
        "Embedding 不是给文字编号，而是给“含义”定位。",
        outline=(245, 158, 11, 190),
        title_size=28,
        body_size=22,
        wrap=22,
    )

    out = ASSETS / "embedding_meaning_map_labeled.png"
    Image.alpha_composite(img, overlay).convert("RGB").save(out, quality=95)


def annotate_rag() -> None:
    img = Image.open(ASSETS / "embedding_rag_base.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.text((60, 34), "Embedding 如何支撑语义搜索和 RAG", fill=(14, 28, 42), font=font(42, True))
    draw.text((60, 90), "同一个“向量坐标系”里比较距离：问题离哪份资料最近，就先把哪份资料拿出来。", fill=(82, 92, 105), font=font(25))

    top_labels = [
        ((42, 115, 330, 162), "1 用户问题"),
        ((445, 115, 775, 162), "2 问题变向量"),
        ((885, 115, 1215, 162), "3 找最近资料"),
        ((1320, 115, 1624, 162), "4 生成回答"),
    ]
    for box, label in top_labels:
        rounded_label(draw, box, label, "", fill=(255, 255, 255, 232), outline=(30, 64, 175, 160), title_size=24, radius=14)

    notes = [
        ((44, 548, 342, 650), "不是只看关键词", "“包裹卡在转运中心”也能找到“中转异常处理”。"),
        ((430, 708, 795, 820), "资料提前入库", "文档先切块，再各自生成向量，存进向量库。"),
        ((870, 650, 1218, 764), "相似度排序", "常用余弦相似度：方向越接近，语义越可能接近。"),
        ((1320, 618, 1608, 734), "答案仍需核对", "检索能补资料，但不能保证模型不误读。"),
    ]
    colors = [(20, 184, 166, 180), (245, 158, 11, 180), (37, 99, 235, 180), (22, 163, 74, 180)]
    for (box, title, body), color in zip(notes, colors):
        rounded_label(draw, box, title, body, outline=color, title_size=27, body_size=21, wrap=13)

    rounded_label(
        draw,
        (470, 352, 790, 460),
        "Embedding 模型",
        "把文字压成一串数字：\n[0.12, -0.38, ...]",
        fill=(247, 253, 252, 238),
        outline=(13, 148, 136, 180),
        title_size=28,
        body_size=23,
        wrap=16,
    )
    rounded_label(
        draw,
        (880, 336, 1158, 446),
        "向量空间",
        "最近的点，通常就是最相关的资料块。",
        fill=(255, 255, 255, 238),
        outline=(37, 99, 235, 180),
        title_size=28,
        body_size=22,
        wrap=13,
    )

    out = ASSETS / "embedding_rag_flow_labeled.png"
    Image.alpha_composite(img, overlay).convert("RGB").save(out, quality=95)


SECTIONS = [
    {
        "id": "why",
        "title": "为什么这个概念重要？",
        "body": """
<p>Embedding 解决的是一个非常根本的问题：计算机原本只擅长比较“符号是否一样”，却不擅长比较“意思是否相近”。</p>
<p>如果你在搜索框里输入“电脑发烫怎么办”，传统关键词系统更容易找含有“电脑”“发烫”的文章；但你真正想找的，也许是“笔记本散热异常”“CPU温度过高”“风扇清灰”。这些词不完全一样，但意思在同一片区域。Embedding 的价值，就是把这种“意思相近”变成可以计算的距离。</p>
<div class="insight"><b>行业为什么离不开它：</b>AI 搜索、RAG、推荐系统、相似图片检索、客服知识库、内容聚类、多模态模型，都需要先把复杂内容变成向量，才能快速比较和召回。</div>
<p>它改变了很多 AI 产品的底层逻辑：从“找到完全匹配的字”，升级为“找到真正相关的意思”。这也是为什么你问 AI 一个很生活化的问题，它可以从文档库里找出并不含原句、但确实相关的资料。</p>
""",
    },
    {
        "id": "analogy",
        "title": "一个直观类比：会摆书的图书管理员",
        "body": """
<p>想象一所巨大的图书馆。老管理员只会按书名里的字摆书：书名有“猫”的放一排，有“狗”的放一排，有“宠物”的又放另一排。结果是：一本《新手铲屎官指南》和一本《狗狗洗澡手册》明明都在讲宠物照护，却被分得很远。</p>
<p>Embedding 像一位更聪明的管理员。它读完每本书后，不只看标题，而是判断这本书在讲什么，然后把它放到“意思地图”上的一个位置。讲宠物照护的书靠近，讲芯片制造的书靠近，讲旅行计划的书靠近。</p>
<p>当你问“猫掉毛严重怎么办”，管理员不会只找包含这几个字的书，而是先把你的问题也放到地图上，再拿出离它最近的一堆资料。你看到的结果，就更像“懂你在问什么”。</p>
""",
        "image": "assets/embedding_meaning_map_labeled.png",
        "caption": "图解 1：Embedding 把内容放进“意义地图”。相似含义聚在一起，语义搜索就是找最近的点。",
    },
    {
        "id": "how",
        "title": "工作原理：从文字到可计算的坐标",
        "body": """
<div class="steps">
  <div><span>1</span><b>输入内容</b><p>可以是一句话、一段文档、一张图片，甚至一段音频。系统先把它交给 embedding 模型。</p></div>
  <div><span>2</span><b>压成向量</b><p>模型输出一串数字，比如 [0.12, -0.38, ...]。单个数字通常没有直观含义，整串数字才代表位置。</p></div>
  <div><span>3</span><b>比较距离</b><p>两个向量方向越接近，系统越认为它们语义相近。常见做法是计算余弦相似度。</p></div>
  <div><span>4</span><b>用于召回</b><p>找到最相近的资料、商品、图片或用户兴趣，再交给搜索、推荐或大模型继续处理。</p></div>
</div>
<p>训练 embedding 的直觉并不神秘。模型看过大量语料后，会发现“猫”“狗”经常出现在“宠物、喂养、毛发、洗澡”附近；“芯片”“GPU”“算力”经常出现在另一组上下文附近。久而久之，模型学会把经常共享语境的内容放近一些。</p>
<p>这也是为什么现代 embedding 不只是“单词表”。同一个词在不同句子里可能有不同含义：“银行提高利率”和“河流冲刷银行”在中文里不常见，但英文 bank 就有金融机构和河岸两种意思。更强的模型会结合上下文，尽量给出更贴近当前语境的向量。</p>
""",
        "image": "assets/embedding_rag_flow_labeled.png",
        "caption": "图解 2：在 RAG/AI 搜索里，问题和资料都先变成向量，再按距离找最相关内容。",
    },
    {
        "id": "terms",
        "title": "关键术语解释",
        "body": """
<table>
  <thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead>
  <tbody>
    <tr><td>Embedding</td><td>把文本、图像等对象映射到连续向量空间的表示方法。</td><td>给内容做一个“意义坐标”。</td></tr>
    <tr><td>Vector 向量</td><td>由多个数字组成的数组，用来表示对象在空间中的位置。</td><td>像 GPS 坐标，只是维度更多。</td></tr>
    <tr><td>Dimension 维度</td><td>向量里的数字数量，例如 256、1024、3072 维。</td><td>描述位置用多少个“刻度”。更多不一定永远更好。</td></tr>
    <tr><td>Semantic Similarity</td><td>两个对象在语义上的接近程度。</td><td>说法不同，但意思是不是很像。</td></tr>
    <tr><td>Cosine Similarity</td><td>用两个向量夹角衡量相似度的常见方法。</td><td>看两个箭头是不是指向差不多的方向。</td></tr>
    <tr><td>Vector Database</td><td>专门存储和检索大量向量的数据库。</td><td>一座按“意思距离”找资料的图书馆。</td></tr>
    <tr><td>Chunk</td><td>把长文档切成较短、可独立检索的片段。</td><td>把整本书拆成可查询的小卡片。</td></tr>
  </tbody>
</table>
""",
    },
    {
        "id": "case",
        "title": "真实应用案例：企业知识库客服",
        "body": """
<p>假设一家物流企业有几千份内部知识文档：派送规则、异常件处理、理赔流程、网点操作手册。用户问：“我的包裹卡在中转场两天了，该怎么办？”</p>
<p>知识库里真正有用的文档标题可能叫《中转异常滞留处理规范》，里面未必出现“卡住”这个词。传统关键词搜索可能漏掉它；embedding 搜索会发现“卡在中转场”和“中转异常滞留”在意思地图上很近，于是把这份规范召回。</p>
<p>接下来，大模型拿着召回资料生成回答：先解释可能原因，再给用户下一步操作，再提醒哪些情况需要人工介入。这里 embedding 负责“把资料找对”，大模型负责“把话说清楚”。两者配合，才是很多 RAG 系统的基本形态。</p>
<div class="insight"><b>一句话看懂分工：</b>Embedding 像检索员，负责找相关资料；大模型像讲解员，负责把资料组织成自然语言答案。</div>
""",
    },
    {
        "id": "myths",
        "title": "常见误区",
        "body": """
<div class="myths">
  <div><b>误区一：Embedding 等于真正理解。</b><p>不是。它是高效的统计表示，能捕捉很多语义关系，但不等于人类理解、常识判断或事实核验。</p></div>
  <div><b>误区二：距离近就一定正确。</b><p>距离近只代表“可能相关”。相似资料也可能过时、片面或错误，所以 RAG 仍需要来源、权限、时间和质量控制。</p></div>
  <div><b>误区三：向量数据库就是万能记忆。</b><p>向量库擅长相似检索，不擅长自动保证因果、计算、权限和最新事实。它不是大模型的无限大脑。</p></div>
  <div><b>误区四：维度越高越好。</b><p>高维可能更细腻，也可能更贵、更慢、更占空间。工程上通常要在效果、成本和速度之间取平衡。</p></div>
  <div><b>误区五：Embedding 可以完全替代关键词搜索。</b><p>很多生产系统会混合使用：关键词适合精确匹配编号、人名、订单号；向量适合语义相近但字面不同的问题。</p></div>
</div>
""",
    },
    {
        "id": "summary",
        "title": "3句话总结",
        "body": """
<ol class="summary">
  <li>Embedding 的本质，是把复杂内容变成一串数字坐标，让机器能计算“意思相近”。</li>
  <li>它让 AI 搜索、RAG、推荐、聚类、多模态检索从“字面匹配”升级到“语义匹配”。</li>
  <li>但相似不等于真实，embedding 解决的是“找相关资料”，不是自动保证答案正确。</li>
</ol>
""",
    },
    {
        "id": "quiz",
        "title": "复习问题",
        "body": """
<div class="quiz">
  <p><b>1.</b> 如果用户问“笔记本太烫怎么办”，为什么 embedding 可能找到“CPU温度过高处理指南”，即使标题没有“太烫”两个字？</p>
  <p><b>2.</b> 在企业 RAG 系统里，embedding 和大模型分别承担什么角色？如果资料召回错了，会发生什么？</p>
  <p><b>3.</b> 为什么订单号、身份证号、精确产品型号这类信息，通常不能只靠向量相似度来检索？</p>
</div>
""",
    },
]


def render_toc() -> str:
    items = []
    for idx, section in enumerate(SECTIONS, 1):
        items.append(f'<a href="#{section["id"]}"><span>{idx:02d}</span>{escape(section["title"])}</a>')
    return "\n".join(items)


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
  --coral: #e4572e;
  --green: #15803d;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: #eef2f6;
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
  padding: 76px 78px 54px;
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
  margin: 92px 0 18px;
  font-size: 72px;
  line-height: 1.04;
  letter-spacing: 0;
}
.subtitle {
  max-width: 720px;
  margin: 0;
  color: #334155;
  font-size: 28px;
  line-height: 1.38;
}
.one-line {
  width: min(780px, 100%);
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
  h1 { font-size: 48px; }
  .subtitle { font-size: 22px; }
  .hero-grid, .toc-links, .steps { grid-template-columns: 1fr; }
}
"""
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Embedding（向量表示）｜AI每日深度科普</title>
  <style>{css}</style>
</head>
<body>
<main class="page">
  <header class="hero">
    <div class="meta"><span>AI每日深度科普</span><span>2026-07-03</span><span>Concept 进阶</span></div>
    <div>
      <h1>Embedding<br>向量表示</h1>
      <p class="subtitle">为什么 AI 能听懂“意思相近”，而不只是“字面相同”？</p>
      <div class="one-line"><b>核心一句话：</b>Embedding 的本质，是把文字、图片、声音等内容压成一串数字坐标，让 AI 可以计算“谁和谁更像”。</div>
    </div>
    <div class="hero-grid">
      <div><b>它解决什么</b><p>把“语义”变成可计算距离，让机器不再只看关键词。</p></div>
      <div><b>它连接什么</b><p>RAG、AI搜索、向量数据库、推荐系统、多模态检索。</p></div>
      <div><b>今天要记住</b><p>相似不等于真实，召回正确只是回答正确的第一步。</p></div>
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
      <li><a href="https://developers.openai.com/api/docs/guides/embeddings">OpenAI API Docs: Vector embeddings</a></li>
      <li><a href="https://developers.google.com/machine-learning/crash-course/embeddings">Google Machine Learning Crash Course: Embeddings</a></li>
      <li><a href="https://arxiv.org/abs/1301.3781">Mikolov et al., Efficient Estimation of Word Representations in Vector Space</a></li>
      <li><a href="https://arxiv.org/abs/1908.10084">Reimers &amp; Gurevych, Sentence-BERT</a></li>
      <li><a href="https://arxiv.org/abs/2005.11401">Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks</a></li>
      <li><a href="https://developers.openai.com/cookbook/examples/question_answering_using_embeddings">OpenAI Cookbook: Question answering using embeddings-based search</a></li>
    </ul>
  </footer>
</main>
</body>
</html>
"""
    HTML.write_text(html, encoding="utf-8")


def write_sidecars() -> None:
    EMAIL_SUBJECT.write_text("【AI每日深度科普】Embedding：为什么AI能理解“意思相近”？\n", encoding="utf-8")
    EMAIL_BODY.write_text(
        """今天的主题是 Embedding（向量表示）。

这是理解 RAG、向量数据库、AI搜索、推荐系统和多模态检索的基础概念。

附件会用“会摆书的图书管理员”和“意义地图”的方式解释：
为什么 AI 不只匹配关键词，而能找到意思相近的内容。

适合非技术读者、AI初学者、产品经理和研究者阅读。
""",
        encoding="utf-8",
    )
    SOURCES.write_text(
        """# Sources

- OpenAI API Docs: Vector embeddings — https://developers.openai.com/api/docs/guides/embeddings
- Google Machine Learning Crash Course: Embeddings — https://developers.google.com/machine-learning/crash-course/embeddings
- Mikolov et al., Efficient Estimation of Word Representations in Vector Space — https://arxiv.org/abs/1301.3781
- Reimers & Gurevych, Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks — https://arxiv.org/abs/1908.10084
- Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks — https://arxiv.org/abs/2005.11401
- OpenAI Cookbook: Question answering using embeddings-based search — https://developers.openai.com/cookbook/examples/question_answering_using_embeddings

Image generation note:

- Two clean diagram bases were generated with the built-in ChatGPT image generation tool under `/Users/mac/.codex/generated_images/019f2546-d587-7d71-92f4-f69c7f9fa047/`.
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
    annotate_map()
    annotate_rag()
    write_html()
    write_sidecars()
    render_pdf()
    print(HTML)
    print(PDF)


if __name__ == "__main__":
    main()
