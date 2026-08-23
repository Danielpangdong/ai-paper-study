from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 170
    page_w: int = 1406  # A4 @ 170dpi
    page_h: int = 1987
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
    fig_teacher = base / "distill_teacher_student.png"
    fig_softlabels = base / "distill_softlabels_temperature.png"
    out_pdf = base / "2026-05-06_AI概念精讲_知识蒸馏（Knowledge Distillation）.pdf"

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
    draw.text((style.margin_x + 22, y + 58), "知识蒸馏：把“大老师”压缩成“小高手”", font=title_font, fill=style.ink)
    meta = "日期：2026-05-06    难度：高中友好    关键词：大模型 / 小模型 / 省钱省电"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 30

    y = draw_section_title(draw, style, h2_font, "为什么重要", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "很多时候，我们想要“像大模型一样聪明”，又希望它能：\n"
        "更快（手机/边缘设备也能跑）、更省钱（推理成本低）、更省电（功耗低）、更容易部署。\n"
        "但直接训练一个小模型，往往学不到大模型那么多“见识”和“做题技巧”。\n"
        "知识蒸馏的思路是：让一个很强的“老师模型”带着“学生模型”练习，\n"
        "学生不是只背标准答案，而是学习老师的“做题思路”，最后变成一个更强的小模型。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 18
    box = (style.margin_x, y, style.page_w - style.margin_x, y + 112)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 28),
        "一句话记住：知识蒸馏 = 用老师的“更细的反馈”教会学生。",
        font=body_font,
        fill=style.accent2,
    )
    y += 130

    y = draw_section_title(draw, style, h2_font, "直观类比（图1）", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_teacher,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=700,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图1：老师—学生类比：老师给“更细的提示”，学生学会更像老师。", font=small_font, fill=style.muted)
    pages.append(page)

    # Page 2
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（图2）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "蒸馏的关键不是“把参数剪掉”，而是“换一种更会教的训练方式”。\n"
        "和普通训练只告诉学生“对/错”不同，蒸馏会让老师给出“每个选项的倾向程度”。\n"
        "举个例子：\n"
        "问题：‘北京属于哪个国家？’\n"
        "硬答案（Hard label）：只告诉你正确选项是‘中国’。\n"
        "软提示（Soft label）：老师还会告诉你：‘中国’非常高，‘日本/韩国’很低，\n"
        "并且可能给出‘首都/地理’这些相关线索。学生学到的是“区分度”和“相似度”。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = paste_image_fit(
        page,
        fig_softlabels,
        style.margin_x,
        y,
        max_w=style.page_w - style.margin_x * 2,
        max_h=640,
        border=True,
        style=style,
    )
    draw.text((style.margin_x, y + 8), "图2：软标签与温度：老师给“分布式提示”，学生学习更平滑的判断。", font=small_font, fill=style.muted)
    y += 56

    y = draw_section_title(draw, style, h2_font, "工作原理（不用堆术语）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "知识蒸馏通常分三步：\n"
        "1）准备一个强老师：先有一个表现很好的大模型（不一定是你训练的）。\n"
        "2）让老师出题+给提示：把训练题喂给老师，让老师输出“它觉得各个答案的可能性”。\n"
        "3）训练学生去模仿：学生模型不只追求“选对”，还要尽量学得像老师的“概率分布”。\n"
        "结果：学生模型更小、更快，但表现更接近老师。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 3
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "关键术语解释（高中生版）", style.margin_x, y)
    terms = [
        ("老师模型（Teacher）", "很强、但通常很大很贵的模型：像“名师”。"),
        ("学生模型（Student）", "更小更便宜的模型：像“跟老师学的小同学”。"),
        ("硬标签（Hard label）", "只有“标准答案”这一条信息：对就是对、错就是错。"),
        ("软标签（Soft label）", "老师给的“各个选项的可能性”分布：更像评分细则。"),
        ("温度（Temperature）", "把老师的输出变得更“柔和”的旋钮：让学生更容易学到相似度。"),
        ("蒸馏损失（Distillation loss）", "衡量学生“像不像老师”的分数：越像越好。"),
        ("推理（Inference）", "模型已经学会后，真正拿来做题/聊天的过程。蒸馏主要省的是推理成本。"),
    ]
    max_w = style.page_w - style.margin_x * 2
    for key, val in terms:
        draw.text((style.margin_x, y), f"{key}：", font=body_font, fill=style.ink)
        y = draw_paragraph(draw, body_font, val, style.margin_x + 290, y, max_w - 290, style.muted, line_gap=10)
        y += 6

    y += 6
    y = draw_section_title(draw, style, h2_font, "一个实际应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "“手机端离线翻译/拍照识别”\n"
        "你想把一个很强的云端模型搬到手机上，但手机算力、电量和网络都有限。\n"
        "做法：用云端的大老师模型产生大量“带软提示”的训练数据（或者直接用老师在线指导），\n"
        "训练一个更小的学生模型。上线后，手机只跑学生模型：更快、更省电、更便宜。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 4
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "常见误区", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）误区：蒸馏就是“把大模型压缩一下”。事实：核心是训练方式变了，不是简单剪参数。\n"
        "2）误区：学生一定能完全复刻老师。事实：学生容量有限；蒸馏能接近，但不保证一样强。\n"
        "3）误区：只要有老师输出就行。事实：训练题的覆盖面、质量、以及“温度”等设置都影响效果。\n"
        "4）误区：蒸馏只对分类任务有用。事实：对语言模型也常用（例如让小模型学会更好的回答风格）。",
        style.margin_x,
        y,
        style.page_w - style.margin_x * 2,
        style.ink,
        line_gap=10,
    )
    y += 14

    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）为什么蒸馏比只给“标准答案”更会教学生？\n"
        "2）软标签里包含了哪类信息？用你自己的例子说明“相似度”的含义。\n"
        "3）你能想到一个场景：为什么我们宁愿用更小的学生模型，而不是直接用老师模型？",
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
