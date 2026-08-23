#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 论文学习站 · 索引生成器
扫描顶层每日精读 HTML 与 reports/ 下的深度文章，
提取 日期/标题/机构/主题标签/摘要，生成 data/papers.js（站点数据）。
"""
import glob
import html as htmlmod
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
OUT_JS = os.path.join(DATA_DIR, "papers.js")
OUT_JSON = os.path.join(DATA_DIR, "papers.json")

# ---------------------------------------------------------------- helpers

def read(p):
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""

def strip_tags(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def title_of(text):
    m = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.S | re.I)
    return strip_tags(m.group(1)) if m else ""

def extract_summary(text):
    """在「一句话总结 / 一句话精读 / TL;DR」小节后取第一段文字；否则取正文首段。"""
    m = re.search(
        r"<h2[^>]*>([^<]*(?:一句话|精读|TL;DR|TLDR)[^<]*)</h2>(.*?)</section>",
        text, flags=re.S | re.I)
    if not m:
        m = re.search(
            r"<h2[^>]*>([^<]*(?:一句话|精读|TL;DR|TLDR)[^<]*)</h2>(.*?)<h2",
            text, flags=re.S | re.I)
    if m:
        body = m.group(2)
        # 跳过 KPI 数字卡片等结构，取第一段 <p>
        pm = re.search(r"<p[^>]*>(.*?)</p>", body, flags=re.S | re.I)
        seg = pm.group(1) if pm else body
        seg = re.sub(r"<div[^>]*class=\"kpi[^\"]*\"[^>]*>.*?</div>", " ", seg, flags=re.S)
        s = strip_tags(seg)
        if len(s) > 40:
            return s
    # 回退：正文里第一个足够长的段落
    for pm in re.finditer(r"<p[^>]*>(.*?)</p>", text, flags=re.S | re.I):
        s = strip_tags(pm.group(1))
        if len(s) > 60:
            return s
    return ""

def minutes_of(text):
    t = strip_tags(text)
    n = len(t)
    return max(2, round(n / 550))

# ---------------------------------------------------------------- 分类词典

ORG_RULES = [
    (r"anthropic|claude", "Anthropic"),
    (r"openai|gpt-?5|astra", "OpenAI"),
    (r"deepmind|gemini", "DeepMind"),
    (r"\bmeta\b|brain2qwerty", "Meta"),    (r"qwen", "阿里 Qwen"),
    (r"minimax", "MiniMax"),
    (r"cosmos|nvidia", "NVIDIA"),
    (r"icml|arxiv|论文精选|概念精讲|concept|科普", "学术/AI前沿"),
    (r"google", "Google"),
]
ORG_NAMES = ["Anthropic", "OpenAI", "DeepMind", "Meta", "Google", "学术/AI前沿"]

def detect_org(text):
    t = text.lower()
    for pat, name in ORG_RULES:
        if re.search(pat, t):
            return name
    return "其他"

def detect_org_from_article(text, fallback_text):
    """标题/文件名有机构则优先；否则看正文前部是否有压倒性的机构名。"""
    base = detect_org(fallback_text)
    if base != "其他":
        return base
    head = re.sub(r"<style.*?</style>|<script.*?</script>", " ", text[:6000], flags=re.S | re.I)
    head = re.sub(r"<[^>]+>", " ", head).lower()
    # 单篇解读的主角几乎总是 Anthropic / OpenAI / DeepMind；Google/Meta 多为顺带提及
    names = ["Anthropic", "OpenAI", "DeepMind"]
    counts = {n: len(re.findall(r"\b" + re.escape(n.lower()) + r"\b", head)) for n in names}
    best = max(counts, key=counts.get)
    second = sorted(counts.values(), reverse=True)[1] if len(counts) > 1 else 0
    if counts[best] >= 3 and counts[best] >= 2 * max(second, 1):
        return best
    return "其他"

# 主题标签：按优先级匹配，最多取 3 个
TAG_RULES = [
    (r"对齐|alignment|misalign|控制|control|红队|red.?team|护栏|guardrail|奖励黑客|reward.?hack|弥散|唯我论|超智能|oversight|安全评估", "对齐与安全"),
    (r"可解释|interpretab|自编码|autoencoder|j-?space|全局工作空间|工作空间|工作区|特征激活|机制可解释", "可解释性"),
    (r"密码|cryptograph|安全漏洞|漏洞", "网络安全"),
    (r"世界模型|world model|物理|physical|weathernext|气旋|台风|气象|gamma|cosmos", "世界模型"),
    (r"数学|erdős|erdos|单位距离|猜想|firstproof|mathematic|math|十大|突破", "数学与推理"),
    (r"agent|智能体|agentic|mcp|函数调用|function.?call|a2ui|computer use|deepagent", "智能体"),
    (r"生物|biology|生命科学|lifesci|化学|chemist|chemdraw|nmr|bio", "生物与化学"),
    (r"多模态|multimodal|vla|视觉|vision|omnimodal", "多模态"),
    (r"推理|reasoning|deep.?think|默想|latent|思考|mipu|deepagent", "推理"),
    (r"记忆|memory|metis", "记忆"),
    (r"强化学习|rl|reinforce|mipu|vpo|policy", "强化学习"),
    (r"蒸馏|distill|训练|training|tokenization|token|scaling|缩放|scaling law|evolve|di?loco|recursive|flow model|flow", "训练与方法"),
    (r"transformer|attention|moe|专家|kv.?cache|缓存|架构|architecture|sparse|路由|routing", "架构"),
    (r"rag|检索|embedding|向量|context", "检索与上下文"),
    (r"基准|benchmark|bench|exam|arena|评估|评测", "基准与评估"),
    (r"部署|仿真|deploy|infrastructure|系统|system card|systemcard|min.?t", "系统与部署"),
    (r"科学|science|scientist|发现|研究", "AI for Science"),
    (r"机器人|robot|脑机|qwerty|world action", "机器人"),
    (r"模型能力|能力|expertise|专家|frontier|前沿", "模型能力"),
]

def detect_tags(text, max_tags=3):
    t = text.lower()
    found = []
    for pat, name in TAG_RULES:
        if re.search(pat, t) and name not in found:
            found.append(name)
        if len(found) >= max_tags:
            break
    return found

def date_from_text(text, filename):
    m = re.search(r"(\d{4})[-_]?(\d{2})[-_]?(\d{2})", filename)
    if m:
        return "%s-%s-%s" % (m.group(1), m.group(2), m.group(3))
    m = re.search(r"(\d{4})[-_]?(\d{2})[-_]?(\d{2})", text)
    if m:
        return "%s-%s-%s" % (m.group(1), m.group(2), m.group(3))
    return ""

# ---------------------------------------------------------------- 扫描

def scan_top_level():
    papers = []
    for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        name = os.path.basename(p)
        if name in ("index.html", "reader.html"):
            continue
        text = read(p)
        title = title_of(text)
        if not title:
            continue
        date = date_from_text(text, name)
        tag_src = title + " " + name
        papers.append({
            "file": name,
            "date": date or "0000-00-00",
            "title": title,
            "org": detect_org_from_article(text, tag_src),
            "type": "每日精读",
            "tags": detect_tags(tag_src),
            "summary": extract_summary(text),
            "minutes": minutes_of(text),
        })
    return papers

def scan_reports():
    papers = []
    seen_titles = set()
    for p in sorted(glob.glob(os.path.join(ROOT, "reports", "*", "*.html"))):
        name = os.path.basename(p)
        folder = os.path.basename(os.path.dirname(p))
        if folder == "source_papers":       # 原始论文抓取页，非学习文章
            continue
        text = read(p)
        title = title_of(text)
        if not title:
            continue
        if title in seen_titles:   # 去重（如 email 版）
            continue
        date = date_from_text(text, folder + name)
        tag_src = title + " " + folder + " " + name
        # 类型判定：概念精讲 / 深度科普 vs 论文精选
        #   概念类目录用下划线分隔日期（2026-05-03_RAG），论文精选用连字符（2026-05-13-xxx）
        if re.search(r"concept|概念|科普", tag_src, re.I) or re.match(r"\d{4}-\d{2}-\d{2}_", folder):
            ptype = "概念精讲"
        elif re.search(r"论文精选|AI-Daily-Paper|ai-paper|daily-paper|精选", tag_src, re.I):
            ptype = "论文精选"
        else:
            ptype = "深度精读"
        seen_titles.add(title)
        papers.append({
            "file": os.path.join("reports", folder, name).replace(os.sep, "/"),
            "date": date or "0000-00-00",
            "title": title,
            "org": detect_org(tag_src),
            "type": ptype,
            "tags": detect_tags(tag_src),
            "summary": extract_summary(text),
            "minutes": minutes_of(text),
        })
    return papers

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    papers = scan_top_level() + scan_reports()
    papers.sort(key=lambda x: x["date"], reverse=True)

    stats = {
        "total": len(papers),
        "daily": sum(1 for x in papers if x["type"] == "每日精读"),
        "concept": sum(1 for x in papers if x["type"] == "概念精讲"),
        "picks": sum(1 for x in papers if x["type"] == "论文精选"),
        "orgs": sorted({x["org"] for x in papers}),
        "first": min((x["date"] for x in papers if x["date"] != "0000-00-00"), default=""),
        "last": max((x["date"] for x in papers if x["date"] != "0000-00-00"), default=""),
    }

    payload = {"generated": "2026-08-22", "stats": stats, "papers": papers}
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write("/* 自动生成，勿手改 —— 由 tools/build.py 生成 */\n")
        f.write("window.PAPERS = ")
        f.write(json.dumps(payload, ensure_ascii=False))
        f.write(";\n")

    from collections import Counter
    print("papers:", len(papers))
    print("stats:", stats)
    print("types:", dict(Counter(x["type"] for x in papers)))
    print("orgs:", dict(Counter(x["org"] for x in papers)))
    print("missing date:", sum(1 for x in papers if x["date"] == "0000-00-00"))
    print("missing summary:", sum(1 for x in papers if not x["summary"]))

if __name__ == "__main__":
    main()
