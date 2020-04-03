

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


class Attack():
      
        

    def __init__(self,bot): 
        self.bot=bot
        self.pointAttack=0

    def send_keyboard(self,messageId,myId,gamer):
        size=len(gamer)
        kboard=[]
        i=2

        while(i<size):
            pprint(gamer[i].name)
            if gamer[i].id==myId:
                i=i+1
            if i==size:
                break
            elif i==(size-1) or (gamer[i+1].id==myId and (i+1)==(size-1) ):
                kboard.append([KeyboardButton(text=gamer[i].name)])
            elif gamer[i+1].id==myId and (i+1)<(size-1):
                kboard.append([KeyboardButton(text=gamer[i].name),KeyboardButton(text=gamer[i+2].name)])
                i=i+3
                continue
            else:
                kboard.append([KeyboardButton(text=gamer[i].name),KeyboardButton(text=gamer[i+1].name)])
            i=i+2
        kboard.append([KeyboardButton(text=costant.back)])

        #pprint(kboard)
        keyboard=ReplyKeyboardMarkup(keyboard=kboard,one_time_keyboard=True,selective=True
                        )
        self.bot.sendMessage(gamer[1],"Scegli chi vuoi attaccare!",reply_to_message_id=messageId ,reply_markup=keyboard)




    def prepareAttack(self,player,gamer):
        #index=self.getIndexFromId(gamer)
        #messageId=self.gamer[index].messageId
        messageId=player.messageId
        self.send_keyboard(messageId,player.id,gamer)



    def isTroll(self):
        k=random.uniform(0.0, 1.0)
        return k

    def attack(self,gamers,currentDefensor):

        if self.isTroll()>=float(0.8):
            indexAttackTroll=random.randint(1, 3)
            atk = open(costant.root_gif_path   +  costant.troll_att_path  +  str(indexAttackTroll)  +  costant.extension,"rb")
            self.bot.sendDocument(gamers[1], atk)   
            atk.close()
            self.pointAttack=costant.attackTroll[indexAttackTroll-1]
            #self.updatePoint(self.gamer[self.attackTurn],point)
            #self.newRound()
            return 1

        else:
            indexGifAttack=random.randint(1, 10)
            atk = open(costant.root_gif_path   +  costant.att_path  +  str(indexGifAttack)  +  costant.extension,"rb")
            self.bot.sendDocument(gamers[1], atk)   
            atk.close()
            self.pointAttack=indexGifAttack
            return 0


    def doubleAttack(self,gamers,currentDefensor):
        self.attack(gamers,currentDefensor)
        pointAtt=self.pointAttack
        self.attack(gamers,currentDefensor)
        pointAtt+=self.pointAttack
        self.pointAttack=pointAtt
        if self.pointAttack<0:
            return 1
        else:
            return 0



    def back(self,player,chat_id):
            keyboard=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=costant.kboardAttack),KeyboardButton(text=costant.kboardEvocation)],
                                                    [KeyboardButton(text=costant.kboardDefense),KeyboardButton(text=costant.kboardPrayer)],
                                                     [KeyboardButton(text='Punteggio: '+str(player.punteggio)),KeyboardButton(text=costant.kboardEffect)],
                                                     [KeyboardButton(text=costant.kboardEscape)]
                                                ],one_time_keyboard=True,selective=True
                        )
            self.bot.sendMessage(chat_id,"St apple fa solo danni",reply_to_message_id=player.messageId ,reply_markup=keyboard)





