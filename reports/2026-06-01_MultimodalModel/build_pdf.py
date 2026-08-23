from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 120
    page_w: int = 1240
    page_h: int = 1754
    margin_x: int = 96
    margin_y: int = 86
    ink: tuple[int, int, int] = (15, 23, 42)
    muted: tuple[int, int, int] = (71, 85, 105)
    quiet: tuple[int, int, int] = (100, 116, 139)
    line: tuple[int, int, int] = (226, 232, 240)
    soft: tuple[int, int, int] = (248, 250, 252)
    blue: tuple[int, int, int] = (37, 99, 235)
    teal: tuple[int, int, int] = (13, 148, 136)
    green: tuple[int, int, int] = (22, 163, 74)
    amber: tuple[int, int, int] = (217, 119, 6)
    red: tuple[int, int, int] = (225, 29, 72)
    violet: tuple[int, int, int] = (124, 58, 237)


STYLE = Style()


def load_font(size: int, weight: int = 0) -> ImageFont.FreeTypeFont:
    candidates = [
        ("/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc", 0),
        ("/System/Library/Fonts/PingFang.ttc", 0),
        ("/System/Library/Fonts/STHeiti Medium.ttc", 0),
        ("/Library/Fonts/Arial Unicode.ttf", 0),
        ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 0),
    ]
    for path, index in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size, index=index)
    return ImageFont.load_default()


def text_width(font: ImageFont.ImageFont, text: str) -> float:
    try:
        return font.getlength(text)
    except Exception:
        return font.getbbox(text)[2]


def wrap_text(font: ImageFont.ImageFont, text: str, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        para = para.rstrip()
        if not para:
            lines.append("")
            continue
        buf = ""
        for ch in para:
            trial = buf + ch
            if text_width(font, trial) <= max_w:
                buf = trial
                continue
            if ch in "，。；：！？、）】》”’" and buf:
                lines.append((buf + ch).rstrip())
                buf = ""
                continue
            if buf:
                lines.append(buf.rstrip())
                buf = ch.lstrip()
            else:
                lines.append(trial)
                buf = ""
        if buf:
            lines.append(buf.rstrip())
    return lines


def draw_paragraph(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.ImageFont,
    text: str,
    x: int,
    y: int,
    max_w: int,
    fill: tuple[int, int, int],
    line_gap: int = 6,
) -> int:
    for line in wrap_text(font, text, max_w):
        if not line:
            y += int(getattr(font, "size", 18) * 0.75)
            continue
        draw.text((x, y), line, font=font, fill=fill)
        y += getattr(font, "size", 18) + line_gap
    return y


def draw_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int],
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int],
    width: int = 5,
) -> None:
    draw.line((start[0], start[1], end[0], end[1]), fill=color, width=width)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) >= abs(ey - sy):
        direction = 1 if ex >= sx else -1
        points = [(ex, ey), (ex - direction * 18, ey - 12), (ex - direction * 18, ey + 12)]
    else:
        direction = 1 if ey >= sy else -1
        points = [(ex, ey), (ex - 12, ey - direction * 18), (ex + 12, ey - direction * 18)]
    draw.polygon(points, fill=color)


def draw_badge(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.ImageFont,
    text: str,
    x: int,
    y: int,
    fg: tuple[int, int, int],
    bg: tuple[int, int, int],
    outline: tuple[int, int, int],
) -> int:
    pad_x = 16
    pad_y = 8
    w = int(text_width(font, text)) + pad_x * 2
    h = getattr(font, "size", 18) + pad_y * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=bg, outline=outline, width=2)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fg)
    return x + w + 10


def draw_header(
    draw: ImageDraw.ImageDraw,
    section: str,
    page_no: int,
    small_font: ImageFont.ImageFont,
) -> None:
    style = STYLE
    draw.text((style.margin_x, 38), "AI每日深度科普", font=small_font, fill=style.quiet)
    draw.text((style.page_w - style.margin_x - 155, 38), f"{page_no:02d}", font=small_font, fill=style.quiet)
    draw.line((style.margin_x, 70, style.page_w - style.margin_x, 70), fill=style.line, width=2)
    if section:
        draw.text((style.margin_x, 86), section, font=small_font, fill=style.teal)


