from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
HTML = BASE / "2026-07-06_EvaluationMetrics（评估指标）.html"
PDF = BASE / "2026-07-06_EvaluationMetrics（评估指标）.pdf"
PREVIEW = BASE / "html_preview.png"
EMAIL_SUBJECT = BASE / "email_subject.txt"
EMAIL_BODY = BASE / "email_body.txt"
SOURCES = BASE / "sources.md"


TITLE = "Evaluation Metrics 评估指标"
SUBTITLE = "为什么 AI 不能只看“答得像不像”？"
CORE_SENTENCE = "评估指标的本质，是把“感觉还行”变成一组可比较、可复盘、可改进的证据。"


SECTIONS = [
    {
        "id": "why",
        "title": "为什么这个概念重要？",
        "body": """
<p>很多人判断 AI 好不好，第一反应是：“它这次回答得像不像人？” 但真实产品不能只靠感觉。一个客服 AI 可能语气很自然，却漏掉了最关键的赔付条件；一个 AI 搜索可能引用了来源，却没有真正回答用户的问题；一个 Agent 可能步骤看起来完整，却把错误参数传给了工具。</p>
<p>评估指标要解决的，就是把这些模糊感受变成可观察的信号。它不只问“答对了吗”，还会问：漏掉了多少？有没有编造？格式有没有合规？用户等了多久？一次任务花了多少钱？失败案例集中在哪些场景？</p>
<div class="insight"><b>它解决的问题：</b>让团队知道 AI 系统到底哪里好、哪里坏、改动后有没有真的变好，而不是只凭几次演示和主观印象做判断。</div>
<p>这也是 AI 行业离不开它的原因。RAG 让 AI 会查资料，结构化输出让 AI 能交付数据，工具调用让 AI 能做事；评估指标则告诉我们：这些能力在真实任务里是否可靠、可控、值得上线。</p>
""",
    },
    {
        "id": "analogy",
        "title": "一个直观类比：AI 的体检报告",
        "body": """
<p>想象你去体检。医生不会只看一个总分，然后说“身体 86 分，还可以”。真正有用的是一组指标：血压、血糖、心率、肝功能、睡眠、体重变化。每个指标看的是不同问题，组合起来才像一张完整地图。</p>
<p>评估 AI 也是这样。客服机器人不能只看“总体正确率”，还要看有没有漏掉高风险投诉；AI 搜索不能只看“回答流畅度”，还要看引用是否支持结论；自动化 Agent 不能只看“任务完成率”，还要看是否越权、是否重复执行、失败后能不能回滚。</p>
<p>所以评估指标不是给 AI 打一个漂亮分数，而是帮我们找到“哪里需要复查”。一个指标像体温计，多个指标组合才像体检报告。</p>
""",
        "image": "assets/evaluation_metrics_health_report.png",
        "caption": "图解 1：评估指标像 AI 的体检报告。准确率、召回率、精确率、幻觉率、延迟和成本分别检查不同问题。",
    },
    {
        "id": "how",
        "title": "工作原理（深入浅出）",
        "body": """
<p>一次靠谱的 AI 评估，通常不是打开模型随便问几句，而是按一条清晰流程走。</p>
<div class="steps">
  <div><span>1</span><b>先说清楚任务目标</b><p>例如“回答物流政策问题”“从合同里抽取付款条款”“判断用户是否需要转人工”。目标不同，指标也不同。</p></div>
  <div><span>2</span><b>准备有代表性的测试样本</b><p>不要只放简单题，也要放边界情况、容易误判的题、真实用户常问的问题。</p></div>
  <div><span>3</span><b>选择评分指标</b><p>常见指标包括正确率、召回率、精确率、幻觉率、格式通过率、延迟、成本和人工满意度。</p></div>
  <div><span>4</span><b>让系统作答并打分</b><p>打分可以由规则完成，也可以由人工完成，有时还会用另一个模型当评委，但关键样本最好有人复核。</p></div>
  <div><span>5</span><b>分析失败案例</b><p>只看平均分容易误导。真正有价值的是找出失败模式：是资料没检索到，还是提示词不清楚，还是模型编造？</p></div>
  <div><span>6</span><b>改进后重复测试</b><p>每次改提示词、模型、RAG 数据或工具逻辑，都要回归测试，确认旧问题没有回来，新问题没有出现。</p></div>
</div>
<p>这里最重要的直觉是：评估不是上线前的一次考试，而是 AI 产品的“持续体检”。因为用户问题会变、资料会更新、模型会升级、业务规则也会改变。一次通过，不等于永远可靠。</p>
""",
        "image": "assets/evaluation_loop.png",
        "caption": "图解 2：AI 应用评估闭环。上线前做离线评估，上线后继续看线上监控，并用失败案例驱动下一轮改进。",
    },
    {
        "id": "terms",
        "title": "关键术语解释",
        "body": """
<table>
  <thead><tr><th>术语</th><th>专业解释</th><th>白话解释</th></tr></thead>
  <tbody>
    <tr><td>Evaluation Metrics</td><td>用于衡量模型或 AI 应用表现的一组量化指标。</td><td>给 AI 做体检时看的各项数字。</td></tr>
    <tr><td>Test Set</td><td>用于评估系统表现的样本集合，通常不参与训练。</td><td>专门留出来考试的一套题。</td></tr>
    <tr><td>Golden Answer</td><td>人工确认或权威来源给出的参考答案。</td><td>老师手里的标准答案，但现实题目不一定只有一种写法。</td></tr>
    <tr><td>Accuracy 准确率</td><td>所有样本中答对的比例。</td><td>一百道题里答对了多少道。</td></tr>
    <tr><td>Precision 精确率</td><td>系统判断为“是”的结果中，真正为“是”的比例。</td><td>它报警的那些里面，有多少是真的。</td></tr>
    <tr><td>Recall 召回率</td><td>所有真实为“是”的样本中，被系统找出来的比例。</td><td>真正该报警的，有多少没有漏掉。</td></tr>
    <tr><td>F1 Score</td><td>综合 Precision 和 Recall 的指标，用于平衡误报和漏报。</td><td>既看“别乱报”，也看“别漏报”的折中分。</td></tr>
    <tr><td>Hallucination Rate</td><td>回答中包含无依据、编造或与来源不一致内容的比例。</td><td>AI 有没有一本正经地瞎编。</td></tr>
    <tr><td>Latency 延迟</td><td>从请求发出到结果返回的时间。</td><td>用户要等多久。</td></tr>
    <tr><td>Cost per Task</td><td>完成单个任务所消耗的模型、检索、工具和基础设施成本。</td><td>让 AI 做一件事要花多少钱。</td></tr>
    <tr><td>Model-as-Judge</td><td>用另一个模型按评分标准评价输出质量。</td><td>请一个 AI 当评卷老师，但重要题还要人抽查。</td></tr>
    <tr><td>Regression Test</td><td>改动系统后，重复旧测试以确认旧能力没有退化。</td><td>修了新问题，也要检查老问题有没有复发。</td></tr>
  </tbody>
</table>
""",
    },
    {
        "id": "case",
        "title": "一个真实应用案例",
        "body": """
<p>假设一家物流公司上线一个 AI 客服助手，用来回答“包裹为什么停在中转场”“什么情况可以赔付”“是否需要转人工”等问题。</p>
<p>如果只看“用户觉得回答像人”，系统可能很快上线。但真正的评估会拆成多项指标：</p>
<ul class="plain-list">
  <li><b>答案正确率：</b>回答是否符合最新物流政策。</li>
  <li><b>召回率：</b>高风险投诉、丢件、破损、理赔场景有没有漏掉。</li>
  <li><b>幻觉率：</b>是否编造不存在的赔付承诺或配送时间。</li>
  <li><b>引用覆盖率：</b>关键结论是否能对应到内部制度、运单轨迹或客服知识库。</li>
  <li><b>格式通过率：</b>是否能稳定输出订单号、问题类型、紧急程度、下一步动作。</li>
  <li><b>延迟和成本：</b>用户是否等得起，公司是否用得起。</li>
</ul>
<p>这组指标会告诉团队：问题不是“这个 AI 聪不聪明”，而是“它在什么场景下可靠，什么场景下必须转人工”。这比一个总分更接近真实业务。</p>
<div class="insight"><b>现实意义：</b>评估指标让 AI 从演示走向生产。没有评估，团队只是在相信模型；有了评估，团队才能持续改进系统。</div>
""",
    },
    {
        "id": "myths",
        "title": "常见误区（非常重要）",
        "body": """
<div class="myths">
  <div><b>误区一：Benchmark 分数高，产品就一定好用。</b><p>不一定。Benchmark 像统一考试，产品评估像岗位试用。真实用户、业务规则、数据质量和响应速度都会影响结果。</p></div>
  <div><b>误区二：看 Accuracy 一个指标就够了。</b><p>很多任务里，漏报比误报更危险，或者误报比漏报更贵。只看准确率可能掩盖关键风险。</p></div>
  <div><b>误区三：Model-as-Judge 完全客观。</b><p>模型评委很有用，但也会偏向流畅文字、受提示词影响、漏掉细节。高风险任务仍需要人工抽检。</p></div>
  <div><b>误区四：平均分提高，就代表系统整体更安全。</b><p>平均分可能上升，但少数关键场景变差。真实评估要看失败案例和分场景表现。</p></div>
  <div><b>误区五：评估是上线前做一次就结束。</b><p>不是。知识库会更新，用户问题会变化，模型版本会更换，所以评估要持续运行。</p></div>
  <div><b>误区六：回答越流畅，质量越高。</b><p>流畅只是表达能力，不等于事实正确、来源可靠、操作安全。</p></div>
</div>
""",
    },
    {
        "id": "summary",
        "title": "总结：3句话讲清核心认知",
        "body": """
<ol class="summary-list">
  <li>评估指标不是一个总分，而是一组帮助我们看清 AI 能力、风险、成本和体验的体检项目。</li>
  <li>不同任务要选择不同指标：问答看正确性和幻觉率，分类看精确率和召回率，Agent 还要看权限、成功率和回滚能力。</li>
  <li>好评估不是一次考试，而是持续闭环：测试、发现失败、改进系统、再测试、上线后继续监控。</li>
</ol>
""",
    },
    {
        "id": "questions",
        "title": "复习问题",
        "body": """
<div class="questions">
  <div><b>1. 为什么只看“准确率”可能会误导我们？</b><p>请用“漏报”和“误报”的区别举一个生活例子。</p></div>
  <div><b>2. 一个 AI 搜索助手回答得很流畅，为什么还要检查幻觉率和引用覆盖率？</b><p>提示：区分表达顺滑和事实可靠。</p></div>
  <div><b>3. 如果你要评估一个能自动填写报销单的 AI Agent，你会选择哪 4 个指标？为什么？</b><p>请同时考虑正确性、权限、安全和成本。</p></div>
</div>
""",
    },
]


