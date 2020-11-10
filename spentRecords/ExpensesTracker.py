import sqlite3
import time
import datetime
import uuid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('ggplot')

from tabulate import tabulate
import os.path

conn= sqlite3.connect('spent.db')
c=conn.cursor()



def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS expenses(amount REAL, category STRING, message STRING, date STRING, buying_date STRING)")
def add_colum():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "spent.db")
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()

    cursor = c.execute('SELECT * FROM expenses')
    names = [description[0] for description in cursor.description]
    if 'buyingDate' not in names:
        sql = 'ALTER TABLE expenses ADD COLUMN buyingDate STRING'
        c.execute(sql)
    print(names)
def dynamic_data_entry(amount, category, message="", timestamp=""):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "spent.db")
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()

    id = uuid.uuid4().int & (1<<20)-1

    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y %H:%M:%S')) #('%Y-%m-%d %H:%M:%S')

    # Convert to timestamp
    day, month, year = map(int, timestamp.split('.'))
    date_timestamp = str(datetime.date(year, month, day))
    date_timestamp = str(datetime.datetime.strptime(date_timestamp, '%Y-%m-%d').strftime('%d-%m-%Y'))

    #date_timestamp = time.mktime(time.strptime(timestamp, "%d/%m/%Y"))

    c.execute("INSERT INTO expenses(amount, category, message, date, buyingDate) VALUES(?,?,?,?,?)", (amount, category, message, date, date_timestamp))
    conn.commit()

def read_from_db(type = None):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "spent.db")
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()


    if type:
        sql = '''select * from expenses where category = '{}' '''.format(type)
        sql_sum = '''select sum(amount) from expenses where category = '{}' '''.format(type)
    else:
        sql = '''select * from expenses'''.format(type)
        sql_sum = '''select sum(amount) from expenses'''.format(type)

    c.execute(sql)
    tabelle = c.fetchall()

    c.execute(sql_sum)
    summe = c.fetchone()[0]

    print(summe)
    print(80 * '#')
    print(tabulate(tabelle))


def graph_data(fr='', til=''):

    if fr and not til:
        raise AssertionError('du muss ein Beginndatum und Enddatum eingeben!')

    elif til and not fr:
        raise AssertionError('du muss ein Beginndatum und Enddatum eingeben!')

    elif fr and til:
        #der Datum Eintrag auftrennen
        day, month, year = map(int, fr.split('.'))
        tild, tilm, tily= map(int,til.split('.'))
        #jedes Element zu Zeitformat
        date_from = str(datetime.date(year, month, day))
        date_til = str(datetime.date(tild, tilm, tily))
        #
        date_from = str(datetime.datetime.strptime(date_from, '%Y-%m-%d').strftime('%d-%m-%Y'))
        date_til= str(datetime.datetime.strptime(date_til, '%Y-%m-%d').strftime('%d-%m-%Y'))
        #

        sql= '''select date, amount, buyingDate from expenses where  amount between '{}' and '{}' '''.format(date_from, date_til)

    else:
        sql= 'SELECT amount, date, buyingDate FROM expenses'

    #c.execute('SELECT date, amount from expenses')

    c.execute(sql)
    amount = []
    dates= []
    buyingDate=[]
    for row in c.fetchall():
        print(row[0])
        print(row[1])
        print((row[2]))
        dates.append(int(row[0]))
        amount.append(int(row[1]))
        buyingDate.append(int((row[2])))
    # ax sind die Abbildungen und bei subplots(row, cols) wo sie sich befinden
    fig, (ax1, ax2)= plt.subplots(1,2, sharex=True)
    #plt.plot_date(dates, amount, '-')
    ax1[0,0].plot_date(buyingDate, amount, 'r', '-')
    ax1[0,0].set_title('Einkaufsdatum vs Ausgabe')
    ax2[0,1].plot_date(date,amount, 'b', '-' )
    ax2[0,1].set_title('Eintragsdatum vs Ausgabe')

    plt.show()

def delete(amount, category, message="", timestamp=""):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "spent.db")
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()

    if message:

        sql = '''delete from expenses where amount = '{}' and category = '{}' and message = '{}' '''. format(amount, category, message)

    elif timestamp:

        date_timestamp = time.mktime(time.strptime(timestamp, "%d/%m/%Y"))
        sql = '''delete from expenses where amount = '{}' and category = '{}' and date_timestamp = '{}' '''.format(amount, category, date_timestamp)

    else:

        sql = '''delete from expenses where amount = '{}' and category = '{}' '''.format(amount, category)

    c.execute(sql)
    conn.commit()

    c.execute('SELECT * FROM expenses')
    tabelle_nach = c.fetchall()
    print(tabulate(tabelle_nach))



