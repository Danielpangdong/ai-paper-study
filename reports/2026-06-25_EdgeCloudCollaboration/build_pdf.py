from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from string import Template

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-25"
CONCEPT_CN = "端云协同"
CONCEPT_EN = "Edge-cloud Collaboration"
CONCEPT_FULL = f"{CONCEPT_CN}（{CONCEPT_EN}）"
HTML_NAME = f"{DATE}_{CONCEPT_FULL}.html"
PDF_NAME = f"{DATE}_{CONCEPT_FULL}.pdf"

FIG_ANALOGY_BASE = "chatgpt_edge_cloud_analogy_base.png"
FIG_WORKFLOW_BASE = "chatgpt_edge_cloud_workflow_base.png"
FIG_ANALOGY = "chatgpt_edge_cloud_analogy.png"
FIG_WORKFLOW = "chatgpt_edge_cloud_workflow.png"

FONT_REGULAR = Path("/System/Library/Fonts/STHeiti Light.ttc")
FONT_BOLD = Path("/System/Library/Fonts/STHeiti Medium.ttc")


WHY = [
    "过去我们常把 AI 想成两种形态：要么在手机、电脑、摄像头里本地运行；要么把问题发到云端，让大模型回答。但真实的 AI 产品通常不是二选一，而是在多个位置之间做分工。",
    "端云协同要解决的，就是“把任务放在哪里做最合适”的问题。简单、敏感、需要立刻响应的任务，适合放在用户设备或附近节点；复杂推理、长文本、多工具调用和大知识库任务，往往需要云端大模型。",
    "这个概念重要，是因为它同时影响用户体验、隐私边界、成本结构和系统稳定性。一次 AI 请求慢不慢、贵不贵、是否泄露敏感信息、断网时还能不能工作，都和端云协同有关。",
    "理解端云协同之后，你会发现 AI 产品不是“一个模型回答一切”，而是一套调度系统：像交通枢纽一样，持续判断哪条路最快、最稳、最省、最安全。",
]

ANALOGY = [
    "想象一个城市外卖系统。用户点餐后，并不是所有订单都送到最远的总部厨房处理。",
    "如果只是热一杯咖啡，小区门口的便利店就能完成，最快也最省。如果是热门套餐，附近的中央厨房提前备好了半成品，几分钟就能送到。如果是非常复杂的定制宴席，才需要总部大厨和完整后厨。",
    "AI 里的端云协同也是这样。手机里的 NPU 像小区便利店，负责本地、隐私、即时的小任务；边缘节点像附近中央厨房，离用户更近，可以缓存热门模型、降低延迟；云端大模型像总部后厨，能力最强，但距离更远、成本更高，也更需要严谨的隐私和权限设计。",
    "真正聪明的地方不在于“谁最强”，而在于调度器会看订单：这件事是不是敏感？要不要马上完成？本地模型够不够？网络好不好？云端成本值不值？然后把任务交给合适的位置。",
]

MECHANISM = [
    ("请求进入 AI 应用", "用户说一句话、上传一张图、打开相机翻译，系统先把它识别成一个具体 AI 任务。"),
    ("调度器判断任务类型", "系统会看隐私、延迟、能力、成本和网络状态：能在本地做就不必上云，本地做不好再升级。"),
    ("设备端处理小而敏感的任务", "例如关键词识别、照片分类、简单改写、键盘预测、离线翻译等，优先用手机或电脑里的模型和 NPU。"),
    ("边缘节点负责就近加速", "靠近用户的服务器可以承接热门任务、缓存模型结果、减少网络往返时间，也能在局部区域内更稳定地服务。"),
    ("云端处理复杂任务", "需要大模型、长上下文、多步推理、多工具调用或企业知识库时，系统会把请求送到云端。"),
    ("结果合并后返回用户", "用户看到的是一个连续体验，背后可能已经经过本地预处理、边缘加速和云端推理。"),
    ("监控反馈持续优化", "系统会记录速度、成本、失败率和质量表现，下一次遇到类似任务时就能更聪明地选择路线。"),
]

