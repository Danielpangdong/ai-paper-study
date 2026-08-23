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

    fig_pipeline = base / "fine_tuning_pipeline.png"
    fig_peft = base / "peft_lora_vs_full.png"
    out_pdf = base / "2026-05-22_Fine-tuning（微调）.pdf"

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
        "Fine-tuning（微调）：为什么它像给 AI 做“岗位培训”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-22    难度：高中友好    关键词：岗位培训 / 数据质量 / 过拟合 / LoRA"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 22

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 150)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 20),
        "核心一句话：微调的本质，是在“通用大模型”之上用少量高质量数据做定向训练，"
        "让它更贴合某一类任务——但它不是魔法，必须配合评估与安全边界。",
        font=body_font,
        fill=style.accent2,
    )
    y += 176

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "现实里，大模型常见的尴尬是：\n"
        "- 它“什么都懂一点”，但一到你的业务语气、规范格式、专业术语，就开始跑偏。\n"
        "- 你要它写得更像公司内部文档，它却像在写“网上通用答案”。\n"
        "\n"
        "微调之所以重要，是因为它回答了 AI 落地的三大问题：\n"
        "1）怎么让模型更懂你的“岗位”：客服、质检、法务摘要、运营文案、内部助手。\n"
        "2）怎么把“好用的提示词经验”固化成稳定能力：减少靠人手反复改 Prompt。\n"
        "3）怎么在成本与效果之间做工程权衡：不可能每次都用更大模型硬堆资源。\n"
        "\n"
        "一句话：微调是把“通用会说话”变成“特定任务好用、稳定、可规模化”的关键手段。",
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
        "把大模型想成一个“通识很强的新人”：\n"
        "- 它读过很多书，表达很好，但还不懂你们公司的岗位要求。\n"
        "- 你让它直接上岗，它会用“通用常识”回答，遇到公司术语、规则、口径就容易走样。\n"
        "\n"
        "微调就像“岗位培训 + 标准答案练习”：\n"
        "1）给它看一小批高质量范例：这个问题我们要怎么答、语气怎么拿捏、格式怎么写。\n"
        "2）反复练到形成习惯：下次看到相似问题，它自然就按你的风格与规则来。\n"
        "\n"
        "注意：培训最怕两件事——\n"
        "（1）教材质量差：错的范例会把新人教歪；\n"
        "（2）只背题不理解：遇到没见过的题就失灵。\n"
        "所以“数据质量 + 评估”比“数据数量”更重要。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = draw_section_title(draw, style, h2_font, "图解：从预训练到微调", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_pipeline,
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
        "一句话解释“微调在干什么”：\n"
        "它在悄悄调整模型内部的“习惯”，让模型在看到某类输入时，更倾向产出你想要的回答方式。\n"
        "\n"
        "微调通常分三步（更像工程流程，而不是玄学）：\n"
        "1）数据准备：把真实业务问题做成“输入 → 理想输出”的样本，并清洗错例与噪声。\n"
        "2）训练更新：让模型在这些样本上反复练习，逐步变成“更像标准答案的那种模型”。\n"
        "3）评估上线：用测试集与线上灰度去看：准确率是否上升？幻觉是否变多？敏感问题会不会更危险？\n"
        "\n"
        "很多团队会选择“参数高效微调（PEFT）”，比如 LoRA：\n"
        "- 不改动整套大模型主干，而是在少数位置加“小补丁”。\n"
        "- 这样训练更省、迭代更快，也更容易回滚（换回原模型或换一套补丁）。",
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
        "1）预训练（Pre-training）\n"
        "   专业：用海量通用数据训练出“通用语言能力”。\n"
        "   白话：先把“语文、常识、表达”打好底子。\n"
        "\n"
        "2）微调（Fine-tuning）\n"
        "   专业：在特定数据上继续训练，让模型更适配任务。\n"
        "   白话：做岗位培训：学你们公司的规则与口径。\n"
        "\n"
        "3）指令微调（Instruction Tuning）\n"
        "   专业：用“指令—回答”格式数据，让模型更会按要求做事。\n"
        "   白话：把问题讲清楚，让它学会“照要求交作业”。\n"
        "\n"
        "4）过拟合（Overfitting）\n"
        "   专业：模型把训练样本背下来，泛化变差。\n"
        "   白话：只会背题，换个问法就不会了。\n"
        "\n"
        "5）LoRA / PEFT（参数高效微调）\n"
        "   专业：冻结大模型大部分参数，只训练少量新增参数。\n"
        "   白话：不改整本教材，只加几张便签就能适配新任务。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 6
    y = draw_section_title(draw, style, h2_font, "图解：全量微调 vs LoRA", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_peft,
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
        "场景：公司做一个“客服工单自动回复 + 统一口径”的 AI 助手。\n"
        "\n"
        "问题：如果只靠提示词（Prompt）\n"
        "- 运营改一次话术，你就得改一堆提示词；\n"
        "- 不同同事写不同 Prompt，风格不一致；\n"
        "- 一到复杂规则（退换、赔付、时效），模型容易“说得像但不准确”。\n"
        "\n"
        "做法：用微调把“口径”变成模型习惯\n"
        "1）整理 500–5000 条高质量样本：真实问题 + 合规标准回复 + 禁止回答的反例。\n"
        "2）选择 LoRA 微调：成本低、迭代快，话术更新时重新训练一版小补丁。\n"
        "3）上线前评估：准确率、拒答率、敏感问题表现；上线后灰度 + 可回滚。\n"
        "\n"
        "结果：提示词工作量下降，回复更一致；但仍需要知识库/RAG 来覆盖“最新规则”，避免旧口径。",
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
        "误区 1：微调 = 让模型“记住更多事实”\n"
        "澄清：微调更擅长学“回答方式与规则习惯”；最新事实更适合用知识库/RAG 更新。\n"
        "\n"
        "误区 2：数据越多越好\n"
        "澄清：低质量数据会把模型教坏；少量高质量、覆盖边界的样本通常更有效。\n"
        "\n"
        "误区 3：微调一次就一劳永逸\n"
        "澄清：业务会变、口径会变；微调是“持续迭代的工程流程”，需要版本管理与回滚。\n"
        "\n"
        "误区 4：微调后就不会幻觉\n"
        "澄清：微调可能让它更“自信地按口径回答”；要降低幻觉仍要证据链与校验。",
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
        "1）微调像岗位培训：让通用模型更贴合你的任务、口径与输出格式。\n"
        "2）效果的关键在数据：高质量、覆盖边界、带反例；不是一味堆数量。\n"
        "3）微调是工程：评估、灰度、版本与回滚缺一不可；最新事实常要配合知识库/RAG。",
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
        "1）为什么说微调更像“学岗位习惯”，而不是“背百科全书”？请举一个工作场景例子。\n"
        "2）当数据很少、又需要频繁迭代时，你为什么可能更适合用 LoRA 而不是全量微调？\n"
        "3）如果你要把客服口径固化进模型，你会怎样准备训练样本？请说出至少 3 条具体规则。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：强调直觉类比与可落地的工程边界。",
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

