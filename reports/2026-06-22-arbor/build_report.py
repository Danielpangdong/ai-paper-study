from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATE = "2026-06-22"
REPORT = ROOT / "AI-Daily-Paper-Arbor-2026-06-22-embedded.html"
EMAIL_BODY = ROOT / "email-body.html"
HERO = ROOT / "arbor-hero.png"


hero_data = base64.b64encode(HERO.read_bytes()).decode("ascii")

html = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI每日论文精选｜Arbor：让AI像研究团队一样累积假设、实验与证据</title>
<style>
  :root {
    color-scheme: light dark;
    --ink: #162022;
    --muted: #617075;
    --paper: #f6f7f4;
    --panel: #ffffff;
    --line: #d9e0dc;
    --teal: #0b6f6b;
    --teal-2: #0f8e8a;
    --amber: #b9822f;
    --dark: #0e1719;
    --soft: #edf4f1;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", "PingFang SC", Arial, sans-serif;
    background: var(--paper);
    color: var(--ink);
    line-height: 1.72;
    letter-spacing: 0;
  }
  a { color: var(--teal); text-decoration: none; }
  .wrap { max-width: 980px; margin: 0 auto; padding: 0 18px 56px; }
  .hero {
    position: relative;
    min-height: 560px;
    overflow: hidden;
    background: #0b1416;
    color: white;
  }
  .hero img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: .78;
  }
  .hero:after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(8,15,17,.94), rgba(8,15,17,.62) 42%, rgba(8,15,17,.12));
  }
  .hero-inner {
    position: relative;
    z-index: 1;
    max-width: 980px;
    margin: 0 auto;
    padding: 78px 18px 72px;
  }
  .eyebrow {
    display: inline-block;
    padding: 6px 10px;
    border: 1px solid rgba(255,255,255,.28);
    border-radius: 999px;
    font-size: 13px;
    color: #d8ece9;
    background: rgba(255,255,255,.06);
  }
  h1 {
    margin: 22px 0 18px;
    max-width: 760px;
    font-size: 42px;
    line-height: 1.13;
    letter-spacing: 0;
  }
  .subtitle {
    max-width: 710px;
    font-size: 19px;
    color: #d8e4e2;
  }
  .hero-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    max-width: 760px;
    margin-top: 30px;
  }
  .metric {
    padding: 14px;
    border: 1px solid rgba(255,255,255,.2);
    background: rgba(255,255,255,.08);
    border-radius: 8px;
  }
  .metric b { display: block; font-size: 22px; color: #fff; }
  .metric span { display: block; font-size: 12px; color: #c4d6d3; }
  section { margin-top: 34px; }
  h2 {
    margin: 0 0 14px;
    font-size: 25px;
    line-height: 1.24;
  }
  h3 {
    margin: 0 0 9px;
    font-size: 18px;
    line-height: 1.35;
  }
  p { margin: 0 0 14px; }
  .card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 12px 28px rgba(21,40,39,.05);
  }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
  .info-table, .data-table {
    width: 100%;
    border-collapse: collapse;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 8px;
    overflow: hidden;
  }
  th, td {
    padding: 12px 13px;
    border-bottom: 1px solid var(--line);
    vertical-align: top;
    text-align: left;
  }
  th { background: #eaf2ef; color: #263334; font-weight: 700; }
  tr:last-child td { border-bottom: 0; }
  .tag {
    display: inline-block;
    margin: 0 6px 6px 0;
    padding: 4px 9px;
    border-radius: 999px;
    background: var(--soft);
    color: #24524f;
    font-size: 12px;
    font-weight: 700;
  }
  .quote {
    border-left: 4px solid var(--teal);
    background: #eef6f3;
    padding: 16px 18px;
    border-radius: 0 8px 8px 0;
    font-size: 20px;
    font-weight: 750;
  }
  .plain {
    font-size: 18px;
    color: #203033;
  }
  .diagram {
    width: 100%;
    height: auto;
    display: block;
    background: #101a1c;
    border-radius: 8px;
    border: 1px solid #203235;
  }
  .note { color: var(--muted); font-size: 14px; }
  .accent { color: var(--teal); font-weight: 800; }
  .warn { border-left: 4px solid var(--amber); }
  .source-list li { margin-bottom: 8px; }
  .footer {
    margin-top: 42px;
    color: var(--muted);
    font-size: 13px;
  }
  @media (max-width: 720px) {
    .hero { min-height: 620px; }
    h1 { font-size: 31px; }
    .subtitle { font-size: 17px; }
    .hero-grid, .grid-2, .grid-3 { grid-template-columns: 1fr; }
    th, td { display: block; width: 100%; }
    tr { display: block; border-bottom: 1px solid var(--line); }
    tr:last-child { border-bottom: 0; }
    th { border-bottom: 0; }
  }
</style>
</head>
<body>
<header class="hero">
  <img src="data:image/png;base64,{{HERO_DATA}}" alt="Arbor hypothesis tree research workflow">
  <div class="hero-inner">
    <span class="eyebrow">AI每日论文精选 · 2026-06-22</span>
    <h1>Arbor：让 AI 像研究团队一样累积假设、实验与证据</h1>
    <p class="subtitle">今天这篇论文不是在说“又一个 Agent 会写代码了”，而是在回答一个更大的问题：AI 能不能像科学家一样，记住每次试验的教训，把失败也变成下一次研究的燃料？</p>
    <div class="hero-grid">
      <div class="metric"><b>6/6</b><span>真实研究任务 held-out 最优</span></div>
      <div class="metric"><b>2.5x+</b><span>平均相对增益超过 Codex / Claude Code</span></div>
      <div class="metric"><b>86.36%</b><span>MLE-Bench Lite Any Medal</span></div>
      <div class="metric"><b>HTR</b><span>Hypothesis Tree Refinement</span></div>
    </div>
  </div>
</header>

<main class="wrap">
  <section>
    <h2>1. 论文基本信息</h2>
    <table class="info-table">
      <tr><th>论文</th><td><b>Toward Generalist Autonomous Research via Hypothesis-Tree Refinement</b><br>中文可译：通过“假设树细化”迈向通用自主研究</td></tr>
      <tr><th>作者</th><td>Jiajie Jin, Yuyang Hu, Kai Qiu, Qi Dai, Chong Luo, Guanting Dong, Xiaoxi Li, Tong Zhao, Xiaolong Ma, Gongrui Zhang, Zhirong Wu, Bei Liu, Zhengyuan Yang, Linjie Li, Lijuan Wang, Hongjin Qian, Yutao Zhu, Zhicheng Dou</td></tr>
      <tr><th>机构</th><td>论文/项目作者页显示来自 Renmin University of China 相关团队，并包含 Microsoft Research 作者；代码仓库由 RUC-NLPIR 发布。</td></tr>
      <tr><th>发布时间</th><td>arXiv 提交：2026-06-10；平台：arXiv / GitHub / 项目页</td></tr>
      <tr><th>链接</th><td><a href="https://arxiv.org/abs/2606.11926">arXiv 摘要</a> · <a href="https://arxiv.org/html/2606.11926v1">arXiv HTML</a> · <a href="https://github.com/RUC-NLPIR/Arbor">GitHub</a> · <a href="https://RUC-NLPIR.github.io/Arbor/">项目页</a></td></tr>
    </table>
  </section>

  <section>
    <h2>2. 为什么今天选它？</h2>
    <div class="grid-2">
      <div class="card">
        <h3>它把“AI 做研究”从聊天推进到系统</h3>
        <p>大多数 Agent 像一个很努力但健忘的实习生：试一次、写一段、失败了，然后在长长的对话里逐渐丢失上下文。Arbor 的关键变化是把研究过程外部化成一棵“假设树”：每个想法、实验、结果、经验都成为树上的节点。</p>
      </div>
      <div class="card">
        <h3>它强调验证，而不是自我感觉良好</h3>
        <p>论文最值得关注的不是分数，而是 dev / held-out 的纪律：日常试验可以在开发集上摸索，但真正合并改进必须经过隔离的 held-out 检查。这一点决定了它更像研究系统，而不是刷榜脚本。</p>
      </div>
    </div>
    <div class="card" style="margin-top:14px">
      <span class="tag">长期价值</span><span class="tag">AI Agent</span><span class="tag">自动化科研</span><span class="tag">实验工程</span>
      <p class="plain">如果未来 AI 真能帮人做科研、做工程优化、做产品实验，它不能只会“多试几次”。它必须会管理证据、继承经验、避免重复错误。Arbor 把这个问题讲得非常具体。</p>
    </div>
  </section>

  <section>
    <h2>3. 一句话讲透论文</h2>
    <div class="quote">Arbor 本质上是在给 AI 配一个“研究项目经理”：它让 AI 把每次试验变成可追踪的假设、证据和经验，而不是散落在聊天记录里的临时灵感。</div>
  </section>

  <section>
    <h2>4. 核心贡献拆解</h2>
    <div class="grid-3">
      <div class="card">
        <h3>提出 AO 任务形态</h3>
        <p><b>Autonomous Optimization</b> 指的是：给 AI 一个初始研究产物、目标和评测器，让它在没有逐步人工指导的情况下反复实验并改进。</p>
      </div>
      <div class="card">
        <h3>提出 HTR 假设树</h3>
        <p>每个节点记录一个假设、对应代码/产物、实验结果、提炼出的经验。它像科研笔记本，但更结构化、更适合机器读写。</p>
      </div>
      <div class="card">
        <h3>分离 Coordinator 与 Executor</h3>
        <p>Coordinator 像 PI 或产品负责人，决定研究方向；Executor 像工程师，在隔离 worktree 里实现一个想法并跑实验。</p>
      </div>
    </div>
  </section>

  <section>
    <h2>5. 工作原理：像一家小型研究公司</h2>
    <p>可以把 Arbor 想成一家只有两类员工的研究公司。老板不是每天亲自写代码，而是维护一张“我们相信什么、试过什么、证据是什么”的路线图。工程师每次只负责一个假设：改代码、跑实验、交结果。最后，只有经得起独立验证的结果才会进入主线。</p>
    <svg class="diagram" viewBox="0 0 960 360" role="img" aria-label="Arbor workflow diagram">
      <defs>
        <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#0b6f6b"/><stop offset="1" stop-color="#b9822f"/></linearGradient>
      </defs>
      <rect width="960" height="360" fill="#101a1c"/>
      <g fill="#f5fbfa" font-family="Arial, sans-serif" font-size="20" font-weight="700">
        <text x="50" y="58">研究目标</text>
        <text x="262" y="58">Coordinator</text>
        <text x="494" y="58">Executors</text>
        <text x="742" y="58">Held-out Gate</text>
      </g>
      <g stroke="url(#g)" stroke-width="4" fill="none" marker-end="url(#arrow)">
        <path d="M160 115 C210 115 220 115 255 115"/>
        <path d="M390 115 C435 115 450 88 495 88"/>
        <path d="M390 115 C435 115 450 142 495 142"/>
        <path d="M390 115 C435 115 450 196 495 196"/>
        <path d="M650 142 C690 142 705 142 745 142"/>
        <path d="M815 215 C760 290 378 292 330 210"/>
      </g>
      <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
          <path d="M0,0 L0,6 L9,3 z" fill="#8bbfbb"/>
        </marker>
      </defs>
      <g>
        <rect x="42" y="84" width="126" height="70" rx="8" fill="#17272a" stroke="#2e4649"/>
        <text x="63" y="126" fill="#dcefed" font-size="16">目标 + 评测器</text>
        <rect x="255" y="78" width="142" height="92" rx="8" fill="#122f31" stroke="#187a75"/>
        <text x="276" y="112" fill="#e9fffb" font-size="16">维护假设树</text>
        <text x="276" y="142" fill="#bfe4df" font-size="14">选择/剪枝/合并</text>
        <rect x="500" y="56" width="150" height="58" rx="8" fill="#20282a" stroke="#476568"/>
        <rect x="500" y="124" width="150" height="58" rx="8" fill="#20282a" stroke="#476568"/>
        <rect x="500" y="192" width="150" height="58" rx="8" fill="#20282a" stroke="#476568"/>
        <text x="527" y="91" fill="#f3fbfa" font-size="15">实验 A</text>
        <text x="527" y="159" fill="#f3fbfa" font-size="15">实验 B</text>
        <text x="527" y="227" fill="#f3fbfa" font-size="15">实验 C</text>
        <rect x="746" y="92" width="154" height="96" rx="8" fill="#302617" stroke="#b9822f"/>
        <text x="772" y="129" fill="#fff6e8" font-size="16">独立验证</text>
        <text x="772" y="160" fill="#f0d8ae" font-size="14">通过才进入主线</text>
      </g>
      <text x="302" y="322" fill="#9bb7b3" font-size="15">失败也会回流成经验：不是浪费，而是下一轮假设的边界条件。</text>
    </svg>
  </section>

  <section>
    <h2>6. 关键术语解释</h2>
    <table class="data-table">
      <tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr>
      <tr><td>Hypothesis Tree</td><td>把假设、产物、证据、洞见组织成持久树结构。</td><td>像一张会长大的科研路线图，记录“我们为什么走到这里”。</td></tr>
      <tr><td>Held-out Evaluation</td><td>与日常探索隔离的最终验证集或评测流程。</td><td>平时练习题可以反复做，但期末考试不能提前看。</td></tr>
      <tr><td>Coordinator</td><td>长期运行、管理全局状态与搜索策略的 Agent。</td><td>研究主管，决定下一步试什么，不亲自做所有实验。</td></tr>
      <tr><td>Executor</td><td>短期执行单个假设、修改产物并返回证据的 Agent。</td><td>实验工程师，拿一个明确任务去跑实验。</td></tr>
      <tr><td>Autonomous Optimization</td><td>Agent 在目标、评测器和预算下自主改进初始产物。</td><td>给 AI 一个项目和评分标准，让它自己迭代改好。</td></tr>
    </table>
  </section>

  <section>
    <h2>7. 实验结果怎么读</h2>
    <p>这篇论文的结果不要只看“谁分数高”。更重要的是：它比较的是同一任务接口、同一资源预算下，结构化研究流程是否比普通单 Agent 更能积累收益。</p>
    <table class="data-table">
      <tr><th>任务</th><th>初始</th><th>Codex</th><th>Claude Code</th><th>Arbor</th><th>意味着什么</th></tr>
      <tr><td>Terminal-Bench 2.0</td><td>69.81</td><td>73.59</td><td>71.70</td><td><b>77.36</b></td><td>在终端工程任务中，结构化实验比一次性修补更稳。</td></tr>
      <tr><td>BrowseComp</td><td>45.33</td><td>50.00</td><td>53.33</td><td><b>67.67</b></td><td>搜索 Agent 的关键不是多搜，而是保存证据、合并线索。</td></tr>
      <tr><td>Math-Reasoning Data</td><td>1.04</td><td>6.25</td><td>8.33</td><td><b>20.83</b></td><td>数据合成任务尤其吃“反复试错后沉淀规则”。</td></tr>
      <tr><td>MLE-Bench Lite</td><td colspan="3">GPT-5.5 条件下比较</td><td><b>86.36% Any Medal</b></td><td>说明同一套控制器可迁移到更像 Kaggle 的机器学习研究场景。</td></tr>
    </table>
    <div class="card" style="margin-top:14px">
      <h3>一个直觉判断</h3>
      <p>Arbor 的优势不是“脑子突然更聪明”，而是“组织方式更像真正团队”。它把局部发现变成全局记忆，把失败变成约束，把验证变成准入门槛。</p>
    </div>
  </section>

  <section>
    <h2>8. 局限性与风险</h2>
    <div class="grid-2">
      <div class="card warn">
        <h3>它仍依赖好评测器</h3>
        <p>如果目标本身写错、指标太窄、测试集不能代表真实世界，Arbor 也可能把错误方向优化得很漂亮。</p>
      </div>
      <div class="card warn">
        <h3>成本和基础设施更重</h3>
        <p>多分支实验、隔离 worktree、重复验证都需要时间、算力和工程管理。它不适合“今天随手问一下”的轻量任务。</p>
      </div>
      <div class="card warn">
        <h3>高层创意仍可能卡住</h3>
        <p>论文也承认，当进步需要全新的问题表述，而不是沿着已有树枝细化时，系统仍依赖模型本身和人类定义的搜索空间。</p>
      </div>
      <div class="card warn">
        <h3>安全边界需要同步提高</h3>
        <p>越会长期实验的 Agent，越需要权限隔离、审计、预算控制和人工准入。否则“自动研究”也可能变成自动扩大错误。</p>
      </div>
    </div>
  </section>

  <section>
    <h2>9. 产业影响分析</h2>
    <table class="data-table">
      <tr><th>受益者</th><th>可能变化</th></tr>
      <tr><td>AI 工程团队</td><td>把提示词调参、数据清洗、评测 harness 优化变成可持续实验流程，而不是靠个人经验。</td></tr>
      <tr><td>创业公司</td><td>小团队可用 Agent 承担一部分“实验工程师”角色，降低试错组织成本。</td></tr>
      <tr><td>科研机构</td><td>AI 不只是文献助手，而可能成为长期项目中的实验执行与证据管理层。</td></tr>
      <tr><td>平台型 Agent 公司</td><td>竞争焦点会从“单次回答质量”转向“长期目标管理、验证纪律和可审计研究状态”。</td></tr>
    </table>
  </section>

  <section>
    <h2>10. 延伸阅读</h2>
    <ul class="source-list">
      <li><a href="https://arxiv.org/abs/2606.11926">原论文摘要：Toward Generalist Autonomous Research via Hypothesis-Tree Refinement</a></li>
      <li><a href="https://arxiv.org/html/2606.11926v1">arXiv HTML 全文</a></li>
      <li><a href="https://github.com/RUC-NLPIR/Arbor">Arbor GitHub 仓库</a></li>
      <li><a href="https://RUC-NLPIR.github.io/Arbor/">Arbor 官方项目页</a></li>
      <li><a href="https://venturebeat.com/orchestration/new-ai-optimization-framework-beats-claude-code-and-codex-by-2-5x-on-the-same-compute-budget">VentureBeat 报道：AI optimization framework beats Claude Code and Codex by 2.5x</a></li>
    </ul>
  </section>

  <section>
    <h2>11. 引用来源</h2>
    <div class="card">
      <p><b>主要英文来源：</b>arXiv 摘要页、arXiv HTML 全文、RUC-NLPIR/Arbor GitHub README、Arbor 官方项目页、VentureBeat 报道链接。</p>
      <p><b>本报告处理方式：</b>未直接截图论文图，而是用中文重新设计“假设树 + Coordinator/Executor + held-out gate”图示，并用表格解释实验结果含义。</p>
      <p class="note">视觉资产使用内置图片生成工具生成，报告中已嵌入为 base64，便于邮件附件独立打开。</p>
    </div>
  </section>

  <div class="footer">生成时间：2026-06-22 07:00 CST · 文件：AI-Daily-Paper-Arbor-2026-06-22-embedded.html</div>
</main>
</body>
</html>
"""

html = html.replace("{{HERO_DATA}}", hero_data)

EMAIL_BODY.write_text(
    """<!doctype html><html lang="zh-CN"><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',Arial,sans-serif;line-height:1.7;color:#162022">
<p>今天精选的论文是 <b>Toward Generalist Autonomous Research via Hypothesis-Tree Refinement</b>。</p>
<p>一句话推荐理由：它把 AI Agent 从“一次性尝试”推进到“像研究团队一样积累假设、实验和证据”的长期研究系统。</p>
<p>这可能是自动化科研、AI 工程优化和 Agent 产品形态的重要方向。附件为中文深度拆解 HTML 报告，适合非技术读者阅读。</p>
</body></html>
""",
    encoding="utf-8",
)
REPORT.write_text(html, encoding="utf-8")
print(REPORT)
print(EMAIL_BODY)
