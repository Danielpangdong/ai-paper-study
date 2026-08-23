from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-12"
CONCEPT_CN = "AI可解释性"
CONCEPT_EN = "Interpretability"
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
    resample = getattr(Image, "Resampling", Image).LANCZOS
    img = img.resize((nw, nh), resample)
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
            "AI可解释性解决的是一个朴素但关键的问题：AI 给了一个答案，我们能不能知道它为什么这样判断？如果一个模型拒绝贷款、推荐药物、筛选简历或让客服转人工，只看结果远远不够，人们还需要看见证据、原因和边界。",
            "在大模型时代，AI 不再只是做一道选择题。它会写方案、调工具、生成报告、影响业务流程。越是进入真实生活，越不能只问“它答对了吗”，还要问“它是靠什么答对的，如果错了我们怎么发现”。",
            "可解释性让 AI 从一个神秘黑箱，变成一个可以检查、可以讨论、可以修复的系统。它不能保证模型永远正确，但能让错误更早暴露，让信任建立在证据上，而不是建立在感觉上。",
        ],
    },
    {
        "id": "analogy",
        "title": "一个直观类比：老师不只看答案，还看解题步骤",
        "body": [
            "想象一个学生做数学题，最后答案写对了。老师仍然会看草稿：用了什么公式？有没有偷换条件？中间哪一步最关键？因为答案可能是蒙对的，也可能是用错方法碰巧得到的。",
            "AI可解释性也是在看“解题步骤”。我们不一定能完整读出模型大脑里的每个念头，但可以要求它留下可检查的线索：它参考了哪些资料，关注了输入里的哪些部分，哪些因素最影响结果。",
            "这件事的重点不是让 AI 像人一样讲一个漂亮故事，而是让人类能追问：这个解释站得住脚吗？证据够不够？如果换一个条件，结论会不会变？",
        ],
    },
    {
        "id": "mechanism",
        "title": "工作原理：可解释性怎样运作？",
        "body": [
            "第一步，看输入。对文本模型来说，输入可能是一段话、一个问题、一份合同；对视觉模型来说，输入可能是一张 X 光片或道路照片。解释要先说明模型到底在看什么。",
            "第二步，看证据。AI 搜索和 RAG 系统常用引用来源来解释答案；风控模型会列出收入、负债、历史记录等关键因素；图像模型可能用热力图标出它关注的区域。",
            "第三步，看影响。可解释工具会估计：如果某个词、某个特征、某条证据被拿掉，结果会不会明显变化。影响越大，越值得人类重点检查。",
            "第四步，让人核对。解释不是自动等于真相。医生、工程师、产品经理或审核员要判断解释是否符合常识、规则和业务证据。",
            "第五步，用解释改进系统。如果解释暴露出偏见、错误证据或脆弱逻辑，就要修数据、调规则、补评测，甚至限制模型的使用范围。",
        ],
    },
    {
        "id": "terms",
        "title": "关键术语解释",
        "terms": [
            ("可解释性", "专业解释：让模型输出和关键决策因素能够被人理解、检查和验证的能力。", "白话解释：AI 不能只给答案，还要留下人能看懂的理由和证据。"),
            ("黑箱模型", "专业解释：内部机制复杂，难以直接观察每个判断原因的模型。", "白话解释：像一个锁着的盒子，输入进去、结果出来，但里面怎么想不容易看见。"),
            ("特征贡献", "专业解释：某个输入因素对最终预测结果的影响程度。", "白话解释：看看到底是收入、病历、关键词还是图片区域，把结果推向了这个方向。"),
            ("注意力热图", "专业解释：用颜色显示模型在输入不同位置上的关注强弱。", "白话解释：像老师用荧光笔标重点，颜色越亮，说明模型越关注那里。"),
            ("反事实解释", "专业解释：通过假设某个条件改变，观察模型结论是否随之改变。", "白话解释：问一句“如果这个条件不一样，AI 还会给同样答案吗？”"),
            ("可审计性", "专业解释：系统决策过程、证据和记录能被事后检查与追责。", "白话解释：出了问题不能只说“AI 就是这么说的”，要能回头查清楚发生了什么。"),
        ],
    },
    {
        "id": "case",
        "title": "一个真实应用案例：AI 贷款审核",
        "body": [
            "假设银行用 AI 辅助判断一个人能否获得贷款。如果系统只给出“拒绝”两个字，用户会困惑，业务人员也很难知道模型是否公平。可解释性要求系统说明：主要影响因素是收入稳定性、已有负债、还款记录，还是资料不完整。",
            "一个合格的解释不应该泄露商业机密，也不应该编造理由。它至少要让人知道：哪些因素最重要，哪些证据可以补充，模型有没有使用不该使用的敏感线索。",
            "这对企业也有价值。如果很多被拒案例都被解释为“地址区域风险高”，工程和合规团队就要警惕：模型是否把地理位置当成了收入、族群或职业的替代线索？这就是可解释性帮助发现偏见的地方。",
        ],
    },
    {
        "id": "mistakes",
        "title": "常见误区",
        "items": [
            ("误区一：AI 能解释，就说明它一定正确。", "不对。解释只是可检查的线索，不是正确性的保证。一个学生也可能把错误步骤讲得很流畅。"),
            ("误区二：可解释性就是让 AI 说出思考过程。", "不完全是。大模型生成的理由可能是事后组织的语言，真正可靠的解释还要看证据、特征影响和可验证记录。"),
            ("误区三：解释越复杂越专业。", "好的解释应该让目标读者能做判断。给普通用户看，应清楚说明主要原因和可行动建议，而不是堆满术语。"),
            ("误区四：黑箱模型完全不能用。", "不一定。关键是看场景风险。低风险推荐可以宽松一些；医疗、金融、招聘等高风险场景就必须有更强解释和审计。"),
            ("误区五：开源模型天然更可解释。", "开源能帮助研究者检查结构和权重，但普通用户仍然需要面向具体任务的证据、日志和解释界面。"),
        ],
    },
    {
        "id": "summary",
        "title": "3句话总结",
        "bullets": [
            "AI可解释性的本质，是让模型判断留下人类可以检查的原因、证据和影响线索。",
            "解释不是正确性的证明，但能帮助我们发现错误、偏见、脆弱逻辑和不该上线的风险。",
            "理解可解释性，能让你从“相信 AI 的答案”升级为“审视 AI 的依据”。",
        ],
    },
    {
        "id": "quiz",
        "title": "复习问题",
        "bullets": [
            "为什么一个 AI 答案看起来正确，仍然需要可解释性？请用“老师看解题步骤”的类比回答。",
            "在贷款审核、医疗建议、短视频推荐这三个场景里，哪个最需要强解释？为什么？",
            "如果一个 AI 说“因为用户画像相似，所以推荐这份工作”，你会继续追问哪三个问题？",
        ],
    },
]


