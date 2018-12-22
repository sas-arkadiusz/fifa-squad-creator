#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import re
from urllib.request import Request, urlopen

URL_GK = "https://www.futbin.com/19/players?page=1&version=all_nif&position=GK"
URL_RB = "https://www.futbin.com/19/players?page=1&position=RB,RWB&version=all_nif"
URL_LB = "https://www.futbin.com/19/players?page=1&version=all_nif&position=LB,LWB"
URL_CB = "https://www.futbin.com/19/players?page=1&version=all_nif&position=CB"
URL_CM = "https://www.futbin.com/19/players?page=1&version=all_nif&position=CDM,CM,CAM"
URL_LM = "https://www.futbin.com/19/players?page=1&version=all_nif&position=LM,LW,LF"
URL_RM = "https://www.futbin.com/19/players?page=1&version=all_nif&position=RM,RW,RF"
URL_ST = "https://www.futbin.com/19/players?page=1&position=CF,ST&version=all_nif"

# auxiliary function that retrieves the code of a given page
def doRequest(url):
    return urllib.request.urlopen(url).read().decode()


# auxiliary function that returns player info
def getInfo(player_ID, URL):

    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode()

    id = player_ID    

    # pattern for name
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+')
    info_full = pattern.findall(webpage)
    name = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>', "", info_full[0])

    # pattern for club
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+')
    info_full = pattern.findall(webpage)
    club = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="', "", info_full[0])

    # pattern for nation
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+')
    info_full = pattern.findall(webpage)
    nation = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="', "", info_full[0])

    # pattern for overall
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}')
    info_full = pattern.findall(webpage)
    overall = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">', "", info_full[0])

    # pattern for position
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}')
    info_full = pattern.findall(webpage)
    position = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">', "", info_full[0])

    # pattern for price
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}')
    info_full = pattern.findall(webpage)
    price = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">', "", info_full[0])

    # pattern for pace stats
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}')
    info_full = pattern.findall(webpage)
    pace = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>', "", info_full[0])

    # pattern for shooting stats
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}')
    info_full = pattern.findall(webpage)
    shooting = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>', "", info_full[0])

    #pattern for passing stats
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}')
    info_full = pattern.findall(webpage)
    passing = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>', "", info_full[0])

    # pattern for dribbling stats
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}')
    info_full = pattern.findall(webpage)
    dribbling = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>', "", info_full[0])

    # pattern for defending stats
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}')
    info_full = pattern.findall(webpage)
    defending = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>', "", info_full[0])

    # pattern for physicality stats
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}')
    info_full = pattern.findall(webpage)
    physicality = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>', "", info_full[0])

    # pattern for height
    pattern = re.compile(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td>\d{3}')
    info_full = pattern.findall(webpage)
    height = re.sub(player_ID + r'/[\w\s\.\']+" [\w\=\_\"\.]+>[\w\s\']+</a>\r\n\s*[\<>/\w]+\r\n\s*\r\n\s*<div>\r\n\s*[\<>=_";:&?\/\-\,\w\s]+title="[\w\s\-]+"[\w\s\-\"<>:;=\/\.]+\r\n\s*[\w\s\=<>"?&_\/\-\,]+title="[\w]+[\w\s\-\="><:;\/\.]+\r\n\s*[\w\s\=_"?&><:;\/\.\,\-]+\r\n\s*</span>\r\n\s*</div>\r\n\s*</div>\r\n\s*</td>\r\n\s*[\w\s\<>="]+">\d{2}[\w\<>/]+\r\n\s*[\w\s\<="]+">\w{2,3}</td>\r\n\s*[\w\s\<="->]+</td>\r\n\s*[\w\s\<>="_-]+">[\d\.]+\w{1}[\w\s\<="_>/\.\-]+\r\n\s*<td>\d{1}[\w\s\<>=:;/"\-]+\r\n\s*<td>\d{1}[\w\s\=":;<>/\-\\]+>[H,L,M]{1}</span></td>\r\n\s*<td><[\w\s\="\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td><[\w\s\=_"\-]+>\d{2}</span></td>\r\n\s*<td>', "", info_full[0])
    
    #print(info_full)
    #print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(id, name, club, nation, height, overall, position, price, pace, shooting, passing, dribbling, defending, physicality))

    # return part
    dane = [id, name, club, nation, position, height, overall, price, pace, shooting, passing, dribbling, defending, physicality]
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
 ('169', 'gk'), ('171', 'gk'), ('567', 'gk'), ('1022', 'gk'), ('1098', 'gk'),
 ('434', 'rb'), ('317', 'rb'), ('361', 'rb'), ('614', 'rb'), ('259', 'rb'), ('532', 'rb'), ('817', 'rb'), ('869', 'rb'), ('871', 'rb'), ('1025', 'rb'),
 ('177', 'rb'), ('201', 'rb'), ('741', 'rb'), ('1337', 'rb'), ('1417', 'rb'),
 ('603', 'lb'),  ('356', 'lb'),  ('155', 'lb'), ('437', 'lb'), ('905', 'lb'), ('771', 'lb'), ('395', 'lb'), ('822', 'lb'), ('920', 'lb'), ('323', 'lb'),
 ('489', 'lb'), ('539', 'lb'), ('740', 'lb'), ('1166', 'lb'), ('2571', 'lb'),
 ('594', 'cb'), ('894', 'cb'), ('146', 'cb'), ('421', 'cb'), ('852', 'cb'), ('355', 'cb'), ('357', 'cb'), ('517', 'cb'), ('724', 'cb'), ('157', 'cb'),
 ('158', 'cb'), ('306', 'cb'), ('387', 'cb'), ('427', 'cb'), ('609', 'cb'),
 ('291', 'cm'), ('592', 'cm'), ('596', 'cm'), ('147', 'cm'), ('295', 'cm'), ('386', 'cm'), ('598', 'cm'), ('242', 'cm'), ('353', 'cm'), ('423', 'cm'),
 ('514', 'cm'), ('605', 'cm'), ('354', 'cm'), ('725', 'cm'), ('6419', 'cm'),
 ('846', 'lm'), ('385', 'lm'), ('351', 'lm'), ('720', 'lm'), ('154', 'lm'), ('305', 'lm'), ('466', 'lm'), ('1326', 'lm'), ('189', 'lm'), ('436', 'lm'),
 ('611', 'lm'), ('767', 'lm'), ('903', 'lm'), ('525', 'lm'), ('254', 'lm'),
 ('461', 'rm'), ('602', 'rm'), ('854', 'rm'), ('308', 'rm'), ('310', 'rm'), ('435', 'rm'), ('1650', 'rm'), ('170', 'rm'), ('314', 'rm'), ('390', 'rm'),
 ('729', 'rm'), ('860', 'rm'), ('1366', 'rm'), ('1988', 'rm'), ('256', 'rm'),
 ('143', 'st'), ('341', 'st'), ('343', 'st'), ('418', 'st'), ('294', 'st'), ('512', 'st'), ('849', 'st'), ('896', 'st'), ('664', 'st'), ('464', 'st'),
 ('806', 'st'), ('723', 'st'), ('932', 'st'), ('1322', 'st'), ('430', 'st'), 
 
)

