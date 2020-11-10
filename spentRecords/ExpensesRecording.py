import sqlite3
import time
import datetime
import uuid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('ggplot')

from tabulate import tabulate

conn= sqlite3.connect('spent.db')
c=conn.cursor()

def create_table():
    #c.execute('CREATE TABLE IF NOT EXISTS MyExpenses(count REAL, product TEXT, price REAL, datestamp TEXT)')
    c.execute("CREATE TABLE IF NOT EXISTS expenses(amount REAL, category STRING, message STRING, date STRING)")

def dynamic_data_entry(amount, category, message=""):
    id = uuid.uuid4().int & (1<<20)-1

    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y %H:%M:%S')) #('%Y-%m-%d %H:%M:%S')

   # Convert to timestamp
    #date_timestamp = time.mktime(time.strptime(timestamp, "%d/%m/%Y"))

    c.execute("INSERT INTO expenses(amount, category, message, date) VALUES(?,?,?,?)", (amount, category, message, date))
    conn.commit()

def read_from_db(type= None):
    #c.execute("SELECT * FROM expenses")
    #type= str(input('welche Produktkategorie sollte ausgewählt werden:'))

    if type:
        #c.execute("SELECT * FROM expenses WHERE category = 'type' ")
        sql = '''select * from expenses where category = '{}' '''.format(type)
        sql_sum = '''select sum(amount) from expenses where category = '{}' '''.format(type)
    else:
        sql = '''select * from expenses'''.format(type)
        sql_sum = '''select sum(amount) from expenses'''.format(type)

    c.execute(sql)
    #for i in c.fetchall():
    #   print(i)
    tabelle = c.fetchall()

    c.execute(sql_sum)
    summe = c.fetchone()[0]
    print(summe)
    print(80 * '=')
    print(tabulate(tabelle))

    #return summe, tabulate(tabelle)


def graph_data():

    c.execute('SELECT date, amount from expenses')
    dates= []
    amount=[]
    for row in c.fetchall():
        #print(row[0])
        #print(row[1])
        dates.append(row[0])
        amount.append(row[1])
    plt.plot_date(dates, amount, '-')
    plt.show()

def delete(amount, category, message=""):
    #c.execute('SELECT * FROM expenses')
    #[print(row) for row in c.fetchall()]
    #tabelle_vor = c.fetchall()
    #print(tabulate(tabelle_vor))

    if message:

        sql = '''delete from expenses where amount = '{}' and category = '{}' and message = '{}' '''. format(amount, category, message)
    else:

        sql = '''delete from expenses where amount = '{}' and category = '{}' '''.format(amount, category)

    c.execute(sql)
    conn.commit()

    c.execute('SELECT * FROM expenses')
    #[print(row) for row in c.fetchall()]
    tabelle_nach = c.fetchall()
    print(tabulate(tabelle_nach))



def update_one(am, cat, new_am="", new_cat=""):
    #c.execute('SELECT * FROM expenses')
    #[print(row) for row in c.fetchall()]


    if new_am:

        sql_update = '''update expenses set amount = '{}' where amount = '{}' and category = '{}' 
        '''.format(new_am, am, cat)

    elif new_cat:
        sql_update = '''update expenses set category = '{}' where amount = '{}' and category = '{}' 
        '''.format(new_cat, am, cat)



    c.execute(sql_update)
    conn.commit()

    c.execute('SELECT * FROM expenses')
    #[print(row) for row in c.fetchall()]
    data=c.fetchall()
    print(tabulate(data))

#def update_more(am,cat,new_am=):


    #sql = '''update from expenses set amount= '{}' and category= '{}' where amount = '{}' and category = '{}'
       # '''.format(new_am, new_cat, am, cat)

if __name__=='__main__':
    print('Zugriff zur Tabelle spent.db erfolgreich')

    print('0: Tabelle mit eingetragenen Angaben sehen')
    print('1: Neue Rechnung eingeben')
    print('2: eine bereits eingetragene Angabe löschen')
    print('3: bereits eingetragene Abgaben aktualizieren')
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


        #print('Gesamte Ausgabensumme:,', total)
        tabelle = read_from_db(type)
        print(tabelle)

        print('Verbindung erfolgreich')

    elif args == 1:
        while True:

            try:
                category = str(input("Kategorie des Produkts eingeben: ")).strip()
                amount = float(input("Preise des Produkts eingeben: "))
                message = str(input('weitere Infos: '))
                dynamic_data_entry(amount, category, message)
                break
            except ValueError as v:
                print(v)
                print('Vesuche es nochmal')
    elif args==2:

        print('Um die vollständige Tabelle zu sehen, drücke ENTER. Sonst tippe den Namen der Kategorie ein, '
              'die aufgerufen werden soll:')
        while True:
            try:
                type = str(input())
                break
            except ValueError:
                print('Gebe den Kategorienamme ein')

        # print('Gesamte Ausgabensumme:,', total)
        tabelle = read_from_db(type)
        print(tabelle)

        while True:
            try:
                category = str(input("Kategorie des Produkts eingeben: ")).strip()
                amount = float(input("Preise des Produkts eingeben: "))
                #datum = str(input('Datum spesifizieren: '))
                delete(amount, category)
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

        # print('Gesamte Ausgabensumme:,', total)
        tabelle = read_from_db(type)
        print(tabelle)

        while True:

            print('gebe die Info der zu verändernden Angabe ein')

            try:

                amount = float(input('die Ausgabesumme als Referenz:'))
                category = str(input('die Kategoriename:')).strip()
            except ValueError as e:
                print(e)

            print('gebe die neue Info der Angabe ein')

            try:
                new_am = float(input('die neue Ausgabesumme:'))
                new_cat = str(input('die neue Kategoriename:')).strip()
                break
            except ValueError as e:
                print(e)

        update_one(amount, category, new_am, new_am )


    #create_table()


    #graph_data()

    #delete()
    c.close()
    conn.close()
