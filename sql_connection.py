import mysql.connector
import pymysql
import config
import datetime
import random

SQL_HOST = config.SQL_HOST
SQL_PORT = config.SQL_PORT
SQL_USER = config.SQL_USER
SQL_PASSWORD = config.SQL_PASSWORD
SQL_DATABASE = config.SQL_DATABASE


connessione = mysql.connector.connect(
# Parametri per la connessione
  host=SQL_HOST,
  user=SQL_USER,
  password=SQL_PASSWORD,
  db=SQL_DATABASE
)

# Stampa dell'handle di connessione

# Generazione del cursore
cursor = connessione.cursor()
# Comando SQL per la visualizzazione dei database
#cursore.execute("SHOW DATABASES")
cursor.execute("SHOW COLUMNS FROM players FROM tg_db")
# Visualizzazione dei database

db = pymysql.connect(host=SQL_HOST, port=SQL_PORT, user=SQL_USER, passwd=SQL_PASSWORD, db=SQL_DATABASE)
cursor = db.cursor()

def register(bot, chat_id, user_id, username):
    
    sql = 'SELECT * FROM players WHERE user_id = %s'
    
    cursor.execute(sql, [user_id])
    myresult = cursor.fetchall()

    if len(myresult) == 1:
       return True
    else:
       sql = 'INSERT INTO players(registration_date, user_id, chat_id, username, HP, balls, pozioni) VALUES(%s, %s, %s, %s, %s, %s, %s)'
       cursor.execute(sql, [datetime.datetime.today(), user_id, chat_id, username, 100, 0, 0])
       db.commit()
       bot.sendMessage(chat_id, "Ti sei registrato")




time_threshold = datetime.timedelta(minutes=15)

# variabile per tenere traccia dell'ultimo momento in cui il tasto è stato premuto
last_pressed_time = None

def on_button_press(bot, chat_id, user_id):
    global last_pressed_time

    # ottenere il tempo corrente
    current_time = datetime.datetime.now()

    # controllare se il tasto può essere premuto o meno
   # if last_pressed_time is None or current_time - last_pressed_time >= time_threshold:
        # il tasto può essere premuto
    #    last_pressed_time = current_time
    random(bot, chat_id, user_id)
    #else:
        # non sono ancora passati 15 minuti dall'ultima volta che il tasto è stato premuto
     #   remaining_time = last_pressed_time + time_threshold - current_time
     #   bot.sendMessage(chat_id, "Puoi raccogliere tra " + str(remaining_time.seconds // 60) + " minuti")


def random(bot, chat_id, user_id):
   import random
   prob = random.randint(1, 7)
   if prob == 5:
      pozioni(bot, chat_id, user_id)
   else:
      palla(bot, chat_id, user_id)



def pozioni(bot, chat_id, user_id):
   
   sql = 'SELECT pozioni FROM players WHERE user_id = %s'
    
   cursor.execute(sql, [user_id])
   myresult = cursor.fetchone()

   pozioni = myresult[0]
   pozioni += 1
   sql = 'UPDATE players SET pozioni = %s WHERE user_id = %s'
   cursor.execute(sql, [pozioni, user_id])
   db.commit()
   bot.sendMessage(chat_id, "Hai trovato una pozione!")




def palla(bot, chat_id, user_id):

   sql = 'SELECT balls FROM players WHERE user_id = %s'
    
   cursor.execute(sql, [user_id])
   myresult = cursor.fetchone()

   balls = myresult[0]
   balls += 1
   sql = 'UPDATE players SET balls = %s WHERE user_id = %s'
   cursor.execute(sql, [balls, user_id])
   db.commit()
   bot.sendMessage(chat_id, "Hai raccolto una palla di neve!")


def usa(bot, chat_id, user_id):
   sql = 'SELECT pozioni FROM players WHERE user_id = %s'
    
   cursor.execute(sql, [user_id])
   myresult = cursor.fetchone()

   pozioni = myresult[0]
   if pozioni > 0:
      pozioni -= 1
      sql = 'UPDATE players SET pozioni = %s WHERE user_id = %s'

      cursor.execute(sql, [pozioni, user_id])

      punti = 'SELECT HP FROM players WHERE user_id = %s'
      cursor.execute(punti, [user_id])
      myresult = cursor.fetchone()

      HP = myresult[0]
      HP += 50
      punti = 'UPDATE players SET HP = %s WHERE user_id = %s'

      cursor.execute(punti, [HP, user_id])
      db.commit()
      bot.sendMessage(chat_id, "Hai recuperato 50 punti vita")
   
   else:
         bot.sendMessage(chat_id, "Non hai pozioni da usare")
   



def stats(bot, chat_id, user_id):

   sql = 'SELECT * FROM players WHERE user_id = %s'
    
   cursor.execute(sql, [user_id])
   myresult = cursor.fetchone()
   bot.sendMessage(chat_id, "\nusername: " + myresult[4] + "\npunti vita: " + str(myresult[5]) + "\npalle di neve: " + str(myresult[6]) + "\npozioni: " + str(myresult[7]))


      

def pg(bot, chat_id, user_id, avversario, username):

   pv = 'SELECT HP FROM players WHERE user_id = %s'
   cursor.execute(pv, [user_id])
   myresult = cursor.fetchone()
   HP = myresult[0]
   print("pg HP: ", HP)
   if HP < 1:
      bot.sendMessage(chat_id, "Non puoi lanciare palle da morto")
   else:
      ball = 'SELECT balls FROM players WHERE user_id = %s'
      cursor.execute(ball, [user_id])
      myresult = cursor.fetchone()
      balls = myresult[0]
      if balls < 1:
         bot.sendMessage(chat_id, "Non hai palle da tirare")
      else:
         print(avversario)
         tira(bot, chat_id, user_id, avversario)
         ricevi(bot, avversario, username)



      
def avs(bot, chat_id, user_id, avversario, username):

   avv = 'SELECT * FROM players WHERE username = %s'
   cursor.execute(avv, [avversario])
   myresult = cursor.fetchone()
    
   if myresult is not None:
      pv = 'SELECT HP FROM players WHERE username = %s'
      cursor.execute(pv, [avversario])
      myresult = cursor.fetchone()
      HP = myresult[0]
      print("HP avs1: ", HP)
      if HP < 1:
         bot.sendMessage(chat_id, "il tuo avversario è già morto")
      else:
         pg(bot, chat_id, user_id, avversario, username)
         
   else:
      bot.sendMessage(chat_id, "avversario non trovato")



def tira(bot, chat_id, user_id, avversario):

   ball = 'SELECT balls FROM players WHERE user_id = %s'
   cursor.execute(ball, [user_id])
   myresult = cursor.fetchone()
   balls = myresult[0]
   balls -= 1
   sql = 'UPDATE players SET balls = %s WHERE user_id = %s'
   cursor.execute(sql, [balls, user_id])
   db.commit()
   bot.sendMessage(chat_id, "Hai tirato una palla di neve a %s" % avversario)



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