from __future__ import annotations

import html
import shutil
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
DATE = "2026-07-08"
CONCEPT = "Top-p（核采样）"
HTML = BASE / f"{DATE}_{CONCEPT}.html"
PDF = BASE / f"{DATE}_{CONCEPT}.pdf"
PREVIEW = BASE / "html_preview.png"
EMAIL_SUBJECT = BASE / "email_subject.txt"
EMAIL_BODY = BASE / "email_body.txt"
SOURCES_MD = BASE / "sources.md"
CHATGPT_IMAGE_DIR = Path("/Users/mac/.codex/generated_images/019f3f06-9926-73f2-b30a-d0575091268a")
CHATGPT_CANDIDATE_POOL = CHATGPT_IMAGE_DIR / "ig_05110629926fffe8016a4d939961a4819a895a00d7b0d4a508.png"
CHATGPT_TEMPERATURE_VS_TOPP = CHATGPT_IMAGE_DIR / "ig_05110629926fffe8016a4d93ce3880819ab4237516c3b3c1fb.png"

NAVY = "#122033"
INK = "#233044"
MUTED = "#65758b"
TEAL = "#16a394"
BLUE = "#2d6cdf"
ORANGE = "#e58b2a"
GREEN = "#2d9d68"
RED = "#d55a5f"
PALE = "#f5f8fb"
LINE = "#d8e1ea"


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    index = 0
    if weight in {"bold", "semibold"}:
        index = 1
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size, index=index)
            except Exception:
                return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


FONT_TITLE = font(58, "bold")
FONT_H2 = font(38, "bold")
FONT_H3 = font(28, "bold")
FONT_BODY = font(24)
FONT_SMALL = font(19)
FONT_TINY = font(16)


def wrap(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        current = ""
        for char in paragraph:
            candidate = current + char
            width = draw.textbbox((0, 0), candidate, font=font_obj)[2]
            if width <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = char
        if current:
            lines.append(current)
    return lines


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font_obj: ImageFont.FreeTypeFont,
    fill: str = INK,
    max_width: int | None = None,
    line_gap: int = 8,
) -> int:
    x, y = xy
    lines = [text] if max_width is None else wrap(draw, text, font_obj, max_width)
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += draw.textbbox((0, 0), line, font=font_obj)[3] + line_gap
    return y


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline: str | None = None, width: int = 2) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill: str = BLUE, width: int = 5) -> None:
    draw.line([start, end], fill=fill, width=width)
    x1, y1 = start
    x2, y2 = end
    if x2 >= x1:
        pts = [(x2, y2), (x2 - 18, y2 - 10), (x2 - 18, y2 + 10)]
    else:
        pts = [(x2, y2), (x2 + 18, y2 - 10), (x2 + 18, y2 + 10)]
    draw.polygon(pts, fill=fill)


