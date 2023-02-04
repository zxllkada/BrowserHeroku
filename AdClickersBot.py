from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.contacts import UnblockRequest

from Detectors import DetectAnimals, DetectEmoji, DelectNumbers, DelectText
from bypass_faucet import *


# Create a browser
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
		
	
    	
async def AdClickersBot(event):
    bot_username = "@adclickersbot"
    
    # join chats
    async def AdClickersBot_JoinChats():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('📢 Join Chats')
                Channel = await conv.get_response()
                
                if "✅ Task Completed !" in str(Channel.text) or "✅ Success ! 👍" in str(Channel.text):
                    pass
                elif 'Press the **"📣 Join Chat"** button below.' in str(Channel.text):
                    Channel_id = (Channel.reply_markup.rows[0].buttons[0].url).replace('https://t.me/', '').split('?')[0]
                    try:
                        if "+" in Channel_id:
                            Channel_hash = Channel_id.replace('+', '')
                            Join = await event.client(ImportChatInviteRequest(hash=Channel_hash))
                        else:
                            Join = await event.client(JoinChannelRequest(channel=Channel_id))
                    except:
                        pass
                    Sleep, Confirm = await asyncio.sleep(1), await Channel.click(1)
                elif '😔 Sorry, there are no task available.' in str(Channel.text):
                    Sleep = await asyncio.sleep(2)
                    break
                else:
                    text_button_1, text_button_2, text_button_3, text_button_4 = Channel.reply_markup.rows[0].buttons[0].text, Channel.reply_markup.rows[0].buttons[1].text, Channel.reply_markup.rows[1].buttons[0].text, Channel.reply_markup.rows[1].buttons[1].text
                    
                    if "Tap The Matching **Animal** Below" in str(Channel.text):
                        captcha_answer = await DetectAnimals(event, Channel)
                    elif "Tap The Matching **Emoji** Below" in str(Channel.text):
                        captcha_answer = await DetectEmoji(event, Channel, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Number** Below" in str(Channel.text):
                        captcha_answer = await DelectNumbers(event, Channel, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Text** Below" in str(Channel.text):
                        captcha_answer = await DelectText(event, Channel, text_button_1, text_button_2, text_button_3, text_button_4)
                    else:
                        captcha_answer = None
                    
                    if captcha_answer != None:
                        SolveCaptcha, Sleep = await Channel.click(text=captcha_answer), await asyncio.sleep(2)
                        
            await asyncio.sleep(2)
                        
    
    # join bots
    async def AdClickersBot_JoinBots():
        while True:
            async with event.client.conversation(bot_username, timeout=10) as conv:
                await conv.send_message('🤖 Message Bots')
                Bot_data = await conv.get_response()
                
                if "✅ Task Completed !" in str(Bot_data.text):
                    pass
                elif 'Press the **"✉️ Message Bot"** button below.' in str(Bot_data.text):
                    Bot_id = (Bot_data.reply_markup.rows[0].buttons[0].url).replace('https://t.me/', '').split('?')[0]
                    try:
                        unban = await event.client(UnblockRequest(id=Bot_id))
                    except:
                        pass
                    
                    StartBot, Start, Sleep = await Bot_data.click(text="✅ Started"),await event.client.send_message(entity=Bot_id, message='/start'), await asyncio.sleep(1)
                    Message = await event.client(GetHistoryRequest(peer=Bot_id, offset_id=0, offset_date=None, add_offset=0, limit=1, max_id=0, min_id=0, hash=0))
                    Forward = await event.client(ForwardMessagesRequest(from_peer=Bot_id, to_peer=bot_username, id=[Message.messages[0].id]))
                    DeleteBot = await event.client(DeleteHistoryRequest(peer=Bot_id, max_id=0, just_clear=True, revoke=True))
            
                elif '😔 Sorry, there are no task available.' in str(Bot_data.text):
                    Sleep = await asyncio.sleep(2)
                    break
                else:
                    text_button_1, text_button_2, text_button_3, text_button_4 = Bot_data.reply_markup.rows[0].buttons[0].text, Bot_data.reply_markup.rows[0].buttons[1].text, Bot_data.reply_markup.rows[1].buttons[0].text, Bot_data.reply_markup.rows[1].buttons[1].text
                    
                    if "Tap The Matching **Animal** Below" in str(Bot_data.text):
                        captcha_answer = await DetectAnimals(event, Bot_data)
                    elif "Tap The Matching **Emoji** Below" in str(Bot_data.text):
                        captcha_answer = await DetectEmoji(event, Bot_data, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Number** Below" in str(Bot_data.text):
                        captcha_answer = await DelectNumbers(event, Bot_data, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Text** Below" in str(Bot_data.text):
                        captcha_answer = await DelectText(event, Bot_data, text_button_1, text_button_2, text_button_3, text_button_4)
                    else:
                        captcha_answer = None
                    
                    if captcha_answer != None:
                        SolveCaptcha, Sleep = await Bot_data.click(text=captcha_answer), await asyncio.sleep(2)
                        
            await asyncio.sleep(2)
    
    # view posts
    async def AdClickersBot_ViewPosts():
        while True:
            async with event.client.conversation(bot_username, timeout=20) as conv:
                await conv.send_message('📄 View Posts')
                ViewAd = await conv.get_response()
                
                if "✅ Task Completed !" in str(ViewAd.text):
                    pass
                elif 'Press the **"📄 View Post"** button below.' in str(ViewAd.text):
                    View, Sleep = await ViewAd.click(text="📄 View Post"), await asyncio.sleep(12)
                elif '😔 Sorry, there are no task available.' in str(ViewAd.text):
                    Sleep = await asyncio.sleep(2)
                    break
                else:
                    text_button_1, text_button_2, text_button_3, text_button_4 = ViewAd.reply_markup.rows[0].buttons[0].text, ViewAd.reply_markup.rows[0].buttons[1].text, ViewAd.reply_markup.rows[1].buttons[0].text, ViewAd.reply_markup.rows[1].buttons[1].text
                    
                    if "Tap The Matching **Animal** Below" in str(ViewAd.text):
                        captcha_answer = await DetectAnimals(event, ViewAd)
                    elif "Tap The Matching **Emoji** Below" in str(ViewAd.text):
                        captcha_answer = await DetectEmoji(event, ViewAd, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Number** Below" in str(ViewAd.text):
                        captcha_answer = await DelectNumbers(event, ViewAd, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Text** Below" in str(ViewAd.text):
                        captcha_answer = await DelectText(event, ViewAd, text_button_1, text_button_2, text_button_3, text_button_4)
                    else:
                        captcha_answer = None
                    
                    if captcha_answer != None:
                        SolveCaptcha, Sleep = await ViewAd.click(text=captcha_answer), await asyncio.sleep(2)
        
            await asyncio.sleep(2)
    
    # visit links
    async def AdClickersBot_VisitLinks():
        while True:
            async with event.client.conversation(bot_username, timeout=300) as conv:
                await conv.send_message('🖥 Visit Sites')

                rewardMSG = await conv.get_response()
                if str(rewardMSG.text).startswith('ℹ️ There are no more ads available.'):
                    await asyncio.sleep(2)
                    break
                else:
                    try:
                        # browser = createDriver()
                        # browser.get(rewardMSG.reply_markup.rows[0].buttons[0].url)
                        # await asyncio.sleep(165)
                        break
                    except:
                        pass
                    
                    text_button_1, text_button_2, text_button_3, text_button_4 = rewardMSG.reply_markup.rows[0].buttons[0].text, rewardMSG.reply_markup.rows[0].buttons[1].text, rewardMSG.reply_markup.rows[1].buttons[0].text, rewardMSG.reply_markup.rows[1].buttons[1].text
                    
                    if "Tap The Matching **Animal** Below" in str(rewardMSG.text):
                        captcha_answer = await DetectAnimals(event, rewardMSG)
                    elif "Tap The Matching **Emoji** Below" in str(rewardMSG.text):
                        captcha_answer = await DetectEmoji(event, rewardMSG, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Number** Below" in str(rewardMSG.text):
                        captcha_answer = await DelectNumbers(event, rewardMSG, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Text** Below" in str(rewardMSG.text):
                        captcha_answer = await DelectText(event, rewardMSG, text_button_1, text_button_2, text_button_3, text_button_4)
                    else:
                        captcha_answer = None
                    
                    if captcha_answer != None:
                        SolveCaptcha, Sleep = await rewardMSG.click(text=captcha_answer), await asyncio.sleep(2)
                    
            await asyncio.sleep(2)
    
    # faucet captcha
    async def AdClickersBot_Faucet():
        while True:
            async with event.client.conversation(bot_username, timeout=20) as conv:
                await conv.send_message('🎁 Faucet')

                rewardMSG = await conv.get_response()
                if str(rewardMSG.text).startswith('🎁 Claim faucet every 15 minutes.'):
                    reward_url = rewardMSG.reply_markup.rows[0].buttons[0].url
                    try_solving = await SolveCaptchaBrowser(reward_url)
                    is_rewarded = await conv.get_response()
                    if "🎁 You claimed faucet successfully!" in is_rewarded.text:
                        RewardInfo = await event.client.send_message(entity="zkada", message=is_rewarded.text)
                        break
                elif "Please wait for" in rewardMSG.text:
                    sleep_for = (rewardMSG.text).replace("🕐 Please wait for **", "").split("m:")[0]
                    await asyncio.sleep(int(sleep_for)*60)
                    break
                else:
                    text_button_1, text_button_2, text_button_3, text_button_4 = rewardMSG.reply_markup.rows[0].buttons[0].text, rewardMSG.reply_markup.rows[0].buttons[1].text, rewardMSG.reply_markup.rows[1].buttons[0].text, rewardMSG.reply_markup.rows[1].buttons[1].text
                    
                    if "Tap The Matching **Animal** Below" in str(rewardMSG.text):
                        # captcha_answer = await DetectAnimals(event, rewardMSG)
                        captcha_answer = None
                    elif "Tap The Matching **Emoji** Below" in str(rewardMSG.text):
                        captcha_answer = await DetectEmoji(event, rewardMSG, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Number** Below" in str(rewardMSG.text):
                        captcha_answer = None
                        #captcha_answer = await DelectNumbers(event, rewardMSG, text_button_1, text_button_2, text_button_3, text_button_4)
                    elif "Tap The Matching **Text** Below" in str(rewardMSG.text):
                        captcha_answer = None
                        #captcha_answer = await DelectText(event, rewardMSG, text_button_1, text_button_2, text_button_3, text_button_4)
                    else:
                        captcha_answer = None
                    
                    if captcha_answer != None:
                        SolveCaptcha, Sleep = await rewardMSG.click(text=captcha_answer), await asyncio.sleep(2)
                    
            await asyncio.sleep(2)
    
    # Join_Chats = await AdClickersBot_JoinChats()
    # await asyncio.sleep(5)
    # Join__Bots = await AdClickersBot_JoinBots()
    # await asyncio.sleep(5)
    # View_Posts = await AdClickersBot_ViewPosts()
    # await asyncio.sleep(5)
    # VisitLinks = await AdClickersBot_VisitLinks()
    # await asyncio.sleep(5)
    Faucet____ = await AdClickersBot_Faucet()
    
    
    