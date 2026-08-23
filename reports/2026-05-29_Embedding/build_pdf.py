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

    fig_space = base / "embedding_space_similarity.png"
    fig_uses = base / "embedding_applications_three_uses.png"
    out_pdf = base / "2026-05-29_Embedding（向量嵌入）.pdf"

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
        "Embedding（向量嵌入）：为什么 AI 能“理解相似意思”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-29    难度：高中友好    关键词：向量 / 相似度 / 语义检索 / 推荐 / RAG"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 18

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 162)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 18),
        "核心一句话：Embedding 的本质，是把“文字/句子”变成一串坐标（向量），"
        "让“意思像不像”可以用距离/相似度去计算。",
        font=body_font,
        fill=style.accent2,
    )
    y += 186

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "很多人以为 AI 的能力都来自“会说话的大模型”。但在真实产品里，决定体验的常常是：\n"
        "你能不能在海量信息里，快速找到“意思相近的内容”。\n\n"
        "Embedding 就是解决这件事的底层零件：\n"
        "- 它让搜索从“找关键词”升级成“找意思”。\n"
        "- 它让推荐系统能把“你”和“商品”放进同一张地图做匹配。\n"
        "- 它让 RAG 先检索资料再生成，回答更可靠、更可追溯。\n\n"
        "一句话：没有 Embedding，AI 很难把‘语义’变成可计算、可工程化的能力。",
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
    x_next = draw_badge(draw, style, small_font, "场景：外卖平台做“口味相似”推荐", x_next, y0, style.ink, style.soft)
    x_next = draw_badge(draw, style, small_font, "目标：别只靠关键词", x_next, y0, style.ink, style.soft)

    y1 = y0 + 56
    y1 = draw_paragraph(
        draw,
        body_font,
        "想象你在外卖平台搜“麻辣香锅”。\n"
        "你真正想要的可能是：偏辣、偏麻、油一点、肉多一点——这是“意思”，不是某个固定词。\n\n"
        "平台如果只靠关键词，会很蠢：\n"
        "- 你写“麻辣香锅”，它就只找标题里包含这四个字的店。\n"
        "- 你写“想吃重口一点”，它直接懵了。\n\n"
        "Embedding 的做法更像“画一张口味地图”：\n"
        "把每家店、每道菜、甚至每个用户的口味偏好，都变成地图上的一个坐标。\n"
        "你下单越多，你的坐标就越准确。下一次想吃什么，平台只要找离你最近的一批店——\n"
        "推荐就会更懂你。\n\n"
        "一句话：Embedding 把‘感觉很像’这件事，变成了‘距离很近’这件事。",
        x0,
        y1,
        max_w - 44,
        style.ink,
        line_gap=6,
    )
    pages.append(page)

    # Page 3: Principle + space figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "先把一句话说透：Embedding 模型会把文本变成一串数字（向量）。\n"
        "这串数字不是随便编的，而是通过大量数据训练出来的“意义坐标”。\n\n"
        "它大致经历三步：\n"
        "1) 编码：把词/句子输入模型，输出一个固定长度的向量。\n"
        "2) 拉近/推远：在训练中，让相关的文本更接近、不相关的更远（比如问题-答案、标题-正文、同义句）。\n"
        "3) 比较：上线后，用距离/相似度来判断“像不像”。\n\n"
        "你可以把向量当成‘意义的指纹’：相似的意思 → 指纹更像 → 距离更近。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=6,
    )

    y += 10
    caption = "读图提示：点之间越近，表示语义越相似；同一类内容会自然聚成一团。"
    cap_box = (style.margin_x, y, style.page_w - style.margin_x, y + 76)
    draw.rounded_rectangle(cap_box, radius=18, outline=style.line, width=3, fill=style.soft)
    y = draw_paragraph(draw, small_font, caption, style.margin_x + 18, y + 16, max_w - 36, style.muted, line_gap=4)
    y += 12
    y = paste_image_fit(page, fig_space, style.margin_x, y, max_w, 820, border=True, style=style)
    pages.append(page)

    # Page 4: Terms + real use figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    terms = (
        "1) 向量（Vector）\n"
        "   专业：由一串数字组成的表示，用来承载信息。\n"
        "   白话：把一句话压缩成“坐标”。\n\n"
        "2) Embedding（嵌入）\n"
        "   专业：把离散符号（词/句/图片）映射到连续向量空间。\n"
        "   白话：把‘文字’翻译成‘可计算的坐标语言’。\n\n"
        "3) 维度（Dimension）\n"
        "   专业：向量长度（比如 384/768/1536 维）。\n"
        "   白话：坐标有多少个方向（但不代表越多越好）。\n\n"
        "4) 相似度（Similarity）\n"
        "   专业：衡量两个向量是否接近（常见：余弦相似度）。\n"
        "   白话：两个意思像不像的‘分数’。\n\n"
        "5) 向量数据库（Vector DB）\n"
        "   专业：用于存储向量并做近似最近邻检索（ANN）。\n"
        "   白话：在海量坐标里，秒找离你最近的那几条。"
    )
    y = draw_paragraph(draw, body_font, terms, style.margin_x, y, max_w, style.ink, line_gap=6)

    y += 6
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "案例：AI 搜索 / 企业知识库问答（RAG）。\n\n"
        "你问：“报销多久到账？”\n"
        "系统不会只找包含‘报销’‘到账’这两个词的文档，而是：\n"
        "1) 把你的问题做 Embedding → 得到问题向量。\n"
        "2) 去向量数据库里检索 → 找到意思最接近的制度条款/FAQ。\n"
        "3) 把检索到的资料交给大模型 → 生成一段可读的回答，并尽量带引用依据。\n\n"
        "这样做的好处是：资料越全，回答越稳；资料缺失时，系统也更容易暴露‘找不到依据’而不是胡编。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=6,
    )

    y += 10
    y = paste_image_fit(page, fig_uses, style.margin_x, y, max_w, 640, border=True, style=style)
    pages.append(page)

    # Page 5: Misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)
    mis = (
        "误区 1：Embedding 就是“高级关键词匹配”\n"
        "  纠正：关键词匹配看字面；Embedding 更像在比“意思的坐标”。\n\n"
        "误区 2：维度越高一定越好\n"
        "  纠正：维度是容量，不是质量。训练数据与对齐目标更关键；维度过高还会增加存储与检索成本。\n\n"
        "误区 3：Embedding 能保证检索永远准确\n"
        "  纠正：不同领域/不同语言、甚至不同写法都会影响向量分布；工程上要做评测、阈值、重排与兜底。\n\n"
        "误区 4：向量是“安全的”，不会泄露信息\n"
        "  纠正：向量可能携带原始文本的痕迹；对隐私数据要做脱敏、权限、加密与生命周期管理。"
    )
    y = draw_paragraph(draw, body_font, mis, style.margin_x, y, max_w, style.ink, line_gap=6)

    y += 6
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    summary = (
        "1) Embedding 把文本变成向量坐标，让‘相似’这件事可以被距离/相似度计算。\n"
        "2) 它支撑语义检索、推荐系统和 RAG：先找“意思接近”的资料，再生成更可靠的回答。\n"
        "3) 做好 Embedding 不只是选模型：还要评测、阈值、检索加速、权限与隐私治理。"
    )
    y = draw_paragraph(draw, body_font, summary, style.margin_x, y, max_w, style.ink, line_gap=6)

    y += 6
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    qs = (
        "1) 用你自己的类比解释：为什么 Embedding 能让“意思像不像”变成可计算的距离？\n"
        "2) 在 RAG 里，Embedding 负责哪一步？如果 Embedding 很差，会导致什么问题？\n"
        "3) 你会如何验证一个 Embedding 系统“真的懂语义”而不是“碰巧撞对关键词”？"
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