def save_candidate_pool() -> None:
    img = Image.new("RGB", (1800, 1050), "#ffffff")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1800, 1050), fill="#ffffff")
    draw.rectangle((0, 0, 1800, 176), fill=PALE)
    draw_text(draw, (84, 52), "Top-p 核采样：只在可靠候选池里做选择", FONT_TITLE, NAVY)
    draw_text(draw, (86, 126), "核心直觉：先按概率排序，再把累计概率达到 p 的那一小圈留下，最后只在这圈里抽样。", FONT_BODY, MUTED)

    panels = [
        (90, 240, 520, 840, "1 模型先给候选 token 打概率", "像老师批改作文时，给每个可能的下一个词打一个“合适程度”。"),
        (685, 240, 1115, 840, "2 按概率从高到低排队", "最可能的词站前面，不靠谱的词站后面，形成一条候选长队。"),
        (1280, 240, 1710, 840, "3 截到累计概率 p=0.9", "只保留前面足够可靠的核心候选池，尾部小概率词暂时不参与抽样。"),
    ]
    for box in panels:
        x1, y1, x2, y2, title, desc = box
        rounded(draw, (x1, y1, x2, y2), 28, "#fbfdff", LINE, 3)
        draw_text(draw, (x1 + 34, y1 + 32), title, FONT_H3, NAVY, x2 - x1 - 68)
        draw_text(draw, (x1 + 34, y1 + 96), desc, FONT_SMALL, MUTED, x2 - x1 - 68, 6)

    tokens = [
        ("苹果", 0.36, GREEN),
        ("香蕉", 0.24, TEAL),
        ("水果", 0.18, BLUE),
        ("蛋糕", 0.12, ORANGE),
        ("火箭", 0.06, RED),
        ("古堡", 0.04, RED),
    ]
    base_y = 420
    for i, (label, prob, color) in enumerate(tokens):
        y = base_y + i * 66
        rounded(draw, (130, y, 480, y + 42), 15, "#ffffff", LINE, 2)
        draw.text((154, y + 8), label, font=FONT_SMALL, fill=INK)
        draw.rounded_rectangle((260, y + 12, 450, y + 30), radius=9, fill="#e9eef5")
        draw.rounded_rectangle((260, y + 12, int(260 + 190 * prob / 0.4), y + 30), radius=9, fill=color)
        draw.text((456, y + 5), f"{prob:.2f}", font=FONT_TINY, fill=MUTED)

    sorted_tokens = tokens
    cumulative = 0.0
    for i, (label, prob, color) in enumerate(sorted_tokens):
        y = base_y + i * 66
        cumulative += prob
        rounded(draw, (724, y, 1076, y + 46), 16, "#ffffff", LINE, 2)
        draw.text((748, y + 9), f"{i + 1}. {label}", font=FONT_SMALL, fill=INK)
        draw.text((885, y + 9), f"概率 {prob:.2f}", font=FONT_SMALL, fill=color)
        draw.text((994, y + 9), f"累计 {cumulative:.2f}", font=FONT_TINY, fill=MUTED)

    core = sorted_tokens[:4]
    tail = sorted_tokens[4:]
    draw_text(draw, (1324, 408), "核心候选池", FONT_H3, GREEN)
    cumulative = 0.0
    for i, (label, prob, color) in enumerate(core):
        cumulative += prob
        y = 468 + i * 62
        rounded(draw, (1330, y, 1648, y + 44), 15, "#ecf8f5", "#b8e5dd", 2)
        draw.text((1356, y + 9), label, font=FONT_SMALL, fill=INK)
        draw.text((1520, y + 9), f"{prob:.2f}", font=FONT_SMALL, fill=color)
    draw_text(draw, (1324, 738), "尾部小概率词：本轮不选", FONT_SMALL, RED)
    for i, (label, prob, _) in enumerate(tail):
        rounded(draw, (1330 + i * 158, 780, 1468 + i * 158, 822), 13, "#fff3f2", "#f3cccc", 2)
        draw.text((1354 + i * 158, 789), f"{label} {prob:.2f}", font=FONT_TINY, fill=RED)

    arrow(draw, (548, 540), (652, 540))
    arrow(draw, (1144, 540), (1248, 540))
    rounded(draw, (90, 906, 1710, 988), 22, "#122033", None)
    draw_text(
        draw,
        (132, 932),
        "一句话：Top-p 不是让 AI 更懂事实，而是减少它从很长尾、很奇怪的候选词里乱抽的机会。",
        FONT_BODY,
        "#ffffff",
        1536,
    )
    img.save(ASSETS / "top_p_candidate_pool.png")


