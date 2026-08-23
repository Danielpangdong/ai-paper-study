from __future__ import annotations

import base64
from pathlib import Path
from textwrap import dedent

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "AI-Daily-Paper-Sumi-2026-06-23-embedded.html"
EMAIL_BODY = ROOT / "email-body.html"
EMAIL_SUBJECT = ROOT / "email_subject.txt"
SOURCES = ROOT / "sources.md"
HERO = ROOT / "sumi-hero.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size, index=1 if bold else 0)
        except Exception:
            continue
    return ImageFont.load_default()


def make_hero() -> None:
    width, height = 1600, 900
    img = Image.new("RGB", (width, height), "#0f1718")
    draw = ImageDraw.Draw(img)

    for y in range(height):
        shade = int(18 + 28 * (y / height))
        draw.line([(0, y), (width, y)], fill=(shade, shade + 8, shade + 9))

    # Ink wash circles.
    for i, (cx, cy, r, color) in enumerate(
        [
            (1170, 260, 260, (26, 93, 99)),
            (1320, 630, 310, (98, 91, 55)),
            (920, 700, 240, (55, 105, 87)),
        ]
    ):
        for k in range(r, 0, -6):
            alpha = k / r
            fill = tuple(int(c * alpha + 15 * (1 - alpha)) for c in color)
            draw.ellipse((cx - k, cy - k, cx + k, cy + k), outline=fill, width=3)

    title_f = font(66, True)
    sub_f = font(30)
    label_f = font(26, True)
    small_f = font(21)
    draw.text((86, 96), "Sumi", fill="#f4f0e8", font=title_f)
    draw.text((90, 176), "开放 Uniform Diffusion 语言模型", fill="#bfd8d4", font=sub_f)
    draw.text((90, 228), "不是从左到右写字，而是在整张画布上反复把噪声擦成答案。", fill="#d7ddd8", font=small_f)

    x0, y0 = 105, 360
    token_w, token_h = 98, 62
    words = ["随", "机", "噪", "声", "?", "?", "?", "?"]
    final = ["问", "题", "→", "草", "稿", "→", "修", "正"]
    for row, items in enumerate([words, final]):
        y = y0 + row * 118
        for col, item in enumerate(items):
            x = x0 + col * (token_w + 14)
            fill = "#263537" if row == 0 else "#eaf1ed"
            outline = "#415759" if row == 0 else "#93b7ad"
            text_fill = "#c6d0cb" if row == 0 else "#173438"
            draw.rounded_rectangle((x, y, x + token_w, y + token_h), radius=10, fill=fill, outline=outline, width=2)
            tw = draw.textlength(item, font=label_f)
            draw.text((x + (token_w - tw) / 2, y + 16), item, fill=text_fill, font=label_f)
    draw.text((105, y0 - 52), "传统 AR：像排队打字", fill="#f0c66e", font=label_f)
    draw.text((105, y0 + 184), "Sumi：像修一整张草稿", fill="#9ed7cb", font=label_f)

    # Directional arrows.
    for y in (y0 + 31, y0 + 149):
        draw.line((950, y, 1190, y), fill="#d8c17a", width=4)
        draw.polygon([(1190, y), (1166, y - 13), (1166, y + 13)], fill="#d8c17a")
    draw.rounded_rectangle((1220, 322, 1480, 600), radius=22, fill="#f4f0e8", outline="#9fb8ad", width=3)
    draw.text((1262, 368), "7B", fill="#173438", font=font(58, True))
    draw.text((1260, 448), "1.5T tokens", fill="#173438", font=font(36, True))
    draw.text((1260, 512), "Apache 2.0", fill="#557069", font=font(28))

    HERO.parent.mkdir(parents=True, exist_ok=True)
    img.save(HERO, format="PNG", optimize=True)


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


make_hero()
hero_data = b64(HERO)

subject = "【AI每日论文精选】如果AI不再一个字一个字地写答案？"

