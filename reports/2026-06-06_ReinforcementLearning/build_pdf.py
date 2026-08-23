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
    footer = "2026-06-06  |  强化学习（Reinforcement Learning）  |  让普通人看懂 AI"
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
    w, h = 1536, 864
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = load_font(54)
    h2 = load_font(30)
    body = load_font(22)
    draw.text((70, 52), "强化学习：AI 如何通过反馈学会行动", font=title, fill=style.ink)
    draw.text((70, 120), "核心闭环：观察状态，选择动作，得到奖励，再调整策略。", font=body, fill=style.muted)
    nodes = [
        ("状态 State", "当前局面", style.amber, (160, 300)),
        ("智能体 Agent", "做选择的 AI", style.blue, (600, 190)),
        ("动作 Action", "下一步怎么做", style.blue, (1030, 300)),
        ("环境 Environment", "行动发生的世界", style.teal, (1030, 560)),
        ("奖励 Reward", "结果好坏的信号", style.green, (600, 660)),
    ]
    centers: list[tuple[int, int]] = []
    for name, desc, color, (x, y) in nodes:
        draw.ellipse((x - 105, y - 105, x + 105, y + 105), fill=(248, 250, 252), outline=color, width=5)
        draw.text((x - int(text_width(h2, name) / 2), y - 28), name, font=h2, fill=color)
        draw.text((x - int(text_width(body, desc) / 2), y + 34), desc, font=body, fill=style.ink)
        centers.append((x, y))
    for start, end, color in [
        (centers[0], centers[1], style.amber),
        (centers[1], centers[2], style.blue),
        (centers[2], centers[3], style.teal),
        (centers[3], centers[4], style.green),
        (centers[4], centers[0], style.teal),
    ]:
        draw_arrow(draw, start, end, color, 9)
    box = (155, 715, 1380, 815)
    draw_card(draw, box, 28, (239, 246, 255), (191, 219, 254), 3)
    draw.text((205, 744), "核心：不是背答案，而是在试错中学会更好的选择", font=h2, fill=style.blue)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=95)


