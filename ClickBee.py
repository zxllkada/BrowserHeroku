from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.contacts import UnblockRequest

import asyncio, os



async def createDriver():
    driver_path = os.environ.get("GOOGLEDRIVER_PATH")
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--disable-popup-blocking")
    
    myDriver = webdriver.Chrome(executable_path=driver_path, options=options)
    return myDriver

# # Create a browser
# def createDriver() -> webdriver.Chrome:
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


async def ClickBee_Function(event):
    bot_username = "@ClickBeeLTCBot"
		
    # visit links
    async def VisitWebsites():
        while True:
            async with event.client.conversation(bot_username, timeout=300) as conv:
                await conv.send_message('💻 Visit Sites')

                Website = await conv.get_response()
                if str(Website.message).startswith('⛔️ Oh no! There are NO TASKS available at the moment.'):
                    await asyncio.sleep(2)
                    break
                else:
                    browser = await createDriver()
                    browser.get(Website.reply_markup.rows[0].buttons[1].url)
                        
                    is_reward = await conv.get_response()
                    if (is_reward.text).startswith('⚡️ Congratulations!'):
                        browser.quit()
                    else:
                        Skip = await Website.click(text='➡️ Skip')
            await asyncio.sleep(2)
                            
                        
    # Message Bots
    async def MessageBotsForward():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('🤖 Join Bots')

                MessageBot = await conv.get_response()
                if str(MessageBot.message).startswith('⛔️ Oh no! There are NO TASKS available at the moment.'):
                    await asyncio.sleep(2)
                    break
                else:
                    Bot_id, start_bot = (MessageBot.reply_markup.rows[0].buttons[0].url).replace('https://t.me/', '').split('?')[0], await MessageBot.click(text='🤖 Start the Bot 🤖')
                    try:
                        try:
                            unban = await event.client(UnblockRequest(id=Bot_id))
                        except:
                            pass
                        StartTheTargetBot, confirm, Sleep = await event.client.send_message(entity=Bot_id, message='/start'), await MessageBot.click(text='✅ Started'), await asyncio.sleep(1)
                        Message = await event.client(GetHistoryRequest(peer=Bot_id, offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
                        Forward = await event.client(ForwardMessagesRequest(from_peer=Bot_id, to_peer=bot_username, id=[Message.messages[0].id]))
                        DeleteBot = await event.client(DeleteHistoryRequest(peer=Bot_id, max_id=0, just_clear=True, revoke=True))
                    except Exception as error:
                        await conv.send_message('🔙 Back')
                        await conv.send_message('🤖 Message Bots')
                        MessageBot = await conv.get_response()
                        Skip = await MessageBot.click(text='➡️ Skip')
            await asyncio.sleep(2)
              
    # Join Channels
    async def JoinChannels():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('📣 Join Channels')
                    
                MessageBot = await conv.get_response()
                if str(MessageBot.message).startswith('⛔️ Oh no! There are NO TASKS available at the moment.'):
                    await asyncio.sleep(2)
                    break
                else:
                    channel_id = (MessageBot.reply_markup.rows[0].buttons[0].url).replace('https://t.me/', '').split('?')[0]
                    try:
                        if "+" in channel_id:
                            channel_ID = channel_id.replace("+", "").strip()
                            Join = await event.client(ImportChatInviteRequest(hash=channel_ID))
                        else:
                            join = await event.client(JoinChannelRequest(channel=channel_id))
                    except:
                        pass
                    watched, Sleep = await MessageBot.click(text='✅ Joined'), await asyncio.sleep(1)
                    try:
                        leave = await event.client(LeaveChannelRequest(channel=channel_id))
                    except:
                        pass
            await asyncio.sleep(2)
                        
    # Watch posts
    async def WatchPosts():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('👁 Views Posts')
                    
                MessageBot = await conv.get_response()
                if str(MessageBot.message).startswith('⛔️ Oh no! There are NO TASKS available at the moment.'):
                    await asyncio.sleep(2)
                    break
                else:
                    Watching, watched = await asyncio.sleep(2), await MessageBot.click(text='✅ Watched')
            await asyncio.sleep(2)

             
    visitWebsites = await VisitWebsites()
    Message__Bots = await MessageBotsForward()
    Join_Channels = await JoinChannels()
    Watch___Posts = await WatchPosts()
        
        
        
