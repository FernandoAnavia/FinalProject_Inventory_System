from tkinter import *
from tkinter import messagebox
from db import *
from tkinter import ttk
import re
from tkcalendar import *
from datetime import date, time, datetime



def OpenNewWindowItemAcq(Frame):


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
        
        val =  ItemID_combo.get()

        sql = "SELECT ItemID FROM Item where IName = %s"
    
        cursor.execute(sql, (val,))
        BId = cursor.fetchone()
        print(BId)
        ItemID_entry.delete(0,END)
        ItemID_entry.insert(0,BId)


    def combo_inputOrder():
    
        cursor = mydb.cursor()

        cursor.execute("SELECT ODescription FROM Orders")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0])

        return result
        

    def combo_inputOrderID(event):
        
        cursor = mydb.cursor()
        
        val =  OrderID_combo.get()

        sql = "SELECT OrderID FROM Orders where ODescription = %s"
    
        cursor.execute(sql, (val,))
        BId = cursor.fetchone()
        print(BId)
        OrderID_entry.delete(0,END)
        OrderID_entry.insert(0,BId)

    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT I.ItemId, X.IName, I.OrderID, O.ODescription, I.ExpDate, I.PurchasePrice, I.taxes, I.Quantity FROM ItemAcquired I LEFT JOIN Item X ON X.ItemID = I.ItemID LEFT JOIN Orders O ON O.OrderID = I.OrderID ORDER BY O.Odate")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_item():
        
        if ItemID_text.get() == '' or OrderID_text.get() == '' or expDate_text.get() == '' or pPrice_text.get() == '' or Taxes_text.get() == '' or Quantity_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up all fields')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO ItemAcquired (ItemID, OrderID, ExpDate, PurchasePrice, taxes, Quantity) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (ItemID_text.get(), OrderID_text.get(), expDate_text.get(), pPrice_text.get(), Taxes_text.get(), Quantity_text.get())
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        fill_list()

        print(mycursor.rowcount, "Item added")


    def select_item(event):
        try:
            global selected_item
            index = part_list.curselection()[0]
            selected_item = part_list.get(index)


            ItemID_entry.delete(0, END)
            ItemID_entry.insert(END, selected_item[0])
            ItemID_combo.set(selected_item[1])
            OrderID_entry.delete(0, END)
            OrderID_entry.insert(END, selected_item[2])
            OrderID_combo.set(selected_item[3])
            expDate_entry.delete(0, END)
            expDate_entry.insert(END, selected_item[4])
            pPrice_entry.delete(0, END)
            pPrice_entry.insert(END, selected_item[5])
            Taxes_entry.delete(0, END)
            Taxes_entry.insert(END, selected_item[6])
            Quantity_entry.delete(0, END)
            Quantity_entry.insert(END, selected_item[7])

        except IndexError:
            pass

    def delete_item():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM ItemAcquired WHERE ItemId = %s and OrderID = %s and ExpDate = %s"
        val = (ItemID_text.get(), OrderID_text.get(), expDate_text.get())
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to delete the Item?', icon = 'warning')
        if MsgBox == 'yes':
        
            try:
                mycursor.execute(sql, val)
                mydb.commit()
            
            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "Item(s) deleted"))

        else:
            messagebox.showinfo ('Message', 'The item was not deleted')

    def update_item():

        mycursor = mydb.cursor()

        sql = "UPDATE ItemAcquired SET PurchasePrice = %s, taxes = %s, Quantity = %s WHERE ItemID = %s and OrderID = %s and ExpDate = %s"
        val = (pPrice_text.get(), Taxes_text.get(), Quantity_text.get(), ItemID_text.get(), OrderID_text.get(), expDate_text.get())
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to update the Item?', icon = 'warning')
        if MsgBox == 'yes':

            try:
        
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "Item(s) updated"))

        else:
            messagebox.showinfo ('Message', 'The item was not updated')


    def clear_text():

        value = 0.0
        ItemID_entry.delete(0,END)
        ItemID_combo.set('')
        OrderID_entry.delete(0,END)
        OrderID_combo.set('')
        pPrice_entry.delete(0,END)
        pPrice_entry.insert(0,value)
        Taxes_entry.delete(0,END)
        Taxes_entry.insert(0,value)
        Quantity_entry.delete(0,END)
        today1()

    def find_item():
        
        mycursor = mydb.cursor()

        sql = "SELECT PurchasePrice, Taxes, Quantity FROM ItemAcquired where ItemID = %s and orderID = %s and ExpDate = %s"
        val = (ItemID_text.get(), OrderID_text.get(), expDate_text.get())
        
        try:
        
            mycursor.execute(sql, val)
            
            record = mycursor.fetchone()

            for X in record:
                print(X)

            pPrice_entry.delete(0, END)
            pPrice_entry.insert(END, record[0])
            Taxes_entry.delete(0, END)
            Taxes_entry.insert(END, record[1])
            Quantity_entry.delete(0, END)
            Quantity_entry.insert(END, record[2])

        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

    def getDate(event):
        expDate_entry.delete(0,END)
        expDate_entry.insert(0,cal.selection_get())

    def today1():
        expDate_entry.delete(0,END)
        expDate_entry.insert(0,date.today())



    #ItemID

    n = StringVar()
    ItemID_combo = ttk.Combobox (Frame, state="readonly", width = 16, textvariable = n) 

    ItemID_combo['values'] = combo_inputItem()
    ItemID_combo.bind("<<ComboboxSelected>>",combo_inputItemID)
    ItemID_combo.grid(row=0, column=1) 
    
    ItemID_text = StringVar()
    ItemID_label = Label(Frame, text='Item Name', font=('bold', 14), pady=20)
    ItemID_label.grid(row=0,column=0, sticky=W)
    ItemID_entry = Entry(Frame, textvariable = ItemID_text)
    #ItemID_entry.grid(row=0, column=1)

    #OrderID

    m = StringVar()
    OrderID_combo = ttk.Combobox (Frame, state="readonly", width = 16, textvariable = m) 

    OrderID_combo['values'] = combo_inputOrder()
    OrderID_combo.bind("<<ComboboxSelected>>",combo_inputOrderID)
    OrderID_combo.grid(row=0, column=3) 
    
    OrderID_text = StringVar()
    OrderID_label = Label(Frame, text='Order Desc', font=('bold', 14), pady=20)
    OrderID_label.grid(row=0,column=2, sticky=W)
    OrderID_entry = Entry(Frame, textvariable = OrderID_text)
    #OrderID_entry.grid(row=0, column=1)

    #expDate
    expDate_text = StringVar()
    expDate_label = Label(Frame, text='Expiry Date', font=('bold', 14), pady=20)
    expDate_label.grid(row=0,column=5, sticky=W)
    expDate_entry = Entry(Frame, textvariable = expDate_text)
    #expDate_entry.grid(row=0, column=4)


    #Purchase Price
    pPrice_text = DoubleVar()
    pPrice_label = Label(Frame, text='Total', font=('bold', 14), pady=20)
    pPrice_label.grid(row=2,column=0, sticky=W)
    pPrice_entry = Entry(Frame, textvariable = pPrice_text)
    pPrice_entry.grid(row=2, column=1)

    #Taxes
    Taxes_text = DoubleVar()
    Taxes_label = Label(Frame, text='Taxes Paid', font=('bold', 14), pady=20)
    Taxes_label.grid(row=2,column=2, sticky=W)
    Taxes_entry = Entry(Frame, textvariable = Taxes_text)
    Taxes_entry.grid(row=2, column=3)

    #Quantity
    Quantity_text = IntVar()
    Quantity_label = Label(Frame, text='Quantity', font=('bold', 14), pady=20)
    Quantity_label.grid(row=2,column=4, sticky=W)
    Quantity_entry = Entry(Frame, textvariable = Quantity_text)
    Quantity_entry.grid(row=2, column=5)

    #calendar
    todays_date = date.today()

    cal = Calendar(Frame, selectmode="day", year=todays_date.year, month=todays_date.month, day=todays_date.day)
    cal.place (x=670, y=20)
    cal.bind('<<CalendarSelected>>', getDate)

    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.place(x= 50, y= 220, width = 850, height = 300)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=895, y=220, height = 300)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_item)

    #Buttons

    find_btn = Button(Frame, text='Find Item by ID', width=12, command=find_item)
    find_btn.place(x=30, y=155)

    add_btn = Button(Frame, text='Add Item', width=12, command=add_item)
    add_btn.place(x=155, y=155)

    delete_btn = Button(Frame, text='Delete Item', width=12, command=delete_item)
    delete_btn.place(x=280, y=155)

    update_btn = Button(Frame, text='Update Item', width=12, command=update_item)
    update_btn.place(x=405, y=155)

    clear_btn = Button(Frame, text='Clear input', width=12, command=clear_text)
    clear_btn.place(x=530, y=155)

    today1()
    fill_list()
    return


if __name__ == "__main__":
    app = Tk()
    app.title('Items Acquired')
    app.geometry('950x600')

    OpenNewWindowItemAcq(app)
    app.mainloop()