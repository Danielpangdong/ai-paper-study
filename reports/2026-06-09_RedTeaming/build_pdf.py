from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-09"
CONCEPT_CN = "红队测试"
CONCEPT_EN = "Red Teaming"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"


@dataclass(frozen=True)
class Style:
    dpi: int = 120
    page_w: int = 1240
    page_h: int = 1754
    margin_x: int = 92
    margin_y: int = 84
    ink: tuple[int, int, int] = (15, 23, 42)
    muted: tuple[int, int, int] = (71, 85, 105)
    quiet: tuple[int, int, int] = (100, 116, 139)
    line: tuple[int, int, int] = (226, 232, 240)
    soft: tuple[int, int, int] = (248, 250, 252)
    navy: tuple[int, int, int] = (30, 58, 138)
    teal: tuple[int, int, int] = (13, 148, 136)
    cyan: tuple[int, int, int] = (8, 145, 178)
    green: tuple[int, int, int] = (22, 163, 74)
    amber: tuple[int, int, int] = (217, 119, 6)
    red: tuple[int, int, int] = (225, 29, 72)
    violet: tuple[int, int, int] = (109, 40, 217)


STYLE = Style()


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        ("/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc", 0),
        ("/System/Library/Fonts/PingFang.ttc", 0),
        ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
        ("/System/Library/Fonts/STHeiti Medium.ttc", 0),
        ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 0),
    ]
    for path, index in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size, index=index)
    return ImageFont.load_default()


FONTS = {
    "hero": load_font(74, True),
    "h1": load_font(48, True),
    "h2": load_font(36, True),
    "h3": load_font(28, True),
    "body": load_font(25),
    "body_b": load_font(25, True),
    "small": load_font(20),
    "tiny": load_font(17),
}


def tw(font: ImageFont.ImageFont, text: str) -> int:
    try:
        return int(font.getlength(text))
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
            if tw(font, trial) <= max_w:
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
    line_gap: int = 8,
) -> int:
    for line in wrap_text(font, text, max_w):
        if not line:
            y += int(getattr(font, "size", 22) * 0.72)
            continue
        draw.text((x, y), line, font=font, fill=fill)
        y += getattr(font, "size", 22) + line_gap
    return y


def card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int] = (255, 255, 255),
    outline: tuple[int, int, int] = STYLE.line,
    radius: int = 20,
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int], width: int = 5) -> None:
    draw.line((start[0], start[1], end[0], end[1]), fill=color, width=width)
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) >= abs(ey - sy):
        d = 1 if ex >= sx else -1
        pts = [(ex, ey), (ex - d * 18, ey - 12), (ex - d * 18, ey + 12)]
    else:
        d = 1 if ey >= sy else -1
        pts = [(ex, ey), (ex - 12, ey - d * 18), (ex + 12, ey - d * 18)]
    draw.polygon(pts, fill=color)


def badge(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, fg: tuple[int, int, int], bg: tuple[int, int, int], outline: tuple[int, int, int]) -> int:
    f = FONTS["small"]
    pad_x = 16
    pad_y = 8
    w = tw(f, text) + pad_x * 2
    h = getattr(f, "size", 20) + pad_y * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=bg, outline=outline, width=2)
    draw.text((x + pad_x, y + pad_y - 2), text, font=f, fill=fg)
    return x + w + 10


