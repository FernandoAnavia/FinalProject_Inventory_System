from tkinter import *
from tkinter import messagebox
from db import *
from tkinter import ttk
import re
from tkcalendar import *
from logInSession import *

def OpenNewWindowStore(Frame):

    def combo_inputItem():

        cursor = mydb.cursor()

        cursor.execute("SELECT IName FROM Item")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0])

        return result

    def combo_inputItemID(event):

        cursor = mydb.cursor()
        
        val =  Item_combo.get()
        print (val)

        sql = "SELECT ItemID FROM Item where IName = %s"       

        cursor.execute(sql, (val,))
        BId = cursor.fetchone()

        print(BId)
        ID_entry.delete(0,END)
        ID_entry.insert(0,BId)

        sql = "SELECT (Select IFNULL(SUM(Quantity),0) from Itemacquired where ItemID = %s) - (Select IFNULL(SUM(Quantity),0) from Itemoutput where ItemID = %s)AS Difference"
        cursor.execute(sql, (BId[0], BId[0],))

        AvaValue = cursor.fetchone()

        AvMax.set(AvaValue)

        sql = "SElECT S_Price, Discount FROM Item Where ItemID = %s"

        cursor.execute(sql, (BId[0],))
        currentVal = cursor.fetchone()

        PSet.set(currentVal[0])
        DiscountV.set(currentVal[1])

        print(currentVal)




    def combo_payment():

        cursor = mydb.cursor()

        cursor.execute("SELECT Method FROM payment")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0])

        return result


    def combo_paymentID(event):
        
        cursor = mydb.cursor()
        
        val =  paymentMethod_combo.get()

        sql = "SELECT PaymentID FROM payment where method = %s"

        cursor.execute(sql, (val,))
        BId = cursor.fetchone()

        paymentMethod_entry.delete(0,END)
        paymentMethod_entry.insert(0,BId)



    def fill_list():

        cursor = mydb.cursor()

        sql = "SELECT I.IName, O.quantity, I.S_Price, I.Discount, round((O.quantity * I.S_Price * I.Discount/100),2) AS Savings, round((O.quantity * I.S_Price * (1 - I.Discount/100)),2) AS subtotal FROM ItemOutput O Left Join Item I  on I.ItemID = O.ItemID where TicketID = %s"
        val = UserDetails.CurrentTicket

        cursor.execute(sql,(val,))

        tree.delete(*tree.get_children())

        for rec in cursor:
            tree.insert('','end',value=rec)

    def addItemTo():

        mycursor = mydb.cursor()

        sql = "SELECT (Select IFNULL(SUM(Quantity),0) from Itemacquired where ItemID = %s) - (Select IFNULL(SUM(Quantity),0) from Itemoutput where ItemID = %s)AS Difference"

        mycursor.execute(sql, (ID_text.get(),ID_text.get(),))
        currentVal2 = mycursor.fetchone()

        if ID_text.get() == '' or quantity_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up all fields')
            return
    
        if quantity_text.get() > currentVal2[0]:
            messagebox.showerror('Error','Insufficient Stock')
            return

        sql = "INSERT INTO ItemOutput (ItemId, TicketID, StatusID, S_Price, Discount, Quantity) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Quantity = Quantity + %s"
        val = (ID_text.get(), str(UserDetails.CurrentTicket), 1, PSet.get(), DiscountV.get(), quantity_text.get(), quantity_text.get())
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        fill_list()

        sql = "select round(sum((O.quantity * I.S_Price * (1 - I.Discount/100))),2) as Total From ItemOutput O Left Join Item I  on I.ItemID = O.ItemID where TicketID = %s"
        val = UserDetails.CurrentTicket

        mycursor.execute(sql,(val,))
        
        totalV = mycursor.fetchone()

        valTotal.set(totalV)

        newMax = currentVal2[0] - quantity_text.get()
        AvMax.set(newMax)

        quantity_entry.delete(0,END)
        quantity_entry.insert(0,1)


        print(mycursor.rowcount, "Item added")



    def TicketClosure():

        mycursor = mydb.cursor()
        
        sqlD = "select round(sum((O.quantity * I.S_Price * (I.Discount/100))),2) as Total From ItemOutput O Left Join Item I  on I.ItemID = O.ItemID where ticketID = %s"
        ticket = UserDetails.CurrentTicket

        if paymentMethod_text.get() == '':
            messagebox.showerror ('Error', 'Please choose a payment method')
            return

        mycursor.execute(sqlD,(ticket,))
        DiscTot = mycursor.fetchone()

        sqlT = "select round(sum((O.quantity * I.S_Price * (1 - I.Discount/100))),2) as Total From ItemOutput O Left Join Item I  on I.ItemID = O.ItemID where ticketID = %s"

        mycursor.execute(sqlT,(ticket,))
        TotalFinal = mycursor.fetchone()

        sql2 = "UPDATE Ticket SET paymentID = %s, Total = %s, Discount = %s WHERE TicketID = %s"
        val = (paymentMethod_text.get(),TotalFinal[0],DiscTot[0],ticket)
      
        try:
            mycursor.execute(sql2, val)
            mydb.commit()
            messagebox.showinfo('Transaction completed', 'Ticket created')
        
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)




    def clear_ticket():
        value = 0.0
        Item_combo.set('')
        ID_entry.delete(0,END)
        quantity_entry.delete(0,END)
        quantity_entry.insert(0,1)
        AvMax.set(0)
        PSet.set(0.0)
        DiscountV.set(0.0)
        paymentMethod_combo.set('')


    def startingData ():
        mycursor = mydb.cursor()

              #SELECT MAX(TicketID) From ticket
        sql = "SELECT TicketID From ticket order by TicketID DESC limit 1"
        mycursor.execute(sql)

        tickNumb = mycursor.fetchone()
        UserDetails.CurrentTicket = tickNumb[0]

        #Main Label
        TicketLabel = Label (Frame, text= 'Ticket # ' + str(UserDetails.CurrentTicket), font=('bold', 20), fg="red")
        TicketLabel.grid(row=0, column=0, columnspan = 2, pady = 10)

        fill_list()



    #Item to be added
    ID_text = StringVar()
    ID_label = Label(Frame, text='ITEM', font=('bold', 14), pady=10, padx=15)
    ID_label.grid(row=1,column=0, sticky=W)
    ID_entry = Entry(Frame, textvariable = ID_text)
    #ID_entry.grid(row=1, column=2)

    m = StringVar()
    Item_combo = ttk.Combobox (Frame, state="readonly", width = 17, textvariable = m) 

    # Adding combobox drop down list (Item to be added)

    Item_combo['values'] = combo_inputItem()
    Item_combo.bind("<<ComboboxSelected>>",combo_inputItemID)
    Item_combo.grid(row=1, column=1)


    #Available
    AvMax = IntVar()
    AvMax.set(0)
    
    Available_label = Label(Frame, text='Availability', font=('bold', 14), pady=20)
    Available_label.grid(row=1,column=4, sticky=W, padx = 15)
    Availability_label = Label(Frame, textvariable = AvMax, font=(12), fg="darkblue", pady=20)
    Availability_label.grid(row=1,column=5)

    #Price
    PSet = DoubleVar()
    PSet.set(0.0)
    
    Price_label = Label(Frame, text='Price (€)', font=('bold', 14), pady=20, padx=15)
    Price_label.grid(row=2,column=0, sticky=W)
    PriceUpdated_label = Label(Frame, textvariable = PSet, font=(12), fg="darkblue", pady=20)
    PriceUpdated_label.grid(row=2,column=1)

    #Discount
    DiscountV = DoubleVar()
    DiscountV.set(0.0)
    
    Discount_label = Label(Frame, text='Discount (%)', font=('bold', 14), pady=20, padx=15)
    Discount_label.grid(row=2,column=2, sticky=W)
    DiscountApplied_label = Label(Frame, textvariable = DiscountV, font=(12), fg="darkblue", pady=20, padx=50)
    DiscountApplied_label.grid(row=2,column=3)

    #Quantity
    quantity_text = IntVar()
    quantity_text.set(1)
    quantity_label = Label(Frame, text='Quantity', font=('bold', 14), pady=20, padx = 15)
    quantity_label.grid(row=2,column=4, sticky=W)
    quantity_entry = Entry(Frame, textvariable = quantity_text)
    quantity_entry.grid(row=2, column=5)


    #paymentMethod

    n = StringVar()
    paymentMethod_combo = ttk.Combobox (Frame, state="readonly", width = 17, textvariable = n) 

    # Adding combobox drop down list 
    paymentMethod_combo['values'] = combo_payment()
    paymentMethod_combo.bind("<<ComboboxSelected>>",combo_paymentID)
    paymentMethod_combo.grid(row=3, column=1) 



    paymentMethod_text = StringVar()
    paymentMethod_label = Label(Frame, text='Payment', font=('bold', 14), pady=20, padx=15)
    paymentMethod_label.grid(row=3,column=0, sticky=W)
    paymentMethod_entry = Entry(Frame, textvariable = paymentMethod_text)

    #paymentMethod_entry.grid(row=3, column=3)

    # Total

    valTotal = DoubleVar()


    TotalLabel = Label (Frame, text= 'TOTAL', font=('bold', 20), fg="red")
    TotalLabel.grid(row=3, column=4)
    TicketLabel = Label (Frame, textvariable = valTotal , font=('bold', 20), fg="red")
    TicketLabel.grid(row=3, column=5)

    #treeView

    columns = ('Item', 'Quantity', 'Price', 'Discount', 'Savings', 'Subtotal')
    tree = ttk.Treeview(Frame, height=10, columns=columns, show='headings')
    tree.place(x=50, y= 320, width = 700 , height = 200)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=CENTER)

    sb = Scrollbar(Frame, orient=VERTICAL, command=tree.yview)
    sb.place(x=731, y=321, height=198)
    tree.config(yscrollcommand=sb.set)


    #Buttons

    addItem_btn = Button(Frame, text='Add Item', width=12, command=addItemTo)
    addItem_btn.place(x=75, y=265)

    closeTicket_btn = Button(Frame, bg = "indianred2", text='Close Ticket', width=12, command=TicketClosure)
    closeTicket_btn.place(x=260, y=265)

    clear_btn = Button(Frame, text='Clear input', width=12, command=clear_ticket)
    clear_btn.place(x=445, y=265)


    startingData()
    return


if __name__ == "__main__":
    app = Tk()
    app.title('Store System')
    app.geometry('800x600')

    OpenNewWindowStore(app)
    app.mainloop()