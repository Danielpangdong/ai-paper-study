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

    fig_flow = base / "moe_routing_flow.png"
    fig_compare = base / "moe_vs_dense_comparison.png"
    out_pdf = base / "2026-05-30_MoE（混合专家）.pdf"

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
        "1. 为什么重要",
        "2. 直观类比",
        "3. 工作原理",
        "4. 关键术语",
        "5. 真实案例",
        "6. 常见误区",
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
        "MoE（混合专家）：为什么大模型能“变大但不更贵”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-30    难度：高中友好    关键词：稀疏激活 / Router / 专家 / Top-k / 推理成本"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 18

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 162)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 18),
        "核心一句话：MoE 的本质，是把模型做成“专家库”，每次只叫少数专家处理一个 Token，"
        "用更少计算换更大能力。",
        font=body_font,
        fill=style.accent2,
    )
    y += 186

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "大模型最贵的部分，不是“参数写在纸上有多少”，而是：\n"
        "你每生成一个 Token，要做多少次计算。\n\n"
        "如果每次都让整个超大网络全量运转，模型越大，推理越慢、越贵、越难部署。\n"
        "MoE（混合专家）提供了一条很聪明的路：\n"
        "- 把同一个模型拆成很多“专家子网络”（专家库可以很大）。\n"
        "- 对每个 Token，只挑 Top-k 个专家来算（其余专家这次不工作）。\n"
        "- 于是：总参数能变大，但每次计算不一定成倍增加。\n\n"
        "一句话：MoE 让“更大模型”不必等价于“更贵的每次推理”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=6,
    )

    y += 10
    draw.text((style.margin_x, style.page_h - 56), "目录：" + "  |  ".join(toc_items), font=tiny_font, fill=style.muted)
    pages.append(page)

    # Page 2: Analogy
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)

    analogy_box_h = 600
    box = (style.margin_x, y, style.page_w - style.margin_x, y + analogy_box_h)
    draw.rounded_rectangle(box, radius=22, outline=style.line, width=3, fill=(255, 255, 255))

    x0 = style.margin_x + 22
    y0 = y + 18
    x_next = x0
    x_next = draw_badge(draw, style, small_font, "场景：公司有一个“专家客服中心”", x_next, y0, style.ink, style.soft)
    x_next = draw_badge(draw, style, small_font, "目标：每单只叫最合适的人", x_next, y0, style.ink, style.soft)

    y1 = y0 + 56
    y1 = draw_paragraph(
        draw,
        body_font,
        "想象一家公司每天收到成千上万条工单：\n"
        "“发票怎么开？”“系统登录不了？”“合同盖章流程在哪？”\n\n"
        "如果公司只有一个“万能客服”，每单都由同一个人从头处理：\n"
        "- 简单问题被拖慢；复杂问题也可能答不准。\n"
        "- 工单越多，越容易崩。\n\n"
        "更聪明的做法是：建立一个“专家库”：\n"
        "- 财务专家、IT 专家、法务专家、物流专家……（专家很多）。\n"
        "- 但每张工单不需要全员出动：只要叫 1～2 个最匹配的专家就够。\n\n"
        "MoE 就像把大模型做成“专家客服中心”。Router（分诊台）负责判断：\n"
        "这个 Token 该交给哪几个专家。\n\n"
        "一句话：人很多，但每单只叫少数人——能力更强，平均成本更低。",
        x0,
        y1,
        max_w - 44,
        style.ink,
        line_gap=6,
    )
    pages.append(page)

    # Page 3: Principles + flow figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "先把一句话说透：MoE = Router（门控/路由） + 多个专家（Experts）。\n"
        "它的关键不在于“专家越多越好”，而在于：每个 Token 只激活少数专家（稀疏激活）。\n\n"
        "把它想成 4 步：\n"
        "1) 读入 Token：模型准备生成/理解下一个字。\n"
        "2) Router 打分：判断这个 Token 更适合哪些专家处理。\n"
        "3) 选 Top-k 专家：只让 k 个专家参与计算（常见 k=1 或 2）。\n"
        "4) 合并结果：把被选中的专家输出加权合成，得到最终输出。\n\n"
        "下面这张图把信息流画出来：",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=6,
    )

    y += 10
    caption = "图 1：MoE 的“分诊 + 专家处理 + 合并”流程。要点：专家库很大，但每次只点少数专家的名。"
    cap_box = (style.margin_x, y, style.page_w - style.margin_x, y + 76)
    draw.rounded_rectangle(cap_box, radius=18, outline=style.line, width=3, fill=style.soft)
    y = draw_paragraph(draw, small_font, caption, style.margin_x + 18, y + 16, max_w - 36, style.muted, line_gap=4)
    y += 12
    y = paste_image_fit(page, fig_flow, style.margin_x, y, max_w, 820, border=True, style=style)
    pages.append(page)

    # Page 4: Terms + real case + compare figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    terms = (
        "1) 专家（Expert）\n"
        "   专业：MoE 中的子网络/子模块，各自学习处理不同类型输入。\n"
        "   白话：一群“专科医生”，各自擅长不同问题。\n\n"
        "2) Router / 门控网络（Gating）\n"
        "   专业：为每个 Token 计算各专家的分数，并选择要激活的专家。\n"
        "   白话：分诊台：这单该交给谁。\n\n"
        "3) Top-k（稀疏激活）\n"
        "   专业：每个 Token 只选 k 个专家参与计算。\n"
        "   白话：这次只叫 1～2 个专家，不让全员开会。\n\n"
        "4) 负载均衡（Load Balancing）\n"
        "   专业：训练时约束 Router，避免少数专家过热、其他专家闲置。\n"
        "   白话：别让“明星专家”被挤爆，也别让某些专家一直没活干。\n\n"
        "5) 总参数 vs 每次计算量\n"
        "   专业：MoE 的总参数可以很大，但每次只计算其中一小部分。\n"
        "   白话：公司员工很多，但每单只派少数人处理。"
    )
    y = draw_paragraph(draw, body_font, terms, style.margin_x, y, max_w, style.ink, line_gap=6)

    y += 6
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "案例：大模型推理服务“高峰期也要稳”。\n\n"
        "想象一个 AI 客服在双 11：同一秒有大量用户提问。\n"
        "如果模型是 Dense（稠密模型），每个 Token 都要跑完整网络，吞吐压力很大。\n"
        "如果是 MoE，服务端可以做到：\n"
        "- Token 先经过 Router 分流；\n"
        "- 只调用少数专家完成计算；\n"
        "- 在接近相同算力预算下，获得更强能力或更高吞吐。\n\n"
        "现实里，一些开源大模型家族采用了 MoE 思路（例如 Mixtral 等），\n"
        "目的就是在可控成本下追求更强效果（具体实现会因模型而异）。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=6,
    )

    y += 10
    y = paste_image_fit(page, fig_compare, style.margin_x, y, max_w, 640, border=True, style=style)
    pages.append(page)

    # Page 5: Misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)
    mis = (
        "误区 1：MoE 就是“把模型拆开”，一定更省钱\n"
        "  纠正：MoE 省的是每 Token 的计算，但工程成本更高（路由、并行、通信、负载均衡）。\n\n"
        "误区 2：专家越多，效果必然越好\n"
        "  纠正：专家多只是“容量”大；如果 Router 学不会分流、专家没形成分工，收益会很小。\n\n"
        "误区 3：Router 只要选得准就行，不用管负载\n"
        "  纠正：如果所有 Token 都挤到少数专家，会出现拥堵/退化；训练时通常需要负载均衡约束。\n\n"
        "误区 4：MoE 没有坏处，只是更强\n"
        "  纠正：MoE 可能出现专家闲置、路由失灵、延迟波动、部署复杂等问题；适合“想扩能力但预算有限”的场景。"
    )
    y = draw_paragraph(draw, body_font, mis, style.margin_x, y, max_w, style.ink, line_gap=6)

    y += 6
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    summary = (
        "1) MoE 把模型变成“专家库”，每个 Token 只激活少数专家（Top-k），实现稀疏计算。\n"
        "2) 这让总参数可以做得很大，但每次推理的计算量不必等比例暴涨。\n"
        "3) MoE 的挑战在 Router 与负载均衡：分流要准、拥堵要防、工程实现要稳。"
    )
    y = draw_paragraph(draw, body_font, summary, style.margin_x, y, max_w, style.ink, line_gap=6)

    y += 6
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    qs = (
        "1) 用“公司专家库”的类比解释：MoE 为什么能做到“人很多，但每单不贵”？\n"
        "2) 如果 Router 把大部分 Token 都分给同一个专家，会发生什么？你会怎么缓解？\n"
        "3) 你认为 MoE 更适合哪类产品场景：极致低延迟，还是高峰期高吞吐？为什么？"
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