def page(section: str, page_no: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (STYLE.page_w, STYLE.page_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((STYLE.margin_x, 38), "AI每日深度科普", font=FONTS["small"], fill=STYLE.quiet)
    draw.text((STYLE.page_w - STYLE.margin_x - 152, 38), f"{page_no:02d}", font=FONTS["small"], fill=STYLE.quiet)
    draw.line((STYLE.margin_x, 70, STYLE.page_w - STYLE.margin_x, 70), fill=STYLE.line, width=2)
    if section:
        draw.text((STYLE.margin_x, 86), section, font=FONTS["small"], fill=STYLE.teal)
    footer = f"{DATE}  |  {CONCEPT_FULL}  |  让普通人看懂 AI"
    draw.line((STYLE.margin_x, STYLE.page_h - 78, STYLE.page_w - STYLE.margin_x, STYLE.page_h - 78), fill=STYLE.line, width=2)
    draw.text((STYLE.margin_x, STYLE.page_h - 54), footer, font=FONTS["tiny"], fill=STYLE.quiet)
    draw.text((STYLE.page_w - STYLE.margin_x - 40, STYLE.page_h - 54), str(page_no), font=FONTS["tiny"], fill=STYLE.quiet)
    return img, draw


def section_title(draw: ImageDraw.ImageDraw, title: str, x: int, y: int, color: tuple[int, int, int] = STYLE.teal) -> int:
    draw.rounded_rectangle((x, y + 10, x + 30, y + 42), radius=10, fill=color)
    draw.text((x + 48, y), title, font=FONTS["h2"], fill=STYLE.ink)
    return y + 62


def paste_image_fit(base: Image.Image, img_path: Path, x: int, y: int, max_w: int, max_h: int) -> int:
    img = Image.open(img_path).convert("RGB")
    scale = min(max_w / img.width, max_h / img.height)
    nw = int(img.width * scale)
    nh = int(img.height * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((x - 6, y - 6, x + nw + 6, y + nh + 6), radius=24, fill=(255, 255, 255), outline=STYLE.line, width=3)
    base.paste(img, (x, y))
    return y + nh + 28


def draw_steps(draw: ImageDraw.ImageDraw, steps: list[tuple[str, str]], x: int, y: int, max_w: int, accent: tuple[int, int, int], row_h: int = 118) -> int:
    for i, (title, body) in enumerate(steps, start=1):
        card(draw, (x, y, x + max_w, y + row_h), (255, 255, 255), STYLE.line, 20, 2)
        draw.ellipse((x + 20, y + 28, x + 78, y + 86), fill=accent)
        draw.text((x + 40, y + 36), str(i), font=FONTS["h3"], fill=(255, 255, 255))
        draw.text((x + 102, y + 18), title, font=FONTS["h3"], fill=STYLE.ink)
        draw_paragraph(draw, FONTS["small"], body, x + 102, y + 58, max_w - 130, STYLE.muted, 6)
        y += row_h + 14
    return y


def generate_fire_drill_diagram(path: Path) -> None:
    w, h = 1680, 945
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, h), fill=(248, 250, 252))
    draw.text((72, 54), "AI红队测试：像给 AI 做消防演练", font=load_font(48, True), fill=STYLE.ink)
    draw.text((74, 118), "上线前主动模拟威胁，越早发现问题，越少把风险交给真实用户。", font=load_font(27), fill=STYLE.muted)
    cards = [
        ((78, 230, 420, 620), STYLE.navy, "真实目标", "上线前发现风险\n不要等事故发生"),
        ((486, 230, 828, 620), STYLE.red, "红队角色", "主动扮演挑刺者\n站在攻击者视角"),
        ((894, 230, 1236, 620), STYLE.amber, "测试方式", "诱导、绕过\n压力场景"),
        ((1302, 230, 1644, 620), STYLE.green, "改进结果", "修漏洞、加边界\n再测试"),
    ]
    for idx, (box, color, head, body) in enumerate(cards, start=1):
        card(draw, box, (255, 255, 255), (203, 213, 225), 26, 3)
        x1, y1, x2, _ = box
        draw.ellipse((x1 + 28, y1 + 28, x1 + 88, y1 + 88), fill=color)
        draw.text((x1 + 50, y1 + 38), str(idx), font=load_font(30, True), fill=(255, 255, 255))
        draw.text((x1 + 112, y1 + 34), head, font=load_font(32, True), fill=STYLE.ink)
        draw_paragraph(draw, load_font(29), body, x1 + 36, y1 + 130, x2 - x1 - 72, STYLE.muted, 14)
    for sx in [432, 840, 1248]:
        arrow(draw, (sx, 420), (sx + 42, 420), STYLE.cyan, 7)
    draw.rounded_rectangle((120, 724, 1560, 842), radius=32, fill=(239, 246, 255), outline=(191, 219, 254), width=3)
    draw.text((180, 760), "核心：不是证明 AI 完美，而是尽早发现它哪里会出错。", font=load_font(40, True), fill=STYLE.navy)
    img.save(path, "PNG")


def generate_workflow_diagram(path: Path) -> None:
    w, h = 1680, 945
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((72, 54), "红队测试的工作流：从找风险到修边界", font=load_font(48, True), fill=STYLE.ink)
    draw.text((74, 118), "红队不是一次性打分，而是一轮轮发现问题、修复、再挑战。", font=load_font(27), fill=STYLE.muted)
    steps = [
        (STYLE.navy, "风险地图", "列出可能出错的场景"),
        (STYLE.teal, "设计攻击", "编写诱导与绕过问题"),
        (STYLE.cyan, "执行测试", "记录模型失败方式"),
        (STYLE.amber, "归因分级", "判断严重度和原因"),
        (STYLE.red, "修复复测", "改提示、改规则、改训练"),
    ]
    x = 56
    y = 260
    bw = 292
    for idx, (color, title, body) in enumerate(steps, start=1):
        card(draw, (x, y, x + bw, y + 330), (248, 250, 252), (203, 213, 225), 24, 3)
        draw.rounded_rectangle((x + 92, y - 42, x + 200, y + 22), radius=18, fill=color)
        draw.text((x + 132, y - 32), str(idx), font=load_font(34, True), fill=(255, 255, 255))
        draw.text((x + 36, y + 72), title, font=load_font(32, True), fill=STYLE.ink)
        draw_paragraph(draw, load_font(27), body, x + 36, y + 132, bw - 72, STYLE.muted, 12)
        if idx < len(steps):
            arrow(draw, (x + bw + 12, y + 166), (x + bw + 54, y + 166), STYLE.navy, 7)
        x += bw + 52
    draw.rounded_rectangle((290, 710, 1390, 832), radius=32, fill=(240, 253, 250), outline=(153, 246, 228), width=3)
    draw.text((360, 748), "循环：发现问题 → 修复 → 再挑战 → 再验证", font=load_font(38, True), fill=STYLE.teal)
    img.save(path, "PNG")


SECTIONS = [
    {
        "id": "why",
        "title": "为什么这个概念重要？",
        "body": [
            "红队测试解决的是一个很现实的问题：AI 产品上线前，我们不能只问“它大多数时候能不能答对”，还要问“它在被诱导、压力很大、边界模糊时会不会出错”。",
            "大模型越能办事，出错的代价就越高。一个聊天机器人说错一句话可能只是尴尬；一个 AI 客服泄露隐私、一个代码助手生成危险指令、一个企业 Agent 乱用工具，就可能变成真实损失。",
            "所以红队测试不是给 AI 找茬，而是给系统做体检。它让团队在真实用户遇到问题之前，先主动模拟坏情况，把漏洞、误导、越权和不安全行为找出来。",
        ],
    },
    {
        "id": "analogy",
        "title": "一个直观类比：消防演练",
        "body": [
            "想象一栋新大楼准备营业。管理者不会只看大厅漂不漂亮、灯亮不亮，还会做消防演练：模拟起火、停电、拥挤、有人走错楼梯，看看系统会不会卡住。",
            "红队测试就是 AI 世界里的消防演练。红队成员会故意提出刁钻问题、诱导模型越界、测试它是否泄露敏感信息，或者让它在多轮指令里迷路。",
            "这听起来像“攻击”，但目标不是破坏，而是提前发现薄弱点。越早发现，修复成本越低，真实用户越安全。",
        ],
    },
    {
        "id": "mechanism",
        "title": "工作原理：红队怎样测试 AI？",
        "body": [
            "第一步，先画风险地图。团队会列出模型可能出错的场景，比如隐私泄露、危险建议、偏见歧视、编造事实、工具误用、越权操作。",
            "第二步，设计挑战问题。红队会像压力测试员一样，写出正常问题、诱导问题、绕过限制的问题和多轮对话陷阱。",
            "第三步，执行测试并记录失败方式。重要的不是一句“模型错了”，而是记录它为什么错：是理解错、边界不清、拒答策略过度，还是工具权限太宽。",
            "第四步，按严重度分级并修复。修复可能包括改系统提示、加规则、限制工具权限、补训练数据、调整评测集。最后还要复测，确认问题没有换个形式回来。",
        ],
    },
    {
        "id": "terms",
        "title": "关键术语解释",
        "terms": [
            ("红队", "专业解释：主动模拟攻击者或极端使用者来发现系统弱点的测试团队。", "白话解释：专门站在“挑刺者”角度，提前帮系统找麻烦的人。"),
            ("越狱提示", "专业解释：诱导模型绕过安全规则或开发者限制的输入方式。", "白话解释：像用话术哄模型“别听规则，按我说的做”。"),
            ("风险场景", "专业解释：模型可能造成伤害、误导、泄露或越权的具体使用情境。", "白话解释：提前想象 AI 在什么情况下最容易出事。"),
            ("严重度分级", "专业解释：按影响范围、可复现性和潜在损害给问题排序。", "白话解释：不是所有错误都一样，要先修最危险、最可能发生的。"),
            ("复测", "专业解释：修复后再次运行相同或相似测试，确认风险是否降低。", "白话解释：补完漏洞后再演练一遍，看看门是不是真的关上了。"),
        ],
    },
    {
        "id": "case",
        "title": "真实应用案例：企业 AI 客服上线前",
        "body": [
            "假设一家银行要上线 AI 客服。普通测试会问：它能不能解释账单、能不能引导用户改密码、能不能回答营业时间。",
            "红队测试会问得更尖锐：如果用户套取别人的账户信息，它会不会泄露？如果用户伪装成内部员工，它会不会透露后台流程？如果用户用多轮对话慢慢诱导，它会不会绕过身份验证？",
            "红队发现问题后，团队可能会增加身份校验、限制可查询字段、把高风险请求转人工、给模型加入更明确的拒答边界，并把这些案例加入持续评测。",
            "这就是红队测试的价值：它不只看 AI 会不会回答，还看 AI 在压力和诱导下能不能守住边界。",
        ],
    },
    {
        "id": "mistakes",
        "title": "常见误区",
        "items": [
            ("误区一：红队测试就是黑客攻击。", "不准确。红队会借用攻击视角，但目标是帮助建设者发现风险、改进系统，而不是破坏系统。"),
            ("误区二：做一次红队测试就够了。", "不够。模型、提示词、工具权限和用户行为都会变化，红队测试应该是持续循环。"),
            ("误区三：红队测试只看安全问题。", "不只如此。它也会检查偏见、幻觉、隐私、过度拒答、工具误用和用户体验风险。"),
            ("误区四：通过红队测试就说明 AI 完全安全。", "不能这么理解。红队测试只能发现已想到、已测试的一部分风险，它降低风险，但不等于消除风险。"),
        ],
    },
    {
        "id": "summary",
        "title": "3句话总结",
        "bullets": [
            "红队测试的本质，是在 AI 上线前主动模拟坏情况，提前找出系统薄弱点。",
            "它不是为了证明 AI 完美，而是为了知道 AI 在哪里会失败、失败有多严重、应该先修哪里。",
            "理解红队测试，能帮助普通人看懂 AI 安全、企业上线评估和模型治理为什么必须持续进行。",
        ],
    },
    {
        "id": "quiz",
        "title": "复习问题",
        "bullets": [
            "为什么一个企业 AI 客服不能只做“正常问题回答测试”，还要做红队测试？",
            "如果你要红队测试一个代码助手，你会设计哪些可能危险或越界的场景？",
            "为什么“通过一次红队测试”不等于“这个 AI 一直安全”？",
        ],
    },
]


def ensure_figures() -> tuple[Path, Path]:
    fig1 = ROOT / "chatgpt_red_teaming_fire_drill.png"
    fig2 = ROOT / "chatgpt_red_teaming_workflow.png"
    if not fig1.exists():
        fig1 = ROOT / "red_teaming_fire_drill_fallback.png"
        generate_fire_drill_diagram(fig1)
    if not fig2.exists():
        fig2 = ROOT / "red_teaming_workflow_fallback.png"
        generate_workflow_diagram(fig2)
    return fig1, fig2


def make_cover() -> Image.Image:
    img, draw = page("", 1)
    draw.rectangle((0, 0, STYLE.page_w, STYLE.page_h), fill=(248, 250, 252))
    draw.rounded_rectangle((STYLE.margin_x, 132, STYLE.page_w - STYLE.margin_x, 1520), radius=44, fill=(255, 255, 255), outline=STYLE.line, width=3)
    x = STYLE.margin_x + 62
    y = 210
    y = badge(draw, "AI安全", x, y, STYLE.red, (255, 241, 242), (251, 113, 133))
    y = badge(draw, "上线前评估", y, 210, STYLE.navy, (239, 246, 255), (191, 219, 254))
    badge(draw, "高中生可读", y, 210, STYLE.teal, (240, 253, 250), (153, 246, 228))

    draw.text((x, 330), CONCEPT_CN, font=FONTS["hero"], fill=STYLE.ink)
    draw.text((x, 420), CONCEPT_EN, font=FONTS["h1"], fill=STYLE.navy)
    draw.text((x, 530), "为什么要主动给 AI 找麻烦？", font=FONTS["h2"], fill=STYLE.ink)
    draw.rounded_rectangle((x, 650, STYLE.page_w - STYLE.margin_x - 62, 782), radius=26, fill=(239, 246, 255), outline=(191, 219, 254), width=3)
    draw.text((x + 28, 690), "核心一句话：红队测试是在事故发生前，主动模拟坏情况，找出 AI 的薄弱点。", font=FONTS["body_b"], fill=STYLE.navy)

    idea_y = 925
    for color, title, body in [
        (STYLE.red, "不是故意破坏", "它用攻击视角帮助建设者提前发现风险。"),
        (STYLE.amber, "不是一次打分", "它是发现、修复、复测、再挑战的循环。"),
        (STYLE.teal, "关键是上线前", "问题越早暴露，真实用户越少承担代价。"),
    ]:
        card(draw, (x, idea_y, STYLE.page_w - STYLE.margin_x - 62, idea_y + 124), (255, 255, 255), STYLE.line, 22, 2)
        draw.rounded_rectangle((x + 24, idea_y + 30, x + 72, idea_y + 78), radius=16, fill=color)
        draw.text((x + 96, idea_y + 24), title, font=FONTS["h3"], fill=STYLE.ink)
        draw.text((x + 96, idea_y + 66), body, font=FONTS["small"], fill=STYLE.muted)
        idea_y += 150
    draw.text((STYLE.margin_x + 62, 1440), f"{DATE}  |  每日 AI 概念精讲", font=FONTS["small"], fill=STYLE.quiet)
    return img


def make_toc() -> Image.Image:
    img, draw = page("学习路径", 2)
    y = section_title(draw, "目录：今天要建立的 8 个认知节点", STYLE.margin_x, 156, STYLE.navy)
    toc = [
        ("01", "为什么重要", "上线前主动找风险，而不是上线后被事故教育"),
        ("02", "直观类比", "消防演练：模拟坏情况，验证系统能否扛住"),
        ("03", "工作原理", "风险地图、攻击设计、执行测试、归因分级、修复复测"),
        ("04", "关键术语", "红队、越狱提示、风险场景、严重度分级、复测"),
        ("05", "真实案例", "企业 AI 客服为什么需要红队测试"),
        ("06", "常见误区", "红队不是破坏，也不是一次测试就万事大吉"),
        ("07", "3 句话总结", "把核心认知压缩成可复习的短句"),
        ("08", "复习问题", "用场景问题检查你是否真正理解"),
    ]
    for no, title, desc in toc:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 126), (255, 255, 255), STYLE.line, 20, 2)
        draw.rounded_rectangle((STYLE.margin_x + 24, y + 28, STYLE.margin_x + 88, y + 92), radius=20, fill=(239, 246, 255), outline=(191, 219, 254), width=2)
        draw.text((STYLE.margin_x + 38, y + 42), no, font=FONTS["small"], fill=STYLE.navy)
        draw.text((STYLE.margin_x + 116, y + 24), title, font=FONTS["h3"], fill=STYLE.ink)
        draw.text((STYLE.margin_x + 116, y + 68), desc, font=FONTS["small"], fill=STYLE.muted)
        y += 144
    return img


