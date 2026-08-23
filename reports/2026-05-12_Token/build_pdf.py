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
    fig_tokens = base / "tokenization_example.png"
    fig_budget = base / "context_window_budget.png"
    out_pdf = base / "2026-05-12_Token（词元）.pdf"

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
        "2. 直观类比：把文本装进“标准周转箱”",
        "3. 工作原理：Tokenizer 怎么把字变成 Token",
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
    draw.text((style.margin_x + 22, y + 58), "Token（词元）：AI 读文本为什么要“切片”？", font=title_font, fill=style.ink)
    meta = "日期：2026-05-12    难度：高中友好    关键词：分词 / 上下文 / 计费 / 生成"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 124)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：Token 是大模型处理文字的“最小小票单位”——先把文本切成小块，模型才能在有限的上下文里一步步算下去。",
        font=body_font,
        fill=style.accent2,
    )
    y += 150

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "你和大模型的所有互动，都绕不开 Token：\n"
        "（1）为什么“同样一段话”，有时会被提示“超出上下文”？——因为 Token 塞满了；\n"
        "（2）为什么一句话换个说法，价格和速度会变？——因为 Token 数量变了；\n"
        "（3）为什么模型输出是一字一字（更准确说：一小块一小块）吐出来？——它是按 Token 逐步预测的。\n"
        "\n"
        "把 Token 想成 AI 世界的“统一计量单位”，就像快递行业必须有：\n"
        "统一的面单、统一的分拣规则、统一的计费口径。\n"
        "你理解了 Token，就能把很多“AI 玄学问题”变成可解释、可调参的工程问题：\n"
        "到底是写得太长？历史对话太多？检索材料塞太满？还是输出上限太低？\n"
        "\n"
        "一句话：Token 决定了三件现实大事——能装多少（上下文窗口）、要花多少（成本）、跑多快（速度）。",
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
    hint = "阅读顺序建议：先看图1理解“怎么切” → 再看图2理解“怎么被上下文限制” → 最后读误区避坑。"
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
        "把一段文字想成“散装货”，模型没法直接处理无限形状的散件。\n"
        "Tokenizer（分词器）做的事，像分拣中心把散件装进“标准周转箱”：\n"
        "每个箱子都有编号（Token ID），系统只认编号，不直接认原始文字。\n"
        "\n"
        "更妙的是：装箱规则不是“一个字一个箱”。\n"
        "常见组合（比如‘宫保’‘鸡丁’、‘北京’、‘ing’）会被当成一个更大的箱子，\n"
        "这样箱子更少，运输更省（Token 更少 → 更省上下文、更省成本、更快）。\n"
        "\n"
        "关键直觉：Token 不是“词”，也不是“字”，而是模型世界里的一块“可计算积木”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 14
    y = paste_image_fit(
        page,
        fig_tokens,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=950,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：同一句话会被切成若干 Token（小块），每块有对应的 Token ID。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 4: How it works + fig2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（图2）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "用 6 句人话讲清 Token 如何参与大模型工作：\n"
        "（1）你输入文字；\n"
        "（2）Tokenizer 按规则切成 Token，并变成一串编号（Token ID）；\n"
        "（3）模型把这些编号查表（Embedding），变成一排可计算的向量；\n"
        "（4）Transformer 读完这些向量后，预测“下一个最可能出现的 Token”；\n"
        "（5）把预测出来的 Token 追加到尾部，再预测下一个……循环往复；\n"
        "（6）直到达到停止条件（比如遇到结束符，或输出 Token 上限）。\n"
        "\n"
        "这也解释了：\n"
        "为什么输出是“流式”的（一步步预测）；为什么对话会忘（上下文窗口塞满会截断）；\n"
        "以及为什么成本=你输入多少 Token + 模型输出多少 Token（都要算）。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(
        page,
        fig_budget,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=980,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：上下文窗口像“固定容量的行李箱”：装了历史就少了输出空间。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 5: Terms + case + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("Token（词元）", "专业：模型处理的离散单位。白话：AI 读写时的一块块“小积木/小票”。"),
        ("Tokenizer（分词器）", "专业：把文本编码为 Token ID 的程序。白话：把散装文字装箱并贴编号的工厂。"),
        ("Token ID", "专业：每个 Token 对应的整数编号。白话：箱子的条码编号。"),
        ("BPE/合并规则", "专业：常见的子词切分与合并策略之一。白话：把常见组合直接打包成“大箱”。"),
        ("上下文窗口", "专业：模型一次最多能处理的 Token 总数。白话：一只固定容量的行李箱。"),
        ("输出上限", "专业：一次生成最多输出多少 Token。白话：这次最多说多少“积木块”。"),
        ("流式输出", "专业：边生成边返回。白话：想到一点说一点，因为它本来就是一步步预测。"),
        ("计费/成本", "专业：多数 API 按输入/输出 Token 计费。白话：你让它“看”和“说”都要算工时。"),
    ]
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 330, y, max_w - 330, style.muted, line_gap=10)
        y += 6

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "“AI 客服为什么越聊越慢，还开始忘事？”\n"
        "一个电商/快递客服机器人，刚开始回答很快；聊到第 30 轮后，突然变慢、变贵，甚至开始‘记不住前文’。\n"
        "\n"
        "典型原因是 Token 爆了：\n"
        "1）历史对话被全部塞回去（history tokens 变得很大）；\n"
        "2）还同时塞了大量商品/订单/政策资料（RAG 证据 tokens 很大）；\n"
        "3）为了更礼貌，模型被要求输出很长（output tokens 很大）。\n"
        "\n"
        "解决思路（可落地）：\n"
        "（1）把历史对话压成“要点摘要”再塞回去（省 Token）；\n"
        "（2）RAG 只取最相关的 3~5 段，且每段限制长度（控 Token）；\n"
        "（3）对输出设“短答优先”，必要时再点开详解（省 Token + 省用户时间）。\n"
        "\n"
        "这类问题表面像‘模型变笨’，本质往往是 Token 预算管理没做好。",
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
        "1）误区：Token=字数。事实：不等；同样 1000 字，不同写法 Token 可能差很多。\n"
        "2）误区：Token=词。事实：中文常见是 1~2 个字一块，英文常见是子词；‘宫保鸡丁’可能是多块也可能合成一块。\n"
        "3）误区：上下文窗口=永久记忆。事实：它更像‘本次对话的行李箱’，装不下就要截断或改成摘要。\n"
        "4）误区：把资料塞得越多越好。事实：塞太多会挤掉关键问题与输出空间，反而更容易答非所问。\n"
        "5）误区：流式输出说明它在“思考得更深”。事实：更多是生成方式；深不深取决于信息、指令与推理预算。",
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
        "1）Token 是大模型读写文字的最小单位：先切块、编号、再计算。\n"
        "2）上下文窗口是 Token 容量上限：历史越多，留给输出的空间越少。\n"
        "3）很多“变慢/变贵/忘事”的问题，本质是 Token 预算没管理好：该摘要就摘要，该裁剪就裁剪。",
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
        "1）用“标准周转箱”类比解释：为什么 Token 不是‘字’也不是‘词’？\n"
        "2）为什么‘把更多资料塞给模型’有时会让回答更差？请用 Token 预算解释。\n"
        "3）如果你要做一个 50 轮对话的 AI 客服，你会用哪两种办法控制 Token 成本并避免忘事？",
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

