#!/usr/bin/env python3
import requests
import time
import schedule


def telegram_bot_sendtext(bot_message):
    bot_token = '1755134661:AAE4ysHFi75lUqF2o2H_Fs3Or3jHDlfKUjM'
    bot_chatID = '597759896'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    print(send_text)
    response = requests.get(send_text)

    return response.json()

test = telegram_bot_sendtext("Testing Telegram bot")
print(test)