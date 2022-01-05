# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 12:57:39 2021

@author: cafe_
"""

import os

ENV = "DEV"
#ENV = "PROD"



## keys
if ENV == "DEV":
	telegram_key = "5047789487:AAFrTGoR4auz3rP1tLg34QSmW3_OUiQDGpk"
	mongodb_key = "mongodb+srv://emhurtadom:Batman1@telegramdatesreminderbo.wlafu.mongodb.net/TelegramDatesReminderBot?retryWrites=true&w=majority"

elif ENV == "PROD":
	import ast
	telegram_key = ast.literal_eval(os.environ["telegram_key"])
	mongodb_key = ast.literal_eval(os.environ["mongodb_key"])



## server
host = "0.0.0.0"
port = int(os.environ.get("PORT", 5000))
webhook = 'https://botdatareminder.herokuapp.com/'


## fs
#root = os.path.dirname(os.path.dirname(__file__)) + "/"
