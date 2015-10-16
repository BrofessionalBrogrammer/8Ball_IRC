#!/usr/bin/python3
# Magic 8 Ball IRC bot
# Created by Lance Brignoni on 8.9.15
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import socket
import random
server = "CHANGETHIS"
channel = "CHANGETHIS"
botnick = "ball-bot"
password = "PASSHERE"
#list of responses
responses = ["Not so sure", "42", "Most likely", "Who's asking?", "Chances are high", "Absolutely not", "Outlook is good", 
"I see good things happening", "Never", "Stop asking", "If lain wills it", "Yes but you must worship me", "No, sorry", "Yes!", "If you try hard", "Sorry, no",
"I see it happening in your lifetime", "Yes but be careful", "No, don't count on it", "It's a possibility", "No chance", "I'd imagine so",
"Negative", "Could be", "Unclear, ask again", "Yes", "No", "Possible, but not probable", "Eat 2 fortune cookies then ask again"]
#all bytes must be converted to UTF-8
#pings
def ping():
    ircsock.send(bytes("PONG :Pong\n", "UTF-8"))
#join channel
def joinchan(chan):
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))

#The two first lines are used to connect to the server through port 6667 which is the most used irc-port. 
#The third line sends the username, realname etc. 
#The fourth line assigns a nick to the bot and the fifth line identifies the user
#The last line then joins the configured channel. 
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :connected\n", "UTF-8"))
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8"))
ircsock.send(bytes("NICKSERV :IDENTIFY %s\r\n" % password, "UTF-8"))
joinchan(channel)
#constantly checks for new messages
while 1:
    def answer_query():
        return(random.choice(responses))
    msg = answer_query()
    def sendmsg(chan , msg):
        ircsock.send(bytes("PRIVMSG "+ chan +" :"+ msg +"\n", "UTF-8"))
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip(bytes('\n\r', "UTF-8")) # removing any unnecessary linebreaks.
    print(ircmsg) # Here we print what's coming from the server
    #send message to channel if !ball is called
    if ircmsg.find(bytes(":!ball", "UTF-8")) != -1: 
        sendmsg(channel, msg)
    if ircmsg.find(bytes("PING :", "UTF-8")) != -1: # respond to pings
        ping()
