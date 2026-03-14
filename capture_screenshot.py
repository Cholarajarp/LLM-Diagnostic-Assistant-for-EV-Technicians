import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        print("Navigating to Streamlit app...")
        await page.goto("http://localhost:8501", timeout=60000)

        # Wait for Streamlit to load completely
        print("Waiting for app to load...")
        # A more robust selector: wait for the main stApp div
        await page.wait_for_selector('.stApp', state='attached', timeout=60000)
        # Give Streamlit's iframe/react components a moment to finish rendering
        await page.wait_for_timeout(5000)

        # 1. Capture Light Mode (Default)
        print("Taking Light Mode screenshot...")
        await page.screenshot(path="screenshot_light.png", full_page=True)

        # 2. Toggle to Dark Mode
        print("Switching to Dark Mode...")
        # Target the radio button label specifically
        await page.click('label:has-text("Dark Mode")')
        await page.wait_for_timeout(3000) # Wait for CSS injection to take effect
        print("Taking Dark Mode screenshot...")
        await page.screenshot(path="screenshot_dark.png", full_page=True)

        # 3. Enter Query and get response
        print("Entering complex query in Dark Mode...")
        # Streamlit inputs can sometimes be tricky to find immediately
        await page.wait_for_selector('input[type="text"]')
        await page.fill('input[type="text"]', "How to check Inverter resistance for Nissan?")

        # Click the "Get Diagnosis" button
        await page.click('button:has-text("Get Diagnosis")')

        print("Waiting for LLM response...")
        await page.wait_for_selector('h3:has-text("Diagnostic Response:")', timeout=180000)
        await page.wait_for_timeout(4000) # Allow response and source expanders to render fully

        print("Taking Response screenshot...")
        await page.screenshot(path="screenshot_response.png", full_page=True)

        await browser.close()
        print("Screenshots captured successfully: screenshot_light.png, screenshot_dark.png, screenshot_response.png")

if __name__ == "__main__":
    asyncio.run(main())
