from tkinter import *
from tkinter import messagebox
from db import *
from tkinter import ttk
import re
from tkcalendar import *
from datetime import date, time, datetime



def OpenNewWindowOrders(Frame):

    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM Orders")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_item():
        
        if Description_text.get() == '' or orderDate_text.get() == '' or total_text.get() == '' or taxPaid_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up all fields')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO Orders (ODescription, ODate, Total, TaxPaid) VALUES (%s, %s, %s, %s)"
        val = (Description_text.get(), orderDate_text.get(), total_text.get(), taxPaid_text.get())
        
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


            ID_entry.delete(0, END)
            ID_entry.insert(END, selected_item[0])
            Description_entry.delete(0, END)
            Description_entry.insert(END, selected_item[1])
            orderDate_entry.delete(0, END)
            orderDate_entry.insert(END, selected_item[2])
            total_entry.delete(0, END)
            total_entry.insert(END, selected_item[3])
            taxPaid_entry.delete(0, END)
            taxPaid_entry.insert(END, selected_item[4])

        except IndexError:
            pass

    def delete_item():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM Orders WHERE OrderID = %s"
        val = ID_text.get()
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to delete the Item?', icon = 'warning')
        if MsgBox == 'yes':
        
            try:
                mycursor.execute(sql, (val,))
                mydb.commit()
            
            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "Item(s) deleted"))

        else:
            messagebox.showinfo ('Message', 'The item was not deleted')

    def update_item():

        mycursor = mydb.cursor()

        sql = "UPDATE Orders SET ODescription = %s, ODate = %s, Total = %s, TaxPaid = %s WHERE OrderID = %s"
        val = (Description_text.get(), orderDate_text.get(), total_text.get(), taxPaid_text.get(), ID_text.get())
        
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
        ID_entry.delete(0,END)
        Description_entry.delete(0,END)
        Description_entry.delete(0,END)
        total_entry.delete(0,END)
        total_entry.insert(0,value)
        taxPaid_entry.delete(0,END)
        taxPaid_entry.insert(0,value)
        today1()

    def find_item():
        
        mycursor = mydb.cursor()

        sql = "SELECT ODescription, Odate, Total, TaxPaid FROM Orders where OrderID = %s"
        val = ID_text.get()
        
        try:
        
            mycursor.execute(sql, (val,))
            
            record = mycursor.fetchone()

            Description_entry.delete(0, END)
            Description_entry.insert(END, record[0])
            orderDate_entry.delete(0, END)
            orderDate_entry.insert(END, record[1])
            total_entry.delete(0, END)
            total_entry.insert(END, record[2])
            taxPaid_entry.delete(0, END)
            taxPaid_entry.insert(END, record[3])

        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

    def getDate(event):
        orderDate_entry.delete(0,END)
        orderDate_entry.insert(0,cal.selection_get())

    def today1():
        orderDate_entry.delete(0,END)
        orderDate_entry.insert(0,date.today())



    #ID
    ID_text = StringVar()
    ID_label = Label(Frame, text='Order ID (A_I)', font=('bold', 14), pady=20)
    ID_label.grid(row=0,column=0, sticky=W)
    ID_entry = Entry(Frame, textvariable = ID_text)
    ID_entry.grid(row=0, column=1)

    #Description
    Description_text = StringVar()
    Description_label = Label(Frame, text='Description', font=('bold', 14), pady=20)
    Description_label.grid(row=0,column=2, sticky=W)
    Description_entry = Entry(Frame, textvariable = Description_text)
    Description_entry.grid(row=0, column=3)

    #orderDate
    orderDate_text = StringVar()
    orderDate_label = Label(Frame, text='Order Date', font=('bold', 14), pady=20)
    orderDate_label.grid(row=0,column=4, sticky=W)
    orderDate_entry = Entry(Frame, textvariable = orderDate_text)
    #orderDate_entry.grid(row=0, column=5)


    #Total
    total_text = DoubleVar()
    total_label = Label(Frame, text='Total', font=('bold', 14), pady=20)
    total_label.grid(row=2,column=0, sticky=W)
    total_entry = Entry(Frame, textvariable = total_text)
    total_entry.grid(row=2, column=1)

    #taxPaid
    taxPaid_text = DoubleVar()
    taxPaid_label = Label(Frame, text='Taxes Paid', font=('bold', 14), pady=20)
    taxPaid_label.grid(row=2,column=2, sticky=W)
    taxPaid_entry = Entry(Frame, textvariable = taxPaid_text)
    taxPaid_entry.grid(row=2, column=3)

    #calendar
    todays_date = date.today()

    cal = Calendar(Frame, selectmode="day", year=todays_date.year, month=todays_date.month, day=todays_date.day)
    cal.place (x=500, y=60)
    cal.bind('<<CalendarSelected>>', getDate)

    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.place(x= 50, y= 270, width = 700, height = 250)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=745, y=270, height = 250)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_item)

    #Buttons

    find_btn = Button(Frame, text='Find Item by ID', width=12, command=find_item)
    find_btn.place(x=125, y=200)

    add_btn = Button(Frame, text='Add Item', width=12, command=add_item)
    add_btn.place(x=50, y=150)

    delete_btn = Button(Frame, text='Delete Item', width=12, command=delete_item)
    delete_btn.place(x=200, y=150)

    update_btn = Button(Frame, text='Update Item', width=12, command=update_item)
    update_btn.place(x=350, y=150)

    clear_btn = Button(Frame, text='Clear input', width=12, command=clear_text)
    clear_btn.place(x=275, y=200)

    today1()
    fill_list()
    return


if __name__ == "__main__":
    app = Tk()
    app.title('Orders Control')
    app.geometry('800x600')

    OpenNewWindowOrders(app)
    app.mainloop()