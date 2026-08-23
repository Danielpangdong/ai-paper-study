from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class FigStyle:
    w: int = 2400
    h: int = 1350
    margin: int = 110
    ink: tuple[int, int, int] = (15, 23, 42)
    muted: tuple[int, int, int] = (71, 85, 105)
    line: tuple[int, int, int] = (226, 232, 240)
    soft: tuple[int, int, int] = (248, 250, 252)
    accent: tuple[int, int, int] = (14, 165, 163)
    accent2: tuple[int, int, int] = (37, 99, 235)
    danger: tuple[int, int, int] = (239, 68, 68)
    ok: tuple[int, int, int] = (16, 185, 129)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size, index=0)
    return ImageFont.load_default()


def text_w(font: ImageFont.ImageFont, text: str) -> float:
    try:
        return font.getlength(text)
    except Exception:
        return font.getbbox(text)[2]


def wrap(font: ImageFont.ImageFont, text: str, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            lines.append("")
            continue
        buf = ""
        for ch in para:
            if ch == "\r":
                continue
            trial = buf + ch
            if text_w(font, trial) <= max_w:
                buf = trial
                continue
            if buf:
                lines.append(buf.rstrip())
                buf = ch.lstrip()
            else:
                lines.append(trial)
                buf = ""
        if buf:
            lines.append(buf.rstrip())
        lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def draw_block_text(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.ImageFont,
    text: str,
    x: int,
    y: int,
    max_w: int,
    fill: tuple[int, int, int],
    line_gap: int = 10,
) -> int:
    for line in wrap(font, text, max_w):
        if not line:
            y += int(font.size * 0.65)
            continue
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], r: int, **kw) -> None:
    draw.rounded_rectangle(box, radius=r, **kw)


