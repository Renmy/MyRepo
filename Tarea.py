import os
import re
import sqlite3


myCon = sqlite3.connect("Tarea.db")
myCursor = myCon.cursor()

targetDir = input('Introduce el directorio a explorar: ')
keyword = input("Introduce el criterio de busqueda: ")

listMatch = []

listFiles = [file for file in os.scandir(targetDir)]

for f in listFiles:
    if re.search(keyword, f.name, re.IGNORECASE) and f.is_file:
        print(f.name, '----', f.path, '----', f.stat(follow_symlinks=False).st_size)
        myCursor.execute("INSERT INTO Archivos VALUES(NULL,?,?,?)", (keyword, f.name, f.path))

myCon.commit()

myCon.close()

#--------Menu APP-----

'''opt = ''  #-----Opcion Elegida------
while opt != 's':
    opt = input('Presione 1 para filtrar por tamaño.\nPresione 2 para filtrar por fecha de modificacion.\nPresione s para salir del Programa.')
    if opt == 1:'''