SOURCES_TEXT = """# Sources

- OpenAI Platform Docs, Evals: https://developers.openai.com/api/docs/guides/evals
- OpenAI Platform Docs, Evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- Google Machine Learning Crash Course, Classification: Accuracy, recall, precision, and related metrics: https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall
- scikit-learn User Guide, Model evaluation: https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn API Reference, precision_recall_fscore_support: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
"""


CSS = """
:root {
  --ink: #0f172a;
  --muted: #475569;
  --soft: #f8fafc;
  --line: #dbeafe;
  --blue: #2563eb;
  --cyan: #0891b2;
  --green: #059669;
  --amber: #d97706;
  --red: #dc2626;
  --paper: #ffffff;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  color: var(--ink);
  background: #edf4f8;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  line-height: 1.75;
}

.page {
  max-width: 1120px;
  margin: 0 auto;
  background: var(--paper);
  box-shadow: 0 22px 80px rgba(15, 23, 42, 0.14);
}

.cover {
  min-height: 760px;
  padding: 72px 74px 42px;
  color: #fff;
  background:
    linear-gradient(120deg, rgba(15, 23, 42, 0.96), rgba(8, 47, 73, 0.94)),
    radial-gradient(circle at 74% 22%, rgba(45, 212, 191, 0.25), transparent 34%),
    radial-gradient(circle at 20% 72%, rgba(245, 158, 11, 0.18), transparent 36%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.kicker {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #a5f3fc;
  font-size: 15px;
  letter-spacing: 0;
  font-weight: 700;
}

.kicker::before {
  content: "";
  width: 32px;
  height: 2px;
  background: #22d3ee;
}

h1 {
  margin: 56px 0 18px;
  font-size: 62px;
  line-height: 1.08;
  letter-spacing: 0;
}

.subtitle {
  max-width: 820px;
  margin: 0;
  color: #dbeafe;
  font-size: 28px;
  line-height: 1.45;
  font-weight: 650;
}

.core {
  max-width: 860px;
  margin-top: 44px;
  padding: 24px 28px;
  border: 1px solid rgba(165, 243, 252, 0.38);
  background: rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  font-size: 22px;
}

.cover-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-top: 54px;
}

.cover-chip {
  padding: 16px 18px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.09);
  border: 1px solid rgba(226, 232, 240, 0.16);
}

.cover-chip b {
  display: block;
  color: #fff;
  margin-bottom: 4px;
}

.cover-chip span {
  color: #cbd5e1;
  font-size: 14px;
}

.meta {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  padding-top: 48px;
  color: #cbd5e1;
  font-size: 15px;
}

.content {
  padding: 48px 74px 82px;
}

.toc {
  margin: 0 0 46px;
  padding: 28px 30px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #f8fbff;
}

.toc h2 {
  margin: 0 0 16px;
  font-size: 24px;
}

.toc ol {
  margin: 0;
  padding-left: 22px;
  columns: 2;
  column-gap: 44px;
}

.toc li { break-inside: avoid; margin: 6px 0; }

.toc a {
  color: var(--ink);
  text-decoration: none;
  border-bottom: 1px solid rgba(37, 99, 235, 0.22);
}

section {
  padding: 38px 0 8px;
  border-top: 1px solid #e5edf7;
}

h2 {
  margin: 0 0 20px;
  font-size: 34px;
  line-height: 1.25;
  letter-spacing: 0;
}

p {
  margin: 13px 0;
  font-size: 18px;
}

.plain-list {
  margin: 18px 0 20px;
  padding-left: 24px;
  font-size: 17px;
}

.plain-list li { margin: 8px 0; }

code {
  padding: 2px 6px;
  border-radius: 5px;
  background: #eff6ff;
  color: #1d4ed8;
  font-family: "SFMono-Regular", Menlo, Consolas, monospace;
}

.insight {
  margin: 24px 0;
  padding: 20px 22px;
  border-left: 5px solid var(--cyan);
  background: #ecfeff;
  border-radius: 0 8px 8px 0;
  font-size: 18px;
}

.figure {
  margin: 30px 0 14px;
}

.figure img {
  width: 100%;
  display: block;
  border-radius: 8px;
  border: 1px solid #dbeafe;
}

.caption {
  margin-top: 10px;
  color: var(--muted);
  font-size: 15px;
}

.steps {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  margin: 24px 0;
}

.steps div {
  position: relative;
  min-height: 164px;
  padding: 20px 20px 18px 72px;
  border: 1px solid #dbeafe;
  border-radius: 8px;
  background: #f8fbff;
}

.steps span {
  position: absolute;
  left: 20px;
  top: 22px;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--blue);
  color: #fff;
  font-weight: 800;
}

.steps b {
  display: block;
  margin-bottom: 8px;
  font-size: 18px;
}

.steps p {
  margin: 0;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.65;
}

table {
  width: 100%;
  margin: 22px 0;
  border-collapse: collapse;
  font-size: 14px;
}

th {
  color: #fff;
  background: #0f172a;
}

th, td {
  padding: 12px 13px;
  border: 1px solid #dbeafe;
  text-align: left;
  vertical-align: top;
}

td:first-child {
  width: 18%;
  font-weight: 800;
  color: #0f766e;
}

.myths {
  display: grid;
  grid-template-columns: 1fr;
  gap: 13px;
  margin: 22px 0;
}

.myths div,
.questions div {
  padding: 18px 20px;
  border: 1px solid #fed7aa;
  border-radius: 8px;
  background: #fff7ed;
}

.myths b,
.questions b {
  display: block;
  margin-bottom: 5px;
  color: #9a3412;
  font-size: 18px;
}

.myths p,
.questions p {
  margin: 0;
  color: var(--muted);
  font-size: 16px;
}

.summary-list {
  margin: 22px 0 8px;
  padding-left: 26px;
  font-size: 20px;
}

.summary-list li {
  margin: 14px 0;
  padding-left: 6px;
}

.questions {
  display: grid;
  gap: 14px;
}

.source-list {
  margin-top: 36px;
  padding: 24px 28px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.source-list h2 {
  font-size: 24px;
}

.source-list li {
  margin: 7px 0;
  color: var(--muted);
  font-size: 14px;
  word-break: break-word;
}

@page {
  size: A4;
  margin: 10mm;
}

@media print {
  body { background: #fff; }
  .page { box-shadow: none; max-width: none; }
  .cover { min-height: 268mm; page-break-after: always; }
  .content { padding: 0 8mm 8mm; }
  .toc { page-break-after: always; margin-top: 8mm; }
  section { break-inside: avoid; }
  .figure { break-inside: avoid; }
  h2 { break-after: avoid; }
  .steps { grid-template-columns: 1fr 1fr; }
}
"""


