
import telepot
import time
from textblob import TextBlob
import random
import os
import requests
import PIL.Image
import json
import io


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import redis
import controllerGame
import session
import costant
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent,InlineQueryResultCachedGif,InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from pprint import pprint


class BotRoyale:
    
    def __init__(self, bot): 
        self.bot = bot 
        self.c=controllerGame.ControllerGame(self.bot)
        self.session = session.Session(self.bot,costant.role) 
    
    """metodo che riceve i messaggi dalla chat"""
    def chat(self,msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        pprint(msg)


        if msg['text']== '/info' or msg['text']== '/info@BottleRoyale_bot':
            self.bot.sendMessage(chat_id, costant.commands)
        
        """controllo i comandi base per la sessione d ingresso al gioco: partecipa, chiudi,inizia"""
        self.session.checkCommandsBase(chat_id,msg)
        """controllo i comandi base per il gioco vero e proprio"""
        self.c.checkCommandsGame(self.session,chat_id,msg)
      

    
    def send_mex(self,type_m,id_m,title_m,text_m,query_id):
        if type_m == 'gif':
            articles = [InlineQueryResultCachedGif(
                    id=id_m,
                    title=title_m,
                    gif_file_id=text_m
                    )
            ]
        elif type_m == 'text':
            articles = [InlineQueryResultArticle(
                            id=id_m,
                            title=title_m,
                            input_message_content=InputTextMessageContent(
                                message_text=text_m
                            )
                    )]
        self.bot.answerInlineQuery(query_id, articles)

    def on_inline_query(self,msg):
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print ('Inline Query:', query_id, from_id, query_string)

        
    def on_chosen_inline_result(self,msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print ('Chosen Inline Result:', result_id, from_id, query_string)
    
    
    def on_callback_query(self,msg):
        query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
        pprint("STAMPO IL MEX In ARRIVO")
        pprint(msg)
       
    
        self.session.checkCommandsInline(query_data,msg)
        if query_data=='Inizia':
            if self.session.game(msg,msg['message']['chat']['id'])==1:
                pprint("sono nell'inline e questa è la lista di gamer="+ str(self.session.getGamerFromChatId(msg['message']['chat']['id'])))

                listGamer = self.session.getGamerFromChatId(msg['message']['chat']['id'])
                if self.c.getGame(msg['message']['chat']['id'])==-1:
                    self.c.startGame(listGamer )

            
            
       

                    
"""class Connect:
    def connect_redis(self):

        return redis.from_url(os.environ.get("REDIS_URL"))"""

   

def main():

    """conn= Connect()
    r=conn.connect_redis()
    
    r.delete("msg:hello")
    r.set("msg:hello", "Hello Redis!!!")

    # step 5: Retrieve the hello message from Redis
    msg = r.get("msg:hello")
    print("ciao")
    print(msg)  
    print("ciao") """

    botRoyale=BotRoyale(telepot.Bot(costant.TOKEN))


    MessageLoop(botRoyale.bot, {'chat':botRoyale.chat,'inline_query': botRoyale.on_inline_query,
                    'chosen_inline_result': botRoyale.on_chosen_inline_result,'callback_query': botRoyale.on_callback_query}).run_as_thread()
  
    print('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)



if __name__ == '__main__':
    main()



