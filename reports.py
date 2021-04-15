from tkinter import *
from tkinter import messagebox
import sellsIncome
import itemAnalysis


def OpenNewWindowReports():


    def S_Income():
        app.iconify()
        win1 = Toplevel(app)
        win1.geometry('700x200')
        win1.title('Income Report')
        sellsIncome.OpenNewWindowSells(win1)
        return

    def IAnalysis():
        print('Item Analysis')
        app.iconify()
        win2 = Toplevel(app)
        win2.geometry('700x200')
        win2.title('Item Analysis')
        itemAnalysis.OpenNewWindowIAnalysis(win2)
        return

    def AccountingExpenses():
        print('Another Value')
        #app.iconify()
        #win3 = Toplevel(app)
        #win3.geometry('700x450')
        #win3.title('Branch control')
        #branch_Dashboard.OpenNewWindowBranchD(win3)
        #return
        #Buttons

    app = Tk()
    app.title('Reports Window')
    app.geometry('400x300')

    payment_btn = Button(app, text='Sells Income', width=25, command=S_Income)
    payment_btn.place(x=50, y=50)

    Users_btn = Button(app, text='Item Analysis', width=25, command=IAnalysis)
    Users_btn.place(x=50, y=100)

    Branch_btn = Button(app, text='Expenses', width=25, command=AccountingExpenses)
    Branch_btn.place(x=50, y=150)



    app.mainloop()

if __name__ == "__main__":
    OpenNewWindowReports()



