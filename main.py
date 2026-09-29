import os
import subprocess
from playwright.sync_api import sync_playwright, Error
from pages import pagesList

# set up the browser
playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=True)
page = browser.new_page()
page.set_default_timeout(12000)

# cs log in
try:
    page.goto("https://cs.elfak.ni.ac.rs/nastava/login/index.php")
    page.locator('xpath=//*[@id="username"]').fill(os.environ['email'])
    page.locator('xpath=//*[@id="password"]').fill(os.environ['password'])
    page.locator('xpath=//*[@id="loginbtn"]').click()
    page.wait_for_selector('xpath=//*[@id="page-header"]/div/div[1]/div/div[1]')
except Error as e:
    print(f"CS LOG IN: {e}")
    browser.close()
    playwright.stop()
    exit(1)

# scrapping 
for pageName, info in pagesList.items():
    try:
        response = page.goto(info['url'])
        if not response or not response.ok:
            print(f"Skipping {pageName}")
            continue
        page_content = page.locator(info['element']).first.inner_text()
        with open (f"{pageName}.md", "r+", encoding="utf-8") as f:
            file_content = f.read().strip()
            if file_content != page_content:
                f.seek(0)
                f.truncate(0)
                f.write(page_content)
                print(f"{pageName}.md is updated !!!")
                subprocess.run([
                    "python", "discordBot.py", 
                    str(info['id']), 
                    info['url']
                ])
    except Error as e:
        print(f"{pageName} : {e}")
        continue

browser.close()
playwright.stop()
