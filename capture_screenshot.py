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
        # Streamlit chat_input uses a textarea for multiline capability
        await page.wait_for_selector('textarea[aria-label="Ask about EV errors (e.g., \'BMS_a066\' or \'How to check Inverter resistance?\')"]')
        await page.fill('textarea[aria-label="Ask about EV errors (e.g., \'BMS_a066\' or \'How to check Inverter resistance?\')"]', "How to check Inverter resistance for Nissan?")

        # Press Enter to send the chat message
        await page.press('textarea[aria-label="Ask about EV errors (e.g., \'BMS_a066\' or \'How to check Inverter resistance?\')"]', "Enter")

        print("Waiting for LLM response...")
        # Wait for the "Sources Cited:" markdown to appear in the assistant's response bubble
        await page.wait_for_selector('text=Sources Cited:', timeout=180000)
        await page.wait_for_timeout(4000) # Allow response and source expanders to render fully

        print("Taking Response screenshot...")
        await page.screenshot(path="screenshot_response.png", full_page=True)

        await browser.close()
        print("Screenshots captured successfully: screenshot_light.png, screenshot_dark.png, screenshot_response.png")

if __name__ == "__main__":
    asyncio.run(main())
