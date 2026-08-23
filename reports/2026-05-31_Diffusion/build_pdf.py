from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Style:
    dpi: int = 120
    page_w: int = 1240
    page_h: int = 1754
    margin_x: int = 98
    margin_y: int = 86
    ink: tuple[int, int, int] = (15, 23, 42)
    muted: tuple[int, int, int] = (71, 85, 105)
    quiet: tuple[int, int, int] = (100, 116, 139)
    line: tuple[int, int, int] = (226, 232, 240)
    soft: tuple[int, int, int] = (248, 250, 252)
    blue: tuple[int, int, int] = (37, 99, 235)
    teal: tuple[int, int, int] = (13, 148, 136)
    green: tuple[int, int, int] = (22, 163, 74)
    warn: tuple[int, int, int] = (225, 29, 72)
    amber: tuple[int, int, int] = (245, 158, 11)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
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
            y += int(font.size * 0.72)
            continue
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def draw_header(
    draw: ImageDraw.ImageDraw,
    style: Style,
    section: str,
    page_no: int,
    small_font: ImageFont.ImageFont,
) -> None:
    draw.text((style.margin_x, 38), "AI每日深度科普", font=small_font, fill=style.quiet)
    draw.text((style.page_w - style.margin_x - 150, 38), f"{page_no:02d}", font=small_font, fill=style.quiet)
    draw.line((style.margin_x, 70, style.page_w - style.margin_x, 70), fill=style.line, width=2)
    if section:
        draw.text((style.margin_x, 86), section, font=small_font, fill=style.teal)


def draw_footer(
    draw: ImageDraw.ImageDraw,
    style: Style,
    page_no: int,
    tiny_font: ImageFont.ImageFont,
) -> None:
    footer = "2026-05-31  |  Diffusion（扩散模型）  |  让普通人看懂 AI"
    draw.line((style.margin_x, style.page_h - 78, style.page_w - style.margin_x, style.page_h - 78), fill=style.line, width=2)
    draw.text((style.margin_x, style.page_h - 54), footer, font=tiny_font, fill=style.quiet)
    draw.text((style.page_w - style.margin_x - 40, style.page_h - 54), str(page_no), font=tiny_font, fill=style.quiet)


def draw_section_title(
    draw: ImageDraw.ImageDraw,
    style: Style,
    title_font: ImageFont.ImageFont,
    title: str,
    x: int,
    y: int,
    color: tuple[int, int, int] | None = None,
) -> int:
    color = color or style.teal
    draw.rounded_rectangle((x, y + 8, x + 28, y + 36), radius=10, fill=color)
    draw.text((x + 46, y), title, font=title_font, fill=style.ink)
    return y + title_font.size + 22


def draw_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int],
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


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
    pad_x = 15
    pad_y = 9
    w = int(text_width(font, text)) + pad_x * 2
    h = font.size + pad_y * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=bg, outline=outline, width=2)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fg)
    return x + w + 10


def paste_image_fit(
    page: Image.Image,
    img_path: Path,
    x: int,
    y: int,
    max_w: int,
    max_h: int,
    style: Style,
) -> int:
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
    style: Style,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
    steps: list[tuple[str, str]],
    x: int,
    y: int,
    max_w: int,
    accent: tuple[int, int, int],
) -> int:
    for i, (title, body) in enumerate(steps, start=1):
        h = 122
        draw_card(draw, (x, y, x + max_w, y + h), 20, (255, 255, 255), style.line, 2)
        draw.ellipse((x + 18, y + 24, x + 78, y + 84), fill=accent)
        draw.text((x + 39, y + 34), str(i), font=title_font, fill=(255, 255, 255))
        draw.text((x + 98, y + 20), title, font=title_font, fill=style.ink)
        draw_paragraph(draw, body_font, body, x + 98, y + 60, max_w - 124, style.muted, line_gap=5)
        y += h + 16
    return y


