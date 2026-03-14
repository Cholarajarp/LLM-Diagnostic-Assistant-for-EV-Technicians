import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        print("Navigating to Streamlit app...")
        await page.goto("http://localhost:8501")

        # Wait for Streamlit to load
        print("Waiting for app to load...")
        await page.wait_for_selector('input[type="text"]', timeout=30000)

        # 1. Capture Light Mode (Default)
        print("Taking Light Mode screenshot...")
        await page.wait_for_timeout(2000) # Give fonts/css time to load
        await page.screenshot(path="screenshot_light.png", full_page=True)

        # 2. Toggle to Dark Mode
        print("Switching to Dark Mode...")
        # Radio buttons in streamlit. The second label is "Dark Mode"
        await page.click('label:has-text("Dark Mode")')
        await page.wait_for_timeout(2000) # Wait for CSS injection to take effect
        print("Taking Dark Mode screenshot...")
        await page.screenshot(path="screenshot_dark.png", full_page=True)

        # 3. Enter Query and get response
        print("Entering complex query in Dark Mode...")
        await page.fill('input[type="text"]', "How to check Inverter resistance for Nissan?")
        await page.click('button:has-text("Get Diagnosis")')

        print("Waiting for LLM response...")
        await page.wait_for_selector('h3:has-text("Diagnostic Response:")', timeout=120000)
        await page.wait_for_timeout(3000) # Allow response and source expanders to render

        print("Taking Response screenshot...")
        await page.screenshot(path="screenshot_response.png", full_page=True)

        await browser.close()
        print("Screenshots captured successfully: screenshot_light.png, screenshot_dark.png, screenshot_response.png")

if __name__ == "__main__":
    asyncio.run(main())