def save_temperature_vs_topp() -> None:
    img = Image.new("RGB", (1800, 1050), "#ffffff")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1800, 1050), fill="#ffffff")
    draw.rectangle((0, 0, 1800, 176), fill=PALE)
    draw_text(draw, (86, 52), "Temperature 调形状，Top-p 定范围", FONT_TITLE, NAVY)
    draw_text(draw, (88, 126), "两个旋钮常被混在一起：一个改变概率分布的“尖或平”，一个决定参与抽样的“候选池有多大”。", FONT_BODY, MUTED)

    rounded(draw, (100, 244, 806, 844), 28, "#fbfdff", LINE, 3)
    rounded(draw, (994, 244, 1700, 844), 28, "#fbfdff", LINE, 3)
    draw_text(draw, (144, 286), "Temperature：调概率形状", FONT_H2, NAVY)
    draw_text(draw, (1038, 286), "Top-p：定候选范围", FONT_H2, NAVY)
    draw_text(draw, (144, 352), "像把“冒险程度”调高或调低。低温让最高概率更突出，高温让更多词有机会。", FONT_BODY, MUTED, 585)
    draw_text(draw, (1038, 352), "像菜单筛选：只允许累计概率达到 p 的那批候选上桌，尾部暂时不参与。", FONT_BODY, MUTED, 585)

    x0 = 184
    y0 = 640
    bars_low = [270, 145, 70, 34, 20]
    bars_high = [190, 160, 132, 100, 76]
    colors = [GREEN, TEAL, BLUE, ORANGE, RED]
    draw_text(draw, (178, 684), "低温：更保守", FONT_SMALL, GREEN)
    for i, h in enumerate(bars_low):
        x = x0 + i * 72
        draw.rounded_rectangle((x, y0 - h, x + 42, y0), radius=10, fill=colors[i])
    draw_text(draw, (510, 684), "高温：更发散", FONT_SMALL, ORANGE)
    for i, h in enumerate(bars_high):
        x = 520 + i * 72
        draw.rounded_rectangle((x, y0 - h, x + 42, y0), radius=10, fill=colors[i])
    draw.line((160, y0, 760, y0), fill=LINE, width=3)

    cx = 1126
    cy = 616
    probs = [0.36, 0.24, 0.18, 0.12, 0.05, 0.03, 0.02]
    labels = ["A", "B", "C", "D", "E", "F", "G"]
    cumulative = 0.0
    for i, prob in enumerate(probs):
        cumulative += prob
        x = cx + i * 74
        y = cy - int(prob * 520)
        in_pool = cumulative <= 0.90
        fill = [GREEN, TEAL, BLUE, ORANGE, "#8a9db5", "#a7b3c2", "#bec7d2"][i]
        if not in_pool:
            fill = "#d8dee6"
        draw.rounded_rectangle((x, y, x + 46, cy), radius=11, fill=fill)
        draw.text((x + 12, cy + 18), labels[i], font=FONT_TINY, fill=INK)
    draw.line((1096, cy, 1648, cy), fill=LINE, width=3)
    draw.line((1418, 478, 1418, 696), fill=RED, width=4)
    draw_text(draw, (1362, 424), "p=0.9 截断线", FONT_SMALL, RED)
    draw_text(draw, (1114, 738), "左侧留下：核心候选池", FONT_SMALL, GREEN)
    draw_text(draw, (1460, 738), "右侧暂不参与", FONT_SMALL, MUTED)

    rounded(draw, (100, 884, 1700, 982), 24, "#fff8ec", "#f1d19a", 2)
    draw_text(
        draw,
        (140, 912),
        "使用建议：日常问答通常保持默认；创意写作可以略放宽；事实任务不要指望 Top-p 自动纠错，仍要靠检索、证据和评估。",
        FONT_BODY,
        "#6c4a16",
        1510,
    )
    img.save(ASSETS / "temperature_vs_top_p.png")


