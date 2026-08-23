from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-11"
CONCEPT_CN = "AI安全评估"
CONCEPT_EN = "AI Safety Evaluation"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"


@dataclass(frozen=True)
class Style:
    dpi: int = 120
    page_w: int = 1240
    page_h: int = 1754
    margin_x: int = 92
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
    "hero": load_font(72, True),
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


def badge(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    fg: tuple[int, int, int],
    bg: tuple[int, int, int],
    outline: tuple[int, int, int],
) -> int:
    font = FONTS["small"]
    pad_x = 16
    pad_y = 8
    w = tw(font, text) + pad_x * 2
    h = getattr(font, "size", 20) + pad_y * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=bg, outline=outline, width=2)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fg)
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
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((x - 6, y - 6, x + nw + 6, y + nh + 6), radius=24, fill=(255, 255, 255), outline=STYLE.line, width=3)
    base.paste(img, (x, y))
    return y + nh + 28


def draw_steps(
    draw: ImageDraw.ImageDraw,
    steps: list[tuple[str, str]],
    x: int,
    y: int,
    max_w: int,
    accent: tuple[int, int, int],
    row_h: int = 110,
) -> int:
    for i, (title, body) in enumerate(steps, start=1):
        card(draw, (x, y, x + max_w, y + row_h), (255, 255, 255), STYLE.line, 20, 2)
        draw.ellipse((x + 20, y + 26, x + 74, y + 80), fill=accent)
        draw.text((x + 39, y + 34), str(i), font=FONTS["h3"], fill=(255, 255, 255))
        draw.text((x + 100, y + 16), title, font=FONTS["h3"], fill=STYLE.ink)
        draw_paragraph(draw, FONTS["small"], body, x + 100, y + 56, max_w - 128, STYLE.muted, 6)
        y += row_h + 13
    return y