# execute many records
cur.executemany('INSERT INTO player VALUES(?,?)', players)
# commit changes
con.commit()

# auxiliary function that returns player IDs (by derived position)
def readData(position, id_list):
    if position == 'gk':
        cur.execute('SELECT player.id FROM player WHERE player.position = "gk"')
    if position == 'rb':
        cur.execute('SELECT player.id FROM player WHERE player.position = "rb"')
    if position == 'lb':
        cur.execute('SELECT player.id FROM player WHERE player.position = "lb"')
    if position == 'cb':
        cur.execute('SELECT player.id FROM player WHERE player.position = "cb"')
    if position == 'cm':
        cur.execute('SELECT player.id FROM player WHERE player.position = "cm"')
    if position == 'lm':
        cur.execute('SELECT player.id FROM player WHERE player.position = "lm"')
    if position == 'rm':
        cur.execute('SELECT player.id FROM player WHERE player.position = "rm"')
    if position == 'st':
        cur.execute('SELECT player.id FROM player WHERE player.position = "st"')
        
    players = cur.fetchall()
    for player in players:
        id_list.append(player['id'])

# create table which contains player's squad
cur.execute("DROP TABLE IF EXISTS squad;")
cur.execute("""
 CREATE TABLE IF NOT EXISTS squad (
     id varchar(250) UNIQUE,
     squad_position varchar(250) NOT NULL UNIQUE
 );""")