SECTIONS = [
    (
        "why",
        "为什么这个概念重要？",
        """
        大模型每次回答，不是一次性把整段话“想好”，而是一个 token 一个 token 地往外生成。每一步，它都会面对一张候选名单：下一个最可能是“苹果”、也可能是“香蕉”、还可能是一些概率很低但奇怪的词。

        如果模型总是选概率最高的那个词，回答会很稳定，但可能像模板一样死板。如果它完全随便抽，回答会更有变化，却更容易跑偏。Top-p 就是在这两者之间放了一个边界：不是从所有词里乱抽，而是只从“累计概率够高的一小圈候选词”里抽。

        这很重要，因为今天的 AI 写作、客服、搜索总结、代码助手和创意工具，都要在“稳定”和“多样”之间做平衡。Top-p 决定了模型生成时的候选范围，理解它，就能看懂很多 AI 产品为什么会有不同的风格、风险和使用建议。
        """,
    ),
    (
        "analogy",
        "一个直观类比：在菜单里点菜",
        """
        想象你走进一家餐厅，服务员根据你的口味推荐下一道菜。菜单上有 100 道菜，但前几道特别符合你的需求：清蒸鱼、炒青菜、米饭、汤。后面也有一些菜，比如生日蛋糕、辣椒冰淇淋、实验室试剂风味饮料，虽然不是绝对不可能，但明显很离谱。

        如果服务员从 100 道菜里随便抽，你可能会吃到奇怪组合。如果他只给你概率最高的第一道菜，每次都很安全，但也太单调。Top-p 像一个“只看靠谱菜单”的规则：把最符合需求的菜按推荐概率排好，累计到 90% 左右就停，剩下长尾奇怪选项先不看。

        所以，Top-p 的核心不是“让 AI 更聪明”，而是“让 AI 在一个更合理的候选范围里做选择”。它像餐厅经理在点菜前先划掉不靠谱选项。
        """,
    ),
    (
        "principle",
        "工作原理：Top-p 到底怎么运作？",
        """
        第一步，模型先给所有可能的下一个 token 打分。这个分数还不是最终概率，可以理解为“它觉得每个词有多合适”。

        第二步，系统把这些分数变成概率，并从高到低排序。比如最高概率的词是 0.36，第二个是 0.23，第三个是 0.15。

        第三步，从最高概率开始往后累加，直到累计概率达到 p。假设 p=0.9，那么前面几个词的概率加起来一旦达到 90%，候选池就截断。

        第四步，模型只在这个候选池里抽样，生成下一个 token。下一步再重新计算、重新排序、重新截断。也就是说，Top-p 不是一次设置后固定菜单，而是每生成一个 token 都动态更新。
        """,
    ),
    (
        "terms",
        "关键术语解释",
        "",
    ),
    (
        "case",
        "一个真实应用案例：AI 写作助手为什么要用 Top-p",
        """
        假设你让 AI 写一封客户道歉邮件。模型下一句可以写“非常抱歉给您带来不便”，也可以写“我们理解您的着急”，这些都是合理候选。它也可能有极低概率写出夸张、幽默或不合场景的话。

        在严肃客服场景里，产品通常希望回复稳定、得体、少出错，于是会用较保守的采样设置：Top-p 不放得太宽，Temperature 也不太高。这样模型仍有一点表达变化，但不太容易跳到奇怪词汇。

        在广告文案、故事创作、头脑风暴里，系统可能允许更宽的候选池，让模型探索更多表达。此时 Top-p 可以略放宽，但仍不是越大越好。越大，长尾词越容易进来，惊喜和跑偏会同时增加。
        """,
    ),
    (
        "misconceptions",
        "常见误区",
        """
        误区一：Top-p 越高，AI 越聪明。不对。Top-p 只改变候选范围，不增加知识，也不会提高推理能力。

        误区二：Top-p 可以防止幻觉。不对。它能减少一部分离谱抽样，但事实错误主要还要靠检索、证据、工具调用和评估。

        误区三：Top-p 和 Temperature 是同一个东西。不对。Temperature 改变概率分布的形状，Top-p 决定候选池的边界。

        误区四：把 Top-p 设成 1 就最好。不一定。p=1 接近允许从完整分布里抽样，长尾词更容易参与，创意可能增加，失控风险也会增加。

        误区五：所有任务都应该手动调 Top-p。不需要。大多数普通用户保持默认即可。只有当你明确要控制稳定性、创意性或批量生成风格时，才值得调整。
        """,
    ),
    (
        "summary",
        "总结：3句话讲清核心认知",
        "",
    ),
    (
        "questions",
        "复习问题",
        "",
    ),
]

TERMS = [
    ("Token", "模型处理和生成文本时的基本单位，可以是字、词或词的一部分。", "AI 写字时不是一次写整段，而是像拼积木一样一个小块一个小块往外放。"),
    ("Logits", "模型在变成概率之前，对每个候选 token 给出的原始分数。", "像老师先给每个答案打草稿分，还没换算成百分比。"),
    ("Probability Distribution", "所有候选 token 概率加起来为 1 的分布。", "像一张抽奖券表：每个词有自己的中奖概率。"),
    ("Top-p / Nucleus Sampling", "按概率从高到低累加，保留累计概率达到 p 的最小候选集合，再从中抽样。", "只在最靠谱的一圈候选词里抽，不让很长尾的奇怪词随便混进来。"),
    ("Temperature", "调节概率分布尖锐或平坦程度的采样参数。", "像调“保守或冒险”的旋钮，但不是智商旋钮。"),
]

SUMMARY_POINTS = [
    "Top-p 的本质，是给模型的下一 token 抽样画出一个“可靠候选池”。",
    "它控制的是生成范围，不是知识来源，也不是事实检查器。",
    "理解 Top-p 后，你会更清楚：AI 的回答风格，既来自模型能力，也来自生成时的采样规则。",
]

