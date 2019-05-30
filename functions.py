'''
Inventory Manager
Nathan Tang
19/05/16
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlalchemy
import os

class itemsClass:
    def __init__(self):
        self.item = None
        self.ID = None
        self.price = int
        self.totAvail = object
        self.totChecked = object
        self.description = str

    def setItem(self, item):
        self.item = item
        return self.item

    def setID(self, ID):
        self.ID = ID
        return self.ID

    def setPrice(self, price):
        self.price = price
        return self.price

    def setTotAvail(self, totAvail):
        self.totAvail = totAvail

    def setTotChecked(self, totChecked):
        self.totChecked = totChecked

    def setDescription(self, description):
        self.description = description

    def getItem(self):
        return self.item
    
    def getID(self):
        return self.ID
    
    def getPrice(self):
        return self.price

    def getTotAvail(self):
        return self.totAvail

    def getTotChecked(self):
        return self.totChecked

    def getDescription(self):
        return self.description

    
class totalAvailable:
    def __init__(self):
        self.totAvail = None

class totalChecked:
    def __init__(self):
        self.totChecked = None

def openFile():
    fil = open(filedialog.askopenfilename(initialdir="/", filetypes=(("CSV", "*.csv"),("Database", "*.db"),("All Files", "*.*"))))
    print(fil)
    return fil

def newFile():
    directory = filedialog.askdirectory()
    return directory

def sort(tree, column, descending): # Allows user to sort the data

    data = [(tree.set(child, column), child) for child in tree.get_children('')] # Places values to sort in data

    data.sort(reverse=descending) # Reorders data
    for index, item in enumerate(data):
        tree.move(item[1], '', index)

    tree.heading(column, command=lambda col=column: sort(tree, column, int(not descending)))



def addMenu(tree, engine, connection, metadata, inventory, query, resultProxy):

    def getItemArgs(*args):
        item = stringvar1.get()
        ID = stringvar2.get()
        price = intVar1.get()
        available = intVar2.get()
        checkedOut = intVar3.get()
        description = stringvar3.get()
        if item and ID and price and available and checkedOut and description:
            ContButton.config(state='normal', command=lambda: ContButtonFunc(item, ID, price, available, checkedOut, description))
            
            # return itemsStr, IDStr, priceStr, availableStr, checkedOutStr, descriptionStr
        else:
            ContButton.config(state='disabled')

    # def ContButtonFunc(itemsStr, IDStr, priceStr, availableStr, checkedOutStr, descriptionStr):
    #     addItemsArray = [itemsStr, IDStr, priceStr, availableStr, checkedOutStr, descriptionStr]
    #     query = sqlalchemy.insert(inventory)
    #     values = [{'Item':addItemsArray[0], 'ID':addItemsArray[1], 'Price':addItemsArray[2], 'Available':addItemsArray[3], 'Checked Out':addItemsArray[4], 'Description':addItemsArray[5]}]
    #     resultProxy = connection.execute(query, values)
    #     results = connection.execute(sqlalchemy.select([inventory])).fetchall()
    #     root.destroy()

    def ContButtonFunc(item, ID, price, available, checkedOut, description):
        # item = items.get()
        # ID = ID.get()
        # price = price.get()
        # available = available.get()
        # checkedOut = checkedOut.get()
        # description = description.get()
        
        newItem = itemsClass()
        newItem.setItem(item)
        newItem.setID(ID)
        newItem.setPrice(price)
        newItem.setTotAvail(available)
        newItem.setTotChecked(checkedOut)
        newItem.setDescription(description)

        # Write to tree
        tree.insert("", len(tree.get_children()), values=(newItem.getItem(), newItem.getID(), newItem.getPrice(), newItem.getTotAvail(), newItem.getTotChecked(), newItem.getDescription()))

        # Write to DB
        query = sqlalchemy.insert(inventory)
        values = [{'Item':newItem.getItem(), 'ID':newItem.getID(), 'Price':newItem.getPrice(), 'Available':newItem.getTotAvail(), 'Checked Out':newItem.getTotChecked(), 'Description':newItem.getDescription()}]
        resultProxy = connection.execute(query, values)
        results = connection.execute(sqlalchemy.select([inventory])).fetchall()
        
        root.destroy()
    
    
    root = tk.Tk()
    root.wm_title('Add A New Item')
    root.focus_force()
    labels=('Item: ', 'ID: ', 'Price: ', 'Available: ', 'Checked Out: ', 'Description: ')
    for i in labels:
        tk.Label(root, text=i, justify=tk.LEFT, anchor='w').grid(row=labels.index(i))

    stringvar1 = tk.StringVar(root)
    stringvar2 = tk.StringVar(root)
    stringvar3 = tk.StringVar(root)
    intVar1 = tk.IntVar(root)
    intVar2 = tk.IntVar(root)
    intVar3 = tk.IntVar(root)

    stringvar1.trace('w', getItemArgs)
    stringvar2.trace('w', getItemArgs)
    stringvar3.trace('w', getItemArgs)
    intVar1.trace('w', getItemArgs)
    intVar2.trace('w', getItemArgs)
    intVar3.trace('w', getItemArgs)

    item = tk.Entry(root, width=40, textvariable=stringvar1)
    ID = tk.Entry(root, width=40, textvariable=stringvar2)
    price = tk.Entry(root, width=40, textvariable=intVar1)
    available = tk.Entry(root, width=40, textvariable=intVar2)
    checkedOut = tk.Entry(root, width=40, textvariable=intVar3)
    description = tk.Entry(root, width=40, textvariable=stringvar3)

    
    # items = tk.Entry(root, width=40)
    # ID = tk.Entry(root, width=40)
    # price = tk.Entry(root, width=40)
    # available = tk.Entry(root, width=40)
    # checkedOut = tk.Entry(root, width=40)
    # description = tk.Entry(root, width=40)

    item.grid(row=0, column=1)
    ID.grid(row=1, column=1)
    price.grid(row=2, column=1)
    available.grid(row=3, column=1)
    checkedOut.grid(row=4, column=1)
    description.grid(row=5, column=1)

    ContButton = tk.Button(root, text='Continue', command=lambda: getItemArgs(item, ID, price, available, checkedOut, description))
    # ContButton = tk.Button(root, text='Continue', command=lambda: ContButtonFunc(items, ID, price, available, checkedOut, description))
    ContButton.grid(row=6, column=1)

    

    root.focus_force()

    root.mainloop()



def printTreeview(tree, resultSet): # Updates the treeview with CSV data

    tree.delete(*tree.get_children()) # Delete tree

    # Writes updated tree
    for i in range(len(resultSet)):
        tree.insert("", i, values=(resultSet[i][0],resultSet[i][1],resultSet[i][2],resultSet[i][3],resultSet[i][4],resultSet[i][5]))