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

    fig_pipeline = base / "benchmark_eval_pipeline.png"
    fig_pitfalls = base / "benchmark_pitfalls_and_tips.png"
    out_pdf = base / "2026-05-27_模型评测（Benchmark）.pdf"

    title_font = load_font(46)
    kicker_font = load_font(19)
    h2_font = load_font(28)
    body_font = load_font(21)
    small_font = load_font(17)

    pages: list[Image.Image] = []

    def new_page() -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
        page = Image.new("RGB", (style.page_w, style.page_h), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        y0 = style.margin_y
        return page, draw, y0

    max_w = style.page_w - style.margin_x * 2

    toc_items = [
        "1. 为什么这个概念重要？",
        "2. 一个直观类比（非常重要）",
        "3. 工作原理（深入浅出）",
        "4. 关键术语解释",
        "5. 一个真实应用案例",
        "6. 常见误区（非常重要）",
        "7. 3句话总结",
        "8. 3个复习问题",
    ]

    # Page 1: Title + importance
    page, draw, y = new_page()
    header_h = 250
    header_box = (style.margin_x, y, style.page_w - style.margin_x, y + header_h)
    draw.rounded_rectangle(header_box, radius=26, outline=style.line, width=3, fill=(247, 252, 252))
    draw.text((style.margin_x + 22, y + 18), "AI每日深度科普", font=kicker_font, fill=style.muted)
    draw.text(
        (style.margin_x + 22, y + 58),
        "模型评测（Benchmark）：为什么 AI 不能只看“榜单分数”？",
        font=title_font,
        fill=style.ink,
    )
    meta = "日期：2026-05-27    难度：高中友好    关键词：考试 / 可重复对比 / 指标 / 榜单 / 数据泄漏"
    draw.text((style.margin_x + 22, y + 58 + title_font.size + 18), meta, font=small_font, fill=style.muted)
    y += header_h + 22

    box = (style.margin_x, y, style.page_w - style.margin_x, y + 150)
    draw.rounded_rectangle(box, radius=20, outline=style.line, width=3, fill=style.soft)
    draw.text(
        (style.margin_x + 22, y + 20),
        "核心一句话：Benchmark 的本质，是给 AI 一套“可重复的标准化考试”，用同一把尺子比较模型能力；"
        "但当分数变成目标时，榜单也会被“刷题、泄题、挑题”误导——所以看分数，更要看考法。",
        font=body_font,
        fill=style.accent2,
    )
    y += 176

    y = draw_section_title(draw, style, h2_font, "为什么这个概念重要？", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "在 AI 领域，你会经常看到这种说法：\n"
        "“我们在某某 Benchmark 上 SOTA（最强）了！”\n"
        "\n"
        "问题是：\n"
        "- 同一个模型，在榜单上很强，但到你公司真实业务里可能并不好用。\n"
        "- 有的模型靠“刷题技巧”拿高分，但遇到真实世界的脏数据、长对话、复杂流程就掉链子。\n"
        "\n"
        "Benchmark（模型评测）存在的价值，是解决三件现实问题：\n"
        "1）可比较：不同模型、不同版本，用同一套题和同一套规则来比。\n"
        "2）可复现：别人能重复你的评测过程，而不是只相信宣传。\n"
        "3）可定位：通过分项题型，知道模型“强在什么、弱在什么”。\n"
        "\n"
        "而当你真正理解 Benchmark，你就会立刻变得更“清醒”：\n"
        "- 分数不是实力本身，只是某种测量方式下的结果。\n"
        "- 好评测能帮你选模型；坏评测会让你在生产里踩坑。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    pages.append(page)

    # Page 2: TOC + analogy + pipeline figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "目录（你将学到什么）", style.margin_x, y)
    toc_text = "\n".join([f"{i+1}. {t.split('.', 1)[1].strip()}" for i, t in enumerate(toc_items)])
    y = draw_paragraph(draw, body_font, toc_text, style.margin_x, y, max_w, style.ink, line_gap=10)

    y += 10
    y = draw_section_title(draw, style, h2_font, "一个直观类比（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "把模型想成一个学生，把真实任务想成“你希望它在工作里做的事”。\n"
        "\n"
        "那 Benchmark 就像一场“统一考试”：\n"
        "- 题目固定：每个学生都做同一套题。\n"
        "- 规则固定：阅卷标准一致（怎么判对、怎么给分）。\n"
        "- 结果可比：你能比较谁数学更好、谁作文更好。\n"
        "\n"
        "但考试也有天然限制：\n"
        "1）只考得到的题：考试覆盖不了所有真实情况。\n"
        "2）容易“刷题”：学生可能专门练题型，而不是提升真实能力。\n"
        "3）可能“泄题”：如果学生提前见过答案，那分数就不可信。\n"
        "\n"
        "所以：Benchmark 不是无用，而是要学会“读懂考试”。\n"
        "懂得看：考什么、怎么考、题从哪来、有没有作弊空间。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = draw_section_title(draw, style, h2_font, "图解：一次标准评测是怎么发生的？", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_pipeline,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=560,
        border=True,
        style=style,
    )
    pages.append(page)

    # Page 3: mechanism + terms + pitfalls figure
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "工作原理（深入浅出）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "一套 Benchmark，通常包含 4 个关键零件：\n"
        "\n"
        "1）任务与数据（题库）\n"
        "   比如：选择题（常识）、阅读理解、写代码、总结长文、做数学题。\n"
        "\n"
        "2）提示词/输入格式（发卷方式）\n"
        "   同一题，如果你用不同的问法，模型成绩可能差很多。\n"
        "   所以评测必须尽量固定提示词，或者明确“允许的提示策略”。\n"
        "\n"
        "3）评分器（阅卷老师）\n"
        "   有的题可以自动判分（对/错）；有的需要人工打分（好不好用、是否有帮助）。\n"
        "\n"
        "4）指标（分数怎么统计）\n"
        "   常见的有：准确率、通过率、平均分、召回率、成本/延迟等。\n"
        "\n"
        "最终你看到的“榜单分数”，只是这 4 个零件组合后的一个数字。\n"
        "这也是为什么：看榜单时，最重要的是先看评测设定，而不是只看名次。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 8
    y = draw_section_title(draw, style, h2_font, "关键术语解释", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "• Benchmark（基准评测/基准测试）\n"
        "  专业：一套标准化任务与指标，用于可重复地评估模型能力。\n"
        "  白话：一份统一试卷 + 阅卷规则。\n"
        "\n"
        "• Metric（指标）\n"
        "  专业：把表现变成数值的统计方式（准确率、F1、延迟、成本等）。\n"
        "  白话：分数怎么算。\n"
        "\n"
        "• Leaderboard（排行榜/榜单）\n"
        "  专业：按某个指标展示不同模型成绩的排名。\n"
        "  白话：成绩单。\n"
        "\n"
        "• Data contamination（数据污染/泄题）\n"
        "  专业：评测题目（或答案）出现在训练数据里，导致分数虚高。\n"
        "  白话：学生提前背过答案。\n"
        "\n"
        "• Goodhart 定律（指标失效）\n"
        "  专业：当一个指标变成目标，它往往不再能真实衡量想要的能力。\n"
        "  白话：为了分数而学习，反而学偏了。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    y += 6
    y = draw_section_title(draw, style, h2_font, "图解：榜单分数常见陷阱 + 正确读法", style.margin_x, y)
    y = paste_image_fit(
        page,
        fig_pitfalls,
        style.margin_x,
        y,
        max_w=max_w,
        max_h=520,
        border=True,
        style=style,
    )
    pages.append(page)

    # Page 4: application + misconceptions + summary + questions
    page, draw, y = new_page()
    y = draw_section_title(draw, style, h2_font, "一个真实应用案例", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "场景：你要给公司选一套“AI 客服”的大模型。\n"
        "\n"
        "如果你只看公开榜单：\n"
        "- 你可能选到“刷题型高分选手”：在标准题上很好，但遇到真实用户的乱表达就不稳。\n"
        "\n"
        "更靠谱的做法，是把 Benchmark 思维用到你的业务里：\n"
        "1）先定义你要的能力：例如“能抓住问题要点、能用政策回答、不能编造”。\n"
        "2）做一套小型业务 Benchmark：\n"
        "   - 从真实工单里抽样（去隐私），覆盖高频、难题、边界情况。\n"
        "   - 统一提示词与工具使用规则（例如是否允许查知识库）。\n"
        "   - 设定评分：正确性、礼貌、可执行、是否胡编、成本与速度。\n"
        "3）把评测跑起来：用数据说话，而不是只看宣传。\n"
        "\n"
        "这样做的意义是：\n"
        "- 公开榜单告诉你“基础盘”；业务 Benchmark 告诉你“能不能上岗”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "常见误区（非常重要）", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "误区 1：Benchmark 分数高 = 真实工作能力强\n"
        "澄清：评测覆盖有限；真实世界有长尾、噪声、分布变化、流程约束。\n"
        "\n"
        "误区 2：只要选榜一，就不用做自己的评测\n"
        "澄清：你的目标、数据、流程可能完全不同；选型必须贴近你的任务定义。\n"
        "\n"
        "误区 3：评测越多越好，越复杂越专业\n"
        "澄清：评测要服务决策；先从“能区分模型差异、覆盖关键风险”的小评测开始。\n"
        "\n"
        "误区 4：自动打分就一定客观\n"
        "澄清：自动评分也会偏；关键任务往往需要人工抽检 + 明确评分 rubric。\n"
        "\n"
        "误区 5：榜单不可信，所以 Benchmark 没意义\n"
        "澄清：正确做法不是放弃，而是：看评测设定、看数据来源、看是否防泄漏，并做自己的任务评测。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "3句话总结", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）Benchmark 是标准化考试：让模型成绩可比较、可复现、可定位。\n"
        "2）分数要配合“考法”一起看：题库、提示词、评分器、指标决定了你看到的数字。\n"
        "3）最靠谱的选型方式：公开榜单看基础盘，业务自建评测看能否上岗，并警惕泄题与刷题。",
        style.margin_x,
        y,
        max_w,
        style.accent2,
        line_gap=10,
    )

    y += 6
    y = draw_section_title(draw, style, h2_font, "3个复习问题", style.margin_x, y)
    y = draw_paragraph(
        draw,
        body_font,
        "1）为什么同一个模型在不同 Benchmark 上分数差很多？请用“考试科目不同”的类比解释。\n"
        "2）你看到一个模型登顶榜单时，你会用哪 3 个问题去检查这个分数是否可信？\n"
        "3）如果让你为“AI 客服”做一套小型业务评测，你会如何选题、定规则、定指标？",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=10,
    )
    draw.text(
        (style.margin_x, style.page_h - style.margin_y + 18),
        "本材料面向高中生友好：用“统一考试”类比，强调看分数更要看考法。",
        font=small_font,
        fill=style.muted,
    )
    pages.append(page)

    # Keep the PDF under Gmail's 25MB attachment limit:
    target_w = int(style.page_w * 0.8)
    target_h = int(style.page_h * 0.8)
    scaled_pages = [p.resize((target_w, target_h), Image.LANCZOS) for p in pages]
    pal_pages = [p.convert("P", palette=Image.Palette.ADAPTIVE, colors=192) for p in scaled_pages]
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

