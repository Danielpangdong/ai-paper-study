from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 200
    page_w: int = 1654  # A4 @ 200dpi
    page_h: int = 2339
    margin_x: int = 118
    margin_y: int = 108
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
    rag_flow = base / "rag_flow.png"
    embedding_map = base / "embedding_map.png"
    out_pdf = base / "2026-05-03_AI概念精讲_RAG检索增强生成.pdf"

    title_font = load_font(52)
    kicker_font = load_font(19)
    h2_font = load_font(30)
    body_font = load_font(23)
    small_font = load_font(18)

    pages: list[Image.Image] = []

    def new_page() -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
        page = Image.new("RGB", (style.page_w, style.page_h), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        y0 = style.margin_y
        return page, draw, y0

    # Page 1
    page, draw, y = new_page()
    header_h = 210
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "每日AI概念精讲", font=kicker_font, fill=style.muted)
    draw.text((style.margin_x + 22, y + 58), "RAG（检索增强生成）：让大模型“先翻资料再答题”", font=title_font, fill=style.ink)
    meta = "日期：2026-05-03    难度：高中友好    关键词：检索 / 向量 / 资料依据"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 30

    y = draw_section_title(draw, style, h2_font, "为什么重要", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "大模型很像“口才很好、见多识广的同学”，但它常见两个问题：\n"
        "1）记不住你公司/课堂/书里的最新资料；\n"
        "2）遇到不确定时可能会编得很像真的（俗称“胡编”）。\n"
        "RAG 的核心思想是：不要让模型闭眼作答，而是让它在回答前先去你的资料库里“找证据”，再基于证据组织答案。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 18
    callout = "一句话记住：RAG = 检索（找资料） + 生成（写答案）。"
    box = (style.margin_x, y, style.page_w - style.margin_x, y + 112)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text((style.margin_x + 22, y + 28), callout, font=body_font, fill=style.accent2)
    y += 130

    y = draw_section_title(draw, style, h2_font, "直观类比", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "想象你在做一道历史题：如果你先翻课本找到相关段落，再用自己的话总结，正确率通常更高；\n"
        "如果你不翻书凭感觉写，很可能写得流畅但细节错。\n"
        "RAG 就是把“先翻书”这一步做成系统：让模型自动去“课本”（知识库）里翻到最相关的几页，再回答。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 10

    y = draw_section_title(draw, style, h2_font, "工作原理（流程图）", style.margin_x, y)
    y = paste_image_fit(
        page,
        rag_flow,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=560,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：RAG 的整体流程（先检索，再生成）。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "Embedding（向量）是什么？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "在 RAG 里，系统会把“问题”和“资料片段”都变成一串数字（向量）。\n"
        "这些数字的“距离”可以表示语义相似：距离越近，意思越像。\n"
        "检索器会挑出离问题最近的几段资料（Top‑K），再交给大模型写答案。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 10
    y = paste_image_fit(
        page,
        embedding_map,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=660,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：向量/Embedding：把“意思”变成可计算的距离。", font=small_font, fill=style.muted)
    y += 54

    y = draw_section_title(draw, style, h2_font, "关键术语解释（不背也能懂）", style.margin_x, y)
    terms = [
        ("知识库", "你自己的资料集合：课件、文档、FAQ、制度、论文、笔记等。"),
        ("切片", "把长文档切成小段（例如每段 200～500 字），更利于精确检索。"),
        ("向量数据库", "专门做“按相似度快速找内容”的数据库，就像按意思检索的图书馆系统。"),
        ("Top‑K", "最相似的前 K 段资料（例如前 3 段、前 5 段）。"),
        ("提示词（Prompt）", "给大模型的说明：用户问题 + 找到的资料 + 回答要求（如必须依据资料）。"),
    ]
    max_w = style.page_w - style.margin_x * 2
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 210, y, max_w - 210, style.muted, line_gap=10)
        y += 6
    pages.append(page)

    # Page 3
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "实际应用：公司制度问答机器人", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "员工问“加班调休怎么申请？”如果只用大模型，它可能回答得很像真的，但和公司最新流程不一致。\n"
        "用 RAG：把制度文档放进知识库并切片 → 先检索到最相关的几段原文 → 再由大模型用更易懂的语言整理步骤并提醒关键信息。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 12
    box = (style.margin_x, y, style.page_w - style.margin_x, y + 126)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 24),
        "效果：答案更贴合“你自己的资料”。制度更新后只需更新知识库，不必重新训练大模型。",
        font=body_font,
        fill=style.accent2,
    )
    y += 154

    y = draw_section_title(draw, style, h2_font, "常见误区（容易踩坑）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）误区：RAG = 绝对不会胡编。事实：检索到的资料不相关或资料本身有误，仍会出错。\n"
        "2）误区：整本书不切片直接塞进去。事实：会变慢、会截断，也更难精确命中。\n"
        "3）误区：只看“检索到没”，不看“是否用上了”。事实：需要要求模型必须依据资料回答。\n"
        "4）误区：资料越多越好。事实：资料质量与组织方式更重要，噪音会拖累检索。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 14

    y = draw_section_title(draw, style, h2_font, "3个复习问题（自测）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）用一句话解释：为什么 RAG 能减少大模型“胡编”？\n"
        "2）Embedding（向量）在 RAG 里主要负责做什么？\n"
        "3）如果检索出来的 Top‑K 资料不相关，你会优先从哪三件事排查？",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：强调直观理解与可视化。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Pillow in this environment may be built without JPEG support; PDF export
    # for RGB pages uses JPEG internally. Use an indexed palette to avoid JPEG.
    pal_pages = [
        p.convert("P", palette=Image.Palette.ADAPTIVE, colors=256) for p in pages
    ]
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
