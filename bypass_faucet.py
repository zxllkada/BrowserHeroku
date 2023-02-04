from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import asyncio, os

# driver_path = "chromedriver.exe"
# browser = webdriver.Chrome(executable_path=driver_path)

async def createDriver():
    driver_path = os.environ.get("GOOGLEDRIVER_PATH")
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")
    
    myDriver = webdriver.Chrome(executable_path=driver_path, options=options)
    return myDriver

# Create a browser
# def createDriver() -> webdriver.Chrome:
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     #chrome_options.add_argument("--disable-popup-blocking")
# 
#     prefs = {"profile.managed_default_content_settings.images":2}
#     chrome_options.headless = True
# 
#     chrome_options.add_experimental_option("prefs", prefs)
#     myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# 
#     return myDriver


async def SolveCaptchaBrowser(url):
    solve, count = False, 1
    
    browser = await createDriver()
    browser.get(url)
    while solve != True:
        if count == 15:
            break
        
        handles = browser.window_handles
        browser.switch_to.window(handles[0])
        html = browser.page_source
        
        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all("script")
        for script in scripts:
            if "const canvas" in script.text:
                emoji = ((script.text).split('contex.fillText("')[1]).split('", canvas.width')[0]
                buttons = soup.find_all('button', class_='emojibtn')
                for idx, button in enumerate(buttons, start=1):
                    if str(button.text).strip() == emoji:
                        currect_button = idx
                        break

                wait = WebDriverWait(browser, 40)
                button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="main_div"]/div/div/div/div/div/button[{currect_button}]')))
                button.click()
                
                await asyncio.sleep(3)
                ClickSubmit = wait.until(EC.element_to_be_clickable((By.ID, "button"))).click()
                
                html = browser.page_source
                if "You claimed faucet successfully!" in html:
                    solve = True
                    break
                
            elif "const randomNumber" in script.text:
                CaptchaText = ((script.text).split('ctx.fillText("')[1]).split('"[i], xInitialSpace')[0]
                wait = WebDriverWait(browser, 40)
                input_field = wait.until(EC.element_to_be_clickable((By.NAME, "answer")))
                input_field.send_keys(CaptchaText)
                
                await asyncio.sleep(3)
                ClickSubmit = wait.until(EC.element_to_be_clickable((By.ID, "button"))).click()
                
                html = browser.page_source
                if "You claimed faucet successfully!" in html:
                    solve = True
                    break

        count += 1
        if solve == False:
            await asyncio.sleep(3)
            browser.refresh()
            
    browser.quit()
    solve, count = False, 1

