from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 120
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
    fig_seats = base / "positional_encoding_seats.png"
    fig_pipeline = base / "positional_encoding_pipeline.png"
    out_pdf = base / "2026-05-16_位置编码（Positional Encoding）.pdf"

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
        "2. 直观类比：一句话 + 座位号",
        "3. 工作原理：位置编码怎么“喂给”Transformer",
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
    draw.text(
        (style.margin_x + 22, y + 58),
        "位置编码（Positional Encoding）：让AI看懂“顺序”的小心机",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-16    难度：高中友好    关键词：顺序 / 句子 / Transformer / 注意力"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 124)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：位置编码的本质，是给每个Token贴一张“第几位”的小标签，让模型不仅知道“有什么词”，还知道“它们按什么顺序出现”。",
        font=body_font,
        fill=style.accent2,
    )
    y += 150

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "你可能直觉觉得：句子的顺序当然重要。\n"
        "但 Transformer 的注意力机制本身更像“把一桌上的词都摆出来，让它们互相打分谁更相关”。\n"
        "如果不给“顺序提示”，模型会遇到一个致命问题：\n"
        "“我知道这些词都在这儿，但我不确定它们的先后。”\n"
        "\n"
        "这会直接影响三类现实任务：\n"
        "（1）长文理解：前后因果、转折、时间线，需要顺序；\n"
        "（2）代码与公式：一位错了就全错；\n"
        "（3）对话与指令：‘先做A再做B’，顺序就是规则。\n"
        "\n"
        "所以位置编码不是“学术装饰”，它决定了：\n"
        "Transformer 能不能像人一样把一句话按顺序读懂；也决定了长上下文里信息会不会‘串台’。",
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
    y += 26
    draw.rounded_rectangle(
        (style.margin_x, y, style.page_w - style.margin_x, y + 92),
        radius=20,
        outline=style.line,
        width=3,
        fill=(245, 250, 255),
    )
    draw.text(
        (style.margin_x + 22, y + 20),
        "阅读建议：先看“座位号类比”建立直觉 → 再看“管道图”理解怎么进入模型 → 最后看误区避坑。",
        font=body_font,
        fill=style.ink,
    )
    pages.append(page)

    # Page 3: Analogy + figure 1
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个直观类比：一句话 + 座位号", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把一句话想成“观众入场”。\n"
        "词是人，顺序是座位号。\n"
        "\n"
        "如果你只知道“来了哪些人”，但不知道他们坐在哪一排哪一座，\n"
        "你就很难回答：谁坐在谁前面？谁挨着谁？哪个人先出场？\n"
        "\n"
        "同理：\n"
        "‘狗 咬 人’和‘人 咬 狗’用的是同一批词，但顺序完全不同，意思天差地别。\n"
        "\n"
        "位置编码就是给每个 Token 补上一张“座位号”小票：\n"
        "第1位、第2位、第3位……\n"
        "有了它，注意力机制才能在‘相关性’之外，把‘先后关系’也纳入判断。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(page, fig_seats, style.margin_x, y, max_w, 720, border=True, style=style)
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "图1：没有“座位号”，只剩一堆词；有了“座位号”，顺序就能被计算。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 4: How it works + figure 2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理：位置编码怎么“喂给”Transformer", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "用最工程化的一句话：\n"
        "模型真正吃进去的不是“词本身”，而是“词的向量表示（词的身份证）”。\n"
        "位置编码做的事，就是把“第几位”的信息也变成一个向量，合到每个词的身份证里。\n"
        "\n"
        "你可以把它理解成：\n"
        "每个 Token 原本是一张“人脸照”（表示它是谁），\n"
        "位置编码再贴一张“座位号贴纸”（表示它在哪儿）。\n"
        "两张贴在一起，模型就能同时看见“是谁 + 在哪里”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(page, fig_pipeline, style.margin_x, y, max_w, 780, border=True, style=style)
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "图2：位置编码进入Transformer的一条“管道图”。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 5: Key terms
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "Token：\n"
        "专业：模型处理文本的离散单位。\n"
        "白话：把文字切成“可计数的小块”。\n"
        "\n"
        "Embedding（词向量/表征）：\n"
        "专业：把离散Token映射到连续向量空间的表示。\n"
        "白话：把“词/片段”变成一串数字坐标，方便计算相似与关联。\n"
        "\n"
        "Position / Positional Encoding（位置/位置编码）：\n"
        "专业：为序列中的每个位置提供可学习或固定的向量表示。\n"
        "白话：给每个Token贴“第几位”的标签，让顺序不丢。\n"
        "\n"
        "Self-Attention（自注意力）：\n"
        "专业：序列元素之间两两计算相关性并聚合信息。\n"
        "白话：一句话里，哪些词更该互相“多看一眼”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 6: Real-world case
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例：为什么它影响“指令执行”", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "场景：你让AI做一段操作——\n"
        "“先把表格按城市分组，再按金额从高到低排序，最后把前10名导出。”\n"
        "\n"
        "这类指令里最关键的信息不是‘有哪些词’，而是‘顺序与依赖关系’：\n"
        "先分组→再排序→最后导出。\n"
        "\n"
        "如果模型对顺序理解弱，常见结果是：\n"
        "（1）把顺序做反；（2）漏掉中间一步；（3）把“最后”当成“另外”。\n"
        "\n"
        "位置编码提供的“序列结构感”，会影响模型在注意力里如何把“先/再/最后”与对应动作绑定。\n"
        "在代码生成、长文摘要、会议纪要里，同样是这个逻辑：顺序对，结构才对。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 7: Misconceptions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "误区1：位置编码就是“告诉模型第1/2/3个词”。\n"
        "纠正：不是把数字当文本喂进去，而是把位置变成向量信号，和词向量合在一起被计算。\n"
        "\n"
        "误区2：有了位置编码，模型就一定不会搞错顺序。\n"
        "纠正：位置编码只是“提供线索”。长上下文里还会受上下文窗口、注意力分布、训练数据等影响。\n"
        "\n"
        "误区3：位置编码只有一种实现。\n"
        "纠正：有固定的（如正弦/余弦）、也有可学习的；还有相对位置编码等变体，目的都是让顺序可计算。\n"
        "\n"
        "误区4：位置编码是Transformer独有。\n"
        "纠正：凡是要处理序列、又想并行计算的模型，都需要某种“顺序注入”办法，只是名字不一定叫它。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 8: Summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）Transformer 的注意力擅长“看关联”，但不天然自带“看顺序”。\n"
        "2）位置编码通过给每个Token加“第几位”的向量标签，把顺序注入模型。\n"
        "3）顺序理解强不强，直接影响：长文结构、指令步骤、代码与公式的正确性。",
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
        "1）用“座位号”类比解释：为什么‘狗咬人’和‘人咬狗’需要位置编码才能区分？\n"
        "2）为什么说位置编码是给注意力机制补上‘顺序线索’，而不是替代注意力？\n"
        "3）当你让AI执行“先A再B最后C”的任务时，如果它常做反，你会如何用今天的概念解释原因？",
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