QUESTIONS = [
    "如果一个 AI 写客服回复总是太死板，你会更可能调 Top-p、Temperature，还是让它联网搜索？为什么？",
    "为什么 Top-p 能减少一部分奇怪表达，却不能保证回答事实正确？请用“菜单点菜”的类比解释。",
    "Temperature 和 Top-p 都会影响生成结果。请分别用一句话说明：一个在调什么，一个在限制什么。",
]

SOURCES = [
    ("OpenAI API Reference: Responses create - temperature and top_p parameters", "https://developers.openai.com/api/reference/resources/responses/methods/create"),
    ("Hugging Face Transformers: Text generation parameters", "https://huggingface.co/docs/transformers/en/main_classes/text_generation"),
    ("Hugging Face Transformers: Generation strategies", "https://huggingface.co/docs/transformers/en/generation_strategies"),
    ("Holtzman et al.: The Curious Case of Neural Text Degeneration", "https://arxiv.org/abs/1904.09751"),
    ("OpenAI Cookbook: How to generate text - sampling controls", "https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models"),
]


def paragraph_html(text: str) -> str:
    parts = [p.strip() for p in textwrap.dedent(text).strip().split("\n\n") if p.strip()]
    return "\n".join(f"<p>{html.escape(part)}</p>" for part in parts)