SOURCE_ITEMS = [
    ("OpenAI Platform Docs", "Evals", "https://developers.openai.com/api/docs/guides/evals"),
    ("OpenAI Platform Docs", "Evaluation best practices", "https://developers.openai.com/api/docs/guides/evaluation-best-practices"),
    (
        "Google Machine Learning Crash Course",
        "Classification: Accuracy, recall, precision, and related metrics",
        "https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall",
    ),
    ("scikit-learn User Guide", "Model evaluation", "https://scikit-learn.org/stable/modules/model_evaluation.html"),
    (
        "scikit-learn API Reference",
        "precision_recall_fscore_support",
        "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html",
    ),
    ("NIST", "AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework"),
]


def render_toc() -> str:
    items = "\n".join(
        f'<li><a href="#{escape(section["id"])}">{escape(section["title"])}</a></li>'
        for section in SECTIONS
    )
    return f'<nav class="toc"><h2>目录</h2><ol>{items}</ol></nav>'


def render_sections() -> str:
    rendered: list[str] = []
    for section in SECTIONS:
        image_html = ""
        if "image" in section:
            image_html = (
                '<figure class="figure">'
                f'<img src="{escape(section["image"])}" alt="{escape(section["caption"])}">'
                f'<figcaption class="caption">{escape(section["caption"])}</figcaption>'
                "</figure>"
            )
        rendered.append(
            f'<section id="{escape(section["id"])}">'
            f'<h2>{escape(section["title"])}</h2>'
            f'{section["body"]}'
            f'{image_html}'
            "</section>"
        )
    return "\n".join(rendered)


