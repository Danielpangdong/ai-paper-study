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
    fig1 = base / "attention_highlight.png"
    fig2 = base / "self_attention_qkv_multihead.png"
    out_pdf = base / "2026-05-13_Attention（注意力机制）.pdf"

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
        "2. 直观类比：荧光笔“动态划重点”（图1）",
        "3. 工作原理：Self-Attention 的 6 步（图2）",
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
        "Attention（注意力机制）：为什么 AI 终于学会了“抓重点”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-13    难度：高中友好    关键词：抓重点 / 指代 / 长文理解 / Transformer"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 124)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：注意力机制的本质，是让模型在“当下这个问题”里，动态判断哪些词最重要，然后把重要信息加权汇总。",
        font=body_font,
        fill=style.accent2,
    )
    y += 150

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "如果你只记住一句：大模型之所以像“会读书”，关键不是背了多少，而是会不会抓重点。\n"
        "\n"
        "注意力机制解决的是一个很现实的问题：\n"
        "一句话里，关键线索可能隔得很远——但你仍然要把它们联系起来。\n"
        "比如：\n"
        "“我把书放在桌子上，因为它很稳。”\n"
        "这里的“它”指什么？人会自然想到“桌子”。传统模型很容易在长句/长文里丢线索。\n"
        "\n"
        "注意力机制带来的变化，是把‘顺序挨个读’升级成‘边读边回头对照’：\n"
        "模型会给每个词打“相关性分数”，谁更关键就看得更重。\n"
        "\n"
        "现实影响非常大：\n"
        "（1）更擅长长文摘要与问答；（2）更擅长指代与关系理解；（3）它是 Transformer 的核心零件，后面的 MoE、KV Cache、长上下文优化都绕不开它。",
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
    hint = "阅读顺序建议：先看图1建立直觉 → 再看图2理解怎么“算” → 最后看误区，避免把注意力当成玄学。"
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
        "把读文章想成：老师批改作文。\n"
        "同一篇文章，老师回答不同问题时，划重点的位置也不同：\n"
        "问“主旨是什么”，就圈主题句；问“它指的是谁”，就盯指代词附近的线索。\n"
        "\n"
        "注意力机制就像一支“会变的荧光笔”：\n"
        "它不是把所有字都一视同仁，而是给每个词一个分数——\n"
        "分数越高，代表它对当前理解/生成越重要。\n"
        "\n"
        "关键直觉：注意力不是‘记住更多’，而是‘在当下更会挑重点’。\n"
        "当句子变长、线索分散时，这个能力决定了模型是否还能把意思串起来。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 14
    y = paste_image_fit(
        page,
        fig1,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=930,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：同一句话里，不同词对“当前词”的重要性不同；注意力会动态给权重。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 4: How it works + fig2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（图2）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把 Self-Attention 想成“在一堆便签里找最相关的几张，再汇总成新笔记”。\n"
        "用 6 句人话讲清它怎么做：\n"
        "（1）每个词先变成向量（Embedding）；\n"
        "（2）每个词都生成三份小便签：Q（我在找什么）、K（我是什么）、V（我带着什么信息）；\n"
        "（3）拿当前词的 Q 去和所有词的 K 做相似度打分（谁更相关谁更高）；\n"
        "（4）把分数变成“权重”（softmax：让它们加起来等于 1）；\n"
        "（5）用这些权重把所有词的 V 做加权汇总，得到“更懂关系”的新向量；\n"
        "（6）多头注意力=多种视角同时打分再合并：有人看语法，有人看指代，有人看主题。\n"
        "\n"
        "这一套算完，模型就不再只看眼前几个字，而是能在整段话里‘全局对照’。",
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
    draw.text((style.margin_x, y + 8), "图2：Q/K/V + 多头：本质是“相关性加权汇总”，用多种视角并行找关系。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 5: Terms + case + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("Attention（注意力）", "专业：对输入各部分分配权重并汇总。白话：给每个词打相关性分数，再按分数加权。"),
        ("Self-Attention（自注意力）", "专业：同一序列内部互相计算注意力。白话：一句话里的词彼此“互相对照”。"),
        ("Cross-Attention（交叉注意力）", "专业：在两段序列之间计算注意力。白话：一边是‘问题’，一边是‘资料’，让问题去找资料里关键句。"),
        ("Q / K / V", "专业：Query/Key/Value 三种投影。白话：Q=我想找什么；K=我是什么标签；V=我带的内容。"),
        ("权重（Attention Weight）", "专业：softmax 后的归一化分数。白话：每个词被‘看重’的比例，合起来等于 100%。"),
        ("多头注意力", "专业：并行计算多组注意力再合并。白话：像 4 位老师从不同角度划重点，最后拼成更完整的结论。"),
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
        "“AI 法务助手怎么从一份 50 页合同里，直接找到你关心的那一条？”\n"
        "你问：‘如果对方延迟交付，我能怎么索赔？’\n"
        "模型需要在长合同里把‘延迟交付’、‘违约责任’、‘赔付上限’这些条款联系起来。\n"
        "\n"
        "注意力机制的作用是：\n"
        "当模型在理解你的问题或生成答案时，会把注意力更多放在相关条款附近的关键词和句子上，\n"
        "而不是平均看待每一页。\n"
        "\n"
        "在工程上，这也是为什么 RAG（把相关条款检索出来）+ 注意力（在检索结果里抓重点）通常要配套使用：\n"
        "RAG 决定‘把哪几页拿给模型’，注意力决定‘在这些页里看哪里更关键’。",
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
        "1）误区：注意力=记忆。事实：注意力是‘当下的相关性’，不等于长期存储。\n"
        "2）误区：注意力权重=解释原因。事实：它能提供线索，但不等同于“可解释性证明”。\n"
        "3）误区：注意力越分散越差。事实：有时需要综合多处信息（例如总结全文），分散并不一定是坏事。\n"
        "4）误区：头数越多越强。事实：多头是工具；是否更强取决于训练、数据与算力预算。\n"
        "5）误区：有注意力就能处理无限长文本。事实：仍受上下文窗口限制；长文往往还需要检索/摘要/分段。",
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
        "1）注意力机制让模型在当下任务里“抓重点”：给各词打相关性分数并加权汇总。\n"
        "2）Self-Attention 让句子内部词与词互相对照，解决长距离依赖与指代理解。\n"
        "3）它是 Transformer 的核心零件：长文问答、摘要、RAG 阅读、推理加速等能力都离不开它。",
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
        "1）用“荧光笔动态划重点”的类比解释：为什么注意力不是记忆？\n"
        "2）把 Q/K/V 翻译成一句人话：分别代表什么？它们为什么要分开？\n"
        "3）在“RAG + 注意力”的组合里：RAG 解决什么问题？注意力又解决什么问题？请用合同例子回答。",
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

