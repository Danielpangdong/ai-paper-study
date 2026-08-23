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

    fig_causes = base / "hallucination_causes_mitigations.png"
    fig_compare = base / "answering_modes_comparison.png"
    out_pdf = base / "2026-05-21_AI幻觉（Hallucination）.pdf"

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
        "AI 幻觉（Hallucination）：为什么它会“自信胡说”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-21    难度：高中友好    关键词：可靠性 / 证据链 / RAG / 校验"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 22

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 144)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：AI 幻觉的本质，是模型在“没有足够证据”时，仍然会用很像真的语言把答案补齐——"
        "它擅长把话说圆，但不保证每句话都可查证。",
        font=body_font,
        fill=style.accent2,
    )
    y += 170

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "如果你只把大模型当成“聊天工具”，幻觉只是尴尬；\n"
        "但一旦它进入工作流（写报告、做客服、查政策、给建议），幻觉就会变成风险。\n"
        "\n"
        "理解幻觉很重要，因为它决定了三件现实问题：\n"
        "1）你该把它当“会说话的助手”，还是当“可以直接采信的专家”？\n"
        "2）产品要不要接入外部资料、工具与校验？不接，哪里会翻车？\n"
        "3）普通人如何安全使用：哪些问题可以问，哪些必须带证据与核对？\n"
        "\n"
        "一句话：幻觉不是小毛病，它是 AI 走向“可用、可信、可规模化”的必修课。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC + analogy + figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（你将学到什么）", style.margin_x, y)
    toc_text = "\n".join([f"{i+1}. {t.split('.', 1)[1].strip()}" for i, t in enumerate(toc_items)])
    y = draw_paragraph(draw, body_font, toc_text, style.margin_x, y, max_w, style.ink, line_gap=10)

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把大模型想成一个“作文特别好”的同学：\n"
        "- 你给它一个题目，它很会写：语气像、逻辑像、结论像。\n"
        "- 但如果你让它写“某城市今天的最新政策”或“某个冷门数字”，\n"
        "  它可能会在没有资料的情况下，凭感觉把细节补齐。\n"
        "\n"
        "这就像：\n"
        "老师问你一个你不确定的知识点，你为了不冷场，硬把话说圆——\n"
        "听起来很像真的，但其实缺证据。\n"
        "\n"
        "所以，降低幻觉的关键不是“让它更会说”，而是给它更完整的证据链：\n"
        "让它先查资料、能做计算、再按步骤解释，并且能被核对。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = draw_section_title(draw, style, h2_font, "图解：幻觉从哪里来？", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_causes,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=560,
        border=True,
        style=style,
    )
    pages.append(page)

    # Page 3: mechanism + terms + compare figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "一个更准确的理解是：\n"
        "大模型的“默认技能”是——在当前上下文里，生成最像人类文本的下一句话。\n"
        "它并不是天生就会：\n"
        "（1）主动去查外部资料；（2）为每一句话附上证据；（3）在不确定时自动说“我不知道”。\n"
        "\n"
        "所以当你问：\n"
        "- 需要最新事实（比如“2026 年某项政策”）\n"
        "- 需要精确数字/引用（比如“某论文第几页写了什么”）\n"
        "- 或者上下文没给够\n"
        "它就可能用“写作能力”把空白补齐，于是出现幻觉。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）幻觉（Hallucination）\n"
        "   专业：模型生成了与事实不一致、或无法被证据支持的内容。\n"
        "   白话：它把“猜的”说得像“真的”。\n"
        "\n"
        "2）证据链\n"
        "   专业：回答所依据的可追溯资料、工具计算结果与推理步骤。\n"
        "   白话：你能说清“我凭什么这么说”。\n"
        "\n"
        "3）RAG（检索增强生成）\n"
        "   专业：先检索外部知识，再结合检索结果生成回答。\n"
        "   白话：开卷考试：先翻书再作答。\n"
        "\n"
        "4）校验（Verification）\n"
        "   专业：用规则、工具或多源对照去验证答案关键点。\n"
        "   白话：写完先自查/互查，别把“差不多”当“正确”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 6
    y = draw_section_title(draw, style, h2_font, "图解：三种回答方式对比", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_compare,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=520,
        border=True,
        style=style,
    )
    pages.append(page)

    # Page 4: application + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "场景：公司里做一个“政策与运费规则问答”的 AI 助手。\n"
        "\n"
        "如果你只让模型直接回答：\n"
        "- 它可能把旧政策当新政策；\n"
        "- 把不同地区规则混在一起；\n"
        "- 把“看起来合理”的数字补出来。\n"
        "\n"
        "更稳的做法是把它变成“有证据的助手”：\n"
        "1）先检索：在公司知识库/公告/FAQ 里找到相关条款（RAG）。\n"
        "2）再工具：对价格/时效做计算，或按规则引擎核对。\n"
        "3）再输出：要求它引用来源、按步骤解释，并标注不确定点。\n"
        "\n"
        "结果：回答速度可能慢一点，但稳定性和可追责性会高很多。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "误区 1：幻觉 = 模型“在撒谎”\n"
        "澄清：它通常不是故意骗你，而是“缺证据也要把话说圆”的生成副作用。\n"
        "\n"
        "误区 2：更大模型就不会幻觉\n"
        "澄清：更大常常更稳，但在需要最新事实、精确数字、或上下文缺失时仍会出错。\n"
        "\n"
        "误区 3：接了 RAG 就彻底解决\n"
        "澄清：RAG 只是补资料；检索质量、引用方式、以及是否做校验，仍决定可靠性。\n"
        "\n"
        "误区 4：只要回答很像“专家语气”就可信\n"
        "澄清：可信的标志不是语气，而是：能给证据、能被核对、能承认不确定。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）幻觉的本质：没证据也要把话说圆，听起来像真的但可能不真实。\n"
        "2）降低幻觉的关键：补“证据链”——检索、工具、结构化输出与校验。\n"
        "3）使用原则：越高风险的场景（钱/健康/政策/合同），越要可查证与多重核对。",
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
        "1）为什么说大模型更像“续写高手”而不是“事实查询器”？请用一个生活例子解释。\n"
        "2）同样一个问题：纯模型回答 vs RAG vs 工具+校验，幻觉风险为何不同？\n"
        "3）如果你要做一个面向客户的 AI 助手，你会怎样设计“证据链”来降低幻觉？请给出 2–3 个具体步骤。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：强调直觉、类比与可落地的安全使用方法。",
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

