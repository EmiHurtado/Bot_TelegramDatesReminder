# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 18:45:17 2021

@author: cafe_
"""

###############################################################################  #                            RUN MAIN                                         #  ###############################################################################    
# setup  
## pkg  
import telebot
import dateparser  
import pymongo 
import flask 
import datetime 
import threading
import os
#import logging   
#import config    

# Se agrega una nueva aplicación del lado del servidor con flask 
server = flask.Flask("botdatareminder")

# Se configura un webhook
@server.route('/Telegram API TOKEN', methods=['POST'])  
def getMessage():   
    bot.process_new_updates([telebot.types.Update.de_json(  flask.request.stream.read().decode("utf-8"))])   
    return "!", 200@server.route("/")  

def webhook():   
    bot.remove_webhook()   
    bot.set_webhook(url='Heroku App Web Address /'   +'Telegram API TOKEN')   
    return "!", 200


## bot  
# Se llama a la instacia de pyTelegramBotAPI e inserta el TOKEN de la API de Telegram 
# proporcionado por BotFather
bot = telebot.TeleBot("5047789487:AAFrTGoR4auz3rP1tLg34QSmW3_OUiQDGpk")  

# Se define un diccionario vacío que tiene la tarea de almacenar información temporal 
# del usuario (como la identificación del usuario)
dic_user = {}    

## setup db  
# Se concecta a la base de datos usando pymongo y la cadena de MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://emhurtadom:Batman1@telegramdatesreminderbo.wlafu.mongodb.net/TelegramDatesReminderBot?retryWrites=true&w=majority") 
db_name = "TelegramDatesReminderBot"  
collection_name = "users"  
db = client[db_name][collection_name] 

# logging  
"""logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)  
logger = logging.getLogger(__name__)   """     

# Se crea el comando que se ejecuta automáticamente cuando comienzas a chatear 
# con el Bot por primera vez
@bot.message_handler(commands=['start'])  
def _start(message):   
    msg = "Hello " + str(message.chat.username)+   ", I'm a date reminder. Tell me birthdays and events to remind you. To learn how to use me, use \n/help"   
    bot.send_message(message.chat.id, msg) 

# Se crea el comando para guardar eventos
@bot.message_handler(commands=['save'])  
def _save(message):   
    msg = "Set an event in the format 'month dd', for example: \n\   xmas day: Dec 25 \n\  I also understand: \n\  today, tomorrow, in 3 days, in 1 week, in 6 months, yesterday, 3 days ago ... so you can do: \n\   meeting: tomorrow"   
    message = bot.reply_to(message, msg)   
    bot.register_next_step_handler(message, save_event)

def save_event(message):   
    dic_user["id"] = str(message.chat.id)     
    ## get text   
    txt = message.text   
    name = txt.split(":")[0].strip()    
    date = txt.split(":")[1].strip()     
    ## check date   
    date = dateparser.parse(date).strftime('%b %d')     
    ## save   
    lst_users = db.distinct(key="id")   
    if dic_user["id"] not in lst_users:   
        db.insert_one({"id":dic_user["id"], "events":{name:date}})   
    else:   
        dic_events = db.find_one({"id":dic_user["id"]})["events"]   
        dic_events.update({name:date})   
        db.update_one({"id":dic_user["id"]}, {"$set":   {"events":dic_events}})    
    ## send done   
    msg = name + ": " + date + " saved."   
    bot.send_message(message.chat.id, msg)

@bot.message_handler(func=lambda m: True)  
def chat(message):   
    txt = message.text   
    if any(x in txt.lower() for x in ["thank","thx","cool"]):   
        msg = "anytime"   
    elif any(x in txt.lower() for x in ["hi","hello","yo","hey"]):   
        msg = "yo " + str(message.chat.username)
    else:   
        msg = "save a date with \n/save"   
    bot.send_message(message.chat.id, msg)
    
# Se crea un programador que verifique los eventos de hoy cada vez que se ejecute y envíe recordatorios de eventos.
def scheduler():   
    lst_users = db.distinct(key="id")   
    for user in lst_users:   
        dic_events = db.find_one({"id":user})["events"]   
        today = datetime.datetime.today().strftime('%b %d')   
        res = [k for k,v in dic_events.items() if v == today]   
        if len(res) > 0:   
            msg = "Today's events: "+", ".join(res)   
            bot.send_message(user, msg)

if __name__ == "__main__":  
    threading.Thread(target=scheduler).start()   
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    
bot.polling()
