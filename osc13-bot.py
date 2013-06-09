#!/usr/bin/env python

## openSUSE Conference 2013 - IRC Bot
## Author: Pavlos Ratis <dastergon@gmail.com>
## Features:
##  Live feed from the oSC
##  Enables irc users to ask questions easily
##  Useful infos about oSC

import json
import simplejson
import socket
import string
import sys
import urllib


def parseTweet(query):
    '''
    Messing with Twitter Search API
    '''
    search = urllib.urlopen(
        "http://search.twitter.com/search.json?q=from:" + query)
    dict = simplejson.loads(search.read())
    result = dict['results']
    return result[0]['text']


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
    elif line.find('!geeko website') != -1:
        s.send("PRIVMSG %s :%s: %s\r\n" % (CHAN, user[0], WEBSITE))
    elif line.find('!geeko schedule') != -1:
        s.send("PRIVMSG %s :%s: %s\r\n" % (CHAN, user[0], SCHEDULE))
    elif line.find('!ask') != -1:
            room_user = complete[1].split()
            question = complete[1].split(None, 2)
            question = string.rstrip(question[2])
            if room_user[1] in room:
                s.send("PRIVMSG %s :%s asks: %s\r\n" % (
                    room_user[1], user[0], json.dumps(question)))
    elif line.find('!help') != -1:
        s.send("PRIVMSG %s :%s: !geeko {website, schedule}, !ask room_name question\r\n" % (CHAN, user[0]))

if __name__ == "__main__":

    HOST = "irc.freenode.net"
    PORT = 6667
    NICK = "greek_geeko"
    IDENT = "greek0"
    REALNAME = "oSC'13 bot by Pavlos Ratis"
    CHAN = "#osc13"
    OWNER = "dastergon"
    TWITTER_USER = "openSUSE"
    WEBSITE = 'http://conference.opensuse.org'
    SCHEDULE = 'http://conference.opensuse.org/#schedule'
    ROOM = ['room1', 'room2', 'room3']

    readbuffer = ""

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("NICK %s\r\n" % NICK)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    s.send("JOIN :%s\r\n" % CHAN)

    tweet = []
    tweet.append(parseTweet(TWITTER_USER))
    counter = 1
    while True:
        line = s.recv(512)  # issue for tweets: recv() waits for any input, so if there is no input the loop doesn't continue.
        print line
        tweet.append(parseTweet(TWITTER_USER))
        if tweet[counter] != tweet[counter - 1]:
            s.send(
                "PRIVMSG %s :!now: %s\r\n" % (CHAN, json.dumps(tweet[counter])))  # update latest tweet
            counter = 0
            tweet = []
            tweet.append(parseTweet(TWITTER_USER))
        counter += 1
        commandBot(line, ROOM)
        line = string.rstrip(line)
        line = string.split(line)
        if(line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
