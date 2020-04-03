

import telepot
import time
import random
import os
import requests
import json
import redis
import threading
import functools                                                                
import costant
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent,InlineQueryResultCachedGif,InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from pprint import pprint
from threading import Timer
from threading import Thread
import time 


class User:
    def __init__(self,id,name,username,messageId):
        self.id=id 
        self.name=name
        self.messageId=messageId
        self.punteggio=50
        self.effectEv=[]
        self.trollEv=[]
        for i in range(0, 2 ):
            self.trollEv.append(0)
        for i in range(0, 5 ):
            self.effectEv.append(0)