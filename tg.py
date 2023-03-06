import datetime
import random
import time
from pprint import pprint
import config
import telepot
from sql_connection import register
from sql_connection import on_button_press
from sql_connection import stats
from sql_connection import avs
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup



def on_chat_message(msg):
    chat_id = msg['chat']['id']
    tokenized_text = msg['text'].split()
    command = tokenized_text[0]
    user_id = msg['chat']['id']
    username = msg['chat']['username']

    if command == '/dado':
        max_n = 6  
        if len(tokenized_text) > 1:
            max_n = int(tokenized_text[1])     
        bot.sendMessage(chat_id, random.randint(1, max_n))       
    
    if command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    
    if command == '/start':
        if username == "":
            bot.sendMessage(chat_id, "per iniziare inserisci un username")
        else:
            register(bot, chat_id, user_id, username)
    
    if command == '/raccogli':
        register(bot, chat_id, user_id, username)
        on_button_press(bot, chat_id, user_id,)
    
    if command == '/stats':
        register(bot, chat_id, user_id, username)
        stats(bot, chat_id, user_id)

    if command == '/tira':
        register(bot, chat_id, user_id, username)
        if len(tokenized_text) > 1:
            avversario = tokenized_text[1] 
            avs(bot, chat_id, user_id, avversario, username)
        else:
            bot.sendMessage(chat_id, "a chi vuoi tirare la palla di neve?")


bot = telepot.Bot(config.TOKEN)
bot.message_loop({'chat': on_chat_message})

while 1:
    time.sleep(10)