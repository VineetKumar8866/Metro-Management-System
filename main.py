from tabulate import tabulate
import mysql.connector as mysql
from datetime import datetime

db=mysql.connect(host='localhost',user='root',passwd='admin',database='metro')
cur=db.cursor()

def fair_calc(f,t):
    cur.execute("select {} from fair where city='{}'".format(f,t))
    c=cur.fetchone()[0]
    return c

def see_route():
    print('Munshi Pulia-------Indira Nagar-------Bhootnath------Badshah Nagar--+')
    print('    (mnp)              (ind)            (bhm)             (bdn)     |')
    print('                                                                    |')
    print('                                                                    |')
    print('+-Hazrat Ganj-------KD Singh---------University------IT Chauraha----+')
    print('|   (hzg)             (kds)            (uni)             (itc)       ')
    print('|                                                                    ')
    print('|                                                                    ')
    print('+--Charbagh----------Alambagh----------Krishna Nagar-----------Amausi')
    print('    (chr)             (alm)                (krn)               (amu) ')
    
def new_card(username):
    date=str(datetime.now())[:11]
    cur.execute('select * from cards')
    cardno=cur.fetchall()[-1][0]+1
    cur.execute("insert into cards values({},'{}','{}',0)").format(cardno,username,date)
    db.commit()

def recharge(cardno,balance):
    cur.execute("update cards set balance={} where card={}").format(balance,cardno)
    db.commit()    

def decline_card(cardno):
    cur.execute("delete from cards where card={}").format(cardno)
    db.commit()

def show_balance(cardno):
    cur.execute("select balance from cards where cardno={}".format(cardno))
    d=cur.fetchone()[0]
    return d

def see_users():
    cur.execute("select userid,username,card from users")
    d=cur.fetchall()
    h=[['User ID','User Name','Card']]
    print(tabulate(d, headers=h, tablefmt='pretty'))

def price_change(f,t,p):
    cur.execute("update fair set {}={} where city='{}'".format(f,p,t))
    db.commit()

def history():
    cur.execute("select * from users")
    d=cur.fetchall()
    h=[['User ID','User Name','From To','No. of Tokens','Amount','Card','Returning']]
    print(tabulate(d, headers=h, tablefmt='pretty'))

def revenue():
    cur.execute("select revenue from revenue")
    d=cur.fetchone()[0]
    print(tabulate([['Revenue generated is : {}'.format(d)]], tablefmt='pretty'))

def get_ticket():
    username=input('Enter name: ')
    see_route()
    f,t=tuple(input('Enter starting and ending destination\nLike "mnp-hzg" (Kindly use correct station code)\n').split('-'))
    token=int(input('Enter number of tokens: '))
    r=input('Do you want return tickets y/n? :')
    c=input('Do you have card y/n? : ')
    price=fair_calc(f,t) if r=='n' else fair_calc(f,t)*2
    if c=='y':
        cardno=int(input('Enter card number: '))
        cur.execute("select balance from cards where cardno={}".format(cardno))
        d=cur.fetchone()[0]
        rtrn=0 if r=='n' else 1
        cur.execute("select userid from users")
        userid=cur.fetchall()[-1][0]+1
        if d>price:
            cur.execute("insert into users values({},'{}','{}',{},{},{},{})").format(userid,username,f+' '+t,token,price,cardno,rtrn)
            cur.execute("update cards set balance=balance-{} where card={}").format(price,cardno)
            db.commit()
            print(tabulate([['Ticket confirmed. Current balance: {}'.format(d-price)]]))
        else:
            print('Unsufficient Balance!')
    elif c=='n':
        rtrn=0 if r=='n' else 1
        cur.execute("insert into users values({},'{}','{}',{},{},None,{})").format(userid,username,f+' '+t,token,price,rtrn)
        print(tabulate([['Ticket confirmed. You\'ve to pay {} INR'.format(price)]]))

