#!/usr/bin/env python

## openSUSE Conference 2013 - IRC Bot
## Author: Pavlos Ratis <dastergon@gmail.com>
## Features:
##  Enables irc users to ask questions easily
##  Useful info about oSC

import json
import socket
import string
import sys


def commandBot(line, room):
    '''
    Bot Commands
    '''
    complete = line[1:].split(':', 1)
    info = complete[0].split(' ')
    user = info[0].split('!')
    if line.find('!geeko out') != -1 and line.find(OWNER) != -1:
        s.send('QUIT\r\n')
        sys.exit()
    elif line.find('!website') != -1:
        s.send("PRIVMSG %s :%s: %s\r\n" % (CHAN, user[0], WEBSITE))
    elif line.find('!schedule') != -1:
        s.send("PRIVMSG %s :%s: %s\r\n" % (CHAN, user[0], SCHEDULE))
    elif line.find('!asma') != -1:
        s.send("PRIVMSG %s :%s: %s\r\n" % (CHAN, user[0],
               'http://youtu.be/Iv2WaDZi7YQ'))
    elif line.find('!ask') != -1:
            room_user = complete[1].split()
            try:
                question = complete[1].split(None, 2)
                question = string.rstrip(question[2])
            except IndexError:
                s.send("PRIVMSG %s :%s: Wrong syntax: !ask room_name question\r\n" % (CHAN, user[0]))
            else:
                if room_user[1] in room:
                    s.send("PRIVMSG %s :%s asks: %s\r\n" % (
                           room_user[1], user[0], json.dumps(question)))
    elif line.find('!help') != -1:
        s.send("PRIVMSG %s :%s: http://goo.gl/DvnQD\r\n" % (CHAN, user[0]))

if __name__ == "__main__":

    HOST = "irc.freenode.net"
    PORT = 6667
    NICK = "greek_geeko"
    IDENT = "greek0"
    REALNAME = "oSC'13 bot by Pavlos Ratis"
    CHAN = "#opensuse-conference"
    OWNER = "dastergon"
    TWITTER_USER = "openSUSE"
    WEBSITE = 'http://conference.opensuse.org'
    SCHEDULE = 'http://conference.opensuse.org/#schedule'
    ROOM = ['zeus', 'dimitra', 'hiphaistus']

    readbuffer = ""

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    s.send("JOIN :%s\r\n" % CHAN)

    while True:
        line = s.recv(2048)
        print line
        commandBot(line, ROOM)
        line = string.rstrip(line)
        line = string.split(line)
        if(line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
