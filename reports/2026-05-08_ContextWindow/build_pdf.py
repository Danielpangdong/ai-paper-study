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
    fig_workbench = base / "context_window_workbench.png"
    fig_compare = base / "longcontext_rag_memory_compare.png"
    out_pdf = base / "2026-05-08_上下文窗口（Context Window）.pdf"

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
        "2. 直观类比：工作台大小",
        "3. 工作原理：滑动窗口与截断",
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
    draw.text((style.margin_x + 22, y + 58), "上下文窗口（Context Window）：大模型一次能“看见”多少？", font=title_font, fill=style.ink)
    meta = "日期：2026-05-08    难度：高中友好    关键词：Token / 截断 / 长对话"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 26

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 124)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 22),
        "核心一句话：上下文窗口决定了模型这一次回答时，桌面上能摊开的“材料上限”。",
        font=body_font,
        fill=style.accent2,
    )
    y += 150

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "你可能遇到过这些现象：\n"
        "（1）对话聊着聊着，模型开始“忘记前面说过什么”；\n"
        "（2）让它读一份很长的报告/合同，它只能回答前半段；\n"
        "（3）同样的问题，换成“把关键内容贴进来”就更准。\n"
        "\n"
        "这些现象背后，一个非常关键的限制就是：上下文窗口。\n"
        "大模型不是把互联网都装在脑子里随时可用；\n"
        "它更像一次考试时，你能带进考场的资料页数是有限的。\n"
        "\n"
        "在真实产品里，上下文窗口会直接影响：\n"
        "长对话是否稳定、长文是否看得懂、代码助手能否跨文件理解，\n"
        "以及你的成本、延迟和体验（窗口越大，通常越贵/越慢）。",
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
    hint = "阅读顺序建议：先看“工作台”类比 → 再看对比图 → 最后读误区与复习题。"
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
        "把大模型想成一个“桌面上做作业的学生”。\n"
        "桌面越大，他一次能摊开的资料越多：课本、讲义、草稿纸、参考答案……\n"
        "但桌面再大也不是无限大。\n"
        "\n"
        "上下文窗口（Context Window）就是这个“桌面大小”。\n"
        "你发给模型的提示词、历史对话、粘贴的文档，都会被拆成一张张小卡片（Token）放到桌面上。\n"
        "桌面放满了，新卡片要进来，旧卡片就得被挤走（截断/滑动窗口）。\n"
        "于是模型回答时，真的“看不见”的那部分，就很可能被忘掉。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 14
    y = paste_image_fit(
        page,
        fig_workbench,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=950,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：上下文窗口=工作台；Token=卡片；内容太长会被截断。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 4: How it works + fig2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（图2）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "理解上下文窗口，不需要数学，只要抓住三个动作：\n"
        "（1）拆分：文本会被切成 Token；\n"
        "（2）装盘：这些 Token 会被放进“当前工作台”（上下文）；\n"
        "（3）生成：模型回答时，只能基于工作台上看得见的 Token 来推理。\n"
        "\n"
        "当对话变长，系统通常会用三种办法应对：\n"
        "A. 直接把窗口做大（长上下文）；\n"
        "B. 用 RAG 去“资料库”按需检索（不把全文都塞进来）；\n"
        "C. 把早期内容总结成更短的“笔记”，再放回工作台（外部记忆/摘要）。\n"
        "这三种方法常常会组合使用。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(
        page,
        fig_compare,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=980,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：长上下文、RAG、外部记忆三种办法的分工与误区。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 5: Terms + case + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("Token（词元）", "专业：模型处理文本的最小单位（不一定等于一个字）。白话：桌面上的“小卡片”。"),
        ("上下文（Context）", "专业：本次推理时可见的输入集合。白话：这次做题你摊在桌上的材料。"),
        ("上下文窗口（Context Window）", "专业：上下文可包含的最大 Token 数。白话：桌面最大面积。"),
        ("截断（Truncation）", "专业：超过窗口时丢弃一部分输入。白话：桌面满了，旧纸被挤掉。"),
        ("长上下文（Long Context）", "专业：扩大可处理长度的模型与系统能力。白话：换一张更大的桌子。"),
        ("RAG（检索增强生成）", "专业：从外部知识库检索相关材料再让模型回答。白话：需要时去图书馆拿参考书。"),
        ("摘要/外部记忆（Summary/Memory）", "专业：把历史压缩成更短的记录并持续更新。白话：把长篇对话写成“会议纪要”。"),
    ]
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 350, y, max_w - 350, style.muted, line_gap=10)
        y += 6

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "“企业AI助手读规章制度”\n"
        "很多公司希望 AI 助手能回答：报销规则、合同条款、流程制度、产品手册。\n"
        "但这些资料通常很长，直接整本粘进对话里会超过上下文窗口，\n"
        "还会让成本上升、回答变慢。\n"
        "\n"
        "更可靠的做法通常是：\n"
        "用 RAG 先从知识库里检索出与问题最相关的几段（像只带“关键页”进考场），\n"
        "再把这些段落放进上下文里让模型回答。\n"
        "这样既不超窗，又能让回答“有依据”。",
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
        "1）误区：上下文窗口=永久记忆。事实：它只是“本次可见材料”，下一次不一定还在。\n"
        "2）误区：窗口越大一定越聪明。事实：更像“能看更多材料”，但不保证理解更好。\n"
        "3）误区：模型忘了=模型坏了。事实：很可能是早期内容被截断了。\n"
        "4）误区：RAG=联网搜索。事实：RAG 可以是你自己的内部资料库，关键是“检索+引用”。",
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
        "1）上下文窗口决定：模型这一次回答时，最多能看见多少 Token。\n"
        "2）对话变长会触发截断：旧内容看不见，模型就可能“忘记”。\n"
        "3）解决长内容问题常用组合：长上下文 + RAG 检索 + 摘要/外部记忆。",
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
        "1）用“桌面做作业”的类比解释：为什么模型会在长对话里忘记早期信息？\n"
        "2）你会在什么情况下优先用 RAG，而不是一味追求更长的上下文窗口？\n"
        "3）如果你在做一个长期项目助理（要记住目标与偏好），你会怎么设计“摘要/外部记忆”策略？",
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

