from tkinter import *
from tkinter import messagebox
from logInSession import *
from datetime import date, time, datetime
from db import *
#import ordersSys
#import itemAcquSys
#import storeSys
from sys import exit

def openNewInventoryW(Frame):



    def Orders():
        from ordersSys import OpenNewWindowOrders
        #Frame.iconify()
        win1 = Toplevel(Frame)
        win1.geometry('800x600')
        win1.title('Orders Control')
        Frame.withdraw()
        OpenNewWindowOrders(win1)
        #win1.deiconify()
        return

    def itemAcquired():
        from itemAcquSys import OpenNewWindowItemAcq
        #Frame.iconify()
        win2 = Toplevel(Frame)
        win2.geometry('950x600')
        win2.title('Item Acquired')
        Frame.withdraw()
        OpenNewWindowItemAcq(win2)
        return

    def store():
        from storeSys import OpenNewWindowStore

        now = datetime.now()
        print(date.today())
        print(time(now.hour, now.minute, now.second))

        IDVal = UserDetails.UserID
        print (IDVal)
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO Ticket (UserID, TDate, TTime) VALUES (%s, %s, %s)"
        val = (UserDetails.UserID, date.today(), time(now.hour, now.minute, now.second))
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)


        #Frame.iconify()
        win3 = Toplevel(Frame)
        win3.geometry('800x600')
        win3.title('Store System')
        Frame.withdraw()
        OpenNewWindowStore(win3)
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

    orders_btn = Button(Frame, text='orders', width=15, command=Orders)
    orders_btn.place(x=50, y=50)

    itemAcquired_btn = Button(Frame, text='Items Acquired', width=15, command=itemAcquired)
    itemAcquired_btn.place(x=50, y=100)

    store_btn = Button(Frame, text='Store', width=15, command=store)
    store_btn.place(x=50, y=150)

    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=380, y=250)


    Frame.protocol('WM_DELETE_WINDOW',closure)
    return

if __name__ == "__main__":
    app = Tk()
    app.title('Inventory')
    app.geometry('500x300')

    openNewInventoryW(app)
    app.mainloop()
    

