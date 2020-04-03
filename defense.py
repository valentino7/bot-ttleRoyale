

import telepot
import time
import random
import os
import requests
import json
import redis
import game
import threading
import functools                                                                
import costant
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent,InlineQueryResultCachedGif,InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from pprint import pprint
from threading import Timer
from threading import Thread
import time 


class Defense():
      
        

    def __init__(self,bot): 
        self.bot=bot



    def isTroll(self):
        k=random.uniform(0.0, 1.0)
        return k

    def defense(self,chat_id):
        defensePoint=0
        if self.isTroll()>=float(0.8):
            indexGifDefense=random.randint(1, 3)
            defensePoint=costant.defenseTroll[indexGifDefense-1]
            defe = open(costant.root_gif_path   +  costant.troll_def_path  +  str(indexGifDefense)  +  costant.extension,"rb")
            self.bot.sendDocument(chat_id, defe)   
            defe.close()

        else:
            indexGifDefense=random.randint(1, 10)
            defensePoint=indexGifDefense
            defe = open(costant.root_gif_path   +  costant.def_path  +  str(indexGifDefense)  +  costant.extension,"rb")
            self.bot.sendDocument(chat_id, defe)   
            defe.close()
        pprint(defensePoint)
        return defensePoint        