def render_html() -> str:
    toc = "\n".join(f'<a href="#{sid}">{i + 1}. {html.escape(title)}</a>' for i, (sid, title, _) in enumerate(SECTIONS))
    section_blocks: list[str] = []
    for sid, title, body in SECTIONS:
        if sid == "analogy":
            content = paragraph_html(body) + """
            <figure>
              <img src="assets/top_p_candidate_pool.png" alt="Top-p 核采样候选池流程图">
              <figcaption>图解：Top-p 先按概率排序，再截出核心候选池，最后只在池内抽样。</figcaption>
            </figure>
            """
        elif sid == "principle":
            content = """
            <figure>
              <img src="assets/temperature_vs_top_p.png" alt="Temperature 和 Top-p 的分工图">
              <figcaption>图解：Temperature 改变概率分布形状，Top-p 决定抽样候选范围。</figcaption>
            </figure>
            """ + paragraph_html(body) + """
            <div class="steps">
              <div><b>1. 打分</b><span>模型给所有候选 token 一个原始分数。</span></div>
              <div><b>2. 排序</b><span>把概率从高到低排队。</span></div>
              <div><b>3. 累加</b><span>从前往后加到 p，例如 0.9。</span></div>
              <div><b>4. 抽样</b><span>只在保留下来的候选池里选。</span></div>
            </div>
            """
        elif sid == "terms":
            rows = "\n".join(
                f"<tr><th>{html.escape(term)}</th><td>{html.escape(pro)}</td><td>{html.escape(plain)}</td></tr>"
                for term, pro, plain in TERMS
            )
            content = f"""
            <table>
              <thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
            """
        elif sid == "misconceptions":
            items = []
            for line in [p.strip() for p in body.strip().split("\n\n") if p.strip()]:
                head, rest = line.split("。", 1)
                items.append(f"<li><strong>{html.escape(head)}。</strong><span>{html.escape(rest.strip())}</span></li>")
            content = "<ul class=\"mistakes\">" + "\n".join(items) + "</ul>"
        elif sid == "summary":
            content = "<div class=\"summary-grid\">" + "\n".join(
                f"<div>{i + 1}. {html.escape(point)}</div>" for i, point in enumerate(SUMMARY_POINTS)
            ) + "</div>"
        elif sid == "questions":
            content = "<ol class=\"questions\">" + "\n".join(f"<li>{html.escape(q)}</li>" for q in QUESTIONS) + "</ol>"
        else:
            content = paragraph_html(body)
        section_blocks.append(f'<section id="{sid}"><h2>{html.escape(title)}</h2>{content}</section>')

    source_links = "\n".join(f'<li><a href="{url}">{html.escape(name)}</a></li>' for name, url in SOURCES)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{DATE}_{CONCEPT}</title>
  <style>
    :root {{
      --navy: #122033;
      --ink: #253044;
      --muted: #637083;
      --line: #dce5ee;
      --paper: #f5f8fb;
      --teal: #16a394;
      --blue: #2d6cdf;
      --orange: #e58b2a;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: #ffffff;
      line-height: 1.75;
      letter-spacing: 0;
    }}
    .page {{
      width: min(1080px, calc(100% - 44px));
      margin: 0 auto;
    }}
    .hero {{
      min-height: 760px;
      padding: 88px 0 52px;
      background:
        linear-gradient(180deg, #f6f9fc 0%, #ffffff 86%);
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      display: inline-flex;
      gap: 10px;
      align-items: center;
      font-size: 14px;
      color: var(--muted);
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 8px 14px;
      background: rgba(255,255,255,.76);
    }}
    h1 {{
      font-size: clamp(52px, 8vw, 98px);
      line-height: 1.02;
      margin: 42px 0 22px;
      color: var(--navy);
      letter-spacing: 0;
    }}
    h1 span {{
      display: block;
      color: var(--teal);
      font-size: .54em;
      margin-top: 16px;
    }}
    .subtitle {{
      font-size: 30px;
      color: #405168;
      margin: 0 0 28px;
      max-width: 880px;
    }}
    .core {{
      display: block;
      max-width: 900px;
      background: #122033;
      color: #ffffff;
      border-radius: 8px;
      padding: 24px 28px;
      font-size: 25px;
      line-height: 1.55;
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 14px;
      margin-top: 44px;
    }}
    .hero-grid div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px 18px 16px;
      background: rgba(255,255,255,.72);
      min-height: 118px;
    }}
    .hero-grid b {{
      display: block;
      color: var(--navy);
      margin-bottom: 6px;
    }}
    .toc {{
      position: sticky;
      top: 0;
      z-index: 2;
      background: rgba(255,255,255,.94);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--line);
    }}
    .toc .page {{
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding: 14px 0;
    }}
    .toc a {{
      white-space: nowrap;
      color: var(--muted);
      text-decoration: none;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 7px 12px;
      font-size: 14px;
    }}
    section {{
      padding: 58px 0;
      border-bottom: 1px solid var(--line);
    }}
    h2 {{
      color: var(--navy);
      font-size: 34px;
      line-height: 1.25;
      margin: 0 0 22px;
      letter-spacing: 0;
    }}
    p {{
      font-size: 19px;
      margin: 0 0 18px;
    }}
    figure {{
      margin: 34px 0;
      padding: 0;
    }}
    img {{
      display: block;
      width: 100%;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: #fff;
    }}
    figcaption {{
      color: var(--muted);
      font-size: 15px;
      margin-top: 10px;
    }}
    .steps {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-top: 28px;
    }}
    .steps div, .summary-grid div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      background: #fbfdff;
    }}
    .steps b {{
      display: block;
      color: var(--teal);
      margin-bottom: 6px;
    }}
    .steps span {{
      color: var(--muted);
      font-size: 15px;
      line-height: 1.55;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 8px;
      font-size: 16px;
    }}
    th, td {{
      text-align: left;
      vertical-align: top;
      padding: 16px;
      border-bottom: 1px solid var(--line);
    }}
    th {{
      color: var(--navy);
      background: #f5f8fb;
      width: 22%;
    }}
    thead th {{
      background: #122033;
      color: #ffffff;
    }}
    .mistakes {{
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      gap: 12px;
    }}
    .mistakes li {{
      border-left: 5px solid var(--orange);
      background: #fff9ef;
      border-radius: 8px;
      padding: 16px 18px;
    }}
    .mistakes strong {{
      display: block;
      color: #6b4311;
      margin-bottom: 4px;
    }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      font-size: 18px;
    }}
    .questions {{
      font-size: 19px;
      padding-left: 26px;
    }}
    .questions li {{
      margin-bottom: 14px;
      padding-left: 6px;
    }}
    .sources {{
      background: #f6f8fb;
      padding: 48px 0 64px;
      color: var(--muted);
    }}
    .sources h2 {{
      font-size: 26px;
    }}
    .sources a {{
      color: var(--blue);
    }}
    @page {{
      size: A4;
      margin: 0;
    }}
    @media print {{
      body {{ background: #fff; }}
      .toc {{ position: static; }}
      section {{ break-inside: avoid; padding: 36px 0; }}
      .hero {{ min-height: 680px; }}
      img {{ max-height: 520px; object-fit: contain; }}
    }}
    @media (max-width: 760px) {{
      .page {{ width: min(100% - 28px, 1080px); }}
      .hero {{ padding-top: 56px; min-height: auto; }}
      .subtitle {{ font-size: 23px; }}
      .core {{ font-size: 20px; }}
      .hero-grid, .steps, .summary-grid {{ grid-template-columns: 1fr; }}
      h2 {{ font-size: 28px; }}
      p {{ font-size: 17px; }}
      table {{ font-size: 14px; }}
      th, td {{ padding: 12px; }}
    }}
  </style>
</head>
<body>
  <header class="hero">
    <div class="page">
      <div class="eyebrow">AI 每日深度科普 · {DATE} · 生成式 AI 基础认知</div>
      <h1>Top-p 核采样<span>为什么 AI 不是从所有词里乱选？</span></h1>
      <p class="subtitle">从“概率菜单”理解大模型如何在稳定与多样之间做选择。</p>
      <div class="core">核心一句话：Top-p 的本质，是给 AI 的下一个词选择画出一个“可靠候选池”，让它只在最可能的一圈答案里抽样。</div>
      <div class="hero-grid">
        <div><b>它解决什么</b><span>减少从长尾小概率词里抽到奇怪表达的机会。</span></div>
        <div><b>它影响什么</b><span>回答的稳定性、多样性、创意性和失控风险。</span></div>
        <div><b>它不是什么</b><span>不是事实检查器，也不会让模型凭空知道更多。</span></div>
      </div>
    </div>
  </header>
  <nav class="toc"><div class="page">{toc}</div></nav>
  <main class="page">
    {''.join(section_blocks)}
  </main>
  <footer class="sources">
    <div class="page">
      <h2>参考来源</h2>
      <ul>{source_links}</ul>
    </div>
  </footer>
</body>
</html>
"""


def write_text_assets() -> None:
    EMAIL_SUBJECT.write_text("【AI每日深度科普】Top-p 核采样：为什么AI不是从所有词里乱选？\n", encoding="utf-8")
    EMAIL_BODY.write_text(
        """今天的主题是 Top-p（核采样）。

这是理解大模型“生成风格”的关键概念之一：它解释了 AI 为什么既不能总选最稳的词，也不能从所有词里乱抽。

附件内容将用“菜单点菜”和“候选词池”的类比，讲清楚：
Top-p 如何限制抽样范围、它和 Temperature 的区别，以及为什么它不是事实检查器。

本封为最终图解版，请以此附件为准。

适合：
非技术读者、AI初学者、产品经理、业务负责人、投资研究者阅读。
""",
        encoding="utf-8",
    )
    SOURCES_MD.write_text(
        "# Sources\n\n" + "\n".join(f"- {name}\n  {url}" for name, url in SOURCES) + "\n",
        encoding="utf-8",
    )


def copy_chatgpt_image_assets() -> None:
    if CHATGPT_CANDIDATE_POOL.exists() and CHATGPT_TEMPERATURE_VS_TOPP.exists():
        shutil.copy2(CHATGPT_CANDIDATE_POOL, ASSETS / "top_p_candidate_pool.png")
        shutil.copy2(CHATGPT_TEMPERATURE_VS_TOPP, ASSETS / "temperature_vs_top_p.png")


def launch_chromium(playwright):
    candidates = [
        None,
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    last_error: Exception | None = None
    for executable_path in candidates:
        try:
            kwargs = {"headless": True}
            if executable_path and Path(executable_path).exists():
                kwargs["executable_path"] = executable_path
            elif executable_path:
                continue
            return playwright.chromium.launch(**kwargs)
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not launch Chromium/Chrome: {last_error}")


def build_pdf() -> None:
    with sync_playwright() as p:
        browser = launch_chromium(p)
        try:
            page = browser.new_page(viewport={"width": 1240, "height": 1754}, device_scale_factor=1)
            page.goto(HTML.as_uri(), wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(PDF),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            page.screenshot(path=str(PREVIEW), full_page=True)
        finally:
            browser.close()


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    save_candidate_pool()
    save_temperature_vs_topp()
    copy_chatgpt_image_assets()
    HTML.write_text(render_html(), encoding="utf-8")
    write_text_assets()
    build_pdf()
    print(PDF)


if __name__ == "__main__":
    main()
