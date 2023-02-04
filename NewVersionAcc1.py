from telethon import TelegramClient, events
import asyncio

# HandyBot
from HandyBot import *
from AdClickersBot import *

# DATA
api_id = 1724716
api_hash = "00b2d8f59c12c1b9a4bc63b70b461b2f"

iqthon = TelegramClient("Acc1", api_id, api_hash)
iqthon.start()


# ACTIVE SCRIPTS
HandyBtc, AdClickers = False, False

#############################################################################################
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'start script handybtc'))
async def HandyBtcActive(event):
    global HandyBtc
    HandyBtc, reply = True, await event.reply('**script handybtc started**')
    run = await handybtc_earn(event)
    
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'stop script handybtc'))
async def HandyBtcUnActive(event):
    global HandyBtc
    HandyBtc, reply = False, await event.reply('**script handybtc stopped**')
    
async def handybtc_earn(event):
    global HandyBtc
    
    if HandyBtc == True:
        while True:
            if HandyBtc == False:
                break
            try:
                start = await HandyBot_Clickers(event)
            except Exception as error:
                print (error)
                pass
            await asyncio.sleep(120)
###############################################################################################
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'start script adclickers'))
async def AdClickersActive(event):
    global AdClickers
    AdClickers, reply = True, await event.reply('**script adclickers started**')
    run = await adclickers_earn(event)
    
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'stop script adclickers'))
async def AdClickersUnActive(event):
    global AdClickers
    AdClickers, reply = False, await event.reply('**script adclickers stopped**')

async def adclickers_earn(event):
    global AdClickers
    
    if AdClickers == True:
        while True:
            if AdClickers == False:
                break
            try:
                start = await AdClickersBot(event)
            except Exception as error:
                print (error)
                pass
            await asyncio.sleep(30)







            
# RUN
iqthon.run_until_disconnected()