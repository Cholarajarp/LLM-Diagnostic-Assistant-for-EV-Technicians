import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:8501")
        await page.wait_for_timeout(10000) # wait for the app to load

        # 1. Initial Light Mode
        await page.screenshot(path="light_mode_initial.png")

        # Switch to Dark Mode
        await page.locator("text=Dark Mode").click()
        await page.wait_for_timeout(2000)

        # 2. Initial Dark Mode
        await page.screenshot(path="dark_mode_initial.png")

        # Switch back to Light Mode
        await page.locator("text=Light Mode").click()
        await page.wait_for_timeout(2000)

        # Type into the chat input
        chat_input = page.locator("textarea")
        await chat_input.fill("How to check Inverter resistance for Nissan?")
        await chat_input.press("Enter")

        # Wait for the response to load
        await page.wait_for_timeout(30000) # wait for the response to fully load

        # Expand citations
        expanders = await page.locator("div[data-testid='stExpander']").all()
        for expander in expanders:
            await expander.click()
            await page.wait_for_timeout(1000)

        # 3. Response Light Mode
        await page.screenshot(path="light_mode_response.png", full_page=True)

        # Switch to Dark Mode
        await page.locator("text=Dark Mode").click()
        await page.wait_for_timeout(2000)

        # 4. Response Dark Mode
        await page.screenshot(path="dark_mode_response.png", full_page=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
