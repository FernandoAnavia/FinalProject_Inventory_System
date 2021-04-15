from tkinter import *
from tkinter import messagebox
from logInSession import *
from datetime import date, time, datetime
from db import *
import ordersSys
import itemAcquSys
import storeSys


def openNewInventoryW():



    def Orders():

        app.iconify()
        win1 = Toplevel(app)
        win1.geometry('800x600')
        win1.title('Orders Control')
        ordersSys.OpenNewWindowOrders(win1)
        return

    def itemAcquired():

        app.iconify()
        win2 = Toplevel(app)
        win2.geometry('950x600')
        win2.title('Item Acquired')
        itemAcquSys.OpenNewWindowItemAcq(win2)
        return

    def store():
        print("store")

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


        app.iconify()
        win3 = Toplevel(app)
        win3.geometry('800x600')
        win3.title('Store System')
        storeSys.OpenNewWindowStore(win3)
        return



    app = Tk()
    app.title('Inventory')
    app.geometry('500x300')

    #Buttons

    orders_btn = Button(app, text='orders', width=15, command=Orders)
    orders_btn.place(x=50, y=50)

    itemAcquired_btn = Button(app, text='Items Acquired', width=15, command=itemAcquired)
    itemAcquired_btn.place(x=50, y=100)

    store_btn = Button(app, text='Store', width=15, command=store)
    store_btn.place(x=50, y=150)


    app.mainloop()

if __name__ == "__main__":
    openNewInventoryW()

