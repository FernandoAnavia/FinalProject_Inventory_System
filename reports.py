from tkinter import *
from tkinter import messagebox
#import sellsIncome
#import itemAnalysis
from sys import exit

def OpenNewWindowReports(Frame):


    def S_Income():
        from sellsIncome import OpenNewWindowSells
        win1 = Toplevel(Frame)
        win1.geometry('700x200')
        win1.title('Income Report')
        Frame.withdraw()
        OpenNewWindowSells(win1)
        return

    def IAnalysis():
        from itemAnalysis import OpenNewWindowIAnalysis
        win2 = Toplevel(Frame)
        win2.geometry('700x200')
        win2.title('Item Analysis')
        Frame.withdraw()
        OpenNewWindowIAnalysis(win2)
        return

    def AccountingExpenses():
        from Expenses import OpenNewWindowExpenses
        win3 = Toplevel(Frame)
        win3.geometry('700x200')
        win3.title('Expenses Report')
        OpenNewWindowExpenses(win3)
        return

    def backCom():
        from admin_Dashboard import OpenNewWindowAdmnDash

        #Frame.iconify()
        win1 = Toplevel(Frame)
        win1.geometry('800x400')
        win1.title('Administrator')
        Frame.withdraw()
        OpenNewWindowAdmnDash(win1)
        #win1.deiconify()
        return

    def closure():
        exit(0)

    #        Buttons

    payment_btn = Button(Frame, text='Sells Income', width=25, command=S_Income)
    payment_btn.place(x=50, y=50)

    Users_btn = Button(Frame, text='Item Analysis', width=25, command=IAnalysis)
    Users_btn.place(x=50, y=100)

    Branch_btn = Button(Frame, text='Expenses', width=25, command=AccountingExpenses)
    Branch_btn.place(x=50, y=150)

    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=280, y=250)


    Frame.protocol('WM_DELETE_WINDOW',closure)
    return

if __name__ == "__main__":

    app = Tk()
    app.title('Reports Window')
    app.geometry('400x300')

    OpenNewWindowReports(app)
    app.mainloop()



