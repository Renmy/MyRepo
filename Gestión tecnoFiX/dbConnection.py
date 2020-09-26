import sqlite3

class db_Connection:

   def __init__(self, dbname):
        """Initialize db class variables"""
        self.connection = sqlite3.connect(dbname)
        self.cur = self.connection.cursor()

   def close(self):
        """close sqlite3 connection"""
        self.connection.close()

   def execute(self, sql):
        """execute a row of data to current cursor"""
        self.cur.execute(sql)

   def executemany(self, sql, values):
        """execute a row of data to current cursor"""
        self.cur.execute(sql, values)

   def create_table(self):
        """create a database table if it does not exist already"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS ARCHIVOS''')

   def commit(self):
        """commit changes to database"""
        self.connection.commit()