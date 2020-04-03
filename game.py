import telepot
import time
import random
import os
import requests
import io
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


class Game:
    def __init__(self,bot,gamer): 
        self.bot=bot
        self.gamer=gamer

        
        #TODO scrivere le regole
        #TODO aggiungere ad update,la list di turner deve essere aggiornata ogni votla che un giocatore viene eliminato e
            #  bisogna controllare se è 0

        #TODO rendere idempotente l'attacco
        #TODO scrivere cosa succede se esce evocazione e preghiera
        self.attackTurn=2
        self.listTurner=[]
        self.fillListTurner()
        self.currentTurn='Attack'
        self.effectUsed=0
        self.effectOn=0
        self.currentEffect=0
        self.defenseWin=0
        self.currentIndexGifAttack=0
        self.currentDefensor=0
      

    def getIndexFromId(self,id):
        for i in range(2, len(self.gamer) ):
            if self.gamer[i].id==id:
                return i
        return -1


    def update(self,msg):
        i=self.gamer.getIndexFromId(msg['from']['id'])
        self.gamer.pop(i)
        if self.attackTurn==i:
            self.addTurn()
        
        
    def chatIdIsInGame(self,chat_id):
        if self.gamer[1]==chat_id:
            return 1
        return 0
            
    
    def addTurn(self):
        self.attackTurn+=1
        if self.attackTurn > len(self.gamer)-1:
            self.attackTurn=2


    def fillListTurner(self):
        if len(self.gamer)==0:
            pprint("ERRORE,LISTA VUOTA DI GAMER QUANDO RIEMPIO LA LISTA DI TURNI")
        else:
            for i in range(2,len(self.gamer)):
                self.listTurner.append(i)

    def checkRefillListTurner(self):
        if len(self.listTurner)==0:
            self.fillListTurner()

    def setRandomAttackTurn(self):
        #la random mi restituisce l elemento random nella lista di turni che salva le posizioni del vettore dei giocatori
        # ad esempio restituisce la posizione dell utente 2 nel vettore di gamer
        self.checkRefillListTurner()
        self.attackTurn=random.choice(self.listTurner)
        pprint("lista di turni"+str(self.listTurner))
        self.listTurner.remove(self.attackTurn)


   
    def start(self):
        self.setRandomAttackTurn()
        for x in range(len(self.gamer)-2):
            keyboard=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=costant.kboardAttack),KeyboardButton(text=costant.kboardEvocation)],
                                                     [KeyboardButton(text=costant.kboardDefense),KeyboardButton(text=costant.kboardPrayer)],
                                                     [KeyboardButton(text='Punteggio: '+str(self.gamer[x+2].punteggio)),KeyboardButton(text=costant.kboardEffect)],
                                                     [KeyboardButton(text=costant.kboardEscape)]
                                                ],one_time_keyboard=True,selective=True
                        )
            self.bot.sendMessage(self.gamer[1],self.gamer[x+2].name+" è entrato nel gioco",reply_to_message_id=self.gamer[x+2].messageId ,reply_markup=keyboard)
        
        self.currentTurn='Attack'
        self.bot.sendMessage(self.gamer[1],self.gamer[self.attackTurn].name+" deve attaccare/evocare! ⚔️⚔️") 



    def newRound(self):
        self.setRandomAttackTurn()
        time.sleep(5)

        for x in range(len(self.gamer)-2):
            keyboard=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=costant.kboardAttack),KeyboardButton(text=costant.kboardEvocation)],
                                                     [KeyboardButton(text=costant.kboardDefense),KeyboardButton(text=costant.kboardPrayer)],
                                                     [KeyboardButton(text='Punteggio: '+str(self.gamer[x+2].punteggio)),KeyboardButton(text=costant.kboardEffect)],
                                                     [KeyboardButton(text=costant.kboardEscape)]
                                                ],one_time_keyboard=True,selective=True
                        )
            self.bot.sendMessage(self.gamer[1],self.gamer[x+2].name+" ha "+ str(self.gamer[x+2].punteggio) + " punti.",reply_to_message_id=self.gamer[x+2].messageId ,reply_markup=keyboard)
        
        self.currentTurn='Attack'
        self.bot.sendMessage(self.gamer[1],self.gamer[self.attackTurn].name+" deve attaccare/evocare! ") 



    
    def getPlayer(self,idGamer):
         index=self.getIndexFromId(idGamer)
         return self.gamer[index]


    def trollEffect(self,idGamer):
        index=self.getIndexFromId(idGamer)
        for i in range(len(self.gamer[index].trollEv)):
            if self.gamer[index].trollEv[i]>0:
                if costant.evocationTroll[i]=='perditurno':
                    self.gamer[index].trollEv[i]-=1
                    return 1
                else :
                    if costant.evocationTroll[i]=='sceglichifarperdereturno' :
                        self.gamer[index].trollEv[i]-=1
                        return 0




    def setTrollEvocation(self,effect,idGamer):
        index=self.getIndexFromId(idGamer)
        self.gamer[index].trollEv[effect]+=1
        if self.defenseWin==1:
            self.currentDefensor=0
            self.defenseWin=0

    def setEvocation(self,effect,idGamer):
        index=self.getIndexFromId(idGamer)
        self.gamer[index].effectEv[effect]+=1
        if self.defenseWin==1:
            self.currentDefensor=0
            self.defenseWin=0


    
    def rightTurnEvocation(self,gamer):
        if self.rightTurnAttack(gamer)==1 and self.effectOn==0:
            self.effectOn=1
            return 1
        if self.currentDefensor.id== gamer and self.currentTurn=='Defense' and self.defenseWin==1 and self.effectOn==0:
            self.effectOn=1
            return 1
        
        return -1


    def rightTurnEffect(self,gamer):
        if self.rightTurnAttack(gamer)==1 or self.rightTurnDefense(gamer)==1:
            return 1
        return -1


        
    def rightTurnAttack(self,gamer):
        if self.gamer[self.attackTurn].id== gamer and self.currentTurn=='Attack' :
            return 1
        return -1



   

    def updatePoint(self,gamer,point):
        self.getPlayer(gamer)
        gamer.punteggio+=point


    def back(self,player,index):
            keyboard=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=costant.kboardAttack),KeyboardButton(text=costant.kboardEvocation)],
                                                    [KeyboardButton(text=costant.kboardDefense),KeyboardButton(text=costant.kboardPrayer)],
                                                    [KeyboardButton(text='Punteggio: '+str(player.punteggio)),KeyboardButton(text=costant.kboardEffect)],
                                                    [KeyboardButton(text=costant.kboardEscape)]
                                                ],one_time_keyboard=True,selective=True
                        )
            self.bot.sendMessage(self.gamer[1],"L'effetto è stato utilizzato:"+ costant.kboardEffect[index] +"puoi attaccare!",reply_to_message_id=player.messageId ,reply_markup=keyboard)

    def useEffect(self,index):
        #attacco 2x
        if index==0:
            self.currentEffect=1
        #attacco due volte
        elif index==4:
            self.currentEffect=2
        elif index==1:
            #def 2x
            self.currentEffect=3
        elif index==3:
            #non ti attaccano
            self.currentEffect=4



    def useAttEffect(self,msg,idGamer):
        pprint("use effect")
        self.effectUsed=1
        index=costant.keyboardEvocation.index(msg)
        indexUser= self.getIndexFromId(idGamer)
        self.gamer[indexUser].effectEv[index]-=1
        pprint("use effect"+ str( self.gamer[index].effectEv))
        self.useEffect(index)
        self.back(self.gamer[indexUser],index)




    def showEffects(self,gamer):
        index=self.getIndexFromId(gamer)
        effects=[]
        for i in range(len(self.gamer[index].effectEv)):
            if self.gamer[index].effectEv[i]>0:
                    effects.append(costant.keyboardEvocation[i])
                
        
        
        if len(effects)==0:
            return -1
        else:
            key=[]
            i=0
            while (i<len(effects)):
                if len(effects)==1:
                    key.append([KeyboardButton(text=effects[i])])
                else:
                    key.append([KeyboardButton(text=effects[i]),KeyboardButton(text=effects[i+1])])
                i+=2
            keyboard=ReplyKeyboardMarkup(keyboard=key,one_time_keyboard=True,selective=True)
            self.bot.sendMessage(self.gamer[1],self.gamer[index].name+" scegli cosa evocare!",reply_to_message_id=self.gamer[index].messageId ,reply_markup=keyboard)
        
            self.currentTurn='Attack'
            self.bot.sendMessage(self.gamer[1],self.gamer[self.attackTurn].name+" deve attaccare/evocare! ") 
            return 1





    #controlla se l'avversario scelto dall'attaccante è valido e se l'attaccante aveva il permesso di sferrare l'attacco
    def checkResultTargetAttack(self,id,name):
        pprint("sono in attack 2")
        pprint(self.attackTurn)
        if id==self.gamer[self.attackTurn].id and self.currentTurn=='Attack':
            pprint("sono in attack 3")

            for i in range(2,len(self.gamer)):
                if name==self.gamer[i].name:
                    self.currentDefensor=self.gamer[i]
                    return 1
        else:
            return -1
        


    def computePoint(self,defensePoint):
        pprint("defense: "+str(defensePoint))
        pprint("attack: "+str(self.currentIndexGifAttack))
        total_point=0

        total_point=self.currentIndexGifAttack-defensePoint
        #se il numero è positivo significa che ha vinto l'attacco e quindi tolgo i punti alla difesa, se è negativo il contrario
        if total_point>0:
            #vince attacco
            total_point-=2*total_point
            self.updatePoint(self.currentDefensor,total_point)
            self.bot.sendMessage(self.gamer[1],"VINCEEE....................L'ATTACCOOOOO! 🎊🎉🎊🎉🎊🎉 ") 
            self.newRound()
            self.currentDefensor=0

        elif total_point==0:
            self.bot.sendMessage(self.gamer[1],"Signori e signori ...vinceeeeeee....PAREGGIO") 
            self.newRound()
            self.currentDefensor=0

        else:
            #vince difesa
            self.updatePoint(self.gamer[self.attackTurn],total_point)
            self.bot.sendMessage(self.gamer[1],"VINCEEEE...................LA DIFESAAAAAA! 🎊🎉🎊🎉🎊🎉") 
            self.bot.sendMessage(self.gamer[1],"PUOI LANCIARE UN'EVOCAZIONE! 🎊🎉🎊🎉🎊🎉") 
            self.defenseWin=1

    def rightTurnDefense(self,gamer):
        if self.currentDefensor.id== gamer and self.currentTurn=='Defense' :
            return 1
        return -1


    def prayer(self):
        self.bot.sendSticker(self.gamer[1],sticker=costant.oak)