def make_why_page() -> Image.Image:
    img, draw = page("为什么重要", 3)
    y = section_title(draw, "为什么红队测试值得普通人理解？", STYLE.margin_x, 146, STYLE.red)
    y = draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[0]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 11)
    y += 34
    cards = [
        ("它解决的问题", "让团队看到 AI 在边界、诱导和压力场景下会怎样失败。"),
        ("它改变的认知", "安全不是口号，而是上线前反复挑战出来的工程能力。"),
        ("它的现实意义", "客服、代码、搜索、Agent 和企业工具都需要先发现高风险失败方式。"),
    ]
    for title, body in cards:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 132), (248, 250, 252), STYLE.line, 20, 2)
        draw.text((STYLE.margin_x + 28, y + 24), title, font=FONTS["h3"], fill=STYLE.navy)
        draw.text((STYLE.margin_x + 280, y + 30), body, font=FONTS["body"], fill=STYLE.muted)
        y += 154
    return img


def make_analogy_page(fig_path: Path) -> Image.Image:
    img, draw = page("直观类比", 4)
    y = section_title(draw, "一个直观类比：消防演练", STYLE.margin_x, 126, STYLE.amber)
    y = paste_image_fit(img, fig_path, STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, 600)
    y += 10
    draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[1]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 10)
    return img


