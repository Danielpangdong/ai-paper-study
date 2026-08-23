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

    fig_pipeline = base / "rlhf_training_pipeline.png"
    fig_analogy = base / "rlhf_restaurant_analogy.png"
    out_pdf = base / "2026-05-23_RLHF（人类反馈强化学习）.pdf"

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
        "RLHF（人类反馈强化学习）：为什么 AI 变得更“听人话”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-23    难度：高中友好    关键词：偏好 / 奖励 / 对齐 / 安全边界"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 22

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 152)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 18),
        "核心一句话：RLHF 的本质，是让 AI 不只“会说”，还要学会“什么回答更让人满意、更安全”。\n"
        "它通过人类的偏好反馈，把模型往“更像一个靠谱助手”的方向推。",
        font=body_font,
        fill=style.accent2,
    )
    y += 182

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "如果你只做过“让模型更聪明”的训练（比如多读书、多做题），你会发现一个现实问题：\n"
        "AI 变强了，但它的“说话方式”和“做事习惯”未必让人舒服——比如：\n"
        "- 语气太冲、太官腔、太啰嗦；\n"
        "- 明明不确定也很自信；\n"
        "- 不知道什么该拒绝、怎么拒绝更合适；\n"
        "- 在同样正确的多个回答里，它选了一个“最不合人意”的版本。\n"
        "\n"
        "RLHF 之所以重要，是因为它解决的是 AI 落地最关键的那一层：\n"
        "把“语言能力”变成“助手能力”。\n"
        "它让模型学会：在多种可能回答之间，优先选择更有帮助、更礼貌、更安全、符合规则的那一个。\n"
        "\n"
        "一句话：RLHF 不是让 AI 更懂世界，而是让 AI 更懂“人怎么希望它回答”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC + analogy figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（快速预览）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "\n".join(f"• {item}" for item in toc_items),
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=8,
    )
    y += 6
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把 AI 想成一家餐厅的新服务员。\n"
        "同一句话，服务员可以用很多种方式回答：有的礼貌清晰，有的冷冰冰，有的说一大堆废话。\n"
        "餐厅老板真正想要的是：客人更满意、投诉更少、风险更低。\n"
        "\n"
        "RLHF 就像给服务员加了一套“顾客偏好评分系统”：\n"
        "让人类评审在两个回答里选更喜欢的那个，然后训练 AI 以后更偏向这种风格。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y = paste_image_fit(
        page,
        fig_analogy,
        style.margin_x,
        y + 10,
        max_w=max_w,
        max_h=560,
        border=True,
        style=style,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "提示：反馈是“偏好”，不等于“事实真理”；因此需要多样人群与明确的安全规则。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 3: mechanism + pipeline figure + terms
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "可以把 RLHF 想成三步走（很多产品会再加上“安全规则/拒答策略”）：\n"
        "Step 1｜先把模型“教到及格”（SFT）：用人工标注的好答案，让它学会基本说法。\n"
        "Step 2｜学会“什么更讨喜”（Reward Model）：给两条回答，让人选更好那条，训练一个打分器。\n"
        "Step 3｜把模型往高分方向推（PPO / DPO）：让模型更常输出能拿高分的回答风格。\n"
        "\n"
        "你可以把它理解为：\n"
        "先教会它怎么答题，再告诉它“老师更喜欢哪种解题步骤”，最后让它形成稳定习惯。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y = paste_image_fit(
        page,
        fig_pipeline,
        style.margin_x,
        y + 10,
        max_w=max_w,
        max_h=620,
        border=True,
        style=style,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "• SFT（监督微调）\n"
        "  专业：用标注数据做监督学习，让模型先学会“像样地回答”。\n"
        "  白话：先把服务员培训到会按流程说话。\n"
        "\n"
        "• Preference（偏好数据）\n"
        "  专业：同一问题下，多条候选回答的人类比较选择（A 更好还是 B 更好）。\n"
        "  白话：让顾客在两种服务方式里选更舒服的那个。\n"
        "\n"
        "• Reward Model（奖励模型）\n"
        "  专业：把人类偏好学成一个“打分器”，给回答打高低分。\n"
        "  白话：一个自动评分员，告诉你这次服务大概能得几分。\n"
        "\n"
        "• PPO / DPO（对齐优化方法）\n"
        "  专业：用强化学习或偏好优化，让策略更倾向高分答案。\n"
        "  白话：让服务员慢慢形成“高分习惯”，更常用大家喜欢的表达方式。\n"
        "\n"
        "• Alignment（对齐）\n"
        "  专业：让模型输出更符合人类意图与安全规范。\n"
        "  白话：让它更像靠谱助手，而不是“什么都敢说”的大喇叭。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 4: case + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "以 ChatGPT 这类“对话助手”为例：\n"
        "同一个问题，模型可能给出多个都“语法通顺”的回答，但人类更希望它：\n"
        "- 先给结论，再给步骤；\n"
        "- 诚实表达不确定，并给可验证的建议；\n"
        "- 在涉及危险/违法/隐私时，能拒绝并给安全替代方案。\n"
        "\n"
        "RLHF 的作用，是把这些“人类更喜欢的回答风格”和“安全边界”变成模型的稳定习惯，\n"
        "从而让产品体验更一致：同样的输入，不会忽好忽坏、忽热情忽敷衍。",
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
        "误区 1：RLHF = 让模型更“正确”。\n"
        "更准确的说法：它更像“让模型更符合人类偏好与规则”。偏好并不天然等于事实。\n"
        "\n"
        "误区 2：有了 RLHF，模型就不会胡说八道。\n"
        "现实：它能改善语气与可靠性表达，但“知识是否准确”仍受训练数据与检索/工具影响。\n"
        "\n"
        "误区 3：奖励模型打分越高越好。\n"
        "现实：会出现‘迎合评分’（reward hacking）：为了高分而变得油滑、过度拒答或过度讨好。\n"
        "\n"
        "误区 4：只要找少数专家评审就够。\n"
        "现实：偏好存在差异；需要多样人群、明确标准、以及对安全/公平的持续评估。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 8
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）RLHF 让 AI 学会“什么回答更让人满意、更安全”，把语言能力变成助手习惯。\n"
        "2）它靠人类偏好训练出打分器，再把模型往高分方向优化（如 PPO / DPO）。\n"
        "3）偏好不等于真理：必须配合清晰规则、多样评审与评估，避免迎合与偏见。",
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
        "1）为什么说 RLHF 更像在教 AI“服务习惯”，而不是给 AI“涨知识”？\n"
        "2）如果一条回答‘事实正确但很刺耳’，另一条‘更温和但更含糊’，你觉得奖励模型会更偏向哪条？为什么？\n"
        "3）为了减少偏见与迎合，你认为偏好标注的规则与人群选择需要注意哪些点？请至少说出 3 条。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：用类比 + 流程图解释 RLHF 的直觉与边界。",
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

