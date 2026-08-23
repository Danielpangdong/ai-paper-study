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
    fig_workflow = base / "function_calling_workflow.png"
    fig_analogy = base / "function_calling_frontdesk_analogy.png"
    out_pdf = base / "2026-05-17_Function Calling（函数调用）.pdf"

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
        "2. 一个直观类比：公司前台 + 专家部门",
        "3. 工作原理：从 tool_call 到 tool_result",
        "4. 关键术语解释",
        "5. 一个真实应用案例：数据周报自动化",
        "6. 常见误区（非常重要）",
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
        "Function Calling（函数调用）：让大模型真正“会用工具”",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-17    难度：高中友好    关键词：工具 / 结构化输出 / 可控 / Agent"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 124)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：函数调用的本质，是让模型在“要做事”时先输出一条可执行的工具请求（带参数），由系统去执行，再把结果交回模型组织成答案。",
        font=body_font,
        fill=style.accent2,
    )
    y += 150

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "很多人第一次用大模型会有两种失望：\n"
        "（1）它会“编”——一本正经地胡说；\n"
        "（2）它会“拖”——你要它做一件事，它只能用文字讲思路，无法真的去执行。\n"
        "\n"
        "函数调用要解决的就是这两个痛点：\n"
        "让模型把“要做什么”说清楚，并把“真正做事”交给可信工具。\n"
        "\n"
        "现实里你几乎每天都会碰到这种需求：\n"
        "查数据、算指标、订票、写周报、发邮件、调用公司系统……\n"
        "如果只靠模型“自由发挥”，错误会很隐蔽；\n"
        "而函数调用把流程拆成两段：\n"
        "（模型做决策）→（工具做执行）→（模型做表达）。\n"
        "\n"
        "这带来三件行业级价值：\n"
        "更准：关键事实来自工具结果；\n"
        "更可控：每一步可审计、可重放；\n"
        "更可扩展：接上更多工具，就能做更复杂的工作流。",
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
        "阅读建议：先看“前台类比”建立直觉 → 再看“工作流图”理解流程 → 最后看误区避坑。",
        font=body_font,
        fill=style.ink,
    )
    pages.append(page)

    # Page 3: Analogy + figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个直观类比：公司前台 + 专家部门", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把大模型想成一家公司的“前台主管”。\n"
        "它擅长的是：听懂你要什么、决定该找谁、把结果写成你看得懂的报告。\n"
        "\n"
        "但它不应该自己去“写数据库”“算公式”“跑报表”。\n"
        "这些活应该交给专业部门（工具）：\n"
        "数据库查询、统计计算、画图表、写作润色。\n"
        "\n"
        "函数调用就像：前台主管拿起对讲机，\n"
        "用一条清晰的指令（带参数）呼叫某个部门，\n"
        "等部门把结构化结果回传后，再把它组织成一份自然语言输出。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(page, fig_analogy, style.margin_x, y, max_w, 760, border=True, style=style)
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "图1：模型像“前台主管”，工具像“各部门专家”。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 4: How it works + workflow diagram
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理：从 tool_call 到 tool_result", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "用最清晰的四步讲透：\n"
        "\n"
        "第1步：你提需求（自然语言）。\n"
        "第2步：模型先不直接回答，而是输出一条“工具请求”（tool_call）。\n"
        "——它会写清楚：调用哪个工具、传什么参数。\n"
        "第3步：系统执行工具，拿到结果（tool_result）。\n"
        "——结果最好是结构化的，比如 JSON、表格、数字。\n"
        "第4步：模型把工具结果翻译成你能读懂的答案，并补上解释与下一步建议。\n"
        "\n"
        "你可以把 tool_call 理解成“可执行的指令单”，\n"
        "把 tool_result 理解成“执行回执”。\n"
        "当系统把这两者记录下来，整条链路就具备了可审计性：\n"
        "出了错，你能追溯是“决策错”还是“工具结果错”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(page, fig_workflow, style.margin_x, y, max_w, 760, border=True, style=style)
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "图2：函数调用工作流（从请求到执行再到答复）。",
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
        "Tool（工具）：\n"
        "专业：一个可被系统调用的能力（函数/API/数据库查询等）。\n"
        "白话：模型“可以找人帮忙”的外部技能。\n"
        "\n"
        "Schema / 参数约束：\n"
        "专业：定义工具需要哪些字段、类型是什么、哪些必填。\n"
        "白话：给前台主管一张“表单”，照着填就不会乱写。\n"
        "\n"
        "tool_call（工具请求）：\n"
        "专业：模型输出的结构化调用意图（工具名 + 参数）。\n"
        "白话：一张写清楚“找谁、要什么”的工单。\n"
        "\n"
        "tool_result（工具结果）：\n"
        "专业：工具执行后返回的结构化输出。\n"
        "白话：工单的回执单（带数据）。\n"
        "\n"
        "Agent（智能体）：\n"
        "专业：能规划步骤、反复调用工具完成目标的系统。\n"
        "白话：不是只聊天，而是能“做完一件事”的自动化助理。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 6: Real-world case
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例：数据周报自动化", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "场景：运营同学说：\n"
        "“把本周各城市的订单量、准时率、投诉率做个周报，标出异常城市，并给出可能原因。”\n"
        "\n"
        "如果只让模型“凭空写”，很容易出现：\n"
        "数据是编的、指标口径不一致、异常判断随意。\n"
        "\n"
        "用函数调用的正确做法是：\n"
        "（1）模型先生成 tool_call：去数据库拉取本周数据（含时间范围、字段口径）。\n"
        "（2）工具返回 tool_result：真实表格/统计数字。\n"
        "（3）模型再调用计算/画图工具：算同比环比、画趋势图。\n"
        "（4）最后模型把结果写成周报：\n"
        "——用自然语言解释“哪个城市异常、异常在哪里、可能原因有哪些、需要进一步查什么”。\n"
        "\n"
        "一句话：\n"
        "模型负责“理解与表达”，工具负责“事实与执行”。",
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
        "误区1：函数调用 = 模型变聪明了。\n"
        "纠正：它不一定更聪明，但会“更会用工具”。关键事实应来自工具结果，而不是猜。\n"
        "\n"
        "误区2：有了函数调用，就不会出错。\n"
        "纠正：tool_call 可能选错工具/参数，工具也可能返回脏数据；但好处是：错误能被定位与复盘。\n"
        "\n"
        "误区3：函数调用就是“联网搜索”。\n"
        "纠正：搜索只是工具之一。函数调用更像“把任何可执行能力接入模型”。\n"
        "\n"
        "误区4：模型可以随便调用任何工具。\n"
        "纠正：必须有权限与白名单；否则会有安全风险（比如被提示注入诱导去做不该做的操作）。\n"
        "\n"
        "误区5：工具结果一返回就等于真相。\n"
        "纠正：工具结果也要校验口径、时间范围、异常值；函数调用不是免检章，而是流程规范化。",
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
        "1）函数调用让模型先输出可执行的“工具工单”，而不是只靠嘴回答。\n"
        "2）工具负责拿到真实结果，模型负责把结果组织成可读的解释与建议。\n"
        "3）这让AI更准、更可控、更可审计，是从“聊天”走向“办事”的关键一步。",
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
        "1）用“公司前台”的类比解释：为什么模型不该自己去‘查库/算数’，而应该调用工具？\n"
        "2）tool_call 和 tool_result 各自像现实里的什么？它们为什么让流程更可控？\n"
        "3）如果你要做‘自动周报’，你会设计哪些工具？分别负责哪一段工作？",
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

