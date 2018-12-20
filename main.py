#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import re
from urllib.request import Request, urlopen

URL_GK = "https://www.futbin.com/19/players?page=1&version=all_nif&position=GK"

#auxiliary function that retrieves the code of a given page
def doRequest(url):
    return urllib.request.urlopen(url).read().decode()

req = Request(URL_GK, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read().decode()

player_ID = '239'

def getInfo():
    #pattern = re.compile(player_ID + r'/[\w\s]+">\s*\n\s*')
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>')
    info_full = pattern.findall(webpage)
    id = player_ID
    name = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>', "Name: ", info_full[0])
    name = re.sub(r'</a>', "", name)
    print("ID: {0}\n{1}".format(id, name))

getInfo()