def draw_footer(draw: ImageDraw.ImageDraw, page_no: int, tiny_font: ImageFont.ImageFont) -> None:
    style = STYLE
    footer = "2026-06-01  |  多模态模型（Multimodal Model）  |  让普通人看懂 AI"
    draw.line((style.margin_x, style.page_h - 78, style.page_w - style.margin_x, style.page_h - 78), fill=style.line, width=2)
    draw.text((style.margin_x, style.page_h - 54), footer, font=tiny_font, fill=style.quiet)
    draw.text((style.page_w - style.margin_x - 40, style.page_h - 54), str(page_no), font=tiny_font, fill=style.quiet)


def draw_section_title(
    draw: ImageDraw.ImageDraw,
    title_font: ImageFont.ImageFont,
    title: str,
    x: int,
    y: int,
    color: tuple[int, int, int] | None = None,
) -> int:
    style = STYLE
    color = color or style.teal
    draw.rounded_rectangle((x, y + 9, x + 28, y + 38), radius=10, fill=color)
    draw.text((x + 46, y), title, font=title_font, fill=style.ink)
    return y + getattr(title_font, "size", 30) + 22


def paste_image_fit(
    page: Image.Image,
    img_path: Path,
    x: int,
    y: int,
    max_w: int,
    max_h: int,
) -> int:
    style = STYLE
    img = Image.open(img_path).convert("RGB")
    scale = min(max_w / img.width, max_h / img.height)
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(page)
    draw.rounded_rectangle((x - 5, y - 5, x + new_w + 5, y + new_h + 5), radius=24, fill=(255, 255, 255), outline=style.line, width=3)
    page.paste(img, (x, y))
    return y + new_h + 22


def draw_steps(
    draw: ImageDraw.ImageDraw,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
    steps: list[tuple[str, str]],
    x: int,
    y: int,
    max_w: int,
    accent: tuple[int, int, int],
    row_h: int = 125,
) -> int:
    style = STYLE
    for i, (title, body) in enumerate(steps, start=1):
        draw_card(draw, (x, y, x + max_w, y + row_h), 20, (255, 255, 255), style.line, 2)
        draw.ellipse((x + 18, y + 25, x + 78, y + 85), fill=accent)
        draw.text((x + 38, y + 34), str(i), font=title_font, fill=(255, 255, 255))
        draw.text((x + 98, y + 19), title, font=title_font, fill=style.ink)
        draw_paragraph(draw, body_font, body, x + 98, y + 60, max_w - 122, style.muted, line_gap=5)
        y += row_h + 16
    return y


