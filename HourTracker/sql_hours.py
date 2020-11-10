import sqlite3
import time
import datetime
import os
import pandas as pd
from get_time import fechas as Date
from typing import List, Dict, Tuple, TypeVar
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#from matplotlib import style
#style.use('ggplot')
from tabulate import tabulate


class CreateDataBank:

    def __init__(self, csv_file:str, db_file:str, table_name:str ):
        #self.start:str = start
        #self.end: str = end
        #self.period:list = von_bis
        BASE_DIR: os.path = os.path.dirname(os.path.abspath(__file__))
        self.CSV_PATH: os.path = os.path.join(BASE_DIR, csv_file)
        self.DB_PATH: os.path = os.path.join(BASE_DIR, db_file)
        self.table: str = table_name
        if not os.path.exists(self.DB_PATH):
            self._insert_values_to_table()


    def _connect_to_db(self):
        """
        Connect to an SQlite database, if db file does not exist it will be created
        :param db_file: absolute or relative path of db file
        :return: sqlite3 connection
        """
        sqlite3_conn = None

        try:
            sqlite3_conn: sqlite3.Connection = sqlite3.connect(self.DB_PATH)
            return sqlite3_conn

        except Exception as err:
            print(err)

            if sqlite3_conn is not None:
                sqlite3_conn.close()

    def _get_column_names_from_db_table(self, sql_cursor) -> list:
        """
        Scrape the column names from a database table to a list
        :param sql_cursor: sqlite cursor
        :param table: table name to get the column names from
        :return: a list with table column names
        """
        table_column_names:str = 'PRAGMA table_info(' + self.table + ');'
        sql_cursor.execute(table_column_names)
        table_column_names: sqlite3.Cursor = sql_cursor.fetchall()

        column_names = list()

        for name in table_column_names:
            column_names.append(name[1])

        return column_names

    def _insert_values_to_table(self):
        """
        Open a csv file with pandas, store its content in a pandas data frame, change the data frame headers to the table
        column names and insert the data to the table
        :param table_name: table name in the database to insert the data into
        :param xl_file: path of the xl file to process
        :return: None
        """
        conn: sqlite3 = self._connect_to_db()
        if conn is not None:
            c:sqlite3.Cursor = conn.cursor()

            # Create table if it is not exist
            c.execute('CREATE TABLE IF NOT EXISTS ' + self.table +
                      '(Datum       VARCHAR,'
                      'Beginn       STRING,'
                      'Ende         STRING,'
                      'Pause        STRING,'
                      'Total        STRING,'
                      'Fehlende Stunden STRING,'
                      'Überstunde   STRING,'
                      'Entgeld      DECIMAL)')
            try:
                df:pd.Union = pd.read_excel(self.CSV_PATH)
            except Exception as e:
                print(e)
                try:
                    df:pd.read_csv = pd.read_csv(self.CSV_PATH)
                except Exception as e:
                    print(e)

            df.columns = self._get_column_names_from_db_table(c)
            df.to_sql(name=self.table, con=conn, if_exists='append', index=False)
            conn.close()
            print('SQL insert process finished')
        else:
            print('Connection to database failed')



