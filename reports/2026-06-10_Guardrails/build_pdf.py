from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-10"
CONCEPT_CN = "AI安全护栏"
CONCEPT_EN = "Guardrails"
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


def badge(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    fg: tuple[int, int, int],
    bg: tuple[int, int, int],
    outline: tuple[int, int, int],
) -> int:
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
            "AI安全护栏解决的是一个朴素但关键的问题：当 AI 越来越会回答、会搜索、会调用工具时，我们怎样让它在高风险场景里少犯错、少越权、出问题后还能追踪和复盘？",
            "没有护栏的 AI，就像一个很聪明但没有流程意识的实习生：它可能知道很多，也可能因为一句模糊指令就给出危险建议、泄露信息，或调用了不该调用的工具。",
            "护栏不是让 AI 变得更聪明，而是给 AI 的输入、资料、工具、输出和事后记录加上安全边界。它让 AI 产品从“能用”走向“可控、可审计、可上线”。",
        ],
    },
    {
        "id": "analogy",
        "title": "一个直观类比：机场安检",
        "body": [
            "想象你要坐飞机。机场并不是不信任每个旅客，而是知道飞行是高风险系统，所以必须层层把关：看证件、查行李、过安检、异常情况转人工。",
            "AI护栏也是这样。用户请求进来后，系统会先判断意图是否敏感，再检查权限是否足够；如果要调用工具，就放进受限环境；如果输出有风险，就改写、拒绝或转给人处理。",
            "这套机制的重点不是“每个人都危险”，而是承认系统总会遇到边界情况。好护栏让大多数正常请求顺畅通过，也让高风险请求被及时拦住。",
        ],
    },
    {
        "id": "mechanism",
        "title": "工作原理：护栏怎样让 AI 更可靠？",
        "body": [
            "第一层是输入护栏。它检查用户请求是否涉及隐私、违法、医疗、金融、暴力、自伤或越权操作，并在信息不足时要求补充背景。",
            "第二层是知识护栏。AI 不是随便使用任何材料，而是优先检索可信资料、记录来源，并限制模型把不确定内容说得太肯定。",
            "第三层是工具护栏。AI 调用邮箱、数据库、浏览器或支付系统时，必须遵守最小权限、沙箱执行、关键动作确认和失败回滚。",
            "第四层是输出护栏。系统会检查回答是否包含危险指导、隐私泄露、未经证实的事实或过度承诺，必要时改写、拒绝或转人工。",
            "第五层是日志与复盘。每一次高风险拦截、人工接管和用户反馈都应该被记录，成为下一轮改进、评测和红队测试的材料。",
        ],
    },
    {
        "id": "terms",
        "title": "关键术语解释",
        "terms": [
            ("护栏", "专业解释：围绕 AI 输入、检索、工具、输出和监控建立的风险控制机制。", "白话解释：给 AI 装上规则、权限和刹车，避免它想怎么答就怎么答。"),
            ("策略规则", "专业解释：系统预先定义的允许、限制、拒绝和升级条件。", "白话解释：提前写好的红绿灯，告诉 AI 哪些事能做、哪些事不能做。"),
            ("最小权限", "专业解释：工具或账号只获得完成任务所必需的最低访问能力。", "白话解释：让 AI 只拿需要的钥匙，不把整栋楼的钥匙都交给它。"),
            ("人工复核", "专业解释：高风险或不确定请求由人类审查、批准或接管。", "白话解释：遇到关键决策时，别让 AI 自己拍板，要请人看一眼。"),
            ("审计日志", "专业解释：记录请求、判断、工具调用、输出和拦截结果的可追踪证据。", "白话解释：像监控录像和操作记录，事后能查清 AI 为什么这么做。"),
        ],
    },
    {
        "id": "case",
        "title": "真实应用案例：企业 AI 助手处理报销",
        "body": [
            "假设公司上线一个 AI 助手，员工可以让它查询报销制度、填写表单、读取发票、提交审批。没有护栏时，它可能把别人的报销记录发给错误的人，或者在信息不完整时直接提交。",
            "有护栏后，流程会变成：先确认员工身份和部门权限；只检索公司批准的制度文档；读取发票时只访问当前任务需要的字段；提交前让用户确认；异常金额或敏感信息自动转人工。",
            "这就是护栏的现实意义。它不只是“内容安全过滤器”，而是把 AI 放进企业流程里时必须具备的权限控制、事实校验、人工审批和事后审计。",
        ],
    },
    {
        "id": "mistakes",
        "title": "常见误区",
        "items": [
            ("误区一：护栏就是关键词过滤。", "关键词过滤只是很粗的一种方式。真正的护栏还包括上下文判断、权限控制、工具沙箱、事实核验和人工复核。"),
            ("误区二：护栏越多，AI 越安全。", "不一定。过多护栏会让正常任务卡住，甚至让用户绕开系统。好护栏要区分风险等级，而不是一刀切。"),
            ("误区三：有护栏就不需要红队测试。", "相反，红队测试会不断挑战护栏，帮助团队发现规则漏洞、权限漏洞和绕过方式。"),
            ("误区四：护栏只适合聊天机器人。", "不对。AI 搜索、客服、代码助手、企业 Agent、医疗问答、金融助手和机器人都需要不同类型的护栏。"),
        ],
    },
    {
        "id": "summary",
        "title": "3句话总结",
        "bullets": [
            "AI安全护栏的本质，是在输入、知识、工具、输出和复盘环节给 AI 加上边界。",
            "它不是让 AI 更聪明，而是让 AI 在高风险场景里更可控、更可追踪、更适合真实上线。",
            "理解护栏，能帮助普通人看懂为什么企业 AI 不能只追求能力，还必须重视权限、流程和责任。",
        ],
    },
    {
        "id": "quiz",
        "title": "复习问题",
        "bullets": [
            "为什么“关键词过滤”不能代表完整的 AI 安全护栏？",
            "如果一个 AI 助手可以帮你发邮件，至少应该给它加哪几类护栏？",
            "为什么好护栏既要拦住高风险请求，又不能把所有正常请求都挡住？",
        ],
    },
]