def build() -> Path:
    style = Style()
    base = Path(__file__).resolve().parent
    fig_process = base / "diffusion_process_flow.png"
    fig_analogy = base / "diffusion_restore_analogy.png"
    out_pdf = base / "2026-05-31_Diffusion（扩散模型）.pdf"

    title_font = load_font(54, bold=True)
    subtitle_font = load_font(31)
    h2_font = load_font(30, bold=True)
    h3_font = load_font(23, bold=True)
    body_font = load_font(21)
    small_font = load_font(17)
    tiny_font = load_font(15)
    quote_font = load_font(24)

    max_w = style.page_w - style.margin_x * 2
    pages: list[Image.Image] = []

    def new_page(section: str, page_no: int) -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
        page = Image.new("RGB", (style.page_w, style.page_h), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        draw_header(draw, style, section, page_no, tiny_font)
        draw_footer(draw, style, page_no, tiny_font)
        return page, draw, 128

    # Page 1: title page + auto-generated table of contents
    page, draw, y = new_page("", 1)
    hero = (style.margin_x, 132, style.page_w - style.margin_x, 492)
    draw_card(draw, hero, 28, (247, 252, 252), style.line, 3)
    draw.text((style.margin_x + 28, 162), "2026-05-31", font=small_font, fill=style.quiet)
    draw.text((style.margin_x + 28, 205), "Diffusion（扩散模型）", font=title_font, fill=style.ink)
    draw.text((style.margin_x + 28, 285), "为什么 AI 不是“凭空画图”，而是在一步步去噪？", font=subtitle_font, fill=style.blue)
    draw_paragraph(
        draw,
        quote_font,
        "核心一句话：扩散模型的本质，是让 AI 学会把一团噪声逐步还原成有意义的图像、音频或视频。",
        style.margin_x + 28,
        350,
        max_w - 56,
        style.teal,
        line_gap=8,
    )
    bx = style.margin_x + 28
    by = 430
    for label, color in [
        ("高中友好", style.teal),
        ("图像生成", style.blue),
        ("去噪思维", style.green),
        ("常见误区澄清", style.amber),
    ]:
        bx = draw_badge(draw, small_font, label, bx, by, color, (255, 255, 255), style.line)

    y = 555
    y = draw_section_title(draw, style, h2_font, "目录", style.margin_x, y, style.blue)
    toc = [
        ("01", "为什么这个概念重要？", "它解释了图像、视频、音频生成的底层逻辑。"),
        ("02", "一个直观类比", "像从雪花屏里一点点找回画面。"),
        ("03", "工作原理", "训练时加噪，生成时去噪。"),
        ("04", "关键术语解释", "噪声、时间步、潜空间、条件引导、采样器。"),
        ("05", "真实应用案例", "从一句话到一张海报。"),
        ("06", "常见误区", "它不是凭空变魔术，也不是简单复制图片。"),
        ("07", "3句话总结 + 复习问题", "用问题检验是否真正理解。"),
    ]
    for num, title, desc in toc:
        row_h = 98
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + row_h), 18, (255, 255, 255), style.line, 2)
        draw.text((style.margin_x + 20, y + 28), num, font=h3_font, fill=style.teal)
        draw.text((style.margin_x + 92, y + 18), title, font=h3_font, fill=style.ink)
        draw.text((style.margin_x + 92, y + 54), desc, font=small_font, fill=style.muted)
        y += row_h + 14
    pages.append(page)

    # Page 2: why important
    page, draw, y = new_page("01 为什么重要", 2)
    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y, style.teal)
    y = draw_paragraph(
        draw,
        body_font,
        "如果说 Transformer 让 AI 学会了处理文字和上下文，那么扩散模型让 AI 真正走进了“生成视觉世界”的时代。\n\n"
        "今天你看到的 AI 绘画、产品海报、视频生成、图片修复、局部重绘、风格迁移，背后常常都有扩散模型或它的变体。"
        "它解决的不是“怎么找一张图”，而是“怎么从无序噪声里逐步构造出一张符合要求的新图”。\n\n"
        "这很重要，因为普通人最容易误解生成式 AI：\n"
        "- 以为它像搜索引擎，只是把图库里的图拿出来。\n"
        "- 以为它像魔术，一句话就凭空冒出结果。\n"
        "- 以为图像越真实，模型就越懂现实世界。\n\n"
        "扩散模型能帮我们建立一个更准确的直觉：AI 生成不是“一步到位画完”，而是“反复修正错误噪声，让画面逐渐清晰”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 18
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 260), 24, (248, 250, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 22), "它改变了什么？", font=h2_font, fill=style.blue)
    draw_paragraph(
        draw,
        body_font,
        "1) 创作门槛降低：不会画画的人，也能用语言描述视觉想法。\n"
        "2) 设计流程变快：海报、插画、分镜、商品图可以先快速出草图。\n"
        "3) 多模态能力打开：图像、视频、3D、音频生成都能借用“逐步去噪”的思想。\n"
        "4) 风险也变现实：版权、真实性、安全边界、审美同质化，都需要新的规则。",
        style.margin_x + 24,
        y + 78,
        max_w - 48,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    # Page 3: analogy with generated image
    page, draw, y = new_page("02 直观类比", 3)
    y = draw_section_title(draw, style, h2_font, "一个直观类比：从雪花屏里找回画面", style.margin_x, y, style.teal)
    y = draw_paragraph(
        draw,
        body_font,
        "想象你拿到一张被噪点覆盖的老照片。第一眼看，它像电视雪花屏，几乎什么都看不清。\n\n"
        "但如果你是一个经验丰富的修图师，你会做几件事：先判断哪里像边缘，哪里像天空，哪里可能是人的轮廓；"
        "再一点点擦掉不像真实画面的噪声；最后把局部细节补得更自然。\n\n"
        "扩散模型也在做类似的事。它不是突然“画出一张图”，而是从随机噪声开始，反复预测："
        "哪些部分更像噪声，哪些部分更像真实图像结构，然后逐步把噪声减掉。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 22
    y = paste_image_fit(page, fig_analogy, style.margin_x, y, max_w, 690, style)
    draw_paragraph(
        draw,
        small_font,
        "图 1：生活类比。把扩散模型想成“修复一张被噪声盖住的照片”，普通读者就能抓住核心直觉：不断预测噪声、减去噪声、让画面变清楚。",
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=5,
    )
    pages.append(page)

    # Page 4: working principle with generated image
    page, draw, y = new_page("03 工作原理", 4)
    y = draw_section_title(draw, style, h2_font, "工作原理：训练时加噪，生成时去噪", style.margin_x, y, style.blue)
    steps = [
        ("训练第一步：把真实图片逐渐加噪", "模型先看到清晰图片，然后系统故意一步步加入噪声，直到图片几乎变成随机雪花。"),
        ("训练第二步：学习每一步该怎么去噪", "神经网络看到“带噪图片 + 当前噪声程度 + 文字条件”，学习预测应该减掉哪一部分噪声。"),
        ("生成时：从随机噪声开始", "真正使用时，模型不从真实图片开始，而是从一团随机噪声出发，一步步反向去噪。"),
        ("最终：得到符合提示词的新图", "文字提示词像方向盘，引导模型在去噪过程中靠近“雪山湖泊”“科幻城市”“产品海报”等目标。"),
    ]
    y = draw_steps(draw, style, h3_font, small_font, steps, style.margin_x, y, max_w, style.blue)
    y += 6
    y = paste_image_fit(page, fig_process, style.margin_x, y, max_w, 610, style)
    pages.append(page)

    # Page 5: terms
    page, draw, y = new_page("04 关键术语", 5)
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y, style.teal)
    terms = [
        ("噪声（Noise）", "专业解释：随机扰动，通常像彩色雪花点，会遮住图像结构。", "白话解释：照片上铺了一层乱七八糟的雪花。"),
        ("去噪（Denoising）", "专业解释：模型预测并移除噪声，让样本逐步接近真实数据分布。", "白话解释：一点点擦掉错误杂点，让画面越来越像真的。"),
        ("时间步（Timestep）", "专业解释：扩散过程中的第几步，用来表示当前噪声有多重。", "白话解释：修图进度条：现在是非常模糊，还是已经快清楚了。"),
        ("潜空间（Latent Space）", "专业解释：模型常在压缩后的特征空间里生成，再解码成图片。", "白话解释：先在草稿纸上画结构，最后再变成高清成品。"),
        ("条件引导（Conditioning）", "专业解释：用文本、图片、边缘图、姿态等条件约束生成方向。", "白话解释：提示词和参考图就是导航，让模型别乱画。"),
        ("采样器 / 调度器（Sampler / Scheduler）", "专业解释：决定每一步如何从噪声走向更清晰样本的算法。", "白话解释：不同修图路线：有的快，有的细，有的风格更稳定。"),
    ]
    col_w = (max_w - 26) // 2
    left_x = style.margin_x
    right_x = style.margin_x + col_w + 26
    y_left = y
    y_right = y
    for idx, (name, pro, plain) in enumerate(terms):
        x = left_x if idx % 2 == 0 else right_x
        yy = y_left if idx % 2 == 0 else y_right
        box_h = 232
        draw_card(draw, (x, yy, x + col_w, yy + box_h), 20, (255, 255, 255), style.line, 2)
        draw.text((x + 20, yy + 18), name, font=h3_font, fill=style.blue if idx % 2 == 0 else style.teal)
        draw_paragraph(draw, small_font, pro, x + 20, yy + 62, col_w - 40, style.ink, line_gap=5)
        draw_paragraph(draw, small_font, plain, x + 20, yy + 132, col_w - 40, style.muted, line_gap=5)
        if idx % 2 == 0:
            y_left = yy + box_h + 18
        else:
            y_right = yy + box_h + 18
    pages.append(page)

    # Page 6: real application case
    page, draw, y = new_page("05 真实应用", 6)
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例：从一句话到一张活动海报", style.margin_x, y, style.blue)
    y = draw_paragraph(
        draw,
        body_font,
        "假设一家咖啡店要做一张新品海报，提示词是：\n"
        "“清晨阳光下，一杯冰拿铁放在木桌上，旁边有蓝色花朵，画面干净高级。”\n\n"
        "扩散模型大致会这样工作：",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 12
    case_steps = [
        ("1. 理解文字条件", "模型把“冰拿铁、木桌、清晨阳光、蓝色花朵、干净高级”变成可计算的语义线索。"),
        ("2. 从随机噪声开始", "画布一开始没有咖啡、桌子、花朵，只有随机噪声。"),
        ("3. 每一步都问：现在该减掉什么噪声？", "在文字条件引导下，模型逐渐形成杯子的边缘、桌面的材质、光影和背景。"),
        ("4. 最后得到一张完整图像", "结果不是从图库复制一张，而是在学到的图像规律中生成一个新的组合。"),
    ]
    y = draw_steps(draw, style, h3_font, small_font, case_steps, style.margin_x, y, max_w, style.teal)
    y += 10
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 236), 24, (248, 250, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 20), "这对现实工作有什么意义？", font=h2_font, fill=style.teal)
    draw_paragraph(
        draw,
        body_font,
        "它让“视觉创意”从一次性外包，变成可以快速迭代的对话：换背景、换风格、修局部、生成多个方案。"
        "但它也要求使用者更懂审美、版权、真实性和安全边界，因为生成能力越强，责任也越具体。",
        style.margin_x + 24,
        y + 78,
        max_w - 48,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    # Page 7: misconceptions
    page, draw, y = new_page("06 常见误区", 7)
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y, style.warn)
    myths = [
        ("误区 1：扩散模型是在图库里找图", "纠正：它不是传统搜索。它学习的是大量图像中的统计规律，再通过去噪过程生成新样本。"),
        ("误区 2：它是凭空变魔术", "纠正：不是凭空。它依赖训练数据、模型结构、文字条件、采样算法和随机种子。"),
        ("误区 3：提示词越长越好", "纠正：好提示词不是堆形容词，而是清楚说明主体、场景、风格、构图和约束。"),
        ("误区 4：生成步数越多一定越好", "纠正：步数太少可能粗糙，太多也可能浪费时间或带来过度处理；关键是采样器与场景匹配。"),
        ("误区 5：图像逼真就说明 AI 懂现实", "纠正：逼真不等于真实理解。模型会生成合理外观，但可能在物理、文字、细节一致性上犯错。"),
    ]
    for title, body in myths:
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 176), 20, (255, 255, 255), style.line, 2)
        draw.text((style.margin_x + 22, y + 18), title, font=h3_font, fill=style.warn)
        draw_paragraph(draw, body_font, body, style.margin_x + 22, y + 64, max_w - 44, style.ink, line_gap=7)
        y += 194
    pages.append(page)

    # Page 8: summary and review questions
    page, draw, y = new_page("07 总结复习", 8)
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y, style.teal)
    summary = [
        "1) 扩散模型先在训练中学习“如何把被噪声破坏的图像修回来”，再在生成时从随机噪声一步步还原。",
        "2) 文字提示词不是直接画图命令，而是去噪过程的方向盘，帮助模型靠近用户想要的画面。",
        "3) 它不是图库搜索，也不是真正理解世界；它强在生成与修复，弱点在事实、细节一致性和安全边界。",
    ]
    for line in summary:
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 118), 20, (248, 250, 252), style.line, 2)
        draw_paragraph(draw, body_font, line, style.margin_x + 24, y + 26, max_w - 48, style.ink, line_gap=7)
        y += 138

    y += 12
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y, style.blue)
    questions = (
        "1) 为什么说扩散模型不是“一步画图”，而是“多步修复”？请用老照片修复的类比解释。\n\n"
        "2) 如果模型从随机噪声开始，它怎么知道最后要生成“咖啡店海报”而不是“雪山风景”？\n\n"
        "3) 为什么“生成图片看起来很真实”不等于“AI真正理解了现实世界”？请举一个可能出错的细节。"
    )
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 408), 24, (255, 255, 255), style.line, 3)
    draw_paragraph(draw, body_font, questions, style.margin_x + 26, y + 28, max_w - 52, style.ink, line_gap=9)
    y += 448
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 190), 24, (247, 252, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 24), "下一步学习建议", font=h2_font, fill=style.teal)
    draw_paragraph(
        draw,
        body_font,
        "理解扩散模型后，可以继续学习：多模态模型、视频生成、世界模型、AI安全与合成内容检测。"
        "这些主题都围绕一个问题展开：当 AI 可以生成越来越真实的世界，我们如何理解、使用并约束它？",
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
