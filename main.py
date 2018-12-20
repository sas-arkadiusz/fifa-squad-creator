#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
import re
import urllib.request

URL_GK = "https://www.futbin.com/19/players?page=1&version=all_nif&position=GK"

#auxiliary function that retrieves the code of a given page
def doRequest(url):
    return urllib.request.urlopen(url).read().decode()

# connect to the local database
con = sqlite3.connect('test1.db')

# access to columns by indexes and by name
con.row_factory = sqlite3.Row

# create a cursor object
cur = con.cursor()

""" CREATE TABLES FOR PLAYERS """

# goalkeeper
cur.execute("""
     CREATE TABLE IF NOT EXISTS goalkeeper (
     id INTEGER PRIMARY KEY ASC,
     name varchar(250) NOT NULL,
     club varchar(250) NOT NULL,
     nation varchar(250) NOT NULL,
     pac INTEGER NOT NULL,
     sho INTEGER NOT NULL,
     pas INTEGER NOT NULL,
     dri INTEGER NOT NULL,
     def INTEGER NOT NULL,
     phy INTEGER NOT NULL,
     height INTEGER NOT NULL,
     )""")