# squad players list
squad = ((239, 'gk'), (434, 'rb'), (None, 'lb'),
         (None, 'cb_1'), (None, 'cb_2'), (None, 'cm_1'),
         (None, 'cm_2'), (None, 'lm'), (None, 'rm'), (None, 'st_1'), (None, 'st_2'))

# execute many records
cur.executemany('INSERT INTO squad VALUES(?,?)', squad)

# auxiliary function that short information about player's squad
def displaySquad():
    cur.execute('SELECT squad.id, squad.squad_position FROM squad')
    players = cur.fetchall()
    for player in players:
        if (player['id'] == None):
            print("Niedodano zawodnika")
            continue
        elif (player['squad_position'] == 'gk'):
            url = URL_GK
        elif (player['squad_position'] == 'rb'):
            url = URL_RB
        elif (player['squad_position'] == 'lb'):
            url = URL_LB
        elif (player['squad_position'] == 'cb_1' or player['squad_position'] == 'cb_2'):
            url = URL_CB
        elif (player['squad_position'] == 'cm_1' or player['squad_position'] == 'cm_2'):
            url = URL_CM
        elif (player['squad_position'] == 'lm'):
            url = URL_LM
        elif (player['squad_position'] == 'rm'):
            url = URL_RM
        elif (player['squad_position'] == 'st_1' or player['squad_position'] == 'st_2'):
            url = URL_ST
        full_info = getInfo(player['id'], url)
        print(full_info[4], ": ", full_info[1])

# auxiliary function that detailed information about player's squad
def displayDetailedSquad():
    cur.execute('SELECT squad.id, squad.squad_position FROM squad')
    players = cur.fetchall()
    for player in players:
        if (player['id'] == None):
            print("Niedodano zawodnika")
            continue
        elif (player['squad_position'] == 'gk'):
            url = URL_GK
        elif (player['squad_position'] == 'rb'):
            url = URL_RB
        elif (player['squad_position'] == 'lb'):
            url = URL_LB
        elif (player['squad_position'] == 'cb_1' or player['squad_position'] == 'cb_2'):
            url = URL_CB
        elif (player['squad_position'] == 'cm_1' or player['squad_position'] == 'cm_2'):
            url = URL_CM
        elif (player['squad_position'] == 'lm'):
            url = URL_LM
        elif (player['squad_position'] == 'rm'):
            url = URL_RM
        elif (player['squad_position'] == 'st_1' or player['squad_position'] == 'st_2'):
            url = URL_ST
        full_info = getInfo(player['id'], url)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nPosition: {4}\nHeight: {5} cm\nOverall: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))
        
# function that calculates value of a player
def player_value(price):
    length = len(price)
    if price[length - 1] == 'K':
        price = price[:(length-1)]
        price = float(price)
        price = price*1000
        return price
    elif price[length - 1] == 'M':
        price = price[:(length-1)]
        price = float(price)
        price = price*1000000
        return price
    else:
        price = float(price)
        return price

# function that shows stats of your time

