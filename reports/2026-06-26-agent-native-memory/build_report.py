from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HERO = ROOT / "agent-native-memory-hero.png"
REPORT = ROOT / "AI-Daily-Paper-Agent-Native-Memory-2026-06-26-embedded.html"
EMAIL_BODY = ROOT / "email-body.html"
SUBJECT = ROOT / "email_subject.txt"
SOURCES = ROOT / "sources.md"
RUN_SUMMARY = ROOT / "run_summary.md"


def data_uri(path: Path) -> str:
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


hero_uri = data_uri(HERO)
generated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI每日论文精选：Agent 原生记忆系统</title>
  <style>
    :root {{
      color-scheme: light dark;
      --ink:#111827;
      --muted:#5f6b7a;
      --soft:#f5f7fb;
      --line:#d9e1ec;
      --paper:#ffffff;
      --navy:#101827;
      --cyan:#2aa8d8;
      --gold:#c7903f;
      --green:#2f9b78;
      --red:#b85656;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0;
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Arial,sans-serif;
      background:#edf1f7;
      color:var(--ink);
      line-height:1.72;
      letter-spacing:0;
    }}
    a {{ color:#156b9a; text-decoration:none; border-bottom:1px solid rgba(21,107,154,.25); }}
    .page {{ max-width:1080px; margin:0 auto; background:var(--paper); box-shadow:0 20px 70px rgba(16,24,39,.12); }}
    .hero {{
      position:relative;
      min-height:560px;
      color:#fff;
      overflow:hidden;
      background:#0d1320;
    }}
    .hero img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.7; }}
    .hero::after {{
      content:"";
      position:absolute; inset:0;
      background:linear-gradient(90deg,rgba(7,12,21,.95),rgba(7,12,21,.72) 48%,rgba(7,12,21,.24));
    }}
    .hero-inner {{ position:relative; z-index:1; max-width:760px; padding:72px 54px 54px; }}
    .eyebrow {{ font-size:13px; color:#b8d8e8; text-transform:uppercase; font-weight:700; letter-spacing:.08em; }}
    h1 {{ margin:18px 0 16px; font-size:48px; line-height:1.08; letter-spacing:0; }}
    .subtitle {{ font-size:21px; color:#e8eef5; max-width:680px; }}
    .hero-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:34px; max-width:720px; }}
    .metric {{ border:1px solid rgba(255,255,255,.18); background:rgba(255,255,255,.08); padding:14px; border-radius:8px; backdrop-filter:blur(8px); }}
    .metric strong {{ display:block; font-size:24px; line-height:1.1; color:#fff; }}
    .metric span {{ display:block; margin-top:6px; font-size:12px; color:#c8d3de; line-height:1.45; }}
    section {{ padding:42px 54px; border-top:1px solid var(--line); }}
    h2 {{ margin:0 0 18px; font-size:28px; line-height:1.25; letter-spacing:0; }}
    h3 {{ margin:28px 0 10px; font-size:19px; line-height:1.35; letter-spacing:0; }}
    p {{ margin:0 0 15px; }}
    .lead {{ font-size:19px; color:#263342; }}
    .cards {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:18px; }}
    .card {{ border:1px solid var(--line); border-radius:8px; padding:18px; background:#fff; }}
    .card h3 {{ margin-top:0; }}
    .kicker {{ display:inline-block; font-size:12px; font-weight:700; color:#445468; background:#ecf3f8; border-radius:999px; padding:3px 10px; margin-bottom:8px; }}
    table {{ width:100%; border-collapse:collapse; margin:18px 0 8px; font-size:14px; }}
    th,td {{ border-bottom:1px solid var(--line); padding:12px 10px; text-align:left; vertical-align:top; }}
    th {{ background:#f4f7fb; color:#263342; font-weight:700; }}
    .note {{ border-left:4px solid var(--cyan); background:#eef8fc; padding:14px 16px; margin:18px 0; color:#20313d; }}
    .risk {{ border-left-color:var(--red); background:#fff3f2; }}
    .quote {{ font-size:22px; line-height:1.45; font-weight:700; color:#111827; padding:22px; background:#f6f8fb; border:1px solid var(--line); border-radius:8px; }}
    .viz {{ margin:22px 0; border:1px solid var(--line); border-radius:8px; background:#fbfdff; overflow:hidden; }}
    .viz svg {{ width:100%; height:auto; display:block; }}
    .caption {{ font-size:13px; color:var(--muted); margin:8px 0 0; }}
    .two {{ display:grid; grid-template-columns:1.1fr .9fr; gap:20px; align-items:start; }}
    .term {{ display:grid; grid-template-columns:180px 1fr 1fr; gap:0; border:1px solid var(--line); border-bottom:none; }}
    .term div {{ padding:12px; border-bottom:1px solid var(--line); }}
    .term div:nth-child(3n+1) {{ font-weight:700; background:#f4f7fb; }}
    .footer {{ background:#101827; color:#cbd5e1; padding:34px 54px; font-size:14px; }}
    .footer a {{ color:#9ed8f4; }}
    @media (max-width:760px) {{
      .page {{ box-shadow:none; }}
      .hero {{ min-height:620px; }}
      .hero-inner, section, .footer {{ padding:30px 22px; }}
      h1 {{ font-size:36px; }}
      .subtitle {{ font-size:18px; }}
      .hero-grid, .cards, .two {{ grid-template-columns:1fr; }}
      .term {{ grid-template-columns:1fr; }}
      .term div:nth-child(3n+1) {{ border-top:10px solid #fff; }}
      table {{ font-size:13px; }}
    }}
  </style>
</head>
<body>
<main class="page">
  <header class="hero">
    <img src="{hero_uri}" alt="Agent 原生记忆系统主题图">
    <div class="hero-inner">
      <div class="eyebrow">AI DAILY PAPER SELECTION · 2026-06-26</div>
      <h1>AI Agent 终于要有真正的“记忆系统”了吗？</h1>
      <p class="subtitle">今日论文不是在给模型加一个更大的文件夹，而是在追问：如果 Agent 要长期工作、持续学习、记住用户和工具执行过程，记忆层到底该像搜索引擎、数据库，还是像一个有生命周期的操作系统？</p>
      <div class="hero-grid">
        <div class="metric"><strong>12+2</strong><span>12 个代表性记忆系统 + 2 个基线</span></div>
        <div class="metric"><strong>5</strong><span>端到端评估视角：效果、检索、更新、长程、成本</span></div>
        <div class="metric"><strong>11</strong><span>横跨 5 类工作负载的数据集</span></div>
        <div class="metric"><strong>结论</strong><span>没有一种记忆架构可以通吃所有任务</span></div>
      </div>
    </div>
  </header>

  <section>
    <h2>1. 标题区</h2>
    <table>
      <tr><th>论文</th><td><strong>Are We Ready For An Agent-Native Memory System?</strong><br>中文译名：我们准备好构建 Agent 原生记忆系统了吗？</td></tr>
      <tr><th>作者</th><td>Wei Zhou, Xuanhe Zhou, Shaokun Han, Hongming Xu, Guoliang Li, Zhiyu Li, Feiyu Xiong, Fan Wu</td></tr>
      <tr><th>机构</th><td>Shanghai Jiao Tong University, Tsinghua University, MemTensor (Shanghai) Technology Co., Ltd</td></tr>
      <tr><th>发布时间</th><td>2026-06-23，arXiv:2606.24775v1</td></tr>
      <tr><th>平台</th><td>arXiv · cs.CL / cs.DB / cs.IR；官方代码库 MemoryData 已公开</td></tr>
      <tr><th>链接</th><td><a href="https://arxiv.org/abs/2606.24775">arXiv 摘要</a> · <a href="https://arxiv.org/html/2606.24775">arXiv HTML</a> · <a href="https://github.com/OpenDataBox/MemoryData">GitHub / MemoryData</a> · <a href="https://huggingface.co/papers/2606.24775">Hugging Face Papers</a></td></tr>
    </table>
  </section>

  <section>
    <h2>2. 为什么今天选它？</h2>
    <p class="lead">因为 Agent 的下一场竞争，很可能不只是“谁的模型更聪明”，而是“谁的系统更会记、会忘、会更新、会用证据”。</p>
    <div class="cards">
      <div class="card"><span class="kicker">行业意义</span><h3>记忆正从功能变成基础设施</h3><p>今天很多产品说自己有记忆，本质只是把聊天记录塞回上下文。论文指出，真正的 Agent 记忆要支持持久存储、更新、冲突解决、检索路由和维护成本管理。</p></div>
      <div class="card"><span class="kicker">技术突破</span><h3>把“记忆”拆成四个工程模块</h3><p>作者没有只看最终答题分数，而是拆成表示/存储、抽取、检索/路由、维护四层。这样才能知道到底是“没记住”“找不到”“记错了”，还是“维护太贵”。</p></div>
      <div class="card"><span class="kicker">长期价值</span><h3>它给 Agent 工程立了一把尺</h3><p>未来做企业助理、个人助理、科研 Agent、数据 Agent，都绕不开长期状态管理。这篇论文像是在给 Agent 记忆系统做一次基础体检。</p></div>
    </div>
    <div class="note">一句判断：如果 2023-2025 年大家在问“Agent 会不会用工具”，那么 2026 年更关键的问题会变成“Agent 能不能在长期工作中管理自己的经验”。</div>
  </section>

  <section>
    <h2>3. 一句话讲透论文</h2>
    <div class="quote">这篇论文在说：AI Agent 不能只靠“把过去聊天搜出来”，它需要一套像公司档案室一样的记忆系统，知道什么该存、怎么分类、何时更新、用时怎么找、过期了怎么删。</div>
  </section>

  <section>
    <h2>4. 核心贡献拆解</h2>
    <table>
      <tr><th>贡献</th><th>它解决了什么</th><th>为什么更好</th></tr>
      <tr><td>四模块框架</td><td>把 Agent 记忆拆成表示/存储、抽取、检索/路由、维护。</td><td>不再把记忆系统当黑盒，能定位系统问题。</td></tr>
      <tr><td>统一评测</td><td>在 5 类工作负载、11 个数据集上比较 12 个系统和 2 个基线。</td><td>避免每篇论文只在自己的小赛道里赢。</td></tr>
      <tr><td>细粒度消融</td><td>分别测试表示、抽取、检索、维护策略的作用。</td><td>告诉工程师到底该改哪个零件。</td></tr>
      <tr><td>成本视角</td><td>不仅看准确率，也看索引构建、查询延迟、维护开销。</td><td>把“能跑 demo”推进到“能不能生产部署”。</td></tr>
    </table>
  </section>

  <section>
    <h2>5. 工作原理：把 Agent 记忆想成一家公司档案室</h2>
    <p>一个长期工作的 Agent，就像一个不断接案的咨询团队。它每天收到用户偏好、工具调用记录、任务结果、环境变化。如果只是把所有聊天记录堆在桌上，短期还行，长期一定混乱。</p>
    <div class="viz">
      <svg viewBox="0 0 980 460" role="img" aria-label="Agent 记忆系统四模块流程图">
        <defs>
          <linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="#101827"/><stop offset="1" stop-color="#1f6f91"/></linearGradient>
          <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#557085"/></marker>
        </defs>
        <rect width="980" height="460" fill="#fbfdff"/>
        <rect x="36" y="52" width="190" height="108" rx="8" fill="#101827"/>
        <text x="62" y="92" fill="#fff" font-size="24" font-weight="700">原始经历</text>
        <text x="62" y="124" fill="#cbd5e1" font-size="15">对话、工具日志、环境观察</text>
        <line x1="226" y1="106" x2="286" y2="106" stroke="#557085" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="286" y="38" width="160" height="136" rx="8" fill="#eef8fc" stroke="#9bd3e8"/>
        <text x="312" y="76" fill="#183649" font-size="20" font-weight="700">1. 表示/存储</text>
        <text x="312" y="108" fill="#516173" font-size="14">事实、向量、图谱、树</text>
        <text x="312" y="132" fill="#516173" font-size="14">决定“放哪里”</text>
        <line x1="446" y1="106" x2="496" y2="106" stroke="#557085" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="496" y="38" width="160" height="136" rx="8" fill="#fff8ec" stroke="#e7c58e"/>
        <text x="522" y="76" fill="#563b14" font-size="20" font-weight="700">2. 记忆抽取</text>
        <text x="522" y="108" fill="#625544" font-size="14">从经历提炼可用事实</text>
        <text x="522" y="132" fill="#625544" font-size="14">决定“记什么”</text>
        <line x1="656" y1="106" x2="706" y2="106" stroke="#557085" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="706" y="38" width="200" height="136" rx="8" fill="#f1f7f4" stroke="#9bceb6"/>
        <text x="732" y="76" fill="#173f31" font-size="20" font-weight="700">3. 检索/路由</text>
        <text x="732" y="108" fill="#50675c" font-size="14">按问题找证据、走图谱</text>
        <text x="732" y="132" fill="#50675c" font-size="14">决定“怎么找”</text>
        <rect x="286" y="244" width="620" height="118" rx="8" fill="url(#g1)"/>
        <text x="326" y="286" fill="#fff" font-size="22" font-weight="700">4. 维护：更新、合并、去重、忘记</text>
        <text x="326" y="320" fill="#d6e5ee" font-size="15">旧事实被新事实覆盖；冲突要解决；低价值信息要清理；否则系统会越来越慢、越来越矛盾。</text>
        <path d="M806 174 C806 226 760 252 690 270" fill="none" stroke="#557085" stroke-width="3" marker-end="url(#arrow)"/>
        <path d="M370 244 C300 220 304 182 344 174" fill="none" stroke="#557085" stroke-width="3" marker-end="url(#arrow)"/>
        <rect x="54" y="294" width="160" height="82" rx="8" fill="#ffffff" stroke="#d9e1ec"/>
        <text x="78" y="328" fill="#111827" font-size="19" font-weight="700">Agent 决策</text>
        <text x="78" y="354" fill="#5f6b7a" font-size="14">拿到正确上下文再行动</text>
        <path d="M706 170 C560 230 330 276 214 326" fill="none" stroke="#557085" stroke-width="3" marker-end="url(#arrow)"/>
      </svg>
    </div>
    <p class="caption">重构图示：论文的四模块框架。普通理解：先决定资料怎么建档，再决定从经历里提取什么，之后按任务找证据，最后持续维护档案健康。</p>

    <h3>为什么这比普通 RAG 更难？</h3>
    <table>
      <tr><th>系统</th><th>像什么</th><th>主要动作</th><th>短板</th></tr>
      <tr><td>普通 RAG</td><td>临时查资料</td><td>问一次，检索一次，塞进上下文</td><td>多半是只读、静态、无生命周期管理</td></tr>
      <tr><td>长上下文</td><td>把所有材料摊在桌上</td><td>让模型自己在长文本里找</td><td>成本高，干扰多，远距离事实容易被淹没</td></tr>
      <tr><td>Agent 原生记忆</td><td>有管理员的档案室</td><td>写入、分类、索引、更新、合并、遗忘</td><td>设计复杂，需要权衡准确率、延迟、维护成本</td></tr>
    </table>
  </section>

  <section>
    <h2>6. 关键术语解释</h2>
    <div class="term">
      <div>Agent Memory</div><div>专业解释：Agent 在多轮执行中持久管理历史交互、环境观察、工具执行和中间状态的数据系统。</div><div>白话：AI 的工作笔记和档案室。</div>
      <div>Representation</div><div>专业解释：记忆被编码成文本、向量、图、树或复合对象的方式。</div><div>白话：同一份资料，是写成便签、表格、地图，还是知识图谱。</div>
      <div>Retrieval / Routing</div><div>专业解释：根据当前查询选择相关记忆子集，并决定通过向量搜索、图遍历、过滤或多阶段路由访问。</div><div>白话：来问题时，去哪几个柜子里翻档案。</div>
      <div>Maintenance</div><div>专业解释：冲突解决、版本更新、容量控制、语义合并和遗忘策略。</div><div>白话：档案管理员定期整理、去重、废弃过期记录。</div>
      <div>Recall@K</div><div>专业解释：前 K 个检索结果里是否包含标准证据。</div><div>白话：翻出的前几份材料里，有没有真正需要的那份。</div>
      <div>Long-Horizon Stability</div><div>专业解释：当历史变长、证据距离当前问题更远时，系统性能是否还能保持。</div><div>白话：半年后还能不能记得今天说过的关键事。</div>
    </div>
  </section>

  <section>
    <h2>7. 实验结果解读：结果意味着什么</h2>
    <table>
      <tr><th>发现</th><th>论文数据点</th><th>人话解释</th></tr>
      <tr><td>没有万能记忆架构</td><td>Zep 在 LongMemEval LLM Judge Accuracy 达到 48.0；Cognee 的 ROUGE-L F1 为 35.3；MemOS 在 LoCoMo EM 达到 11.5；DB-Bench 上 Long Context EM 为 48.20，MemoChat Task Success Rate 为 55.40。</td><td>不同任务需要不同档案室。找跨会话事实、找精确个人偏好、执行数据库操作，最优结构并不一样。</td></tr>
      <tr><td>检索不是只看第一条</td><td>SimpleMem 的 Recall@1 最高为 39.0；但 A-MEM 在 Recall@5/@10 达到 69.5/85.9，MemTree 达到 59.7/80.5。</td><td>复杂问题常需要多份证据。只翻出一条看似相关的记忆，不等于能回答好。</td></tr>
      <tr><td>长上下文不等于长记忆</td><td>LongBench 中 Long Context 从短上下文 42.6 准确率跌到中等上下文 19.0；LoCoMo 中 Embedding RAG 随证据距离扩大从 37.1 Answer F1 跌到 7.4。</td><td>材料越堆越多，模型不一定更聪明，反而更容易在噪声里迷路。</td></tr>
      <tr><td>局部维护更划算</td><td>LightMem 以 3.67 秒/查询达到 48.3 Normalized Utility；MemTree 15.9 秒达到 63.5；而 Cognee/Zep 超过 84 Utility 需要 116.5/155.1 秒级开销。</td><td>档案室越精细，整理越贵。生产系统不能只看准确率，还要看每次更新和查询要花多少钱。</td></tr>
    </table>
    <div class="viz">
      <svg viewBox="0 0 980 420" role="img" aria-label="实验发现图示">
        <rect width="980" height="420" fill="#fbfdff"/>
        <text x="40" y="48" font-size="25" font-weight="700" fill="#111827">三条最值得记住的实验结论</text>
        <g transform="translate(40 82)">
          <rect width="280" height="250" rx="8" fill="#eef8fc" stroke="#9bd3e8"/>
          <text x="24" y="42" font-size="21" font-weight="700" fill="#17364a">1. 架构要匹配任务</text>
          <rect x="24" y="78" width="210" height="18" rx="4" fill="#2aa8d8"/>
          <rect x="24" y="112" width="150" height="18" rx="4" fill="#7bbfd8"/>
          <rect x="24" y="146" width="230" height="18" rx="4" fill="#156b9a"/>
          <text x="24" y="205" font-size="15" fill="#516173">跨会话、精确问答、执行任务</text>
          <text x="24" y="230" font-size="15" fill="#516173">需要不同记忆形态。</text>
        </g>
        <g transform="translate(350 82)">
          <rect width="280" height="250" rx="8" fill="#fff8ec" stroke="#e7c58e"/>
          <text x="24" y="42" font-size="21" font-weight="700" fill="#563b14">2. 找证据要成组</text>
          <circle cx="72" cy="112" r="28" fill="#c7903f"/>
          <circle cx="142" cy="112" r="28" fill="#e5bf7b"/>
          <circle cx="212" cy="112" r="28" fill="#f1d9a8"/>
          <path d="M100 112 H114 M170 112 H184" stroke="#7a5520" stroke-width="3"/>
          <text x="24" y="205" font-size="15" fill="#625544">复杂问题不是命中一条记录，</text>
          <text x="24" y="230" font-size="15" fill="#625544">而是拼回完整证据链。</text>
        </g>
        <g transform="translate(660 82)">
          <rect width="280" height="250" rx="8" fill="#f1f7f4" stroke="#9bceb6"/>
          <text x="24" y="42" font-size="21" font-weight="700" fill="#173f31">3. 维护范围决定成本</text>
          <rect x="26" y="78" width="58" height="128" rx="6" fill="#2f9b78"/>
          <rect x="106" y="122" width="58" height="84" rx="6" fill="#75b89f"/>
          <rect x="186" y="48" width="58" height="158" rx="6" fill="#b85656"/>
          <text x="24" y="230" font-size="15" fill="#50675c">局部更新便宜；全局重排昂贵。</text>
        </g>
      </svg>
    </div>
  </section>

  <section>
    <h2>8. 局限性与问题</h2>
    <div class="cards">
      <div class="card"><span class="kicker">现实瓶颈</span><h3>统一评测仍不等于真实生产</h3><p>论文覆盖多个基准，但企业 Agent 会遇到权限、隐私、业务状态、审计追踪、跨系统事务等更复杂问题。</p></div>
      <div class="card"><span class="kicker">成本问题</span><h3>结构化记忆可能很贵</h3><p>图谱、多引擎同步、全局整理能提高组织能力，但延迟可能很高。生产环境必须设预算，而不是无限整理。</p></div>
      <div class="card"><span class="kicker">安全风险</span><h3>记错比忘记更危险</h3><p>如果 Agent 把过期偏好、错误工具结果或冲突事实当成真相，可能稳定地产生错误决策。</p></div>
    </div>
    <div class="note risk">关键风险：记忆系统会把“偶发错误”变成“长期错误”。所以未来 Agent 安全不只要防提示注入，还要防错误记忆、污染记忆和越权记忆。</div>
  </section>

  <section>
    <h2>9. 产业影响分析</h2>
    <table>
      <tr><th>对象</th><th>可能受益</th><th>可能被冲击</th></tr>
      <tr><td>企业 Agent 平台</td><td>可以把记忆层做成可观测、可评估、可计费的基础设施。</td><td>只提供简单向量库接入的 Agent 框架会显得不够完整。</td></tr>
      <tr><td>数据库 / 向量库 / 图数据库厂商</td><td>记忆系统需要混合检索、版本管理、时间关系、成本优化，给数据基础设施打开新需求。</td><td>单一向量相似度搜索会被证明不是万能答案。</td></tr>
      <tr><td>AI 产品经理</td><td>可以把“记住用户”拆成可设计的产品能力：记什么、多久、谁可见、如何修改。</td><td>如果记忆体验不透明，用户会质疑隐私和控制权。</td></tr>
      <tr><td>投资研究者</td><td>Agent memory 可能成为 Agent 工程栈的独立层，类似检索、观测、评测之后的新基础设施赛道。</td><td>只押注更长上下文窗口，可能低估了结构化长期状态管理的价值。</td></tr>
    </table>
  </section>

  <section>
    <h2>10. 延伸阅读</h2>
    <ul>
      <li><a href="https://arxiv.org/abs/2606.24775">Are We Ready For An Agent-Native Memory System?</a></li>
      <li><a href="https://github.com/OpenDataBox/MemoryData">MemoryData: A Unified Memory Benchmark Suite for Memory-Augmented Agents</a></li>
      <li><a href="https://developers.openai.com/cookbook/examples/agents_sdk/context_personalization/">OpenAI Cookbook: Context Engineering for Personalization</a></li>
      <li><a href="https://adk.dev/sessions/memory/">Google ADK Memory Service documentation</a></li>
      <li><a href="https://huggingface.co/papers/2606.24775">Hugging Face Papers page</a></li>
    </ul>
  </section>

  <section>
    <h2>11. 引用来源</h2>
    <p>本报告优先使用英文原始来源：arXiv 摘要、arXiv HTML/PDF、官方 GitHub README、Hugging Face Papers、OpenAI Cookbook 与 Google ADK 文档。Semantic Scholar API 本次返回 429，因此未将其作为有效事实来源。</p>
    <table>
      <tr><th>来源</th><th>用途</th></tr>
      <tr><td>arXiv:2606.24775</td><td>标题、作者、机构、摘要、实验设置、核心结论、数据点。</td></tr>
      <tr><td>OpenDataBox/MemoryData GitHub</td><td>代码公开、基准套件、22 个 method presets、4 类 benchmark families。</td></tr>
      <tr><td>OpenAI Cookbook</td><td>产业交叉验证：长期记忆、状态管理、去重、冲突解决、遗忘。</td></tr>
      <tr><td>Google ADK Memory</td><td>产业交叉验证：Agent 长期记忆服务正在被框架化。</td></tr>
    </table>
  </section>

  <div class="footer">
    <strong>AI每日论文精选</strong><br>
    本期主题：Agent 原生记忆系统。生成时间：{generated_at}。报告为中文解读，不替代原论文阅读；关键数字均来自英文原始来源。
  </div>
</main>
</body>
</html>
"""

email_body = """<!doctype html>
<html lang="zh-CN"><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',Arial,sans-serif;line-height:1.7;color:#111827">
<p>今天精选的论文是 <strong>Are We Ready For An Agent-Native Memory System?</strong>。</p>
<p>一句话推荐理由：它把 AI Agent 的“记忆”从聊天记录检索，提升为一套需要表示、抽取、检索、更新和维护的长期数据系统。</p>
<p>这可能是 Agent 从演示走向长期生产力工具时，必须补上的基础设施层。</p>
<p>附件为中文深度拆解 HTML 报告，适合非技术读者阅读，也适合在手机和浏览器打开。</p>
</body></html>
"""

sources_md = """# Sources

- arXiv abstract: https://arxiv.org/abs/2606.24775
- arXiv HTML: https://arxiv.org/html/2606.24775
- arXiv PDF: https://arxiv.org/pdf/2606.24775
- GitHub: https://github.com/OpenDataBox/MemoryData
- Hugging Face Papers: https://huggingface.co/papers/2606.24775
- OpenAI Cookbook: https://developers.openai.com/cookbook/examples/agents_sdk/context_personalization/
- Google ADK Memory: https://adk.dev/sessions/memory/

Local source files are in `sources/`.
Semantic Scholar API returned 429 and was not used as a factual source.
"""

run_summary = f"""# Run Summary

- Automation: AI每日论文博客精选
- Automation ID: ai
- Run date: 2026-06-26 Asia/Shanghai
- Selected paper: Are We Ready For An Agent-Native Memory System? (arXiv:2606.24775)
- Authors: Wei Zhou, Xuanhe Zhou, Shaokun Han, Hongming Xu, Guoliang Li, Zhiyu Li, Feiyu Xiong, Fan Wu
- Institutions: Shanghai Jiao Tong University; Tsinghua University; MemTensor (Shanghai) Technology Co., Ltd
- Why selected: long-term Agent infrastructure signal; reframes memory as a persistent data management system with representation, extraction, retrieval/routing, and maintenance modules.
- Recently avoided: Qwen-AgentWorld, AI Chemist / LifeSciBench, Sumi, Arbor, SkillOpt, ToolPrivBench, MiniMax Sparse Attention, ABC-Bench, SWITCH latent reasoning, HiViG, LoopCoder-v2.
- Key facts: evaluates 12 representative memory systems plus two baselines; five benchmark workloads; 11 datasets; no single architecture dominates; localized maintenance is more cost-efficient than global reorganization.
- Generated image: {HERO}
- Artifact: {REPORT}
- Email body: {EMAIL_BODY}
- Sources: arXiv HTML/PDF, GitHub README, Hugging Face Papers, OpenAI Cookbook, Google ADK Memory docs.
- Generated at: {generated_at}
"""

REPORT.write_text(html, encoding="utf-8")
EMAIL_BODY.write_text(email_body, encoding="utf-8")
SUBJECT.write_text("【AI每日论文精选】AI Agent 终于要有真正的记忆系统了？\n", encoding="utf-8")
SOURCES.write_text(sources_md, encoding="utf-8")
RUN_SUMMARY.write_text(run_summary, encoding="utf-8")

print(f"wrote {REPORT}")
print(f"wrote {EMAIL_BODY}")
print(f"wrote {SUBJECT}")
print(f"wrote {SOURCES}")
print(f"wrote {RUN_SUMMARY}")
