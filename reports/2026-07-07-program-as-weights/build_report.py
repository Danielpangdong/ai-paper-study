from base64 import b64encode
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
HTML = OUT_DIR / "AI-Daily-Paper-Program-as-Weights-2026-07-07.html"
SUBJECT = OUT_DIR / "email_subject.txt"
BODY = OUT_DIR / "email_body.txt"
SOURCES = OUT_DIR / "sources.md"
HERO = OUT_DIR / "paw-hero.png"


hero_data = b64encode(HERO.read_bytes()).decode("ascii")

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI每日论文精选｜当大模型从“答题机器”变成“工具编译器”</title>
  <style>
    :root {{
      color-scheme: light dark;
      --ink: #142033;
      --muted: #5f6c7d;
      --paper: #f6f8fb;
      --panel: #ffffff;
      --line: #d9e1ec;
      --blue: #235fc6;
      --cyan: #087f8c;
      --green: #0f8a5f;
      --red: #ba3f35;
      --gold: #a66b00;
      --violet: #5b4abf;
      --soft-blue: #eef5ff;
      --soft-green: #effaf5;
      --soft-red: #fff2f0;
      --soft-gold: #fff7e6;
      --soft-violet: #f3f0ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
      background: var(--paper);
      color: var(--ink);
      line-height: 1.72;
    }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .wrap {{ max-width: 1080px; margin: 0 auto; padding: 28px 18px 56px; }}
    .hero {{
      display: grid;
      grid-template-columns: 1.05fr .95fr;
      gap: 24px;
      align-items: center;
      padding: 32px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: linear-gradient(180deg, #ffffff 0%, #f0f5fb 100%);
    }}
    .hero-img {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      display: block;
      background: #fff;
    }}
    .eyebrow {{
      color: var(--blue);
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0;
      margin-bottom: 14px;
    }}
    h1 {{
      margin: 0;
      font-size: 40px;
      line-height: 1.14;
      letter-spacing: 0;
    }}
    .subtitle {{ margin: 16px 0 0; color: var(--muted); font-size: 17px; }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin-top: 18px;
    }}
    .meta, .card, .term {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }}
    .meta {{ padding: 12px; }}
    .meta b {{ display: block; color: var(--muted); font-size: 12px; margin-bottom: 3px; }}
    .meta span {{ display: block; font-weight: 780; font-size: 14px; }}
    section {{ margin-top: 22px; }}
    .section {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 24px;
    }}
    h2 {{ margin: 0 0 14px; font-size: 25px; line-height: 1.22; letter-spacing: 0; }}
    h3 {{ margin: 18px 0 8px; font-size: 18px; letter-spacing: 0; }}
    p {{ margin: 9px 0; }}
    .lead {{ font-size: 18px; color: #26364e; }}
    .one-line {{
      margin: 14px 0 0;
      padding: 17px;
      border-left: 4px solid var(--blue);
      background: var(--soft-blue);
      border-radius: 8px;
      font-size: 20px;
      font-weight: 850;
    }}
    .cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 14px; }}
    .card {{ padding: 15px; }}
    .card b {{ display: block; margin-bottom: 6px; }}
    .kpi {{ font-size: 34px; line-height: 1; font-weight: 850; color: var(--blue); margin: 8px 0 4px; }}
    .tag {{
      display: inline-flex;
      min-height: 24px;
      align-items: center;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f8fafc;
      color: #31435d;
      font-size: 12px;
      font-weight: 760;
    }}
    .tag.red {{ color: var(--red); background: var(--soft-red); }}
    .tag.green {{ color: var(--green); background: var(--soft-green); }}
    .tag.gold {{ color: var(--gold); background: var(--soft-gold); }}
    .tag.violet {{ color: var(--violet); background: var(--soft-violet); }}
    .note {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px 16px;
      margin-top: 12px;
      background: #fbfdff;
    }}
    .why {{ background: var(--soft-green); border-color: #cce8db; }}
    .risk {{ background: var(--soft-red); border-color: #f0c8c3; }}
    .gold {{ background: var(--soft-gold); border-color: #ecd5a8; }}
    .table-wrap {{ overflow-x: auto; margin-top: 14px; border: 1px solid var(--line); border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 760px; background: #fff; }}
    th, td {{ padding: 12px 14px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ background: #f2f6fb; color: var(--muted); font-size: 13px; }}
    tr:last-child td {{ border-bottom: 0; }}
    .diagram {{
      margin-top: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdff;
      overflow: hidden;
    }}
    .diagram svg {{ display: block; width: 100%; height: auto; }}
    .terms {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
    .term {{ padding: 14px; }}
    .term strong {{ color: var(--blue); }}
    .bars {{ margin-top: 12px; }}
    .bar-row {{ display: grid; grid-template-columns: 170px 1fr 78px; gap: 10px; align-items: center; margin: 10px 0; font-size: 14px; }}
    .track {{ height: 14px; border-radius: 999px; background: #e7edf5; overflow: hidden; }}
    .bar {{ height: 100%; border-radius: 999px; background: var(--blue); }}
    .bar.red {{ background: var(--red); }}
    .bar.green {{ background: var(--green); }}
    .bar.gold {{ background: var(--gold); }}
    .bar.violet {{ background: var(--violet); }}
    ul {{ padding-left: 20px; margin: 10px 0; }}
    li {{ margin: 6px 0; }}
    .footer {{ color: var(--muted); font-size: 13px; margin-top: 18px; }}
    @media (max-width: 840px) {{
      .wrap {{ padding: 14px 12px 36px; }}
      .hero {{ grid-template-columns: 1fr; padding: 22px; }}
      h1 {{ font-size: 31px; }}
      .subtitle, .lead {{ font-size: 16px; }}
      .meta-grid, .cards, .terms {{ grid-template-columns: 1fr; }}
      .section {{ padding: 18px; }}
      h2 {{ font-size: 22px; }}
      .bar-row {{ grid-template-columns: 120px 1fr 54px; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <header class="hero">
      <div>
        <div class="eyebrow">AI每日论文精选 · 2026-07-07</div>
        <h1>当大模型从“答题机器”变成“工具编译器”</h1>
        <p class="subtitle">今日精选论文：<i>Program-as-Weights: A Programming Paradigm for Fuzzy Functions</i>。它提出一个很有启发性的方向：不要每次都把模糊任务丢给远程大模型，而是先让大模型把任务“编译”成一个小权重文件，之后像普通函数一样在本地反复调用。</p>
        <div class="meta-grid">
          <div class="meta"><b>论文</b><span>Program-as-Weights</span></div>
          <div class="meta"><b>作者</b><span>Wentao Zhang, Liliana Hotsko, Woojeong Kim, Pengyu Nie, Stuart Shieber, Yuntian Deng</span></div>
          <div class="meta"><b>机构</b><span>University of Waterloo, Cornell University, Harvard University</span></div>
          <div class="meta"><b>平台</b><span>arXiv · 2026-07-02 · cs.LG</span></div>
        </div>
      </div>
      <img class="hero-img" alt="Program-as-Weights：云端编译器生成本地神经程序" src="data:image/png;base64,{hero_data}">
    </header>

    <section class="section">
      <h2>1. 标题区</h2>
      <div class="table-wrap">
        <table>
          <tr><th>项目</th><th>内容</th></tr>
          <tr><td>英文标题</td><td><i>Program-as-Weights: A Programming Paradigm for Fuzzy Functions</i></td></tr>
          <tr><td>中文译名</td><td>权重即程序：面向模糊函数的新编程范式</td></tr>
          <tr><td>作者</td><td>Wentao Zhang, Liliana Hotsko, Woojeong Kim, Pengyu Nie, Stuart Shieber, Yuntian Deng</td></tr>
          <tr><td>机构</td><td>University of Waterloo, Cornell University, Harvard University</td></tr>
          <tr><td>发布时间</td><td>2026-07-02</td></tr>
          <tr><td>会议/平台</td><td>arXiv:2607.02512，Computer Science - Machine Learning</td></tr>
          <tr><td>链接</td><td><a href="https://arxiv.org/abs/2607.02512">arXiv 摘要</a> · <a href="https://arxiv.org/html/2607.02512v1">arXiv HTML</a> · <a href="https://github.com/programasweights">GitHub</a> · <a href="https://programasweights.com">Demo 网站</a></td></tr>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>2. 为什么今天选它？</h2>
      <p class="lead">因为它不是在问“模型能不能再大一点”，而是在问一个更贴近真实产品的问题：很多业务里需要的 AI 功能，其实只是一个会处理模糊输入的小函数，为什么每次都要远程调用一台昂贵的大模型？</p>
      <div class="cards">
        <div class="card"><span class="tag green">工程范式</span><div class="kpi">编译一次</div><p>把自然语言需求变成小型神经程序，之后本地反复调用。</p></div>
        <div class="card"><span class="tag gold">成本变化</span><div class="kpi">约 50x</div><p>论文报告 0.6B 解释器推理内存约为 Qwen3-32B prompting 的五十分之一。</p></div>
        <div class="card"><span class="tag violet">长期价值</span><div class="kpi">小模型运行时</div><p>大模型负责“造工具”，小模型负责日常执行，这可能影响端侧 AI 与企业私有化部署。</p></div>
      </div>
      <div class="note why"><b>我的判断：</b>PAW 的重要性不在于今天已经能替代所有 LLM API，而在于它提出了一条清晰路线：把高频、重复、模糊但边界清楚的 AI 能力，从“每次问大模型”变成“先编译成可版本管理的本地函数”。这会影响 AI 工程成本、隐私、可复现性和软件交付形态。</div>
    </section>

    <section class="section">
      <h2>3. 一句话讲透论文</h2>
      <div class="one-line">这篇论文本质上是在让大模型像“工具工厂”：先把一句模糊需求铸造成一个小插件，之后普通电脑就能离线反复使用它。</div>
      <p>可以把它想成手机上的离线翻译包。你不需要每句话都发到云端重新请专家翻译，而是先下载一个适合任务的小包，之后在本地快速运行。PAW 想把这种思路推广到日志筛选、JSON 修复、搜索重排、工具路由、文本分类等“规则写不完、但大模型又太贵”的场景。</p>
    </section>

    <section class="section">
      <h2>4. 核心贡献拆解</h2>
      <div class="table-wrap">
        <table>
          <tr><th>贡献</th><th>它解决什么问题</th><th>为什么比旧方法更好</th></tr>
          <tr><td>提出 fuzzy-function programming</td><td>很多函数无法用 if/else 或正则稳定表达，比如“这条日志是否重要”。</td><td>把模糊任务当成软件函数管理，而不是当成一次性聊天请求。</td></tr>
          <tr><td>Program-as-Weights</td><td>每个任务被编译成一个 LoRA/PEFT 小权重文件。</td><td>可以缓存、版本化、离线执行，类似一个 Python 模块。</td></tr>
          <tr><td>Compiler-Interpreter 架构</td><td>大模型每次执行太贵，小模型理解任务又不够强。</td><td>4B 编译器读懂需求，0.6B 解释器负责本地运行。</td></tr>
          <tr><td>FuzzyBench-10M</td><td>缺少“从规格编译模糊函数”的训练数据。</td><td>论文构建 1000 万样例，覆盖 29 个版本、800+ 子类别。</td></tr>
          <tr><td>本地执行接口</td><td>研究原型经常离开发者太远。</td><td>论文展示 `paw.compile()` 与 `paw.function()` 形态，强调可作为软件构件使用。</td></tr>
        </table>
      </div>
      <div class="note gold"><b>关键区别：</b>传统 LLM API 像“每个订单都请专家现场判断”；PAW 像“请专家先写一本岗位手册，再交给本地员工执行”。专家仍然重要，但调用频率从“每个输入一次”变成“每个函数一次”。</div>
    </section>

    <section class="section">
      <h2>5. 工作原理（深入浅出）</h2>
      <p>PAW 的流程像一家工厂：需求部门写一句话，资深工程师先把需求整理成清楚的操作说明，再由模型编译器把它压缩成一个小权重包，最后本地小模型加载这个权重包来处理真实输入。</p>
      <div class="diagram" aria-label="PAW 编译执行流程图">
        <svg viewBox="0 0 880 470" role="img">
          <rect width="880" height="470" fill="#fbfdff"/>
          <text x="36" y="46" font-size="25" font-weight="800" fill="#142033">Program-as-Weights：从“问模型”到“造函数”</text>
          <text x="36" y="76" font-size="15" fill="#5f6c7d">云端负责编译，本地负责执行；大模型从解题者变成工具制造者</text>
          <g transform="translate(45 120)">
            <rect x="0" y="0" width="180" height="90" rx="8" fill="#eef5ff" stroke="#c9d9f3"/>
            <text x="18" y="31" font-size="16" font-weight="800" fill="#235fc6">自然语言规格</text>
            <text x="18" y="58" font-size="13" fill="#142033">“判断邮件是否需要</text>
            <text x="18" y="78" font-size="13" fill="#142033">马上处理”</text>
          </g>
          <path d="M235 165 H310" stroke="#8fa6c6" stroke-width="3" marker-end="url(#arrow)"/>
          <g transform="translate(320 120)">
            <rect x="0" y="0" width="180" height="90" rx="8" fill="#fff7e6" stroke="#ecd5a8"/>
            <text x="18" y="31" font-size="16" font-weight="800" fill="#a66b00">伪程序清洗</text>
            <text x="18" y="58" font-size="13" fill="#142033">改写需求 + 生成</text>
            <text x="18" y="78" font-size="13" fill="#142033">代表性例子</text>
          </g>
          <path d="M510 165 H585" stroke="#8fa6c6" stroke-width="3" marker-end="url(#arrow)"/>
          <g transform="translate(595 120)">
            <rect x="0" y="0" width="220" height="90" rx="8" fill="#f3f0ff" stroke="#d7d0f5"/>
            <text x="18" y="31" font-size="16" font-weight="800" fill="#5b4abf">Text-to-LoRA 编译器</text>
            <text x="18" y="58" font-size="13" fill="#142033">输出一个约 23MB 的</text>
            <text x="18" y="78" font-size="13" fill="#142033">任务专用权重适配器</text>
          </g>
          <g transform="translate(220 275)">
            <rect x="0" y="0" width="190" height="92" rx="8" fill="#effaf5" stroke="#cce8db"/>
            <text x="18" y="32" font-size="16" font-weight="800" fill="#0f8a5f">本地解释器</text>
            <text x="18" y="59" font-size="13" fill="#142033">冻结的 0.6B 小模型</text>
            <text x="18" y="79" font-size="13" fill="#142033">加载共享基础模型</text>
          </g>
          <path d="M705 220 C705 260 640 310 420 320" fill="none" stroke="#8fa6c6" stroke-width="3" marker-end="url(#arrow)"/>
          <g transform="translate(460 275)">
            <rect x="0" y="0" width="180" height="92" rx="8" fill="#fff2f0" stroke="#f0c8c3"/>
            <text x="18" y="32" font-size="16" font-weight="800" fill="#ba3f35">真实输入</text>
            <text x="18" y="59" font-size="13" fill="#142033">“今天 3 点前请</text>
            <text x="18" y="79" font-size="13" fill="#142033">签字确认”</text>
          </g>
          <path d="M650 320 H725" stroke="#8fa6c6" stroke-width="3" marker-end="url(#arrow)"/>
          <g transform="translate(735 275)">
            <rect x="0" y="0" width="110" height="92" rx="8" fill="#142033"/>
            <text x="21" y="43" font-size="16" font-weight="800" fill="#fff">输出</text>
            <text x="21" y="69" font-size="14" fill="#dbe8ff">immediate</text>
          </g>
          <g transform="translate(45 400)">
            <rect x="0" y="0" width="790" height="38" rx="8" fill="#eef5ff" stroke="#c9d9f3"/>
            <text x="18" y="25" font-size="14" font-weight="800" fill="#235fc6">重点：</text>
            <text x="64" y="25" font-size="14" fill="#142033">编译时可以用大模型和云端资源；运行时只需要小模型、共享 base 和一个任务小权重。</text>
          </g>
          <defs>
            <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
              <path d="M0,0 L0,6 L9,3 z" fill="#8fa6c6"/>
            </marker>
          </defs>
        </svg>
      </div>
      <h3>四步理解</h3>
      <ul>
        <li><b>第一步，写规格：</b>开发者用自然语言描述一个模糊函数，例如“只筛出真正需要报警的日志”。</li>
        <li><b>第二步，规格清洗：</b>一个 4B 伪编译器把口语需求改写成更清楚的伪程序，并补几个例子。</li>
        <li><b>第三步，生成权重：</b>训练过的 LoRA 编译器把规格和伪程序变成一个小型适配器。</li>
        <li><b>第四步，本地运行：</b>冻结的小解释器加载这个适配器，像普通函数一样处理每个输入。</li>
      </ul>
    </section>

    <section class="section">
      <h2>6. 关键术语解释</h2>
      <div class="terms">
        <div class="term"><strong>Fuzzy Function</strong><p><b>专业解释：</b>难以用确定规则完整定义、但可以通过语言、例子或约束描述的函数。</p><p><b>白话解释：</b>像“这条客户反馈是不是很紧急”这种人能判断、代码规则很难写全的任务。</p></div>
        <div class="term"><strong>Program-as-Weights</strong><p><b>专业解释：</b>把一个任务编译成参数高效适配器，由冻结解释器执行。</p><p><b>白话解释：</b>程序不再是一段代码，而是一个小权重文件。</p></div>
        <div class="term"><strong>LoRA</strong><p><b>专业解释：</b>低秩适配方法，用小矩阵改变大模型行为，不改动原模型主体。</p><p><b>白话解释：</b>像给模型戴一副任务专用眼镜，而不是重做整颗大脑。</p></div>
        <div class="term"><strong>PEFT</strong><p><b>专业解释：</b>Parameter-Efficient Fine-Tuning，用少量参数适配大模型。</p><p><b>白话解释：</b>用很小的外挂包，让模型学会一个新习惯。</p></div>
        <div class="term"><strong>Interpreter</strong><p><b>专业解释：</b>冻结的小模型运行时，负责加载任务权重并生成输出。</p><p><b>白话解释：</b>固定的本地播放器；不同任务换不同插件。</p></div>
        <div class="term"><strong>Quantization</strong><p><b>专业解释：</b>用更低精度表示模型权重，减少内存与磁盘占用。</p><p><b>白话解释：</b>把大件行李压缩打包，让普通电脑也能带得动。</p></div>
      </div>
    </section>

    <section class="section">
      <h2>7. 实验结果解读</h2>
      <p>论文最抓人的结果是：一个 0.6B 的 Qwen3 解释器执行 PAW 程序，在 FuzzyBench 上达到 73.78% exact match，高于直接 prompt Qwen3-32B 的 68.70%。作者还报告推理内存大约从 60GB 降到 1.2GB 级别。</p>
      <div class="bars">
        <div class="bar-row"><span>PAW 0.6B</span><div class="track"><div class="bar green" style="width:73.78%"></div></div><b>73.78%</b></div>
        <div class="bar-row"><span>Qwen3-32B prompt</span><div class="track"><div class="bar" style="width:68.70%"></div></div><b>68.70%</b></div>
        <div class="bar-row"><span>Qwen3-14B prompt</span><div class="track"><div class="bar gold" style="width:63.96%"></div></div><b>63.96%</b></div>
        <div class="bar-row"><span>Qwen3-4B prompt</span><div class="track"><div class="bar violet" style="width:49.63%"></div></div><b>49.63%</b></div>
        <div class="bar-row"><span>Qwen3-0.6B prompt</span><div class="track"><div class="bar red" style="width:9.84%"></div></div><b>9.84%</b></div>
      </div>
      <div class="table-wrap">
        <table>
          <tr><th>结果</th><th>论文数字</th><th>普通读者应如何理解</th></tr>
          <tr><td>主任务准确率</td><td>PAW 0.6B：73.78%；Qwen3-32B prompt：68.70%</td><td>小模型加“任务插件”可以超过大模型临场发挥。</td></tr>
          <tr><td>推理内存</td><td>约 1.2GB vs 约 60GB</td><td>从服务器级部署，靠近普通设备或私有边缘节点部署。</td></tr>
          <tr><td>本地速度</td><td>MacBook M3 上约 30 tokens/s；Q5_K_M + Q4_0 为 31.6 tokens/s</td><td>不是只能停留在论文服务器上的演示，作者强调了端侧可运行性。</td></tr>
          <tr><td>部署大小</td><td>共享 base 约 430MB；每个任务 LoRA 约 23MB</td><td>一个 base 可以服务很多小函数；新增任务主要增加小插件。</td></tr>
          <tr><td>工具调用案例</td><td>10 个 PAW 函数组成 pipeline，在 TOOLCALL-15 上得 93%</td><td>复杂产品可以由多个小模糊函数拼成，而不是单个全能大模型顶到底。</td></tr>
        </table>
      </div>
      <div class="note"><b>结果意味着什么：</b>如果后续被更多任务验证，企业可以把大量“轻量但高频”的 AI 判断放到本地：日志报警、工单分类、客服意图识别、搜索重排、格式修复。大模型仍然在编译阶段发挥价值，但运行成本会显著下降。</div>
    </section>

    <section class="section">
      <h2>8. 局限性与问题</h2>
      <div class="cards">
        <div class="card"><span class="tag red">数据依赖</span><p>FuzzyBench 主要由强模型生成，测试集也经过模型一致性过滤。它很适合训练原型，但仍需要真实业务数据验证。</p></div>
        <div class="card"><span class="tag gold">任务边界</span><p>PAW 适合边界清楚的模糊函数，不适合开放式长推理、复杂规划或需要持续外部知识更新的任务。</p></div>
        <div class="card"><span class="tag violet">调试困难</span><p>权重文件比源码更难读。它可版本化，但不等于可解释；上线前仍需要测试集、回归评估和异常监控。</p></div>
      </div>
      <ul>
        <li><b>安全问题：</b>如果编译器被投毒，生成的小权重可能隐藏偏见或后门。未来需要“神经程序扫描器”和签名机制。</li>
        <li><b>更新问题：</b>模糊函数一旦部署，业务规则变化时需要重新编译并验证，不是一次生成永远正确。</li>
        <li><b>长输出问题：</b>论文在图像条件任务中也显示，长输入/长输出场景可能挤占小解释器上下文，性能并非全面胜出。</li>
        <li><b>评测泛化：</b>73.78% 是 FuzzyBench verified test set 上的结果，不能直接外推到所有企业场景。</li>
      </ul>
    </section>

    <section class="section">
      <h2>9. 产业影响分析</h2>
      <p class="lead">如果这条路线成熟，AI 产品会从“云端大模型接口”多一层演化成“可分发、可缓存、可审计的小型神经函数库”。</p>
      <div class="table-wrap">
        <table>
          <tr><th>受益方</th><th>可能变化</th><th>需要补上的能力</th></tr>
          <tr><td>企业软件团队</td><td>把高频分类、抽取、重排、清洗任务下沉到本地或私有环境。</td><td>神经函数的测试、版本、回滚、灰度和监控。</td></tr>
          <tr><td>端侧 AI / PC / 手机厂商</td><td>共享小模型 base + 多个任务插件，形成更轻的本地 AI 生态。</td><td>模型运行时、插件市场、权限管理和能耗优化。</td></tr>
          <tr><td>LLM 平台</td><td>收入形态可能从“按 token 执行”扩展到“编译任务、分发工具”。</td><td>编译 API、质量证明、适配器托管和企业合规。</td></tr>
          <tr><td>开源生态</td><td>未来可能出现类似 npm/pip 的神经程序包。</td><td>权重签名、许可证、供应链安全和复现标准。</td></tr>
          <tr><td>数据与安全团队</td><td>隐私敏感判断可以不离开本地设备。</td><td>本地评测集、偏差审计、漂移检测。</td></tr>
        </table>
      </div>
      <div class="diagram" aria-label="产业形态变化示意图">
        <svg viewBox="0 0 880 330" role="img">
          <rect width="880" height="330" fill="#fbfdff"/>
          <text x="36" y="44" font-size="24" font-weight="800" fill="#142033">从 API 经济到“神经函数库”</text>
          <g transform="translate(60 86)">
            <rect x="0" y="0" width="290" height="170" rx="8" fill="#eef5ff" stroke="#c9d9f3"/>
            <text x="24" y="34" font-size="18" font-weight="800" fill="#235fc6">今天常见形态</text>
            <text x="24" y="72" font-size="14" fill="#142033">每条输入 → 远程大模型</text>
            <text x="24" y="104" font-size="14" fill="#142033">优点：通用、灵活</text>
            <text x="24" y="132" font-size="14" fill="#142033">代价：贵、慢、依赖网络、难复现</text>
          </g>
          <path d="M380 170 H500" stroke="#8fa6c6" stroke-width="4" marker-end="url(#arrow2)"/>
          <g transform="translate(530 86)">
            <rect x="0" y="0" width="290" height="170" rx="8" fill="#effaf5" stroke="#cce8db"/>
            <text x="24" y="34" font-size="18" font-weight="800" fill="#0f8a5f">PAW 想象形态</text>
            <text x="24" y="72" font-size="14" fill="#142033">任务规格 → 编译一次</text>
            <text x="24" y="104" font-size="14" fill="#142033">之后本地小模型反复执行</text>
            <text x="24" y="132" font-size="14" fill="#142033">像安装很多可管理的小 AI 函数</text>
          </g>
          <defs>
            <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
              <path d="M0,0 L0,6 L9,3 z" fill="#8fa6c6"/>
            </marker>
          </defs>
        </svg>
      </div>
    </section>

    <section class="section">
      <h2>10. 延伸阅读</h2>
      <ul>
        <li><a href="https://arxiv.org/abs/2607.02512">Program-as-Weights arXiv abstract</a>：论文摘要、作者与提交时间。</li>
        <li><a href="https://arxiv.org/html/2607.02512v1">arXiv HTML</a>：适合浏览器阅读的正文版本。</li>
        <li><a href="https://github.com/programasweights">Program-as-Weights GitHub</a>：作者给出的代码入口。</li>
        <li><a href="https://programasweights.com">Program-as-Weights demo</a>：公开 demo 网站。</li>
        <li><a href="https://huggingface.co/papers/2607.02512">Hugging Face Papers</a>：社区论文页。</li>
        <li><a href="https://arxiv.org/abs/2106.09685">LoRA: Low-Rank Adaptation of Large Language Models</a>：理解 PAW 权重适配器的基础论文。</li>
        <li><a href="https://arxiv.org/abs/2506.02153">Small Language Models are the Future of Agentic AI</a>：论文引用的“小模型未来”背景方向。</li>
      </ul>
    </section>

    <section class="section">
      <h2>11. 引用来源</h2>
      <div class="table-wrap">
        <table>
          <tr><th>来源</th><th>用途</th><th>链接</th></tr>
          <tr><td>arXiv abstract</td><td>标题、作者、机构、日期、摘要</td><td><a href="https://arxiv.org/abs/2607.02512">https://arxiv.org/abs/2607.02512</a></td></tr>
          <tr><td>arXiv HTML/PDF</td><td>核心方法、实验数字、FuzzyBench、局限分析</td><td><a href="https://arxiv.org/html/2607.02512v1">https://arxiv.org/html/2607.02512v1</a></td></tr>
          <tr><td>Program-as-Weights GitHub</td><td>代码与项目入口核验</td><td><a href="https://github.com/programasweights">https://github.com/programasweights</a></td></tr>
          <tr><td>Program-as-Weights demo</td><td>公开演示入口核验</td><td><a href="https://programasweights.com">https://programasweights.com</a></td></tr>
          <tr><td>Hugging Face Papers</td><td>社区论文页交叉确认</td><td><a href="https://huggingface.co/papers/2607.02512">https://huggingface.co/papers/2607.02512</a></td></tr>
        </table>
      </div>
      <p class="footer">本报告使用英文原始信息源写成。图示为重新设计的中文解释图，不是论文截图。生成式头图由内置图像生成工具创建，并以内嵌 data URI 放入 HTML，确保附件离线可读。</p>
    </section>
  </main>
</body>
</html>
"""

HTML.write_text(html, encoding="utf-8")
SUBJECT.write_text("【AI每日论文精选】当大模型开始把自己编译成小工具", encoding="utf-8")
BODY.write_text(
    """今天精选的论文是 Program-as-Weights，来自 University of Waterloo、Cornell University 与 Harvard University。

一句话推荐理由：
它把大模型从“每次都远程回答问题”，改造成“先把模糊任务编译成一个本地可运行的小权重函数”。

这可能改变 AI 工程的成本结构、隐私边界和端侧部署方式。

附件为中文深度拆解 HTML 报告，适合非技术读者阅读。
""",
    encoding="utf-8",
)
SOURCES.write_text(
    """# Sources

- arXiv abstract: https://arxiv.org/abs/2607.02512
- arXiv HTML: https://arxiv.org/html/2607.02512v1
- arXiv PDF: https://arxiv.org/pdf/2607.02512
- Official GitHub organization: https://github.com/programasweights
- Official demo: https://programasweights.com
- Hugging Face Papers: https://huggingface.co/papers/2607.02512
- Papers With Code search checked: https://paperswithcode.com/search?q=Program-as-Weights
- Local PDF text extraction: reports/2026-07-07-program-as-weights/sources/paw_pdf.txt
- Generated hero image: reports/2026-07-07-program-as-weights/paw-hero.png

Key checked facts:

- Selected paper: `Program-as-Weights: A Programming Paradigm for Fuzzy Functions`.
- arXiv ID: `2607.02512`; submitted 2026-07-02.
- Authors: Wentao Zhang, Liliana Hotsko, Woojeong Kim, Pengyu Nie, Stuart Shieber, Yuntian Deng.
- Institutions: University of Waterloo, Cornell University, Harvard University.
- Core idea: compile fuzzy functions from natural-language specifications into compact locally executable neural artifacts.
- System: 4B compiler, frozen lightweight interpreter, current best instantiation is Text-to-LoRA.
- Dataset: FuzzyBench, 10M examples across 29 thematic versions and more than 800 sub-categories.
- Main result used in report: PAW Qwen3-0.6B 73.78% exact match on FuzzyBench vs Qwen3-32B prompting 68.70%; roughly 50x less inference memory.
- Local execution facts used in report: about 430MB shared GGUF base plus about 23MB per-program LoRA adapter; roughly 30 tokens/s on MacBook M3; Q5_K_M + Q4_0 table reports 31.6 tokens/s with 0.48s cold load.
""",
    encoding="utf-8",
)

print(HTML)
