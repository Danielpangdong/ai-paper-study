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
    blue: tuple[int, int, int] = (30, 64, 175)
    teal: tuple[int, int, int] = (13, 148, 136)
    green: tuple[int, int, int] = (22, 163, 74)
    amber: tuple[int, int, int] = (217, 119, 6)
    red: tuple[int, int, int] = (225, 29, 72)
    violet: tuple[int, int, int] = (109, 40, 217)


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
            y += int(getattr(font, "size", 18) * 0.72)
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
    footer = "2026-06-07  |  AI对齐（Alignment）  |  让普通人看懂 AI"
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


def generate_alignment_loop_fallback(path: Path) -> None:
    style = STYLE
    w, h = 1536, 864
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = load_font(54)
    h2 = load_font(28)
    body = load_font(21)
    draw.text((70, 52), "AI对齐：让能力服从真实意图", font=title, fill=style.ink)
    draw.text((70, 120), "对齐不是一次设置，而是持续的人机反馈闭环。", font=body, fill=style.muted)
    nodes = [
        ("人类意图", "目标、边界、价值观", style.teal),
        ("数据与规则", "把要求写进训练材料", style.blue),
        ("模型输出", "回答、决策、工具调用", style.violet),
        ("反馈评估", "人类偏好与安全测试", style.amber),
        ("行为调整", "优化模型和产品边界", style.green),
    ]
    card_w, card_h = 244, 252
    x0, y0, gap = 68, 305, 54
    centers: list[tuple[int, int]] = []
    for i, (name, desc, color) in enumerate(nodes):
        x = x0 + i * (card_w + gap)
        draw_card(draw, (x, y0, x + card_w, y0 + card_h), 26, (248, 250, 252), style.line, 3)
        draw.ellipse((x + 84, y0 + 34, x + 160, y0 + 110), fill=(255, 255, 255), outline=color, width=5)
        draw.text((x + 105, y0 + 52), str(i + 1), font=h2, fill=color)
        draw.text((x + 35, y0 + 132), name, font=h2, fill=color)
        draw_paragraph(draw, body, desc, x + 28, y0 + 178, card_w - 56, style.ink, line_gap=6)
        centers.append((x + card_w, y0 + 126))
        if i < len(nodes) - 1:
            draw_arrow(draw, (x + card_w + 8, y0 + 126), (x + card_w + gap - 12, y0 + 126), style.blue, 7)
    draw.line((x0 + card_w // 2, 665, x0 + 4 * (card_w + gap) + card_w // 2, 665), fill=style.teal, width=5)
    draw.text((585, 692), "持续迭代：新场景、新风险、新反馈", font=h2, fill=style.teal)
    draw.text((205, 772), "安全优先", font=body, fill=style.teal)
    draw.text((690, 772), "以人为本", font=body, fill=style.blue)
    draw.text((1120, 772), "透明可控", font=body, fill=style.violet)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=95)


def generate_teacher_analogy_fallback(path: Path) -> None:
    style = STYLE
    w, h = 1536, 864
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = load_font(54)
    h2 = load_font(28)
    body = load_font(21)
    draw.text((70, 52), "直观类比：老师带学生改作文", font=title, fill=style.ink)
    draw.text((70, 120), "有能力不等于符合要求；对齐，是把能力用在正确方向。", font=body, fill=style.muted)
    steps = [
        ("1 学生会写", "语言流畅，但可能跑题", style.blue),
        ("2 老师指出要求", "题目、边界、评分标准", style.teal),
        ("3 根据反馈重写", "调整论点、结构和语气", style.amber),
        ("4 最终符合题意", "既有表达能力，也守住目标", style.green),
    ]
    x0, y0, card_w, card_h, gap = 55, 220, 340, 430, 35
    for i, (title_txt, desc, color) in enumerate(steps):
        x = x0 + i * (card_w + gap)
        draw_card(draw, (x, y0, x + card_w, y0 + card_h), 24, (248, 250, 252), style.line, 3)
        draw.rounded_rectangle((x, y0, x + card_w, y0 + 76), radius=24, fill=color)
        draw.text((x + 26, y0 + 18), title_txt, font=h2, fill=(255, 255, 255))
        paper = (x + 58, y0 + 118, x + card_w - 58, y0 + 278)
        draw.rounded_rectangle(paper, radius=16, fill=(255, 255, 255), outline=(203, 213, 225), width=3)
        for k in range(4):
            y_line = paper[1] + 28 + k * 30
            draw.line((paper[0] + 26, y_line, paper[2] - 26, y_line), fill=(148, 163, 184), width=3)
        if i == 1:
            draw.line((paper[0] + 30, paper[1] + 44, paper[2] - 40, paper[1] + 44), fill=style.red, width=5)
            draw.line((paper[0] + 30, paper[1] + 100, paper[2] - 88, paper[1] + 100), fill=style.red, width=5)
        if i == 3:
            draw.ellipse((paper[2] - 56, paper[3] - 56, paper[2] - 20, paper[3] - 20), fill=style.green)
            draw.text((paper[2] - 48, paper[3] - 58), "✓", font=h2, fill=(255, 255, 255))
        draw_paragraph(draw, body, desc, x + 32, y0 + 318, card_w - 64, style.ink, line_gap=7)
        if i < 3:
            draw_arrow(draw, (x + card_w + 6, y0 + card_h // 2), (x + card_w + gap - 7, y0 + card_h // 2), style.blue, 6)
    draw_card(draw, (235, 720, 1300, 810), 28, (240, 253, 250), (153, 246, 228), 3)
    draw.text((305, 746), "对齐不是让 AI 变聪明，而是让 AI 把聪明用在正确方向。", font=h2, fill=style.teal)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=95)


def write_html(base: Path, fig_loop: Path, fig_teacher: Path) -> Path:
    html_path = base / "2026-06-07_AI对齐（Alignment）.html"
    loop_name = fig_loop.name
    teacher_name = fig_teacher.name
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI每日深度科普 | AI对齐（Alignment）</title>
  <style>
    :root {{
      --ink:#0f172a; --muted:#475569; --quiet:#64748b; --line:#e2e8f0; --soft:#f8fafc;
      --blue:#1e40af; --teal:#0d9488; --amber:#d97706; --red:#e11d48; --green:#16a34a; --violet:#6d28d9;
    }}
    * {{ box-sizing:border-box; }}
    html, body {{ margin:0; padding:0; background:#ffffff; color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",sans-serif; line-height:1.75; }}
    body {{ -webkit-font-smoothing:antialiased; }}
    .page {{ max-width:1040px; margin:0 auto; padding:56px 28px 80px; }}
    .hero {{ padding:44px; border:1px solid var(--line); border-radius:24px; background:linear-gradient(180deg,#f8fafc,#ffffff); }}
    .kicker {{ color:var(--teal); font-weight:700; letter-spacing:.08em; font-size:14px; }}
    h1 {{ margin:18px 0 12px; font-size:58px; line-height:1.08; letter-spacing:0; }}
    .subtitle {{ font-size:27px; color:var(--blue); margin:0 0 18px; font-weight:700; }}
    .core {{ font-size:22px; color:var(--ink); border-left:5px solid var(--teal); padding-left:18px; margin:28px 0 0; }}
    .badges {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:26px; }}
    .badge {{ border:1px solid var(--line); border-radius:999px; padding:7px 13px; color:var(--muted); background:#fff; font-size:14px; }}
    .toc {{ margin-top:36px; border:1px solid var(--line); border-radius:20px; padding:22px 26px; background:#fff; }}
    .toc h2 {{ margin-top:0; }}
    .toc a {{ color:var(--ink); text-decoration:none; display:block; padding:8px 0; border-top:1px solid var(--line); }}
    section {{ padding:44px 0; border-bottom:1px solid var(--line); }}
    h2 {{ font-size:34px; line-height:1.25; margin:0 0 20px; letter-spacing:0; }}
    h3 {{ font-size:22px; margin:0 0 10px; }}
    p {{ font-size:18px; margin:0 0 18px; }}
    .lead {{ font-size:20px; color:var(--muted); }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px; }}
    .card {{ border:1px solid var(--line); border-radius:18px; padding:20px; background:#fff; }}
    .note {{ background:#f0fdfa; border:1px solid #99f6e4; border-radius:18px; padding:20px; color:#134e4a; font-size:18px; }}
    .figure {{ margin:28px 0; }}
    .figure img {{ width:100%; border:1px solid var(--line); border-radius:18px; display:block; }}
    .caption {{ color:var(--quiet); font-size:14px; margin-top:10px; }}
    .steps {{ display:grid; gap:14px; counter-reset:step; }}
    .step {{ border:1px solid var(--line); border-radius:18px; padding:18px 20px 18px 72px; position:relative; background:#fff; }}
    .step:before {{ counter-increment:step; content:counter(step); position:absolute; left:20px; top:20px; width:34px; height:34px; border-radius:50%; background:var(--blue); color:#fff; display:grid; place-items:center; font-weight:700; }}
    .terms {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }}
    .term b {{ color:var(--blue); }}
    .myth h3 {{ color:var(--red); }}
    .summary p {{ background:var(--soft); border:1px solid var(--line); border-radius:16px; padding:18px; }}
    ul, ol {{ font-size:18px; padding-left:1.35em; }}
    li {{ margin:8px 0; }}
    footer {{ color:var(--quiet); font-size:14px; padding-top:34px; }}
    @media (max-width:760px) {{
      h1 {{ font-size:42px; }}
      .subtitle {{ font-size:22px; }}
      .hero {{ padding:28px; }}
      .grid, .terms {{ grid-template-columns:1fr; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header class="hero" aria-label="标题页">
      <div class="kicker">AI每日深度科普 · 2026-06-07 · 高中友好</div>
      <h1>AI对齐<br>Alignment</h1>
      <p class="subtitle">为什么强大的 AI 还需要学会“按人的意思做事”？</p>
      <p class="core">核心一句话：AI对齐的本质，是让模型的能力、目标和边界尽量贴近人类真实意图，而不是只会“看起来很聪明”。</p>
      <div class="badges">
        <span class="badge">能力 ≠ 可靠</span><span class="badge">人类反馈</span><span class="badge">安全边界</span><span class="badge">RLHF 之后必学</span>
      </div>
    </header>

    <nav class="toc" aria-label="目录">
      <h2>目录（自动生成）</h2>
      <a href="#why">01 为什么这个概念重要？</a>
      <a href="#analogy">02 一个直观类比</a>
      <a href="#how">03 工作原理</a>
      <a href="#terms">04 关键术语解释</a>
      <a href="#case">05 一个真实应用案例</a>
      <a href="#myths">06 常见误区</a>
      <a href="#summary">07 3句话总结 + 复习问题</a>
    </nav>

    <section id="why">
      <h2>01 为什么这个概念重要？</h2>
      <p class="lead">AI 越强，越不能只问“它会不会做”，还要问“它会不会按我们真正想要的方式做”。</p>
      <p>一个模型可以写得很快、算得很准、调用工具很熟练，但如果它误解目标、泄露隐私、编造证据、绕过规则，能力越强，风险越大。AI对齐解决的正是这个问题：让模型不仅有能力，还要尽量有正确方向、边界感和可控性。</p>
      <div class="grid">
        <div class="card"><h3>它解决什么问题？</h3><p>人类说的话经常含糊、场景复杂、价值取舍难。对齐要减少“模型按字面钻空子，却违背真实意图”的情况。</p></div>
        <div class="card"><h3>为什么行业离不开它？</h3><p>AI客服、AI医生、自动驾驶、企业 Agent 都会影响真实人和真实系统。没有对齐，就很难上线到高风险场景。</p></div>
        <div class="card"><h3>它改变了什么？</h3><p>训练目标从“预测下一个词”扩展到“更有帮助、更诚实、更安全、更符合人类偏好”。</p></div>
        <div class="card"><h3>现实意义</h3><p>对齐让普通用户敢用，让企业敢接入，也让监管和产品团队有办法定义边界、评估风险、持续改进。</p></div>
      </div>
    </section>

    <section id="analogy">
      <h2>02 一个直观类比：老师带学生改作文</h2>
      <p>想象一个学生很会写字，词语丰富，句子漂亮。但老师要求写《科技如何改变学习方式》，他却写成“我最喜欢的小动物”。文章可能很流畅，但跑题了。</p>
      <p>这时老师不会说“你完全不会写”。老师会指出：题目是什么、哪些内容偏了、应该怎么组织论点、哪里不能乱编。学生根据反馈重写后，文章才从“有能力”变成“符合要求”。</p>
      <figure class="figure"><img src="{teacher_name}" alt="AI对齐像老师带学生改作文"><figcaption class="caption">图 1：对齐不是让 AI 变聪明，而是让 AI 把聪明用在正确方向。</figcaption></figure>
      <p class="note">抓住这个直觉：没有对齐的 AI，可能像一个很聪明但不看题目的学生。对齐要做的，是把能力拉回真实目标。</p>
    </section>

    <section id="how">
      <h2>03 工作原理：对齐如何发生？</h2>
      <figure class="figure"><img src="{loop_name}" alt="AI对齐闭环流程图"><figcaption class="caption">图 2：AI对齐通常是“人类意图、训练规则、模型输出、反馈评估、行为调整”的持续闭环。</figcaption></figure>
      <div class="steps">
        <div class="step"><h3>先定义人类真正想要什么</h3><p>不是只写一句“回答用户问题”，而是明确：要准确、要有帮助、不能泄露隐私、不能虚构来源、危险请求要拒绝。</p></div>
        <div class="step"><h3>用示范和规则教模型</h3><p>通过高质量指令数据、系统规则、安全政策，让模型看到“什么叫好的回答，什么叫不该做”。</p></div>
        <div class="step"><h3>收集人类偏好反馈</h3><p>让人比较多个回答：哪个更清楚？哪个更诚实？哪个更安全？这些偏好会变成训练信号。</p></div>
        <div class="step"><h3>不断评估、红队测试和修正</h3><p>上线前后都要用测试题、极端场景、真实反馈检查模型是否跑偏。对齐不是一次完成，而是长期维护。</p></div>
      </div>
    </section>

    <section id="terms">
      <h2>04 关键术语解释</h2>
      <div class="terms">
        <div class="card term"><b>对齐（Alignment）</b><p>专业解释：让 AI 系统的行为与人类意图、价值约束和安全要求尽量一致。<br>白话解释：让 AI 不只是能干，还要朝正确方向干。</p></div>
        <div class="card term"><b>能力（Capability）</b><p>专业解释：模型完成任务、理解信息、调用工具或生成内容的水平。<br>白话解释：学生会不会写、会不会算、会不会操作。</p></div>
        <div class="card term"><b>人类意图（Human Intent）</b><p>专业解释：用户在具体语境下真正希望系统完成的目标。<br>白话解释：你说“帮我写封邮件”，真正想要的是合适、准确、不过界。</p></div>
        <div class="card term"><b>偏好数据（Preference Data）</b><p>专业解释：人类对多个模型输出进行比较和排序得到的数据。<br>白话解释：老师在几篇答案里挑出更好的，并说明哪种更符合要求。</p></div>
        <div class="card term"><b>RLHF</b><p>专业解释：基于人类反馈的强化学习，用偏好信号优化模型行为。<br>白话解释：让模型根据人的打分和偏好，少犯同类错误。</p></div>
        <div class="card term"><b>奖励黑客（Reward Hacking）</b><p>专业解释：模型找到提升奖励分数但违背真实目标的行为。<br>白话解释：为了拿高分钻规则空子，表面赢了，实际跑偏了。</p></div>
      </div>
    </section>

    <section id="case">
      <h2>05 一个真实应用案例：企业 AI 客服</h2>
      <p>假设一家物流公司接入 AI 客服。用户问：“我的包裹延误了，能不能赔付？”一个能力强但未对齐的模型可能会为了“让用户满意”，直接承诺不该承诺的赔偿；也可能为了显得专业，编一个不存在的政策条款。</p>
      <p>对齐后的系统会更像一名受过培训的客服：先查订单状态，引用真实规则，说明能做什么和不能做什么；涉及退款、地址变更、隐私信息时，需要工具校验或人工确认。</p>
      <div class="grid">
        <div class="card"><h3>没有对齐</h3><p>回答听起来热情，但可能越权承诺、虚构政策、暴露隐私。</p></div>
        <div class="card"><h3>完成对齐</h3><p>既能解决问题，又守住证据、权限、隐私和安全边界。</p></div>
      </div>
    </section>

    <section id="myths">
      <h2>06 常见误区（非常重要）</h2>
      <div class="steps myth">
        <div class="step"><h3>误区 1：模型越聪明，就自然越对齐</h3><p>纠正：能力和方向是两回事。会写作文的学生，也可能跑题；会调用工具的 Agent，也可能调用错工具。</p></div>
        <div class="step"><h3>误区 2：对齐就是“限制模型”</h3><p>纠正：对齐不只是拒绝危险内容，更包括更准确、更诚实、更符合用户真实需求。</p></div>
        <div class="step"><h3>误区 3：写好提示词就等于完成对齐</h3><p>纠正：提示词只是表层约束。真正的对齐还涉及训练数据、偏好反馈、安全评估和上线监控。</p></div>
        <div class="step"><h3>误区 4：RLHF 可以一劳永逸解决对齐</h3><p>纠正：RLHF 很重要，但不完美。新场景、新攻击、新产品功能都会带来新的跑偏方式。</p></div>
        <div class="step"><h3>误区 5：拒绝越少，模型就越好用</h3><p>纠正：有些拒绝是在保护用户和系统。真正好的模型，是该帮时帮，该问清时问清，该拒绝时拒绝。</p></div>
      </div>
    </section>

    <section id="summary" class="summary">
      <h2>07 3句话总结</h2>
      <p>1. AI对齐关注的是“能力有没有用在正确方向”，而不只是模型是否强大。</p>
      <p>2. 对齐通常依靠示范数据、人类偏好反馈、安全规则、评估测试和持续迭代共同完成。</p>
      <p>3. 对齐不是一次性工程，也不是简单限制模型；它是让 AI 在真实世界可用、可信、可控的关键。</p>
      <h2>3个复习问题</h2>
      <ol>
        <li>为什么“学生作文写得流畅”并不等于“作文符合题目要求”？这个类比对应 AI 的什么问题？</li>
        <li>企业 AI 客服如果只追求“让用户满意”，可能会出现哪些跑偏行为？应该如何用对齐思路修正？</li>
        <li>为什么说 RLHF 很重要，但不能一劳永逸解决所有对齐问题？</li>
      </ol>
    </section>
    <footer>本报告为《AI每日深度科普》2026-06-07 期。中文图示为本次任务生成与重构，适合公开分享和邮件阅读。</footer>
  </main>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
    return html_path


def build() -> tuple[Path, Path]:
    style = STYLE
    base = Path(__file__).resolve().parent
    fallback_loop = base / "alignment_loop_fallback.png"
    fallback_teacher = base / "alignment_teacher_analogy_fallback.png"
    chatgpt_loop = base / "chatgpt_alignment_loop.png"
    chatgpt_teacher = base / "chatgpt_alignment_teacher_analogy.png"
    fig_loop = chatgpt_loop if chatgpt_loop.exists() else fallback_loop
    fig_teacher = chatgpt_teacher if chatgpt_teacher.exists() else fallback_teacher
    out_pdf = base / "2026-06-07_AI对齐（Alignment）.pdf"

    generate_alignment_loop_fallback(fallback_loop)
    generate_teacher_analogy_fallback(fallback_teacher)
    html_path = write_html(base, fig_loop, fig_teacher)

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

    page, draw, y = new_page("", 1)
    hero = (style.margin_x, 132, style.page_w - style.margin_x, 518)
    draw_card(draw, hero, 28, (247, 252, 252), style.line, 3)
    draw.text((style.margin_x + 28, 162), "2026-06-07", font=small_font, fill=style.quiet)
    draw.text((style.margin_x + 28, 205), "AI对齐", font=title_font, fill=style.ink)
    draw.text((style.margin_x + 28, 278), "Alignment", font=subtitle_font, fill=style.blue)
    draw.text((style.margin_x + 28, 328), "为什么强大的 AI 还需要学会“按人的意思做事”？", font=subtitle_font, fill=style.teal)
    draw_paragraph(
        draw,
        quote_font,
        "核心一句话：AI对齐的本质，是让模型的能力、目标和边界尽量贴近人类真实意图，而不是只会“看起来很聪明”。",
        style.margin_x + 28,
        386,
        max_w - 56,
        style.ink,
        line_gap=8,
    )
    bx = style.margin_x + 28
    for label, color in [
        ("高中友好", style.teal),
        ("能力与边界", style.blue),
        ("人类反馈", style.violet),
        ("AI安全基础", style.amber),
    ]:
        bx = draw_badge(draw, small_font, label, bx, 462, color, (255, 255, 255), style.line)

    y = 590
    y = draw_section_title(draw, h2_font, "目录（自动生成）", style.margin_x, y, style.blue)
    toc = [
        ("01", "为什么这个概念重要？", "能力越强，越要问它是否按真实意图行动。"),
        ("02", "一个直观类比", "像老师带学生改作文：会写不等于符合题意。"),
        ("03", "工作原理", "意图、规则、输出、反馈、调整的闭环。"),
        ("04", "关键术语解释", "能力、偏好数据、RLHF、奖励黑客。"),
        ("05", "真实应用案例", "企业 AI 客服如何既帮忙又不过界。"),
        ("06", "常见误区", "对齐不是简单限制，也不是一次完成。"),
        ("07", "3句话总结 + 复习问题", "检查是否真正理解“能力与方向”的区别。"),
    ]
    for num, title, desc in toc:
        row_h = 94
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + row_h), 18, (255, 255, 255), style.line, 2)
        draw.text((style.margin_x + 20, y + 27), num, font=h3_font, fill=style.teal)
        draw.text((style.margin_x + 92, y + 17), title, font=h3_font, fill=style.ink)
        draw.text((style.margin_x + 92, y + 52), desc, font=small_font, fill=style.muted)
        y += row_h + 13
    pages.append(page)

    page, draw, y = new_page("01 为什么重要", 2)
    y = draw_section_title(draw, h2_font, "为什么这个概念重要？", style.margin_x, y, style.teal)
    y = draw_paragraph(
        draw,
        body_font,
        "AI 越强，越不能只问“它会不会做”，还要问“它会不会按我们真正想要的方式做”。\n\n"
        "一个模型可以写得很快、算得很准、调用工具很熟练。但如果它误解目标、泄露隐私、编造证据、绕过规则，能力越强，风险越大。"
        "AI对齐解决的正是这个问题：让模型不仅有能力，还要尽量有正确方向、边界感和可控性。\n\n"
        "这也是为什么 ChatGPT、AI客服、自动驾驶、AI医生、企业 Agent 都离不开对齐。它们影响的不是一道练习题，而是真实的人、真实的钱、真实的数据和真实的安全。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 20
    cards = [
        ("它解决什么问题？", "人类说的话经常含糊，场景又复杂。对齐要减少“模型按字面钻空子，却违背真实意图”的情况。", style.blue),
        ("为什么行业离不开它？", "高风险 AI 产品必须守住隐私、证据、权限和安全边界。没有对齐，就很难可靠上线。", style.teal),
        ("它改变了什么？", "训练目标从“预测下一个词”扩展到“更有帮助、更诚实、更安全、更符合人类偏好”。", style.violet),
        ("现实意义", "对齐让用户敢用、企业敢接入，也让产品团队能持续定义边界、评估风险、改进体验。", style.amber),
    ]
    col_w = (max_w - 26) // 2
    for i, (title, body, color) in enumerate(cards):
        x = style.margin_x if i % 2 == 0 else style.margin_x + col_w + 26
        yy = y + (i // 2) * 244
        draw_card(draw, (x, yy, x + col_w, yy + 222), 20, (255, 255, 255), style.line, 2)
        draw.text((x + 22, yy + 20), title, font=h3_font, fill=color)
        draw_paragraph(draw, body_font, body, x + 22, yy + 66, col_w - 44, style.ink, line_gap=7)
    pages.append(page)

    page, draw, y = new_page("02 直观类比", 3)
    y = draw_section_title(draw, h2_font, "一个直观类比：老师带学生改作文", style.margin_x, y, style.teal)
    y = draw_paragraph(
        draw,
        body_font,
        "想象一个学生很会写字，词语丰富，句子漂亮。但老师要求写《科技如何改变学习方式》，他却写成“我最喜欢的小动物”。"
        "文章可能很流畅，但跑题了。\n\n"
        "这时老师不会说“你完全不会写”。老师会指出：题目是什么、哪些内容偏了、应该怎么组织论点、哪里不能乱编。"
        "学生根据反馈重写后，文章才从“有能力”变成“符合要求”。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 24
    y = paste_image_fit(page, fig_teacher, style.margin_x, y, max_w, 620)
    draw_paragraph(
        draw,
        small_font,
        "图 1：对齐不是让 AI 变聪明，而是让 AI 把聪明用在正确方向。",
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
        "没有对齐的 AI，可能像一个很聪明但不看题目的学生。对齐要做的，是把能力拉回真实目标。",
        style.margin_x + 28,
        y + 86,
        max_w - 56,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    page, draw, y = new_page("03 工作原理", 4)
    y = draw_section_title(draw, h2_font, "工作原理：对齐如何发生？", style.margin_x, y, style.blue)
    y = paste_image_fit(page, fig_loop, style.margin_x, y, max_w, 620)
    draw_paragraph(
        draw,
        small_font,
        "图 2：AI对齐通常是“人类意图、训练规则、模型输出、反馈评估、行为调整”的持续闭环。",
        style.margin_x,
        y,
        max_w,
        style.muted,
        line_gap=5,
    )
    y += 70
    steps = [
        ("第一步：定义人类真正想要什么", "明确目标、边界、隐私、证据和安全要求，而不是只写一句“回答用户问题”。"),
        ("第二步：用示范和规则教模型", "用高质量指令数据、系统规则和安全政策，让模型看到什么叫好的回答。"),
        ("第三步：收集人类偏好反馈", "让人比较多个回答：哪个更清楚、更诚实、更安全，并把偏好变成训练信号。"),
        ("第四步：持续评估和修正", "用红队测试、上线监控、用户反馈检查模型是否跑偏；对齐不是一次完成。"),
    ]
    draw_steps(draw, h3_font, small_font, steps, style.margin_x, y, max_w, style.blue, row_h=119)
    pages.append(page)

    page, draw, y = new_page("04 关键术语", 5)
    y = draw_section_title(draw, h2_font, "关键术语解释", style.margin_x, y, style.teal)
    terms = [
        ("对齐（Alignment）", "专业解释：让 AI 系统的行为与人类意图、价值约束和安全要求尽量一致。", "白话解释：让 AI 不只是能干，还要朝正确方向干。"),
        ("能力（Capability）", "专业解释：模型完成任务、理解信息、调用工具或生成内容的水平。", "白话解释：学生会不会写、会不会算、会不会操作。"),
        ("人类意图（Human Intent）", "专业解释：用户在具体语境下真正希望系统完成的目标。", "白话解释：你说“帮我写封邮件”，真正想要的是合适、准确、不过界。"),
        ("偏好数据（Preference Data）", "专业解释：人类对多个模型输出进行比较和排序得到的数据。", "白话解释：老师在几篇答案里挑出更好的，并说明哪种更符合要求。"),
        ("RLHF", "专业解释：基于人类反馈的强化学习，用偏好信号优化模型行为。", "白话解释：让模型根据人的打分和偏好，少犯同类错误。"),
        ("奖励黑客（Reward Hacking）", "专业解释：模型找到提升奖励分数但违背真实目标的行为。", "白话解释：为了拿高分钻规则空子，表面赢了，实际跑偏了。"),
    ]
    col_w = (max_w - 26) // 2
    y_left = y
    y_right = y
    for idx, (name, pro, plain) in enumerate(terms):
        x = style.margin_x if idx % 2 == 0 else style.margin_x + col_w + 26
        yy = y_left if idx % 2 == 0 else y_right
        box_h = 238
        draw_card(draw, (x, yy, x + col_w, yy + box_h), 20, (255, 255, 255), style.line, 2)
        draw.text((x + 20, yy + 18), name, font=h3_font, fill=style.blue if idx % 2 == 0 else style.teal)
        draw_paragraph(draw, small_font, pro, x + 20, yy + 62, col_w - 40, style.ink, line_gap=5)
        draw_paragraph(draw, small_font, plain, x + 20, yy + 136, col_w - 40, style.muted, line_gap=5)
        if idx % 2 == 0:
            y_left = yy + box_h + 18
        else:
            y_right = yy + box_h + 18
    pages.append(page)

    page, draw, y = new_page("05 真实应用", 6)
    y = draw_section_title(draw, h2_font, "真实应用案例：企业 AI 客服", style.margin_x, y, style.blue)
    y = draw_paragraph(
        draw,
        body_font,
        "假设一家物流公司接入 AI 客服。用户问：“我的包裹延误了，能不能赔付？”\n\n"
        "一个能力强但未对齐的模型，可能会为了“让用户满意”，直接承诺不该承诺的赔偿；也可能为了显得专业，编一个不存在的政策条款。"
        "这不是因为它不会说话，而是因为它没有把真实规则、证据边界和权限边界放在正确位置。\n\n"
        "对齐后的系统会更像一名受过培训的客服：先查订单状态，引用真实规则，说明能做什么和不能做什么；涉及退款、地址变更、隐私信息时，需要工具校验或人工确认。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    y += 22
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 462), 26, (248, 250, 252), style.line, 3)
    draw.text((style.margin_x + 28, y + 28), "同一句用户请求，两种系统表现", font=h2_font, fill=style.teal)
    left = (style.margin_x + 28, y + 96, style.margin_x + max_w // 2 - 14, y + 404)
    right = (style.margin_x + max_w // 2 + 14, y + 96, style.page_w - style.margin_x - 28, y + 404)
    draw_card(draw, left, 20, (255, 255, 255), (254, 202, 202), 3)
    draw_card(draw, right, 20, (255, 255, 255), (153, 246, 228), 3)
    draw.text((left[0] + 22, left[1] + 20), "没有对齐", font=h3_font, fill=style.red)
    draw_paragraph(draw, body_font, "听起来热情，但可能越权承诺、虚构政策、暴露隐私。", left[0] + 22, left[1] + 68, left[2] - left[0] - 44, style.ink, line_gap=8)
    draw.text((right[0] + 22, right[1] + 20), "完成对齐", font=h3_font, fill=style.teal)
    draw_paragraph(draw, body_font, "既能解决问题，又守住证据、权限、隐私和安全边界。", right[0] + 22, right[1] + 68, right[2] - right[0] - 44, style.ink, line_gap=8)
    y += 500
    draw_paragraph(
        draw,
        body_font,
        "这就是对齐的产品价值：不是让 AI 少做事，而是让 AI 在真实世界里做得更可靠、更可追责、更值得信任。",
        style.margin_x,
        y,
        max_w,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    page, draw, y = new_page("06 常见误区", 7)
    y = draw_section_title(draw, h2_font, "常见误区（非常重要）", style.margin_x, y, style.red)
    myths = [
        ("误区 1：模型越聪明，就自然越对齐", "纠正：能力和方向是两回事。会写作文的学生，也可能跑题；会调用工具的 Agent，也可能调用错工具。"),
        ("误区 2：对齐就是“限制模型”", "纠正：对齐不只是拒绝危险内容，更包括更准确、更诚实、更符合用户真实需求。"),
        ("误区 3：写好提示词就等于完成对齐", "纠正：提示词只是表层约束。真正的对齐还涉及训练数据、偏好反馈、安全评估和上线监控。"),
        ("误区 4：RLHF 可以一劳永逸解决对齐", "纠正：RLHF 很重要，但不完美。新场景、新攻击、新产品功能都会带来新的跑偏方式。"),
        ("误区 5：拒绝越少，模型就越好用", "纠正：有些拒绝是在保护用户和系统。真正好的模型，是该帮时帮，该问清时问清，该拒绝时拒绝。"),
    ]
    for title, body in myths:
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 178), 20, (255, 255, 255), style.line, 2)
        draw.text((style.margin_x + 22, y + 18), title, font=h3_font, fill=style.red)
        draw_paragraph(draw, body_font, body, style.margin_x + 22, y + 65, max_w - 44, style.ink, line_gap=7)
        y += 196
    pages.append(page)

    page, draw, y = new_page("07 总结复习", 8)
    y = draw_section_title(draw, h2_font, "3句话总结", style.margin_x, y, style.teal)
    summary = [
        "1. AI对齐关注的是“能力有没有用在正确方向”，而不只是模型是否强大。",
        "2. 对齐通常依靠示范数据、人类偏好反馈、安全规则、评估测试和持续迭代共同完成。",
        "3. 对齐不是一次性工程，也不是简单限制模型；它是让 AI 在真实世界可用、可信、可控的关键。",
    ]
    for line in summary:
        draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 120), 20, (248, 250, 252), style.line, 2)
        draw_paragraph(draw, body_font, line, style.margin_x + 24, y + 26, max_w - 48, style.ink, line_gap=7)
        y += 140

    y += 12
    y = draw_section_title(draw, h2_font, "3个复习问题", style.margin_x, y, style.blue)
    questions = (
        "1. 为什么“学生作文写得流畅”并不等于“作文符合题目要求”？这个类比对应 AI 的什么问题？\n\n"
        "2. 企业 AI 客服如果只追求“让用户满意”，可能会出现哪些跑偏行为？应该如何用对齐思路修正？\n\n"
        "3. 为什么说 RLHF 很重要，但不能一劳永逸解决所有对齐问题？"
    )
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 390), 24, (255, 255, 255), style.line, 3)
    draw_paragraph(draw, body_font, questions, style.margin_x + 26, y + 28, max_w - 52, style.ink, line_gap=9)
    y += 430
    draw_card(draw, (style.margin_x, y, style.page_w - style.margin_x, y + 196), 24, (247, 252, 252), style.line, 3)
    draw.text((style.margin_x + 24, y + 24), "下一步学习建议", font=h2_font, fill=style.teal)
    draw_paragraph(
        draw,
        body_font,
        "学完强化学习、RLHF 和 AI对齐后，适合继续学习 AI 安全、红队测试、多Agent系统和 Agent治理。"
        "这些主题会继续回答：当 AI 开始行动时，怎样让它既有效，又可靠。",
        style.margin_x + 24,
        y + 82,
        max_w - 48,
        style.ink,
        line_gap=8,
    )
    pages.append(page)

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    target_w = int(style.page_w * 0.82)
    target_h = int(style.page_h * 0.82)
    scaled_pages = [p.resize((target_w, target_h), Image.Resampling.LANCZOS) for p in pages]
    pal_pages = [p.convert("P", palette=Image.Palette.ADAPTIVE, colors=192) for p in scaled_pages]
    pal_pages[0].save(
        out_pdf,
        "PDF",
        resolution=100,
        save_all=True,
        append_images=pal_pages[1:],
        quality=88,
    )
    return out_pdf, html_path


if __name__ == "__main__":
    pdf, html = build()
    print(pdf)
    print(html)