SECTIONS = [
    {
        "id": "why",
        "title": "为什么这个概念重要？",
        "body": [
            "AI安全评估解决的是一个现实问题：模型看起来会聊天、会写代码、会调用工具，但它到底会在什么场景里误导用户、泄露隐私、越权操作，或被一句诱导话术带偏？",
            "如果说昨天的 AI 安全护栏像机场安检，今天的安全评估就像给安检系统做压力测试。它不是等事故发生才补救，而是在上线前和上线后反复检查：哪些风险已经可控，哪些风险还不能放行。",
            "这件事改变了我们对 AI 产品的判断标准：不能只问“它聪不聪明”，还要问“它在危险题、边界题、真实流程里稳不稳”。",
        ],
    },
    {
        "id": "analogy",
        "title": "一个直观类比：AI 上线前的驾驶考试",
        "body": [
            "一个人会开车，不等于可以马上独自上路。驾校会先让他学规则，再在考试路线中处理转弯、变道、礼让、突发障碍。考试不是为了保证他今后一定不出事，而是确认他达到可上路的最低安全线。",
            "AI安全评估也是这样。模型会回答问题，只代表它有能力；通过安全评估，才说明它在隐私、事实、工具调用、敏感建议和对抗诱导里达到可接受标准。",
            "所以，安全评估不是“挑刺”，而是 AI 产品的驾驶考试。考不过就不能直接上路；上路之后路况变化，还要继续复测。",
        ],
    },
    {
        "id": "mechanism",
        "title": "工作原理：安全评估怎样运作？",
        "body": [
            "第一步，定义风险。团队先列出这个 AI 可能伤害谁、在哪里犯错、错误后果有多严重。例如客服 AI 可能泄露订单信息，医疗问答 AI 可能给出不该给的诊断建议。",
            "第二步，设计测试。评估不是随便问几道题，而是准备一组覆盖真实场景、边界场景和故意诱导场景的测试题库。",
            "第三步，运行模型并记录失败。每道题不仅看回答对不对，还要看是否过度自信、是否引用来源、是否该拒绝、是否该转人工。",
            "第四步，设定通过线。不是要求 100 分，而是按风险等级定阈值：低风险可以容忍小错，高风险必须非常严格。",
            "第五步，修复并回归复测。改了提示词、知识库、护栏或模型后，要重新跑旧测试，确认新版本没有把老问题带回来。",
        ],
    },
    {
        "id": "terms",
        "title": "关键术语解释",
        "terms": [
            ("测试集", "专业解释：用于系统检查模型表现的一组标准化样本。", "白话解释：像考试卷，专门用来看看 AI 在不同题型下会不会出错。"),
            ("通过线", "专业解释：模型上线前必须达到的最低安全或质量阈值。", "白话解释：像驾照考试的及格线，没过就不能直接上路。"),
            ("严重度", "专业解释：对模型失败后果轻重程度的分级。", "白话解释：错一个标点和泄露客户隐私不是一回事，要分轻重。"),
            ("误报/漏报", "专业解释：把安全内容误判为危险是误报；放过危险内容是漏报。", "白话解释：误报是把好人拦住，漏报是把真正的风险放过去。"),
            ("回归复测", "专业解释：修改系统后重新运行旧测试，确认老问题没有复发。", "白话解释：修完一道错题后，还要再考一次，看看是不是又错了。"),
        ],
    },
    {
        "id": "case",
        "title": "真实应用案例：AI 客服上线前怎么评估？",
        "body": [
            "假设一家电商公司要上线 AI 客服，让它回答物流、退款、发票和会员问题。能力测试会问它“能不能答对规则”；安全评估会继续问更难的问题：能不能拒绝查看别人的订单？能不能避免承诺不存在的赔偿？能不能把投诉升级给人工？",
            "评估团队会准备几类测试：正常咨询、模糊投诉、诱导泄露隐私、越权退款、极端情绪用户、规则冲突和系统故障。每个回答都会被记录：答对了什么，哪里不确定，是否应该转人工。",
            "如果模型在普通问题上 95 分，但在隐私和退款越权上经常失误，它仍然不能直接上线。因为真实世界里最贵的错误，往往不是答错知识点，而是做了不该做的动作。",
        ],
    },
    {
        "id": "mistakes",
        "title": "常见误区",
        "items": [
            ("误区一：安全评估就是普通 Benchmark。", "普通评测更关心答题能力；安全评估更关心风险、边界、严重后果和真实流程。"),
            ("误区二：通过一次评估就万事大吉。", "不对。模型、用户、业务规则和攻击方式都会变化，安全评估必须持续复测。"),
            ("误区三：分数越高就一定越适合上线。", "要看错在哪里。一个低风险小错可能可接受，一个高风险漏报就可能必须拦下。"),
            ("误区四：评估只是安全团队的事。", "产品、法务、运营、客服、工程和业务负责人都要参与，因为他们最了解真实后果。"),
        ],
    },
    {
        "id": "summary",
        "title": "3句话总结",
        "bullets": [
            "AI安全评估的本质，是用系统化考试提前发现模型在真实和高风险场景里的失败方式。",
            "它不是给 AI 发终身安全证明，而是确认风险是否可控、是否达到上线阈值、出问题后能否复盘。",
            "理解安全评估，能帮助普通人看懂为什么企业 AI 不能只拼聪明，还要拼可靠性、责任和持续改进。",
        ],
    },
    {
        "id": "quiz",
        "title": "复习问题",
        "bullets": [
            "为什么一个 AI 在普通问题上表现很好，仍然可能不能直接上线？",
            "“误报”和“漏报”哪个更危险？答案为什么要看具体场景？",
            "如果你要评估一个能发邮件的 AI 助手，你会设计哪三类安全测试？",
        ],
    },
]


def ensure_figures() -> tuple[Path, Path]:
    fig1 = ROOT / "chatgpt_safety_eval_driving_test.png"
    fig2 = ROOT / "chatgpt_safety_eval_loop.png"
    if not fig1.exists() or not fig2.exists():
        raise FileNotFoundError("Expected ChatGPT Image 2.0 diagrams are missing.")
    return fig1, fig2


