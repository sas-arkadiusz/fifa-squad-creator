#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import re
from urllib.request import Request, urlopen

URL_GK = "https://www.futbin.com/19/players?page=1&version=all_nif&position=GK"

# auxiliary function that retrieves the code of a given page
def doRequest(url):
    return urllib.request.urlopen(url).read().decode()

req = Request(URL_GK, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read().decode()

# auxiliary function that returns player info
def getInfo(player_ID):

    id = player_ID    

    # pattern for name
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+')
    info_full = pattern.findall(webpage)
    name = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>', "", info_full[0])

    # pattern for club
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\w\s]+')
    info_full = pattern.findall(webpage)
    club = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="', "", info_full[0])

    # pattern for nation
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\<>=?&\/\.\-"]+title="[\w\s]+')
    info_full = pattern.findall(webpage)
    nation = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\<>=?&\/\.\-"]+title="', "", info_full[0])

    # pattern for overall
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}')
    info_full = pattern.findall(webpage)
    overall = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">', "", info_full[0])

    # pattern for position
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*<td class="">\w{2,3}')
    info_full = pattern.findall(webpage)
    position = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*<td class="">', "", info_full[0])

    # pattern for price
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\="<>/]+\r\n\s*[\w\s\-="<>/]+bold">[\d\.]+\w{1}')
    info_full = pattern.findall(webpage)
    price = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\="<>/]+\r\n\s*[\w\s\-="<>/]+bold">', "", info_full[0])

    # pattern for pace stats
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\="<>/]+\r\n\s*[\w\s\-="<>/.:;\\]+bold">[\d\.]+\w{1}[\w\s\<="-/>]+\r\n\s*[\w\d\s\<>="-:;/]+\r\n\s*[\w\d\s\<>=":;/\\\-]+M</span></td>\r\n\s*[\w\d\s\<>="_\-]+>\d{2}')
    info_full = pattern.findall(webpage)
    pace = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\="<>/]+\r\n\s*[\w\s\-="<>/.:;\\]+bold">[\d\.]+\w{1}[\w\s\<="-/>]+\r\n\s*[\w\d\s\<>="-:;/]+\r\n\s*[\w\d\s\<>=":;/\\\-]+M</span></td>\r\n\s*[\w\d\s\<>="_\-]+>', "", info_full[0])

    # pattern for shooting stats
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\="<>/]+\r\n\s*[\w\s\-="<>/.:;\\]+bold">[\d\.]+\w{1}[\w\s\<="-/>]+\r\n\s*[\w\d\s\<>="-:;/]+\r\n\s*[\w\d\s\<>=":;/\\\-]+M</span></td>\r\n\s*[\w\d\s\<>="_\-]+>\d{2}[\w\<>/]+\r\n\s*[\w\s\="_<>\-]+p-2 [\w\-\">]+>\d{2}')
    info_full = pattern.findall(webpage)
    shooting = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\="<>/]+\r\n\s*[\w\s\-="<>/.:;\\]+bold">[\d\.]+\w{1}[\w\s\<="-/>]+\r\n\s*[\w\d\s\<>="-:;/]+\r\n\s*[\w\d\s\<>=":;/\\\-]+M</span></td>\r\n\s*[\w\d\s\<>="_\-]+>\d{2}[\w\<>/]+\r\n\s*[\w\s\="_<>\-]+p-2 [\w\-\">]+>', "", info_full[0])

    # pattern for passing stats
    pattern = re.compile(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\="<>/]+\r\n\s*[\w\s\-="<>/.:;\\]+bold">[\d\.]+\w{1}[\w\s\<="-/>]+\r\n\s*[\w\d\s\<>="-:;/]+\r\n\s*[\w\d\s\<>=":;/\\\-]+M</span></td>\r\n\s*[\w\d\s\<>="_\-]+>\d{2}[\w\<>/]+\r\n\s*[\w\s\="_<>\-]+[\w\/<>]+\r\n\s*[\w\s\<>="_\-]+p-2 [\w\-"]+>\d{2}')
    info_full = pattern.findall(webpage)
    passing = re.sub(player_ID + r'/[\w\s]+" [\w\=\_\"]+>[\w\s]+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=";:&?\/\-\w\s]+title="[\s\w\-\"=<>:;\/\.]+\r\n\s*[\w\d\s\="?&\-\/]+[\w\s\d\:;<>=?&\/\.\-"]+form rating ut19[\s\w]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\="<>/]+\r\n\s*[\w\s\-="<>/.:;\\]+bold">[\d\.]+\w{1}[\w\s\<="-/>]+\r\n\s*[\w\d\s\<>="-:;/]+\r\n\s*[\w\d\s\<>=":;/\\\-]+M</span></td>\r\n\s*[\w\d\s\<>="_\-]+>\d{2}[\w\<>/]+\r\n\s*[\w\s\="_<>\-]+[\w\/<>]+\r\n\s*[\w\s\<>="_\-]+p-2 [\w\-"]+>', "", info_full[0])
    
    # print part
    #print(info_full)
    height = 0
    print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\n".format(id, name, club, nation, height, overall, position, price, pace, shooting, passing))

    # return part
    dane = [id, name, club, nation, height, overall, pace, shooting, passing]
    return dane

# DATABASE PART

# connect to a database
con = sqlite3.connect('test1.db')
# access to columns by indexes and by name
con.row_factory = sqlite3.Row
# create a cursor object
cur = con.cursor()

# create table which contains players IDs
cur.execute("DROP TABLE IF EXISTS player;")
cur.execute("""
 CREATE TABLE IF NOT EXISTS player (
     id varchar(250) NOT NULL UNIQUE,
     position varchar(250) NOT NULL
 );""")

# players IDs list
players = (
 ('239', 'gk'), ('420', 'gk'), ('595', 'gk'), ('895', 'gk'), ('515', 'gk'), ('853', 'gk'), ('1320', 'gk'), ('606', 'gk'), ('302', 'gk'), ('471', 'gk'),
 ('169', 'gk'), ('171', 'gk'), ('567', 'gk'), ('1022', 'gk'), ('1098', 'gk'), ('1413', 'gk'), ('1683', 'gk'), ('1746', 'gk'), ('3135', 'gk'), ('394', 'gk'),
)

# execute many records
cur.executemany('INSERT INTO player VALUES(?,?)', players)
# commit changes
con.commit()

# auxiliary function that returns player IDs (by derived position)
def readData(position, id_list):
    cur.execute('SELECT player.id FROM player WHERE player.position = position')
    players = cur.fetchall()
    for player in players:
        id_list.append(player['id'])


# USER PART


id_list = []

readData('gk', id_list)
#print(id_list)

for player in id_list:
    getInfo(player)
    print("\n\n")


con.close()