def fig_notebook(out_path: Path) -> Path:
    s = FigStyle()
    img = Image.new("RGB", (s.w, s.h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    title = load_font(82)
    sub = load_font(30)
    h = load_font(44)
    body = load_font(30)
    small = load_font(26)

    y = 56
    draw.text((s.margin, y), "KV Cache（键值缓存）", font=title, fill=s.ink)
    y += title.size + 18
    draw.text((s.margin, y), "像读文章时把关键信息“记在笔记本里”，后面就不用反复回头读。", font=sub, fill=s.muted)
    y += sub.size + 46

    left_x = s.margin
    mid_x = s.w // 2 - 160
    right_x = s.w // 2 + 230
    col_w = s.w // 2 - s.margin - 30

    # Left: timeline
    rounded(draw, (left_x, y, left_x + col_w, s.h - 220), 30, outline=s.line, width=3, fill=s.soft)
    draw.text((left_x + 38, y + 30), "对话 / 生成（时间线）", font=h, fill=s.ink)
    t_y = y + 118
    line_x = left_x + 70
    draw.line((line_x, t_y, line_x, s.h - 270), fill=s.accent2, width=8)
    nodes = [
        ("用户提示", "请介绍一下量子计算。", s.accent2),
        ("模型开始生成第1个字", "“量”", s.ok),
        ("模型生成下一个字", "“子”", s.ok),
        ("模型生成下一个字", "“计”", s.ok),
        ("…", "持续生成", s.muted),
    ]
    for i, (k, v, c) in enumerate(nodes):
        cy = t_y + i * 180
        draw.ellipse((line_x - 16, cy - 16, line_x + 16, cy + 16), fill=c)
        card_x = line_x + 34
        card_w = col_w - (card_x - left_x) - 42
        rounded(draw, (card_x, cy - 60, card_x + card_w, cy + 78), 22, outline=s.line, width=2, fill=(255, 255, 255))
        draw.text((card_x + 26, cy - 44), k, font=body, fill=s.ink)
        draw.text((card_x + 26, cy + 10), v, font=small, fill=s.muted)

    # Middle: notebook
    nb_w = 440
    nb_h = 560
    nb_x = mid_x
    nb_y = y + 160
    rounded(draw, (nb_x, nb_y, nb_x + nb_w, nb_y + nb_h), 36, outline=s.ink, width=4, fill=(255, 255, 255))
    for i in range(7):
        x = nb_x - 26
        y0 = nb_y + 60 + i * 70
        draw.ellipse((x, y0, x + 40, y0 + 40), outline=s.ink, width=4)
    draw.text((nb_x + 68, nb_y + 76), "缓存：", font=h, fill=s.ink)
    draw.text((nb_x + 68, nb_y + 150), "K / V", font=load_font(78), fill=s.accent2)
    draw.text((nb_x + 68, nb_y + 250), "（注意力的 Key / Value）", font=small, fill=s.muted)
    draw.line((nb_x + 68, nb_y + 320, nb_x + nb_w - 68, nb_y + 320), fill=s.line, width=3)
    draw.text((nb_x + 68, nb_y + 352), "像“笔记本”一样\n记录已读内容的关键信息", font=small, fill=s.muted)

    # arrows
    ax1 = left_x + col_w + 30
    ay1 = nb_y + nb_h // 2
    draw.polygon([(ax1, ay1 - 18), (ax1 + 34, ay1), (ax1, ay1 + 18)], fill=s.muted)
    draw.rectangle((ax1 - 50, ay1 - 4, ax1, ay1 + 4), fill=s.muted)
    ax2 = nb_x + nb_w + 30
    draw.polygon([(ax2, ay1 - 18), (ax2 + 34, ay1), (ax2, ay1 + 18)], fill=s.muted)
    draw.rectangle((ax2 - 50, ay1 - 4, ax2, ay1 + 4), fill=s.muted)

    # Right: compare
    right_w = s.w - right_x - s.margin
    top_box = (right_x, y, right_x + right_w, y + 430)
    bot_box = (right_x, y + 470, right_x + right_w, s.h - 220)
    rounded(draw, top_box, 30, outline=s.line, width=3, fill=(255, 255, 255))
    rounded(draw, bot_box, 30, outline=s.line, width=3, fill=(255, 255, 255))
    draw.text((right_x + 36, y + 26), "没有缓存：", font=h, fill=s.danger)
    draw.text((right_x + 36, y + 86), "每生成一个新字都要“回头重读全文”", font=small, fill=s.muted)
    draw.text((right_x + 36, y + 490), "有缓存：", font=h, fill=s.ok)
    draw.text((right_x + 36, y + 550), "只读“新来的这一个字”，并查笔记", font=small, fill=s.muted)

    def token_row(base_y: int, color: tuple[int, int, int], loop: bool) -> None:
        tx = right_x + 36
        ty = base_y
        tokens = ["用户提示（全文）", "量", "子", "计", "…"]
        box_w = (right_w - 36 * 2 - 4 * 20) // 5
        for i, t in enumerate(tokens):
            x0 = tx + i * (box_w + 20)
            rounded(draw, (x0, ty, x0 + box_w, ty + 78), 18, outline=color, width=3, fill=(255, 255, 255))
            draw.text((x0 + 18, ty + 20), t, font=small, fill=s.ink)
        if loop:
            # big looping arrow (red)
            y_mid = ty + 118
            draw.arc((tx + 40, y_mid, tx + right_w - 80, y_mid + 200), start=15, end=165, fill=color, width=10)
            draw.polygon(
                [(tx + right_w // 2 - 18, y_mid + 188), (tx + right_w // 2 + 18, y_mid + 188), (tx + right_w // 2, y_mid + 230)],
                fill=color,
            )
        else:
            # short dashed arrows
            y_mid = ty + 110
            for i in range(1, 5):
                x0 = tx + (i - 1) * (box_w + 20) + box_w
                x1 = tx + i * (box_w + 20)
                for k in range(9):
                    t0 = k / 10
                    sx = int(x0 + (x1 - x0) * t0)
                    ex = int(x0 + (x1 - x0) * (t0 + 0.05))
                    draw.line((sx, y_mid, ex, y_mid), fill=color, width=4)
                draw.polygon([(x1 - 10, y_mid - 10), (x1 - 10, y_mid + 10), (x1 + 10, y_mid)], fill=color)

    token_row(y + 170, s.danger, loop=True)
    token_row(y + 650, s.ok, loop=False)

    # bottom summary ribbon
    ribbon = (s.margin, s.h - 170, s.w - s.margin, s.h - 78)
    rounded(draw, ribbon, 32, outline=s.accent2, width=4, fill=(245, 250, 255))
    draw.text((s.margin + 70, s.h - 148), "KV Cache 主要让“推理更快更省钱”，不是让模型更聪明。", font=h, fill=s.ink)

    img.save(out_path)
    return out_path


def fig_prefill_decode(out_path: Path) -> Path:
    s = FigStyle()
    img = Image.new("RGB", (s.w, s.h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    title = load_font(86)
    h = load_font(44)
    body = load_font(32)
    small = load_font(26)

    y = 60
    draw.text((s.margin, y), "KV Cache：推理加速的关键", font=title, fill=s.ink)
    y += title.size + 50

    left_w = (s.w - s.margin * 2 - 70) // 2
    right_x = s.margin + left_w + 70
    left_x = s.margin

    # Left two cards
    card_h = 380
    c1 = (left_x, y, left_x + left_w, y + card_h)
    c2 = (left_x, y + card_h + 50, left_x + left_w, y + card_h * 2 + 50)
    rounded(draw, c1, 30, outline=s.line, width=3, fill=(255, 255, 255))
    rounded(draw, c2, 30, outline=s.line, width=3, fill=(255, 255, 255))

    draw.text((left_x + 38, y + 34), "1  Prefill（读提示）", font=h, fill=s.accent2)
    draw.text((left_x + 38, y + 110), "一次性读完“用户提示”\n并建立缓存", font=body, fill=s.ink)
    draw.text((left_x + 38, y + 240), "你可以理解为：先把课本读一遍\n把关键点做成笔记。", font=small, fill=s.muted)

    y2 = y + card_h + 50
    draw.text((left_x + 38, y2 + 34), "2  Decode（逐字生成）", font=h, fill=s.accent)
    draw.text((left_x + 38, y2 + 110), "每次只处理“新生成的一个字”\n并复用缓存", font=body, fill=s.ink)
    draw.text((left_x + 38, y2 + 240), "你可以理解为：后面每翻一页\n只补充新笔记，不重读前面。", font=small, fill=s.muted)

    # Right flow
    flow = (right_x, y, s.w - s.margin, s.h - 260)
    rounded(draw, flow, 30, outline=s.line, width=3, fill=s.soft)
    draw.text((right_x + 38, y + 34), "简化流程（只看信息流向）", font=h, fill=s.ink)

    step_x = right_x + 60
    step_y = y + 130
    step_w = s.w - s.margin - step_x - 60
    steps = [
        ("用户提示", s.ink),
        ("计算注意力", s.ink),
        ("写入 KV Cache", s.accent),
        ("生成第1个字", s.ink),
        ("读取 KV Cache + 新字", s.accent),
        ("生成第2个字", s.ink),
        ("…", s.muted),
    ]
    box_h = 88
    gap = 32
    for i, (t, col) in enumerate(steps):
        y0 = step_y + i * (box_h + gap)
        rounded(draw, (step_x, y0, step_x + step_w, y0 + box_h), 22, outline=s.line, width=2, fill=(255, 255, 255))
        draw.text((step_x + 26, y0 + 24), t, font=body, fill=col)
        if i < len(steps) - 1:
            ax = step_x + step_w // 2
            draw.line((ax, y0 + box_h, ax, y0 + box_h + gap - 6), fill=s.muted, width=6)
            draw.polygon([(ax - 14, y0 + box_h + gap - 6), (ax + 14, y0 + box_h + gap - 6), (ax, y0 + box_h + gap + 14)], fill=s.muted)

    # Callouts
    c_y = s.h - 230
    ribbon1 = (s.margin, c_y, s.w - s.margin, c_y + 90)
    ribbon2 = (s.margin, c_y + 110, s.w - s.margin, c_y + 200)
    rounded(draw, ribbon1, 28, outline=s.accent2, width=4, fill=(245, 250, 255))
    rounded(draw, ribbon2, 28, outline=s.accent, width=4, fill=(240, 253, 250))
    draw.text((s.margin + 50, c_y + 26), "缓存的是注意力里的 K/V，不是最终答案", font=h, fill=s.ink)
    draw.text((s.margin + 50, c_y + 136), "缓存会占显存/内存：上下文越长，占用越大", font=h, fill=s.ink)

    img.save(out_path)
    return out_path


def build_all() -> list[Path]:
    base = Path(__file__).resolve().parent
    paths = [
        fig_notebook(base / "kv_cache_notebook.png"),
        fig_prefill_decode(base / "kv_cache_prefill_decode.png"),
    ]
    return paths


if __name__ == "__main__":
    for p in build_all():
        print(str(p))

