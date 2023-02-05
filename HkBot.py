from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.contacts import UnblockRequest

import asyncio


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
# async def createDriver() -> webdriver.Chrome:
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
# 
#     prefs = {"profile.managed_default_content_settings.images":2}
#     chrome_options.headless = True
# 
#     chrome_options.add_experimental_option("prefs", prefs)
#     myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# 
#     return myDriver


async def HkEarn_Function(event):
    bot_username = "@hkearn_usdt_bot"
    
    # check tasks
    async def Check_available_tasks():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('/cancel'), await asyncio.sleep(1), await conv.send_message('/earn')

                Tasks = await conv.get_response()
                TasksMenu = await conv.get_edit()
                
                if "Available tasks:" in TasksMenu.text:
                    tasks = ((TasksMenu.text).split('Available tasks:')[1]).split('|')
                    
                    join_channels_tasks = None
                    join_bots_tasks = None
                    visit_urls_tasks = None
                    view_posts_tasks = None
                    for task in tasks:
                        if "📣" in task.strip():
                            join_channels_tasks = int((((task.replace('📣', '').strip())).replace('(', '')).replace(')', ''))
                        if "🤖" in task.strip():
                            join_bots_tasks = int((((task.replace('🤖', '').strip())).replace('(', '')).replace(')', ''))
                        if "🖥" in task.strip():
                            visit_urls_tasks = int((((task.replace('🖥', '').strip())).replace('(', '')).replace(')', ''))
                        if "👁" in task.strip():
                            view_posts_tasks = int((((task.replace('👁', '').strip())).replace('(', '')).replace(')', ''))

                        
                    
                    if join_channels_tasks != None:
                        click, channel_data = await TasksMenu.click(2), await conv.get_response()
                        if "😟 Sorry, there are no new ads available." in channel_data.text:
                            pass
                        else:
                            start = await HkEarn_JoinChats(event, channel_data)
                    
                    if join_bots_tasks != None:
                        click, bot_data = await TasksMenu.click(3), await conv.get_response()
                        if "😟 Sorry, there are no new ads available." in bot_data.text:
                            pass
                        else:
                            start = await HkEarn_JoinBots(event, bot_data)
                    
                    if visit_urls_tasks != None:
                        click, site_data = await TasksMenu.click(1), await conv.get_response()
                        if "😟 Sorry, there are no new ads available." in site_data.text:
                            pass
                        else:
                            start = await HkEarn_VisitSites(event, site_data)
                    
                    if view_posts_tasks != None:
                        click, view_data = await TasksMenu.click(4), await conv.get_response()
                        if "😟 Sorry, there are no new ads available." in view_data.text:
                            pass
                        elif "Click 'Continue' to view the post and earn your cryptocurrency 👇" in view_data.text:
                            view_url = view_data.reply_markup.rows[0].buttons[0].url
                            browser = await createDriver()
                            browser.get(view_url)
                            button = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-submit"]/button'))).click()
                            await asyncio.sleep(2)
                        else:
                            start = await HkEarn_ViewPosts(event)
                    
                elif "You are currently in an active operation; to use another command or function, you must first cancel this operation." in TasksMenu.text:
                    await conv.send_message('/cancel')
                else:
                    break
            await asyncio.sleep(2)
    
    
    
    # visit sites
    async def HkEarn_VisitSites(event, site_data):
        site_url = site_data.reply_markup.rows[0].buttons[0].url
        
        browser = await createDriver()
        browser.get(site_url)
        button = WebDriverWait(browser, 200).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]/button'))).click()
        await asyncio.sleep(3)
        browser.quit()

    # join chats
    async def HkEarn_JoinChats(event, channel_data):
        channel_url = channel_data.reply_markup.rows[0].buttons[0].url
        
        if "https://t.me/" in channel_url:
            channel_username = channel_url.replace('https://t.me/', '').split('?')[0]
        else:
            browser = await createDriver()
            browser.get(channel_url)
            button = WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-submit"]/button'))).click()
            await asyncio.sleep(5)
            channel_username = (browser.current_url).replace('https://t.me/', '').split('?')[0]

        try:
            if "+" in channel_username:
                channel_hash =channel_username.replace('+', '')
                Join = await event.client(ImportChatInviteRequest(hash=channel_hash))
            else:
                Join = await event.client(JoinChannelRequest(channel=channel_username))
        except:
            pass
            
        confirm, Sleep = await channel_data.click(1), await asyncio.sleep(4)

    
    # join bots
    async def HkEarn_JoinBots(event, bot_data):
        bot_url = bot_data.reply_markup.rows[0].buttons[0].url
        
        if "https://t.me/" in bot_url:
            bott_username = bot_url.replace('https://t.me/', '').split('?')[0]
        else:
            browser = await createDriver()
            browser.get(bot_url)
            button = WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-submit"]/button'))).click()
            await asyncio.sleep(5)
            bott_username = (browser.current_url).replace('https://t.me/', '').split('?')[0]
            
        try:
            UnBlock = await event.client(UnblockRequest(id=bott_username))
        except:
            pass
        
        Start, Sleep = await event.client.send_message(entity=bott_username, message='/start'), await asyncio.sleep(1)
        Message = await event.client(GetHistoryRequest(peer=bott_username, offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
        Forward = await event.client(ForwardMessagesRequest(from_peer=bott_username, to_peer="@hkearn_usdt_bot", id=[Message.messages[0].id]))
        DeleteBot = await event.client(DeleteHistoryRequest(peer=bott_username, max_id=0, just_clear=True, revoke=True))
        Sleep, Cancel = await asyncio.sleep(2), await event.client.send_message(entity="@hkearn_usdt_bot", message='/cancel')
    
    # view posts
    async def HkEarn_ViewPosts(event):
        Sleep, Message = await asyncio.sleep(1), await event.client(GetHistoryRequest(peer="@hkearn_usdt_bot", offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
        Sleep, confirm = await asyncio.sleep(12), await Message.messages[0].click(0)
        
    
    # daily reward
    async def HkEarn_DailyReward():
        pass
    
    
    earn = await Check_available_tasks()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
