from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
HTML = BASE / "2026-06-30_KV Cache（键值缓存）.html"
PDF = BASE / "2026-06-30_KV Cache（键值缓存）.pdf"
PREVIEW = BASE / "html_preview.png"


def launch_chromium(playwright):
    candidates = [
        None,
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    last_error: Exception | None = None
    for executable_path in candidates:
        try:
            kwargs = {"headless": True}
            if executable_path and Path(executable_path).exists():
                kwargs["executable_path"] = executable_path
            elif executable_path:
                continue
            return playwright.chromium.launch(**kwargs)
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not launch Chromium/Chrome: {last_error}")


def main() -> None:
    if not HTML.exists():
        raise FileNotFoundError(HTML)

    with sync_playwright() as p:
        browser = launch_chromium(p)
        try:
            page = browser.new_page(viewport={"width": 1240, "height": 1754}, device_scale_factor=1)
            page.goto(HTML.as_uri(), wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(PDF),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            page.screenshot(path=str(PREVIEW), full_page=True)
        finally:
            browser.close()

    print(PDF)


if __name__ == "__main__":
    main()