def render_sources() -> str:
    lis = "\n".join(
        f'<li><b>{escape(org)}</b>：{escape(title)}<br><span>{escape(url)}</span></li>'
        for org, title, url in SOURCE_ITEMS
    )
    return f'<aside class="source-list"><h2>参考来源</h2><ol>{lis}</ol></aside>'


def build_html() -> str:
    today = "2026-07-06"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(TITLE)}｜AI每日深度科普</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="page">
    <header class="cover">
      <div>
        <div class="kicker">AI每日深度科普 · 概念课 {today}</div>
        <h1>{escape(TITLE)}</h1>
        <p class="subtitle">{escape(SUBTITLE)}</p>
        <div class="core"><b>核心一句话：</b>{escape(CORE_SENTENCE)}</div>
        <div class="cover-grid">
          <div class="cover-chip"><b>知识地图位置</b><span>Embedding、RAG、结构化输出之后的质量判断层</span></div>
          <div class="cover-chip"><b>适合读者</b><span>高中生、产品经理、业务负责人、AI 初学者</span></div>
          <div class="cover-chip"><b>今天要建立的直觉</b><span>AI 质量不能只靠感觉，要靠一组指标持续体检</span></div>
        </div>
      </div>
      <div class="meta">
        <span>主题：Evaluation Metrics（评估指标）</span>
        <span>形式：HTML / PDF 科普文档</span>
      </div>
    </header>
    <article class="content">
      {render_toc()}
      {render_sections()}
      {render_sources()}
    </article>
  </main>
