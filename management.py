from tkinter import *
from tkinter import messagebox
import user_Dashboard
import item_Dashboard
import branch_Dashboard
import userType_Dashboard
import payment
import ItemClassification
import ItemStatus

def OpenNewWindowManagement():


    def paymentW():
        app.iconify()
        win1 = Toplevel(app)
        win1.geometry('650x350')
        win1.title('payment control')
        payment.OpenNewWindowPayment(win1)
        return

    def Users():
        app.iconify()
        win2 = Toplevel(app)
        win2.geometry('850x450')
        win2.title('Users control')
        user_Dashboard.OpenNewWindowUserD(win2)
        return

    def Branch():
        app.iconify()
        win3 = Toplevel(app)
        win3.geometry('700x450')
        win3.title('Branch control')
        branch_Dashboard.OpenNewWindowBranchD(win3)
        return

    def Item():
        app.iconify()
        win4 = Toplevel(app)
        win4.geometry('850x450')
        win4.title('Item control')
        item_Dashboard.OpenNewWindowItemD(win4)
        return

    def itemClassifW():
        app.iconify()
        win5 = Toplevel(app)
        win5.geometry('650x350')
        win5.title('Item Classification control')
        ItemClassification.OpenNewWindowItemClassification(win5)
        return

    def itemStatusW():
        app.iconify()
        win6 = Toplevel(app)
        win6.geometry('650x350')
        win6.title('Item Status control')
        ItemStatus.OpenNewWindowItemStatus(win6)
        return


    def userType():
        app.iconify()
        win7 = Toplevel(app)
        win7.geometry('650x350')
        win7.title('userType control')
        userType_Dashboard.OpenNewWindowUserTypeD(win7)
        return


        #Buttons

    app = Tk()
    app.title('Management')
    app.geometry('550x450')

    payment_btn = Button(app, text='Payment', width=25, command=paymentW)
    payment_btn.place(x=50, y=50)

    Users_btn = Button(app, text='Users', width=25, command=Users)
    Users_btn.place(x=50, y=100)

    Branch_btn = Button(app, text='Branch', width=25, command=Branch)
    Branch_btn.place(x=50, y=150)

    Item_btn = Button(app, text='Item', width=25, command=Item)
    Item_btn.place(x=50, y=200)

    itemClassif_btn = Button(app, text='Item Classification', width=25, command=itemClassifW)
    itemClassif_btn.place(x=50, y=250)

    itemStatus_btn = Button(app, text='Item Status', width=25, command=itemStatusW)
    itemStatus_btn.place(x=50, y=300)

    userType_btn = Button(app, text='userType', width=25, command=userType)
    userType_btn.place(x=50, y=350)

    app.mainloop()

if __name__ == "__main__":
    OpenNewWindowManagement()

