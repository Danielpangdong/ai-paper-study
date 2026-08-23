from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 200
    page_w: int = 1654  # A4 @ 200dpi
    page_h: int = 2339
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
    fig_router = base / "moe_router_experts.png"
    fig_canteen = base / "moe_canteen_analogy.png"
    out_pdf = base / "2026-05-04_AI概念精讲_MoE混合专家模型.pdf"

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
    draw.text((style.margin_x + 22, y + 58), "MoE（混合专家模型）：让大模型像“多位专科老师”", font=title_font, fill=style.ink)
    meta = "日期：2026-05-04    难度：高中友好    关键词：专家 / 分流 / 省算力"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 30

    y = draw_section_title(draw, style, h2_font, "为什么重要", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "模型越做越大，能力往往更强，但也更“费电费时间”。\n"
        "MoE 的想法是：让模型像团队协作一样工作——不是每次都全员出动，\n"
        "而是让最擅长这件事的少数专家来处理，从而在保持“大容量”的同时更省计算。",
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
        "一句话记住：MoE = 很多“专家” + 一个“分流器”，每次只调用少数专家。",
        font=body_font,
        fill=style.accent2,
    )
    y += 130

    y = draw_section_title(draw, style, h2_font, "直观类比（图1）", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_router,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=700,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：路由器挑选 Top‑2 专家参与这次计算。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（不用堆术语）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把 MoE 想成一个“多窗口食堂”：\n"
        "1）有很多个窗口（专家），每个擅长不同类型的处理；\n"
        "2）有一个点餐员（路由器），看一眼你的需求就决定去哪个窗口；\n"
        "3）通常只去 1～2 个窗口（Top‑K），其他窗口这次不营业，所以省算力；\n"
        "4）把选中的窗口输出合并，得到最终结果。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = paste_image_fit(
        page,
        fig_canteen,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=640,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：食堂类比：多数时候只让少数厨师开火。", font=small_font, fill=style.muted)
    y += 56

    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("专家（Experts）", "很多个“擅长方向不同的小模块”。"),
        ("路由器（Router）", "负责挑选这次该用哪些专家的“分流器/分诊台”。"),
        ("Top‑K", "只选 K 个专家参与（常见 K=1 或 K=2），其他专家这次不算。"),
        ("稀疏（Sparse）", "不是每次都用全部模块，而是只用一部分。"),
        ("负载均衡", "别让所有请求都挤到同一个专家，否则会排队、效果也可能变差。"),
    ]
    max_w = style.page_w - style.margin_x * 2
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 290, y, max_w - 290, style.muted, line_gap=10)
        y += 6
    pages.append(page)

    # Page 3
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "实际应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "学习助手 App 同时要做：讲数学题、润色作文、写简单代码。\n"
        "MoE 的直觉是：不同问题“更像”不同学科，路由器就把本次输入交给更合适的专家。\n"
        "这样模型可以保持很大的“总容量”，但每次推理只花少数专家的计算量。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 12
    box = (style.margin_x, y, style.page_w - style.margin_x, y + 126)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 24),
        "把它类比成：有很多老师，但每次只请最相关的 1～2 位来辅导你。",
        font=body_font,
        fill=style.accent2,
    )
    y += 154

    y = draw_section_title(draw, style, h2_font, "常见误区", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）误区：MoE 天生更准确。事实：优势主要在“容量大但每次算得省”，准确率还看训练与路由设计。\n"
        "2）误区：专家越多越好。事实：专家太多会增加训练难度、通信/调度成本与负载不均问题。\n"
        "3）误区：路由器随便写规则就行。事实：路由器本身要学习，挑错专家会影响质量。",
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
        "1）用一句话解释 MoE 的核心想法，它主要想省的是什么？\n"
        "2）为什么 MoE 需要路由器？如果没有路由器会怎样？\n"
        "3）举一个生活中的例子：你会只找 Top‑2 专家而不是叫所有人一起做。",
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

