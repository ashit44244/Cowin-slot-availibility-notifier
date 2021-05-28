#!/usr/bin/env python3
import requests
import time
import schedule

def telegram_bot_sendtext(bot_message, bot_chatID):

    bot_token = '1755134661:AAHAXJhDZfdinst1gzqp6MCpT9EAnYKDBUY'
    # cowin U45 bangalore chat id
    #bot_chatID = '-1001129827963'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID +\
                '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


#test = telegram_bot_sendtext("Testing Telegram bot")
#print(test)