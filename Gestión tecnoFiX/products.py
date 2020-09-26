import dbConnection
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk


db = dbConnection.db_Connection('tecnofix.db')
class Product:

    def __init__(self, code, name, desc, stock, cost, price):
        self.code = code
        self.name = name
        self.desc = desc
        self.stock = stock
        self.cost = cost
        self.price = price



def AddProduct(prod):
    try:
        sql = 'INSERT INTO PRODUCTS VALUES(NULL,?,?,?,?,?,?)'
        db.executemany(sql, (prod.code, prod.name, prod.desc, prod.stock, float(prod.cost), float(prod.price)))
        messagebox.showinfo("Exito", "Producto Insertado correctamente.")
        code.set("")
        name.set("")
        stock.set("")
        cost.set("")
        price.set("")
        sctext.delete(1.0, END)
        db.commit()
    except:
        messagebox.showerror("Error", "Rellene todos los Campos.")

def Exit():
    response = messagebox.askquestion("Salir", "Seguro desea salir.")
    if response == 'yes':
        root.destroy()

def FillTreeProducts():
    table.delete(*table.get_children())
    sql = 'SELECT * FROM PRODUCTS'
    db.execute(sql)
    db_rows = db.cur.fetchall()
    for prod in db_rows:
        table.insert('', 'end', text=prod[0], values=prod[1:7])



root = Tk()
root.title("Productos")

code = StringVar()
name = StringVar()
stock = StringVar()
cost = StringVar()
price = StringVar()


#-------Products Form----------
mainFrame = LabelFrame(root, width=400, height=650, text="Gestionar Productos: ")
mainFrame.pack()

Label(mainFrame, text="Código:").grid(row=0, column=0, padx=4, pady=4, sticky="e")
codEntry = Entry(mainFrame, textvariable=code)
codEntry.focus()
codEntry.grid(row=0, column=1, padx=4, pady=4)

Label(mainFrame, text="Nombre:").grid(row=1, column=0, padx=4, pady=4, sticky="e")
nameEntry = Entry(mainFrame, textvariable=name).grid(row=1, column=1, padx=4, pady=4)

Label(mainFrame, text="Cantidad:").grid(row=2, column=0, padx=4, pady=4, sticky="e")
stockEntry = Entry(mainFrame, textvariable=stock).grid(row=2, column=1, padx=4, pady=4)

Label(mainFrame, text="Costo:").grid(row=3, column=0, padx=4, pady=4, sticky="e")
costEntry = Entry(mainFrame, textvariable=cost).grid(row=3, column=1, padx=10, pady=10)

Label(mainFrame, text="Precio:").grid(row=4, column=0, padx=4, pady=4, sticky="e")
priceEntry = Entry(mainFrame, textvariable=price).grid(row=4, column=1, padx=10, pady=10)

Label(mainFrame, text="Descripción:").grid(row=0, column=2, padx=4, pady=4, sticky="e")
sctext = scrolledtext.ScrolledText(mainFrame)
sctext.config(width=20, height=7)
sctext.grid(row=0, column=3, padx=10, pady=4, sticky='nsew', rowspan=5)

#-----------Buttons----------
btnAdd = Button(mainFrame, width=10, text='Agregar', command=lambda: AddProduct(prod=Product(code.get(), name.get(), sctext.get(1.0, END), stock.get(), cost.get(), price.get())))
btnAdd.grid(row=6, column=1, padx=20, pady=15, sticky='n')
btnCancel = Button(mainFrame, width=10, text='Salir', command=lambda: Exit())
btnCancel.grid(row=6, column=3, padx=20, pady=15, sticky='n')

tableFrame = Frame(root)
tableFrame.pack()
table = ttk.Treeview(tableFrame, height=10, columns=('code', 'name', 'desc', 'stock', 'cost', 'price'))
table.grid(row=7, column=0, columnspan=4, padx=10, pady=10)
table.heading('#0', text='ID', anchor='center')
table.column("#0", minwidth=10, width=30, stretch=NO)
table.heading('code', text='Código', anchor='center')
table.column("code", minwidth=10, width=100, stretch=NO)
table.heading('name', text='Producto', anchor='center')
table.column("name", minwidth=10, width=100, stretch=NO)
table.heading('desc', text='Descripción', anchor='center')
table.column("desc", minwidth=10, width=200, stretch=NO)
table.heading('stock', text='Stock', anchor='center')
table.column("stock", minwidth=10, width=50, stretch=NO)
table.heading('cost', text='Costo', anchor='center')
table.column("cost", minwidth=10, width=50, stretch=NO)
table.heading('price', text='Precio', anchor='center')
table.column("price", minwidth=10, width=50, stretch=NO)

scroll = ttk.Scrollbar(tableFrame, orient="vertical", command=table.yview)
scroll.grid(row=7, column=5, sticky='nswe', pady=4)
#scroll.grid(side = 'right', fill = 'y')
table.configure(yscrollcommand=scroll.set)


FillTreeProducts()




root.mainloop()