def update_one(am, cat, date='', new_am="", new_cat="", new_date=''):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "spent.db")
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()

    if new_am:
        sql_update = '''update expenses set amount = '{}' where amount = '{}' and category = '{}' 
        '''.format(new_am, am, cat)

    elif new_cat:
        sql_update = '''update expenses set category = '{}' where amount = '{}' and category = '{}' 
        '''.format(new_cat, am, cat)

    elif date:
        sql_update= '''update expenses set amount = '{}' or category = '{}' where amount = '{}' and category = '{}' and 
         buyingDate = '{}' '''.format(new_am, new_cat, am, cat, date)

    elif new_date:
        sql_update= '''update expenses set buyingDate = '{}' where amount= '{}' and category = '{}' and 
         buyingDate = '{}' '''.format(new_date, am, cat, date)



    c.execute(sql_update)
    conn.commit()

    c.execute('SELECT * FROM expenses')

    data=c.fetchall()
    print(tabulate(data))

def optionen():
    print('Zugriff zur Tabelle spent.db erfolgreich')

    print('0: Tabelle mit eingetragenen Angaben sehen')
    print('1: Neue Rechnung eingeben')
    print('2: eine bereits eingetragene Angabe löschen')
    print('3: bereits eingetragene Abgaben aktualizieren')
    print('4: Abbildung zeigen:')

if __name__=='__main__':

    #add_colum()
    optionen()
    while True:

        try:
            args= int(input('Option-Zahl eingeben:'))
            break
        except ValueError:
            print('das ist nicht eine gültige Option-zahl!')
            print('Versuche es noch einamal')

    if args == 0:

        print('Um die vollständige Tabelle zu sehen, drücke ENTER. Sonst tippe den Namen der Kategorie ein, '
              'die aufgerufen werden soll:')
        while True:
            try:
                type = str(input())
                break
            except ValueError:
                print('Gebe den Kategorienamme ein')

        tabelle = read_from_db(type)
        print(tabelle)

        print('Verbindung erfolgreich')

    elif args == 1:
        while True:

            try:
                category = str(input("Kategorie des Produkts eingeben: ")).strip()
                amount = float(input("Preise des Produkts eingeben: "))
                message = str(input('weitere Infos: '))
                date_entry = input('Datum im TT.MM.JJJJ format eingeben:')
                #timestamp= str(input("Datum eingeben: "))
                dynamic_data_entry(amount, category, message, date_entry)
                break
            except ValueError as v:
                print(v)
                print('Vesuche es nochmal')
    elif args == 2:

        print('Um die vollständige Tabelle zu sehen, drücke ENTER. Sonst tippe den Namen der Kategorie ein, '
              'die aufgerufen werden soll:')
        while True:
            try:
                type = str(input())
                break
            except ValueError:
                print('Gebe den Kategorienamme ein')

        tabelle = read_from_db(type)
        print(tabelle)

        while True:
            try:
                category = str(input("Kategorie des Produkts eingeben: ")).strip()
                amount = float(input("Preise des Produkts eingeben: "))
                message= str(input('weitere Infos:'))
                date_entry = input('Datum im TT.MM.JJJJ format eingeben:')


                delete(amount, category, message, date_entry)
                break
            except ValueError as v:
                print(v)
                print('Vesuche es nochmal')

    elif args == 3:

        print('Um die vollständige Tabelle zu sehen, drücke ENTER. Sonst tippe den Namen der Kategorie ein, '
              'die aufgerufen werden soll:')
        while True:
            try:
                type = str(input())
                break
            except ValueError:
                print('Gebe den Kategorienamme ein')

        tabelle = read_from_db(type)
        print(tabelle)

        while True:

            print('gebe die Info der zu verändernden Angabe ein')

            try:
                category = str(input('die Kategoriename:')).strip()
                amount = float(input('die Ausgabesumme als Referenz:'))
                date = input('Datum im TT.MM.JJJJ format eingeben:')

            except ValueError as e:
                print(e)

            print('gebe die neue Info der Angabe ein')

            try:
                new_cat = str(input('die neue Kategoriename:')).strip()
                new_am = float(input('die neue Ausgabesumme:'))
                new_date = input('Datum im TT.MM.JJJJ format eingeben:')
                break
            except ValueError as e:
                print(e)

        update_one(amount, category, new_am, new_am )

    elif args==4:

        an='''
        1: Zeitabschnitt eingeben 
        2: Alle Zeitpunkten selektieren '''

        print(an)
        opt=int(input('Option eingeben:'))

        if opt==1:
            while True:
                try:
                    von= input('von:')
                    bis= input('bis:')
                    graph_data(von, bis)
                    break
                except Exception as e:
                    print(e)

        else:
            graph_data()




    #create_table()


    #graph_data()

    #delete()
    c.close()
    conn.close()
