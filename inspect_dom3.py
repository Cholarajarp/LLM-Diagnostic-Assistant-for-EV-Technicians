from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8502")
        page.wait_for_selector("textarea")

        # We need to find the parent container that has a white background in dark mode.
        # It's likely `[data-testid="stBottomBlockContainer"]`'s parent or something similar.
        # Let's get the background color of various elements
        script = '''() => {
            const els = [];
            let el = document.querySelector('[data-testid="stBottomBlockContainer"]');
            while(el && el.tagName !== 'BODY') {
                els.push({
                    tag: el.tagName,
                    className: el.className,
                    bg: window.getComputedStyle(el).backgroundColor
                });
                el = el.parentElement;
            }
            return els;
        }'''
        bg_colors = page.evaluate(script)
        import json
        with open("dom3.json", "w") as f:
            json.dump(bg_colors, f, indent=2)
        browser.close()

if __name__ == "__main__":
    run()
