import mysql.connector as mysql

db1 = mysql.connect(host="localhost", user="root", passwd="admin")
cur2 = db1.cursor()
cur2.execute("drop database metro")
cur2.execute("create database metro")

db = mysql.connect(host="localhost", user="root", passwd="admin", database="metro")
cur = db.cursor()

a = """
create table users(
    userid int primary key,
    username varchar(20),
    fromto varchar(50),
    token int,
    amount int,
    card int,
    rtrn int   
)
"""

b = """
create table cards(
    card int,
    username varchar(20),
    created date,
    balance int
)
"""

c = """
create table revenue(
revenue int
)
"""

d = """
create table fair(
    station varchar(20), 
    mnp int, 
    ind int, 
    bhm int,
    bdn int, 
    itc int, 
    uni int, 
    kds int, 
    hzg int,
    chr int, 
    alm int, 
    krn int, 
    ccs int
)
"""
e1 = "insert into fair values('mnp',0,10,20,30,40,50,60,70,80,90,100,110)"
e2 = "insert into fair values('ind',10,0,10,20,30,40,50,60,70,80,90,100)"
e3 = "insert into fair values('bhm',20,10,0,10,20,30,40,50,60,70,80,90)"
e4 = "insert into fair values('bdn',30,20,10,0,10,20,30,40,50,60,70,80)"
e5 = "insert into fair values('itc',40,30,20,10,0,10,20,30,40,50,60,70)"
e6 = "insert into fair values('uni',50,40,30,20,10,0,10,20,30,40,50,60)"
e7 = "insert into fair values('kds',60,50,40,30,20,10,0,10,20,30,40,50)"
e8 = "insert into fair values('hzg',70,60,50,40,30,20,10,0,10,20,30,40)"
e9 = "insert into fair values('chr',80,70,60,50,40,30,20,10,0,10,20,30)"
e10 = "insert into fair values('alm',90,80,70,60,50,40,30,20,10,0,10,20)"
e11 = "insert into fair values('krn',100,90,80,70,60,50,40,30,20,10,0,10)"
e12 = "insert into fair values('ccs',110,100,90,80,70,60,50,40,30,20,10,0)"
e13 = "insert into users values(1,'Sample_user','mnp-ccs',1,100,1000,1)"
e14 = "insert into cards values(1000,'Sample_user','2000-01-01',0)"
e15 = "insert into revenue values(0)"

l = [a, b, c, d, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]
for i in l:
    cur.execute(i)
db.commit()
