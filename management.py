from tkinter import *
from tkinter import messagebox
#import user_Dashboard
#import item_Dashboard
#import branch_Dashboard
#import userType_Dashboard
#import payment
#import ItemClassification
#import ItemStatus
from sys import exit

def OpenNewWindowManagement(Frame):


    def paymentW():
        from payment import OpenNewWindowPayment
        #Frame.iconify()
        win1 = Toplevel(Frame)
        win1.geometry('650x350')
        win1.title('payment control')
        Frame.withdraw()
        OpenNewWindowPayment(win1)
        return

    def Users():
        from user_Dashboard import OpenNewWindowUserD
        #Frame.iconify()
        win2 = Toplevel(Frame)
        win2.geometry('850x450')
        win2.title('Users control')
        Frame.withdraw()
        OpenNewWindowUserD(win2)
        return

    def Branch():
        from branch_Dashboard import OpenNewWindowBranchD
        win3 = Toplevel(Frame)
        win3.geometry('700x450')
        win3.title('Branch control')
        Frame.withdraw()
        OpenNewWindowBranchD(win3)
        return

    def Item():
        from item_Dashboard import OpenNewWindowItemD
        win4 = Toplevel(Frame)
        win4.geometry('700x550')
        win4.title('Item control')
        Frame.withdraw()
        OpenNewWindowItemD(win4)
        return

    def itemClassifW():
        from ItemClassification import OpenNewWindowItemClassification
        #Frame.iconify()
        win5 = Toplevel(Frame)
        win5.geometry('650x350')
        win5.title('Item Classification control')
        Frame.withdraw()
        OpenNewWindowItemClassification(win5)
        return

    def itemStatusW():
        from ItemStatus import OpenNewWindowItemStatus
        #Frame.iconify()
        win6 = Toplevel(Frame)
        win6.geometry('650x350')
        win6.title('Item Status control')
        Frame.withdraw()
        OpenNewWindowItemStatus(win6)
        return


    def userType():
        from userType_Dashboard import OpenNewWindowUserTypeD
        win7 = Toplevel(Frame)
        win7.geometry('650x350')
        win7.title('userType control')
        Frame.withdraw()
        OpenNewWindowUserTypeD(win7)
        return

    def backCom():
        from admin_Dashboard import OpenNewWindowAdmnDash

        #Frame.iconify()
        win1 = Toplevel(Frame)
        win1.geometry('900x500')
        win1.title('Administrator')
        Frame.withdraw()
        OpenNewWindowAdmnDash(win1)
        #win1.deiconify()
        return

    def closure():
        exit(0)

    #Buttons


    payment_btn = Button(Frame, text='Payment', width=25, command=paymentW)
    payment_btn.place(x=50, y=50)

    Users_btn = Button(Frame, text='Users', width=25, command=Users)
    Users_btn.place(x=50, y=100)

    Branch_btn = Button(Frame, text='Branch', width=25, command=Branch)
    Branch_btn.place(x=50, y=150)

    Item_btn = Button(Frame, text='Item', width=25, command=Item)
    Item_btn.place(x=50, y=200)

    itemClassif_btn = Button(Frame, text='Item Classification', width=25, command=itemClassifW)
    itemClassif_btn.place(x=50, y=250)

    itemStatus_btn = Button(Frame, text='Item Status', width=25, command=itemStatusW)
    itemStatus_btn.place(x=50, y=300)

    userType_btn = Button(Frame, text='userType', width=25, command=userType)
    userType_btn.place(x=50, y=350)

    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=430, y=400)

    Frame.protocol('WM_DELETE_WINDOW',closure)

    return

if __name__ == "__main__":

    app = Tk()
    app.title('Management')
    app.geometry('550x450')

    OpenNewWindowManagement(app)
    app.mainloop()

