# from browserforge.fingerprints import Screen
# from camoufox import AsyncCamoufox
from playwright.async_api import async_playwright
import asyncio
import os

MINUTOS = int(os.getenv("MINUTOS"))
URL = os.getenv("URL")
MAX_RETRIES = 3


async def run_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(MINUTOS * 60 * 1000)
        await page.screenshot(path="screen.png", full_page=True)


async def main():
    attempts = 0
    while True:
        try:
            print("🚀 Iniciando navegador...")
            await run_browser()
            print("✅ Finalizado com sucesso")
            break
        except Exception as e:
            attempts += 1
            print(f"❌ Erro (tentativa {attempts}): {e}")
            if MAX_RETRIES and attempts >= MAX_RETRIES:
                print("🛑 Limite de tentativas atingido")
                break
            print("♻️ Reiniciando em 5 segundos...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
