from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from db import *
import re
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
        from settings import OpenNewWindiwSettings
        win3 = Toplevel(Frame)
        win3.geometry('700x550')
        win3.title('Settings')
        Frame.withdraw()
        OpenNewWindiwSettings(win3)
        #win1.deiconify()
        return

    def fillAlerts():

        cursor = mydb.cursor()
        cursor2 = mydb.cursor()

        sql = "select val from SingleVal"
        cursor.execute(sql)
        lowSv = cursor.fetchone()
        print(lowSv[0])

        sql = "Select ItemID, Product, RealStock from (with data as (Select ItemId, substring(IName,1,20) as Product, instock, sold from Item inner join (select ItemId, sum(quantity) as InStock from Itemacquired group by ItemId) a using (ItemID) inner join (select ItemId, sum(quantity) as Sold from Itemoutput group by ItemId) b using (ItemID)) select ItemID, Product, (InStock - Sold) as RealStock from data) x where RealStock < %s order by REalStock"
        cursor.execute(sql,(lowSv[0],))

        treeLowStock.delete(*treeLowStock.get_children())

        for rec in cursor:
            treeLowStock.insert('','end',value=rec)


        sql = "select ItemId from Item"
        cursor.execute(sql)
        ItemIds = cursor.fetchall()
      

        n = -1

        treeExpiry.delete(*treeExpiry.get_children())

        for row in ItemIds:
            n = n+1
            sql = "with data as (Select ItemId, instock, sold from Item inner join (select ItemId, sum(quantity) as InStock from Itemacquired group by ItemId) a using (ItemID) inner join (select ItemId, sum(quantity) as Sold from Itemoutput where ItemId = %s group by ItemId) b using (ItemID)) select ItemId, if((Instock - Sold)<0,InStock-1,Sold) as RealStock from data"
            cursor.execute(sql,ItemIds[n])
            realStock = cursor.fetchone()
            x=0

            for row in realStock:

                if x==0:
                    x=x+1
                    sql = "select a.ItemID, i.IName, min(a.ExpDate) as nextExpDate, datediff((min(a.ExpDate)),(curdate())) as daysLeft, i.ExpDateVal, ((a.cumulative_sum)- %s) as nextExpAmount from (with data as (select ItemID, ExpDate, quantity from Itemacquired where ItemID=%s order by ExpDate) select ItemId, ExpDate, Quantity, sum(Quantity) over (order by ExpDate) as cumulative_sum from data) a left join Item I on a.ItemId = I.ItemID where cumulative_sum > %s"
                
                    valRS = (realStock[1], realStock[0], realStock[1])
                    cursor.execute(sql,valRS)    
                    compDates = cursor.fetchone()

                    if compDates[3]<=compDates[4]:
                        cursor.execute(sql,valRS)
                        for rec in cursor:
                            treeExpiry.insert('','end',value=rec)


    



#700x550
    #def notif(myTitle, myMessage):
    #    notification.notify(
    #    title=myTitle,
    #    message=myMessage,
    #    app_icon=None,
    #    timeout=10
    #)



    def closure():
        exit(0)
        

    #treeView

    columnsExpiry = ('Item ID', 'Product', 'Expiry Date', 'daysDif', 'daysAlarm', '#Items')
    treeExpiry = ttk.Treeview(Frame, height=10, columns=columnsExpiry, show='headings')
    treeExpiry.place(x=250, y= 270, width = 600 , height = 150)

    for col in columnsExpiry:
        treeExpiry.heading(col, text=col)
        treeExpiry.column(col, width=100, anchor=CENTER)

    sb = Scrollbar(Frame, orient=VERTICAL, command=treeExpiry.yview)
    sb.place(x=831, y=271, height=148)
    treeExpiry.config(yscrollcommand=sb.set)


    columnsLowStock = ('Item ID', 'product','Current Stock')
    treeLowStock = ttk.Treeview(Frame, height=10, columns=columnsLowStock, show='headings')
    treeLowStock.place(x=250, y= 50, width = 600 , height = 150)

    for col in columnsLowStock:
        treeLowStock.heading(col, text=col)
        treeLowStock.column(col, width=100, anchor=CENTER)

    sb = Scrollbar(Frame, orient=VERTICAL, command=treeLowStock.yview)
    sb.place(x=831, y=51, height=148)
    treeLowStock.config(yscrollcommand=sb.set)


    #Buttons

    Data_Manag_btn = Button(Frame, text='Data Management', width=15, command=Data_Management)
    Data_Manag_btn.place(x=100, y=60)

    Inventory_btn = Button(Frame, text='Inventory', width=15, command=Inventory)
    Inventory_btn.place(x=100, y=140)

    Reports_btn = Button(Frame, text='Reports', width=15, command=Reports)
    Reports_btn.place(x=100, y=220)

    Settings_btn = Button(Frame, text='Settings', width=15, command=Settings)
    Settings_btn.place(x=100, y=300)

    #Labels

    LowAvailability_label = Label(Frame, text='Low Availability!!', font=('bold', 15), fg='red')
    LowAvailability_label.place(x=250, y=20)

    Expiry_label = Label(Frame, text='Expired Items or about to expired!!', font=('bold', 15), fg='red')
    Expiry_label.place(x=250, y=240)


    fillAlerts()
    Frame.protocol('WM_DELETE_WINDOW',closure)
    #notif("Alert", "Notification")
    return
    

if __name__ == "__main__":
       

    app = Tk()
    app.title('Administrator')
    app.geometry('900x500')
    

    OpenNewWindowAdmnDash(app)
    app.mainloop()