def make_cover() -> Image.Image:
    img, draw = page("", 1)
    draw.rectangle((0, 0, STYLE.page_w, STYLE.page_h), fill=(248, 250, 252))
    card(draw, (STYLE.margin_x, 132, STYLE.page_w - STYLE.margin_x, 1520), (255, 255, 255), STYLE.line, 44, 3)
    x = STYLE.margin_x + 62
    y = 210
    nx = badge(draw, "AI安全", x, y, STYLE.teal, (240, 253, 250), (153, 246, 228))
    nx = badge(draw, "上线评估", nx, y, STYLE.navy, (239, 246, 255), (191, 219, 254))
    badge(draw, "高中生可读", nx, y, STYLE.violet, (245, 243, 255), (196, 181, 253))

    draw.text((x, 330), CONCEPT_CN, font=FONTS["hero"], fill=STYLE.ink)
    draw.text((x, 420), CONCEPT_EN, font=FONTS["h1"], fill=STYLE.navy)
    draw.text((x, 530), "为什么 AI 上线前也要“考试”？", font=FONTS["h2"], fill=STYLE.ink)
    draw.rounded_rectangle((x, 650, STYLE.page_w - STYLE.margin_x - 62, 828), radius=26, fill=(240, 253, 250), outline=(153, 246, 228), width=3)
    core = "核心一句话：AI安全评估的本质，是用系统化测试提前发现模型会在哪里失控、退步或误伤用户。"
    draw_paragraph(draw, FONTS["body_b"], core, x + 28, 688, STYLE.page_w - STYLE.margin_x * 2 - 180, STYLE.teal, 9)

    idea_y = 948
    for color, title, body in [
        (STYLE.teal, "先列风险", "先问 AI 可能伤害谁、错在哪里、后果有多重。"),
        (STYLE.navy, "再做考试", "用真实题、边界题、诱导题测试模型和护栏。"),
        (STYLE.amber, "持续复测", "上线后继续看日志、修问题、跑旧题，防止退步。"),
    ]:
        card(draw, (x, idea_y, STYLE.page_w - STYLE.margin_x - 62, idea_y + 124), (255, 255, 255), STYLE.line, 22, 2)
        draw.rounded_rectangle((x + 24, idea_y + 30, x + 72, idea_y + 78), radius=16, fill=color)
        draw.text((x + 96, idea_y + 24), title, font=FONTS["h3"], fill=STYLE.ink)
        draw.text((x + 96, idea_y + 66), body, font=FONTS["small"], fill=STYLE.muted)
        idea_y += 150
    draw.text((x, 1440), f"{DATE}  |  每日 AI 概念精讲", font=FONTS["small"], fill=STYLE.quiet)
    return img


def make_toc() -> Image.Image:
    img, draw = page("学习路径", 2)
    y = section_title(draw, "目录：今天要建立的 8 个认知节点", STYLE.margin_x, 156, STYLE.navy)
    toc = [
        ("01", "为什么重要", "AI 产品不能只看聪不聪明，还要看风险是否可控"),
        ("02", "直观类比", "驾驶考试：会开车不等于可以马上独自上路"),
        ("03", "工作原理", "定义风险、设计测试、记录失败、设定通过线、复测"),
        ("04", "关键术语", "测试集、通过线、严重度、误报/漏报、回归复测"),
        ("05", "真实案例", "AI 客服怎样在退款、隐私和转人工中接受考试"),
        ("06", "常见误区", "安全评估不是一次性 Benchmark，也不是只看总分"),
        ("07", "3 句话总结", "把核心认知压缩成可复习的短句"),
        ("08", "复习问题", "用场景问题检查你是否真正理解"),
    ]
    for no, title, desc in toc:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 126), (255, 255, 255), STYLE.line, 20, 2)
        draw.rounded_rectangle((STYLE.margin_x + 24, y + 28, STYLE.margin_x + 88, y + 92), radius=20, fill=(240, 253, 250), outline=(153, 246, 228), width=2)
        draw.text((STYLE.margin_x + 38, y + 42), no, font=FONTS["small"], fill=STYLE.teal)
        draw.text((STYLE.margin_x + 116, y + 24), title, font=FONTS["h3"], fill=STYLE.ink)
        draw.text((STYLE.margin_x + 116, y + 68), desc, font=FONTS["small"], fill=STYLE.muted)
        y += 144
    return img


def make_why_page() -> Image.Image:
    img, draw = page("为什么重要", 3)
    y = section_title(draw, "为什么 AI 安全评估值得理解？", STYLE.margin_x, 146, STYLE.teal)
    y = draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[0]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 11)
    y += 34
    cards = [
        ("它解决的问题", "把“模型可能在哪里出事”提前暴露出来，而不是等用户踩坑。"),
        ("它改变的认知", "AI 上线不是发布按钮，而是一套考试、修复和复测流程。"),
        ("它的现实意义", "客服、搜索、企业 Agent、医疗问答和机器人都需要持续安全评估。"),
    ]
    for title, body in cards:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 132), (248, 250, 252), STYLE.line, 20, 2)
        draw.text((STYLE.margin_x + 28, y + 24), title, font=FONTS["h3"], fill=STYLE.navy)
        draw.text((STYLE.margin_x + 280, y + 30), body, font=FONTS["body"], fill=STYLE.muted)
        y += 154
    return img