def ensure_figures() -> tuple[Path, Path]:
    fig1 = ROOT / "chatgpt_interpretability_blackbox_window.png"
    fig2 = ROOT / "chatgpt_interpretability_loop.png"
    if not fig1.exists() or not fig2.exists():
        raise FileNotFoundError("Expected ChatGPT Image diagrams are missing.")
    return fig1, fig2


def make_cover() -> Image.Image:
    img, draw = page("", 1)
    draw.rectangle((0, 0, STYLE.page_w, STYLE.page_h), fill=STYLE.soft)
    card(draw, (STYLE.margin_x, 132, STYLE.page_w - STYLE.margin_x, 1520), (255, 255, 255), STYLE.line, 44, 3)
    x = STYLE.margin_x + 62
    y = 210
    nx = badge(draw, "AI认知基础", x, y, STYLE.teal, (240, 253, 250), (153, 246, 228))
    nx = badge(draw, "安全与信任", nx, y, STYLE.navy, (239, 246, 255), (191, 219, 254))
    badge(draw, "高中生可读", nx, y, STYLE.violet, (245, 243, 255), (196, 181, 253))

    draw.text((x, 330), CONCEPT_CN, font=FONTS["hero"], fill=STYLE.ink)
    draw.text((x, 420), CONCEPT_EN, font=FONTS["h1"], fill=STYLE.navy)
    draw.text((x, 530), "为什么我们不能只看 AI 答案？", font=FONTS["h2"], fill=STYLE.ink)
    draw.rounded_rectangle((x, 650, STYLE.page_w - STYLE.margin_x - 62, 842), radius=26, fill=(240, 253, 250), outline=(153, 246, 228), width=3)
    core = "核心一句话：可解释性的本质，是让 AI 的判断过程留下可被人检查的原因、证据和边界。"
    draw_paragraph(draw, FONTS["body_b"], core, x + 28, 690, STYLE.page_w - STYLE.margin_x * 2 - 180, STYLE.teal, 9)

    idea_y = 962
    for color, title, body in [
        (STYLE.teal, "看见证据", "知道 AI 参考了哪些资料、数据或输入片段。"),
        (STYLE.navy, "追问原因", "判断哪些因素最影响结果，而不是只接受结论。"),
        (STYLE.amber, "改进系统", "发现偏见、错误线索和脆弱逻辑后持续修复。"),
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
        ("01", "为什么重要", "AI 正进入金融、医疗、招聘、客服等真实流程"),
        ("02", "直观类比", "老师不只看答案，还看解题步骤和关键证据"),
        ("03", "工作原理", "输入、证据、影响、人类核对、系统改进"),
        ("04", "关键术语", "黑箱、特征贡献、热图、反事实、可审计性"),
        ("05", "真实案例", "贷款审核怎样从“拒绝”变成可检查的理由"),
        ("06", "常见误区", "解释不是正确性证明，也不是一段漂亮话"),
        ("07", "3 句话总结", "把核心认知压缩成可复习的短句"),
        ("08", "复习问题", "用真实场景检查你是否真正理解"),
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
    y = section_title(draw, "为什么 AI 可解释性值得理解？", STYLE.margin_x, 146, STYLE.teal)
    y = draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[0]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 11)
    y += 34
    cards = [
        ("它解决的问题", "从“AI 给了答案”推进到“人能检查答案背后的依据”。"),
        ("它改变的认知", "AI 可信不是靠神秘感，而是靠证据、边界和可追问。"),
        ("它的现实意义", "金融、医疗、招聘、推荐、客服和 Agent 都需要解释与审计。"),
    ]
    for title, body in cards:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 132), (248, 250, 252), STYLE.line, 20, 2)
        draw.text((STYLE.margin_x + 28, y + 24), title, font=FONTS["h3"], fill=STYLE.navy)
        draw.text((STYLE.margin_x + 280, y + 30), body, font=FONTS["body"], fill=STYLE.muted)
        y += 154
    return img