def make_mechanism_page(fig_path: Path) -> Image.Image:
    img, draw = page("工作原理", 5)
    y = section_title(draw, "工作原理：红队怎样测试 AI？", STYLE.margin_x, 126, STYLE.cyan)
    y = paste_image_fit(img, fig_path, STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, 570)
    steps = [
        ("画风险地图", "先列出模型可能在什么场景下伤害、误导、泄露或越权。"),
        ("设计挑战问题", "写出诱导、绕过、多轮陷阱和极端压力问题。"),
        ("记录失败方式", "看模型是理解错、边界错、拒答过度，还是工具权限太宽。"),
        ("修复后复测", "改提示、改规则、改训练或改权限，再重新挑战。"),
    ]
    draw_steps(draw, steps, STYLE.margin_x, y + 8, STYLE.page_w - STYLE.margin_x * 2, STYLE.cyan, 112)
    return img


def make_terms_page() -> Image.Image:
    img, draw = page("关键术语", 6)
    y = section_title(draw, "关键术语：专业解释 + 白话解释", STYLE.margin_x, 132, STYLE.violet)
    for term, pro, plain in SECTIONS[3]["terms"]:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 172), (255, 255, 255), STYLE.line, 20, 2)
        draw.text((STYLE.margin_x + 28, y + 22), term, font=FONTS["h3"], fill=STYLE.violet)
        draw.text((STYLE.margin_x + 220, y + 26), pro, font=FONTS["small"], fill=STYLE.ink)
        draw.text((STYLE.margin_x + 220, y + 78), plain, font=FONTS["small"], fill=STYLE.muted)
        y += 190
    return img


