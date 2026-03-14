import asyncio
from playwright.async_api import async_playwright
import time

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Navigating to Streamlit app...")
        await page.goto("http://localhost:8501")

        # Wait for Streamlit to load the app UI fully
        print("Waiting for app to load...")
        await page.wait_for_selector('input[type="text"]', timeout=30000)

        # Type a query
        print("Filling out query...")
        await page.fill('input[type="text"]', "How to fix High Voltage Battery Error?")

        # Click the "Get Diagnosis" button
        print("Clicking Get Diagnosis...")
        # In Streamlit, buttons are wrapped in div.stButton > button
        await page.click('button:has-text("Get Diagnosis")')

        # Wait for the spinner to disappear and the result to appear
        print("Waiting for diagnosis result (this involves the LLM running)...")
        # We wait for the subheader that shows up after generation
        await page.wait_for_selector('h3:has-text("Diagnostic Response:")', timeout=120000)

        # Give it a tiny bit of extra time to render completely
        await page.wait_for_timeout(2000)

        print("Taking screenshot...")
        await page.screenshot(path="screenshot.png", full_page=True)

        await browser.close()
        print("Screenshot saved to screenshot.png")

if __name__ == "__main__":
    asyncio.run(main())
