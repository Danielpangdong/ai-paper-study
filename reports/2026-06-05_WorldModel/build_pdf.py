from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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


def load_font(size: int) -> ImageFont.FreeTypeFont:
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


def draw_header(draw: ImageDraw.ImageDraw, section: str, page_no: int, small_font: ImageFont.ImageFont) -> None:
    style = STYLE
    draw.text((style.margin_x, 38), "AI每日深度科普", font=small_font, fill=style.quiet)
    draw.text((style.page_w - style.margin_x - 155, 38), f"{page_no:02d}", font=small_font, fill=style.quiet)
    draw.line((style.margin_x, 70, style.page_w - style.margin_x, 70), fill=style.line, width=2)
    if section:
        draw.text((style.margin_x, 86), section, font=small_font, fill=style.teal)


def draw_footer(draw: ImageDraw.ImageDraw, page_no: int, tiny_font: ImageFont.ImageFont) -> None:
    style = STYLE
    footer = "2026-06-05  |  世界模型（World Model）  |  让普通人看懂 AI"
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


def paste_image_fit(page: Image.Image, img_path: Path, x: int, y: int, max_w: int, max_h: int) -> int:
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
    row_h: int = 116,
) -> int:
    style = STYLE
    for i, (title, body) in enumerate(steps, start=1):
        draw_card(draw, (x, y, x + max_w, y + row_h), 20, (255, 255, 255), style.line, 2)
        draw.ellipse((x + 18, y + 25, x + 78, y + 85), fill=accent)
        draw.text((x + 38, y + 34), str(i), font=title_font, fill=(255, 255, 255))
        draw.text((x + 98, y + 18), title, font=title_font, fill=style.ink)
        draw_paragraph(draw, body_font, body, x + 98, y + 58, max_w - 122, style.muted, line_gap=5)
        y += row_h + 14
    return y


