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
    warn: tuple[int, int, int] = (225, 29, 72)


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


def draw_badge(
    draw: ImageDraw.ImageDraw,
    style: Style,
    font: ImageFont.ImageFont,
    text: str,
    x: int,
    y: int,
    fg: tuple[int, int, int],
    bg: tuple[int, int, int],
) -> int:
    pad_x = 16
    pad_y = 10
    w = int(text_width(font, text)) + pad_x * 2
    h = font.size + pad_y * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=16, fill=bg, outline=style.line, width=2)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fg)
    return x + w + 10


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

    fig_speedup = base / "kvcache_inference_speedup.png"
    fig_tradeoff = base / "kvcache_memory_tradeoff.png"
    out_pdf = base / "2026-05-28_KV Cache（键值缓存）.pdf"

    title_font = load_font(50)
    kicker_font = load_font(19)
    h2_font = load_font(28)
    body_font = load_font(21)
    small_font = load_font(17)
    tiny_font = load_font(15)

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
    header_h = 260
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "AI每日深度科普", font=kicker_font, fill=style.muted)
    draw.text(
        (style.margin_x + 22, y + 58),
        "KV Cache（键值缓存）：为什么大模型能越聊越快、越省钱？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-28    难度：高中友好    关键词：注意力 / 逐字生成 / 缓存 / 省算力 / 显存"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 18

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 162)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 18),
        "核心一句话：KV Cache 的本质，是把注意力机制里“已经算过的历史信息”缓存起来，"
        "让模型在逐字生成时只计算新来的那一小步，避免每一步都把前面全部重算一遍。",
        font=body_font,
        fill=style.accent2,
    )
    y += 186

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "你在 ChatGPT 里看到的“一个字一个字往外吐”的体验，背后有一个很现实的问题：\n"
        "模型每多生成一个字，就要“回头看一遍”之前所有内容，判断哪些信息更相关。\n\n"
        "如果每一步都把历史内容重新算一遍，速度会越来越慢、成本会越来越高；\n"
        "KV Cache 让推理从“反复重读全文”变成“带着笔记继续写”，这几乎是现代大模型服务的标配。\n\n"
        "一句话：没有 KV Cache，大模型很难做到今天这种低延迟、可持续的对话与长文本生成。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=6,
    )

    y += 10
    draw.text((style.margin_x, style.page_h - 56), "目录：" + "  |  ".join(toc_items), font=tiny_font, fill=style.muted)
    pages.append(page)

    # Page 2: Analogy + core idea
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)

    analogy_box_h = 520
    box = (style.margin_x, y, style.page_w - style.margin_x, y + analogy_box_h)
    draw.rounded_rectangle(box, radius=22, outline=style.line, width=3, fill=(255, 255, 255))

    x0 = style.margin_x + 22
    y0 = y + 18
    x_next = x0
    x_next = draw_badge(draw, style, small_font, "场景：口译员在会议上做同传", x_next, y0, style.ink, style.soft)
    x_next = draw_badge(draw, style, small_font, "目标：越讲越快、别卡顿", x_next, y0, style.ink, style.soft)

    y1 = y0 + 56
    y1 = draw_paragraph(
        draw,
        body_font,
        "想象你是口译员：\n"
        "领导一句一句往外讲，你要一边听一边翻译。\n\n"
        "如果每听到一句新话，你都必须把前面 30 分钟录音从头再听一遍，才能决定这句话怎么翻译，"
        "那你一定会越翻越慢，最后直接崩溃。\n\n"
        "更聪明的做法是：你把“前面已经听过、已经整理过的重点”做成一份随手可用的笔记。"
        "下一句来了，你只需要：看笔记 + 听新句子 → 就能继续翻译。\n\n"
        "KV Cache 就是这份“随手可用的笔记”。",
        x0,
        y1,
        max_w - 44,
        style.ink,
        line_gap=6,
    )
    y += analogy_box_h + 24

    y = draw_section_title(draw, style, h2_font, "工作原理（先用一句话讲透）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "在注意力机制里，模型会把每个 token 变成两份“可被检索的卡片”：Key（索引）和 Value（内容）。\n"
        "生成下一个 token 时，它需要拿“当前这一步的 Query”去对比所有历史的 Key，再按权重取出对应的 Value。\n\n"
        "KV Cache 做的事很简单：历史 token 的 Key/Value 只算一次，存起来；"
        "后面每生成一个新 token，只新增这一条的 Key/Value，旧的直接复用。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=6,
    )
    pages.append(page)

    # Page 3: Figure (speedup) + terms
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "图解：为什么 KV Cache 能加速？", style.margin_x, y)

    caption = "读图提示：左边每步都“重算历史”；右边把历史 K/V 存进缓存盒子，只追加新 token 的 K/V。"
    cap_box = (style.margin_x, y, style.page_w - style.margin_x, y + 88)
    draw.rounded_rectangle(cap_box, radius=18, outline=style.line, width=3, fill=style.soft)
    y = draw_paragraph(draw, small_font, caption, style.margin_x + 18, y + 16, max_w - 36, style.muted, line_gap=4)
    y += 18

    y = paste_image_fit(page, fig_speedup, style.margin_x, y, max_w, 760, border=True, style=style)

    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    terms = (
        "1) Token（词元）\n"
        "   专业：模型处理文本的最小单位（不一定是一个汉字）。\n"
        "   白话：AI“按小块吃进去、按小块吐出来”的颗粒度。\n\n"
        "2) Attention（注意力）\n"
        "   专业：用 Query 去匹配 Key，并加权汇总 Value。\n"
        "   白话：AI 在一段文字里决定“现在更该关注哪几句”。\n\n"
        "3) Key / Value（键 / 值）\n"
        "   专业：注意力检索所需的索引向量与内容向量。\n"
        "   白话：像一本书的“目录（Key）”和“正文（Value）”。\n\n"
        "4) KV Cache（键值缓存）\n"
        "   专业：推理时缓存历史 token 的 K/V，供后续 token 复用。\n"
        "   白话：把已经做好的“重点笔记”存起来，下次继续写不用重做。"
    )
    y = draw_paragraph(draw, body_font, terms, style.margin_x, y, max_w, style.ink, line_gap=6)
    pages.append(page)

    # Page 4: Real case + misconceptions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "案例：你在聊天应用里看到“边想边打字”的 AI。\n\n"
        "1) 你输入一段话（上下文）。\n"
        "2) 模型开始逐字生成回复：每生成一个 token，它都要参考你刚才的输入 + 自己已经生成的前半句。\n"
        "3) KV Cache 让它不必在每一步重新处理整段历史文本，而是复用历史 K/V，只算新的一步。\n\n"
        "这直接带来两件事：\n"
        "- 延迟更低：更像人在“即时打字”。\n"
        "- 成本更可控：同样的 GPU 能服务更多人。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=6,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)

    mis = (
        "误区 1：KV Cache = 让模型“记住更多东西”\n"
        "  纠正：它只是把“同一段历史内容的中间计算结果”保存起来，方便复用；并不会突破上下文窗口。\n\n"
        "误区 2：KV Cache = 数据库 / 长期记忆\n"
        "  纠正：它通常只在一次对话/一次请求的推理过程中存在；结束后就释放，不会长期保存。\n\n"
        "误区 3：开了 KV Cache，模型就会更聪明\n"
        "  纠正：它提升的是速度与成本，而不是能力本身。更聪明来自模型结构、数据、训练与对齐。\n\n"
        "误区 4：KV Cache 只要开了就没代价\n"
        "  纠正：代价是显存/内存占用会随上下文变长而增长；上下文越长，缓存越“肥”。"
    )
    y = draw_paragraph(draw, body_font, mis, style.margin_x, y, max_w, style.ink, line_gap=6)
    pages.append(page)

    # Page 5: Tradeoff figure + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "图解：速度 vs 显存（工程权衡）", style.margin_x, y)
    y = paste_image_fit(page, fig_tradeoff, style.margin_x, y, max_w, 920, border=True, style=style)

    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    summary = (
        "1) 大模型之所以“逐字生成”，是因为每一步都要参考历史内容做注意力判断。\n"
        "2) KV Cache 把历史 token 的 Key/Value 缓存起来，让后续生成只新增一小步，避免重复计算。\n"
        "3) KV Cache 的收益是更快更省算力；代价是上下文越长，缓存越大，显存管理会成为关键工程问题。"
    )
    y = draw_paragraph(draw, body_font, summary, style.margin_x, y, max_w, style.ink, line_gap=6)

    y += 6
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    qs = (
        "1) 为什么“逐字生成”会天然带来大量重复计算？重复在哪里？\n"
        "2) 用你自己的类比解释：KV Cache 缓存的是什么？它没有缓存的又是什么？\n"
        "3) 当上下文从 1K 变成 32K 时，KV Cache 带来的工程挑战是什么？你会怎么权衡速度与显存？"
    )
    y = draw_paragraph(draw, body_font, qs, style.margin_x, y, max_w, style.ink, line_gap=6)
    pages.append(page)

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    pages[0].save(
        out_pdf,
        "PDF",
        resolution=style.dpi,
        save_all=True,
        append_images=pages[1:],
    )
    return out_pdf


if __name__ == "__main__":
    print(build())
