from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 120
    page_w: int = 1240  # A4-ish canvas
    page_h: int = 1754
    margin_x: int = 102
    margin_y: int = 94
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

    fig_pipeline = base / "vector_db_pipeline.png"
    fig_analogy = base / "vector_db_library_analogy.png"
    out_pdf = base / "2026-05-24_向量数据库（Vector Database）.pdf"

    title_font = load_font(46)
    kicker_font = load_font(19)
    h2_font = load_font(28)
    body_font = load_font(21)
    small_font = load_font(17)

    pages: list[Image.Image] = []

    def new_page() -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
        page = Image.new("RGB", (style.page_w, style.page_h), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        y0 = style.margin_y
        return page, draw, y0

    max_w = style.page_w - style.margin_x * 2

    toc_items = [
        "1. 为什么这个概念重要？",
        "2. 一个直观类比（非常重要）",
        "3. 工作原理（深入浅出）",
        "4. 关键术语解释",
        "5. 一个真实应用案例",
        "6. 常见误区（非常重要）",
        "7. 3句话总结",
        "8. 3个复习问题",
    ]

    # Page 1: Title + importance
    page, draw, y = new_page()
    header_h = 250
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "AI每日深度科普", font=kicker_font, fill=style.muted)
    draw.text(
        (style.margin_x + 22, y + 58),
        "向量数据库：为什么 AI 能在海量资料里秒搜到“意思相近”的答案？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-24    难度：高中友好    关键词：Embedding / 相似度检索 / ANN / Top-K"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 22

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 152)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 18),
        "核心一句话：向量数据库的本质，是把“文本的意思”变成可计算的坐标，\n"
        "然后用“距离”在海量资料里找最相近的内容，让 AI 能像人一样按语义查资料。",
        font=body_font,
        fill=style.accent2,
    )
    y += 182

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "你可能遇到过这种场景：\n"
        "公司文档几万份、制度流程几十版、历史邮件和工单堆成山——但你只记得个大概意思。\n"
        "这时你问系统：\n"
        "“有没有办法减少配送延误？我想要一些可操作的经验。”\n"
        "如果系统只会‘关键词搜索’，它可能只会找包含“延误”两个字的文件，\n"
        "而真正有用的内容往往写成：‘异常处理’、‘路线优化’、‘装车顺序’、‘调度策略’……\n"
        "\n"
        "向量数据库的重要性在于：它把检索从“找同样的字”，升级为“找相近的意思”。\n"
        "这正是 AI 搜索、RAG 知识库、智能客服、推荐系统、相似案例匹配的底座能力。\n"
        "\n"
        "一句话：没有向量数据库，很多 AI 产品就会变成——\n"
        "模型很会说，但一查资料就像在图书馆里只会按书名找书。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC + analogy figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（快速预览）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "\n".join(f"• {item}" for item in toc_items),
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=8,
    )
    y += 6
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把向量数据库想成一座“超级图书馆”。\n"
        "普通搜索像是：只按书名/目录里的关键词找；你必须猜对关键字。\n"
        "向量数据库更像：图书馆先理解你在问什么，然后带你去“意思相近”的书架区域。\n"
        "\n"
        "你说“减少配送延误”，它可能会带你去：路线规划、调度策略、异常处理、仓库波次、需求预测等区域。\n"
        "也就是说：你用一句自然语言描述需求，系统用‘语义距离’帮你匹配最相关的经验与方法。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y = paste_image_fit(
        page,
        fig_analogy,
        style.margin_x,
        y + 10,
        max_w=max_w,
        max_h=560,
        border=True,
        style=style,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "提示：它找的是“更可能相关”的内容，不等于“绝对正确”。仍需要验证与引用来源。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 3: mechanism + pipeline figure + terms
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "向量数据库最核心的逻辑只有两句话：\n"
        "1）把文字/图片/语音变成“向量”（一串数字坐标）。\n"
        "2）用距离来找“最接近的意思”。\n"
        "\n"
        "但要让它在海量数据里‘秒级检索’，通常会做这 4 件事：\n"
        "A｜切片（Chunk）：把长文拆成段落小块，便于精确命中。\n"
        "B｜向量化（Embedding）：每个小块都变成一个向量。\n"
        "C｜建索引（ANN）：给海量向量建一套“快速导航系统”，不用每次都全量比对。\n"
        "D｜Top-K 检索：取最相近的 K 个片段，交给大模型组织答案并引用来源。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y = paste_image_fit(
        page,
        fig_pipeline,
        style.margin_x,
        y + 10,
        max_w=max_w,
        max_h=620,
        border=True,
        style=style,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "• 向量（Vector）\n"
        "  专业：用一串数字表示一个内容在语义空间的位置。\n"
        "  白话：给“意思”发一个坐标定位。\n"
        "\n"
        "• Embedding（向量表征）\n"
        "  专业：把文本/图片编码成向量的模型或过程。\n"
        "  白话：把一句话翻译成‘语义坐标’。\n"
        "\n"
        "• 相似度 / 距离（Similarity / Distance）\n"
        "  专业：用余弦相似度等指标衡量两个向量的接近程度。\n"
        "  白话：两句话意思越像，坐标点就越近。\n"
        "\n"
        "• ANN（近似最近邻）\n"
        "  专业：用近似方法快速找到最相近的向量，速度远快于全量遍历。\n"
        "  白话：图书馆的快速导航，不用每次把所有书都翻一遍。\n"
        "\n"
        "• Top-K\n"
        "  专业：返回相似度最高的 K 个结果。\n"
        "  白话：先拿最相关的前几条资料，别一口气把整座图书馆搬来。\n"
        "\n"
        "• Chunk（切片）\n"
        "  专业：把长文拆成更小的片段进行向量化与检索。\n"
        "  白话：把一本书拆成很多段落，方便精准命中。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 4: case + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "以“企业知识库 AI 搜索 / AI 客服”为例：\n"
        "客户问：‘包裹显示到站了但两天没派送，怎么办？’\n"
        "真正有用的信息可能散落在：异常件处理 SOP、站点爆仓预案、路线调整规则、客服话术、历史工单总结。\n"
        "\n"
        "系统流程通常是：\n"
        "1）把这些文档切片并向量化，存进向量数据库；\n"
        "2）用户一提问，就用向量检索找到最相关的几段；\n"
        "3）再由大模型把资料‘读一遍’，用更自然的语言解释，并给出可执行步骤。\n"
        "\n"
        "这样做的价值是：回答不仅更像‘懂业务的同事’，还更容易给出来源依据，减少胡编乱造。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 10
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "误区 1：向量数据库 = 更高级的关键词搜索。\n"
        "更准确：它是一种‘按语义相似度检索’的系统，强项是意思相近，不是字面相同。\n"
        "\n"
        "误区 2：用了向量数据库，AI 就不会胡说。\n"
        "现实：向量检索只能把更相关的资料找出来；答案仍要看大模型是否引用得当、是否遵守规则。\n"
        "\n"
        "误区 3：向量检索永远最准确。\n"
        "现实：Embedding 模型、切片策略、数据质量、索引参数都会影响结果；‘相关’不等于‘正确’。\n"
        "\n"
        "误区 4：向量数据库就是 AI 的长期记忆。\n"
        "现实：它更像‘可检索的外部记忆库’；是否写入、写入什么、何时更新，仍需要工程策略与权限管理。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 8
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）向量数据库把“意思”变成可计算的坐标，用距离来找相近内容。\n"
        "2）它靠切片 + Embedding + ANN 索引，实现海量数据的秒级 Top-K 检索。\n"
        "3）它让 AI 更像‘会查资料的助手’，但结果仍需验证：相关不等于正确。",
        style.margin_x,
        y,
        max_w,
        style.accent2,
        line_gap=10,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）为什么说向量数据库更像在‘按意思找书’，而不是在‘按关键词找书’？请举一个你工作/学习中的例子。\n"
        "2）如果文档切片（Chunk）切得太大或太小，检索结果分别可能出现什么问题？\n"
        "3）向量检索找到了 Top-K 片段后，大模型还需要做什么才能给出可靠答案？你会如何要求它引用来源？",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：用类比 + 流程图解释向量数据库的直觉、用法与边界。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Keep the PDF under Gmail's 25MB attachment limit:
    target_w = int(style.page_w * 0.8)
    target_h = int(style.page_h * 0.8)
    scaled_pages = [p.resize((target_w, target_h), Image.LANCZOS) for p in pages]
    pal_pages = [p.convert("P", palette=Image.Palette.ADAPTIVE, colors=192) for p in scaled_pages]
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

