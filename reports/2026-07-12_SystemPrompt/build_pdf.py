from __future__ import annotations

from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
HTML = BASE / "2026-07-12_系统提示词（System Prompt）.html"
PDF = BASE / "2026-07-12_系统提示词（System Prompt）.pdf"

def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 1600})
            page.goto(HTML.as_uri(), wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(PDF),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=True,
                header_template="<div></div>",
                footer_template='<div style="width:100%;padding-right:42px;text-align:right;color:#60718a;font-size:8px;font-family:-apple-system,BlinkMacSystemFont,sans-serif">AI 每日深度科普 · 2026-07-12 · 第 <span class="pageNumber"></span> / <span class="totalPages"></span> 页</div>',
                margin={"top": "0", "right": "0", "bottom": "12mm", "left": "0"},
            )
        finally:
            browser.close()
    print(PDF)

if __name__ == "__main__":
    main()
