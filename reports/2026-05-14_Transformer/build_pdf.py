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
    fig1 = base / "transformer_meeting_analogy.png"
    fig2 = base / "transformer_overview.png"
    out_pdf = base / "2026-05-14_Transformer.pdf"

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
        "2. 直观类比：开会写纪要（图1）",
        "3. 工作原理：Transformer 的“流水线”（图2）",
        "4. 关键术语解释",
        "5. 一个真实应用案例",
        "6. 常见误区",
        "7. 3句话总结",
        "8. 3个复习问题",
    ]

    max_w = style.page_w - style.margin_x * 2

    # Page 1: Title + importance
    page, draw, y = new_page()
    header_h = 242
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "AI每日深度科普", font=kicker_font, fill=style.muted)
    draw.text(
        (style.margin_x + 22, y + 58),
        "Transformer：为什么它成了大模型的“万能引擎”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-14    难度：高中友好    关键词：全局对照 / 抓重点 / 堆叠 / 生成下一个词"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 136)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：Transformer 把“读一句话”变成“随时回头对照全句抓重点 + 把重点加工成新表达”，\n"
        "再把这个过程堆叠很多层，于是就能从大量文本里学会理解与生成。",
        font=body_font,
        fill=style.accent2,
    )
    y += 166

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "如果把大模型比作“会写作的学生”，Transformer 就是它的写作引擎。\n"
        "\n"
        "它解决了一个非常现实的问题：\n"
        "当信息变多、句子变长、关系变复杂时——你怎么在一堆内容里快速找到关键关系，并写出连贯的下一句？\n"
        "\n"
        "在 Transformer 之前，很多模型更像“按顺序听讲”的学生：\n"
        "前面听过什么，会逐步淡掉；越长的文章越容易丢线索。\n"
        "Transformer 的升级点在于：它允许模型在同一段文字里‘全局对照’——\n"
        "需要解释“它”指代谁，就回头看相关词；需要续写下一句，就看哪些信息最该被带上。\n"
        "\n"
        "现实影响：\n"
        "（1）它让 ChatGPT 这类生成模型能稳定写长文、做总结与对话；\n"
        "（2）它也是多模态、代码模型、搜索增强（RAG）等系统的核心骨架；\n"
        "（3）你学会 Transformer，就等于抓住了现代 AI 的“通用发动机”是怎么工作的。",
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
    hint = "阅读顺序建议：先看图1建立直觉 → 再看图2理解流水线结构 → 最后看误区，避免把 Transformer 当成玄学名词。"
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
        "把 Transformer 想成“开会写纪要”。\n"
        "\n"
        "会议上很多人同时说话：有人讲背景，有人提风险，有人给截止时间。\n"
        "你要写出一份靠谱纪要，关键不是把每句话逐字抄下来，而是：\n"
        "当你要写某一条结论时，立刻判断‘现在最相关的是谁在说什么’，把这些关键句合成更清晰的一句。\n"
        "\n"
        "Transformer 的核心直觉就是三步：\n"
        "（1）注意力：先在全场发言里“抓重点”（谁跟当前任务最相关）；\n"
        "（2）汇总：把重点按权重合成一句更有用的新表述；\n"
        "（3）MLP：再把这句“加工润色”，变成更适合继续写下去的表示。\n"
        "\n"
        "堆叠很多层，就像“反复归纳 → 再归纳”：越往后，能提炼出越抽象、更像‘理解’的东西。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 12
    y = paste_image_fit(
        page,
        fig1,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=940,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：开会写纪要的类比：注意力抓重点，汇总形成结论，MLP把结论加工得更清晰。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 4: How it works + fig2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（图2）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "用一条“流水线”把 Transformer 讲明白（以 GPT 这种只用解码器的版本为例）：\n"
        "\n"
        "（1）切片：把文本切成 Token（词元），像把一句话切成小积木；\n"
        "（2）上坐标：每个 Token 变成 Embedding（向量），再加上位置编码（告诉它顺序）；\n"
        "（3）进工位：进入第 1 层 Transformer Block：\n"
        "    - 多头自注意力：在整段里找“跟当前 Token 最相关的线索”，加权汇总；\n"
        "    - MLP：把汇总后的信息再加工组合，变成更适合表达的特征；\n"
        "    - 残差 + LayerNorm：像‘保留原稿 + 统一格式’，让训练更稳定；\n"
        "（4）反复加工：把第 1 层的输出当作第 2 层输入……堆叠 N 层；\n"
        "（5）输出选择：最后输出“下一个 Token 的概率”，选择一个继续写下去。\n"
        "\n"
        "注意：它不是靠规则写作，而是从海量文本里学到‘什么情况下下一句最可能怎么说’。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(
        page,
        fig2,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=980,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：Transformer 流水线：Embedding+位置 → 多层Block（注意力+MLP） → 下一个词概率。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 5: Terms + case + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("Transformer", "专业：基于注意力的序列建模架构。白话：能在整段话里随时对照抓重点的“写作引擎”。"),
        ("Token（词元）", "专业：模型处理文本的最小单位。白话：把句子切成小积木（可能是字、词或词的一部分）。"),
        ("Embedding（向量表征）", "专业：把离散符号映射到连续向量空间。白话：把‘词的意思’变成一串数字坐标。"),
        ("位置编码", "专业：为序列位置提供可区分的信息。白话：告诉模型“第几个词”，不然顺序会乱。"),
        ("自注意力（Self-Attention）", "专业：序列内部各位置相互计算权重并汇总。白话：一句话里的词彼此回头对照，谁重要就多看。"),
        ("MLP（前馈网络）", "专业：逐位置的非线性变换层。白话：把抓到的重点再‘加工组合’，变成更好用的表达。"),
        ("残差连接", "专业：把输入直接加回输出以稳定训练。白话：像保留原稿，再在上面做增补，防止越改越跑偏。"),
        ("LayerNorm", "专业：对特征做归一化以稳定分布。白话：像统一格式/分布，让每层输出别忽大忽小。"),
    ]
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 370, y, max_w - 370, style.muted, line_gap=10)
        y += 6

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "“AI 写邮件/写周报，为什么能看起来很像人？”\n"
        "\n"
        "假设你给模型输入：\n"
        "‘请帮我给客户写一封邮件：解释我们延迟发货的原因，并提出补偿方案。语气要诚恳。’\n"
        "\n"
        "Transformer 在生成每一个词的时候，都在做同一件事：\n"
        "它会回头看输入里哪些词最重要（延迟、原因、补偿、语气），\n"
        "再把这些信息汇总加工，决定下一词写‘非常抱歉’还是‘感谢理解’，决定先解释原因还是先给方案。\n"
        "\n"
        "这就是为什么它能“写得连贯”：不是背模板，而是每一步都能把关键约束重新对齐一次。",
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
        "1）误区：Transformer=注意力。事实：注意力是核心零件，但还需要 MLP、残差、归一化与层堆叠。\n"
        "2）误区：它‘理解’了所以一定正确。事实：它学的是“像人一样写下一句”的统计规律，会出现幻觉与自信胡说。\n"
        "3）误区：层数越多就一定越好。事实：要看数据、训练方法与算力预算；过深也可能训练不稳或性价比不高。\n"
        "4）误区：有 Transformer 就能记住所有上下文。事实：仍受上下文窗口限制；长文常要配合检索/分段/摘要。\n"
        "5）误区：生成就是抄袭训练数据。事实：更像‘学会写作风格与规律’；是否复现原文取决于数据、提示与温度等设置。",
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
        "1）Transformer 的关键能力：在整段文字里随时回头对照，抓住与当前任务最相关的信息。\n"
        "2）它的基本积木块=注意力（看哪里）+ MLP（怎么加工）+ 稳定训练的残差与归一化。\n"
        "3）把积木块堆叠很多层，再用“预测下一个词”训练，就能学出对话、写作、总结与代码生成等能力。",
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
        "1）用“开会写纪要”的类比解释：为什么注意力能让模型更会抓重点？\n"
        "2）为什么 Transformer 需要“位置编码”？如果没有它会发生什么？\n"
        "3）请用“写客户道歉邮件”的例子说明：模型生成每个词时，为什么要反复回头看输入？",
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