class manage_databank(CreateDataBank):
    A = TypeVar("A", str, list)
    def __init__(self, csv_file, db_file, table_name, period: List = None) -> None: # period= [col_name, start, end]
        super().__init__(csv_file, db_file, table_name)
        self.period: List[str,...] = period # Beginn, 08:10:00
        self.totalhours:str = " "
        self._read_from_db()
        self.tabell: List = self.get_table()

    def __repr__(self) -> tabulate:
        output: list = [list(x) for x in self.tabelle]
        return tabulate(output, headers="firstrow", tablefmt="github")

    def get_table(self) -> List:
        conn: sqlite3.Connection = self._connect_to_db()
        try:
            if conn is not None:
                c: sqlite3.Cursor = conn.cursor()
        except Exception as e:
            print(e)
        sql: str = '''select * from {}'''.format(self.table)

        c.execute(sql)
        names: tuple = tuple(map(lambda x: x[0], c.description))
        output:list = c.fetchall()
        output.insert(0, names)
        return output

    # @staticmethod
    # def convert_date(from_date:str) -> str: # %B %d, %Y
    #     datum: str = datetime.datetime.strptime(from_date, '%B %d,%Y').strftime('%Y-%d-%m')
    #     return datum
    @staticmethod
    def _sumup_time(totalcol:List)->str:
        #totalcol = [item for tuples in totalcol for item in tuples]
        #print(totalcol)
        totalSecs = 0
        for tuple in totalcol:
            for tm in tuple:
                timeParts:list = [int(s) for s in tm.split(':')]
                totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        #print("%d:%02d:%02d" % (hr, min, sec))
        return "%d:%02d:%02d" % (hr, min, sec)

    def show_entry(self, info:Date, curr_time: Date = Date.get_date()) -> Tuple:
        self._dynamic_data_entry(info, curr_time)
        return self._read_from_db()

    def _dynamic_data_entry(self, info:Date, curr_date: Date) -> None:
        info: str = str(info)
        period:list = info.split(",")

        # self.cursor.execute("INSERT INTO expenses(amount, category, message, date) VALUES(?,?,?,?)", (amount, category, message, date))
        conn: sqlite3.Connection = super(manage_databank, self)._connect_to_db()
        try:
            if conn is not None:
                c: sqlite3.Cursor = conn.cursor()
        except Exception as e:
            print(e)

        if (period[0]=="Beginn"):
            sql_start:str = """ INSERT INTO {} (Datum,Beginn, Ende, Pause, Total, Fehlende, Überstunde, Entgeld ) VALUES(?,?,?,?,?,?,?,?)""".format(self.table)
            c.execute(sql_start, (curr_date, period[1], '00:00:00', '00:00:00', '00:00:00', '00:00:00', '00:00:00', "0")  )
        elif(period[0] == "Ende"):
            sql_end:str= """ insert into {} (Beginn, Ende, Pause, Total, Fehlende, Überstunde, Entgeld ) VALUES(?,?,?,?,?,?,?)""".format(self.table)
            c.execute(sql_end, (curr_date, '00:00:00', period[1], '00:00:00', '00:00:00', '00:00:00', '00:00:00', "0")  )
        conn.commit()

    def _read_from_db(self):
        # c.execute("SELECT * FROM expenses")
        # type= str(input('welche Produktkategorie sollte ausgewählt werden:'))
        conn: sqlite3.Connection = super(manage_databank, self)._connect_to_db()
        try:
            if conn is not None:
                c: sqlite3.Cursor = conn.cursor()
        except Exception as e:
            print(e)
        if self.period == None:
            sql: str = '''select * from '{}' '''.format(self.table)
            sql_sum: str = """select Total from '{}' where Total """.format(self.table)
        elif self.period[0]=="Datum":
            # c.execute("SELECT * FROM expenses WHERE category = 'type' ")
            sql:str = '''select Datum, Beginn, Ende, Pause, Total from '{}' where Datum between '{}' and '{}' '''.format(self.table, self.period[1], self.period[2])
            sql_sum:str = """select Total from '{}' where Total """.format(self.table)
        elif self.period[0]=="Beginn":
            sql:str = '''select Datum, Beginn, Ende, Pause, Total from '{}' where Beginn => '{}' and Beginn <='{}' '''.format(self.table, self.period[1], self.period[2])
            sql_sum: str = """select Total from '{}' where Total """.format(self.table)
        elif self.period[0]== "Ende":
            sql:str = """select Datum, Beginn, Ende, Pause, Total from '{}' where Ende => '{}' and Ende <= '{}' """.format(self.table, self.period[1], self.period[2])
            sql_sum: str = """select Total from '{}' where Total """.format(self.table)
        #tabelle
        c.execute(sql)
        # for i in c.fetchall():
        #   print(i)
        self.tabelle = c.fetchall()
        #summe
        c.execute(sql_sum)
        total:list = c.fetchall()
        summe = self._sumup_time(total)

        return summe, self.tabelle
    @classmethod
    def update_tabelle(cls, table: str, task:list) -> None:
        #def update_task(conn, task):
        """
        update priority, begin_date, and end date of a task :param conn, param task, return: project id
        """
        conn: sqlite3.Connection = cls._connect_to_db()
        try:
            if conn is not None:
                c: sqlite3.Cursor = conn.cursor()
        except Exception as e:
            print(e)

        if task[0] == "Beginn":
            sql = ''' UPDATE '{}' SET Beginn = '{}' WHERE Datum= '{}' '''.format(table, task[1], task[0])
        elif task[1] == "Ende":
            sql:str = ''' UPDATE '{}' SET Ende = '{}' WHERE Datum= '{}' '''.format(table, task[1], task[0])

        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()


def create_table(db_path) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.connect = conn.cursor()
    # c.execute('CREATE TABLE IF NOT EXISTS MyExpenses(count REAL, product TEXT, price REAL, datestamp TEXT)')
    sql: str = """CREATE TABLE IF NOT EXISTS stundenzettel (
                Datum VARCHAR, Beginn STRING, Ende STRING, Pause STRING, Total STRING,
                 fehlende Stunde STRING, Überstunden STRING, Entgelt DECIMAL)"""

    cursor.execute(sql)
    conn.commit()

if __name__ == "__main__":
    filename:str = "worktracker.db"
    BASE_DIR: os.path = os.path.dirname(os.path.abspath(__file__))
    db_path: os.path = os.path.join(BASE_DIR, filename)
    # if not os.path.exists(db_path):
    #     create_table(filename)
    #     filename = filename
    hours: Date = Date(1)
    time:Date = Date.get_hours()
    print(hours)
    #sz: CreateDataBank = CreateDataBank("okt.csv", filename, "stundenzettel")
    period: list = ["Datum","September 19, 2020", "September 25, 2020"]
    manager: manage_databank= manage_databank("okt.csv", filename, "stundenzettel")
    print(manager)
    #print(manager.show_entry(hours))