def make_case_page() -> Image.Image:
    img, draw = page("真实应用案例", 7)
    y = section_title(draw, "真实应用案例：企业 AI 客服上线前", STYLE.margin_x, 132, STYLE.green)
    y = draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[4]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 10)
    y += 30
    card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 252), (240, 253, 250), (153, 246, 228), 24, 3)
    draw.text((STYLE.margin_x + 34, y + 30), "一个合格红队问题通常要问：", font=FONTS["h3"], fill=STYLE.teal)
    qy = y + 88
    for q in [
        "模型是否可能泄露不该说的信息？",
        "用户能不能用话术绕过身份或权限边界？",
        "修复后，同类问题是否还会换个说法出现？",
    ]:
        draw.ellipse((STYLE.margin_x + 40, qy + 9, STYLE.margin_x + 58, qy + 27), fill=STYLE.teal)
        draw.text((STYLE.margin_x + 76, qy), q, font=FONTS["body"], fill=STYLE.ink)
        qy += 58
    return img


def make_mistakes_page() -> Image.Image:
    img, draw = page("常见误区", 8)
    y = section_title(draw, "常见误区：别把红队测试想窄了", STYLE.margin_x, 132, STYLE.red)
    for title, body in SECTIONS[5]["items"]:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 176), (255, 255, 255), STYLE.line, 20, 2)
        draw.text((STYLE.margin_x + 28, y + 22), title, font=FONTS["h3"], fill=STYLE.red)
        draw_paragraph(draw, FONTS["small"], body, STYLE.margin_x + 28, y + 72, STYLE.page_w - STYLE.margin_x * 2 - 56, STYLE.muted, 6)
        y += 196
    return img


