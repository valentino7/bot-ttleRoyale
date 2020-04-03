

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


class Evocation():
      
        

    def __init__(self,bot): 
        self.bot=bot
        self.gifTroll=0
        self.gifEv=0


    def isTroll(self):
        k=random.uniform(0.0, 1.0)
        return k

    def evocation(self,chat_id):
        indexGifEv=''
        if self.isTroll()>=float(0.8):
            indexGifEv=random.randint(1, 2)
            self.gifTroll=indexGifEv
            effectEvocation=costant.evocationTroll[indexGifEv-1]
            ev = open(costant.root_gif_path   +  costant.troll_ev_path  +  effectEvocation  +  costant.extension,"rb")
            self.bot.sendDocument(chat_id, ev)   
            ev.close()
            return 0
        else:
            indexGifEv=random.randint(1, 5)
            self.gifEv= indexGifEv
            ev = open(costant.root_gif_path   +  costant.ev_path  +  costant.evocation[indexGifEv-1]  +  costant.extension,"rb")
            self.bot.sendDocument(chat_id, ev)   
            ev.close()
            return 1