def generate_loop_fallback(path: Path) -> None:
    style = STYLE
    w, h = 1536, 1024
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = load_font(54)
    h2 = load_font(30)
    body = load_font(22)
    tiny = load_font(18)
    draw.text((74, 54), "世界模型：AI 的内心小沙盘", font=title, fill=style.ink)
    draw.text((74, 126), "核心流程：观察世界，建立内部模型，在脑中试跑，选择行动，再用反馈更新模型。", font=body, fill=style.muted)
    nodes = [
        ("观察世界", "传感器、文本、图像、动作记录", style.teal),
        ("建立内部模型", "压缩成可计算的世界表示", style.blue),
        ("在脑中试跑", "模拟多种可能的未来", style.violet),
        ("选择行动", "从结果中选更优方案", style.amber),
        ("观察反馈", "用新结果校正模型", style.green),
    ]
    x, y = 74, 250
    card_w, card_h, gap = 250, 250, 42
    centers = []
    for i, (name, desc, color) in enumerate(nodes, start=1):
        xx = x + (i - 1) * (card_w + gap)
        draw_card(draw, (xx, y, xx + card_w, y + card_h), 24, (248, 250, 252), style.line, 3)
        draw.ellipse((xx + 92, y - 38, xx + 158, y + 28), fill=color)
        draw.text((xx + 115, y - 29), str(i), font=h2, fill=(255, 255, 255))
        draw.text((xx + 42, y + 48), name, font=h2, fill=color)
        draw_paragraph(draw, body, desc, xx + 28, y + 112, card_w - 56, style.ink, line_gap=7)
        centers.append((xx + card_w, y + card_h // 2))
        if i < len(nodes):
            draw_arrow(draw, (xx + card_w + 10, y + card_h // 2), (xx + card_w + gap - 14, y + card_h // 2), color, 7)
    draw.line((x + card_w // 2, y + card_h + 56, x + 4 * (card_w + gap) + card_w // 2, y + card_h + 56), fill=style.teal, width=8)
    draw_arrow(draw, (x + 4 * (card_w + gap) + card_w // 2, y + card_h + 56), (x + card_w // 2, y + card_h + 56), style.teal, 8)
    box = (120, 690, 1416, 870)
    draw_card(draw, box, 28, (239, 246, 255), (191, 219, 254), 3)
    draw.text((162, 724), "像司机在脑中预演路线", font=h2, fill=style.blue)
    draw_paragraph(
        draw,
        body,
        "人看到路况后，会在脑中想象：左转会堵吗？直行会不会撞到障碍？世界模型让 AI 也能先模拟后行动。",
        162,
        780,
        1160,
        style.ink,
        line_gap=8,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=95)


def generate_comparison_fallback(path: Path) -> None:
    style = STYLE
    w, h = 1536, 1024
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = load_font(52)
    h2 = load_font(30)
    h3 = load_font(24)
    body = load_font(20)
    draw.text((78, 54), "世界模型不是普通预测", font=title, fill=style.ink)
    draw.text((78, 122), "真正的价值在于：在内部构建可交互的虚拟世界，比较多种未来再决策。", font=body, fill=style.muted)
    cols = [
        ("只识别现在", "看见箱子在前方，但不知道接下来会怎样。", style.blue),
        ("预测下一步", "猜下一帧可能发生什么，但通常只有单一路径。", style.teal),
        ("试跑多种未来", "模拟绕行、等待、直行等选择，比较风险。", style.amber),
    ]
    col_w = 426
    x0, y0, gap = 70, 220, 46
    for i, (name, desc, color) in enumerate(cols):
        x = x0 + i * (col_w + gap)
        draw_card(draw, (x, y0, x + col_w, y0 + 520), 28, (248, 250, 252), style.line, 3)
        draw.ellipse((x + 24, y0 + 28, x + 84, y0 + 88), fill=color)
        draw.text((x + 46, y0 + 37), str(i + 1), font=h3, fill=(255, 255, 255))
        draw.text((x + 104, y0 + 34), name, font=h2, fill=color)
        draw_paragraph(draw, body, desc, x + 40, y0 + 116, col_w - 80, style.ink, line_gap=7)
        road_y = y0 + 260
        draw.rounded_rectangle((x + 55, road_y, x + col_w - 55, road_y + 130), radius=22, fill=(226, 232, 240), outline=(203, 213, 225), width=2)
        draw.rectangle((x + 172, road_y + 40, x + 254, road_y + 106), fill=(190, 150, 100), outline=(120, 90, 60), width=3)
        draw.rounded_rectangle((x + 158, road_y + 98, x + 270, road_y + 132), radius=18, fill=(15, 23, 42))
        if i == 2:
            for j, (label, yy, c) in enumerate([("A 安全", 430, style.green), ("B 可行", 492, style.amber), ("C 危险", 554, style.red)]):
                draw.line((x + 120, y0 + 395, x + 310, y0 + yy - 210), fill=c, width=5)
                draw.text((x + 250, y0 + yy - 210), label, font=body, fill=c)
        else:
            draw.text((x + 70, y0 + 428), "局限：信息少，容易漏掉风险", font=body, fill=style.red if i == 0 else style.amber)
    warning = (70, 810, 1466, 940)
    draw_card(draw, warning, 28, (255, 241, 242), (254, 205, 211), 3)
    draw.text((112, 846), "误区：世界模型不是全知上帝，也不是无限准确的未来预言。", font=h2, fill=style.red)
    draw.text((112, 894), "它仍受训练数据、计算时间和现实环境限制，需要持续校验。", font=body, fill=style.ink)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=95)


def build() -> Path:
    style = STYLE
    base = Path(__file__).resolve().parent
    fallback_loop = base / "world_model_loop_fallback.png"
    fallback_comparison = base / "world_model_comparison_fallback.png"
    chatgpt_loop = base / "chatgpt_world_model_loop.png"
    chatgpt_comparison = base / "chatgpt_world_model_comparison.png"
    fig_loop = chatgpt_loop if chatgpt_loop.exists() else fallback_loop
    fig_comparison = chatgpt_comparison if chatgpt_comparison.exists() else fallback_comparison
    out_pdf = base / "2026-06-05_世界模型（World Model）.pdf"

    generate_loop_fallback(fallback_loop)
    generate_comparison_fallback(fallback_comparison)

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
    draw.text((style.margin_x + 28, 162), "2026-06-05", font=small_font, fill=style.quiet)
    draw.text((style.margin_x + 28, 205), "世界模型", font=title_font, fill=style.ink)
    draw.text((style.margin_x + 28, 278), "World Model", font=subtitle_font, fill=style.blue)
    draw.text((style.margin_x + 28, 328), "为什么 AI 需要一个“内心小沙盘”？", font=subtitle_font, fill=style.teal)
    draw_paragraph(
        draw,
        quote_font,
        "核心一句话：世界模型的本质，是让 AI 在行动前先在内部模拟世界会怎样变化，再选择更可靠的下一步。",
        style.margin_x + 28,
        382,
        max_w - 56,
        style.ink,
        line_gap=8,
    )
    bx = style.margin_x + 28
    for label, color in [
        ("高中友好", style.teal),
        ("内部模拟", style.blue),
        ("因果直觉", style.violet),
        ("机器人与视频", style.amber),
    ]:
        bx = draw_badge(draw, small_font, label, bx, 445, color, (255, 255, 255), style.line)

    y = 570
    y = draw_section_title(draw, h2_font, "目录（自动生成）", style.margin_x, y, style.blue)
    toc = [
        ("01", "为什么这个概念重要？", "AI 从看懂信息，走向理解环境会如何变化。"),
        ("02", "一个直观类比", "像司机在脑中预演路线，先想后动。"),
        ("03", "工作原理", "观察、建模、试跑、选择、反馈。"),
        ("04", "关键术语解释", "状态、动作、预测、模拟、规划、反馈。"),
        ("05", "真实应用案例", "仓库机器人如何绕开障碍。"),
        ("06", "常见误区", "世界模型不是全知上帝，也不是 AGI。"),
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
        "很多 AI 已经能识别图片、生成文字、回答问题。但如果要让 AI 帮人开车、操作机器人、生成连贯视频、安排多步骤任务，"
        "光“看见现在”还不够。它还要能判断：如果我这样做，接下来可能会发生什么？\n\n"
        "世界模型解决的核心问题，就是让 AI 建立一个对环境变化的内部理解。它像一个小沙盘：AI 可以在里面试跑几种可能，"
        "比较风险和收益，然后再决定真实世界中的行动。\n\n"
        "这对 AI 行业很关键，因为未来很多应用不只是聊天，而是要进入动态世界：自动驾驶要预测路人和车辆，机器人要避免碰撞，"
        "视频生成要保持物体运动合理，Agent 要规划多步任务。世界模型就是把“感知”推向“预演和决策”的桥。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 18
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 344), 24, (248, 250, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 22), "它改变了什么？", font=h2_font, fill=style.blue)
    change = (
        "1. 从识别变成理解变化：不只回答“这是什么”，还要回答“接下来会怎样”。\n"
        "2. 从单步反应变成多步规划：先比较几条路，再选择更安全的方案。\n"
        "3. 从被动工具走向行动系统：机器人、自动驾驶和多步骤 Agent 都需要它。\n"
        "4. 从生成好看内容走向生成合理世界：视频里物体不能乱飞，因果关系要站得住。"
    )
    draw_paragraph(draw, body_font, change, style.margin_x + 24, y + 82, max_w - 48, style.ink, line_gap=8)
    pages.append(page)

    # Page 3: analogy
    page, draw, y = new_page("02 直观类比", 3)
    y = draw_section_title(draw, h2_font, "一个直观类比：司机脑中的路线预演", style.margin_x, y, style.teal)
    y = draw_paragraph(
        draw,
        body_font,
        "你开车时看到前面有施工、旁边有行人、远处信号灯快变红。你不会只识别“这里有车、那里有人”。"
        "你会在脑中快速预演：如果直行会不会堵住？如果左转会不会碰到行人？如果等三秒是不是更安全？\n\n"
        "这就是人类很自然的“世界模型”。我们脑子里有一个简化版世界，能预测物体会怎么动，动作会带来什么后果。"
        "它不完美，但足够帮助我们做出更可靠的选择。\n\n"
        "世界模型给 AI 的能力也类似：让 AI 不只是被动看见，而是在内部先试一试。"
        "它让 AI 从“拍照识别员”更接近“会提前想后果的助手”。",
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
        ("看到路况、行人、信号灯", "观察世界"),
        ("脑中形成简化地图", "内部状态表示"),
        ("想象几条路线的后果", "模拟未来"),
        ("选择安全路线并继续观察", "行动与反馈"),
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
        "抓住这个直觉就够了：世界模型不是记住世界的每个细节，而是保留对决策有用的结构，让 AI 能先想象后行动。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    # Page 4: working principle with figure
    page, draw, y = new_page("03 工作原理", 4)
    y = draw_section_title(draw, h2_font, "工作原理：在脑中先试跑，再真实行动", style.margin_x, y, style.blue)
    y = paste_image_fit(page, fig_loop, style.margin_x, y, max_w, 690)
    draw_paragraph(
        draw,
        small_font,
        "图 1：世界模型的闭环。AI 先观察环境，建立内部表示，在模型里模拟多种可能结果，选择行动，然后用真实反馈修正自己的内部模型。",
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=5,
    )
    y += 72
    steps = [
        ("第一步：观察当前状态", "收集文字、图像、传感器、历史动作等信息，判断现在处在什么局面。"),
        ("第二步：压缩成内部模型", "不保存全部细节，而是提取位置、关系、速度、目标、约束等关键结构。"),
        ("第三步：在脑中模拟未来", "尝试不同动作，预测几种可能结果，而不是只猜一个下一帧。"),
        ("第四步：行动并用反馈更新", "执行更优方案，再看真实结果是否符合预期，持续修正模型。"),
    ]
    draw_steps(draw, h3_font, small_font, steps, style.margin_x, y, max_w, style.blue, row_h=115)
    pages.append(page)

    # Page 5: terms
    page, draw, y = new_page("04 关键术语", 5)
    y = draw_section_title(draw, h2_font, "关键术语解释", style.margin_x, y, style.teal)
    terms = [
        ("状态（State）", "专业解释：系统在某一时刻的关键信息表示。", "白话解释：当前局面，比如箱子在哪、机器人在哪、目标在哪。"),
        ("动作（Action）", "专业解释：智能体可以采取的操作或决策。", "白话解释：下一步要做什么，比如左转、等待、绕行、抓取。"),
        ("预测（Prediction）", "专业解释：根据当前状态估计未来状态或结果。", "白话解释：猜一猜如果继续这样，会发生什么。"),
        ("模拟（Simulation）", "专业解释：在内部模型中试运行多种可能过程。", "白话解释：先在脑子里演一遍，不马上在现实里冒险。"),
        ("规划（Planning）", "专业解释：比较多个动作序列，选择更符合目标的方案。", "白话解释：不是走一步看一步，而是先想几步。"),
        ("反馈（Feedback）", "专业解释：用真实结果修正模型的预测误差。", "白话解释：发现想错了，就改地图、改经验、下次更准。"),
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
    y = draw_section_title(draw, h2_font, "真实应用案例：仓库机器人如何绕开障碍", style.margin_x, y, style.blue)
    y = draw_paragraph(
        draw,
        body_font,
        "想象一个仓库机器人正在送货，前方突然出现一个纸箱。如果它只是识别“前面有箱子”，还不够。"
        "它需要判断：直接过去会撞吗？左边能绕吗？右边会不会堵住通道？停下来等人搬走是不是更好？\n\n"
        "世界模型的价值，就是让机器人先在内部试跑这些方案，再选择风险更低、效率更高的一条。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 22
    y = paste_image_fit(page, fig_comparison, style.margin_x, y, max_w, 690)
    draw_paragraph(
        draw,
        small_font,
        "图 2：只识别现在、预测下一步、在脑中试跑多种未来，这三者不是一回事。世界模型更像一个能比较路径风险的内部模拟器。",
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=5,
    )
    y += 72
    case_steps = [
        ("看见当前障碍", "识别箱子、货架、通道宽度和机器人位置。"),
        ("模拟几种路线", "左绕、右绕、等待、直行，每条路径可能有不同风险。"),
        ("选择并校正", "执行更安全方案，同时根据真实反馈更新对环境的理解。"),
    ]
    draw_steps(draw, h3_font, small_font, case_steps, style.margin_x, y, max_w, style.teal, row_h=118)
    pages.append(page)

    # Page 7: misconceptions
    page, draw, y = new_page("06 常见误区", 7)
    y = draw_section_title(draw, h2_font, "常见误区（非常重要）", style.margin_x, y, style.red)
    myths = [
        ("误区 1：世界模型就是“预测下一帧”", "纠正：预测下一帧只是低层能力。真正有用的是理解状态、动作和后果，能比较多种未来。"),
        ("误区 2：世界模型等于真实世界的完整复制", "纠正：它是简化模型，只保留对任务有用的信息。像地图不等于城市，但能帮助导航。"),
        ("误区 3：有了世界模型，AI 就能准确预知未来", "纠正：现实有随机性和未知因素，模型也会错。它只能提高决策质量，不提供绝对预言。"),
        ("误区 4：世界模型只属于机器人", "纠正：视频生成、游戏 AI、自动驾驶、科学模拟、多步骤 Agent 规划，都可能需要世界模型。"),
        ("误区 5：世界模型就是 AGI", "纠正：它是通向更强行动能力的重要组件，但不是通用智能本身，更不自动拥有责任判断。"),
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
        "1. 世界模型让 AI 不只是看见当前信息，而是能形成一个可计算的内部世界，用来理解变化和后果。",
        "2. 它的核心价值是先在脑中试跑多种未来，再选择更可靠的行动，这对机器人、自动驾驶、视频生成和多步骤 Agent 都很关键。",
        "3. 世界模型不是全知上帝，它会受数据、计算和现实环境限制，所以真实应用中必须持续反馈、校验和设置边界。",
    ]
    for line in summary:
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 120), 20, (248, 250, 252), style.line, 2)
        draw_paragraph(draw, body_font, line, style.margin_x + 24, y + 26, max_w - 48, style.ink, line_gap=7)
        y += 140

    y += 12
    y = draw_section_title(draw, h2_font, "3个复习问题", style.margin_x, y, style.blue)
    questions = (
        "1. 为什么说“识别前方有纸箱”和“知道应该怎么绕开纸箱”不是同一种能力？\n\n"
        "2. 如果世界模型只是一个简化版内部世界，它为什么仍然能帮助 AI 做更好的决策？\n\n"
        "3. 在自动驾驶或仓库机器人里，为什么世界模型的预测结果仍然需要真实反馈来不断修正？"
    )
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 390), 24, (255, 255, 255), style.line, 3)
    draw_paragraph(draw, body_font, questions, style.margin_x + 26, y + 28, max_w - 52, style.ink, line_gap=9)
    y += 430
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 196), 24, (247, 252, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 24), "下一步学习建议", font=h2_font, fill=style.teal)
    draw_paragraph(
        draw,
        body_font,
        "学完世界模型后，适合继续学习视频生成、强化学习、机器人控制和自动驾驶。"
        "这些主题会继续回答一个问题：AI 如何从“理解世界”走向“在世界中可靠行动”。",
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