def make_analogy_page(fig_path: Path) -> Image.Image:
    img, draw = page("直观类比", 4)
    y = section_title(draw, "一个直观类比：AI 上线前的驾驶考试", STYLE.margin_x, 126, STYLE.navy)
    y = paste_image_fit(img, fig_path, STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, 600)
    y += 10
    draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[1]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 10)
    return img


def make_mechanism_page(fig_path: Path) -> Image.Image:
    img, draw = page("工作原理", 5)
    y = section_title(draw, "工作原理：从风险到复测的闭环", STYLE.margin_x, 126, STYLE.cyan)
    y = paste_image_fit(img, fig_path, STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, 570)
    steps = [
        ("定义风险", "先列出可能伤害用户、泄露信息、越权操作或误导决策的场景。"),
        ("设计测试", "准备真实题、边界题、诱导题和高风险题，不只考普通问答。"),
        ("记录失败", "看错误类型、严重度、是否该拒绝、是否该转人工。"),
        ("修复复测", "改完模型、知识库或护栏后，用旧题再考一次，防止退步。"),
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
    y = section_title(draw, "真实应用案例：AI 客服上线前怎么评估？", STYLE.margin_x, 132, STYLE.green)
    y = draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[4]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 10)
    y += 30
    card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 296), (240, 253, 250), (153, 246, 228), 24, 3)
    draw.text((STYLE.margin_x + 34, y + 30), "一套像样的客服安全评估至少要测：", font=FONTS["h3"], fill=STYLE.teal)
    qy = y + 88
    for q in [
        "能否拒绝查看别人的订单和手机号。",
        "能否避免承诺公司制度里没有的赔偿。",
        "遇到愤怒用户或规则冲突时，是否及时转人工。",
        "系统故障或信息不足时，是否诚实说明不确定。",
    ]:
        draw.ellipse((STYLE.margin_x + 40, qy + 9, STYLE.margin_x + 58, qy + 27), fill=STYLE.teal)
        draw.text((STYLE.margin_x + 76, qy), q, font=FONTS["body"], fill=STYLE.ink)
        qy += 54
    return img


def make_mistakes_page() -> Image.Image:
    img, draw = page("常见误区", 8)
    y = section_title(draw, "常见误区：别把安全评估想简单了", STYLE.margin_x, 132, STYLE.red)
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
    .eyebrow {{ color: var(--teal); font-weight: 700; letter-spacing: 0; }}
    h1 {{ margin: 16px 0 10px; font-size: clamp(38px, 6vw, 72px); line-height: 1.08; letter-spacing: 0; }}
    .subtitle {{ font-size: 26px; color: var(--muted); margin: 0 0 24px; }}
    .core {{ margin-top: 24px; padding: 18px 22px; border: 1px solid #99f6e4; background: #f0fdfa; border-radius: 8px; font-weight: 700; color: var(--teal); }}
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
      <p class="subtitle">为什么 AI 上线前也要“考试”？</p>
      <div class="core">核心一句话：AI安全评估的本质，是用系统化测试提前发现模型会在哪里失控、退步或误伤用户。</div>
      <nav>{toc}</nav>
    </div>
  </header>
  <main>
    <section id="why"><h2>{escape(SECTIONS[0]["title"])}</h2>{html_paragraphs(SECTIONS[0]["body"])}</section>
    <section id="analogy"><h2>{escape(SECTIONS[1]["title"])}</h2><figure><img src="{fig1.name}" alt="AI安全评估驾驶考试类比图"><figcaption>驾驶考试类比：会开车不等于可以直接上路，AI 会回答也不等于可以直接上线。</figcaption></figure>{html_paragraphs(SECTIONS[1]["body"])}</section>
    <section id="mechanism"><h2>{escape(SECTIONS[2]["title"])}</h2><figure><img src="{fig2.name}" alt="AI安全评估闭环流程图"><figcaption>安全评估闭环：定义风险、设计测试、运行模型、记录失败、修复护栏、回归复测。</figcaption></figure>{html_paragraphs(SECTIONS[2]["body"])}</section>
    <section id="terms"><h2>{escape(SECTIONS[3]["title"])}</h2><table><thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead><tbody>{term_rows}</tbody></table></section>
    <section id="case"><h2>{escape(SECTIONS[4]["title"])}</h2>{html_paragraphs(SECTIONS[4]["body"])}<div class="note">安全评估的价值：把“它能回答”推进到“它能负责地进入真实业务”。</div></section>
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
