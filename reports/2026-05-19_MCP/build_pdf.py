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

    fig_arch = base / "mcp_protocol_architecture.png"
    fig_analogy = base / "mcp_universal_adapter_analogy.png"
    out_pdf = base / "2026-05-19_MCP（模型上下文协议）.pdf"

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
        "2. 一个直观类比：AI 世界的“USB-C / 万能转换头”",
        "3. 工作原理：MCP 到底把什么统一了？",
        "4. 关键术语解释",
        "5. 一个真实应用案例：企业 AI 助手接入内部系统",
        "6. 常见误区（非常重要）",
        "7. 3句话总结",
        "8. 3个复习问题",
    ]

    # Page 1: Title + importance
    page, draw, y = new_page()
    header_h = 230
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "AI每日深度科普", font=kicker_font, fill=style.muted)
    draw.text(
        (style.margin_x + 22, y + 58),
        "MCP（模型上下文协议）：为什么它像 AI 世界的 USB-C？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-19    难度：高中友好    关键词：统一接口 / 工具连接 / 安全边界"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 128)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：MCP 的本质，是让“AI 应用连接工具/数据”的方式标准化——像 USB-C 一样，插同一个口，就能接不同设备。",
        font=body_font,
        fill=style.accent2,
    )
    y += 156

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "如果你只把大模型当成“会聊天的文字引擎”，你很快会遇到一个现实问题：\n"
        "真正有价值的 AI，不是把话说得更漂亮，而是能接入你的工作与数据。\n"
        "\n"
        "例如：查日历、发邮件、拉取订单、查库存、写入工单、读企业文档、跑一段脚本……\n"
        "这些都不是“聊天本身”，而是“连接外部世界”。\n"
        "\n"
        "但过去的连接方式像这样：每做一个 AI 应用，就要为每个系统各写一套适配。\n"
        "一套给邮箱，一套给日历，一套给数据库——接口不同、权限不同、审计方式也不同。\n"
        "结果是：开发慢、维护难、风险高（尤其是权限与数据泄露）。\n"
        "\n"
        "MCP 之所以重要，是因为它把这件事“标准化”了：\n"
        "（1）对应用：用同一种方式接入工具；\n"
        "（2）对工具方：用同一种方式把能力暴露出来；\n"
        "（3）对企业/个人：更容易做权限控制、日志审计与安全边界。\n"
        "\n"
        "一句话：MCP 让 AI 从“会说”迈向“能连接、能落地、可控地做事”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC + analogy (with figure)
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（你将学到什么）", style.margin_x, y)
    toc_text = "\n".join([f"{i+1}. {t.split('.',1)[1].strip()}" for i, t in enumerate(toc_items)])
    y = draw_paragraph(draw, body_font, toc_text, style.margin_x, y, max_w, style.ink, line_gap=10)

    y += 8
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把 AI 应用想成“电器”（聊天、IDE、工作流），把邮件/日历/数据库想成“各种设备”。\n"
        "如果每个电器都要做专属插头，那世界会很乱：新设备一来就得全部重做。\n"
        "\n"
        "MCP 就像 USB-C / 万能转换头：\n"
        "电器只要学会一种插法（MCP 客户端），就能通过同一个口去连接各种设备（MCP 服务器）。\n"
        "而设备厂商也只要提供一个统一的接口（MCP Server），就能被很多 AI 应用复用。\n"
        "\n"
        "这不是“更聪明”，而是“更好接、更可控、更可规模化”。",
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
        y + 8,
        max_w,
        max_h=560,
        border=True,
        style=style,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "图：用“万能转换头”理解 MCP 的价值：把一次次定制，变成一次次插拔。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 3: How it works (with figure)
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "先抓住一句话：MCP 统一的是“连接方式”，不是“模型本身”。\n"
        "\n"
        "你可以把 MCP 想成三层：\n"
        "A）MCP Client：在 AI 应用这边，负责“按协议说话”；\n"
        "B）MCP Protocol：一套标准的约定（怎么列出工具、怎么调用、怎么返回结果）；\n"
        "C）MCP Server：在工具/数据这边，负责“把能力包装成标准接口”。\n"
        "\n"
        "当 AI 要完成一件事（比如“把明天 10 点改到 11 点并通知对方”），流程大致是：\n"
        "1）应用端先问：你这里有哪些能力可用？（列工具/资源/提示词）\n"
        "2）模型决定：要调用哪个工具、传什么参数；\n"
        "3）MCP Server 去执行真实动作（改日历/发邮件），再把结果返回；\n"
        "4）应用把结果展示给用户，并记录日志以便审计。\n"
        "\n"
        "注意：真正关键的不是“能不能调工具”，而是“调工具这件事终于有了统一的标准”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y = paste_image_fit(
        page,
        fig_arch,
        style.margin_x,
        y + 8,
        max_w,
        max_h=640,
        border=True,
        style=style,
    )
    pages.append(page)

    # Page 4: Terms + real-world case
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）MCP Client\n"
        "   专业：实现 MCP 协议的客户端组件，用来发现与调用工具。\n"
        "   白话：AI 应用里的“插头”，负责按统一规则去“插设备”。\n"
        "\n"
        "2）MCP Server\n"
        "   专业：对外暴露工具/资源/提示词的服务端，实现统一接口。\n"
        "   白话：工具方的“转换头”，把自己的能力翻译成统一标准。\n"
        "\n"
        "3）Tool / Resource / Prompt\n"
        "   专业：可调用动作 / 可读取数据 / 可复用提示模板。\n"
        "   白话：能做什么、能看什么、该怎么问更靠谱。\n"
        "\n"
        "4）权限与审计\n"
        "   专业：访问控制、最小权限、日志记录与回放。\n"
        "   白话：谁能用、能用到哪一步、出了事能追溯。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "场景：企业里做一个“运营助理 AI”，每天要做三件事：\n"
        "（1）从内部系统查昨天的订单异常；（2）把重点写成摘要；（3）发邮件给相关负责人。\n"
        "\n"
        "没有 MCP 时：你要写 3 套 SDK/接口适配，还要分别处理鉴权、报错、日志。\n"
        "换个邮箱系统、换个数据库驱动，维护成本立刻爆炸。\n"
        "\n"
        "有 MCP 时：你把“邮件、数据库、内部订单系统”各做成 MCP Server（或接入现成 Server）。\n"
        "AI 应用只要会 MCP 这一种连接方式，就能稳定调用这三类能力。\n"
        "\n"
        "更重要的是：企业可以在 MCP 这一层统一加护栏：\n"
        "哪些工具只读？哪些动作要二次确认？哪些字段要脱敏？所有调用都记录在案。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 5: Misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "误区 1：MCP = Agent\n"
        "澄清：Agent 是“围绕目标做事的闭环”，MCP 是“连接工具的统一接口”。Agent 可以用 MCP，但两者不是一回事。\n"
        "\n"
        "误区 2：接入了 MCP，就等于“自动化无风险”\n"
        "澄清：真正的风险在权限与执行动作上。必须做最小权限、重要操作确认、日志审计与回滚策略。\n"
        "\n"
        "误区 3：MCP 会让模型变更聪明\n"
        "澄清：MCP 主要提升的是“可连接性与工程化落地”，不是模型智商。它让能力更可用、更可控。\n"
        "\n"
        "误区 4：MCP 就是插件商店\n"
        "澄清：商店是分发方式；MCP 是接口标准。有没有商店，标准都能用。",
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
        "1）MCP 解决的是“AI 应用怎么统一接入工具/数据”的工程化难题。\n"
        "2）它像 USB-C：统一接口让能力可复用、可规模化，也更容易做权限与审计。\n"
        "3）MCP 不是 Agent、不是魔法；真正的价值在“标准化 + 可控落地”。",
        style.margin_x,
        y,
        max_w,
        style.accent2,
        line_gap=10,
    )

    y += 8
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）用“USB-C/转换头”的类比解释：MCP 到底把哪件事标准化了？\n"
        "2）为什么说 MCP 的关键价值不只是“能调用工具”，而是“可控与可复用”？\n"
        "3）如果你要把“公司日历”做成一个 MCP Server，你会设计哪些权限边界与审计日志？",
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
