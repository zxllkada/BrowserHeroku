from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.contacts import UnblockRequest

import asyncio, os


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
    
#     prefs = {"profile.managed_default_content_settings.images":2}
#     chrome_options.headless = True

#     chrome_options.add_experimental_option("prefs", prefs)
#     myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#     return myDriver


async def HandyBot_Clickers(event):
    bot_username = "@HandyClickerBot"
    
    # visit links
    async def HandyBot_VisitLinks():
        while True:
            async with event.client.conversation(bot_username, timeout=300) as conv:
                await conv.send_message('🔗 Visit Links')

                Website = await conv.get_response()
                if str(Website.message).startswith('ℹ️ There are no more ads available.'):
                    await asyncio.sleep(1)
                    break
                elif "⚠️ To proceed, resolve the captcha!" in str(Website.message):
                        Message = await event.client(GetHistoryRequest(peer="HandyClickerBot", offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
                        captcha = (((str(Message.messages[0].message).split('Solve the operation:')[1]).split('=')[0]).replace('*', '')).split(' ')
                        if str(captcha[2]) == "+":
                            solve = int(captcha[1]) + int(captcha[3])
                        elif str(captcha[2]) == "-":
                            solve = int(captcha[1]) - int(captcha[3])
                        solved, Sleep = await Message.messages[0].click(text=str(solve)), await asyncio.sleep(1)
                else:
                    try:
                        browser = await createDriver()
                        browser.get(Website.reply_markup.rows[0].buttons[0].url)

                        is_reward = await conv.get_response()
                        if (is_reward.text).startswith('✅ Task Completed!'):
                            browser.quit()
                        else:
                            Skip, quit = await Website.click(text='Skip ➡️'), browser.quit()

                    except:
                        break
            await asyncio.sleep(3)
    
    
    # join channels
    async def HandyBot_JoinChannels():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('📢 Join Chats')

                Channel = await conv.get_response()
                if str(Channel.message).startswith('ℹ️ There are no more ads available.'):
                    await asyncio.sleep(1)
                    break
                elif "⚠️ To proceed, resolve the captcha!" in str(Channel.message):
                        Message = await event.client(GetHistoryRequest(peer="HandyClickerBot", offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
                        captcha = (((str(Message.messages[0].message).split('Solve the operation:')[1]).split('=')[0]).replace('*', '')).split(' ')
                        if str(captcha[2]) == "+":
                            solve = int(captcha[1]) + int(captcha[3])
                        elif str(captcha[2]) == "-":
                            solve = int(captcha[1]) - int(captcha[3])
                        solved, Sleep = await Message.messages[0].click(text=str(solve)), await asyncio.sleep(1)
                else:
                    try:
                        if (Channel.reply_markup.rows[0].buttons[0].url).startswith('https://t.me/'):
                            final_url = Channel.reply_markup.rows[0].buttons[0].url
                        else:
                            browser = await createDriver()
                            browser.get(Channel.reply_markup.rows[0].buttons[0].url)
                            await asyncio.sleep(5)
                            final_url = browser.current_url
                            browser.quit()

                        Channel_username = (final_url).replace('https://t.me/', '').split('?')[0]
                        try:
                            if "+" in Channel_username:
                                channel_hash = Channel_username.replace("+", "").strip()
                                Join = await event.client(ImportChatInviteRequest(hash=channel_hash))
                            else:
                                join = await event.client(JoinChannelRequest(channel=Channel_username))
                        except Exception as error:
                            pass
                        Joined = await Channel.click(text='✅ Joined')
                    except Exception as error:
                        print (error)
            await asyncio.sleep(3)
            
    
    # join bots
    async def HandyBot_JoinBots():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('🤖 Message Bots')

                Bot_data = await conv.get_response()
                if str(Bot_data.message).startswith('ℹ️ There are no more ads available.'):
                    await asyncio.sleep(1)
                    break
                elif "⚠️ To proceed, resolve the captcha!" in str(Bot_data.message):
                        Message = await event.client(GetHistoryRequest(peer="HandyClickerBot", offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
                        captcha = (((str(Message.messages[0].message).split('Solve the operation:')[1]).split('=')[0]).replace('*', '')).split(' ')
                        if str(captcha[2]) == "+":
                            solve = int(captcha[1]) + int(captcha[3])
                        elif str(captcha[2]) == "-":
                            solve = int(captcha[1]) - int(captcha[3])
                        solved, Sleep = await Message.messages[0].click(text=str(solve)), await asyncio.sleep(1)
                else:
                    Started, Bot_info = await Bot_data.click(text='✅ Started'), await conv.get_response()
                    target_bot_username = (Bot_info.message).split(' ')[5]
                    
                    try:
                        try:
                            unban = await event.client(UnblockRequest(id=target_bot_username))
                        except:
                            pass
                        StartBot, Sleep = await event.client.send_message(entity=target_bot_username, message='/start'), await asyncio.sleep(1)
                        Message = await event.client(GetHistoryRequest(peer=target_bot_username, offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
                        Forward = await event.client(ForwardMessagesRequest(from_peer=target_bot_username, to_peer=bot_username, id=[Message.messages[0].id]))
                        DeleteBot = await event.client(DeleteHistoryRequest(peer=target_bot_username, max_id=0, just_clear=True, revoke=True))
                    except Exception as error:
                        print (error)
                        await conv.send_message('Back 🔙')                  
            await asyncio.sleep(3)
    
    # view posts
    async def HandyBot_ViewPosts():
        while True:
            async with event.client.conversation(bot_username, timeout=20) as conv:
                await conv.send_message('📄 Watch Ads')

                ViewAd = await conv.get_response()
                if str(ViewAd.message).startswith('ℹ️ There are no more ads available.'):
                    await asyncio.sleep(1)
                    break
                elif "⚠️ To proceed, resolve the captcha!" in str(ViewAd.message):
                        Message = await event.client(GetHistoryRequest(peer="HandyClickerBot", offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
                        captcha = (((str(Message.messages[0].message).split('Solve the operation:')[1]).split('=')[0]).replace('*', '')).split(' ')
                        if str(captcha[2]) == "+":
                            solve = int(captcha[1]) + int(captcha[3])
                        elif str(captcha[2]) == "-":
                            solve = int(captcha[1]) - int(captcha[3])
                        solved, Sleep = await Message.messages[0].click(text=str(solve)), await asyncio.sleep(1)
                else:
                    Sleep, Watched = await asyncio.sleep(12), await ViewAd.click(text='✅ Watched')
            await asyncio.sleep(3)
    
    # watch youtube
    async def HandyBot_WatchYoutube():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('📹 YouTube')
                
                ViewAd = await conv.get_response()
                if str(ViewAd.message).startswith('ℹ️ There are no more ads available.'):
                    await asyncio.sleep(1)
                    break
                elif "⚠️ To proceed, resolve the captcha!" in str(ViewAd.message):
                        Message = await event.client(GetHistoryRequest(peer="HandyClickerBot", offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
                        captcha = (((str(Message.messages[0].message).split('Solve the operation:')[1]).split('=')[0]).replace('*', '')).split(' ')
                        if str(captcha[2]) == "+":
                            solve = int(captcha[1]) + int(captcha[3])
                        elif str(captcha[2]) == "-":
                            solve = int(captcha[1]) - int(captcha[3])
                        solved, Sleep = await Message.messages[0].click(text=str(solve)), await asyncio.sleep(1)
                else:
                    break
            await asyncio.sleep(2)
                

    VisitLinks = await HandyBot_VisitLinks()
    JoinChannels = await HandyBot_JoinChannels()
    JoinBots = await HandyBot_JoinBots()
    ViewPosts = await HandyBot_ViewPosts()
    #WatchYoutube = await HandyBot_WatchYoutube()
    
    