email_body = """<!doctype html><html lang="zh-CN"><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',Arial,sans-serif;line-height:1.7;color:#162022">
<p>今天精选的论文是 <b>Sumi: Open Uniform Diffusion Language Model from Scratch</b>。</p>
<p>一句话推荐理由：它把“文本生成必须从左到右一个词一个词吐出来”这件事重新打开，提供了第一个从头训练到 7B / 1.5T token 规模的开放 Uniform Diffusion 语言模型。</p>
<p>这可能成为研究下一代低延迟、可控、可并行文本生成路线的重要参照物。附件为中文深度拆解 HTML 报告，适合非技术读者阅读。</p>
</body></html>
"""

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI每日论文精选｜Sumi：如果AI不再一个字一个字地写答案？</title>
<style>
  :root {{
    color-scheme: light dark;
    --ink:#172124; --muted:#607074; --paper:#f5f4ef; --panel:#fffdf8;
    --line:#d9ded8; --green:#23685f; --blue:#2b5f7b; --gold:#aa7b2f;
    --rose:#8b4b55; --dark:#101819; --soft:#eaf1ed;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC","PingFang SC",Arial,sans-serif; background:var(--paper); color:var(--ink); line-height:1.72; letter-spacing:0; }}
  a {{ color:var(--green); text-decoration:none; }}
  .hero {{ position:relative; min-height:560px; color:white; overflow:hidden; background:#101819; }}
  .hero img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.78; }}
  .hero:after {{ content:""; position:absolute; inset:0; background:linear-gradient(90deg,rgba(12,18,19,.92),rgba(12,18,19,.66) 47%,rgba(12,18,19,.12)); }}
  .hero-inner,.wrap {{ max-width:980px; margin:0 auto; padding-left:18px; padding-right:18px; }}
  .hero-inner {{ position:relative; z-index:1; padding-top:74px; padding-bottom:64px; }}
  .eyebrow {{ display:inline-block; padding:6px 10px; border:1px solid rgba(255,255,255,.28); border-radius:999px; background:rgba(255,255,255,.08); color:#dcebe8; font-size:13px; }}
  h1 {{ margin:22px 0 18px; max-width:780px; font-size:42px; line-height:1.13; letter-spacing:0; }}
  .subtitle {{ max-width:730px; color:#dce5df; font-size:19px; }}
  .hero-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; max-width:780px; margin-top:30px; }}
  .metric {{ padding:14px; border:1px solid rgba(255,255,255,.22); border-radius:8px; background:rgba(255,255,255,.08); }}
  .metric b {{ display:block; font-size:22px; color:white; }}
  .metric span {{ display:block; font-size:12px; color:#c6d6d1; }}
  .wrap {{ padding-bottom:58px; }}
  section {{ margin-top:34px; }}
  h2 {{ margin:0 0 14px; font-size:25px; line-height:1.25; }}
  h3 {{ margin:0 0 9px; font-size:18px; line-height:1.35; }}
  p {{ margin:0 0 14px; }}
  .card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:20px; box-shadow:0 12px 28px rgba(34,44,38,.05); }}
  .grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
  .grid-3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }}
  table {{ width:100%; border-collapse:collapse; background:var(--panel); border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
  th,td {{ padding:12px 13px; border-bottom:1px solid var(--line); vertical-align:top; text-align:left; }}
  th {{ background:#e8f0ed; color:#263334; font-weight:750; }}
  tr:last-child td {{ border-bottom:0; }}
  .tag {{ display:inline-block; margin:0 6px 6px 0; padding:4px 9px; border-radius:999px; background:var(--soft); color:#24524f; font-size:12px; font-weight:750; }}
  .quote {{ border-left:4px solid var(--green); background:#eef6f3; padding:16px 18px; border-radius:0 8px 8px 0; font-size:20px; font-weight:800; }}
  .diagram {{ width:100%; height:auto; display:block; background:#111b1d; border-radius:8px; border:1px solid #243437; }}
  .note {{ color:var(--muted); font-size:14px; }}
  .warn {{ border-left:4px solid var(--gold); }}
  .source-list li {{ margin-bottom:8px; }}
  .footer {{ margin-top:42px; color:var(--muted); font-size:13px; }}
  @media (max-width:720px) {{
    .hero {{ min-height:640px; }}
    h1 {{ font-size:31px; }}
    .subtitle {{ font-size:17px; }}
    .hero-grid,.grid-2,.grid-3 {{ grid-template-columns:1fr; }}
    th,td {{ display:block; width:100%; }}
    tr {{ display:block; border-bottom:1px solid var(--line); }}
    tr:last-child {{ border-bottom:0; }}
    th {{ border-bottom:0; }}
  }}
</style>
</head>
<body>
<header class="hero">
  <img src="data:image/png;base64,{hero_data}" alt="Sumi uniform diffusion language model visual">
  <div class="hero-inner">
    <span class="eyebrow">AI每日论文精选 · 2026-06-23</span>
    <h1>Sumi：如果 AI 不再一个字一个字地写答案？</h1>
    <p class="subtitle">今天这篇论文重要，不是因为它马上打败 GPT 系列，而是因为它给了研究社区一个开放参照物：语言模型能否像修一整张草稿一样生成文本，而不是永远从左到右排队吐字。</p>
    <div class="hero-grid">
      <div class="metric"><b>7B</b><span>Uniform Diffusion LM</span></div>
      <div class="metric"><b>1.5T</b><span>从头训练 token 数</span></div>
      <div class="metric"><b>43,308</b><span>GPU-hours</span></div>
      <div class="metric"><b>Apache 2.0</b><span>权重与代码开放</span></div>
    </div>
  </div>
</header>

<main class="wrap">
  <section>
    <h2>1. 论文基本信息</h2>
    <table>
      <tr><th>论文</th><td><b>Sumi: Open Uniform Diffusion Language Model from Scratch</b><br>中文可译：Sumi：从头训练的开放 Uniform Diffusion 语言模型</td></tr>
      <tr><th>作者</th><td>Mengyu Ye, Keito Kudo, Wataru Ikeda, Ryosuke Matsuda, Keisuke Sakaguchi, Jun Suzuki</td></tr>
      <tr><th>机构</th><td>Tohoku University</td></tr>
      <tr><th>发布时间</th><td>arXiv 提交：2026-06-17；平台：arXiv / Hugging Face / GitHub / 项目页</td></tr>
      <tr><th>链接</th><td><a href="https://arxiv.org/abs/2606.19005">arXiv</a> · <a href="https://arxiv.org/html/2606.19005v1">论文 HTML</a> · <a href="https://huggingface.co/tohoku-nlp/sumi-7b">Hugging Face 模型卡</a> · <a href="https://github.com/tohoku-nlp/sumi">GitHub</a> · <a href="https://www.nlp.ecei.tohoku.ac.jp/projects/sumi/">项目页</a></td></tr>
    </table>
  </section>

  <section>
    <h2>2. 为什么今天选它？</h2>
    <div class="grid-2">
      <div class="card">
        <h3>它挑战了文本生成的默认路线</h3>
        <p>过去的大语言模型大多像打字员：先写第一个词，再写第二个词，前面的词一旦写下，后面只能接着补。Sumi 走的是另一条路：先放一整块“带噪声的画布”，再一轮轮把不确定的位置修正成文字。</p>
      </div>
      <div class="card">
        <h3>它是开放参照物，而不是封闭演示</h3>
        <p>论文释放模型权重、检查点、训练配方和公开语料混合说明。对研究者来说，这就像拿到一台可拆开的发动机，而不是只看到一辆跑得很快的样车。</p>
      </div>
    </div>
    <div class="card" style="margin-top:14px">
      <span class="tag">新生成范式</span><span class="tag">开源基础模型</span><span class="tag">并行解码</span><span class="tag">可控生成</span>
      <p>长期看，如果 diffusion language model 继续进步，它可能影响低延迟生成、可编辑写作、代码补全、结构化输出和多轮推理。今天的 Sumi 还不是终点，但它把一条以前难以系统研究的路线，第一次推到了现代大模型规模。</p>
    </div>
  </section>

  <section>
    <h2>3. 一句话讲透论文</h2>
    <div class="quote">Sumi 本质上是在让 AI 像修改一整张草稿一样写作：先铺开整页，再反复擦掉噪声、填上更确定的词。</div>
  </section>

  <section>
    <h2>4. 核心贡献拆解</h2>
    <div class="grid-3">
      <div class="card"><h3>从头训练 UDLM</h3><p>它不是把现有自回归模型改造成 diffusion 模型，而是原生从头训练一个 7B uniform diffusion language model。</p></div>
      <div class="card"><h3>开放完整研究材料</h3><p>权重、检查点、训练配方、数据混合和评测代码都开放，便于复现和横向比较。</p></div>
      <div class="card"><h3>给出早期行为探针</h3><p>论文分析了画布长度、采样策略、并行提交 token、自我修正等行为，为后续研究提供问题清单。</p></div>
    </div>
  </section>

  <section>
    <h2>5. 工作原理：从“打字机”到“整页修稿”</h2>
    <div class="card">
      <svg class="diagram" viewBox="0 0 980 360" role="img" aria-label="Sumi generation workflow">
        <defs>
          <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#d4b15f"/></marker>
        </defs>
        <rect x="0" y="0" width="980" height="360" fill="#111b1d"/>
        <text x="42" y="48" fill="#f2eee6" font-size="26" font-weight="700">两种写作方式</text>
        <text x="58" y="94" fill="#9ed7cb" font-size="18">Autoregressive：排队写字</text>
        <text x="530" y="94" fill="#9ed7cb" font-size="18">Sumi：整页去噪</text>
        <g fill="#263638" stroke="#607d78" stroke-width="2">
          <rect x="58" y="128" width="52" height="48" rx="6"/><rect x="122" y="128" width="52" height="48" rx="6"/><rect x="186" y="128" width="52" height="48" rx="6"/><rect x="250" y="128" width="52" height="48" rx="6"/><rect x="314" y="128" width="52" height="48" rx="6"/>
        </g>
        <text x="74" y="160" fill="#dce5df" font-size="22">我</text><text x="138" y="160" fill="#dce5df" font-size="22">要</text><text x="202" y="160" fill="#dce5df" font-size="22">去</text><text x="266" y="160" fill="#dce5df" font-size="22">...</text><text x="330" y="160" fill="#dce5df" font-size="22">?</text>
        <line x1="390" y1="152" x2="478" y2="152" stroke="#d4b15f" stroke-width="4" marker-end="url(#arrow)"/>
        <text x="60" y="230" fill="#c3d2ce" font-size="17">前一个词会锁住后一个词，天然顺序强。</text>
        <g>
          <rect x="530" y="120" width="360" height="70" rx="10" fill="#243234" stroke="#607d78"/>
          <text x="556" y="164" fill="#ccd8d2" font-size="24">噪 声 ? ? 词 ? ? 草 稿</text>
          <line x1="710" y1="205" x2="710" y2="252" stroke="#d4b15f" stroke-width="4" marker-end="url(#arrow)"/>
          <rect x="530" y="268" width="360" height="50" rx="10" fill="#eaf1ed" stroke="#9ed7cb"/>
          <text x="556" y="301" fill="#173438" font-size="23">问题 → 草稿 → 修正 → 答案</text>
        </g>
        <text x="530" y="230" fill="#c3d2ce" font-size="17">任意位置都可被更新；采样器决定先修哪里。</text>
      </svg>
      <p class="note">白话理解：传统模型像接龙，Sumi 更像 Photoshop 的“反复降噪”。这让它理论上更适合并行生成和后期修正，但论文也说明：这些潜力目前还没有完全兑现。</p>
    </div>
  </section>

  <section>
    <h2>6. 关键术语解释</h2>
    <table>
      <tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr>
      <tr><td>Autoregressive / AR</td><td>按条件概率逐 token 从左到右生成。</td><td>像一个只能往后写、不能回头改的打字员。</td></tr>
      <tr><td>Uniform Diffusion LM</td><td>用离散 diffusion 过程在任意 token 位置去噪和更新。</td><td>像先把整页打乱，再一轮轮把模糊处擦清楚。</td></tr>
      <tr><td>Canvas length</td><td>模型生成时使用的固定 token 画布长度。</td><td>给 AI 的纸张大小。纸太短或太长，Sumi 目前都会不稳定。</td></tr>
      <tr><td>Adaptive sampler</td><td>根据模型置信度选择要提交/更新的位置。</td><td>先填自己最有把握的空，再处理难的空。</td></tr>
      <tr><td>ELBO / NELBO</td><td>diffusion 模型常用的似然训练与评测目标。</td><td>衡量“把噪声还原成正确文本”这件事做得有多好。</td></tr>
    </table>
  </section>

  <section>
    <h2>7. 实验结果怎么读？</h2>
    <table>
      <tr><th>指标</th><th>Sumi-7B</th><th>可比 AR 基线</th><th>怎么理解</th></tr>
      <tr><td>MMLU</td><td><b>51.1</b></td><td>Falcon 27.2 / Llama 2 46.0 / OLMo 28.0</td><td>知识类任务上，在同协议的开放 7B 级模型里表现强。</td></tr>
      <tr><td>GSM8K</td><td><b>32.8</b></td><td>Falcon 5.3 / Llama 2 13.5 / OLMo 3.8</td><td>数学推理明显好于旧 7B 基线，但远未到最强 reasoning model 水平。</td></tr>
      <tr><td>HumanEval</td><td><b>22.6</b></td><td>Falcon 0.0 / Llama 2 12.8 / OLMo 13.4</td><td>代码任务有亮点，可能受代码与教育数据混合影响。</td></tr>
      <tr><td>PIQA / HellaSwag</td><td>66.4 / 60.0</td><td>Falcon 80.5 / 76.3；Llama 2 78.7 / 76.2</td><td>常识题明显短板，说明这条路线还没有“全科强”。</td></tr>
    </table>
    <div class="card" style="margin-top:14px">
      <p>最值得读的结果不是“它赢了谁”，而是：在 7B、1.5T token、完全开放材料的前提下，Uniform Diffusion 已经能在知识、数学、代码上接近或超过若干同量级 AR 基线。换句话说，这条路不再只是玩具实验。</p>
    </div>
  </section>

  <section>
    <h2>8. 局限性与问题</h2>
    <div class="grid-2">
      <div class="card warn"><h3>目前不是可直接部署的聊天模型</h3><p>模型卡和论文都说明它是 pretrained base model，没有指令微调、对齐或安全过滤；真实产品不能直接拿来替代 ChatGPT。</p></div>
      <div class="card warn"><h3>“会回头改”还没真正发生</h3><p>理论上 diffusion 可以修改已提交 token，但论文实验显示，额外去噪大多只是来回覆盖，最终答案几乎不变。</p></div>
      <div class="card warn"><h3>画布长度敏感</h3><p>2048 token 是评测中的稳定区间；太短或过长时，部分任务会明显退化。</p></div>
      <div class="card warn"><h3>常识能力偏弱</h3><p>作者认为教育/代码偏重的数据混合可能解释一部分，但也明确说不能完全归因于数据。</p></div>
    </div>
  </section>

  <section>
    <h2>9. 产业影响分析</h2>
    <div class="grid-3">
      <div class="card"><h3>谁会受益</h3><p>基础模型研究者、推理系统工程师、开源模型社区、需要可控生成的应用团队。</p></div>
      <div class="card"><h3>谁会被冲击</h3><p>短期不会冲击闭源大模型产品；长期会给“AR 是唯一可行路线”的默认判断带来压力。</p></div>
      <div class="card"><h3>可能改变什么</h3><p>如果并行解码和可编辑生成被做实，未来模型服务的延迟、成本和交互方式都可能变化。</p></div>
    </div>
  </section>

  <section>
    <h2>10. 延伸阅读</h2>
    <ul class="source-list">
      <li><a href="https://arxiv.org/abs/2606.19005">Sumi arXiv 摘要页</a></li>
      <li><a href="https://arxiv.org/html/2606.19005v1">Sumi arXiv HTML 全文</a></li>
      <li><a href="https://huggingface.co/tohoku-nlp/sumi-7b">Sumi-7B Hugging Face 模型卡</a></li>
      <li><a href="https://github.com/tohoku-nlp/sumi">Sumi GitHub 仓库</a></li>
      <li><a href="https://huggingface.co/papers/2606.19005">Hugging Face Papers 讨论页</a></li>
      <li><a href="https://arxiv.org/abs/2502.09992">LLaDA：Masked Diffusion 语言模型相关路线</a></li>
      <li><a href="https://deepmind.google/discover/blog/diffusiongemma/">DiffusionGemma：从 AR 模型适配到 diffusion 的相关路线</a></li>
    </ul>
  </section>

  <section>
    <h2>11. 引用来源</h2>
    <table>
      <tr><th>来源</th><th>用于确认</th></tr>
      <tr><td>arXiv 摘要与 HTML/PDF</td><td>标题、作者、机构、提交日期、训练规模、实验结果、局限性。</td></tr>
      <tr><td>Hugging Face 模型卡</td><td>Apache 2.0、模型使用方式、trust_remote_code、生成参数、模型大小。</td></tr>
      <tr><td>GitHub README</td><td>评测工具、lm-eval 插件、canvas_length=2048、adaptive sampler、推理说明。</td></tr>
      <tr><td>Hugging Face Papers / Papers with Code</td><td>社区收录和第三方索引信号。</td></tr>
    </table>
    <p class="footer">本报告为中文解释性重构，不是论文逐字翻译。所有关键数字均来自英文原始来源交叉确认。</p>
  </section>
</main>
</body>
</html>
"""

sources = dedent(
    """\
    # Sources

    - arXiv abstract: https://arxiv.org/abs/2606.19005
    - arXiv HTML: https://arxiv.org/html/2606.19005v1
    - arXiv PDF/source downloaded under `sources/`.
    - Hugging Face model card: https://huggingface.co/tohoku-nlp/sumi-7b
    - Hugging Face Papers: https://huggingface.co/papers/2606.19005
    - GitHub repository: https://github.com/tohoku-nlp/sumi
    - Project page: https://www.nlp.ecei.tohoku.ac.jp/projects/sumi/
    - Papers with Code: https://paperswithcode.co/paper/2606.19005

    Key checked facts:
    - arXiv: submitted 2026-06-17, arXiv:2606.19005, cs.CL/cs.LG.
    - Model: 7B native uniform diffusion language model, pretrained from scratch on 1.5T tokens.
    - Compute: 288 NVIDIA H100 GPUs; 43,308 GPU-hours total.
    - Release: model weights, checkpoints, full training recipe, data mixture; Apache 2.0 model card.
    - Main table values confirmed from arXiv TeX source `tables/table1.tex`.
    """
)

REPORT.write_text(html, encoding="utf-8")
EMAIL_BODY.write_text(email_body, encoding="utf-8")
EMAIL_SUBJECT.write_text(subject + "\n", encoding="utf-8")
SOURCES.write_text(sources, encoding="utf-8")

print(REPORT)
print(EMAIL_BODY)
print(HERO)