def ensure_figures() -> tuple[Path, Path]:
    fig1 = ROOT / "chatgpt_guardrails_airport_security.png"
    fig2 = ROOT / "chatgpt_guardrails_five_layers.png"
    if not fig1.exists() or not fig2.exists():
        raise FileNotFoundError("Expected ChatGPT Image 2.0 diagrams are missing.")
    return fig1, fig2


def make_cover() -> Image.Image:
    img, draw = page("", 1)
    draw.rectangle((0, 0, STYLE.page_w, STYLE.page_h), fill=(248, 250, 252))
    draw.rounded_rectangle((STYLE.margin_x, 132, STYLE.page_w - STYLE.margin_x, 1520), radius=44, fill=(255, 255, 255), outline=STYLE.line, width=3)
    x = STYLE.margin_x + 62
    y = 210
    y = badge(draw, "AI安全", x, y, STYLE.teal, (240, 253, 250), (153, 246, 228))
    y = badge(draw, "企业上线", y, 210, STYLE.navy, (239, 246, 255), (191, 219, 254))
    badge(draw, "高中生可读", y, 210, STYLE.violet, (245, 243, 255), (196, 181, 253))

    draw.text((x, 330), CONCEPT_CN, font=FONTS["hero"], fill=STYLE.ink)
    draw.text((x, 420), CONCEPT_EN, font=FONTS["h1"], fill=STYLE.navy)
    draw.text((x, 530), "为什么强大的 AI 还需要“安全边界”？", font=FONTS["h2"], fill=STYLE.ink)
    draw.rounded_rectangle((x, 650, STYLE.page_w - STYLE.margin_x - 62, 812), radius=26, fill=(240, 253, 250), outline=(153, 246, 228), width=3)
    core = "核心一句话：AI安全护栏不是让 AI 更聪明，而是让 AI 在高风险场景少犯错、可追踪、可复核。"
    draw_paragraph(draw, FONTS["body_b"], core, x + 28, 688, STYLE.page_w - STYLE.margin_x * 2 - 180, STYLE.teal, 9)

    idea_y = 930
    for color, title, body in [
        (STYLE.teal, "先判断风险", "不是所有请求都一样，要先看意图、权限和场景。"),
        (STYLE.navy, "再限制动作", "调用工具时要最小权限、沙箱执行、关键步骤确认。"),
        (STYLE.amber, "最后能复盘", "出问题后要有日志、有证据、有改进路径。"),
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
        ("01", "为什么重要", "AI 越能办事，越需要边界、权限和审计"),
        ("02", "直观类比", "机场安检：正常放行，高风险请求升级处理"),
        ("03", "工作原理", "输入、知识、工具、输出、日志五层护栏"),
        ("04", "关键术语", "护栏、策略规则、最小权限、人工复核、审计日志"),
        ("05", "真实案例", "企业 AI 助手处理报销时怎样防越权"),
        ("06", "常见误区", "护栏不是关键词过滤，也不是越多越好"),
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
    y = section_title(draw, "为什么 AI 安全护栏值得理解？", STYLE.margin_x, 146, STYLE.teal)
    y = draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[0]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 11)
    y += 34
    cards = [
        ("它解决的问题", "让 AI 在敏感、越权、工具调用和不确定场景里不乱答、不乱做。"),
        ("它改变的认知", "AI 上线不是只看能力，还要看权限、流程、证据和责任。"),
        ("它的现实意义", "客服、搜索、代码助手、企业 Agent 和机器人都需要可控边界。"),
    ]
    for title, body in cards:
        card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 132), (248, 250, 252), STYLE.line, 20, 2)
        draw.text((STYLE.margin_x + 28, y + 24), title, font=FONTS["h3"], fill=STYLE.navy)
        draw.text((STYLE.margin_x + 280, y + 30), body, font=FONTS["body"], fill=STYLE.muted)
        y += 154
    return img


