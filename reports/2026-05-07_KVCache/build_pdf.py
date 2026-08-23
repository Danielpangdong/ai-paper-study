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
    fig_analogy = base / "kv_cache_notebook.png"
    fig_flow = base / "kv_cache_prefill_decode.png"
    out_pdf = base / "2026-05-07_KV Cache（键值缓存）.pdf"

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
        "2. 直观类比：做笔记",
        "3. 工作原理：Prefill / Decode",
        "4. 关键术语解释",
        "5. 一个真实应用案例",
        "6. 常见误区",
        "7. 3句话总结",
        "8. 3个复习问题",
    ]

    # Page 1: Title + importance + image 1
    page, draw, y = new_page()
    header_h = 230
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "AI每日深度科普", font=kicker_font, fill=style.muted)
    draw.text((style.margin_x + 22, y + 58), "KV Cache（键值缓存）：为什么它让大模型回答更快？", font=title_font, fill=style.ink)
    meta = "日期：2026-05-07    难度：高中友好    关键词：推理加速 / 成本 / 显存"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 124)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：KV Cache 的本质，是让模型在生成时“复用已读内容的注意力笔记”，避免反复重算。",
        font=body_font,
        fill=style.accent2,
    )
    y += 150

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "你在用 ChatGPT 或其他大模型时，会发现两件事：\n"
        "（1）它是“一个字一个字”往外吐的；\n"
        "（2）同样一段对话，越聊越长，它可能变慢、也更贵。\n"
        "\n"
        "原因之一在于：每生成一个新字，模型都要做注意力计算。\n"
        "如果每次都从头把之前所有内容重新算一遍，就像写作文时每写一句都要重读前面十页——很浪费。\n"
        "\n"
        "KV Cache 就是为了解决这个“重复劳动”的：\n"
        "把已经算过的关键中间结果存起来，下一个字继续用。\n"
        "所以它能显著降低推理延迟、减少算力成本，是部署大模型产品的关键工程手段。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（自动生成）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "\n".join(toc_items),
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    hint = "阅读顺序建议：先看类比，再看原理图，再回到误区与总结。"
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
        "把大模型想成一个正在读长文章、并边读边写“摘抄笔记”的同学：\n"
        "第一次读到前半段时，他会把每一段的关键点（用于后面理解的线索）记在本子上。\n"
        "后面写作文时，他不需要每次都回去重读前半段，只要翻笔记本，就能快速接上思路。\n"
        "\n"
        "KV Cache 就是这个“笔记本”。\n"
        "它缓存的是注意力里用于“回忆上下文”的 Key/Value，而不是最终的回答内容。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 14
    y = paste_image_fit(
        page,
        fig_analogy,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=920,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：用“做笔记”理解 KV Cache：减少重复回头读。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 4: How it works + fig2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（图2）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "理解 KV Cache 不需要公式，只要抓住两件事：\n"
        "（1）生成是“逐字”的：第1个字、第2个字……；\n"
        "（2）注意力要“回看”历史：新字要去看之前的内容。\n"
        "\n"
        "KV Cache 把“历史部分的注意力中间结果”保存下来：\n"
        "第一次读提示（Prefill）时建立缓存；后续逐字生成（Decode）时复用缓存，\n"
        "每一步只需要处理“新来的这一个字”，避免每次都把历史重算一遍。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(
        page,
        fig_flow,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=980,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：Prefill/Decode 两阶段与信息流：缓存 K/V 来加速推理。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 5: Terms + case + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("推理（Inference）", "专业：模型训练好后，用它来生成答案的过程。白话：真正“上场做题/聊天”。"),
        ("注意力（Attention）", "专业：新信息与历史信息做关联的计算。白话：像你读句子时在“抓重点”。"),
        ("Key/Value（K/V）", "专业：注意力里用于匹配与取信息的两类向量。白话：像“索引卡”和“笔记内容”。"),
        ("Prefill（读提示）", "专业：把用户提示一次性喂进模型。白话：先把题干完整读一遍。"),
        ("Decode（逐字生成）", "专业：每次生成一个 token 并继续生成。白话：一个字一个字往外写。"),
        ("上下文窗口（Context Window）", "专业：模型一次能“看见”的最大长度。白话：它能同时摊开在桌上的“纸张大小”。"),
        ("显存/内存占用", "专业：缓存会占用 GPU/CPU 内存。白话：笔记本越厚，占地方越大。"),
    ]
    max_w = style.page_w - style.margin_x * 2
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 320, y, max_w - 320, style.muted, line_gap=10)
        y += 6

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "“AI客服长对话”\n"
        "客服场景经常要和用户来回聊几十轮：订单号、地址、诉求、历史处理记录……都在对话里。\n"
        "如果每回合生成回复都从头重算整段历史，会越来越慢、越来越贵。\n"
        "KV Cache 让系统在同一轮生成的过程中复用历史计算结果，\n"
        "配合对话截断/总结（控制上下文长度），可以显著提升响应速度并降低成本。\n"
        "所以你看到的“打字越来越快/越来越顺”，背后很多是工程优化在发力。",
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
        "1）误区：KV Cache 让模型更聪明。事实：它主要省计算，让回答更快更便宜。\n"
        "2）误区：缓存的是“最终答案”。事实：缓存的是注意力的中间结果（K/V）。\n"
        "3）误区：缓存越大越好。事实：缓存会占显存/内存；上下文越长，占用越大。\n"
        "4）误区：开了 KV Cache 就不会变慢。事实：长对话仍会带来更多读取与管理开销，\n"
        "   还需要配合总结、检索、截断等手段。",
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
        "1）KV Cache = “做笔记”：把历史注意力的关键中间结果存起来复用。\n"
        "2）它主要提升推理速度、降低成本，但会增加显存/内存占用。\n"
        "3）长对话要更稳：KV Cache + 控制上下文长度（总结/检索/截断）通常一起用。",
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
        "1）用你自己的话解释：为什么“逐字生成”会带来重复计算？\n"
        "2）KV Cache 缓存的是什么？为什么说它不等于“记住答案”？\n"
        "3）如果对话越来越长，你会怎么设计系统既快又稳？（提示：不仅仅靠 KV Cache）",
        style.margin_x,
        y,
        max_w,
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