def make_analogy_page(fig_path: Path) -> Image.Image:
    img, draw = page("直观类比", 4)
    y = section_title(draw, "一个直观类比：老师看解题步骤", STYLE.margin_x, 126, STYLE.navy)
    y = paste_image_fit(img, fig_path, STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, 640)
    y += 8
    draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[1]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 10)
    return img


def make_mechanism_page(fig_path: Path) -> Image.Image:
    img, draw = page("工作原理", 5)
    y = section_title(draw, "工作原理：从黑箱结果到可检查线索", STYLE.margin_x, 126, STYLE.cyan)
    y = paste_image_fit(img, fig_path, STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, 590)
    steps = [
        ("看输入", "先确认模型处理的是哪些问题、图片、文本或业务数据。"),
        ("看证据", "引用来源、关键特征、热力图和案例都可以成为解释线索。"),
        ("看影响", "检查哪些因素最能改变结果，找出真正需要关注的部分。"),
        ("让人核对", "解释要经过专业人员、业务人员或用户常识的检查。"),
        ("推动改进", "发现偏见和错误后，修数据、调规则、补评测。"),
    ]
    draw_steps(draw, steps, STYLE.margin_x, y + 4, STYLE.page_w - STYLE.margin_x * 2, STYLE.cyan, 98)
    return img


def make_terms_page() -> Image.Image:
    img, draw = page("关键术语", 6)
    y = section_title(draw, "关键术语：专业解释 + 白话解释", STYLE.margin_x, 118, STYLE.violet)
    for term, pro, plain in SECTIONS[3]["terms"]:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 146), (255, 255, 255), STYLE.line, 18, 2)
        draw.text((STYLE.margin_x + 28, y + 18), term, font=FONTS["h3"], fill=STYLE.violet)
        draw.text((STYLE.margin_x + 220, y + 22), pro, font=FONTS["small"], fill=STYLE.ink)
        draw.text((STYLE.margin_x + 220, y + 70), plain, font=FONTS["small"], fill=STYLE.muted)
        y += 160
    return img


