#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Dependencias
import telebot
import requests
import random
import json
import urllib
from telebot import util
from telebot import types
from bs4 import BeautifulSoup
from bs4 import *


TOKEN = 'Aqui metes el token'
bot = telebot.TeleBot(TOKEN)

#Lee todos los mensajes del chat cuando se envian
def lector_mensajes(chatall):
    for message in chatall:
        #Mensaje de bienvenida a los usuarios que entran al grupo
        if message.content_type == "new_chat_members":
            bot.send_message(message.chat.id,"Bienvenido " + str(message.new_chat_member.username) + " a " + str(message.chat.title))
        elif message.text == '!petada':
            bot.send_voice(message.chat.id, open('./audio/petada.ogg', 'rb'))
        elif message.text != None:
            if "tacens" in message.text:
                bot.send_video(message.chat.id,open('./image/giphy.gif.mp4', 'rb'))

#Comando de chiste
@bot.message_handler(commands=['chiste'])
def chiste(msg):
    url_chistes = "http://www.chistescortos.eu/random"
    r_chistes = requests.get(url_chistes)
    html_content_chistes = r_chistes.text
    soup_chistes = BeautifulSoup(html_content_chistes, "html.parser")
    txt_chiste = soup_chistes.find("a", { "class" : "oldlink" })
    bot.send_message(msg.chat.id, txt_chiste.getText())

#Banear a alguien
@bot.message_handler(commands=['permaban'])
def permaban(msg):
    #Si el mensaje es una respuesta
    if msg.reply_to_message != None:
        #Si el chat id es un grupo
        if msg.chat.id < 0:
            admins = bot.get_chat_administrators(msg.chat.id)
            if admins:
                #Pilla todos los id de los admins
                admins_ids = [x.user.id for x in admins]
                #Si el id del mensaje del user esta en los id de admins
                if msg.from_user.id in admins_ids:
                    reply_user_id = msg.reply_to_message.from_user.id
                    print(reply_user_id)
                    bot.send_message(msg.chat.id, "El usuario " + msg.reply_to_message.from_user.first_name + " se va a comer una polla del tamaño de una farola")
                    bot.kick_chat_member(msg.chat.id, reply_user_id)
                else:
                    bot.send_message(msg.chat.id, "No eres Admin para echar a alguien parguela xddd")

    else:
        bot.send_message(msg.chat.id, "Aprende a usar el comando cacho palomo")
    
#Historias aleatorias (faltan por poner unas cuantas chulas)
@bot.message_handler(commands=['historia'])
def resp_pole(msg):
    user = msg.from_user.username
    rnd1 = random.choice(["empezo a escribir un libro sobre zoofilia", "se aficiono al parchis online", "estaba tranquilamente en la jurisdiccion del surtidor"])
    rnd2 = random.choice(["cuando vio a willyrex", "cuando encontro su dignidad", "mientras salvaba el mundo de Salvador Raya"])
    rnd3 = random.choice(["y vio la oportunidad de tirarle la caña", "y fue secuestrado por Nestor para su club de virgenes", "y se fue a tomar por culo"])
    bot.reply_to(msg, user + " " + rnd1 + ", " + rnd2 + ", " + rnd3)

#Historias sexosintabues
@bot.message_handler(commands=['tabuestexto'])
def tabuestexto(msg):
    url1 = "http://www.sexosintabues.com/ForoSexoErotico-ver-tema-"
    url2 = str(random.randint(11000,18000))
    url3 = "-start-0.html"
    urlFIN = url1 + url2 + url3
    r = requests.get(urlFIN)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")
    td = soup.find("td", { "class" : "lefttoprightbottom" }, { "headers" : "col_1" })
    if td == None:
        print("Reload del sexosintabues")
        tabuestexto(msg)
    else:
        bot.send_message(msg.chat.id, td.getText())

#Precio bitcoin
@bot.message_handler(commands=['bitprice'])
def bitprice(msg):
    with urllib.request.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json") as urlbit:
        databit = json.loads(urlbit.read().decode())
        btc_EUR= str(databit['bpi']['EUR']['rate'])
    bot.send_message(msg.chat.id,"💸 1BTC = " + btc_EUR + '€ 💸' + '\n 😿 Una 480 minando, un gatito muerto por tu culpa 😿')

#Tacens
@bot.message_handler(commands=['tacens'])
def tacens(msg):
    bot.send_message(msg.chat.id,"Fuentes de alimentación Anima\n🍃 Ultrasilenciosas\n⚡️ Potentes\n⚫️ Eficientes https://t.co/K75b8wsZOb https://twitter.com/Tacens_/status/941289863164416000")

#Creditos
@bot.message_handler(commands=['creditos'])
def creditos(msg):
    bot.send_message(msg.chat.id,"Creditos JuanmaHL 2024")


#Actualizar listado de mensajes
bot.set_update_listener(lector_mensajes)
bot.polling(none_stop=True)


