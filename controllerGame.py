import telepot
import time
import random
import os
import requests
import json
import redis
import threading
import game
import attack    
import evocation 
import defense                                                       
import costant
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent,InlineQueryResultCachedGif,InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from pprint import pprint
from threading import Timer
from threading import Thread
import time 


class ControllerGame: 

    def __init__(self,bot): 
        self.bot=bot
        self.game=[]
        self.atk= attack.Attack(bot)

        
    def startGame(self,gamer):
        pprint(gamer)
        currentGame=game.Game(self.bot,gamer)
        self.game.append(currentGame)
        currentGame.start()
        
    def getGame(self,chat_id):                            
        for i in range(len(self.game)):
            if self.game[i].chatIdIsInGame(chat_id)==1:
                return self.game[i]
            
        return -1
    
    def checkMsgEffectAtt(self,msg):
        if msg in costant.keyboardEvocation:
            return 1
        return -1

    def checkCommandsGame(self,session,chat_id,msg):
        if session.userIsGaming(msg['from']['id'],chat_id)==1:
            
            game=self.getGame(chat_id)

            #controllo se il tizio che ha lanciato l'attacco è il corrente attaccante,controllo se il suo avversario corrisponde
            pprint(game)

            #controllo se ha un evocazione troll
            if game.rightTurnAttack(msg['from']['id'])==1 and game.trollEffect(msg['from']['id'])==1:
                self.bot.sendMessage(msg["chat"]["id"],game.gamer[game.attackTurn].name+" perdi turno ! ") 
                game.newRound()
                game.currentDefensor=0

            #ATTACCO- al termine imposto il turno DEFENSE e l'id del currentDefensor

            elif game.checkResultTargetAttack( msg['from']['id'],msg['text'])==1  :
                
                pprint("SONO IN ATTACK")
                #game.attack(msg['from']['id'])
                att=0
                #doppio turno
                if game.currentEffect==2:
                    att=self.atk.doubleAttack(game.gamer,game.currentDefensor.name)
                    game.currentEffect=0
                else:
                    att=self.atk.attack(game.gamer,game.currentDefensor.name)
                #è troll
                if att==1:
                    self.bot.sendMessage(game.gamer[1],"Il troll non perdona , hai perso! 🤡🤡 ") 
                    player=game.getPlayer(msg['from']['id'])
                    game.updatePoint(player,self.atk.pointAttack)
                    game.newRound()
                else:
                    self.bot.sendMessage(game.gamer[1],game.currentDefensor.name +" devi difenderti! 🛡🛡") 
                    game.currentIndexGifAttack=self.atk.pointAttack
                    game.currentTurn='Defense'
                game.effectUsed=0

          
            elif  msg['text']== costant.kboardAttack or  msg['text'] in costant.evocation :
                if game.rightTurnAttack(msg['from']['id'])==1:
                    #game.prepareAttack(msg['from']['id'])

                    #devo passare il player e il bot
                    player=game.getPlayer(msg['from']['id'])
                    self.atk.prepareAttack(player,game.gamer)
                else:
                    self.bot.sendSticker(msg["chat"]["id"],sticker=costant.oak)


            #DIFESA-alla fine della difesa imposto il turno ATTACK e setto l'id del prossimo gamer 
            elif msg['text']== costant.kboardDefense :
                if game.rightTurnDefense(msg['from']['id'])==1:
                    dfs=defense.Defense(self.bot)
                    defensePoint=dfs.defense(msg["chat"]["id"])
                    #attacco 2x
                    if game.currentEffect==1:
                        game.currentIndexGifAttack=game.currentIndexGifAttack*2
                        game.currentEffect=0
                    if game.currentEffect==3:
                        defensePoint*=2
                        self.bot.sendMessage(msg["chat"]["id"],game.gamer[game.attackTurn].name+" difesa per 2 ! ") 
                        game.currentEffect=0
                    if game.currentEffect==4:
                        self.bot.sendMessage(msg["chat"]["id"],game.gamer[game.attackTurn].name+" sei il RE, non puoi essere attaccato ! ") 
                        game.newRound()
                        game.currentEffect=0
                        game.currentDefensor=0
                    else:
                        game.computePoint(defensePoint) 
                   

            #PREGHIERA
            elif msg['text']== costant.kboardPrayer:
                game.prayer()


            #EVOCAZIONE
            elif msg['text']==costant.kboardEvocation :
                if game.rightTurnEvocation(msg['from']['id'])==1:
                    evc=evocation.Evocation(self.bot)
                    effect=evc.evocation(msg["chat"]["id"])
                    if effect==1:
                        game.setEvocation(evc.gifEv,msg["chat"]["id"])
                        evc.gifEv=0
                    else:
                        game.setTrollEvocation(evc.gifTroll,msg["chat"]["id"])
                        evc.gifTroll=0
                    game.effectOn=0
                    game.newRound()
                else:
                    self.bot.sendSticker(msg["chat"]["id"],sticker=costant.oak)
           

            #USA EFFETTO
            elif msg['text']==costant.kboardEffect :
                if game.rightTurnAttack(msg['from']['id'])==1:
                    pprint("sto inright turno attack")
                    evc=game.showEffects(msg["chat"]["id"])
                    if evc==-1:
                        self.bot.sendSticker(msg["chat"]["id"],sticker=costant.oak)

                else:
                    self.bot.sendSticker(msg["chat"]["id"],sticker=costant.oak)

            #EFFETTO SCELTO
            elif game.rightTurnAttack(msg['from']['id'])==1 and game.effectUsed==0:
                if self.checkMsgEffectAtt(msg['text'])==1:
                    pprint("sono in effetto scelto")
                    game.useAttEffect(msg['text'],msg['from']['id'])
                        #decrementare indice effetti
                        #impotare game.effectUsed a 1 a inizio effetto
                        #rimostro la tastiera per attaccare inviando il messaggio
                    #impostare game.effectUsed a 0 quando finisce l'attacco
                    #implemento l'effetto nell'attack
                    #impostare current effect a 0 quando finisce l'attacco
            



            #INDIETRO
            if msg['text']==costant.back:
                if msg['from']['id'] != game.gamer[game.attackTurn].id:
                    self.atk.back(game.gamer[game.attackTurn],msg["chat"]["id"])
                else:
                    self.bot.sendSticker(msg["chat"]["id"],sticker=costant.oak)
                    self.bot.sendMessage(msg["chat"]["id"],game.gamer[game.attackTurn].name+" attendi che termini la fase di attacco ! ") 





            if msg['text'].lower()== costant.kboardEscape:
                """1 se ho eliminato solo 1 utente, -1 se il gioco viene chiuso"""
                string=session.close(chat_id,msg)
                pprint(string)
                if string=="una chiusura":
                    game.update(msg)
                    session.removeGamerFromChatIdAndUser(msg,chat_id)

                elif string=="due chiusure":
                    self.game.remove(game)
                    session.removeGroupFromChatId(chat_id)
                
                
          