def generate_game_fallback(path: Path) -> None:
    style = STYLE
    w, h = 1536, 864
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = load_font(54)
    h2 = load_font(28)
    body = load_font(21)
    draw.text((70, 52), "直观类比：学生练游戏过关", font=title, fill=style.ink)
    draw.text((70, 120), "用游戏学习的过程，理解强化学习的奖励信号如何塑造行为。", font=body, fill=style.muted)
    steps = [
        ("1 第一次乱试", "容易撞墙、掉坑、失败", style.blue),
        ("2 看到反馈", "哪里扣分，哪里得分", style.teal),
        ("3 调整策略", "少踩坑，多拿分", style.amber),
        ("4 反复练习", "形成更稳定的打法", style.blue),
    ]
    x0, y0, card_w, card_h, gap = 55, 220, 340, 420, 35
    for i, (title_txt, desc, color) in enumerate(steps):
        x = x0 + i * (card_w + gap)
        draw_card(draw, (x, y0, x + card_w, y0 + card_h), 24, (248, 250, 252), style.line, 3)
        draw.rounded_rectangle((x, y0, x + card_w, y0 + 72), radius=24, fill=color)
        draw.text((x + 26, y0 + 18), title_txt, font=h2, fill=(255, 255, 255))
        screen = (x + 44, y0 + 112, x + card_w - 44, y0 + 268)
        draw.rounded_rectangle(screen, radius=18, fill=(226, 232, 240), outline=(148, 163, 184), width=3)
        draw.rectangle((screen[0] + 24, screen[3] - 48, screen[2] - 24, screen[3] - 24), fill=(34, 197, 94))
        draw.rectangle((screen[0] + 80, screen[3] - 82, screen[0] + 130, screen[3] - 48), fill=style.amber)
        if i in (0, 1):
            draw.polygon([(screen[0] + 165, screen[3] - 24), (screen[0] + 190, screen[3] - 84), (screen[0] + 215, screen[3] - 24)], fill=style.red)
        if i in (2, 3):
            draw.ellipse((screen[0] + 190, screen[1] + 46, screen[0] + 215, screen[1] + 71), fill=(234, 179, 8))
            draw.polygon([(screen[2] - 84, screen[3] - 24), (screen[2] - 84, screen[3] - 95), (screen[2] - 34, screen[3] - 72), (screen[2] - 84, screen[3] - 50)], fill=style.green)
        draw_paragraph(draw, body, desc, x + 32, y0 + 310, card_w - 64, style.ink, line_gap=7)
        if i < 3:
            draw_arrow(draw, (x + card_w + 6, y0 + card_h // 2), (x + card_w + gap - 7, y0 + card_h // 2), style.blue, 6)
    box = (70, 705, 1466, 815)
    draw_card(draw, box, 28, (240, 253, 250), (153, 246, 228), 3)
    draw.text((120, 740), "像训练 AI：奖励信号会塑造行为，但奖励设计错了，行为也会跑偏。", font=h2, fill=style.teal)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=95)


def build() -> Path:
    style = STYLE
    base = Path(__file__).resolve().parent
    fallback_loop = base / "rl_feedback_loop_fallback.png"
    fallback_game = base / "rl_game_analogy_fallback.png"
    chatgpt_loop = base / "chatgpt_rl_feedback_loop.png"
    chatgpt_game = base / "chatgpt_rl_game_analogy.png"
    fig_loop = chatgpt_loop if chatgpt_loop.exists() else fallback_loop
    fig_game = chatgpt_game if chatgpt_game.exists() else fallback_game
    out_pdf = base / "2026-06-06_强化学习（Reinforcement Learning）.pdf"

    generate_loop_fallback(fallback_loop)
    generate_game_fallback(fallback_game)

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
    draw.text((style.margin_x + 28, 162), "2026-06-06", font=small_font, fill=style.quiet)
    draw.text((style.margin_x + 28, 205), "强化学习", font=title_font, fill=style.ink)
    draw.text((style.margin_x + 28, 278), "Reinforcement Learning", font=subtitle_font, fill=style.blue)
    draw.text((style.margin_x + 28, 328), "为什么 AI 能在试错中越做越好？", font=subtitle_font, fill=style.teal)
    draw_paragraph(
        draw,
        quote_font,
        "核心一句话：强化学习的本质，是让 AI 像练游戏一样，通过行动后的奖励和惩罚，逐步学会更好的选择。",
        style.margin_x + 28,
        382,
        max_w - 56,
        style.ink,
        line_gap=8,
    )
    bx = style.margin_x + 28
    for label, color in [
        ("高中友好", style.teal),
        ("奖励反馈", style.blue),
        ("行动决策", style.violet),
        ("机器人与Agent", style.amber),
    ]:
        bx = draw_badge(draw, small_font, label, bx, 445, color, (255, 255, 255), style.line)

    y = 570
    y = draw_section_title(draw, h2_font, "目录（自动生成）", style.margin_x, y, style.blue)
    toc = [
        ("01", "为什么这个概念重要？", "AI 不只要会回答，还要会在环境中做选择。"),
        ("02", "一个直观类比", "像学生练游戏过关，靠反馈修正打法。"),
        ("03", "工作原理", "智能体、环境、动作、奖励、策略。"),
        ("04", "关键术语解释", "用白话拆开强化学习的核心词。"),
        ("05", "真实应用案例", "AlphaGo 如何从自我对弈中学会下棋。"),
        ("06", "常见误区", "强化学习不是普通监督学习，也不是万能自学。"),
        ("07", "3句话总结 + 复习问题", "检查是否真正理解奖励如何塑造行为。"),
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
        "很多人第一次接触 AI，会把它想成“会背很多答案的机器”。但现实中的许多 AI 任务，并不是背答案就够了。"
        "自动驾驶要决定什么时候刹车，机器人要决定先抓哪个物体，游戏 AI 要决定下一步怎么走，Agent 要决定先查资料还是先调用工具。\n\n"
        "这些任务的共同点是：AI 必须行动，而行动会改变局面。强化学习解决的就是这个问题：当没有标准答案时，"
        "AI 能不能通过一次次尝试和反馈，学会哪种行为更有价值。\n\n"
        "它之所以重要，是因为 AI 时代不只需要“会说”的模型，也需要“会做”的系统。强化学习把 AI 从被动答题，推向主动决策。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 18
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 362), 24, (248, 250, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 22), "它改变了什么？", font=h2_font, fill=style.blue)
    change = (
        "1. 从“给答案”变成“做选择”：AI 学会在多种行动里挑更好的。\n"
        "2. 从“老师逐题批改”变成“结果驱动”：不必每一步都有标准答案，只要最终结果能打分。\n"
        "3. 从“短期反应”变成“长期收益”：有些好选择当下不舒服，但能带来更好的未来。\n"
        "4. 从“静态模型”走向“行动系统”：机器人、游戏、自动驾驶、多步骤 Agent 都离不开它。"
    )
    draw_paragraph(draw, body_font, change, style.margin_x + 24, y + 82, max_w - 48, style.ink, line_gap=8)
    pages.append(page)

    # Page 3: analogy with figure
    page, draw, y = new_page("02 直观类比", 3)
    y = draw_section_title(draw, h2_font, "一个直观类比：学生练游戏过关", style.margin_x, y, style.teal)
    y = draw_paragraph(
        draw,
        body_font,
        "想象一个学生第一次玩闯关游戏。他并不知道最佳路线，只能先试。踩到尖刺扣分，被怪物打败扣分，捡到金币加分，"
        "到达终点加很多分。玩几轮后，他会慢慢学会：哪里要跳，哪里要等，哪里值得冒险。\n\n"
        "强化学习就是类似的过程。AI 不一定有人告诉它“每一步标准答案是什么”，但它能看到行动后的结果。"
        "奖励像分数，惩罚像扣分。分数反复塑造行为，最后形成一套更稳定的策略。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 24
    y = paste_image_fit(page, fig_game, style.margin_x, y, max_w, 620)
    draw_paragraph(
        draw,
        small_font,
        "图 1：游戏过关类比。强化学习不是把答案塞给 AI，而是让它在环境反馈中逐步调整行为。",
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=5,
    )
    y += 70
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 216), 24, (255, 251, 235), (253, 230, 138), 3)
    draw.text((style.margin_x + 28, y + 26), "抓住一个直觉", font=h2_font, fill=style.amber)
    draw_paragraph(
        draw,
        body_font,
        "强化学习真正学习的不是“题库答案”，而是“在某种局面下，哪种行动更可能带来好结果”。这就是它和普通背答案最大的不同。",
        style.margin_x + 28,
        y + 86,
        max_w - 56,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    # Page 4: working principle with figure
    page, draw, y = new_page("03 工作原理", 4)
    y = draw_section_title(draw, h2_font, "工作原理：奖励如何塑造行为", style.margin_x, y, style.blue)
    y = paste_image_fit(page, fig_loop, style.margin_x, y, max_w, 620)
    draw_paragraph(
        draw,
        small_font,
        "图 2：强化学习闭环。AI 观察状态，选择动作，环境给出新状态和奖励，AI 再更新自己的策略。",
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=5,
    )
    y += 70
    steps = [
        ("第一步：看清当前状态", "AI 先判断现在是什么局面：位置、规则、目标、限制、历史动作等。"),
        ("第二步：根据策略选择动作", "策略像一套打法，告诉 AI 在当前局面下更倾向于做什么。"),
        ("第三步：得到奖励或惩罚", "环境反馈结果：成功加分，失败扣分，接近目标也可能有小奖励。"),
        ("第四步：更新策略", "如果某种行为经常带来好结果，就增加它的概率；如果经常吃亏，就减少它。"),
    ]
    draw_steps(draw, h3_font, small_font, steps, style.margin_x, y, max_w, style.blue, row_h=115)
    pages.append(page)

    # Page 5: terms
    page, draw, y = new_page("04 关键术语", 5)
    y = draw_section_title(draw, h2_font, "关键术语解释", style.margin_x, y, style.teal)
    terms = [
        ("智能体（Agent）", "专业解释：在环境中观察、决策并执行动作的系统。", "白话解释：正在玩游戏或做任务的 AI 玩家。"),
        ("环境（Environment）", "专业解释：智能体行动所在的外部系统，会返回状态和奖励。", "白话解释：游戏地图、道路、仓库、网页工具都可以是环境。"),
        ("奖励（Reward）", "专业解释：衡量一次行动结果好坏的数值反馈。", "白话解释：加分、扣分、成功、失败，是 AI 学习方向的信号。"),
        ("策略（Policy）", "专业解释：从状态到动作的决策规则或概率分布。", "白话解释：AI 的打法：看到这种局面，下一步倾向于怎么做。"),
        ("探索（Exploration）", "专业解释：尝试尚不确定的动作，以发现更好选择。", "白话解释：别总走老路，偶尔试试新路线，也许能拿更高分。"),
        ("利用（Exploitation）", "专业解释：选择当前已知收益较高的动作。", "白话解释：已经知道这招有效，就先用这招稳定拿分。"),
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
    y = draw_section_title(draw, h2_font, "真实应用案例：AlphaGo 如何学会下棋", style.margin_x, y, style.blue)
    y = draw_paragraph(
        draw,
        body_font,
        "围棋很难靠穷举解决，因为可能的局面太多。AlphaGo 的一个关键思路，是让 AI 通过大量对弈来评估局面、选择落子，"
        "并从输赢结果中改进自己的判断。\n\n"
        "这很像一个人反复复盘：这手棋让局面更好，下一次可以多考虑；那手棋导致失败，下一次要避免。"
        "强化学习在这里的作用，是把“最终输赢”和“中途局面价值”连接起来，让 AI 逐渐学会更强的长期决策。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 24
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 562), 26, (248, 250, 252), style.line, 3)
    draw.text((style.margin_x + 28, y + 28), "把 AlphaGo 拆成普通人能懂的 4 步", font=h2_font, fill=style.teal)
    app_steps = [
        ("观察棋盘", "当前棋子分布就是状态。"),
        ("选择落子", "下一手下在哪里就是动作。"),
        ("评估好坏", "局面更有利是正反馈，最终获胜是强奖励。"),
        ("改进打法", "反复对弈后，模型更会判断长期价值。"),
    ]
    yy = y + 96
    for idx, (title, body) in enumerate(app_steps, start=1):
        draw_card(draw, (style.margin_x + 34, yy, style.page_w - style.margin_x - 34, yy + 88), 18, (255, 255, 255), style.line, 2)
        draw.ellipse((style.margin_x + 56, yy + 20, style.margin_x + 108, yy + 72), fill=style.blue if idx < 4 else style.green)
        draw.text((style.margin_x + 75, yy + 30), str(idx), font=h3_font, fill=(255, 255, 255))
        draw.text((style.margin_x + 132, yy + 18), title, font=h3_font, fill=style.ink)
        draw.text((style.margin_x + 132, yy + 52), body, font=small_font, fill=style.muted)
        yy += 106
    y += 598
    draw_paragraph(
        draw,
        body_font,
        "同样的思想也能迁移到机器人控制、推荐系统、自动驾驶仿真、多步骤 Agent 训练：只要能定义环境、动作和奖励，就可能用强化学习改进行为。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    # Page 7: misconceptions
    page, draw, y = new_page("06 常见误区", 7)
    y = draw_section_title(draw, h2_font, "常见误区（非常重要）", style.margin_x, y, style.red)
    myths = [
        ("误区 1：强化学习就是普通监督学习", "纠正：监督学习像老师逐题给答案；强化学习更像练习后看分数，不一定知道每一步标准答案。"),
        ("误区 2：奖励越简单越好", "纠正：奖励设计错了，AI 会学会钻空子。比如只奖励速度，可能牺牲安全。"),
        ("误区 3：让 AI 自己试错就一定能变强", "纠正：现实试错很贵也很危险，常需要模拟环境、边界约束和人工检查。"),
        ("误区 4：强化学习只适合游戏", "纠正：游戏是好训练场，但机器人、物流调度、资源分配和 Agent 工具使用也能用到相关思想。"),
        ("误区 5：强化学习等于让 AI 拥有目标感", "纠正：AI 只是在优化人设定的奖励信号。奖励不等于价值观，更不等于真正理解人类意图。"),
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
        "1. 强化学习让 AI 在没有逐步标准答案的情况下，通过行动后的奖励和惩罚，学会更好的决策策略。",
        "2. 它的核心不是“背答案”，而是“在某种局面下选择什么动作更可能带来长期好结果”。",
        "3. 强化学习很强，但奖励设计、试错成本和安全边界决定了它能否可靠落地。"
    ]
    for line in summary:
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 120), 20, (248, 250, 252), style.line, 2)
        draw_paragraph(draw, body_font, line, style.margin_x + 24, y + 26, max_w - 48, style.ink, line_gap=7)
        y += 140

    y += 12
    y = draw_section_title(draw, h2_font, "3个复习问题", style.margin_x, y, style.blue)
    questions = (
        "1. 为什么说“老师告诉每一步正确答案”和“做完后根据分数调整打法”是两种不同学习方式？\n\n"
        "2. 如果一个送货机器人只被奖励“越快越好”，可能会学出哪些危险行为？这说明奖励设计为什么重要？\n\n"
        "3. 为什么强化学习常常需要模拟环境，而不是直接在真实道路、真实仓库或真实用户面前随便试错？"
    )
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 390), 24, (255, 255, 255), style.line, 3)
    draw_paragraph(draw, body_font, questions, style.margin_x + 26, y + 28, max_w - 52, style.ink, line_gap=9)
    y += 430
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 196), 24, (247, 252, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 24), "下一步学习建议", font=h2_font, fill=style.teal)
    draw_paragraph(
        draw,
        body_font,
        "学完世界模型和强化学习后，适合继续学习机器人控制、视频生成和 AI 安全。"
        "这些主题会继续回答：当 AI 开始行动时，怎样让它既有效，又可靠。",
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
    pdf = build()
    print(pdf)
