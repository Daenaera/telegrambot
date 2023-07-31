import mysql.connector
import config
import datetime
import random

SQL_HOST = config.SQL_HOST
SQL_PORT = config.SQL_PORT
SQL_USER = config.SQL_USER
SQL_PASSWORD = config.SQL_PASSWORD
SQL_DATABASE = config.SQL_DATABASE

def db_connection(func):
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DATABASE)
# Stampa dell'handle di connessione
# Generazione del cursore
        cursor = conn.cursor()
# Comando SQL per la visualizzazione dei database
        try:
            result = func(cursor, *args, **kwargs)
            conn.commit()
            return result
        finally:
            cursor.close()
            conn.close()
    return wrapper
  

@db_connection
def register(bot, chat_id, username):
    
    sql = 'SELECT * FROM players WHERE chat_id = %s'
    
    cursor.execute(sql, [chat_id])
    myresult = cursor.fetchall()

    if len(myresult) == 1:
       print(datetime.datetime.now())
       return True
    else:
       sql = 'INSERT INTO players(registration_date, chat_id, username, HP, balls, pozioni) VALUES(%s, %s, %s, %s, %s, %s)'
       cursor.execute(sql, [datetime.datetime.now(), chat_id, username, 100, 0, 0])
       db.commit()
       bot.sendMessage(chat_id, "Ti sei registrato")




time_threshold = datetime.timedelta(minutes=15)

# variabile per tenere traccia dell'ultimo momento in cui il tasto è stato premuto
last_pressed_time = None

def on_button_press(bot, chat_id):
    global last_pressed_time

    current_time = datetime.datetime.now()

    # controllare se il tasto può essere premuto o meno
   # if last_pressed_time is None or current_time - last_pressed_time >= time_threshold:
        # il tasto può essere premuto
    #    last_pressed_time = current_time
    random(bot, chat_id)
    #else:
        # non sono ancora passati 15 minuti dall'ultima volta che il tasto è stato premuto
     #   remaining_time = last_pressed_time + time_threshold - current_time
     #   bot.sendMessage(chat_id, "Puoi raccogliere tra " + str(remaining_time.seconds // 60) + " minuti")


def random(bot, chat_id):
   import random
   prob = random.randint(1, 7)
   if prob == 5:
      pozioni(bot, chat_id)
   else:
      palla(bot, chat_id)


@db_connection
def pozioni(bot, chat_id):
   
   sql = 'SELECT pozioni FROM players WHERE chat_id = %s'
    
   cursor.execute(sql, [chat_id])
   myresult = cursor.fetchone()

   pozioni = myresult[0]
   pozioni += 1
   sql = 'UPDATE players SET pozioni = %s WHERE chat_id = %s'
   cursor.execute(sql, [pozioni, chat_id])
   db.commit()
   bot.sendMessage(chat_id, "Hai trovato una pozione!")



@db_connection
def palla(bot, chat_id):

   sql = 'SELECT balls FROM players WHERE chat_id = %s'
    
   cursor.execute(sql, [chat_id])
   myresult = cursor.fetchone()

   balls = myresult[0]
   balls += 1
   sql = 'UPDATE players SET balls = %s WHERE chat_id = %s'
   cursor.execute(sql, [balls, chat_id])
   db.commit()
   bot.sendMessage(chat_id, "Hai raccolto una palla di neve!")


@db_connection
def usa(bot, chat_id):
   sql = 'SELECT pozioni FROM players WHERE chat_id = %s'
    
   cursor.execute(sql, [chat_id])
   myresult = cursor.fetchone()

   pozioni = myresult[0]
   if pozioni > 0:
      pozioni -= 1
      sql = 'UPDATE players SET pozioni = %s WHERE chat_id = %s'

      cursor.execute(sql, [pozioni, chat_id])

      punti = 'SELECT HP FROM players WHERE chat_id = %s'
      cursor.execute(punti, [chat_id])
      myresult = cursor.fetchone()

      HP = myresult[0]
      HP += 50
      punti = 'UPDATE players SET HP = %s WHERE chat_id = %s'

      cursor.execute(punti, [HP, chat_id])
      db.commit()
      bot.sendMessage(chat_id, "Hai recuperato 50 punti vita")
   
   else:
         bot.sendMessage(chat_id, "Non hai pozioni da usare")
   


