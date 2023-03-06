import datetime
import random
import sys
import time
from pprint import pprint
import config
import telepot
from sql_connection import register
from sql_connection import raccogli
from sql_connection import info
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
        raccogli(bot, chat_id, user_id)
    
    if command == '/info':
        register(bot, chat_id, user_id, username)
        info(bot, chat_id, user_id)

    if command == '/tira':
        register(bot, chat_id, user_id, username)
        if len(tokenized_text) > 1:
            avversario = tokenized_text[1] 
            avs(bot, chat_id, user_id, avversario, username)
        else:
            bot.sendMessage(chat_id, "a chi vuoi tirare la palla di neve?")



            
    '''
    if command == '/numeri' and game == True:
        r = random.randint(1, 100)
        print(r)
        indovinato = False                
        t = 3
        bot.sendMessage(chat_id, "indovina il numero, hai %s tentativi " % (t))
        bot.sendMessage(chat_id, "che numero scegli? ")

        n = command
        print(n)
        while t > 0 and indovinato == False:

            if command == n:
                if n.isnumeric() == True:
                    n = int(n)
                    t -= 1
                    if n == r:
                        indovinato = True
                    elif n < r and t > 0:
                        bot.sendMessage(chat_id, "hai sbagliato, il numero che cerchi è più grande")
                    elif n > r and t > 0:
                        bot.sendMessage(chat_id, "hai sbagliato, il numero che cerchi è più piccolo")
                else:
                    bot.sendMessage(chat_id, "%s" % command)

        if indovinato == True:
            bot.sendMessage(chat_id, "hai vinto! Il numero era %s" % (r))
            game = False

        else:
            bot.sendMessage(chat_id, "hai perso, il numero era %s" % (r))
            game = False
    #    numeri(msg)
       '''
    


bot = telepot.Bot(config.TOKEN)
bot.message_loop({'chat': on_chat_message})

while 1:
    time.sleep(10)