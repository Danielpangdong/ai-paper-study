from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 170
    page_w: int = 1406  # A4 @ 170dpi
    page_h: int = 1987
    margin_x: int = 118
    margin_y: int = 108
    gutter: int = 18
    ink: tuple[int, int, int] = (15, 23, 42)
    muted: tuple[int, int, int] = (71, 85, 105)
    line: tuple[int, int, int] = (226, 232, 240)
    soft: tuple[int, int, int] = (248, 250, 252)
    accent: tuple[int, int, int] = (14, 165, 163)
    accent2: tuple[int, int, int] = (37, 99, 235)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size, index=0)
    return ImageFont.load_default()


def text_width(font: ImageFont.ImageFont, text: str) -> float:
    try:
        return font.getlength(text)
    except Exception:
        return font.getbbox(text)[2]


def wrap_text(font: ImageFont.ImageFont, text: str, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            lines.append("")
            continue
        buf = ""
        for ch in para:
            if ch == "\r":
                continue
            trial = buf + ch
            if text_width(font, trial) <= max_w:
                buf = trial
                continue
            if buf:
                lines.append(buf.rstrip())
                buf = ch.lstrip()
            else:
                lines.append(trial)
                buf = ""
        if buf:
            lines.append(buf.rstrip())
        lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def draw_paragraph(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.ImageFont,
    text: str,
    x: int,
    y: int,
    max_w: int,
    fill: tuple[int, int, int],
    line_gap: int,
) -> int:
    lines = wrap_text(font, text, max_w)
    for line in lines:
        if not line:
            y += int(font.size * 0.6)
            continue
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def draw_section_title(
    draw: ImageDraw.ImageDraw,
    style: Style,
    title_font: ImageFont.ImageFont,
    title: str,
    x: int,
    y: int,
) -> int:
    r = 10
    draw.rounded_rectangle((x, y + 8, x + 26, y + 8 + 26), radius=r, fill=style.accent)
    draw.text((x + 44, y), title, font=title_font, fill=style.ink)
    return y + title_font.size + style.gutter


def paste_image_fit(
    page: Image.Image,
    img_path: Path,
    x: int,
    y: int,
    max_w: int,
    max_h: int,
    border: bool = True,
    style: Style | None = None,
) -> int:
    img = Image.open(img_path).convert("RGB")
    scale = min(max_w / img.width, max_h / img.height, 1.0)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    img = img.resize((new_w, new_h), Image.LANCZOS)
    page.paste(img, (x, y))
    if border and style is not None:
        draw = ImageDraw.Draw(page)
        draw.rounded_rectangle(
            (x - 2, y - 2, x + new_w + 2, y + new_h + 2),
            radius=18,
            outline=style.line,
            width=3,
        )
    return y + new_h + 18


def build() -> Path:
    style = Style()
    base = Path(__file__).resolve().parent
    fig_pipeline = base / "rag_pipeline.png"
    fig_library = base / "rag_library_analogy.png"
    out_pdf = base / "2026-05-05_AI概念精讲_RAG检索增强生成.pdf"

    title_font = load_font(52)
    kicker_font = load_font(19)
    h2_font = load_font(30)
    body_font = load_font(23)
    small_font = load_font(18)

    pages: list[Image.Image] = []

    def new_page() -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
        page = Image.new("RGB", (style.page_w, style.page_h), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        y0 = style.margin_y
        return page, draw, y0

    # Page 1
    page, draw, y = new_page()
    header_h = 210
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "每日AI概念精讲", font=kicker_font, fill=style.muted)
    draw.text((style.margin_x + 22, y + 58), "RAG（检索增强生成）：让大模型“先查资料再回答”", font=title_font, fill=style.ink)
    meta = "日期：2026-05-05    难度：高中友好    关键词：检索 / 向量库 / 减少幻觉"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 30

    y = draw_section_title(draw, style, h2_font, "为什么重要", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "大模型很会“写”，但它并不自带你公司的最新制度、今天的新闻、或你班级的课表。\n"
        "如果只靠模型“凭记忆作答”，就可能编出听起来很像真的内容（这叫“幻觉”）。\n"
        "RAG 的办法是：回答前先去资料库里把最相关的内容找出来，再让模型依据这些内容回答，\n"
        "就像考试时先翻笔记再写答案一样，更可靠、更可控。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 18
    box = (style.margin_x, y, style.page_w - style.margin_x, y + 112)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 28),
        "一句话记住：RAG = 先检索“证据” + 再生成“答案”。",
        font=body_font,
        fill=style.accent2,
    )
    y += 130

    y = draw_section_title(draw, style, h2_font, "工作流程（图1）", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_pipeline,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=700,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：RAG 的基本流水线：检索到资料片段，再交给大模型生成。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "直观类比（图2）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把 RAG 想成“写作文”\n"
        "你要写一篇科普小作文：\n"
        "1）先去图书馆/手机里搜资料，找到最相关的几段；\n"
        "2）把这些段落当作“可引用的材料”；\n"
        "3）最后用自己的话把文章写出来，并且不跑题。\n"
        "RAG 就是把这套流程搬给大模型：先查，再写。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = paste_image_fit(
        page,
        fig_library,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=640,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：图书馆类比：先找“证据段落”，再组织成回答。", font=small_font, fill=style.muted)
    y += 56

    y = draw_section_title(draw, style, h2_font, "工作原理（不用堆术语）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "RAG 通常分三步：\n"
        "1）把资料变成“好检索的形状”：把文档切成小段（chunk），每段做一个“含义指纹”。\n"
        "2）收到问题时先“找”：用同样的方法给问题做指纹，在指纹库里找最像的几段资料。\n"
        "3）再“写”：把找到的资料片段连同问题一起发给大模型，让它依据资料回答。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 3
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("检索（Retrieval）", "像在手机里搜关键词/在图书馆按主题找书：先把相关资料找出来。"),
        ("向量（Vector）", "把一段文字的“含义”用一串数字表示，方便比较“像不像”。"),
        ("向量数据库", "专门存这些“含义数字”的仓库，支持快速找最相近的内容。"),
        ("Embedding（嵌入）", "生成“含义指纹”的过程：把文字变成向量。"),
        ("Chunk（分段）", "把长文拆成短段落；太长会塞不进输入，太短又容易丢上下文。"),
        ("Top‑K", "从库里选出最相关的 K 段资料（常见 K=3～8）。"),
        ("上下文（Context）", "大模型这次回答时“能看到”的材料：问题 + 找到的资料片段。"),
    ]
    max_w = style.page_w - style.margin_x * 2
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 290, y, max_w - 290, style.muted, line_gap=10)
        y += 6

    y += 6
    y = draw_section_title(draw, style, h2_font, "一个实际应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "“公司制度问答助手”\n"
        "把员工手册、报销规则、流程文档放进资料库。员工提问：\n"
        "“出差交通费怎么报销？”系统先检索出最相关的制度条款，再让大模型把条款用人话解释，\n"
        "并给出步骤清单。好处是：内容更新只要更新文档，不必重新训练大模型。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 4
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "常见误区", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）误区：有了 RAG 就不会胡说。事实：检索可能找错段落；模型也可能“断章取义”。\n"
        "2）误区：资料越多越好。事实：资料太杂会让检索变难；更重要的是资料质量与结构。\n"
        "3）误区：只要把文档丢进向量库就行。事实：分段、去重、标题/来源信息、更新策略都很关键。\n"
        "4）误区：RAG 等于联网搜索。事实：RAG 更像“在你自己的资料库里找”，不一定访问互联网。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 14

    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）用一句话解释 RAG：它先做什么、后做什么？\n"
        "2）为什么要把长文切成 chunk？chunk 太长/太短分别有什么问题？\n"
        "3）举一个你身边的场景：如果让 AI 帮你答题，哪些资料应该放进它的“资料库”？",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：强调直观理解与可视化。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Pillow in this environment may be built without JPEG support; PDF export
    # for RGB pages uses JPEG internally. Use an indexed palette to avoid JPEG.
    pal_pages = [p.convert("P", palette=Image.Palette.ADAPTIVE, colors=256) for p in pages]
    pal_pages[0].save(
        out_pdf,
        save_all=True,
        append_images=pal_pages[1:],
        resolution=float(style.dpi),
    )
    return out_pdf


if __name__ == "__main__":
    path = build()
    print(str(path))
