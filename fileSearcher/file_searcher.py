import os
import dbConnection
import datetime as dt
import re


class File_Searcher:

    def __init__(self):
        self.matches = 0
        self.indexes = []
        self.results = []
        self.total_records = 0
        self.db = dbConnection.db_Connection("Tarea.db")

    def new_index(self, target_dir):
        '''create new index if not exist in DB'''
        listfiles = [files for files in os.scandir(target_dir)]
        for d in listfiles:
            creation_date = dt.datetime.today().fromtimestamp(d.stat(follow_symlinks=False).st_ctime)
            self.db.executemany("INSERT INTO Archivos VALUES(NULL,?,?,?,?,?)", (
            target_dir, d.name, d.path, d.stat(follow_symlinks=False).st_size,
            creation_date.isoformat(timespec='seconds')))
        self.db.commit()

    def load_index(self, target_dir):
        '''load index from db from previews search'''
        '''this format param avoid error with colons in sql querry'''
        sql = "SELECT * FROM ARCHIVOS WHERE target_dir={}".format(target_dir.__repr__())
        self.db.execute(sql)
        self.indexes = self.db.cur.fetchall()


    def search_files(self, keyword, target_dir):
        '''search files from keyword and path'''
        '''reset all variables for new search'''
        self.matches = 0
        self.total_records = 0
        self.indexes.clear()
        self.results.clear()

        '''lookup for path's previews searches. if not create new index with target_dir and read again'''
        self.load_index(target_dir)
        if not self.indexes:
            self.new_index(target_dir)
        self.load_index(target_dir)
        self.total_records = len(self.indexes)

        '''this code search match with keyword in indexes'''

        for file in self.indexes:
            if re.search(keyword, file[2], re.IGNORECASE):
                self.results.append(file)
                self.matches += 1


fs = File_Searcher()
fs.search_files('tarea', 'C:/Users/Viktor/Documents/')
print("Se encontraron {} coincidencias en {} archivos escaneados:".format(fs.matches, fs.total_records))
for i in fs.results:
    print(i[2], '---',  i[3], '---', i[4], '---', i[5])