def make_summary_quiz_page() -> Image.Image:
    img, draw = page("总结与复习", 9)
    y = section_title(draw, "3 句话总结", STYLE.margin_x, 132, STYLE.navy)
    for i, item in enumerate(SECTIONS[6]["bullets"], start=1):
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 132), (248, 250, 252), STYLE.line, 20, 2)
        draw.rounded_rectangle((STYLE.margin_x + 24, y + 28, STYLE.margin_x + 82, y + 86), radius=18, fill=STYLE.navy)
        draw.text((STYLE.margin_x + 44, y + 40), str(i), font=FONTS["h3"], fill=(255, 255, 255))
        draw_paragraph(draw, FONTS["body"], item, STYLE.margin_x + 108, y + 24, STYLE.page_w - STYLE.margin_x * 2 - 134, STYLE.ink, 9)
        y += 152
    y += 18
    y = section_title(draw, "复习问题", STYLE.margin_x, y, STYLE.teal)
    for q in SECTIONS[7]["bullets"]:
        draw.ellipse((STYLE.margin_x + 8, y + 10, STYLE.margin_x + 26, y + 28), fill=STYLE.teal)
        y = draw_paragraph(draw, FONTS["body"], q, STYLE.margin_x + 42, y, STYLE.page_w - STYLE.margin_x * 2 - 42, STYLE.ink, 9)
        y += 20
    return img