def make_case_page() -> Image.Image:
    img, draw = page("真实应用案例", 7)
    y = section_title(draw, "真实应用案例：AI 贷款审核", STYLE.margin_x, 132, STYLE.green)
    y = draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[4]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 10)
    y += 30
    card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 316), (240, 253, 250), (153, 246, 228), 24, 3)
    draw.text((STYLE.margin_x + 34, y + 30), "一份合格的解释至少要回答：", font=FONTS["h3"], fill=STYLE.teal)
    qy = y + 88
    for q in [
        "主要影响因素是什么，而不是只给一个分数。",
        "这些因素是否来自真实、允许使用的证据。",
        "用户能否通过补充材料或修正信息改变结果。",
        "有没有把敏感属性或代理变量偷偷当成判断依据。",
    ]:
        draw.ellipse((STYLE.margin_x + 40, qy + 9, STYLE.margin_x + 58, qy + 27), fill=STYLE.teal)
        draw.text((STYLE.margin_x + 76, qy), q, font=FONTS["body"], fill=STYLE.ink)
        qy += 56
    return img


def make_mistakes_page() -> Image.Image:
    img, draw = page("常见误区", 8)
    y = section_title(draw, "常见误区：别把解释当成魔法", STYLE.margin_x, 110, STYLE.red)
    for title, body in SECTIONS[5]["items"]:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 150), (255, 255, 255), STYLE.line, 18, 2)
        draw.text((STYLE.margin_x + 28, y + 18), title, font=FONTS["h3"], fill=STYLE.red)
        draw_paragraph(draw, FONTS["small"], body, STYLE.margin_x + 28, y + 66, STYLE.page_w - STYLE.margin_x * 2 - 56, STYLE.muted, 6)
        y += 168
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
      <p class="subtitle">为什么我们不能只看 AI 答案，还要追问它为什么这样想？</p>
      <div class="core">核心一句话：可解释性的本质，是让 AI 的判断过程留下可被人检查的原因、证据和边界。</div>
      <nav>{toc}</nav>
    </div>
  </header>
  <main>
    <section id="why"><h2>{escape(SECTIONS[0]["title"])}</h2>{html_paragraphs(SECTIONS[0]["body"])}</section>
    <section id="analogy"><h2>{escape(SECTIONS[1]["title"])}</h2><figure><img src="{fig1.name}" alt="AI可解释性黑箱开窗图"><figcaption>黑箱开窗：可解释性让输入、输出和关键解释线索进入人类可检查的范围。</figcaption></figure>{html_paragraphs(SECTIONS[1]["body"])}</section>
    <section id="mechanism"><h2>{escape(SECTIONS[2]["title"])}</h2><figure><img src="{fig2.name}" alt="AI可解释性五步流程图"><figcaption>可解释性闭环：输入任务、模型判断、生成解释线索、人类核对证据、发现问题后改进。</figcaption></figure>{html_paragraphs(SECTIONS[2]["body"])}</section>
    <section id="terms"><h2>{escape(SECTIONS[3]["title"])}</h2><table><thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead><tbody>{term_rows}</tbody></table></section>
    <section id="case"><h2>{escape(SECTIONS[4]["title"])}</h2>{html_paragraphs(SECTIONS[4]["body"])}<div class="note">可解释性的价值：把“AI 说了什么”推进到“人能检查 AI 凭什么这么说”。</div></section>
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
    target_w = int(STYLE.page_w * 0.72)
    target_h = int(STYLE.page_h * 0.72)
    resample = getattr(Image, "Resampling", Image).LANCZOS
    scaled_pages = [p.resize((target_w, target_h), resample) for p in pages]
    pal_pages = [p.convert("P", palette=Image.Palette.ADAPTIVE, colors=128) for p in scaled_pages]
    pdf_path = ROOT / PDF_NAME
    pal_pages[0].save(pdf_path, "PDF", resolution=STYLE.dpi, save_all=True, append_images=pal_pages[1:])
    print(pdf_path)
    print(html_path)
    print(fig1)
    print(fig2)


if __name__ == "__main__":
    build()
