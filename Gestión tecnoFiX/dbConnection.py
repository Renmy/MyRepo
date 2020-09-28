import sqlite3

class db_Connection:

   def __init__(self, dbname):

        self.connection = sqlite3.connect(dbname)
        self.cur = self.connection.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Products (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CODIGO VARCHAR(10) UNIQUE,
            NOMBRE VARCHAR(50),
            DESCRIPCION VARCHAR(100),
            STOCK INTEGER,
            COST VARCHAR(10),
            PRICE VARCHAR(10)
            )""")

   def close(self):

        self.connection.close()

   def execute(self, sql):

        self.cur.execute(sql)

   def executemany(self, sql, values):

        self.cur.execute(sql, values)

   def commit(self):

        self.connection.commit()