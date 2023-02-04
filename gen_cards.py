from telethon import TelegramClient, events
from telethon.tl.types import ReplyInlineMarkup
from telethon.tl.types import KeyboardButtonRow
from telethon.tl.types import KeyboardButtonUrl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

from faker import Faker
import requests, json, asyncio, os

faker = Faker()

# BOT
api_id_bot = 1724716
api_hash_bot = "00b2d8f59c12c1b9a4bc63b70b461b2f"
bot = TelegramClient("Bot_", api_id_bot, api_hash_bot).start(bot_token="1751690617:AAEl--WKu-cL6pEY9XR8-CgkjXISq34cKNs")
#######################################################################################################################
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
    "referer": "https://checker.stery.dev/en.php"
}

Cards_Datails = {}

driver_path = os.environ.get("GOOGLEDRIVER_PATH")
options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
    
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")



async def gen_cards(began_with):
    global Cards_Datails

    card_list = []
    while True:
        card_details = faker.credit_card_full(card_type="mastercard")
        card_type = card_details.split('\n')[0]
        card_holder_name = card_details.split('\n')[1]
        card_number = (card_details.split('\n')[2]).split(' ')[0]
        card_expired = (card_details.split('\n')[2]).split(' ')[1]
        card_cvv = (card_details.split('\n')[3]).replace('CVV:', '').strip()

        card_number = str(began_with) + card_number[len(began_with):]
        if card_number.startswith('5'):
            Cards_Datails[card_number] = {
                "number": card_number,
                "holder": card_holder_name,
                "expired": card_expired,
                "card_cvv": card_cvv
            }

            card_list.append(f'{card_number}|{card_expired.split("/")[0]}|20{card_expired.split("/")[1]}|{card_cvv}')

        if len(card_list) == 20:
            break
    return card_list

async def checker(event, cards_list, reply):
    global Cards_Datails

    checker_api, cards_list_new, live_cards = "https://www.xchecker.cc/api.php?cc=", cards_list, []
    checker_api2 = "https://checker.stery.dev/_tPMe95FrZ1-n2egB9rU5hDf_.php"

    for x, card_data in enumerate(cards_list, start=1):
        try:
            check_ = requests.post(checker_api2, data={"ajax": "1", "do": "check", "sB34zPxaApw2": card_data}, headers=headers)
            data_ = json.loads(str(check_.text))
            print (check_)
        except Exception as error:
            data_ = {"server": "invalid"}
        check = requests.post(checker_api+card_data)
        data = json.loads(str(check.text))

        if data_.get("server") == "working":
            index = cards_list.index(card_data)
            cards_list_new[index] = f'{card_data} -- ✅ Live'
            live_cards.append(card_data)
        elif data.get("status") == "Live":
            index = cards_list.index(card_data)
            cards_list_new[index] = f'{card_data} -- ✅ Live'
            live_cards.append(card_data)
        elif data.get("status") == "Dead":
            index = cards_list.index(card_data)
            cards_list_new[index] = f'{card_data} -- ❌ Dead'
        else:
            index = cards_list.index(card_data)
            cards_list_new[index] = f'{card_data} -- ❕ Unknown'

        Cards = await update_message_cards(cards_list_new)
        edit = await reply.edit(f'**Amount :** `{len(cards_list)}`\n**Card type :** __MasterCard__\n\n`{Cards}`\n\n__⏳ Automated checking **{x}/{len(cards_list)}**__')
    edit = await reply.edit(f'**Amount :** `{len(cards_list)}`\n**Card type :** __MasterCard__\n\n`{Cards}`\n\n__✅ Finished **{x}/{len(cards_list)}**__')
    if len(live_cards) != 0:
        for live_card in live_cards:
            Card_Datail = Cards_Datails.get(live_card.split('|')[0])
            card_info = f"https://dnschecker.org/ajax_files/credit_card_validator.php?ccn={Card_Datail.get('number')}"
            data = json.loads(card_info)
            print (data)
            
            reply = await event.reply(f'🎉 Approved : Mastercard **Approved :** __Mastercard__\n\n**Card Number :** `{Card_Datail.get("number")}`\n**Holder Name :** `{Card_Datail.get("holder")}`\n**Expires in :** `{Card_Datail.get("expired")}`\n**CVV :** `{Card_Datail.get("card_cvv")}`\n**Country :** __{data.get("results").get("country")}__\n**Bank :** __{data.get("results").get("bank")}__\n**Card type :** __{data.get("results").get("card_type")}__')


async def update_message_cards(cards_list):
    Cards = ''
    for card in cards_list:
        Cards = f'{Cards}{card}\n'
    return Cards



async def new_gen(began_with):
    global Cards_Datails
    
    card_list = []

    # Initialize the webdriver
    #driver_path = "chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    
    #Navigate to the website
    driver.get("https://outputter.io/bin-generator/")
    input_bin = driver.find_element(By.XPATH, '//*[@id="content"]/section[3]/div/div[1]/form/div[3]/div/input').send_keys(began_with)
    await asyncio.sleep(3)
    generate = driver.find_element(By.XPATH, '//*[@id="content"]/section[3]/div/div[1]/form/div[5]/div/button').click()
    await asyncio.sleep(3)
    
    textarea = driver.find_element(By.XPATH, '//*[@id="content"]/section[3]/div/div[2]/div')
    generated_cards = (textarea.text).split('\n')
    driver.quit()
    
    for card in generated_cards:
        Cards_Datails[card.split('|')[0]] = {
            "number": card.split('|')[0],
            "expired": f"{card.split('|')[1]}/{card.split('|')[2]}",
            "card_cvv": card.split('|')[3],
            "card_type": card.split('|')[4]
        }
        
        formated = f'{card.split("|")[0]}|{card.split("|")[1]}|{card.split("|")[2]}|{card.split("|")[3]}'
        card_list.append(formated)
        
    return card_list



# MESSAGE ORDER
@bot.on(events.NewMessage(pattern="/gen ?(.*)"))
async def AnOrder(event):
    if event.is_private == False:
        began_with = (event.message.message).replace("/gen", "").strip()
        if began_with != "":
            reply = await event.reply('**⏳ working on it**')
            #cards_list = await gen_cards(began_with)
            cards_list = await new_gen(began_with)
            Cards = await update_message_cards(cards_list)
            edit = await reply.edit(f'**Amount :** `{len(cards_list)}`\n**Card type :** __MasterCard__\n\n`{Cards}`\n\n__⏳ Automated checking **0/{len(cards_list)}**__')
            check = await checker(event, cards_list, reply)
        else:
            reply = await event.reply('**format is -> /gen {bin}\n\nEx : `/gen 520047`**')




bot.run_until_disconnected()