TERMS = [
    ("端侧 / 设备端", "专业解释：用户手机、电脑、摄像头、汽车等终端设备。", "白话解释：离你最近、就在你手边的 AI 运行位置。"),
    ("云端", "专业解释：远程数据中心里的计算资源，通常承载更大模型和更重任务。", "白话解释：能力更强的总部后厨，但要经过网络。"),
    ("边缘节点", "专业解释：位于用户和中心云之间、距离用户更近的计算节点。", "白话解释：附近的中央厨房，比总部近，比你家设备强。"),
    ("本地推理", "专业解释：模型直接在设备上完成输入到输出的计算。", "白话解释：不把题目寄出去，手机自己做完。"),
    ("云端推理", "专业解释：把请求发送到服务器，由云端模型完成计算并返回结果。", "白话解释：把难题交给远处更强的老师。"),
    ("NPU", "专业解释：面向神经网络计算的专用处理单元，常见于手机和电脑。", "白话解释：设备里专门帮 AI 干活的省电芯片。"),
    ("延迟 Latency", "专业解释：从请求发出到收到结果所经历的时间。", "白话解释：你等 AI 回答要等多久。"),
    ("带宽 Bandwidth", "专业解释：单位时间内网络或内存能传输的数据量。", "白话解释：路有多宽，能同时运多少东西。"),
    ("隐私边界", "专业解释：哪些数据可以离开设备、进入哪些系统、被谁处理的规则。", "白话解释：什么东西只能在家里看，不能拿去外面处理。"),
    ("模型路由", "专业解释：根据任务和系统状态，把请求分配给不同模型或计算位置。", "白话解释：给每个问题选最合适的老师和教室。"),
    ("降级 / 回退", "专业解释：当网络、模型或服务异常时，切换到能力较弱但可用的方案。", "白话解释：总部厨房堵单时，先用附近厨房做简化版。"),
    ("混合推理", "专业解释：端侧、边缘和云端共同完成一次或一类 AI 任务。", "白话解释：一道菜由便利店、中央厨房和总部后厨接力完成。"),
]

CASE = [
    "一个真实案例，是现代手机和电脑上的智能助手。很多基础任务可以在设备端完成：识别语音唤醒词、整理照片、做简单文本建议、判断一段内容是否需要继续处理。这样做速度快，也减少敏感数据离开设备的机会。",
    "但当用户提出更复杂的问题，比如总结很长的资料、跨多个应用理解上下文、生成复杂文档或进行多步推理，本地小模型可能能力不够。这时系统可以把任务升级到云端更大的模型，或者进入更严格的私有云计算环境。",
    "Apple 的 Private Cloud Compute 就体现了这种思路：设备优先处理能本地完成的任务，更复杂的请求再进入专门设计的云端隐私计算系统。它说明端云协同不是简单“联网使用 AI”，而是在能力、隐私和成本之间做工程设计。",
    "另一个常见案例是 AI 客服。用户的简单问题可以由本地规则或边缘缓存快速回答；涉及订单、合同、复杂投诉时，再调用云端大模型和企业知识库。用户只看到一个客服窗口，背后其实是一套分层调度系统。",
]

MISTAKES = [
    ("误区一：端云协同就是把 AI 放到云上。", "不对。端云协同强调分工：能本地做的尽量本地做，需要更强能力时才上云或走边缘节点。"),
    ("误区二：本地 AI 一定更安全。", "本地处理通常能减少数据外传，但安全还取决于设备系统、权限管理、模型行为和数据保存方式。"),
    ("误区三：云端 AI 一定更聪明。", "云端模型通常更大，但简单任务交给云端可能浪费时间和成本。本地小模型在特定场景可能更快、更稳。"),
    ("误区四：边缘节点只是一个小云。", "边缘节点的价值在于“近”：更低延迟、更少网络绕路、更适合区域性缓存和实时任务。"),
    ("误区五：端云协同等于联网搜索。", "不是。联网搜索是找资料；端云协同是决定计算在哪里发生，可能包含搜索，也可能完全不搜索。"),
    ("误区六：任务路由只看模型能力。", "实际系统还要看隐私、成本、网络、负载、失败率、设备电量和用户体验。"),
    ("误区七：断网就完全不能用 AI。", "如果设计了本地模型和降级方案，很多简单任务仍能离线工作，只是复杂任务可能受限。"),
    ("误区八：端云协同和边缘AI是同一个概念。", "边缘AI强调 AI 在设备或近端运行；端云协同强调设备、边缘和云端如何一起分工。"),
]

