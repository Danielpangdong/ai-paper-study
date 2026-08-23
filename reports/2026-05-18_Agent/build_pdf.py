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
    fig_loop = base / "agent_loop.png"
    fig_analogy = base / "agent_project_manager_analogy.png"
    out_pdf = base / "2026-05-18_Agent（智能体）.pdf"

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
        "2. 一个直观类比：项目经理 + 专家团队",
        "3. 工作原理：Agent 的“闭环”怎么跑起来？",
        "4. 关键术语解释",
        "5. 一个真实应用案例：客服工单自动处理",
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
        "Agent（智能体）：让大模型从“会说”变成“会办事”",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-18    难度：高中友好    关键词：目标 / 计划 / 工具 / 闭环"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 124)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：Agent 的本质，是让模型围绕一个目标反复执行“想一想→做一做→看结果→再调整”的闭环，而不是一次性把话说完。",
        font=body_font,
        fill=style.accent2,
    )
    y += 150

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "很多人把大模型当成“更聪明的搜索/写作工具”，但很快会遇到天花板：\n"
        "你让它“帮我把这件事办完”，它往往只能写一段建议，不能真正落地。\n"
        "\n"
        "现实工作里，真正耗时间的不是“写一句话”，而是：\n"
        "拆解任务 → 查资料/查数据 → 填表/下单/发消息 → 检查结果 → 继续下一步。\n"
        "\n"
        "Agent（智能体）要解决的，就是把大模型从“会说”推进到“会做”：\n"
        "它不仅回答问题，还会围绕目标主动调用工具、分步骤推进，并在失败时重试或换方案。\n"
        "\n"
        "这对 AI 行业非常关键，因为：\n"
        "（1）产品形态在变：从 Chat（聊天）走向 Workflow（工作流）与自动化；\n"
        "（2）能力边界更清晰：模型负责决策与语言，工具负责执行与事实；\n"
        "（3）可控性更重要：做事就会出错，Agent 必须能被约束、被审计、可回滚。",
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
        "阅读建议：先看“项目经理类比”建立直觉 → 再看“闭环图”理解流程 → 最后看误区避坑。",
        font=body_font,
        fill=style.ink,
    )
    pages.append(page)

    # Page 3: Analogy + figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个直观类比：项目经理 + 专家团队", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把 Agent 想成一个“项目经理”。\n"
        "你对他说：\n"
        "“这周把客户投诉处理一下：分类、找原因、给出解决方案，并更新工单系统。”\n"
        "\n"
        "项目经理不会自己去写代码、查数据库、打电话、改系统。\n"
        "他会做三件事：\n"
        "（1）把目标拆成可执行步骤（先做什么，后做什么）；\n"
        "（2）把具体动作分派给专家（工具/系统/人）：查询、检索、计算、发消息、更新工单；\n"
        "（3）不断看反馈：做完一步就检查结果，不对就返工或换方案。\n"
        "\n"
        "所以 Agent 并不是“模型更会聊天”，\n"
        "而是“模型带着一套做事流程”，像项目经理一样把事推进到交付。",
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
        "图1：Agent 像项目经理；工具/系统像专家团队。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 4: How it works + workflow diagram
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理：Agent 的“闭环”怎么跑起来？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "用最清晰的“五步闭环”讲透：\n"
        "\n"
        "第1步：定目标（Goal）。你说清楚要什么结果。\n"
        "第2步：做计划（Plan）。把目标拆成 3–8 个小步骤。\n"
        "第3步：去执行（Act）。每一步都尽量用工具完成：查数据/发消息/更新系统。\n"
        "——这里常用的“工具调用”，就来自我们昨天讲的 Function Calling。\n"
        "第4步：看结果（Observe）。工具返回结构化结果：表格/JSON/状态码。\n"
        "第5步：再调整（Iterate）。结果不理想就：换参数、换工具、补充信息、重试。\n"
        "\n"
        "你可以把这套闭环理解成：\n"
        "‘先想清楚 → 再动手 → 看反馈 → 再修正’。\n"
        "\n"
        "当系统把每一步记录下来（目标、计划、工具调用、工具结果），\n"
        "Agent 才能做到可审计：\n"
        "出了错，你能定位是“计划错”“执行错”还是“数据错”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(page, fig_loop, style.margin_x, y, max_w, 760, border=True, style=style)
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "图2：Agent 五步闭环（目标→计划→执行→观察→迭代）。",
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
        "Agent（智能体）：\n"
        "专业：以大模型为核心，围绕目标进行规划、调用工具执行、读取结果并迭代推进的系统。\n"
        "白话：会“做事的助理”，不只是会聊天。\n"
        "\n"
        "Goal（目标）：\n"
        "专业：对最终结果的清晰定义（要交付什么、成功标准是什么）。\n"
        "白话：你到底想要“拿到什么”。\n"
        "\n"
        "Plan（计划）：\n"
        "专业：把目标拆成可执行步骤的任务分解。\n"
        "白话：先做 A，再做 B，再做 C 的路线图。\n"
        "\n"
        "Tool（工具）：\n"
        "专业：可被系统调用的外部能力（函数/API/数据库查询/搜索等）。\n"
        "白话：Agent 的“手和眼睛”。\n"
        "\n"
        "Memory（记忆）：\n"
        "专业：让 Agent 在多轮、多天任务中保留关键信息的机制（短期/长期）。\n"
        "白话：助理的“备忘录”，不是天生的超强记忆。\n"
        "\n"
        "Guardrails（护栏）：\n"
        "专业：对工具权限、输入输出、执行范围的限制与校验。\n"
        "白话：给 AI 办事装上的“安全带”和“审批流程”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 6: Real-world case
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例：客服工单自动处理", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "场景：你们公司每天有大量客户工单（丢件、延误、破损、地址异常）。\n"
        "你希望一个“客服 Agent”把处理效率提上去：\n"
        "自动分类、查原因、给出建议、必要时升级人工，并把结果回写系统。\n"
        "\n"
        "如果只让模型“自由发挥”，常见翻车点是：\n"
        "分类不稳定、原因猜测、回复模板不合规、忘了更新系统。\n"
        "\n"
        "用 Agent 的闭环做法是：\n"
        "（1）Goal：把工单处理到“可关闭/可升级”的状态。\n"
        "（2）Plan：分类 → 拉取物流轨迹/历史记录 → 判断是否异常 → 生成回复 → 更新工单。\n"
        "（3）Act：逐步调用工具（查单号、查站点、查历史赔付、写回工单系统）。\n"
        "（4）Observe：看工具结果是否完整（有没有轨迹、时间是否对得上）。\n"
        "（5）Iterate：信息不足就追问；风险高就升级人工；必要时再查一次。\n"
        "\n"
        "一句话：\n"
        "Agent 像客服主管：会拆解、会推进、会校验，不靠‘编’把事情糊过去。",
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
        "误区1：Agent = AGI（通用人工智能）。\n"
        "纠正：Agent 只是“会按流程做事的系统”，能力仍受模型与工具限制。\n"
        "\n"
        "误区2：Agent 一定要全自动。\n"
        "纠正：最实用的是“半自动”：关键步骤需要人确认（比如退款、改地址、发重要邮件）。\n"
        "\n"
        "误区3：有了 Agent，就不会幻觉。\n"
        "纠正：会少一些，但不会消失。必须让关键事实来自工具结果，并做校验。\n"
        "\n"
        "误区4：Agent 的记忆是无限的。\n"
        "纠正：短期记忆受上下文窗口限制；长期记忆需要外部存储与筛选机制。\n"
        "\n"
        "误区5：能调用工具就等于安全。\n"
        "纠正：工具越多风险越大。必须有权限、白名单、审批与日志，防止被诱导执行错误动作。",
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
        "1）Agent 让 AI 围绕目标跑“闭环”：计划→执行→看结果→再调整。\n"
        "2）模型负责决策与表达，工具负责执行与事实；两者分工才能可靠落地。\n"
        "3）真正可用的 Agent 一定带护栏：权限、确认、日志与可回滚。",
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
        "1）用“项目经理”的类比解释：Agent 为什么必须拆解任务并看反馈，而不是一次性写完？\n"
        "2）在 Agent 的五步闭环里，哪两步最容易出错？你会怎么加护栏？\n"
        "3）如果要做“客服工单 Agent”，你会让它拥有哪些工具？哪些动作必须人工确认？",
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
