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

    fig_pretrain_pipeline = base / "pretraining_pipeline.png"
    fig_three_stage = base / "pretrain_finetune_infer.png"
    out_pdf = base / "2026-05-26_预训练（Pre-training）.pdf"

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
        "预训练（Pre-training）：AI 为什么要先“读完半个互联网”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-26    难度：高中友好    关键词：自监督 / 下一词预测 / 数据 / 算力 / 规模定律"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 22

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 150)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 20),
        "核心一句话：预训练的本质，是让模型通过“海量文本的自我练习”学会语言与世界常识的统计规律，"
        "从而获得通用能力——之后再用微调把它变成更像“你的岗位助手”。",
        font=body_font,
        fill=style.accent2,
    )
    y += 176

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "你在用 ChatGPT 时，常会惊讶：\n"
        "- 它会写诗、会讲段子、会改作文、会写代码，像一个“懂很多的通才”。\n"
        "- 但你又没“逐条教过”它这些知识。\n"
        "\n"
        "答案大多来自同一件事：预训练（Pre-training）。\n"
        "预训练决定了一个模型的“底子”：\n"
        "• 见过多少类型的表达方式（小说、新闻、说明书、代码、对话）。\n"
        "• 是否形成了通用的语言能力（总结、改写、推理、举例、翻译）。\n"
        "• 是否能把很多知识点串起来（跨领域联想）。\n"
        "\n"
        "更现实的一点：\n"
        "- 预训练最烧钱：数据、GPU、时间都主要花在这里。\n"
        "- 预训练也最决定“上限”：底子好，微调和推理才更有发挥空间。\n"
        "\n"
        "一句话：预训练是大模型的“通识教育”，决定它先天能不能学得快、想得通、说得顺。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC + analogy + pipeline figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（你将学到什么）", style.margin_x, y)
    toc_text = "\n".join([f"{i+1}. {t.split('.', 1)[1].strip()}" for i, t in enumerate(toc_items)])
    y = draw_paragraph(draw, body_font, toc_text, style.margin_x, y, max_w, style.ink, line_gap=10)

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把模型想成一个要参加“语文 + 常识 + 逻辑综合考试”的学生。\n"
        "\n"
        "预训练就像它的“通识教育阶段”：\n"
        "1）它拿到了一座巨大的图书馆：小说、百科、论坛、教程、代码……什么都有。\n"
        "2）老师不给标准答案，只要求它做一种练习：\n"
        "   读到一句话的前半句，就猜“下一个词/下一个字”最可能是什么。\n"
        "3）它每天都在做这种练习：猜错就改，猜对就强化——久而久之，\n"
        "   它不但学会了语法和表达，还顺便学到了很多事实与常识之间的关联。\n"
        "\n"
        "为什么这种“猜下一个词”的练习会有效？\n"
        "因为想猜对，你必须理解上下文：\n"
        "- 这是在讲人、事、物的哪个部分？\n"
        "- 这句话接下来最合理的走向是什么？\n"
        "\n"
        "所以预训练不是“背答案”，更像“通过大量阅读形成语感与常识”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = draw_section_title(draw, style, h2_font, "图解：预训练在做什么？", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_pretrain_pipeline,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=560,
        border=True,
        style=style,
    )
    pages.append(page)

    # Page 3: mechanism + terms + PEFT figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "预训练最常见的训练目标，是“下一词预测”（也叫自回归语言建模）：\n"
        "给模型一段文本前缀，让它预测下一个 Token 的概率分布。\n"
        "\n"
        "你可以把它想成一个“超级强的自动补全”：\n"
        "1）输入：一段已经出现的文字（上下文）。\n"
        "2）模型输出：下一步最可能出现的词/字的概率表。\n"
        "3）训练时：把模型的预测与真实下一个词对比，错了就调整参数。\n"
        "\n"
        "为什么这能学到‘通用能力’？\n"
        "因为语言里藏着世界：\n"
        "- 要补全“他把冰淇淋放进____”，你得知道常识上应该是“冰箱”。\n"
        "- 要补全一段代码，你得隐约理解语法、变量与目的。\n"
        "\n"
        "预训练的工程要点通常是：\n"
        "• 数据：规模大，但更怕“脏、重复、毒、泄漏”。\n"
        "• 算力：训练越久、模型越大、数据越好，能力往往越强（但成本爆炸）。\n"
        "• 评估：必须用独立测试集/基准来确认能力提升，而不是只看训练损失。\n"
        "\n"
        "一句话：预训练是让模型先形成‘语言直觉’，再谈“专业技能”。",
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
        "• Self-supervised（自监督）\n"
        "  专业：用数据自身构造“题目与答案”（例如预测下一词）来训练模型。\n"
        "  白话：没有老师给标准答案，但你可以用‘原文’当答案做练习。\n"
        "\n"
        "• Next-token prediction（下一词预测）\n"
        "  专业：给定上下文，预测下一个 Token 的概率分布。\n"
        "  白话：像输入法一样做超强补全。\n"
        "\n"
        "• Dataset（训练语料）\n"
        "  专业：用于训练的文本/代码等数据集合。\n"
        "  白话：给学生看的教材和题库。\n"
        "\n"
        "• Compute（算力）\n"
        "  专业：训练所需的计算资源（GPU 时间、并行规模等）。\n"
        "  白话：练习量与练习速度。\n"
        "\n"
        "• Base Model（基座模型）\n"
        "  专业：完成预训练后得到的通用模型。\n"
        "  白话：通识教育毕业的‘通才’，还没做岗位培训。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 6
    y = draw_section_title(draw, style, h2_font, "图解：预训练-微调-推理三阶段", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_three_stage,
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
        "以 ChatGPT 的“通用对话能力”为例，它通常经历三个阶段：\n"
        "\n"
        "1）预训练：\n"
        "   模型在海量文本里练习‘下一词预测’，得到一个能读懂/会表达的基座模型。\n"
        "\n"
        "2）微调（尤其是指令微调）：\n"
        "   用高质量的人类示例告诉它：用户提出请求时，怎样回答更有帮助、更礼貌、更安全。\n"
        "\n"
        "3）推理：\n"
        "   真正上线服务时，它根据上下文一步步生成文字，并用采样/解码策略控制稳定性与风格。\n"
        "\n"
        "你会发现：\n"
        "- 预训练负责‘知识与语言底座’。\n"
        "- 微调负责‘更像一个好助手’。\n"
        "- 推理负责‘每一次具体输出’。",
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
        "误区 1：预训练 = 把互联网内容“背下来”\n"
        "澄清：它更像学语感与规律；确实可能记住一些片段，但能力主要来自统计模式的抽象。\n"
        "\n"
        "误区 2：预训练数据越大，模型就一定越好\n"
        "澄清：数据质量、去重、毒性、安全、版权与泄漏同样关键；“脏数据”会带来稳定坏习惯。\n"
        "\n"
        "误区 3：预训练好就够了，不需要微调\n"
        "澄清：预训练让它会说话，但不一定会按你的需求说话；要做任务对齐往往还要微调与评估。\n"
        "\n"
        "误区 4：预训练会自动得到‘可靠事实’\n"
        "澄清：预训练学到的是“常见说法的概率”，不等于“可验证的事实”；需要检索、证据和工具。",
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
        "1）预训练像通识教育：通过‘下一词预测’让模型形成语言与常识的通用底子。\n"
        "2）预训练最决定上限：数据与算力主要花在这里，底子好后续才更好用。\n"
        "3）预训练不是可靠事实保证：要变成好助手仍需微调、推理策略与证据链。",
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
        "1）为什么“猜下一个词”这种练习，能让模型学到很多通用能力？请用一个生活例子解释。\n"
        "2）预训练、微调、推理三者各自解决什么问题？分别对应‘通识教育/岗位培训/上岗回答’的哪一步？\n"
        "3）如果你发现一个模型说话很顺，但经常胡编细节，你会优先在哪个阶段补救？为什么？",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：强调直觉类比与三阶段全局视角。",
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