@db_connection
def stats(bot, chat_id):

   sql = 'SELECT * FROM players WHERE chat_id = %s'
    
   cursor.execute(sql, [chat_id])
   myresult = cursor.fetchone()
   print(myresult)
   bot.sendMessage(chat_id, "\nusername: " + myresult[3] + "\npunti vita: " + str(myresult[4]) + "\npalle di neve: " + str(myresult[5]) + "\npozioni: " + str(myresult[6]))


      
@db_connection
def pg(bot, chat_id, avversario, username):

   pv = 'SELECT HP FROM players WHERE chat_id = %s'
   cursor.execute(pv, [chat_id])
   myresult = cursor.fetchone()
   HP = myresult[0]
   print("pg HP: ", HP)
   if HP < 1:
      bot.sendMessage(chat_id, "Non puoi lanciare palle da morto")
   else:
      ball = 'SELECT balls FROM players WHERE chat_id = %s'
      cursor.execute(ball, [chat_id])
      myresult = cursor.fetchone()
      balls = myresult[0]
      if balls < 1:
         bot.sendMessage(chat_id, "Non hai palle da tirare")
      else:
         print(avversario)
         tira(bot, chat_id,  avversario)
         ricevi(bot, avversario, username)



@db_connection      
def avs(bot, chat_id, avversario, username):

   avv = 'SELECT * FROM players WHERE username = %s'
   cursor.execute(avv, [avversario])
   myresult = cursor.fetchone()
    
   if myresult is not None:
      pv = 'SELECT HP FROM players WH:ERE username = %s'
      cursor.execute(pv, [avversario])
      myresult = cursor.fetchone()
      HP = myresult[0]
      print("HP avs1: ", HP)
      if HP < 1:
         bot.sendMessage(chat_id, "il tuo avversario è già morto")
      else:
         pg(bot, chat_id, avversario, username)
         
   else:
      bot.sendMessage(chat_id, "avversario non trovato")


@db_connection
def tira(bot, chat_id, avversario):

   ball = 'SELECT balls FROM players WHERE chat_id = %s'
   cursor.execute(ball, [chat_id])
   myresult = cursor.fetchone()
   balls = myresult[0]
   balls -= 1
   sql = 'UPDATE players SET balls = %s WHERE chat_id = %s'
   cursor.execute(sql, [balls, chat_id])
   db.commit()
   bot.sendMessage(chat_id, "Hai tirato una palla di neve a %s" % avversario)


@db_connection
def ricevi(bot, avversario, username):

   pv = 'SELECT HP FROM players WHERE username = %s'
   cursor.execute(pv, [avversario])
   myresult = cursor.fetchone()
   HP = myresult[0]
   print("HP avs2: ", HP)
   HP -= 10
   upd = 'UPDATE players SET HP = %s WHERE username = %s'
   cursor.execute(upd, [HP, avversario])
   avv_chat_id = 'SELECT chat_id FROM players WHERE username = %s'
   cursor.execute(avv_chat_id, [avversario])
   myresult = cursor.fetchone()
   avv_chat_id = myresult[0]
   db.commit()
   bot.sendMessage(avv_chat_id, "%s ti ha tirato una palla di neve\nhai perso 10 HP!" % username)


@db_connection
def lista(cursor, bot, chat_id):
    sql = 'SELECT username FROM players'
    cursor.execute(sql)
    results = cursor.fetchall()

    if results:
        usernames = [result[0] for result in results]
        message = "Giocatori: \n- " + "\n- ".join(usernames)
    else:
        message = "Nessun giocatore trovato nella lista."

    bot.sendMessage(chat_id, message)