def make_analogy_page(fig_path: Path) -> Image.Image:
    img, draw = page("直观类比", 4)
    y = section_title(draw, "一个直观类比：机场安检", STYLE.margin_x, 126, STYLE.navy)
    y = paste_image_fit(img, fig_path, STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, 600)
    y += 10
    draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[1]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 10)
    return img


def make_mechanism_page(fig_path: Path) -> Image.Image:
    img, draw = page("工作原理", 5)
    y = section_title(draw, "工作原理：五层护栏怎样协同？", STYLE.margin_x, 126, STYLE.cyan)
    y = paste_image_fit(img, fig_path, STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, 570)
    steps = [
        ("输入护栏", "识别敏感意图、补充上下文，先判断这件事风险有多高。"),
        ("知识护栏", "优先使用可信资料、标注来源，不把猜测包装成事实。"),
        ("工具护栏", "最小权限、沙箱执行、关键动作确认，避免 AI 乱操作。"),
        ("输出与复盘", "检查风险措辞和事实依据，记录证据并持续改进。"),
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
    y = section_title(draw, "真实应用案例：企业 AI 助手处理报销", STYLE.margin_x, 132, STYLE.green)
    y = draw_paragraph(draw, FONTS["body"], "\n\n".join(SECTIONS[4]["body"]), STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x * 2, STYLE.ink, 10)
    y += 30
    card(draw, (STYLE.margin_x, y, STYLE.page_w - STYLE.margin_x, y + 296), (240, 253, 250), (153, 246, 228), 24, 3)
    draw.text((STYLE.margin_x + 34, y + 30), "一个可靠报销助手至少要做到：", font=FONTS["h3"], fill=STYLE.teal)
    qy = y + 88
    for q in [
        "只读取当前员工有权访问的资料。",
        "提交、删除、转账这类关键动作必须二次确认。",
        "异常金额、敏感字段和制度冲突自动转人工。",
        "每次工具调用和审批结果都可追踪。",
    ]:
        draw.ellipse((STYLE.margin_x + 40, qy + 9, STYLE.margin_x + 58, qy + 27), fill=STYLE.teal)
        draw.text((STYLE.margin_x + 76, qy), q, font=FONTS["body"], fill=STYLE.ink)
        qy += 54
    return img


def make_mistakes_page() -> Image.Image:
    img, draw = page("常见误区", 8)
    y = section_title(draw, "常见误区：别把护栏想简单了", STYLE.margin_x, 132, STYLE.red)
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
      <p class="subtitle">为什么强大的 AI 还需要“安全边界”？</p>
      <div class="core">核心一句话：AI安全护栏不是让 AI 更聪明，而是让 AI 在高风险场景少犯错、可追踪、可复核。</div>
      <nav>{toc}</nav>
    </div>
  </header>
  <main>
    <section id="why"><h2>{escape(SECTIONS[0]["title"])}</h2>{html_paragraphs(SECTIONS[0]["body"])}</section>
    <section id="analogy"><h2>{escape(SECTIONS[1]["title"])}</h2><figure><img src="{fig1.name}" alt="AI安全护栏机场安检类比图"><figcaption>机场安检类比：正常请求顺畅通过，高风险请求被改写、拒绝或升级处理。</figcaption></figure>{html_paragraphs(SECTIONS[1]["body"])}</section>
    <section id="mechanism"><h2>{escape(SECTIONS[2]["title"])}</h2><figure><img src="{fig2.name}" alt="AI安全护栏五层防线图"><figcaption>五层护栏：输入、知识、工具、输出、日志与复盘共同降低风险。</figcaption></figure>{html_paragraphs(SECTIONS[2]["body"])}</section>
    <section id="terms"><h2>{escape(SECTIONS[3]["title"])}</h2><table><thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead><tbody>{term_rows}</tbody></table></section>
    <section id="case"><h2>{escape(SECTIONS[4]["title"])}</h2>{html_paragraphs(SECTIONS[4]["body"])}<div class="note">护栏的价值：把 AI 从“会回答”推进到“能进入真实流程”。</div></section>
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