def html_paragraphs(items: list[str]) -> str:
    return "\n".join(f"<p>{escape(item)}</p>" for item in items)


def build_html(fig1: Path, fig2: Path) -> str:
    toc = "\n".join(f'<a href="#{s["id"]}">{escape(s["title"])}</a>' for s in SECTIONS)
    term_rows = "\n".join(
        f"<tr><th>{escape(term)}</th><td>{escape(pro)}</td><td>{escape(plain)}</td></tr>"
        for term, pro, plain in SECTIONS[3]["terms"]
    )
    mistake_items = "\n".join(
        f"<li><strong>{escape(title)}</strong><br>{escape(body)}</li>"
        for title, body in SECTIONS[5]["items"]
    )
    summary_items = "\n".join(f"<li>{escape(x)}</li>" for x in SECTIONS[6]["bullets"])
    quiz_items = "\n".join(f"<li>{escape(x)}</li>" for x in SECTIONS[7]["bullets"])
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{DATE}_{escape(CONCEPT_FULL)}</title>
  <style>
    :root {{
      --ink: #0f172a; --muted: #475569; --quiet: #64748b; --line: #e2e8f0;
      --soft: #f8fafc; --navy: #1e3a8a; --teal: #0d9488; --amber: #d97706; --red: #e11d48;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      color: var(--ink); background: #f8fafc; line-height: 1.78;
    }}
    header {{ background: #fff; border-bottom: 1px solid var(--line); padding: 56px 24px 42px; }}
    .wrap {{ max-width: 1040px; margin: 0 auto; }}
    .eyebrow {{ color: var(--red); font-weight: 700; letter-spacing: 0; }}
    h1 {{ margin: 16px 0 10px; font-size: clamp(38px, 6vw, 72px); line-height: 1.08; letter-spacing: 0; }}
    .subtitle {{ font-size: 26px; color: var(--muted); margin: 0 0 24px; }}
    .core {{ margin-top: 24px; padding: 18px 22px; border: 1px solid #bfdbfe; background: #eff6ff; border-radius: 8px; font-weight: 700; color: var(--navy); }}
    nav {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin: 28px 0 8px; }}
    nav a {{ color: var(--navy); text-decoration: none; background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 10px 14px; }}
    main {{ padding: 34px 24px 72px; }}
    section {{ max-width: 1040px; margin: 0 auto 28px; background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 28px; }}
    h2 {{ font-size: 32px; line-height: 1.25; margin: 0 0 16px; letter-spacing: 0; }}
    p {{ margin: 12px 0; font-size: 18px; }}
    figure {{ margin: 20px 0; }}
    img {{ display: block; width: 100%; height: auto; border: 1px solid var(--line); border-radius: 8px; background: #fff; }}
    figcaption {{ color: var(--quiet); font-size: 14px; margin-top: 8px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 16px; }}
    th, td {{ border: 1px solid var(--line); padding: 12px; vertical-align: top; }}
    th {{ width: 16%; background: #f8fafc; color: var(--navy); text-align: left; }}
    ul, ol {{ padding-left: 24px; }}
    li {{ margin: 10px 0; font-size: 18px; }}
    .note {{ background: #fff7ed; border: 1px solid #fed7aa; color: #9a3412; border-radius: 8px; padding: 14px 18px; margin-top: 18px; }}
    @media print {{
      body {{ background: #fff; }}
      section {{ break-inside: avoid; border-color: #ddd; }}
      nav a {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <div class="eyebrow">AI每日深度科普 · {DATE}</div>
      <h1>{escape(CONCEPT_CN)}<br><span style="color:var(--navy)">{escape(CONCEPT_EN)}</span></h1>
      <p class="subtitle">为什么要主动给 AI 找麻烦？</p>
      <div class="core">核心一句话：红队测试是在事故发生前，主动模拟坏情况，找出 AI 的薄弱点。</div>
      <nav>{toc}</nav>
    </div>
  </header>
  <main>
    <section id="why"><h2>{escape(SECTIONS[0]["title"])}</h2>{html_paragraphs(SECTIONS[0]["body"])}</section>
    <section id="analogy"><h2>{escape(SECTIONS[1]["title"])}</h2><figure><img src="{fig1.name}" alt="AI红队测试消防演练类比图"><figcaption>消防演练类比：红队测试不是破坏，而是提前发现薄弱点。</figcaption></figure>{html_paragraphs(SECTIONS[1]["body"])}</section>
    <section id="mechanism"><h2>{escape(SECTIONS[2]["title"])}</h2><figure><img src="{fig2.name}" alt="AI红队测试工作流图"><figcaption>红队测试是一轮轮发现、归因、修复和复测的循环。</figcaption></figure>{html_paragraphs(SECTIONS[2]["body"])}</section>
    <section id="terms"><h2>{escape(SECTIONS[3]["title"])}</h2><table><thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead><tbody>{term_rows}</tbody></table></section>
    <section id="case"><h2>{escape(SECTIONS[4]["title"])}</h2>{html_paragraphs(SECTIONS[4]["body"])}<div class="note">红队测试的价值：不只看 AI 会不会回答，还看它在诱导和压力下能不能守住边界。</div></section>
    <section id="mistakes"><h2>{escape(SECTIONS[5]["title"])}</h2><ul>{mistake_items}</ul></section>
    <section id="summary"><h2>{escape(SECTIONS[6]["title"])}</h2><ol>{summary_items}</ol></section>
    <section id="quiz"><h2>{escape(SECTIONS[7]["title"])}</h2><ol>{quiz_items}</ol></section>
  </main>
</body>
</html>
"""


def build() -> None:
    fig1, fig2 = ensure_figures()
    html_path = ROOT / HTML_NAME
    html_path.write_text(build_html(fig1, fig2), encoding="utf-8")

    pages = [
        make_cover(),
        make_toc(),
        make_why_page(),
        make_analogy_page(fig1),
        make_mechanism_page(fig2),
        make_terms_page(),
        make_case_page(),
        make_mistakes_page(),
        make_summary_quiz_page(),
    ]
    pdf_path = ROOT / PDF_NAME
    pages[0].save(pdf_path, "PDF", resolution=STYLE.dpi, save_all=True, append_images=pages[1:])
    print(pdf_path)
    print(html_path)
    print(fig1)
    print(fig2)


if __name__ == "__main__":
    build()
