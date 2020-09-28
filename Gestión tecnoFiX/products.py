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



def AddProduct():
    if validate_entries():
        prod = Product(code.get(), name.get(), sctext.get(1.0, END), stock.get(), "{:.2f}".format(float(cost.get())),
                       "{:.2f}".format(float(price.get())))
        sql = 'INSERT INTO PRODUCTS VALUES(NULL,?,?,?,?,?,?)'
        db.executemany(sql, (prod.code, prod.name, prod.desc, prod.stock, prod.cost, prod.price))
        FillTreeProducts()
        messagebox.showinfo("Exito", "Producto Insertado correctamente.")
        clean_entries()
        db.commit()
    else:
        messagebox.showerror("Error", "Rellene todos los Campos.")

def clean_entries():
    code.set("")
    name.set("")
    stock.set("")
    cost.set("")
    price.set("")
    sctext.delete(1.0, END)

def on_validate_int(P):
    '''validate if key pressed is correct for currencies'''
    if all(c in "0123456789." for c in P):
        return True
    return False

def validate_entries():
    for ent in mainFrame.children.items():
        if isinstance(ent, Entry):
            if ent.isspace() or len(ent.get() < 1):
                return FALSE
    return True




def Exit():
    response = messagebox.askquestion("Salir", "Seguro desea salir.")
    if response == 'yes':
        root.destroy()
        db.close()

def FillTreeProducts():
    table.delete(*table.get_children())
    for prod in db.cur.execute('SELECT * FROM PRODUCTS').fetchall():
        if prod[0] % 2 == 0:
            table.insert('', 'end', prod[0], text=prod[0], values=prod[1:7])
            table.item(prod[0], tag='evenrow')
        else:
            table.insert('', 'end', prod[0], text=prod[0], values=prod[1:7])
            table.item(prod[0], tag='oddrow')
    table.tag_configure('evenrow', background='white', foreground='black')
    table.tag_configure('oddrow', background='black', foreground='white')

def on_double_click(event):
    item_id = event.widget.focus()
    item = event.widget.item(item_id)
    values = item['values']
    code.set(values[0])
    name.set(values[1])
    sctext.delete(1.0, END)
    sctext.insert(1.0, values[2])
    stock.set(values[3])
    cost.set(values[4])
    price.set(values[5])

def Save_Product():
    if validate_entries():
        ask = messagebox.askquestion("Editar", "Desea Editar el Producto con los Siguientes Datos?")
        if ask == 'yes':
            sql = 'UPDATE PRODUCTS SET codigo=?, nombre=?, descripcion=?, stock=?, cost=?, price=? where codigo={}'.format(code.get())
            values = (code.get(), name.get(), sctext.get(1.0, END), stock.get(), "{:.2f}".format(float(cost.get())), "{:.2f}".format(float(price.get())))
            db.executemany(sql, values)
            db.commit()
            FillTreeProducts()
            clean_entries()
        else:
            pass
    else:
        messagebox.showerror("Error", "Rellene todos los Campos.")




root = Tk()
root.title("Gestionar Productos")
validate_integer = (root.register(on_validate_int), '%P')
code = StringVar()
name = StringVar()
stock = StringVar()
cost = StringVar()
price = StringVar()


#-------Products Form----------
mainFrame = LabelFrame(root, width=400, height=650, text="Datos de Producto: ")
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
costEntry = Entry(mainFrame, textvariable=cost, validate='key', validatecommand=validate_integer).grid(row=3, column=1, padx=10, pady=10)

Label(mainFrame, text="Precio:").grid(row=4, column=0, padx=4, pady=4, sticky="e")
priceEntry = Entry(mainFrame, textvariable=price, validate='key', validatecommand=validate_integer).grid(row=4, column=1, padx=10, pady=10)

Label(mainFrame, text="Descripción:").grid(row=0, column=2, padx=4, pady=4, sticky="e")
sctext = scrolledtext.ScrolledText(mainFrame)
sctext.config(width=20, height=7)
sctext.grid(row=0, column=3, padx=10, pady=4, sticky='nsew', rowspan=5)

#-----------Buttons----------
btnAdd = Button(mainFrame, width=10, text='Agregar', command=lambda: AddProduct())
btnAdd.grid(row=6, column=0, padx=10, pady=10, sticky='w')
btnEdit = Button(mainFrame, width=10, text='Guardar', command=lambda: Save_Product())
btnEdit.grid(row=6, column=1, padx=10, pady=10, sticky='e')
btnDelete = Button(mainFrame, width=10, text='Borrar')
btnDelete.grid(row=6, column=3, padx=10, pady=10, sticky='w')
btnCancel = Button(mainFrame, width=10, text='Salir', command=lambda: Exit())
btnCancel.grid(row=6, column=3, padx=10, pady=10, sticky='e')


tableFrame = Frame(root)
tableFrame.config(padx=10, pady=10)
tableFrame.pack()
table = ttk.Treeview(tableFrame, height=10, columns=('code', 'name', 'desc', 'stock', 'cost', 'price'), selectmode='browse')
table.bind("<Double-Button-1>", on_double_click)
table.grid(row=7, column=0, columnspan=4)
table.heading('#0', text='ID', anchor='center')
table.column("#0", minwidth=10, width=30, stretch=NO, anchor='w')
table.heading('code', text='Código', anchor='center')
table.column("code", minwidth=10, width=100, stretch=NO, anchor='center')
table.heading('name', text='Producto', anchor='center')
table.column("name", minwidth=10, width=100, stretch=NO, anchor='center')
table.heading('desc', text='Descripción', anchor='center')
table.column("desc", minwidth=10, width=200, stretch=NO, anchor='center')
table.heading('stock', text='Stock', anchor='center')
table.column("stock", minwidth=10, width=50, stretch=NO, anchor='center')
table.heading('cost', text='Costo', anchor='center')
table.column("cost", minwidth=10, width=50, stretch=NO, anchor='center')
table.heading('price', text='Precio', anchor='center')
table.column("price", minwidth=10, width=50, stretch=NO, anchor='center')

scroll = ttk.Scrollbar(tableFrame, orient="vertical", command=table.yview)
scroll.grid(row=7, column=5, sticky='nswe', pady=4)
#scroll.grid(side = 'right', fill = 'y')
table.configure(yscrollcommand=scroll.set)


FillTreeProducts()




root.mainloop()