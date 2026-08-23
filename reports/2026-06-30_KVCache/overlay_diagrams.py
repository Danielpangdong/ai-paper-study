from __future__ import annotations

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"
FONT_REGULAR = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Songti.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def rounded_label(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    title: str,
    body: str = "",
    *,
    fill: tuple[int, int, int, int] = (255, 255, 255, 232),
    outline: tuple[int, int, int, int] = (37, 99, 235, 180),
    title_color: tuple[int, int, int] = (18, 37, 63),
    body_color: tuple[int, int, int] = (55, 65, 81),
    radius: int = 22,
    title_size: int = 34,
    body_size: int = 24,
    wrap: int = 18,
) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=3)
    draw.text((x1 + 24, y1 + 18), title, fill=title_color, font=font(title_size, True))
    if body:
        lines = []
        for piece in body.split("\n"):
            lines.extend(textwrap.wrap(piece, width=wrap))
        y = y1 + 64
        for line in lines[:4]:
            draw.text((x1 + 24, y), line, fill=body_color, font=font(body_size))
            y += body_size + 9


def annotate_library() -> None:
    img = Image.open(ASSETS / "kv_cache_library_base.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.text((66, 46), "KV Cache：像给AI准备一盒彩色索引卡", fill=(12, 31, 54), font=font(48, True))
    draw.text((66, 108), "不用每说一句话都重读整本书，而是复用前面已经整理好的“重点笔记”。", fill=(69, 80, 97), font=font(28))

    rounded_label(
        draw,
        (76, 210, 690, 330),
        "没有缓存",
        "每生成一个新字，都重新翻一遍前文，慢且浪费算力。",
        outline=(79, 70, 229, 150),
        wrap=22,
    )
    rounded_label(
        draw,
        (960, 220, 1510, 338),
        "有KV Cache",
        "把旧Token的Key/Value存起来，新Token直接查笔记。",
        fill=(238, 250, 255, 238),
        outline=(14, 165, 233, 180),
        wrap=21,
    )
    rounded_label(
        draw,
        (54, 760, 790, 904),
        "直觉类比",
        "像学生做阅读题：第一次读文章时划重点，后面答题就看标注，不必从头逐字重读。",
        outline=(30, 64, 175, 160),
        title_size=32,
        body_size=25,
        wrap=28,
    )
    rounded_label(
        draw,
        (878, 762, 1618, 904),
        "核心价值",
        "节省重复计算，让长对话和流式输出更快；代价是显存会随着上下文变长而增加。",
        fill=(248, 253, 255, 238),
        outline=(22, 163, 74, 170),
        title_size=32,
        body_size=25,
        wrap=28,
    )
    draw.text((808, 526), "复用", fill=(255, 255, 255), font=font(34, True), anchor="mm")

    out = ASSETS / "kv_cache_library_labeled.png"
    Image.alpha_composite(img, overlay).convert("RGB").save(out, quality=95)
    print(out)


def annotate_workflow() -> None:
    img = Image.open(ASSETS / "kv_cache_workflow_base.png").convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.text((46, 38), "KV Cache工作流：只为新Token做新计算，旧Token直接复用", fill=(12, 31, 54), font=font(38, True))
    draw.text((48, 90), "K像“索引”，V像“内容”。缓存保存旧Token的K/V，新Token用Query去查它们。", fill=(70, 80, 94), font=font(22))

    steps = [
        ((40, 224, 258, 276), "1 输入旧Token"),
        ((304, 224, 492, 276), "2 注意力层"),
        ((530, 224, 738, 276), "3 生成K/V"),
        ((786, 224, 990, 276), "4 写入缓存"),
        ((1040, 224, 1248, 276), "5 新Token查询"),
        ((1292, 224, 1492, 276), "6 输出新Token"),
    ]
    for box, text in steps:
        rounded_label(draw, box, text, "", fill=(255, 255, 255, 235), outline=(31, 41, 55, 170), title_size=22, radius=10)

    rounded_label(
        draw,
        (48, 696, 256, 748),
        "重复计算变少",
        "",
        fill=(238, 247, 255, 240),
        outline=(37, 99, 235, 180),
        title_size=24,
        radius=14,
    )
    rounded_label(
        draw,
        (318, 696, 612, 748),
        "每一步更快",
        "",
        fill=(238, 247, 255, 240),
        outline=(37, 99, 235, 180),
        title_size=24,
        radius=14,
    )
    rounded_label(
        draw,
        (992, 696, 1406, 748),
        "缓存越长，占用显存越多",
        "",
        fill=(239, 253, 244, 240),
        outline=(22, 163, 74, 180),
        title_size=24,
        radius=14,
    )
    draw.text((776, 722), "权衡", fill=(55, 65, 81), font=font(26, True), anchor="mm")

    small = [
        ((74, 844, 318, 896), "Prompt旧内容"),
        ((532, 402, 738, 456), "K / V卡片"),
        ((810, 374, 964, 428), "KV缓存池"),
        ((1118, 348, 1320, 402), "Query读取"),
        ((1328, 476, 1512, 530), "下个Token"),
    ]
    for box, text in small:
        x1, y1, x2, y2 = box
        draw.rounded_rectangle(box, radius=12, fill=(255, 255, 255, 228), outline=(148, 163, 184, 160), width=2)
        draw.text((x1 + 20, y1 + 14), text, fill=(15, 23, 42), font=font(21, True))

    out = ASSETS / "kv_cache_workflow_labeled.png"
    Image.alpha_composite(img, overlay).convert("RGB").save(out, quality=95)
    print(out)


if __name__ == "__main__":
    annotate_library()
    annotate_workflow()
