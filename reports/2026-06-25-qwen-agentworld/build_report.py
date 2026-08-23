from __future__ import annotations

import base64
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "AI-Daily-Paper-Qwen-AgentWorld-2026-06-25.html"
EMAIL_BODY = ROOT / "email-body.html"
EMAIL_SUBJECT = ROOT / "email_subject.txt"
SOURCES = ROOT / "sources.md"
RUN_SUMMARY = ROOT / "run_summary.md"
HERO = ROOT / "qwen-agentworld-hero.png"


def image_data_uri(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


hero_uri = image_data_uri(HERO)
now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S%z")

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI每日论文精选 | Qwen-AgentWorld</title>
  <style>
    :root {{
      color-scheme: light dark;
      --ink:#17201d;
      --muted:#5b6762;
      --line:#dbe2df;
      --paper:#f8faf8;
      --card:#ffffff;
      --soft:#edf5f1;
      --accent:#0f766e;
      --accent2:#1f6feb;
      --warn:#9a4b22;
      --dark:#111816;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0;
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Arial,sans-serif;
      line-height:1.72;
      background:var(--paper);
      color:var(--ink);
      letter-spacing:0;
    }}
    a {{ color:var(--accent2); text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    .wrap {{ max-width:980px; margin:0 auto; padding:26px 18px 56px; }}
    .hero {{
      display:grid;
      grid-template-columns:1.05fr .95fr;
      gap:26px;
      align-items:center;
      min-height:520px;
      padding:30px 0 20px;
      border-bottom:1px solid var(--line);
    }}
    .eyebrow {{ font-size:13px; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:.08em; }}
    h1 {{ font-size:44px; line-height:1.08; margin:14px 0 16px; letter-spacing:0; }}
    h2 {{ font-size:26px; line-height:1.22; margin:42px 0 14px; letter-spacing:0; }}
    h3 {{ font-size:18px; line-height:1.35; margin:18px 0 8px; letter-spacing:0; }}
    p {{ margin:10px 0; }}
    .subtitle {{ font-size:19px; color:var(--muted); max-width:760px; }}
    .hero img {{ width:100%; border-radius:8px; display:block; border:1px solid var(--line); }}
    .meta-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:18px; }}
    .pill {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px 12px; }}
    .pill b {{ display:block; font-size:12px; color:var(--muted); font-weight:650; }}
    .pill span {{ display:block; font-size:15px; font-weight:750; }}
    .section {{ padding:8px 0 0; }}
    .cards {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:18px 0; }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:16px; }}
    .card strong {{ display:block; font-size:16px; margin-bottom:6px; }}
    .callout {{ background:#10231f; color:#f2fbf7; border-radius:8px; padding:18px; margin:18px 0; }}
    .callout b {{ color:#9de4d3; }}
    .risk {{ background:#fff8ed; border-color:#e8cba5; }}
    .quote {{ font-size:24px; line-height:1.38; font-weight:800; border-left:5px solid var(--accent); padding:10px 0 10px 16px; margin:20px 0; }}
    table {{ width:100%; border-collapse:collapse; margin:16px 0 22px; background:var(--card); border:1px solid var(--line); border-radius:8px; overflow:hidden; display:table; }}
    th,td {{ padding:11px 10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; font-size:14px; }}
    th {{ background:#eaf2ee; font-weight:800; color:#26332f; }}
    tr:last-child td {{ border-bottom:0; }}
    .num {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
    .svgbox {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px; margin:18px 0; overflow:auto; }}
    svg {{ max-width:100%; height:auto; display:block; }}
    .term-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:12px; }}
    .term {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:14px; }}
    .term b {{ color:var(--accent); }}
    ul {{ padding-left:22px; }}
    .small {{ color:var(--muted); font-size:13px; }}
    .footer {{ margin-top:42px; padding-top:18px; border-top:1px solid var(--line); color:var(--muted); font-size:13px; }}
    @media (max-width:760px) {{
      .wrap {{ padding:18px 14px 44px; }}
      .hero {{ grid-template-columns:1fr; min-height:0; }}
      h1 {{ font-size:34px; }}
      h2 {{ font-size:23px; }}
      .meta-grid,.cards,.term-grid {{ grid-template-columns:1fr; }}
      table {{ display:block; overflow-x:auto; }}
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --ink:#e7efe9; --muted:#aebbb5; --line:#293630; --paper:#0f1412; --card:#151d19; --soft:#18261f; }}
      th {{ background:#1d2c25; color:#e7efe9; }}
      .risk {{ background:#2a2117; border-color:#684420; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <div>
        <div class="eyebrow">AI每日论文精选 · 2026-06-25</div>
        <h1>Qwen-AgentWorld：把 Agent 放进“可学习的模拟世界”</h1>
        <p class="subtitle">今日论文不是在教 AI 多会聊天，而是在解决一个更根本的问题：如果 AI 要长期做事，它能不能先学会“这个世界会怎样回应我的行动”？</p>
        <div class="meta-grid">
          <div class="pill"><b>论文</b><span>Qwen-AgentWorld</span></div>
          <div class="pill"><b>平台</b><span>arXiv cs.CL</span></div>
          <div class="pill"><b>机构</b><span>Qwen Team</span></div>
          <div class="pill"><b>发布时间</b><span>2026-06-23</span></div>
        </div>
      </div>
      <img src="{hero_uri}" alt="Qwen-AgentWorld 可视化题图：AI Agent 在模拟环境中练习网页、终端、代码、API 与系统操作">
    </section>

    <section class="section">
      <h2>1. 标题区</h2>
      <div class="card">
        <p><b>英文标题：</b>Qwen-AgentWorld: Language World Models for General Agents</p>
        <p><b>中文标题：</b>Qwen-AgentWorld：面向通用 Agent 的语言世界模型</p>
        <p><b>作者：</b>Qwen Team</p>
        <p><b>机构：</b>Qwen / Alibaba 相关研究团队</p>
        <p><b>论文链接：</b><a href="https://arxiv.org/abs/2606.24597">https://arxiv.org/abs/2606.24597</a></p>
        <p><b>官方资源：</b><a href="https://github.com/QwenLM/Qwen-AgentWorld">GitHub</a> · <a href="https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B">Hugging Face 模型</a> · <a href="https://qwen.ai/blog?id=qwen-agentworld">官方博客</a></p>
      </div>
    </section>

    <section class="section">
      <h2>2. 为什么今天选它？</h2>
      <div class="callout"><b>核心判断：</b>如果 2024-2026 年的 Agent 热潮主要是在研究“AI 怎么选工具、怎么规划任务”，这篇论文开始补另半张拼图：AI 能不能先预测工具、网页、终端、手机界面和操作系统会怎样回应它。</div>
      <div class="cards">
        <div class="card"><strong>行业意义</strong>Agent 训练最贵的地方不只是模型推理，而是每一步都要和真实环境互动。世界模型让 AI 可以先在模拟环境里大量练习。</div>
        <div class="card"><strong>技术突破</strong>它把 MCP、搜索、终端、软件工程、Android、Web、OS 七类环境统一成“动作 -> 观察”的语言预测问题。</div>
        <div class="card"><strong>长期价值</strong>今天的聊天模型像会答题的学生；未来的 Agent 更像实习生。实习生要进步，必须知道“我做这一步后，系统会怎么变”。</div>
      </div>
      <p>它重要，不是因为分数又高了一点，而是因为它把 Agent 的训练范式从“只训练会行动的模型”，推进到“同时训练懂环境反应的模型”。这更接近自动驾驶里的仿真器：车不能只在真实马路上撞出来经验，Agent 也不能只在真实网页、真实账号、真实代码仓库里试错。</p>
    </section>

    <section class="section">
      <h2>3. 一句话讲透论文</h2>
      <div class="quote">这篇论文本质上是在给 AI Agent 建一个“虚拟练功房”：它每做一步，模型都能预测环境下一秒会怎样变化。</div>
    </section>

    <section class="section">
      <h2>4. 核心贡献拆解</h2>
      <table>
        <thead><tr><th>贡献</th><th>白话解释</th><th>为什么更好</th></tr></thead>
        <tbody>
          <tr><td>语言世界模型</td><td>把网页、终端、工具调用、手机界面都看成一种“可用语言描述的世界”。</td><td>不同环境可以共用一套训练框架，减少碎片化。</td></tr>
          <tr><td>七域统一</td><td>MCP、Search、Terminal、SWE、Android、Web、OS 放到同一个模型里。</td><td>Agent 不再只会一个小场景，而能学到跨环境的交互规律。</td></tr>
          <tr><td>三阶段训练</td><td>CPT 注入环境知识，SFT 激活“预测下一状态”的思维，RL 打磨模拟质量。</td><td>不是事后微调一个聊天模型，而是从训练目标上就让它学世界变化。</td></tr>
          <tr><td>AgentWorldBench</td><td>用 5 个前沿模型在 9 个成熟基准上的真实交互轨迹做评测。</td><td>评的不是作文好不好，而是预测出来的环境响应是否像真的。</td></tr>
          <tr><td>Sim RL 应用</td><td>用 Qwen-AgentWorld 当训练场，让 Agent 在 4000 个模拟 OpenClaw 环境里练习。</td><td>模拟训练在 Claw-Eval 和 QwenClawBench 上分别带来 +4.3 和 +7.1 提升。</td></tr>
        </tbody>
      </table>
    </section>

    <section class="section">
      <h2>5. 工作原理：把世界压成“动作与反馈”</h2>
      <p>想象你在教一个新人使用公司系统。新人点了“提交报销”，系统可能返回成功、报错、要求补充发票，或者跳到审批页。传统 Agent 训练更关注“新人下一步点哪里”。Qwen-AgentWorld 关注的是另一件事：<b>新人点完以后，系统应该出现什么反应。</b></p>
      <div class="svgbox">
        <svg viewBox="0 0 920 320" role="img" aria-label="Qwen-AgentWorld 工作流图">
          <defs>
            <marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#0f766e"/></marker>
          </defs>
          <rect x="20" y="30" width="180" height="90" rx="8" fill="#eaf2ee" stroke="#9fc8bc"/>
          <text x="110" y="66" text-anchor="middle" font-size="18" font-weight="700" fill="#17201d">历史状态</text>
          <text x="110" y="94" text-anchor="middle" font-size="13" fill="#4b5b55">网页/终端/工具/OS</text>
          <rect x="250" y="30" width="180" height="90" rx="8" fill="#f6f8ff" stroke="#b9c8f2"/>
          <text x="340" y="66" text-anchor="middle" font-size="18" font-weight="700" fill="#17201d">Agent 动作</text>
          <text x="340" y="94" text-anchor="middle" font-size="13" fill="#4b5b55">点击/搜索/命令/API</text>
          <rect x="480" y="30" width="190" height="90" rx="8" fill="#10231f" stroke="#0f766e"/>
          <text x="575" y="66" text-anchor="middle" font-size="18" font-weight="700" fill="#f2fbf7">Qwen-AgentWorld</text>
          <text x="575" y="94" text-anchor="middle" font-size="13" fill="#9de4d3">预测下一步环境反馈</text>
          <rect x="720" y="30" width="180" height="90" rx="8" fill="#fff8ed" stroke="#e2b478"/>
          <text x="810" y="66" text-anchor="middle" font-size="18" font-weight="700" fill="#17201d">模拟观察</text>
          <text x="810" y="94" text-anchor="middle" font-size="13" fill="#4b5b55">像真实环境一样回应</text>
          <line x1="200" y1="75" x2="248" y2="75" stroke="#0f766e" stroke-width="3" marker-end="url(#arrow)"/>
          <line x1="430" y1="75" x2="478" y2="75" stroke="#0f766e" stroke-width="3" marker-end="url(#arrow)"/>
          <line x1="670" y1="75" x2="718" y2="75" stroke="#0f766e" stroke-width="3" marker-end="url(#arrow)"/>
          <path d="M810 120 C790 210 190 210 110 120" fill="none" stroke="#0f766e" stroke-width="3" stroke-dasharray="8 7" marker-end="url(#arrow)"/>
          <text x="460" y="238" text-anchor="middle" font-size="15" fill="#4b5b55">把模拟反馈接回训练循环，Agent 可以在低风险环境中反复练习</text>
        </svg>
      </div>
      <h3>三阶段训练像什么？</h3>
      <ul>
        <li><b>CPT：</b>像先读完公司系统手册，知道常见界面、工具、报错、权限、文件结构。</li>
        <li><b>SFT：</b>像看老师示范：“如果用户运行这个命令，终端下一行应该是什么”。</li>
        <li><b>RL：</b>像实战演练后复盘，奖励更真实、更一致、更完整的环境回应。</li>
      </ul>
    </section>

    <section class="section">
      <h2>6. 关键术语解释</h2>
      <div class="term-grid">
        <div class="term"><b>World Model</b><p>专业解释：预测环境状态转移的模型。</p><p>白话：你做一个动作，它能猜出世界接下来会怎样变。</p></div>
        <div class="term"><b>Language World Model</b><p>专业解释：用语言表示状态、动作、观察的世界模型。</p><p>白话：不是生成视频，而是用文本模拟终端、网页、工具返回值和 UI 变化。</p></div>
        <div class="term"><b>Environment Trajectory</b><p>专业解释：一串动作与环境观察组成的交互轨迹。</p><p>白话：像屏幕录像的文字版：点了什么、系统回了什么。</p></div>
        <div class="term"><b>Sim RL</b><p>专业解释：在模拟环境中进行强化学习。</p><p>白话：先在虚拟训练场练，不直接拿真实系统冒险。</p></div>
        <div class="term"><b>MCP</b><p>专业解释：模型上下文协议，让模型以结构化方式调用外部工具。</p><p>白话：给 AI 接上不同软件工具的插座。</p></div>
        <div class="term"><b>Long Context</b><p>专业解释：模型处理很长历史输入的能力。</p><p>白话：Agent 做了 40 步后，仍能记得第 3 步造成了什么影响。</p></div>
      </div>
    </section>

    <section class="section">
      <h2>7. 实验结果解读</h2>
      <table>
        <thead><tr><th>模型</th><th>MCP</th><th>Search</th><th>Terminal</th><th>SWE</th><th>Android</th><th>Web</th><th>OS</th><th>总分</th></tr></thead>
        <tbody>
          <tr><td>GPT-5.4</td><td class="num">70.10</td><td class="num">37.26</td><td class="num">53.69</td><td class="num">66.29</td><td class="num">60.00</td><td class="num">51.80</td><td class="num">68.58</td><td class="num">58.25</td></tr>
          <tr><td>Claude Opus 4.8</td><td class="num">54.93</td><td class="num">35.14</td><td class="num">59.18</td><td class="num">64.10</td><td class="num">61.50</td><td class="num">54.66</td><td class="num">66.62</td><td class="num">56.59</td></tr>
          <tr><td>Qwen3.5-35B-A3B</td><td class="num">57.87</td><td class="num">25.98</td><td class="num">46.13</td><td class="num">47.58</td><td class="num">53.18</td><td class="num">47.10</td><td class="num">56.27</td><td class="num">47.73</td></tr>
          <tr><td><b>Qwen-AgentWorld-35B-A3B</b></td><td class="num">64.79</td><td class="num">36.69</td><td class="num">53.96</td><td class="num">65.63</td><td class="num">58.17</td><td class="num">49.55</td><td class="num">65.92</td><td class="num"><b>56.39</b></td></tr>
          <tr><td><b>Qwen-AgentWorld-397B-A17B</b></td><td class="num">68.24</td><td class="num">37.82</td><td class="num">57.73</td><td class="num">68.49</td><td class="num">60.20</td><td class="num">50.98</td><td class="num">67.89</td><td class="num"><b>58.71</b></td></tr>
        </tbody>
      </table>
      <p>最值得看的是两组对比。第一，35B-A3B 版本从普通 Qwen3.5 的 47.73 提到 56.39，说明“专门学环境响应”确实带来能力增益。第二，397B-A17B 总分 58.71，高于论文报告中的 GPT-5.4 58.25。这不代表它是更强聊天模型，而是说明在“模拟环境反馈”这个专门任务上，训练目标比通用智力更关键。</p>
      <table>
        <thead><tr><th>应用实验</th><th>基线</th><th>加入 Qwen-AgentWorld 模拟训练后</th><th>含义</th></tr></thead>
        <tbody>
          <tr><td>OpenClaw 环境扩展</td><td>Claw-Eval 65.4 / QwenClawBench 47.9</td><td>69.7 / 55.0</td><td>模拟器能把少量真实轨迹扩成 4000 个训练环境。</td></tr>
          <tr><td>MCP 可控模拟</td><td>Tool Decathlon 32.4 / MCPMark 21.5</td><td>36.1 / 33.8</td><td>故意制造分页、错误、部分失败，可训练更稳的工具 Agent。</td></tr>
          <tr><td>虚构搜索世界</td><td>WideSearch F1 Item 34.02</td><td>50.31</td><td>让 Agent 在完全虚构但自洽的世界里学会搜索，而不是背答案。</td></tr>
        </tbody>
      </table>
    </section>

    <section class="section">
      <h2>8. 局限性与问题</h2>
      <div class="cards">
        <div class="card risk"><strong>模拟不等于真实</strong>世界模型会犯错。模拟器一旦产生系统性偏差，Agent 可能学会适应假环境，而不是真实环境。</div>
        <div class="card risk"><strong>初始状态很关键</strong>论文也强调 state 是瓶颈。没有足够详细的文件、权限、账号、工具状态，后续模拟会越来越漂。</div>
        <div class="card risk"><strong>算力门槛高</strong>35B-A3B 虽已开源，但建议至少 128K 上下文；397B-A17B 更接近研究级/平台级能力。</div>
      </div>
      <p>另一个隐含风险是安全：如果世界模型能高质量模拟真实软件和工具反馈，它也可能被用来训练更强的自动化攻击 Agent。因此未来需要把权限控制、审计、沙箱和任务边界设计进训练平台，而不是只追求分数。</p>
    </section>

    <section class="section">
      <h2>9. 产业影响分析</h2>
      <table>
        <thead><tr><th>对象</th><th>可能受益</th><th>可能被冲击</th></tr></thead>
        <tbody>
          <tr><td>Agent 平台公司</td><td>可用模拟环境低成本扩展训练和回归测试。</td><td>只做薄封装工具调用的产品更难形成护城河。</td></tr>
          <tr><td>企业软件与自动化</td><td>能先在模拟 CRM、ERP、工单系统里训练流程 Agent。</td><td>真实系统日志和交互数据会变成关键资产。</td></tr>
          <tr><td>AI 基础设施</td><td>需要环境录制、状态快照、仿真评测、可控扰动、长上下文推理服务。</td><td>传统只看单轮问答的评测会越来越不够用。</td></tr>
          <tr><td>安全与合规</td><td>可以用可控模拟暴露 Agent 弱点，做红队训练。</td><td>同样能力可能降低滥用门槛。</td></tr>
        </tbody>
      </table>
      <p>如果这个方向继续成熟，AI 竞争可能从“谁的模型会回答问题”转向“谁拥有最真实、最多样、最可控的任务世界”。这和自动驾驶类似：车企比拼的不只是车，也包括仿真器、道路数据和闭环训练系统。</p>
    </section>

    <section class="section">
      <h2>10. 延伸阅读</h2>
      <ul>
        <li><a href="https://arxiv.org/abs/2606.24597">Qwen-AgentWorld arXiv 论文页</a></li>
        <li><a href="https://arxiv.org/html/2606.24597v1">arXiv HTML 全文</a></li>
        <li><a href="https://github.com/QwenLM/Qwen-AgentWorld">Qwen-AgentWorld GitHub 仓库</a></li>
        <li><a href="https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B">Qwen-AgentWorld-35B-A3B 模型卡</a></li>
        <li><a href="https://huggingface.co/datasets/Qwen/AgentWorldBench">AgentWorldBench 数据集</a></li>
        <li><a href="https://huggingface.co/papers/2606.24597">Hugging Face Papers 页面</a></li>
        <li><a href="https://news.ycombinator.com/item?id=48654351">Hacker News 讨论</a></li>
      </ul>
    </section>

    <section class="section">
      <h2>11. 引用来源</h2>
      <ol>
        <li>Qwen Team. “Qwen-AgentWorld: Language World Models for General Agents.” arXiv:2606.24597v1, 2026-06-23.</li>
        <li>QwenLM/Qwen-AgentWorld GitHub README, release note dated 2026-06-24.</li>
        <li>Qwen-AgentWorld-35B-A3B Hugging Face model card.</li>
        <li>Qwen official blog page: Qwen-AgentWorld.</li>
        <li>Hugging Face Papers page for arXiv:2606.24597.</li>
      </ol>
      <p class="small">说明：本文为中文解构与重构，不复刻原论文图表；所有流程图、类比和产业分析均为面向普通读者的解释性重绘。</p>
    </section>

    <div class="footer">生成时间：{now} · 本报告为《AI每日论文精选》自动化产物 · 主题：语言世界模型与 Agent 模拟训练</div>
  </main>
</body>
</html>
"""

email_body = """<!doctype html><html lang="zh-CN"><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',Arial,sans-serif;line-height:1.7;color:#17201d">
<p>今天精选的论文是 <b>Qwen-AgentWorld: Language World Models for General Agents</b>。</p>
<p>一句话推荐理由：它把 Agent 训练从“学会下一步怎么做”，推进到“先学会环境会怎样回应”，这可能是通用 Agent 走向真实生产力系统的重要基础设施。</p>
<p>附件为中文深度拆解 HTML 报告，包含论文信息、核心贡献、工作原理图解、实验结果、局限性和产业影响分析，适合非技术读者阅读。</p>
</body></html>
"""

sources = """# Sources

- arXiv abstract: https://arxiv.org/abs/2606.24597
- arXiv HTML: https://arxiv.org/html/2606.24597v1
- arXiv PDF: https://arxiv.org/pdf/2606.24597
- Qwen-AgentWorld GitHub: https://github.com/QwenLM/Qwen-AgentWorld
- Qwen official blog: https://qwen.ai/blog?id=qwen-agentworld
- Hugging Face model: https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B
- Hugging Face dataset: https://huggingface.co/datasets/Qwen/AgentWorldBench
- Hugging Face Papers: https://huggingface.co/papers/2606.24597
- Hacker News discussion: https://news.ycombinator.com/item?id=48654351
"""

summary = f"""# Run summary

- Selected paper: Qwen-AgentWorld: Language World Models for General Agents (arXiv:2606.24597).
- Reason: strongest long-term signal among current candidates; reframes Agent training around language world models and simulator-based RL.
- Artifact: {REPORT}
- Email body: {EMAIL_BODY}
- Key facts: 7 domains; more than 10M interaction trajectories; AgentWorldBench has 2,170 evaluation samples; open-source 35B-A3B model and benchmark; official result reports 397B-A17B overall 58.71 on AgentWorldBench.
- Sources: arXiv HTML/PDF, Qwen official blog, GitHub README, Hugging Face model card, Hugging Face Papers, Hacker News discussion.
- Generated image: {HERO}
- Generated at: {now}
"""

REPORT.write_text(html, encoding="utf-8")
EMAIL_BODY.write_text(email_body, encoding="utf-8")
EMAIL_SUBJECT.write_text("【AI每日论文精选】AI Agent 的虚拟练功房来了\n", encoding="utf-8")
SOURCES.write_text(sources, encoding="utf-8")
RUN_SUMMARY.write_text(summary, encoding="utf-8")
print(REPORT)
