from tkinter import *
from tkinter import messagebox
from management import OpenNewWindowManagement
from inventory import openNewInventoryW




def OpenNewWindowAdmnDash():


    def Data_Management():
        app.destroy()
        OpenNewWindowManagement()
        

    def Inventory():
        app.destroy()
        openNewInventoryW()


    def Reports():
        print("Reports")

    def Settings():
        print("Settings")

    app = Tk()
    app.title('Administrator')
    app.geometry('500x400')

    #Buttons

    #shop_btn = Button(app, text='Shop', width=15, command=shop)
    #shop_btn.place(x=150, y=50)

    Data_Manag_btn = Button(app, text='Data Management', width=15, command=Data_Management)
    Data_Manag_btn.place(x=150, y=50)

    Inventory_btn = Button(app, text='Inventory', width=15, command=Inventory)
    Inventory_btn.place(x=150, y=100)

    #Accounting_btn = Button(app, text='Accounting', width=15, command=Accounting)
    #Accounting_btn.place(x=150, y=200)

    Reports_btn = Button(app, text='Reports', width=15, command=Reports)
    Reports_btn.place(x=150, y=150)

    Settings_btn = Button(app, text='Settings', width=15, command=Settings)
    Settings_btn.place(x=150, y=200)

    app.mainloop()

if __name__ == "__main__":
    OpenNewWindowAdmnDash()