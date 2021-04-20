from tkinter import *
from tkinter import messagebox
#from management import OpenNewWindowManagement
#from inventory import openNewInventoryW
#from reports import OpenNewWindowReports
from sys import exit



def OpenNewWindowAdmnDash(Frame):


    def Data_Management():

        from management import OpenNewWindowManagement
        win0 = Toplevel(Frame)
        win0.geometry('550x450')
        win0.title('Management')
        Frame.withdraw()
        OpenNewWindowManagement(win0)
        return
        

    def Inventory():

        from inventory import openNewInventoryW
        #Frame.iconify()
        win1 = Toplevel(Frame)
        win1.geometry('500x300')
        win1.title('Inventory')
        Frame.withdraw()
        openNewInventoryW(win1)
        #win1.deiconify()
        return


    def Reports():
        
        from reports import OpenNewWindowReports
        win3 = Toplevel(Frame)
        win3.geometry('400x300')
        win3.title('Reports Window')
        Frame.withdraw()
        OpenNewWindowReports(win3)
        #win1.deiconify()
        return


    def Settings():
        print("Settings")

    def closure():
        exit(0)
        


    #Buttons

    #shop_btn = Button(Frame, text='Shop', width=15, command=shop)
    #shop_btn.place(x=150, y=50)

    Data_Manag_btn = Button(Frame, text='Data Management', width=15, command=Data_Management)
    Data_Manag_btn.place(x=150, y=50)

    Inventory_btn = Button(Frame, text='Inventory', width=15, command=Inventory)
    Inventory_btn.place(x=150, y=100)

    #Accounting_btn = Button(Frame, text='Accounting', width=15, command=Accounting)
    #Accounting_btn.place(x=150, y=200)

    Reports_btn = Button(Frame, text='Reports', width=15, command=Reports)
    Reports_btn.place(x=150, y=150)

    Settings_btn = Button(Frame, text='Settings', width=15, command=Settings)
    Settings_btn.place(x=150, y=200)


    Frame.protocol('WM_DELETE_WINDOW',closure)

    return
    

if __name__ == "__main__":
    

    app = Tk()
    app.title('Administrator')
    app.geometry('500x400')
    

    OpenNewWindowAdmnDash(app)
    app.mainloop()