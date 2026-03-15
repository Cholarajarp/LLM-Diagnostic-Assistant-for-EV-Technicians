from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8502")
        page.wait_for_selector("textarea")

        # Get outer HTML of the bottom section
        html = page.evaluate('''() => {
            const el = document.querySelector('[data-testid="stBottomBlockContainer"]').parentElement;
            return el ? el.outerHTML : "Not found";
        }''')
        with open("dom2.html", "w") as f:
            f.write(html)
        browser.close()

if __name__ == "__main__":
    run()
