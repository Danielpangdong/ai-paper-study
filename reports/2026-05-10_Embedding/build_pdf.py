from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 150
    page_w: int = 1240  # A4 @ 150dpi
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
    fig_space = base / "embedding_vector_space.png"
    fig_pipeline = base / "embedding_rag_pipeline.png"
    out_pdf = base / "2026-05-10_Embedding（向量表征）.pdf"

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

    toc_items = [
        "1. 为什么这个概念重要？",
        "2. 直观类比：把意思变成坐标",
        "3. 工作原理：从文字到向量再到检索",
        "4. 关键术语解释",
        "5. 一个真实应用案例",
        "6. 常见误区",
        "7. 3句话总结",
        "8. 3个复习问题",
    ]

    max_w = style.page_w - style.margin_x * 2

    # Page 1: Title + importance
    page, draw, y = new_page()
    header_h = 230
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "AI每日深度科普", font=kicker_font, fill=style.muted)
    draw.text((style.margin_x + 22, y + 58), "Embedding（向量表征）：把“意思”变成“坐标”", font=title_font, fill=style.ink)
    meta = "日期：2026-05-10    难度：高中友好    关键词：相似度 / 向量 / 检索"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 124)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：Embedding 的本质，是把“内容的意思”翻译成一串数字，让机器能计算“像不像”。",
        font=body_font,
        fill=style.accent2,
    )
    y += 150

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "你每天都在用 Embedding，只是你没注意：\n"
        "（1）你在电商搜“轻薄通勤包”，系统能找出“上班用、容量合适、风格简洁”的包；\n"
        "（2）你在短视频刷到一个内容，平台能推更多“意思相近”的内容；\n"
        "（3）你问 AI 助手公司制度，它能从一大堆文档里捞出“最相关的那几段”。\n"
        "\n"
        "这些能力的共同点是：不是按“字面相同”找，而是按“意思相近”找。\n"
        "Embedding 就像给每段文字/图片/代码发一张“坐标卡”，\n"
        "坐标离得越近，代表意思越像。\n"
        "\n"
        "在 AI 工程里，Embedding 是 RAG、向量数据库、语义搜索、推荐系统的地基。\n"
        "你理解了它，就能理解：为什么 AI 搜索比关键词更聪明；\n"
        "也能理解：为什么有些‘看起来很像’的检索，依然会翻车（误区部分会讲）。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（自动生成）", style.margin_x, y)
    y = draw_paragraph(draw, body_font, "\n".join(toc_items), style.margin_x, y, max_w, style.ink, line_gap=10)
    hint = "阅读顺序建议：先看图1的“坐标”直觉 → 再看图2的“RAG流程” → 最后读误区。"
    y += 24
    draw.rounded_rectangle(
        (style.margin_x, y, style.page_w - style.margin_x, y + 92),
        radius=18,
        outline=style.line,
        width=3,
        fill=(245, 250, 255),
    )
    draw.text((style.margin_x + 22, y + 28), hint, font=body_font, fill=style.muted)
    pages.append(page)

    # Page 3: Analogy + fig1
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个直观类比（图1）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把互联网想成一个超级大的“城市”，每一条内容都是一栋楼：\n"
        "“猫”“小猫”“喵星人”是三栋不同的楼，门牌（字面）不一样，但它们在同一个街区（意思相近）。\n"
        "\n"
        "Embedding 做的事，就是给每栋楼一个“坐标”：\n"
        "坐标离得近 → 内容意思更像；坐标离得远 → 意思差得多。\n"
        "这样，机器就不用死盯关键词，而是能用距离来做‘找相似’。\n"
        "\n"
        "关键直觉：Embedding 不是把文字变成“解释”，\n"
        "而是把文字变成“可以被计算的指纹/位置”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 14
    y = paste_image_fit(
        page,
        fig_space,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=950,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：Embedding 把“意思”映射到空间；距离近≈更相似。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 4: How it works + fig2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（图2）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "Embedding 的工程工作流可以用 4 句人话讲清：\n"
        "（1）把问题和资料都变成向量（Embedding）；\n"
        "（2）把资料向量存进向量数据库（像一个按‘意思’排序的索引）；\n"
        "（3）用户提问时，也生成一个问题向量；\n"
        "（4）按距离/相似度找最近的 Top-K 资料片段，再交给大模型写答案。\n"
        "\n"
        "为什么这很强？因为它把‘找资料’变成了数学里的‘找最近邻’。\n"
        "但也要记住：Embedding 只负责“像不像”，\n"
        "不保证“对不对”，更不保证“合规不合规”（误区会详细说）。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(
        page,
        fig_pipeline,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=980,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：Embedding + 向量库让检索从“找字”升级为“找意思”。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 5: Terms + case + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("Token（词元）", "专业：模型处理输入的最小单位。白话：把文字切成一张张小卡片。"),
        ("Embedding（向量表征）", "专业：把输入映射为高维向量。白话：给内容发一张‘坐标卡/指纹卡’。"),
        ("向量（Vector）", "专业：一串数字组成的列表。白话：一排数字坐标，用来当‘位置’。"),
        ("维度（Dimension）", "专业：向量里数字的个数。白话：坐标不是2维平面，而是几百/几千维。"),
        ("相似度/距离", "专业：衡量两个向量接近程度的指标。白话：两张坐标卡离得近不近。"),
        ("余弦相似度", "专业：常用相似度算法之一。白话：看两支‘箭头方向’像不像。"),
        ("向量数据库", "专业：支持向量存储与近邻检索的系统。白话：一个按‘意思’找资料的超级索引。"),
        ("Top-K", "专业：取最相近的 K 条结果。白话：挑出最像的前 K 个候选。"),
    ]
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 350, y, max_w - 350, style.muted, line_gap=10)
        y += 6

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "“企业制度 AI 搜索（报销/合同/流程）”\n"
        "在真实公司里，制度文档往往很多：差旅、报销、审批、采购、合规……\n"
        "员工问一句：‘出差打车能不能报？’\n"
        "如果只做关键词匹配，可能因为写法不同（‘出租车’‘网约车’‘交通费’）漏掉关键条款。\n"
        "\n"
        "做法是：\n"
        "1）把制度拆成很多小段（每段几百字）；\n"
        "2）每段生成 Embedding，存进向量数据库；\n"
        "3）用户提问也生成 Embedding，检索最相近的几段；\n"
        "4）把这几段‘证据’贴进大模型上下文里，让它带着依据回答。\n"
        "\n"
        "结果通常是：更少漏检、更少瞎编、也更容易给出‘引用依据’。",
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
        "1）误区：Embedding=关键词匹配。事实：它更像‘按意思找相近’，但也会受数据与模型影响。\n"
        "2）误区：距离近=一定正确。事实：它只说明‘像’，不说明‘对’；还需要规则、引用与验证。\n"
        "3）误区：Embedding 是万能理解。事实：它是压缩后的指纹，会丢细节；对时间、否定、数字等更要小心。\n"
        "4）误区：有了 Embedding 就不需要上下文窗口。事实：RAG 取回片段后仍要放进上下文里才能回答。\n"
        "5）误区：向量库越大越好。事实：切分方式、更新机制、权限隔离、评测才决定体验。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 10
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）Embedding 把‘意思’变成向量坐标，让机器能计算相似与距离。\n"
        "2）它让搜索/推荐/RAG 从‘找字’升级为‘找意思’，但只负责‘像不像’，不保证‘对不对’。\n"
        "3）要做可靠系统，必须配合：好的切分与权限、检索评测、以及把证据放回上下文。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 10
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）用‘城市坐标’类比解释：为什么 Embedding 能做到“按意思找相近”？\n"
        "2）如果公司制度里写‘出租车费可报销’，员工问‘网约车能报吗？’Embedding 检索为什么可能更好？\n"
        "3）为什么说“距离近不等于答案正确”？你会加哪两道保险来减少翻车？",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：强调直觉、类比与可落地的产品思路。",
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

