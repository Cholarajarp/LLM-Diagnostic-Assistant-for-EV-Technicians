from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8502")
        page.wait_for_selector("textarea")

        # Click dark mode radio button if we need to switch (we can just inject CSS)
        page.evaluate('''() => {
            const style = document.createElement('style');
            style.innerHTML = `
                .stBottom > div { background-color: #121212 !important; }
            `;
            document.head.appendChild(style);
        }''')

        page.screenshot(path="test_css_dark.png")
        browser.close()

if __name__ == "__main__":
    run()
