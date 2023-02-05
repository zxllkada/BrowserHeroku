from telethon import TelegramClient, events
import asyncio

# HandyBot
from HandyBot import *
from AdClickersBot import *
from ClickBee import *
from HkBot import *

# DATA
api_id = 1724716
api_hash = "00b2d8f59c12c1b9a4bc63b70b461b2f"

iqthon = TelegramClient("Kada", api_id, api_hash)
iqthon.start()


# ACTIVE SCRIPTS
HandyBtc, AdClickers, ClickBee, HkBot = False, False, False, False

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
            
###############################################################################
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'start script clickbee'))
async def ClickBeeActive(event):
    global ClickBee
    ClickBee, reply = True, await event.reply('**script clickbee started**')
    run = await clickbee_earn(event)
    
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'stop script clickbee'))
async def ClickBeeUnActive(event):
    global ClickBee
    ClickBee, reply = False, await event.reply('**script clickbee stopped**')

async def clickbee_earn(event):
    global ClickBee
    
    if ClickBee == True:
        while True:
            if ClickBee == False:
                break
            try:
                start = await ClickBee_Function(event)
            except Exception as error:
                print (error)
                pass
            await asyncio.sleep(30)
            
###############################################################################
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'start script hk_usdt'))
async def HkUsdtActive(event):
    global HkBot
    HkBot, reply = True, await event.reply('**script hk_usdt started**')
    run = await hkearn_earn(event)
    
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'stop script hk_usdt'))
async def HkUsdtUnActive(event):
    global HkBot
    HkBot, reply = False, await event.reply('**script hk_usdt stopped**')

async def hkearn_earn(event):
    global HkBot
    
    if HkBot == True:
        while True:
            if HkBot == False:
                break
            try:
                start = await HkEarn_Function(event)
            except Exception as error:
                print (error)
                pass
            await asyncio.sleep(30)











            
# RUN
iqthon.run_until_disconnected()