import sqlite3
import sys

DB_NAME = sys.argv[1]

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

c.execute('pragma foreign_keys')
c.execute('CREATE TABLE user(name TEXT NOT NULL, id INT PRIMARY KEY NOT NULL)')
c.execute('CREATE TABLE dev(_id INT NOT NULL, dev_id TEXT PRIMARY KEY NOT NULL, foreign key(_id) references user(id))')
c.execute('CREATE TABLE entry (entry_date DATE NOT NULL, real_date DATE NOT NULL, _dev_id TEXT NOT NULL, seq INT PRIMARY KEY NOT NULL, foreign key(_dev_id) references dev(dev_id))')
c.execute('create table motion(gx REAL NOT NULL, gy REAL NOT NULL, gz REAL NOT NULL, ax REAL NOT NULL, ay REAL NOT NULL, az REAL NOT NULL, mx REAL NOT NULL, my REAL NOT NULL, int REAL NOT NULL, _seq INT NOT NULL, foreign key(_seq) references entry(seq))')
c.execute('create table lux(lux REAL NOT NULL, _seq INT NOT NULL, foreign key(_seq) references entry(seq))')

c.execute('create table authenticated(ip TEXT NOT NULL, auth_date DATE NOT NULL)')