def calculateValues():
    cur.execute('SELECT squad.id, squad.squad_position FROM squad')
    players = cur.fetchall()

    height = 0
    overall = 0
    price = 0
    pace = 0    
    shooting = 0
    passing = 0
    dribbling = 0
    defending = 0
    physicality = 0
    counter = 0
    
    for player in players:
        if (player['id'] == None):
            #print("Niedodano zawodnika")
            continue
        elif (player['squad_position'] == 'gk'):
            url = URL_GK
            counter = counter + 1
        elif (player['squad_position'] == 'rb'):
            url = URL_RB
            counter = counter + 1
        elif (player['squad_position'] == 'lb'):
            url = URL_LB
            counter = counter + 1
        elif (player['squad_position'] == 'cb_1' or player['squad_position'] == 'cb_2'):
            url = URL_CB
            counter = counter + 1
        elif (player['squad_position'] == 'cm_1' or player['squad_position'] == 'cm_2'):
            url = URL_CM
            counter = counter + 1
        elif (player['squad_position'] == 'lm'):
            url = URL_LM
            counter = counter + 1
        elif (player['squad_position'] == 'rm'):
            url = URL_RM
            counter = counter + 1
        elif (player['squad_position'] == 'st_1' or player['squad_position'] == 'st_2'):
            url = URL_ST
            counter = counter + 1
        if (player['id'] != None):
            full_info = getInfo(player['id'], url)
            full_info[5] = int(full_info[5])
            height = height + full_info[5]
            full_info[6] = int(full_info[6])
            overall = overall + full_info[6]
            player_price = player_value(full_info[7])
            price = price + player_price
            full_info[8] = int(full_info[8])
            pace = pace + full_info[8]
            full_info[9] = int(full_info[9])
            shooting = shooting + full_info[9]
            full_info[10] = int(full_info[10])
            passing = passing + full_info[10]
            full_info[11] = int(full_info[11])
            dribbling = dribbling + full_info[11]
            full_info[12] = int(full_info[12])
            defending = defending + full_info[12]
            full_info[13] = int(full_info[13])
            physicality = physicality + full_info[13]

    if (counter != 0):
        avg_height = height / counter
        avg_overall = overall / counter
        avg_price = price / counter
        avg_pace = pace / counter
        avg_shooting = shooting / counter
        avg_passing = passing / counter
        avg_dribbling = dribbling / counter
        avg_defending = defending / counter
        avg_physicality = physicality / counter
        
        print("\n")
        print("Players in the squad: ", counter)
        print("Total value of the squad: ", price)
        print("Average overall: ", avg_overall)
        print("Average price: ", avg_price)
        print("Average height: ", avg_height, " cm")
        print("Average pace: ", avg_pace)
        print("Average shooting: ", avg_shooting,)
        print("Average passing: ", avg_passing)
        print("Average dribbling: ", avg_dribbling)
        print("Average defending: ", avg_defending)
        print("Average physicality: ", avg_physicality)

# function that modifies player in player's squad
def modifyPlayer(player_id, squad_position):
    cur.execute("UPDATE squad SET id = (?) WHERE squad_position = (?)", (player_id, squad_position))


# USER PART

# display functions
def displayGK():
    readData('gk', id_list)
    for player in id_list:
        full_info = getInfo(player, URL_GK)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))
def displayRB():
    readData('rb', id_list)
    for player in id_list:
        full_info = getInfo(player, URL_RB)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))
def displayLB():
    readData('lb', id_list)
    for player in id_list:
        full_info = getInfo(player, URL_LB)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))
def displayCB():
    readData('cb', id_list)
    for player in id_list:
        full_info = getInfo(player, URL_CB)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))
def displayCM():
    readData('cm', id_list)
    for player in id_list:
        full_info = getInfo(player, URL_CM)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))
def displayLM():
    readData('lm', id_list)
    for player in id_list:
        full_info = getInfo(player, URL_LM)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))
def displayRM():
    readData('rm', id_list)
    for player in id_list:
        full_info = getInfo(player, URL_RM)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))
def displayST():
    readData('st', id_list)
    for player in id_list:
        full_info = getInfo(player, URL_ST)
        print("ID: {0}\nName: {1}\nClub: {2}\nNation: {3}\nHeight: {4} cm\nOverall: {5}\nPosition: {6}\nPrice: {7}\n\nSTATS:\nPace: {8}\nShooting: {9}\nPassing: {10}\nDribbling: {11}\nDefending: {12}\nPhysicality: {13}\n".format(full_info[0], full_info[1], full_info[2], full_info[3], full_info[4], full_info[5], full_info[6], full_info[7], full_info[8], full_info[9], full_info[10], full_info[11], full_info[12], full_info[13]))


# main program
        
id_list = []

