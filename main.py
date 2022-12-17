from tabulate import tabulate
import mysql.connector as mysql
from datetime import datetime

db = mysql.connect(host="localhost", user="root", passwd="admin", database="metro")
cur = db.cursor()


def fair_calc(f, t):
    v = "select {} from fair where station='{}'".format(f, t)
    cur.execute(v)
    c = cur.fetchone()[0]
    return c


def see_route():
    l = [
        ["Munshipulia", "mnp"],
        ["Indira Nagar", "ind"],
        ["Bhootnath Market", "bhm"],
        ["Badshah Nagar", "bdn"],
        ["Hazratganj", "hzg"],
        ["KD Singh", "kds"],
        ["University", "uni"],
        ["IT College", "itc"],
        ["Charbagh", "chr"],
        ["Alambagh", "alm"],
        ["Krishna Nagar", "krn"],
        ["CCS Airport", "ccs"],
    ]
    print(
        tabulate(l, tablefmt="rounded_grid", headers=["Station Name", "Station Code"])
    )


def new_card(username):
    date = str(datetime.now())[:11]
    cur.execute("select * from cards")
    cardno = cur.fetchall()[-1][0] + 1
    cur.execute(
        "insert into cards values({},'{}','{}',0)".format(cardno, username, date)
    )
    db.commit()
    return cardno


def recharge(cardno, balance):
    cur.execute("update cards set balance={} where card={}".format(balance, cardno))
    db.commit()


def decline_card(cardno):
    cur.execute("delete from cards where card={}".format(cardno))
    db.commit()


def show_balance(cardno):
    cur.execute("select balance from cards where card={}".format(cardno))
    d = cur.fetchone()[0]
    return d


def see_cards():
    cur.execute("select * from cards")
    d = cur.fetchall()
    print()
    print(
        tabulate(
            d,
            headers=["Card no", "User name", "Date created", "Balance"],
            tablefmt="rst",
        )
    )
    print()


def delete_user(userid):
    cur.execute("delete from users where userid={}".format(userid))
    db.commit()


def see_users():
    cur.execute("select userid,username,card from users")
    d = cur.fetchall()
    h = ["User ID", "User Name", "Card"]
    print()
    print(tabulate(d, headers=h, tablefmt="rst"))
    print()


def price_change(f, t, p):
    cur.execute("update fair set {}={} where station='{}'".format(f, p, t))
    db.commit()


def history():
    cur.execute("select * from users")
    d = cur.fetchall()
    h = [
        "User ID",
        "User Name",
        "From To",
        "No. of Tokens",
        "Amount",
        "Card",
        "Returning",
    ]
    print()
    print(tabulate(d, headers=h, tablefmt="rst"))
    print()


def revenue():
    cur.execute("select revenue from revenue")
    d = cur.fetchone()[0]
    print()
    print(
        tabulate([["Revenue generated is : {}".format(d)]], tablefmt="rounded_outline")
    )
    print()


def get_token(username):
    see_route()
    try:
        f, t = tuple(
            input(
                'Enter starting and ending destination\nLike "mnp-hzg" (Kindly use correct station code)\n'
            ).split("-")
        )
    except:
        print("You entered the destination in wrong format!")
        print()
        user_page(username)
        return None
    token = int(input("Enter number of tokens: "))
    r = input("Do you want return tickets y/n? :")
    c = input("Do you want to use your metro card y/n? : ")
    price = (fair_calc(f, t) if r == "n" else fair_calc(f, t) * 2) * token
    cur.execute("select userid from users")
    try:
        userid = cur.fetchall()[-1][0] + 1
    except:
        userid = 1
    if c == "y":
        cardno = int(input("Enter card number: "))
        cur.execute("select balance from cards where card={}".format(cardno))
        d = cur.fetchone()[0]
        rtrn = 0 if r == "n" else 1
        if d > price:
            cur.execute(
                "insert into users values({},'{}','{}',{},{},{},{})".format(
                    userid, username, f + "-" + t, token, price, cardno, rtrn
                )
            )
            cur.execute(
                "update cards set balance=balance-{} where card={}".format(
                    price, cardno
                )
            )
            db.commit()
            print()
            print(
                tabulate(
                    [["Ticket confirmed. Current balance: {}".format(d - price)]],
                    tablefmt="rounded_outline",
                )
            )
            cur.execute("update revenue set revenue=revenue+{}".format(price))
        else:
            print()
            print(tabulate([["Unsufficient Balance!"]], tablefmt="rounded_outline"))
    elif c == "n":
        rtrn = 0 if r == "n" else 1
        cur.execute(
            "insert into users values({},'{}','{}',{},{},1001,{})".format(
                userid, username, f + "-" + t, token, price, rtrn
            )
        )
        print()
        print(
            tabulate(
                [["Ticket confirmed. You've to pay {} INR".format(price)]],
                tablefmt="rounded_outline",
            )
        )
        cur.execute("update revenue set revenue=revenue+{}".format(price))
        print()


