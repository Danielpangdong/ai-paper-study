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

    fig_loop = base / "inference_autoregressive_loop.png"
    fig_analogy = base / "training_vs_inference_analogy.png"
    out_pdf = base / "2026-05-25_推理（Inference）.pdf"

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
        "推理（Inference）：大模型为什么是“一个字一个字写出来”的？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-25    难度：高中友好    关键词：自回归 / 采样 / Temperature / Top-p / 延迟"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 22

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 152)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 18),
        "核心一句话：推理（Inference）的本质，是在参数不变的情况下，\n"
        "大模型根据已读内容一步步预测“下一个 Token”，再用采样策略把概率变成具体文字。",
        font=body_font,
        fill=style.accent2,
    )
    y += 182

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "当你用 ChatGPT 或 AI 助手时，有两个常见体验：\n"
        "1）它回答得很像在‘思考’，但其实是‘边写边想’。\n"
        "2）有时它秒回，有时又要等很久——而且越长的回答越慢。\n"
        "\n"
        "这些体验，几乎都发生在同一个环节：推理（Inference）。\n"
        "推理不是训练（Training）。训练是‘在学校刷题，把规律学进脑子里’；\n"
        "推理是‘到了考场，用学到的规律现场作答’。\n"
        "\n"
        "推理为什么重要？因为它决定了：\n"
        "• 速度：一次回答要多久（延迟 Latency）。\n"
        "• 成本：每次生成要烧多少算力（为什么 GPU 这么贵）。\n"
        "• 体验：能不能边打字边输出、能不能在手机上跑、能不能同时服务很多人（吞吐 Throughput）。\n"
        "\n"
        "一句话：你真正‘用到 AI’的那一刻，大多数时间都在为推理买单。",
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
        "把大模型想成一个“学霸学生”。\n"
        "• 训练（Training）：学霸在学校刷题、被老师批改、不断改错。\n"
        "  每刷一次题，学霸都会把‘笔记’调整得更靠谱（这对应：参数更新）。\n"
        "• 推理（Inference）：到了考场，学霸只允许用已经写好的笔记答题。\n"
        "  这时笔记不能改，只能按题目一步步写答案（这对应：参数不变）。\n"
        "\n"
        "你在对话框里输入一句话，就像把题干递给学霸。\n"
        "学霸不会一口气把整篇作文想好再写，而是：先写一个词，再写下一个词……\n"
        "直到写完或被你叫停。这就是你看到的‘边输出边生成’。",
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
        "提示：训练决定能力上限；推理决定使用体验与成本。两者不是一回事。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Page 3: mechanism + loop figure + terms
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "大模型推理的关键动作，其实可以用 6 步讲清：\n"
        "1）你输入一段文字（提示词 Prompt）。\n"
        "2）模型把它切成 Token（可以理解为‘可处理的小积木’）。\n"
        "3）模型读完这些 Token 后，会给出一个“候选表”：\n"
        "   也就是下一步最可能出现的 Token 们，各自的分数有多高（Logits）。\n"
        "4）把这些分数变成概率（可以理解为‘每个候选有多大可能被选中’）。\n"
        "5）用采样策略从概率里挑一个 Token（比如 Temperature、Top-p）。\n"
        "6）把新 Token 接在末尾，再重复 3）～5），直到遇到结束符或达到长度上限。\n"
        "\n"
        "所以你看到的输出，是一个循环：\n"
        "读入已有内容 → 预测下一个 Token → 选出来 → 接上去 → 再预测。\n"
        "\n"
        "这也解释了两件事：\n"
        "• 为什么回复越长越慢：循环次数变多了。\n"
        "• 为什么同一句话可能生成不同答案：采样会引入随机性。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y = paste_image_fit(
        page,
        fig_loop,
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
        "• 推理（Inference）\n"
        "  专业：模型参数固定后，根据输入生成输出的计算过程。\n"
        "  白话：考试现场答题，不能再改笔记。\n"
        "\n"
        "• 自回归（Autoregressive）\n"
        "  专业：每一步都用已有输出作为下一步输入。\n"
        "  白话：写作文时，先写一个词，再接着写下一个词。\n"
        "\n"
        "• Logits（分数）\n"
        "  专业：模型对每个候选 Token 给出的原始评分。\n"
        "  白话：下一步‘更像该选谁’的打分表。\n"
        "\n"
        "• 采样（Sampling）\n"
        "  专业：从概率分布里选出一个具体 Token 的策略。\n"
        "  白话：从‘可能选项’里做最终落笔。\n"
        "\n"
        "• Temperature（温度）\n"
        "  专业：调节概率分布的‘尖锐程度’，影响随机性。\n"
        "  白话：温度越高越敢‘发散’，温度越低越保守。\n"
        "\n"
        "• Top-p（核采样）\n"
        "  专业：只在累计概率达到 p 的候选集合中采样。\n"
        "  白话：只在‘最靠谱的一小圈候选’里做选择。\n"
        "\n"
        "• 延迟 / 吞吐（Latency / Throughput）\n"
        "  专业：单次响应时间 / 单位时间处理请求数。\n"
        "  白话：一个人回得快不快 / 一个团队同时能服务多少人。",
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
        "以 ChatGPT 的回答为例：\n"
        "你输入：‘用 3 点解释一下为什么推理很贵？’\n"
        "\n"
        "后台会发生什么？（只讲最关键的推理部分）\n"
        "1）系统把你的问题变成一串 Token。\n"
        "2）模型开始进入“逐 Token 生成”循环：\n"
        "   每生成一个 Token，都要做一次大计算（矩阵乘法等），\n"
        "   然后采样出下一个 Token。\n"
        "3）当你需要 300 个 Token 的回答，就意味着循环大约 300 次。\n"
        "\n"
        "这就是为什么：\n"
        "• 同样的问题，短答比长答更快；\n"
        "• 同时服务 1000 人，比服务 10 人更难；\n"
        "• 为了更快更便宜，会出现 KV Cache、量化、并行、专用推理芯片等工程优化。\n"
        "\n"
        "一句话：推理是把‘学到的能力’变成‘现场可用服务’的那条生产线。",
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
        "误区 1：推理就是“联网搜索”。\n"
        "更准确：推理是模型内部计算；它不一定联网。很多回答来自模型参数里的统计规律。\n"
        "\n"
        "误区 2：模型会先在脑子里把整段想好，再一次性打出来。\n"
        "更准确：大多数大模型是逐 Token 生成；你看到的‘打字感’，就是它在一边算一边写。\n"
        "\n"
        "误区 3：温度（Temperature）就是“创意开关”。\n"
        "更准确：温度主要调随机性与多样性；温度高不等于更聪明，可能更飘。\n"
        "\n"
        "误区 4：同一个问题推理结果应该完全一致。\n"
        "更准确：采样会引入随机性；同一问题可能有多种合理表述。想要更稳定，可以降低温度/调整采样策略。\n"
        "\n"
        "误区 5：推理越慢就一定越“深度思考”。\n"
        "更准确：慢可能来自更长输出、更大模型、更复杂系统编排或资源拥塞，不等于更正确。",
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
        "1）推理（Inference）是模型参数不变时的“现场生成”过程，不是训练。\n"
        "2）大模型通常按自回归方式逐 Token 生成：预测下一个 Token → 采样 → 接上去 → 循环。\n"
        "3）推理决定速度、成本与体验；采样策略决定稳定性与多样性。",
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
        "1）用你自己的话解释：为什么说大模型更像在‘一个字一个字写出来’，而不是一次性生成整段？\n"
        "2）如果你希望回答更稳定、更像‘标准答案’，你会怎么调 Temperature / Top-p？为什么？\n"
        "3）为什么说推理是 AI 产品的‘成本中心’？请用“输出越长越慢”这个现象解释背后的原因。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：用类比 + 流程图解释推理的直觉、流程与常见误区。",
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