SUMMARY = [
    "端云协同的本质，是把合适的 AI 任务交给合适的位置，而不是让一个模型包办一切。",
    "设备端负责隐私、即时和低功耗，边缘节点负责就近加速，云端负责强推理、大知识和复杂工具协作。",
    "未来好用的 AI 产品，竞争的不只是模型大小，更是调度、成本、隐私和稳定性组成的系统能力。",
]

QUIZ = [
    "如果一个 AI 翻译功能要求“离线、低延迟、保护隐私”，你会把它优先放在设备端、边缘节点还是云端？为什么？",
    "为什么一个复杂 AI 助手不应该把所有请求都发给最大的云端模型？请从成本、速度和隐私三个角度解释。",
    "端云协同和边缘AI有什么区别？请用“外卖系统”的类比说明两者关系。",
]

SOURCES = [
    ("Apple Private Cloud Compute: A new frontier for AI privacy in the cloud", "https://security.apple.com/blog/private-cloud-compute/"),
    ("Apple Private Cloud Compute Security Guide", "https://security.apple.com/documentation/private-cloud-compute"),
    ("Google AI Edge", "https://developers.google.com/edge"),
    ("NVIDIA Edge Computing Solutions", "https://www.nvidia.com/en-us/edge-computing/"),
    ("Microsoft Azure: What is edge computing?", "https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-edge-computing"),
    ("Microsoft Azure IoT Edge", "https://azure.microsoft.com/en-us/products/iot-edge"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(str(path), size=size)


def wrap_text(text: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> str:
    lines: list[str] = []
    current = ""
    probe = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(probe)
    for char in text:
        if char == "\n":
            lines.append(current)
            current = ""
            continue
        trial = current + char
        width = draw.textbbox((0, 0), trial, font=font_obj)[2]
        if width <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return "\n".join(lines)


def draw_label(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    accent: str,
) -> None:
    x1, y1, x2, y2 = box
    radius = 22
    draw.rounded_rectangle((x1, y1, x2, y2), radius=radius, fill=(255, 255, 255, 235), outline=(204, 220, 232), width=2)
    draw.rounded_rectangle((x1 + 16, y1 + 18, x1 + 28, y2 - 18), radius=6, fill=accent)
    title_font = font(34, bold=True)
    body_font = font(24)
    draw.text((x1 + 46, y1 + 20), title, fill=(17, 24, 39), font=title_font)
    wrapped = wrap_text(body, body_font, x2 - x1 - 70)
    draw.multiline_text((x1 + 46, y1 + 68), wrapped, fill=(55, 65, 81), font=body_font, spacing=8)


def draw_badge(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fill: tuple[int, int, int, int],
) -> None:
    badge_font = font(23, bold=True)
    x, y = xy
    w = draw.textbbox((0, 0), text, font=badge_font)[2] + 34
    h = 44
    draw.rounded_rectangle((x, y, x + w, y + h), radius=20, fill=fill)
    draw.text((x + 17, y + 8), text, fill=(255, 255, 255), font=badge_font)


def compose_images() -> None:
    analogy = Image.open(ROOT / FIG_ANALOGY_BASE).convert("RGBA")
    draw = ImageDraw.Draw(analogy, "RGBA")
    draw_label(draw, (86, 88, 455, 210), "用户设备", "隐私、即时、低功耗；适合简单小任务", (15, 139, 141, 255))
    draw_label(draw, (660, 86, 1045, 226), "边缘节点", "离用户更近；缓存、加速、承接热门任务", (18, 56, 114, 255))
    draw_label(draw, (1190, 86, 1608, 226), "云端大模型", "强推理、大知识、长上下文和多工具协作", (35, 122, 87, 255))
    draw_label(draw, (392, 720, 1280, 850), "核心直觉：不是谁取代谁，而是谁更适合", "调度器根据隐私、延迟、成本、能力和网络状态，把任务送到最合适的位置。", (161, 98, 7, 255))
    draw_badge(draw, (180, 248), "本地优先", (15, 139, 141, 230))
    draw_badge(draw, (737, 252), "就近加速", (18, 56, 114, 230))
    draw_badge(draw, (1322, 252), "能力兜底", (35, 122, 87, 230))
    analogy.save(ROOT / FIG_ANALOGY)

    workflow = Image.open(ROOT / FIG_WORKFLOW_BASE).convert("RGBA")
    draw = ImageDraw.Draw(workflow, "RGBA")
    draw_label(draw, (80, 560, 340, 692), "用户请求", "一句话、一张图、一次翻译或一次助手任务", (18, 56, 114, 255))
    draw_label(draw, (555, 92, 980, 246), "智能调度器", "先判断：隐私 / 延迟 / 成本 / 能力 / 网络", (15, 139, 141, 255))
    draw_label(draw, (1180, 86, 1590, 220), "本地处理", "敏感、简单、毫秒级；优先使用设备 NPU", (35, 122, 87, 255))
    draw_label(draw, (1160, 378, 1580, 512), "边缘节点", "靠近用户；缓存热门能力，降低往返延迟", (18, 56, 114, 255))
    draw_label(draw, (1090, 690, 1572, 834), "云端大模型", "复杂推理、长上下文、企业知识库和多工具调用", (161, 98, 7, 255))
    draw_label(draw, (418, 738, 820, 866), "监控反馈", "记录质量、速度、费用、失败率；下一次路由更聪明", (71, 85, 105, 255))
    workflow.save(ROOT / FIG_WORKFLOW)


def image_data_uri(name: str) -> str:
    data = (ROOT / name).read_bytes()
    return f"data:image/png;base64,{base64.b64encode(data).decode('ascii')}"


def paras(items: list[str]) -> str:
    return "\n".join(f"<p>{escape(item)}</p>" for item in items)


def step_cards() -> str:
    cards: list[str] = []
    for idx, (title, body) in enumerate(MECHANISM, 1):
        cards.append(
            f"""
            <article class="step-card">
              <div class="step-num">{idx}</div>
              <div>
                <h3>{escape(title)}</h3>
                <p>{escape(body)}</p>
              </div>
            </article>
            """
        )
    return "\n".join(cards)


def term_rows() -> str:
    return "\n".join(
        f"<tr><th>{escape(term)}</th><td>{escape(pro)}</td><td>{escape(plain)}</td></tr>"
        for term, pro, plain in TERMS
    )


def mistake_items() -> str:
    return "\n".join(
        f"<li><strong>{escape(title)}</strong><span>{escape(body)}</span></li>"
        for title, body in MISTAKES
    )


def numbered(items: list[str]) -> str:
    return "\n".join(f"<li>{escape(item)}</li>" for item in items)


def source_items() -> str:
    return "\n".join(
        f'<li><a href="{escape(url)}">{escape(title)}</a></li>' for title, url in SOURCES
    )


def build_html() -> str:
    toc = [
        ("why", "为什么重要"),
        ("analogy", "直观类比"),
        ("mechanism", "工作原理"),
        ("terms", "关键术语"),
        ("case", "真实案例"),
        ("mistakes", "常见误区"),
        ("summary", "3句话总结"),
        ("quiz", "复习问题"),
    ]
    toc_html = "\n".join(f'<a href="#{slug}">{label}</a>' for slug, label in toc)
    template = Template(
        """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${date}_${concept_full}</title>
  <style>
    :root {
      --ink: #111827;
      --muted: #475569;
      --quiet: #64748b;
      --line: #d7e0ea;
      --paper: #ffffff;
      --soft: #f8fafc;
      --blue: #123872;
      --teal: #0f8b8d;
      --green: #237a57;
      --amber: #a16207;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: #eef3f8;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      line-height: 1.76;
    }
    .cover {
      min-height: 100vh;
      padding: 58px 26px 42px;
      background: linear-gradient(180deg, #ffffff 0%, #f7fbff 58%, #eefbf7 100%);
      border-bottom: 1px solid var(--line);
    }
    .wrap { max-width: 1080px; margin: 0 auto; }
    .eyebrow {
      color: var(--teal);
      font-size: 15px;
      font-weight: 820;
      letter-spacing: 0;
    }
    h1 {
      max-width: 980px;
      margin: 18px 0 14px;
      color: var(--ink);
      font-size: clamp(42px, 6vw, 74px);
      line-height: 1.08;
      letter-spacing: 0;
    }
    h1 span { color: var(--blue); }
    .subtitle {
      max-width: 920px;
      margin: 0;
      color: var(--muted);
      font-size: clamp(22px, 3vw, 32px);
      line-height: 1.35;
      font-weight: 680;
    }
    .core {
      margin: 38px 0 36px;
      max-width: 920px;
      padding: 22px 24px;
      border-left: 6px solid var(--teal);
      background: rgba(255,255,255,0.82);
      box-shadow: 0 20px 50px rgba(18,56,114,0.08);
      border-radius: 8px;
      font-size: 21px;
      font-weight: 760;
      color: #0f172a;
    }
    .cover-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 14px;
      margin-top: 32px;
      max-width: 940px;
    }
    .metric {
      min-height: 118px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
    }
    .metric b { display: block; color: var(--blue); font-size: 28px; line-height: 1.15; margin-bottom: 8px; }
    .metric span { display: block; color: var(--muted); font-size: 15px; line-height: 1.45; }
    .toc {
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(255,255,255,0.94);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--line);
    }
    .toc .wrap {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 12px 26px;
    }
    .toc a {
      color: var(--blue);
      text-decoration: none;
      font-size: 14px;
      font-weight: 760;
      padding: 7px 10px;
      border-radius: 999px;
      background: #f1f7fb;
      border: 1px solid #d8e8f3;
    }
    main { background: var(--paper); }
    section {
      padding: 62px 26px;
      border-bottom: 1px solid var(--line);
    }
    h2 {
      margin: 0 0 22px;
      color: var(--blue);
      font-size: 34px;
      line-height: 1.22;
      letter-spacing: 0;
    }
    h3 {
      margin: 0 0 8px;
      color: #0f172a;
      font-size: 19px;
      line-height: 1.35;
    }
    p {
      margin: 0 0 16px;
      color: var(--muted);
      font-size: 18px;
    }
    .lead {
      font-size: 21px;
      color: #334155;
      font-weight: 650;
      max-width: 900px;
    }
    figure {
      margin: 34px 0 8px;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
      background: #fff;
      box-shadow: 0 22px 60px rgba(15, 23, 42, 0.10);
      page-break-inside: avoid;
    }
    figure img { display: block; width: 100%; height: auto; }
    figcaption {
      padding: 12px 18px 15px;
      color: var(--quiet);
      font-size: 14px;
      background: #f8fafc;
      border-top: 1px solid var(--line);
    }
    .steps {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 24px;
    }
    .step-card {
      display: grid;
      grid-template-columns: 48px 1fr;
      gap: 14px;
      align-items: start;
      padding: 18px;
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 8px;
      page-break-inside: avoid;
    }
    .step-card p { margin: 0; font-size: 16px; }
    .step-num {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: var(--blue);
      color: #fff;
      font-weight: 850;
      font-size: 18px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 22px;
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
      page-break-inside: avoid;
    }
    th, td {
      padding: 13px 14px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
      text-align: left;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.55;
    }
    th {
      width: 18%;
      color: #0f172a;
      background: #f8fafc;
      font-weight: 850;
    }
    tr:last-child th, tr:last-child td { border-bottom: 0; }
    .mistakes {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      padding: 0;
      margin: 24px 0 0;
      list-style: none;
    }
    .mistakes li {
      padding: 18px;
      background: #fffaf0;
      border: 1px solid #f2d7a4;
      border-radius: 8px;
      page-break-inside: avoid;
    }
    .mistakes strong {
      display: block;
      color: #7c4a03;
      font-size: 17px;
      margin-bottom: 7px;
    }
    .mistakes span {
      display: block;
      color: #5f4938;
      font-size: 15px;
      line-height: 1.6;
    }
    .summary-list, .quiz-list {
      margin: 20px 0 0;
      padding-left: 24px;
    }
    .summary-list li, .quiz-list li {
      margin-bottom: 13px;
      color: var(--muted);
      font-size: 18px;
    }
    .summary-box {
      padding: 24px 26px;
      border-radius: 8px;
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      page-break-inside: avoid;
    }
    .source-list {
      margin: 16px 0 0;
      padding-left: 22px;
    }
    .source-list li { margin-bottom: 8px; color: var(--muted); font-size: 14px; }
    .source-list a { color: var(--blue); text-decoration: none; }
    .note {
      margin-top: 24px;
      padding: 18px 20px;
      border: 1px solid #c7d2fe;
      background: #eef2ff;
      color: #29376c;
      border-radius: 8px;
      font-size: 16px;
    }
    @media print {
      body { background: #fff; }
      .toc { position: static; }
      section { page-break-inside: auto; }
      .cover { min-height: 100vh; }
    }
    @media (max-width: 760px) {
      .cover-grid, .steps, .mistakes { grid-template-columns: 1fr; }
      h1 { font-size: 42px; }
      .subtitle { font-size: 22px; }
      section { padding: 44px 20px; }
      .toc .wrap { padding: 10px 20px; }
    }
  </style>
</head>
<body>
  <header class="cover">
    <div class="wrap">
      <div class="eyebrow">AI 每日深度科普 · ${date}</div>
      <h1><span>端云协同</span><br>为什么 AI 有时在手机上跑，有时要去云端？</h1>
      <p class="subtitle">理解 AI 产品背后的“智能调度”：设备、边缘节点和云端如何一起工作。</p>
      <div class="core">核心一句话：端云协同的本质，是把合适的 AI 任务交给合适的位置：设备负责隐私和即时响应，边缘节点负责就近加速，云端负责强能力和大规模知识。</div>
      <div class="cover-grid">
        <div class="metric"><b>隐私</b><span>越敏感的数据，越应该优先考虑本地或受控环境。</span></div>
        <div class="metric"><b>延迟</b><span>越需要立刻响应，越不能让数据绕远路。</span></div>
        <div class="metric"><b>能力</b><span>越复杂的推理，越可能需要云端大模型。</span></div>
      </div>
    </div>
  </header>
  <nav class="toc"><div class="wrap">${toc_html}</div></nav>
  <main>
    <section id="why">
      <div class="wrap">
        <h2>1. 为什么这个概念重要？</h2>
        <p class="lead">端云协同解释了一个普通用户每天都在经历、但很少被看见的问题：你的 AI 请求到底应该在哪里被处理？</p>
        ${why}
      </div>
    </section>

    <section id="analogy">
      <div class="wrap">
        <h2>2. 一个直观类比：城市外卖调度系统</h2>
        ${analogy}
        <figure>
          <img src="${fig_analogy}" alt="端云协同类比图：用户设备、边缘节点和云端大模型像不同距离和能力的厨房，共同处理AI任务。">
          <figcaption>图1：端云协同不是“全部上云”，而是像外卖系统一样，把不同订单交给不同距离、能力和成本的位置。</figcaption>
        </figure>
      </div>
    </section>

    <section id="mechanism">
      <div class="wrap">
        <h2>3. 工作原理：一次 AI 请求如何被分配？</h2>
        <p class="lead">可以把端云协同理解成一个 AI 交通指挥中心。它不只是问“哪个模型最强”，还要问“这条路是否值得走”。</p>
        <figure>
          <img src="${fig_workflow}" alt="端云协同工作流程图：用户请求进入智能调度器，再被分配到本地处理、边缘节点或云端大模型，并通过监控反馈持续优化。">
          <figcaption>图2：系统先判断任务，再选择本地、边缘或云端；监控反馈会让下一次路由更准确。</figcaption>
        </figure>
        <div class="steps">${steps}</div>
      </div>
    </section>

    <section id="terms">
      <div class="wrap">
        <h2>4. 关键术语解释</h2>
        <p class="lead">这些词看起来像工程术语，其实都在描述一个简单问题：AI 任务在哪里做、怎么做、做得快不快。</p>
        <table>
          <tbody>${terms}</tbody>
        </table>
      </div>
    </section>

    <section id="case">
      <div class="wrap">
        <h2>5. 一个真实应用案例</h2>
        ${case}
        <p class="note">注意：这里讲的是系统设计思想，不是某一家公司的完整实现细节。真实产品会根据隐私政策、硬件能力、模型大小和服务成本做不同取舍。</p>
      </div>
    </section>

    <section id="mistakes">
      <div class="wrap">
        <h2>6. 常见误区</h2>
        <ul class="mistakes">${mistakes}</ul>
      </div>
    </section>

    <section id="summary">
      <div class="wrap">
        <h2>7. 用 3 句话总结</h2>
        <div class="summary-box">
          <ol class="summary-list">${summary}</ol>
        </div>
      </div>
    </section>

    <section id="quiz">
      <div class="wrap">
        <h2>8. 复习问题</h2>
        <ol class="quiz-list">${quiz}</ol>
      </div>
    </section>

    <section id="sources">
      <div class="wrap">
        <h2>参考来源</h2>
        <p>以下资料用于核对端侧、边缘与云端 AI 的现实背景和工程语境。</p>
        <ul class="source-list">${sources}</ul>
      </div>
    </section>
  </main>
</body>
</html>
"""
    )
    return template.substitute(
        date=DATE,
        concept_full=CONCEPT_FULL,
        toc_html=toc_html,
        why=paras(WHY),
        analogy=paras(ANALOGY),
        fig_analogy=image_data_uri(FIG_ANALOGY),
        fig_workflow=image_data_uri(FIG_WORKFLOW),
        steps=step_cards(),
        terms=term_rows(),
        case=paras(CASE),
        mistakes=mistake_items(),
        summary=numbered(SUMMARY),
        quiz=numbered(QUIZ),
        sources=source_items(),
    )


def write_email_files() -> None:
    (ROOT / "email_subject.txt").write_text(
        "【AI每日深度科普】端云协同：为什么 AI 有时在手机上跑，有时要去云端？",
        encoding="utf-8",
    )
    (ROOT / "email_body.txt").write_text(
        """今天的主题是端云协同（Edge-cloud Collaboration）。

它解释了一个普通用户每天都在经历、但很少被看见的问题：
AI 请求到底应该在手机、边缘节点，还是云端大模型里处理？

附件内容将用生活化方式解释：
为什么本地 AI 适合隐私和即时响应；
为什么边缘节点能降低延迟；
为什么复杂任务仍然需要云端大模型；
以及好用的 AI 产品如何在隐私、速度、成本和能力之间做调度。

适合：非技术读者、AI初学者、产品经理、投资研究者和关注 AI 产品体验的人阅读。
""",
        encoding="utf-8",
    )


def main() -> None:
    compose_images()
    html = build_html()
    html_path = ROOT / HTML_NAME
    pdf_path = ROOT / PDF_NAME
    html_path.write_text(html, encoding="utf-8")
    write_email_files()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1800}, device_scale_factor=1)
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "14mm", "right": "13mm", "bottom": "14mm", "left": "13mm"},
        )
        page.screenshot(path=str(ROOT / "html_preview.png"), full_page=True)
        browser.close()
    print(f"Wrote {html_path}")
    print(f"Wrote {pdf_path}")


if __name__ == "__main__":
    main()
