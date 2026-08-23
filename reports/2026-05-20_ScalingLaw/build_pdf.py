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

    fig_curve = base / "scaling_law_curves.png"
    fig_school = base / "scaling_law_school_analogy.png"
    out_pdf = base / "2026-05-20_ScalingLaw（规模定律）.pdf"

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
    header_h = 230
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "AI每日深度科普", font=kicker_font, fill=style.muted)
    draw.text(
        (style.margin_x + 22, y + 58),
        "Scaling Law（规模定律）：为什么“堆资源”真的能让 AI 变强？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-20    难度：高中友好    关键词：数据 / 算力 / 参数 / 边际收益"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 128)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：规模定律的本质，是“投入更多数据/算力/参数，模型能力往往会按可预测的规律提升——但越到后面提升越慢”。",
        font=body_font,
        fill=style.accent2,
    )
    y += 156

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "很多人对 AI 的误解来自一句话：\n"
        "“它看起来很聪明，但我不知道它为什么会突然变强。”\n"
        "\n"
        "规模定律告诉你：大模型能力提升，往往不是玄学，而更像“办学校”——\n"
        "你给它更多教材（数据）、更多学习时间（算力）、更大的脑容量（参数），\n"
        "它通常就会更强，而且强到某个程度之前，这种提升是能预期的。\n"
        "\n"
        "这件事为什么重要？因为它直接影响三类现实决策：\n"
        "1）公司/国家：钱该花在哪？更多 GPU？更多数据？还是更好的模型结构？\n"
        "2）产品/创业：为什么同类模型差一点点资源，体验会差很多？\n"
        "3）普通人：为什么“更大的模型”常常更会写、更会推理、更会对话？\n"
        "\n"
        "理解规模定律，你就理解了 AI 进步的一条主线：\n"
        "很多突破来自“规模 + 工程”，而不是每天都在发明全新魔法。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC + analogy (with figure)
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（你将学到什么）", style.margin_x, y)
    toc_text = "\n".join([f"{i+1}. {t.split('.',1)[1].strip()}" for i, t in enumerate(toc_items)])
    y = draw_paragraph(draw, body_font, toc_text, style.margin_x, y, max_w, style.ink, line_gap=10)

    y += 8
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把训练大模型想成“办一所超级学校”：\n"
        "\n"
        "- 数据量：题库/教材/作业量（你让学生见过多少题、多少知识面）\n"
        "- 算力：学习时间/练习次数（你给学生多少节课、多少套卷子）\n"
        "- 参数量：大脑容量（学生能装下多复杂的知识结构）\n"
        "\n"
        "规模定律的直觉就是：\n"
        "这三样通常越多，毕业生（模型）越强；但“只猛加一个”往往会浪费。\n"
        "题库再大，没时间学也不行；时间再多，大脑太小也装不下；脑子再大，没教材也学不到东西。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y = paste_image_fit(
        page,
        fig_school,
        style.margin_x,
        y + 8,
        max_w,
        max_h=620,
        border=True,
        style=style,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "图：用“办学校”理解规模定律：三种资源都重要，而且要讲配比。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 3: How it works (with figure)
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "先抓住两句“人话版规律”：\n"
        "（1）当你把数据/算力/参数做大，模型能力通常会上升；\n"
        "（2）但越到后面越难：同样多加 10%，带来的提升会越来越小（边际收益递减）。\n"
        "\n"
        "为什么会这样？用生活语言讲：\n"
        "- 前期：题库从 100 题变成 10 万题，学生“开眼界”，进步飞快；\n"
        "- 中期：题库再翻倍，更多是在补边角、打磨细节；\n"
        "- 后期：想再涨 1 分，可能要翻好几倍资源。\n"
        "\n"
        "所以现实里经常出现三种现象：\n"
        "1）更大模型常常更聪明，但更贵；\n"
        "2）做产品时，“足够好”的点比“极致最强”更划算；\n"
        "3）工程优化（更快推理、更好的数据、蒸馏/量化）能用更小成本逼近大模型体验。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y = paste_image_fit(
        page,
        fig_curve,
        style.margin_x,
        y + 8,
        max_w,
        max_h=700,
        border=True,
        style=style,
    )
    pages.append(page)

    # Page 4: Terms + real-world case
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）参数量（Parameters）\n"
        "   专业：模型可学习的权重数量。\n"
        "   白话：模型“大脑的容量”，能装下多复杂的知识结构。\n"
        "\n"
        "2）算力（Compute）\n"
        "   专业：训练/推理时消耗的计算资源（比如 GPU 时间）。\n"
        "   白话：学习时间与练习次数，越多越能把知识学扎实。\n"
        "\n"
        "3）数据量（Data）\n"
        "   专业：训练使用的文本/图片/代码等数据规模与质量。\n"
        "   白话：题库与教材的覆盖面，决定你见过多少世界。\n"
        "\n"
        "4）边际收益递减\n"
        "   专业：额外投入带来的提升逐渐变小。\n"
        "   白话：从 60 分到 80 分很快，从 95 分到 96 分很难。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "场景：你在公司里做一个“客服助手”。\n"
        "你有两种路线：\n"
        "A）直接用更大的模型（更贵，但更通用）；\n"
        "B）用一个中等模型 + 更好的数据与流程（更省钱，更可控）。\n"
        "\n"
        "规模定律给你的启发是：\n"
        "1）如果你只追求“更聪明”，确实可以堆资源；\n"
        "2）但产品里更常见的做法是：先找到“足够好”的体验门槛，再用工程手段降成本。\n"
        "\n"
        "例如：\n"
        "- 用更干净的业务知识库/FAQ（提升数据质量）\n"
        "- 用蒸馏把大模型的能力压到小模型（更便宜更快）\n"
        "- 用缓存/提示模板/工具调用把关键步骤固定住（更稳定）\n"
        "\n"
        "一句话：规模定律解释了“为什么大模型更强”，也提醒你“强到哪里才划算”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 5: Misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "误区 1：规模定律 = 只要堆 GPU 就一定行\n"
        "澄清：数据质量、模型结构、训练方法都很关键；只堆算力可能会“烧钱但不长脑”。\n"
        "\n"
        "误区 2：更大模型一定更好\n"
        "澄清：更大常常更强，但也更慢、更贵、更难部署；很多产品追求的是“性价比最优”。\n"
        "\n"
        "误区 3：规模定律意味着 AI 会无限变强\n"
        "澄清：现实中会遇到数据上限、算力成本、安全与对齐约束；而且边际收益会越来越小。\n"
        "\n"
        "误区 4：规模定律只适用于文本大模型\n"
        "澄清：多模态、视觉、语音等领域也常见类似趋势，但具体曲线与瓶颈可能不同。",
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
        "1）规模定律告诉你：数据/算力/参数做大，能力通常会按规律提升。\n"
        "2）但越到后面越难：提升会越来越慢（边际收益递减）。\n"
        "3）做产品时，关键往往不是“最强”，而是“足够好 + 成本可控”。",
        style.margin_x,
        y,
        max_w,
        style.accent2,
        line_gap=10,
    )

    y += 8
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）用“办学校/刷题”的类比解释：参数、算力、数据分别像什么？为什么要平衡？\n"
        "2）为什么说“越到后面提升越慢”？请用一个你熟悉的学习/训练例子解释。\n"
        "3）如果你要做一个 AI 客服产品，你会优先选择“更大模型”还是“中等模型+更好数据/流程”？为什么？",
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

    # Keep the PDF under Gmail's 25MB attachment limit:
    # - downscale pages before export
    # - use an indexed palette (avoids JPEG dependency in this environment)
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