</body>
</html>
"""


def write_email_files() -> None:
    EMAIL_SUBJECT.write_text(
        "【AI每日深度科普】Evaluation Metrics：为什么 AI 不能只看“答得像不像”？",
        encoding="utf-8",
    )
    EMAIL_BODY.write_text(
        """今天的主题是 Evaluation Metrics（评估指标）。

这是理解 AI 产品能否真正上线、持续改进和稳定交付的关键基础概念。

附件会用“AI体检报告”的方式解释：
为什么一个 AI 系统不能只看总分，而要同时看准确率、召回率、幻觉率、延迟、成本和失败案例。

适合非技术读者、AI初学者、产品经理、业务负责人和正在建设 AI 应用的人阅读。""",
        encoding="utf-8",
    )


def main() -> None:
    HTML.write_text(build_html(), encoding="utf-8")
    SOURCES.write_text(SOURCES_TEXT, encoding="utf-8")
    write_email_files()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1600}, device_scale_factor=1)
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.screenshot(path=str(PREVIEW), full_page=True)
        page.pdf(path=str(PDF), format="A4", print_background=True, prefer_css_page_size=True)
        browser.close()

    print(f"Built: {HTML}")
    print(f"Built: {PDF}")
    print(f"Built: {PREVIEW}")
    print(f"Built at: {datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