def generate_shared_space_figure(path: Path) -> None:
    style = STYLE
    w, h = 1600, 1020
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = load_font(50)
    h2 = load_font(30)
    h3 = load_font(25)
    body = load_font(22)
    tiny = load_font(18)

    draw.text((70, 54), "多模态模型：把不同形式翻译成同一种“意义语言”", font=title, fill=style.ink)
    draw.text((70, 124), "核心：文字、图片、声音、视频不是直接混在一起，而是先被编码成可计算的表示。", font=body, fill=style.muted)

    inputs = [
        ("文字 Token", "一句问题、说明书、聊天记录", style.blue),
        ("图片 Patch", "照片被切成小块来观察", style.teal),
        ("声音波形", "语音先变成节奏和音素线索", style.amber),
        ("视频帧", "一连串画面加上时间变化", style.violet),
    ]
    x0, y0 = 76, 220
    card_w, card_h, gap = 310, 128, 28
    centers: list[tuple[int, int]] = []
    for i, (name, desc, color) in enumerate(inputs):
        y = y0 + i * (card_h + gap)
        draw_card(draw, (x0, y, x0 + card_w, y + card_h), 22, (248, 250, 252), style.line, 2)
        draw.rounded_rectangle((x0 + 22, y + 24, x0 + 74, y + 76), radius=14, fill=color)
        if i == 0:
            draw.text((x0 + 37, y + 33), "文", font=h3, fill=(255, 255, 255))
        elif i == 1:
            draw.rectangle((x0 + 35, y + 34, x0 + 61, y + 61), outline=(255, 255, 255), width=4)
            draw.line((x0 + 36, y + 62, x0 + 49, y + 47, x0 + 63, y + 62), fill=(255, 255, 255), width=4)
        elif i == 2:
            for k in range(6):
                xx = x0 + 32 + k * 7
                draw.line((xx, y + 60, xx, y + 40 + (k % 3) * 9), fill=(255, 255, 255), width=4)
        else:
            draw.rectangle((x0 + 32, y + 37, x0 + 64, y + 63), outline=(255, 255, 255), width=4)
            draw.polygon([(x0 + 46, y + 44), (x0 + 46, y + 58), (x0 + 58, y + 51)], fill=(255, 255, 255))
        draw.text((x0 + 92, y + 22), name, font=h3, fill=style.ink)
        draw.text((x0 + 92, y + 67), desc, font=tiny, fill=style.muted)
        centers.append((x0 + card_w, y + card_h // 2))

    enc_box = (535, 350, 785, 585)
    draw_card(draw, enc_box, 28, (239, 246, 255), (191, 219, 254), 3)
    draw.text((583, 390), "编码器", font=h2, fill=style.blue)
    draw.text((587, 430), "Encoder", font=body, fill=style.blue)
    draw_paragraph(draw, tiny, "把每种输入转成一串数字表示", 570, 485, 185, style.muted, line_gap=4)

    for cx, cy in centers:
        draw_arrow(draw, (cx + 18, cy), (enc_box[0] - 16, (enc_box[1] + enc_box[3]) // 2), style.line, 4)

    circle_center = (1035, 468)
    draw.ellipse((circle_center[0] - 170, circle_center[1] - 170, circle_center[0] + 170, circle_center[1] + 170), fill=(236, 253, 245), outline=(153, 246, 228), width=5)
    draw.text((circle_center[0] - 98, circle_center[1] - 70), "共享", font=h2, fill=style.teal)
    draw.text((circle_center[0] - 132, circle_center[1] - 24), "语义空间", font=load_font(42), fill=style.teal)
    draw_paragraph(draw, tiny, "把不同形式放到同一张“意义地图”里比较", circle_center[0] - 118, circle_center[1] + 42, 236, style.muted, line_gap=4)
    draw_arrow(draw, (enc_box[2] + 18, (enc_box[1] + enc_box[3]) // 2), (circle_center[0] - 190, circle_center[1]), style.teal, 6)

    outputs = [
        ("回答问题", style.blue),
        ("生成描述", style.teal),
        ("执行工具", style.green),
        ("辅助决策", style.amber),
    ]
    out_x, out_y = 1270, 278
    for i, (label, color) in enumerate(outputs):
        y = out_y + i * 112
        draw_card(draw, (out_x, y, out_x + 230, y + 72), 18, (255, 255, 255), style.line, 2)
        draw.ellipse((out_x + 18, y + 20, out_x + 50, y + 52), fill=color)
        draw.text((out_x + 72, y + 20), label, font=h3, fill=style.ink)
        draw_arrow(draw, (circle_center[0] + 185, circle_center[1]), (out_x - 18, y + 36), color, 4)

    note_box = (74, 850, 1526, 944)
    draw_card(draw, note_box, 24, (255, 251, 235), (253, 230, 138), 3)
    draw.text((104, 876), "白话理解", font=h2, fill=style.amber)
    draw.text((268, 882), "多模态模型像一个翻译中心：先把照片、文字、声音都翻译成“意思”，再一起推理。", font=body, fill=style.ink)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=95)


def generate_case_workflow_figure(path: Path) -> None:
    style = STYLE
    w, h = 1600, 1020
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = load_font(50)
    h2 = load_font(30)
    h3 = load_font(25)
    body = load_font(21)
    tiny = load_font(18)

    draw.text((70, 54), "真实场景：多模态 AI 助手如何处理一张物流异常照片", font=title, fill=style.ink)
    draw.text((70, 124), "它不是只“看图”，而是把照片线索、文字问题和业务目标放在一起判断。", font=body, fill=style.muted)

    scene = (78, 210, 452, 800)
    draw_card(draw, scene, 30, (248, 250, 252), style.line, 3)
    draw.text((112, 240), "输入", font=h2, fill=style.blue)
    photo = (116, 300, 414, 526)
    draw.rounded_rectangle(photo, radius=22, fill=(226, 232, 240), outline=(203, 213, 225), width=3)
    draw.rectangle((158, 345, 360, 468), fill=(210, 180, 140), outline=(148, 120, 90), width=4)
    draw.line((158, 385, 360, 385), fill=(120, 92, 65), width=3)
    draw.line((255, 345, 255, 468), fill=(120, 92, 65), width=3)
    draw.polygon([(326, 468), (360, 468), (360, 430)], fill=(246, 180, 180), outline=(225, 29, 72))
    draw.text((170, 536), "仓库货箱照片", font=h3, fill=style.ink)
    question = "文字问题：\n这批货为什么可能延误？\n需要补哪些证据？"
    draw_card(draw, (116, 604, 414, 746), 20, (255, 255, 255), style.line, 2)
    draw_paragraph(draw, body, question, 140, 626, 250, style.ink, line_gap=7)

    steps = [
        ("1 视觉编码", "识别破损角、标签、堆放方式、拍摄环境。", style.teal),
        ("2 文本理解", "读懂问题：不是描述图片，而是判断延误风险。", style.blue),
        ("3 融合理解", "把图像线索和业务目标放在同一个语境中。", style.violet),
        ("4 输出建议", "给出风险判断、补拍证据、通知客服、生成处理单。", style.green),
    ]
    start_x, start_y = 535, 236
    step_w, step_h, step_gap = 240, 210, 50
    for i, (label, desc, color) in enumerate(steps):
        x = start_x + i * (step_w + step_gap)
        box = (x, start_y, x + step_w, start_y + step_h)
        draw_card(draw, box, 24, (255, 255, 255), style.line, 2)
        draw.rounded_rectangle((x + 22, start_y + 22, x + 76, start_y + 76), radius=15, fill=color)
        draw.text((x + 38, start_y + 31), str(i + 1), font=h3, fill=(255, 255, 255))
        draw.text((x + 22, start_y + 94), label[2:], font=h3, fill=style.ink)
        draw_paragraph(draw, tiny, desc, x + 22, start_y + 136, step_w - 44, style.muted, line_gap=5)
        if i == 0:
            draw_arrow(draw, (scene[2] + 22, 505), (x - 22, start_y + step_h // 2), style.teal, 5)
        if i < len(steps) - 1:
            draw_arrow(draw, (x + step_w + 10, start_y + step_h // 2), (x + step_w + step_gap - 18, start_y + step_h // 2), style.line, 5)

    output = (548, 585, 1492, 820)
    draw_card(draw, output, 28, (236, 253, 245), (153, 246, 228), 3)
    draw.text((584, 622), "输出不是一句泛泛描述，而是一组可行动建议", font=h2, fill=style.teal)
    bullets = [
        ("风险判断", "箱角破损 + 标签模糊，可能影响分拣与签收证明。"),
        ("补拍证据", "补拍运单号、破损近照、外包装全景、称重记录。"),
        ("处理动作", "标记异常件，通知客服，生成赔付或复核工单。"),
    ]
    bx = 584
    for title_text, body_text in bullets:
        draw.rounded_rectangle((bx, 684, bx + 250, 774), radius=18, fill=(255, 255, 255), outline=style.line, width=2)
        draw.text((bx + 22, 700), title_text, font=h3, fill=style.ink)
        draw_paragraph(draw, tiny, body_text, bx + 22, 735, 206, style.muted, line_gap=4)
        bx += 282

    note_box = (78, 870, 1492, 944)
    draw_card(draw, note_box, 24, (239, 246, 255), (191, 219, 254), 3)
    draw.text((110, 892), "关键认知", font=h2, fill=style.blue)
    draw.text((260, 899), "多模态强在“结合证据”：看见细节、读懂问题、连接目标，再给出下一步。", font=body, fill=style.ink)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=95)


def build() -> Path:
    style = STYLE
    base = Path(__file__).resolve().parent
    fallback_shared = base / "multimodal_shared_space.png"
    fallback_case = base / "multimodal_logistics_workflow.png"
    chatgpt_shared = base / "chatgpt_multimodal_shared_space.png"
    chatgpt_case = base / "chatgpt_multimodal_logistics_workflow.png"
    fig_shared = chatgpt_shared if chatgpt_shared.exists() else fallback_shared
    fig_case = chatgpt_case if chatgpt_case.exists() else fallback_case
    out_pdf = base / "2026-06-01_多模态模型（Multimodal Model）.pdf"

    generate_shared_space_figure(fallback_shared)
    generate_case_workflow_figure(fallback_case)

    title_font = load_font(54)
    subtitle_font = load_font(31)
    h2_font = load_font(30)
    h3_font = load_font(23)
    body_font = load_font(21)
    small_font = load_font(17)
    tiny_font = load_font(15)
    quote_font = load_font(24)
    max_w = style.page_w - style.margin_x * 2
    pages: list[Image.Image] = []

    def new_page(section: str, page_no: int) -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
        page = Image.new("RGB", (style.page_w, style.page_h), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        draw_header(draw, section, page_no, tiny_font)
        draw_footer(draw, page_no, tiny_font)
        return page, draw, 128

    # Page 1: title and table of contents
    page, draw, y = new_page("", 1)
    hero = (style.margin_x, 132, style.page_w - style.margin_x, 502)
    draw_card(draw, hero, 28, (247, 252, 252), style.line, 3)
    draw.text((style.margin_x + 28, 162), "2026-06-01", font=small_font, fill=style.quiet)
    draw.text((style.margin_x + 28, 205), "多模态模型", font=title_font, fill=style.ink)
    draw.text((style.margin_x + 28, 278), "Multimodal Model", font=subtitle_font, fill=style.blue)
    draw.text((style.margin_x + 28, 328), "为什么 AI 开始能同时看、听、读、说？", font=subtitle_font, fill=style.teal)
    draw_paragraph(
        draw,
        quote_font,
        "核心一句话：多模态模型的本质，是把文字、图片、声音、视频翻译成同一种“意义语言”，再放在一起理解和推理。",
        style.margin_x + 28,
        382,
        max_w - 56,
        style.ink,
        line_gap=8,
    )
    bx = style.margin_x + 28
    for label, color in [
        ("高中友好", style.teal),
        ("共享语义空间", style.blue),
        ("视觉语言模型", style.violet),
        ("真实工作案例", style.amber),
    ]:
        bx = draw_badge(draw, small_font, label, bx, 445, color, (255, 255, 255), style.line)

    y = 570
    y = draw_section_title(draw, h2_font, "目录", style.margin_x, y, style.blue)
    toc = [
        ("01", "为什么这个概念重要？", "AI 从只会聊天，走向能理解现实世界的输入。"),
        ("02", "一个直观类比", "像公司指挥中心，把不同线索翻译成同一张案情图。"),
        ("03", "工作原理", "编码、对齐、融合、输出。"),
        ("04", "关键术语解释", "模态、编码器、Embedding、对齐、融合、Grounding。"),
        ("05", "真实应用案例", "AI 助手分析物流异常照片。"),
        ("06", "常见误区", "多模态不是简单看图，也不是 AGI。"),
        ("07", "3句话总结 + 复习问题", "用问题检查是否真正理解。"),
    ]
    for num, title, desc in toc:
        row_h = 94
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + row_h), 18, (255, 255, 255), style.line, 2)
        draw.text((style.margin_x + 20, y + 27), num, font=h3_font, fill=style.teal)
        draw.text((style.margin_x + 92, y + 17), title, font=h3_font, fill=style.ink)
        draw.text((style.margin_x + 92, y + 52), desc, font=small_font, fill=style.muted)
        y += row_h + 13
    pages.append(page)

    # Page 2: why important
    page, draw, y = new_page("01 为什么重要", 2)
    y = draw_section_title(draw, h2_font, "为什么这个概念重要？", style.margin_x, y, style.teal)
    y = draw_paragraph(
        draw,
        body_font,
        "早期的大语言模型像一个只读文字的学生：你给它一段话，它能写总结、回答问题、改文案。"
        "但真实世界并不只由文字组成。我们工作时会看照片、听语音、读表格、看视频、理解图纸，还要把这些线索合在一起做判断。\n\n"
        "多模态模型解决的核心问题就是：AI 如何同时处理不同形式的信息，并把它们放到同一个语境里理解。\n\n"
        "这让 AI 从“会说话的文本工具”，走向“能观察现场、理解证据、辅助行动的智能助手”。"
        "它是 AI 搜索、AI 客服、AI 医疗影像、自动驾驶、教育批改、机器人和视频理解的共同基础。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 18
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 330), 24, (248, 250, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 22), "它改变了什么？", font=h2_font, fill=style.blue)
    change = (
        "1. 交互方式变自然：你可以拍照、发语音、圈出问题，而不必把所有信息都打成文字。\n"
        "2. 工作判断更接近真实：模型可以把“看到的证据”和“你问的问题”结合起来。\n"
        "3. AI 应用边界扩大：从写作、问答，扩展到质检、客服、教学、医学、设计和机器人。\n"
        "4. 风险也更具体：看错图、读错字、误判场景，都可能带来现实后果。"
    )
    draw_paragraph(draw, body_font, change, style.margin_x + 24, y + 82, max_w - 48, style.ink, line_gap=8)
    pages.append(page)

    # Page 3: analogy
    page, draw, y = new_page("02 直观类比", 3)
    y = draw_section_title(draw, h2_font, "一个直观类比：公司里的“联合指挥中心”", style.margin_x, y, style.teal)
    y = draw_paragraph(
        draw,
        body_font,
        "想象一家物流公司发生了异常件：客服拿来用户文字投诉，仓库发来现场照片，司机发来一段语音，系统里还有扫描时间和路线记录。\n\n"
        "如果每个部门只看自己手里的材料，就很容易得出片面的结论。真正有效的做法，是把所有线索交给一个联合指挥中心："
        "有人负责看照片，有人负责听语音，有人负责读记录，最后把线索汇总成同一张“案情图”。\n\n"
        "多模态模型也是这样。它并不是把图片硬塞进文字里，而是先让不同的“专家”把各自的信息翻译成模型能计算的表示，"
        "再把这些表示放在一起，形成对问题的整体理解。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 24
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 390), 26, (255, 251, 235), (253, 230, 138), 3)
    draw.text((style.margin_x + 28, y + 28), "类比对应关系", font=h2_font, fill=style.amber)
    pairs = [
        ("照片、语音、文字、视频", "不同模态"),
        ("各部门初步处理线索", "不同编码器"),
        ("统一案情图", "共享语义空间"),
        ("基于证据给处理建议", "多模态推理与输出"),
    ]
    yy = y + 94
    for left, right in pairs:
        draw_card(draw, (style.margin_x + 28, yy, style.margin_x + 445, yy + 58), 16, (255, 255, 255), style.line, 2)
        draw_card(draw, (style.margin_x + 602, yy, style.page_w - style.margin_x - 28, yy + 58), 16, (255, 255, 255), style.line, 2)
        draw.text((style.margin_x + 48, yy + 14), left, font=small_font, fill=style.ink)
        draw_arrow(draw, (style.margin_x + 470, yy + 29), (style.margin_x + 575, yy + 29), style.amber, 4)
        draw.text((style.margin_x + 622, yy + 14), right, font=small_font, fill=style.teal)
        yy += 72
    y += 430
    draw_paragraph(
        draw,
        body_font,
        "抓住这个直觉就够了：多模态不是“AI 多长了几只眼睛”，而是“AI 学会把不同证据放在同一张理解地图里”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    # Page 4: working principle with figure
    page, draw, y = new_page("03 工作原理", 4)
    y = draw_section_title(draw, h2_font, "工作原理：先翻译，再对齐，再一起推理", style.margin_x, y, style.blue)
    y = paste_image_fit(page, fig_shared, style.margin_x, y, max_w, 690)
    draw_paragraph(
        draw,
        small_font,
        "图 1：多模态模型把不同输入先编码成向量表示，再放进共享语义空间中比较和推理。这样“红色破损货箱照片”和“这批货可能延误吗？”才能被放在同一个问题里理解。",
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=5,
    )
    y += 72
    steps = [
        ("第一步：编码", "文字、图片、声音、视频分别进入不同的编码器，被转成数字表示。"),
        ("第二步：对齐", "模型学习让“同一件事”的文字描述和图片内容在语义空间里靠得更近。"),
        ("第三步：融合", "当用户提问时，模型把不同线索合在一起，判断哪些信息最相关。"),
        ("第四步：输出", "最后生成回答、描述图片、调用工具、填写表单或给出处理建议。"),
    ]
    draw_steps(draw, h3_font, small_font, steps, style.margin_x, y, max_w, style.blue, row_h=115)
    pages.append(page)

    # Page 5: terms
    page, draw, y = new_page("04 关键术语", 5)
    y = draw_section_title(draw, h2_font, "关键术语解释", style.margin_x, y, style.teal)
    terms = [
        ("模态（Modality）", "专业解释：信息的表现形式，例如文本、图像、音频、视频。", "白话解释：同一件事可以用不同方式表达：写出来、拍下来、说出来。"),
        ("编码器（Encoder）", "专业解释：把原始输入转成模型可计算的特征表示。", "白话解释：翻译员，把照片或声音翻译成 AI 看得懂的数字。"),
        ("Embedding", "专业解释：承载语义的向量表示，可用于比较相似度。", "白话解释：把“意思”变成坐标，方便模型判断谁和谁更接近。"),
        ("跨模态对齐（Alignment）", "专业解释：让不同模态中指向同一含义的表示彼此靠近。", "白话解释：让“猫的照片”和“这是一只猫”在地图上离得近。"),
        ("融合（Fusion）", "专业解释：整合来自多个模态的特征，用于统一推理。", "白话解释：把照片证据、文字问题和声音线索放在一起开会。"),
        ("Grounding", "专业解释：把模型语言输出连接到可观察的真实证据。", "白话解释：不要只会说，要能指出答案来自图里的哪块、哪行、哪个动作。"),
    ]
    col_w = (max_w - 26) // 2
    y_left = y
    y_right = y
    for idx, (name, pro, plain) in enumerate(terms):
        x = style.margin_x if idx % 2 == 0 else style.margin_x + col_w + 26
        yy = y_left if idx % 2 == 0 else y_right
        box_h = 236
        draw_card(draw, (x, yy, x + col_w, yy + box_h), 20, (255, 255, 255), style.line, 2)
        draw.text((x + 20, yy + 18), name, font=h3_font, fill=style.blue if idx % 2 == 0 else style.teal)
        draw_paragraph(draw, small_font, pro, x + 20, yy + 62, col_w - 40, style.ink, line_gap=5)
        draw_paragraph(draw, small_font, plain, x + 20, yy + 136, col_w - 40, style.muted, line_gap=5)
        if idx % 2 == 0:
            y_left = yy + box_h + 18
        else:
            y_right = yy + box_h + 18
    pages.append(page)

    # Page 6: real application
    page, draw, y = new_page("05 真实应用", 6)
    y = draw_section_title(draw, h2_font, "真实应用案例：AI 助手分析物流异常照片", style.margin_x, y, style.blue)
    y = draw_paragraph(
        draw,
        body_font,
        "假设客服收到一条咨询：用户说包裹疑似破损，仓库同事上传了一张货箱照片。普通文本模型只能读用户描述，"
        "但多模态模型可以同时看照片、读问题、理解业务目标，然后给出更具体的处理建议。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 22
    y = paste_image_fit(page, fig_case, style.margin_x, y, max_w, 690)
    draw_paragraph(
        draw,
        small_font,
        "图 2：多模态 AI 助手不是只描述“我看到一个箱子”，而是结合问题目标判断风险，并给出补拍证据、通知客服、生成工单等下一步动作。",
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=5,
    )
    y += 72
    case_steps = [
        ("看见证据", "照片里可能有破损角、潮湿痕迹、标签模糊或堆放异常。"),
        ("读懂问题", "用户问的是“是否延误、如何处理”，不是单纯要图片描述。"),
        ("连接业务动作", "模型把视觉线索转成可执行建议：补证、复核、通知、建单。"),
    ]
    draw_steps(draw, h3_font, small_font, case_steps, style.margin_x, y, max_w, style.teal, row_h=118)
    pages.append(page)

    # Page 7: misconceptions
    page, draw, y = new_page("06 常见误区", 7)
    y = draw_section_title(draw, h2_font, "常见误区（非常重要）", style.margin_x, y, style.red)
    myths = [
        ("误区 1：多模态模型就是“会看图的聊天机器人”", "纠正：看图只是入口。真正关键是把图像、文字、声音等线索统一理解，并用于推理和行动。"),
        ("误区 2：把图片转成文字描述，就等于多模态", "纠正：图片描述会丢掉位置、细节、关系和不确定性。强模型会直接利用视觉特征，而不只依赖一句描述。"),
        ("误区 3：模型看到图片，就一定理解现实", "纠正：它可能看错小字、忽略边角、误判物理关系。视觉能力强不等于拥有人的常识和责任判断。"),
        ("误区 4：多模态越多越聪明", "纠正：模态越多，噪声和冲突也越多。关键不是输入数量，而是对齐质量、训练数据和任务设计。"),
        ("误区 5：多模态模型就是 AGI", "纠正：它扩大了感知入口，但仍是任务型系统。它可以辅助判断，不等于自动拥有通用理解和自主责任。"),
    ]
    for title, body in myths:
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 178), 20, (255, 255, 255), style.line, 2)
        draw.text((style.margin_x + 22, y + 18), title, font=h3_font, fill=style.red)
        draw_paragraph(draw, body_font, body, style.margin_x + 22, y + 65, max_w - 44, style.ink, line_gap=7)
        y += 196
    pages.append(page)

    # Page 8: summary and questions
    page, draw, y = new_page("07 总结复习", 8)
    y = draw_section_title(draw, h2_font, "3句话总结", style.margin_x, y, style.teal)
    summary = [
        "1. 多模态模型让 AI 不再只处理文字，而是能把照片、语音、视频和文本放进同一个问题里理解。",
        "2. 它的核心不是“多接几个输入口”，而是编码、对齐、融合，让不同形式的信息变成可比较的意义表示。",
        "3. 它能显著提升真实场景中的辅助判断能力，但仍会看错、漏看、误判，所以必须保留证据、校验和责任边界。",
    ]
    for line in summary:
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 120), 20, (248, 250, 252), style.line, 2)
        draw_paragraph(draw, body_font, line, style.margin_x + 24, y + 26, max_w - 48, style.ink, line_gap=7)
        y += 140

    y += 12
    y = draw_section_title(draw, h2_font, "3个复习问题", style.margin_x, y, style.blue)
    questions = (
        "1. 为什么说多模态模型不是简单地“把图片转成一句文字描述”？请用异常件照片的例子说明。\n\n"
        "2. 如果一个模型既能看图又能读文字，它还需要“跨模态对齐”吗？为什么？\n\n"
        "3. 在真实业务里，为什么多模态模型给出的结论仍然需要证据校验和人工责任边界？"
    )
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 390), 24, (255, 255, 255), style.line, 3)
    draw_paragraph(draw, body_font, questions, style.margin_x + 26, y + 28, max_w - 52, style.ink, line_gap=9)
    y += 430
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 196), 24, (247, 252, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 24), "下一步学习建议", font=h2_font, fill=style.teal)
    draw_paragraph(
        draw,
        body_font,
        "学完多模态模型后，适合继续学习视觉语言模型（VLM）、视频生成、世界模型和机器人。"
        "这些主题会继续回答一个问题：AI 如何从“理解信息”走向“理解环境并采取行动”。",
        style.margin_x + 24,
        y + 82,
        max_w - 48,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    pages[0].save(
        out_pdf,
        "PDF",
        resolution=style.dpi,
        save_all=True,
        append_images=pages[1:],
        quality=88,
    )
    return out_pdf


if __name__ == "__main__":
    print(build())
