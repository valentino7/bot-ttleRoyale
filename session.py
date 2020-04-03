

import time
import random
import os
from user import User 
import json
import threading
import functools                                                                
import costant
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent,InlineQueryResultCachedGif,InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,ReplyKeyboardRemove, KeyboardButton
from pprint import pprint
from threading import Timer
from threading import Thread
import time


def synchronized(wrapped):                                                      
    lock = threading.Lock()                                                     
    @functools.wraps(wrapped)                                                   
    def _wrap(*args, **kwargs):                                                 
        with lock:                                                              
            print ("Calling '%s' with Lock %s from thread %s [%s]"              
                   % (wrapped.__name__, id(lock),                               
                   threading.current_thread().name, time.time()))               
            result = wrapped(*args, **kwargs)                                   
            print ("Done '%s' with Lock %s from thread %s [%s]"                 
                   % (wrapped.__name__, id(lock),                               
                   threading.current_thread().name, time.time()))               
            return result                                                       
    return _wrap  

class Session:
    
    def __init__(self,bot,role): 
        self.bot=bot
        self.gamer=[[]]
        #self.messageId=[[]]
        self.role=role
        
    @synchronized
    def init(self,chat_id,msg):
        keyboard=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Start Game"),KeyboardButton(text="Regole")]
                                            ],one_time_keyboard=True
                    )
        self.bot.sendMessage(chat_id, "BOT-tle Royale",reply_to_message_id=False ,reply_markup=keyboard) 
        pprint("sono in init true")
        pprint(self.gamer)
        
      
    def removeGroupFromChatId(self,chat_id):
        i=self.getIndxOfGamerFromChat(chat_id)
        del self.gamer[i]
        #del self.messageId[i]
        self.checkLenGamer()
        
        
    def removeGamerFromChatIdAndUserIndex(self,index,chat_id):
        i=self.getIndxOfGamerFromChat(chat_id)
        self.gamer[i].pop(index)
        #self.messageId[i].pop(index-2)
        
    def removeGamerFromChatIdAndUser(self,msg,chat_id):
        i=self.getIndxOfGamerFromChat(chat_id)
        #self.messageId[i].pop(self.gamer[i].indexOf(msg['from']['first_name']))
        #self.gamer[i].remove(msg['from']['first_name'])
        self.removeUserInGamer(msg['from']['id'],i)

    """pressione del tasto start game"""
    def start(self,chat_id,msg):
        indexUserIsParticipant=self.getIndxOfGamerFromUserAndChatId( msg['from']['id'],chat_id)
        index=self.getIndxOfGamerFromChat(chat_id)
        
        if index==-1:
            for x in range(len(self.gamer)):
                    if not self.gamer[x]:
                        self.gamer[x].append(0)
                        self.gamer[x].append(chat_id)
                        self.gamer.append([])
                        #self.messageId.append([])
                        self.bot.sendMessage(chat_id, 'Scrivi /partecipa per far parte della sessione di gioco! Il primo giocatore che lo farà deciderà quando iniziare il gioco cliccando successivamente sul bottone Inizia.')
                        keyboard= InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Inizia",callback_data="Inizia")],
                        [InlineKeyboardButton(text="Chiudi gioco",callback_data="Chiudi")]
                                    ]   )
                        self.bot.sendMessage(chat_id,"Partecipa!",reply_to_message_id=msg['message_id'],reply_markup=keyboard)
            pprint("sono in start true")
            pprint(self.gamer)
        elif self.idChatIsInGamer(chat_id)==1 and self.gamer[index][0]==1 and indexUserIsParticipant==-1  :
            self.bot.sendMessage(chat_id, "Aspetta che gli altri giocatori terminino il gioco") 
            pprint("sono in start false")
            pprint(self.gamer)
        else:
            self.bot.sendMessage(chat_id, 'Scrivi /partecipa per far parte della sessione di gioco! Il primo giocatore che cliccherà il bottone deciderà quando iniziare il gioco cliccando successivamente sul bottone Inizia.')
            keyboard= InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Inizia",callback_data="Inizia")],
                        [InlineKeyboardButton(text="Chiudi gioco",callback_data="Chiudi")]
                                    ]   )
                
            self.bot.sendMessage(chat_id,"Partecipa!",reply_to_message_id=msg['message_id'],reply_markup=keyboard)
            pprint("sono nello stato in cui la chat_id del tizio è gia stata inserita")
            pprint(self.gamer)
        

    def getRole(self,chat_id,msg):
        self.bot.sendMessage(chat_id, self.role)
    

    
    def getGamerFromChatId(self,chat_id):
        for x in range(len(self.gamer)):
             if len(self.gamer[x])>1:
                if chat_id == self.gamer[x][1]:
                    return self.gamer[x]
        return -1
    
    def idChatIsInGamer(self,idChat):
        for x in range(len(self.gamer)):
            if len(self.gamer[x])>1:
                if idChat == self.gamer[x][1]:
                    return 1
        return -1
    
    def idUserIsInGamer(self,user):
        for x in range(len(self.gamer)):
            for y in range(2,len(self.gamer[x])):
                if user in self.gamer[x][y].id:                
                    return 1
        return -1
        
    def getIndxOfGamerFromUser(self,user):
        for x in range(len(self.gamer)):
            for y in range(2,len(self.gamer[x])):

                if user ==self.gamer[x][y].id:
                    return x
        return -1

    def getIndxOfGamerFromChat(self,chat_id):
        for x in range(len(self.gamer)):
            if len(self.gamer[x])>1:
                if self.gamer[x][1]== chat_id:
                    return x
        return -1


    def getIndxOfGamerFromUserAndChatId(self,user,chat_id):
        for x in range(len(self.gamer)):
            for y in range(2,len(self.gamer[x])):
                if user==self.gamer[x][y].id and chat_id == self.gamer[x][1]:
                    return x
        return -1

    @synchronized                                                               
    def addGamer(self,chat_id,msg):
         index=self.getIndxOfGamerFromChat(chat_id)
         indexUserInChatGamer= self.getIndxOfGamerFromUser(msg['from']['id'])
         indexUserIsParticipant=self.getIndxOfGamerFromUserAndChatId( msg['from']['id'],chat_id)

         if index!=-1:
            if indexUserIsParticipant!=-1:
                self.bot.sendMessage(chat_id, msg['from']['first_name']+" gia hai scelto di partecipare!") 

            elif self.idChatIsInGamer(chat_id)==1 and self.gamer[index][0]==1 and  indexUserIsParticipant==-1 :
                self.bot.sendMessage(chat_id, "Aspetta che gli altri giocatori terminino il gioco") 
                pprint("sono in addGamer false")
            
            elif self.idChatIsInGamer(chat_id)==1 and self.gamer[index][0]==0 and indexUserIsParticipant==-1 :
                user= User(msg['from']['id'],msg['from']['first_name'],chat_id,msg['message_id'])
                self.gamer[index].append(user)
                #self.messageId[index].append(msg["message_id"])
                pprint(self.gamer)
                pprint("sono in addGamer true")
                message_id=self.bot.sendMessage(chat_id, msg['from']['first_name']+" partecipa al gioco ! Il primo partecipante deve cliccare sul pulsante Inizia.")

         else:
                self.bot.sendMessage(chat_id,"Utilizza i bottoni per iniziare a giocare! Aprili con /bottle_royal") 

    """preparazione prima della partecipazione"""
    def prepare_addGamer(self,msg):
         chat_id= msg['chat']['id']
         index=self.getIndxOfGamerFromChat(chat_id)
         indexUserInChatGamer= self.getIndxOfGamerFromUser(msg['from']['id'])
         indexUserIsParticipant=self.getIndxOfGamerFromUserAndChatId( msg['from']['id'],chat_id)

         if index!=-1:
            if indexUserIsParticipant!=-1:
                self.bot.sendMessage(chat_id, msg['from']['first_name']+" gia hai scelto di partecipare!") 

            elif self.idChatIsInGamer(chat_id)==1 and self.gamer[index][0]==1 and  indexUserIsParticipant==-1 :
                self.bot.sendMessage(chat_id, "Aspetta che gli altri giocatori terminino il gioco") 
                pprint("sono in addGamer false")
            
            elif self.idChatIsInGamer(chat_id)==1 and self.gamer[index][0]==0 and indexUserIsParticipant==-1 :
                message_id=self.bot.sendMessage(chat_id, msg['from']['first_name']+" per partecipare devi inviare il seguente messaggio senza virgolette: </partecipa>")

         else:
                self.bot.sendMessage(chat_id,"Utilizza i bottoni per iniziare a giocare! Aprili con /bottle_royale") 
    
    
    
    def userIsGaming(self,user,chat_id):
        i=self.getIndxOfGamerFromUserAndChatId(user,chat_id)
        if i!=-1 and  self.gamer[i][0]==1:
            return 1
        return -1
    
    """inizia"""
    def game(self,msg,chat_id):
        """devo scorrere gamer per trovare quelo che voglio"""
        indexChat=self.getIndxOfGamerFromChat(chat_id)

        indexUserIsParticipant=self.getIndxOfGamerFromUserAndChatId( msg['from']['id'],chat_id)
        pprint("sono nel game " + str(self.gamer)+ "index: "+str(indexUserIsParticipant))
        
        
        if indexUserIsParticipant != -1 and msg['from']['id']==self.gamer[indexUserIsParticipant][2].id and len(self.gamer[indexUserIsParticipant])>3 and  self.gamer[indexUserIsParticipant][0]==0:
            pprint(self.gamer)
            self.gamer[indexUserIsParticipant][0]=1
            self.bot.sendMessage(chat_id,'Inizio gioco!')
            return 1
            
        elif indexChat == -1  :
            self.bot.sendMessage(chat_id,"Utilizza i bottoni per iniziare a giocare! Aprili con /bottle_royal") 
        elif indexUserIsParticipant==-1 and self.gamer[indexChat][0]==1 :
            self.bot.sendMessage(chat_id, 'Aspetta che la partita termini')
        elif self.gamer[indexChat][0]==0 and  indexUserIsParticipant==-1 : 
            self.bot.sendMessage(chat_id, 'Scrivi /partecipa se vuoi partecipare al gioco!')
        elif msg['from']['id'] != self.gamer[indexUserIsParticipant][2].id :
            self.bot.sendMessage(chat_id,msg['from']['first_name'] + " non sei il primo giocatore che si e registrato nella partecipazione. Solo il primo giocatore puo decidere quando iniziare")
        elif len(self.gamer[indexUserIsParticipant])<4:
            self.bot.sendMessage(chat_id, 'Dovete essere almeno 2 partecipanti')
        return -1

    def checkLenGamer(self):
        if len(self.gamer)==0:
            self.gamer.append([])
            #self.messageId.append([])

    def getIndexFromId(self,id,index):
        for i in range(2, len(self.gamer[index]) ):
            if self.gamer[index][i].id==id:
                return i
        return -1

    def removeUserInGamer(self,id,index):
        for i in range(2,len(self.gamer[index])):
            if self.gamer[index][i].id==id:
                self.gamer[index].pop(i)
                return 1
        pprint("ERRORE, UTENTE NON TROVATO NELLA CLOSE")
        return -1

    @synchronized                                                               
    def close(self,chat_id,msg):
        """scorri e cancella, controlla se : la lista ha 1 solo elemento e quindi cancella tutto,contolla se il primo valore è """
        
        close=""
        index=self.getIndxOfGamerFromUserAndChatId( msg['from']['id'],chat_id)

        pprint(self.gamer)
        #pprint(self.messageId)
        if index!=-1 :

            self.removeUserInGamer(msg['from']['id'],index)
            pprint("operazione remove su gamer"+str(self.gamer))
            
                
            self.bot.sendMessage(chat_id, msg['from']['first_name'] + ' sei uscito')
            pprint("sono in init true")
            pprint(self.gamer)
            close="una chiusura"
            if len(self.gamer[index])<4:
                self.bot.sendMessage(chat_id,' Siete meno di due partecipanti il gioco si chiuderà')
                self.bot.sendMessage(chat_id, 'Deleting keyboard', reply_markup=ReplyKeyboardRemove())
                del self.gamer[index]
                #del self.messageId[index]
                self.checkLenGamer()
                pprint("meno di 2 partecipanti"+ str(self.gamer))
                close="due chiusure"

        elif index==-1 :
            self.bot.sendMessage(chat_id, msg['from']['first_name'] + ' come fai ad uscire se non entri?')
        return close







        
    
    def checkCommandsInline(self,query_data,msg):
        
        if query_data=='Chiudi' and self.userIsGaming(msg['message']['from']['id'],msg['message']['chat']['id'])==-1:
            self.close(msg['message']['chat']['id'],msg)

    
    def checkCommandsBase(self,chat_id,msg):
            
        if msg['text']== 'Start Game' :
            self.start(chat_id,msg)


        if msg['text']== '/partecipa' or msg['text']== '/partecipa@BottleRoyale_bot':
            """self.prepare_addGamer(msg)"""
            self.addGamer(chat_id,msg)

        if msg['text']== 'Regole' :
            self.getRole(chat_id,msg)

        if msg['text'].lower()== '/bottle_royale' or msg['text'].lower()== '/bottle_royale@bottleroyale_bot':
            self.init(chat_id,msg)
            
   
        
            


      
            