def menu():
    print(
        tabulate(
            [["Welcome to Lucknow Metro Rail Corporation LTD."]],
            tablefmt="double_outline",
        )
    )
    print(tabulate([["Login Page"]], tablefmt="git"))
    print(
        tabulate(
            [["To login as admin press 1"], ["To login as user press 2"]],
            tablefmt="double_outline",
        )
    )
    c = int(input("Enter what you've chosen: "))
    return c


def see_fair_matrix():
    cur.execute("select * from fair")
    d = cur.fetchall()
    h = [
        "",
        "mnp",
        "ind",
        "bhm",
        "bdn",
        "itc",
        "uni",
        "kds",
        "hzg",
        "chr",
        "alm",
        "krn",
        "ccs",
    ]
    print(tabulate(d, tablefmt="simple_grid", headers=h))


def user_page(username):
    c = ""
    while c != "exit":
        t = [
            ["To see route press 1"],
            ["To get token press 2"],
            ["To recharge your card press 3"],
            ["To see balance press 4"],
            ["To issue a new card press 5"],
            ["To see fair price press 6"],
            ["To go back to login page press 7"],
            ['To exit type "exit"'],
        ]
        print(tabulate(t, tablefmt="double_outline"))
        print()
        c = input("Enter what you have choosen: ")
        if c == "1":
            see_route()
        elif c == "2":
            get_token(username)
        elif c == "3":
            balance = int(input("Enter the amount: "))
            cardno = int(input("Enter Card no. : "))
            recharge(cardno, balance)
        elif c == "4":
            cardno = int(input("Enter card no.: "))
            print()
            print(
                tabulate(
                    [["Your card has {} Rupees".format(show_balance(cardno))]],
                    tablefmt="rounded_outline",
                )
            )
            print()
        elif c == "5":
            username = input("Enter user name: ")
            c = new_card(username)
            print()
            print(
                tabulate(
                    [["Your card number is: {}".format(c)]], tablefmt="rounded_outline"
                )
            )
            print()
        elif c == "6":
            f, t = tuple(
                input(
                    'Enter starting and ending destination\nLike "mnp-hzg" (Kindly use correct station code)\n'
                ).split("-")
            )

            print()
            print(
                tabulate(
                    [["This ride would cost you {} Rupees".format(fair_calc(f, t))]],
                    tablefmt="rounded_outline",
                )
            )
            print()
        elif c == "7":
            login_page()
            return None
        elif c == "exit":
            break


def admin_page():
    c = ""
    while c != "exit":
        t = [
            ["To see route press 1"],
            ["To see users press 2"],
            ["To delete user press 3"],
            ["To see history press 4"],
            ["To see revenue earned press 5"],
            ["To change the price press 6"],
            ["To see fair price press 7"],
            ["To decline a card press 8"],
            ["To see registered cards press 9 "],
            ["To see fair matrix press 10"],
            ["To go back to login page press 11"],
            ['To exit type "exit"'],
        ]
        print(tabulate(t, tablefmt="double_outline"))
        print()
        c = input("Enter what you have choosen: ")
        if c == "1":
            see_route()
        elif c == "2":
            see_users()
        elif c == "3":
            userid = int(input("Enter the user id: "))
            delete_user(userid)
        elif c == "4":
            history()
        elif c == "5":
            revenue()
        elif c == "6":
            f, t = tuple(
                input(
                    'Enter starting and ending destination\nLike "mnp-hzg" (Kindly use correct station code)\n'
                ).split("-")
            )
            p = int(input("Enter the new price: "))
            price_change(f, t, p)
        elif c == "7":
            f, t = tuple(
                input(
                    'Enter starting and ending destination\nLike "mnp-hzg" (Kindly use correct station code)\n'
                ).split("-")
            )
            print()
            print(
                tabulate(
                    [["This ride would cost you {} Rupees".format(fair_calc(f, t))]],
                    tablefmt="rounded_outline",
                )
            )
            print()
        elif c == "8":
            cardno = int(input("Enter the card no.: "))
            decline_card(cardno)
        elif c == "9":
            see_cards()
        elif c == "10":
            see_fair_matrix()
        elif c == "11":
            login_page()
            return None
        elif c == "exit":
            break


def login_page():
    c = menu()
    if c == 1:
        passwd = input("Enter password: ")
        if passwd == "admin":
            admin_page()
        else:
            print()
            print(
                tabulate([["You entered wrong password!"]], tablefmt="rounded_outline")
            )
            print()
            login_page()
    elif c == 2:
        username = input("Enter user name: ")
        user_page(username)


login_page()
db.commit()