while(True):
    option = input("\nWhat do you want to do? \n\t1. Show my squad\n\t2. Show details of my players\n\t3. Modify my squad\n\t4. Display players \n\t5. Display club info\nOption: ")

    if (option == '1'):
        print("\n")
        displaySquad()
        print("\n")
        continue

    elif (option == '2'):
        print("\n")
        displayDetailedSquad()
        print("\n")
        continue

    elif (option == '3'):
        player_modify = input("Which position do you want to modify?\n\t1. GK\n\t2. RB\n\t3. LB\n\t4. CB_1\n\t5. CB_2\n\t6. CM_1\n\t7. CM_2\n\t8. LM\n\t9. RM\n\t10. ST_1\n\t11. ST_2\nPosition: ")
        print("\n")
        if (player_modify == 'GK' or player_modify == 'gk' or player_modify == '1'):
            display = input("Do you want do display all GKs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayGK()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'gk')
            con.commit()
        if (player_modify == 'RB' or player_modify == 'rb' or player_modify == '2'):
            display = input("Do you want do display all RBs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayRB()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'rb')
            con.commit()
        if (player_modify == 'LB' or player_modify == 'lb' or player_modify == '3'):
            display = input("Do you want do display all LBs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayLB()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'lb')
            con.commit()
        if (player_modify == 'CB_1' or player_modify == 'cb_1' or player_modify == '4'):
            display = input("Do you want do display all CBs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayCB()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'cb_1')
            con.commit()
        if (player_modify == 'CB_2' or player_modify == 'cb_2' or player_modify == '5'):
            display = input("Do you want do display all CBs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayCB()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'cb_2')
            con.commit()
        if (player_modify == 'CM_1' or player_modify == 'cm_1' or player_modify == '6'):
            display = input("Do you want do display all CMs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayCM()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'cm_1')
            con.commit()
        if (player_modify == 'CM_2' or player_modify == 'cm_2' or player_modify == '7'):
            display = input("Do you want do display all CMs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayCM()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'cm_2')
            con.commit()
        if (player_modify == 'LM' or player_modify == 'lm' or player_modify == '8'):
            display = input("Do you want do display all LMs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayLM()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'lm')
            con.commit()
        if (player_modify == 'RM' or player_modify == 'rm' or player_modify == '9'):
            display = input("Do you want do display all RBs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayRM()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'rm')
            con.commit()
        if (player_modify == 'ST_1' or player_modify == 'st_1' or player_modify == '10'):
            display = input("Do you want do display all STs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayST()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'st_1')
            con.commit()
        if (player_modify == 'ST_2' or player_modify == 'st_2' or player_modify == '11'):
            display = input("Do you want do display all STs? Y/N: ")
            if (display == 'Y' or display == 'y'):
                displayST()
            player_modify = input("Type new player's ID: ")
            modifyPlayer(player_modify, 'st_2')
            con.commit()
        print("\n")
        continue

    elif (option == '4'):
        player_position = input("Which position do you want to display? \n\t1. GK\n\t2. RB\n\t3. LB\n\t4. CB\n\t5. CM\n\t6. LM\n\t7. RM\n\t8. ST\nPosition: ")
        print("\n")
        if (player_position == 'GK' or player_position == 'gk' or player_position == '1'):
            displayGK()
        elif (player_position == 'RB' or player_position == 'rb' or player_position == '2'):
            displayRB()
        elif (player_position == 'LB' or player_position == 'lb' or player_position == '3'):
            displayLB()
        elif (player_position == 'CB' or player_position == 'cb' or player_position == '4'):
            displayCB()
        elif (player_position == 'CM' or player_position == 'cm' or player_position == '5'):
            displayCM()
        elif (player_position == 'LM' or player_position == 'lm' or player_position == '6'):
            displayLM()
        elif (player_position == 'RM' or player_position == 'rm' or player_position == '7'):
            displayRM()
        elif (player_position == 'ST' or player_position == 'st' or player_position == '8'):
            displayST()
        print("\n")
        continue

    elif (option == '5'):
        calculateValues()
        
    else:
        print("Unimplemented method")
con.close()
