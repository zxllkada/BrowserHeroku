import keras, cv2, asyncio, os
from keras.applications import ResNet50
import keras.utils as image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import numpy as np

import pytesseract
from PIL import Image
import difflib

from telethon.tl.functions.messages import GetEmojiKeywordsRequest


# only for windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
model = ResNet50(weights='imagenet')

async def DetectAnimals(event, media):
    Image_path = await event.client.download_media(media)
    img = image.load_img(Image_path, target_size=(224, 224, 0))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    predicted_class = decode_predictions(preds, top=1)
    animal_name = predicted_class[0][0][1]

    if "cat" == animal_name.lower() or "tabby" == animal_name.lower():
        animal_name = 'cat'
    elif "dog" == animal_name.lower() or "golden_retriever" == animal_name.lower() or "dingo" == animal_name.lower():
        animal_name = 'dog'
    elif "camel" == animal_name.lower() or "Arabian_camel" == animal_name.lower():
        animal_name = 'camel'
    elif "rabbit" == animal_name.lower() or "hare" == animal_name.lower():
        animal_name = 'rabbit'
    elif "cow" == animal_name.lower() or "ox" == animal_name.lower():
        animal_name = 'cow'
    elif "elephant" == animal_name.lower():
        animal_name = 'elephant'
    elif "lion" == animal_name.lower():
        animal_name = 'lion'
    elif "tiger" == animal_name.lower():
        animal_name = 'tiger'
    elif "fox" == animal_name.lower() or "red_fox" == animal_name.lower():
        animal_name = 'fox'
    elif "monkey" == animal_name.lower() or "macaque" == animal_name.lower():
        animal_name = 'monkey'
    elif "horse" == animal_name.lower() or "sorrel" == animal_name.lower():
        animal_name = 'horse'
    elif "deer" == animal_name.lower() or "ibex" == animal_name.lower() or "gazelle" == animal_name.lower():
        animal_name = 'deer'
    elif "snake" == animal_name.lower():
        animal_name = 'snake'
    elif "kangaroo" == animal_name.lower() or "wallaby" == animal_name.lower():
        animal_name = 'kangaroo'
    elif "spider" == animal_name.lower() or "tarantula" == animal_name.lower() or "black_and_gold_garden_spider" == animal_name.lower() or "barn_spider" == animal_name.lower():
        animal_name = 'spider'
    elif "zebra" == animal_name.lower():
        animal_name = 'zebra'
    elif "panda" == animal_name.lower() or "giant_panda" == animal_name.lower():
        animal_name = 'panda'
    else:
        animal_name = None
        
    os.remove(Image_path)
    if animal_name != None:
        return animal_name.lower()
    else:
        return animal_name


async def DetectEmoji(event, media, emg1, emg2, emg3, emg4):
    global ghost_captcha
    
    captcha_answer = None
    from telethon.tl.functions.messages import GetEmojiKeywordsDifferenceRequest
    emojies = await event.client(GetEmojiKeywordsRequest(lang_code="en"))
    #emojies = await event.client(GetEmojiKeywordsDifferenceRequest(lang_code="en"))
    gif_code = await event.client.download_media(media)
    gif_code = gif_code.replace('.gif', '')
    for emoji in emojies.keywords:
        if emoji.keyword == gif_code.replace('_', ' '):
            ghost_captcha = emoji.emoticons
            break
        else:
            ghost_captcha = None
    
    emoij_list = [emg1, emg2, emg3, emg4]
    if ghost_captcha != None:
        for emoji_ in emoij_list:
            for emoji__ in ghost_captcha:
                if emoji_ == emoji__:
                    captcha_answer = emoji__
                    break
            if captcha_answer != None:
                break

    os.remove(f'{gif_code}.gif')
    return captcha_answer
            

async def DelectNumbers(event, media, num1, num2, num3, num4):
    captcha_answer = None
    
    Image_path = await event.client.download_media(media)
    image = Image.open(Image_path)
    text = pytesseract.image_to_string(image)
    
    try:
        if "+" in text:
            result = int(text.split('+')[0]) + int(text.split('+')[1])
        elif "-" in text:
            result = int(text.split('-')[0]) - int(text.split('-')[1])
        else:
            result = None
    except:
        result = None
        
    number_list = [num1, num2, num3, num4]
    if result != None:
        for number in number_list:
            if int(number) == int(result):
                captcha_answer = number
                break
        
    os.remove(Image_path)
    return captcha_answer

async def DelectText(event, media, tx1, tx2, tx3, tx4):
    captcha_answer = None
    Image_path = await event.client.download_media(media)
    
    image = Image.open(Image_path)
    scraped_text = pytesseract.image_to_string(image)

    text_list = [tx1, tx2, tx3, tx4]
    for text in text_list:
        if text == scraped_text:
            captcha_answer = text
            break
        
    scores = []
    if captcha_answer == None:
        for text in text_list:
            score = difflib.SequenceMatcher(None, text, scraped_text).ratio()
            scores.append(score)

    if captcha_answer == None:
        max_index = scores.index(max(scores))
        if scores[max_index] > 0.50:
            captcha_answer = text_list[max_index]

    os.remove(Image_path)
    return captcha_answer






