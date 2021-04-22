from tkinter import *
from tkinter import messagebox
from db import *
from tkinter import ttk
import re
from tkcalendar import *
from sys import exit

def OpenNewWindowItemD(Frame):
    def combo_input():

        cursor = mydb.cursor()

        cursor.execute("SELECT BName FROM Branch")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0])

        return result

    def combo_inputID(event):
        
        cursor = mydb.cursor()
        
        val =  Branch_combo.get()

        sql = "SELECT BId FROM Branch where BName = %s"

        cursor.execute(sql, (val,))
        BId = cursor.fetchone()
        print(BId)
        Branch_entry.delete(0,END)
        Branch_entry.insert(0,BId)

    def combo_inputIC():

        cursor = mydb.cursor()

        cursor.execute("SELECT Classification FROM ItemClassification")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0])
        return result

    def combo_inputICID(event):
        
        cursor = mydb.cursor()
        
        val =  iClass_combo.get()
        print (val)

        sql = "SELECT ItemClassID FROM ItemClassification where Classification = %s"

        cursor.execute(sql, (val,))
        BId = cursor.fetchone()
        print(BId)
        iClass_entry.delete(0,END)
        iClass_entry.insert(0,BId)


    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT I.ItemId, I.IName, I.IDescription, I.BId, B.BName, I.ItemClassID, C.Classification, I.S_Price, I.Discount FROM Item I LEFT JOIN Branch B ON B.BId = I.BId LEFT JOIN ItemClassification C ON C.ItemClassID = I.ItemClassID ORDER BY I.ItemId")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_item():
        
        if ID_text.get() == '' or Name_text.get() == '' or Description_text.get() == '' or Branch_text.get() == '' or iClass_text.get() == '' or S_price_text.get() == 0.0:
            messagebox.showerror('Require Fields', 'Please fill up all fields')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO item (ItemId, IName, IDescription, BId, ItemClassID, S_Price, Discount, ExpDateVal) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        val = (ID_text.get(), Name_text.get(), Description_text.get(), Branch_text.get(), iClass_text.get(), S_price_text.get(), Discount_text.get(),7)
        
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
            Name_entry.delete(0, END)
            Name_entry.insert(END, selected_item[1])
            Description_entry.delete(0, END)
            Description_entry.insert(END, selected_item[2])
            Branch_entry.delete(0, END)
            Branch_entry.insert(END, selected_item[3])
            Branch_combo.set(selected_item[4])
            iClass_entry.delete(0, END)
            iClass_entry.insert(END, selected_item[5])
            iClass_combo.set(selected_item[6])
            S_price_entry.delete(0, END)
            S_price_entry.insert(END, selected_item[7])
            Discount_entry.delete(0, END)
            Discount_entry.insert(END, selected_item[8])
        except IndexError:
            pass

    def delete_item():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM item WHERE ItemId = %s"
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

        sql = "UPDATE item SET IName = %s, IDescription = %s, BId = %s, ItemClassID = %s, S_Price = %s, Discount = %s WHERE ItemId = %s"
        val = (Name_text.get(), Description_text.get(), Branch_text.get(), iClass_text.get(), S_price_text.get(), Discount_text.get(), ID_text.get())
        
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
        Name_entry.delete(0,END)
        Description_entry.delete(0,END)
        Branch_entry.delete(0,END)
        iClass_entry.delete(0,END)
        S_price_entry.delete(0,END)
        S_price_entry.insert(0,value)
        Discount_entry.delete(0,END)
        Discount_entry.insert(0,value)
        Branch_combo.set('')
        iClass_combo.set('')

    def find_item():
        
        mycursor = mydb.cursor()

        sql = "SELECT I.ItemId, I.IName, I.IDescription, I.BId, B.BName, I.ItemClassID, C.Classification, I.S_Price, I.Discount FROM Item I INNER JOIN Branch B ON B.BId = I.BId INNER JOIN ItemClassification C ON C.ItemClassID = I.ItemClassID and I.ItemId = %s"
        val = ID_text.get()
        
        try:
        
            mycursor.execute(sql, (val,))
            
            record = mycursor.fetchone()

            #for X in record:
            #    print(X)


            Name_entry.delete(0, END)
            Name_entry.insert(0, record[1])
            Description_entry.delete(0, END)
            Description_entry.insert(END, record[2])
            Branch_entry.delete(0, END)
            Branch_entry.insert(END, record[3])
            Branch_combo.set(record[4])
            iClass_entry.delete(0, END)
            iClass_entry.insert(END, record[5])
            iClass_combo.set(record[6])
            S_price_entry.delete(0, END)
            S_price_entry.insert(END, record[7])
            Discount_entry.delete(0, END)
            Discount_entry.insert(END, record[8])

        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

    def backCom():
        from management import OpenNewWindowManagement

        #Frame.iconify()
        win1 = Toplevel(Frame)
        win1.geometry('550x450')
        win1.title('Management')
        Frame.withdraw()
        OpenNewWindowManagement(win1)
        #win1.deiconify()
        return

    def closure():
        exit(0)

    #ID
    ID_text = StringVar()
    ID_label = Label(Frame, text='ID', font=('bold', 14), pady=20)
    ID_label.grid(row=0,column=0, sticky=W)
    ID_entry = Entry(Frame, textvariable = ID_text)
    ID_entry.grid(row=0, column=1)

    #Name
    Name_text = StringVar()
    Name_label = Label(Frame, text='Name', font=('bold', 14), pady=20)
    Name_label.grid(row=0,column=2, sticky=W)
    Name_entry = Entry(Frame, textvariable = Name_text)
    Name_entry.grid(row=0, column=3)

    #Description
    Description_text = StringVar()
    Description_label = Label(Frame, text='Description', font=('bold', 14), pady=20)
    Description_label.grid(row=0,column=4, sticky=W)
    Description_entry = Entry(Frame, textvariable = Description_text)
    Description_entry.grid(row=0, column=5)

    #Branch

    n = StringVar()
    Branch_combo = ttk.Combobox (Frame, state="readonly", width = 17, textvariable = n) 

    # Adding combobox drop down list 
    Branch_combo['values'] = combo_input()
    Branch_combo.bind("<<ComboboxSelected>>",combo_inputID)
    Branch_combo.grid(row=2, column=1) 



    Branch_text = StringVar()
    Branch_label = Label(Frame, text='Branch', font=('bold', 14), pady=20)
    Branch_label.grid(row=2,column=0, sticky=W)
    Branch_entry = Entry(Frame, textvariable = Branch_text)

    #Branch_entry.grid(row=3, column=1)



    #ItemClass

    m = StringVar()

    iClass_combo = ttk.Combobox (Frame, state="readonly", width = 17, textvariable = m) 

    iClass_combo['values'] = combo_inputIC()
    iClass_combo.bind("<<ComboboxSelected>>",combo_inputICID)
    iClass_combo.grid(row=2, column=3) 

    iClass_text = DoubleVar()
    iClass_label = Label(Frame, text='Item Class', font=('bold', 14), pady=20)
    iClass_label.grid(row=2,column=2, sticky=W)
    iClass_entry = Entry(Frame, textvariable = iClass_text)
    #iClass_entry.grid(row=2, column=3)

    #Selling Price
    S_price_text = DoubleVar()
    S_price_label = Label(Frame, text='Selling Price', font=('bold', 14), pady=20)
    S_price_label.grid(row=2,column=4, sticky=W)
    S_price_entry = Entry(Frame, textvariable = S_price_text)
    S_price_entry.grid(row=2, column=5)

    #Discount
    Discount_text = DoubleVar()
    Discount_label = Label(Frame, text='Discount (%)', font=('bold', 14), pady=20)
    Discount_label.grid(row=4,column=4, sticky=W)
    Discount_entry = Entry(Frame, textvariable = Discount_text)
    Discount_entry.grid(row=4, column=5)

    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.grid(row=7, column=0, columnspan=6, rowspan=8, pady=20, padx=20)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=610, y=285, height = 160)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_item)

    #Buttons

    find_btn = Button(Frame, text='Find Item by ID', width=12, command=find_item)
    find_btn.grid(row=6, column=1, pady=20)

    add_btn = Button(Frame, text='Add Item', width=12, command=add_item)
    add_btn.grid(row=6, column=2)

    delete_btn = Button(Frame, text='Delete Item', width=12, command=delete_item)
    delete_btn.grid(row=6, column=3)

    update_btn = Button(Frame, text='Update Item', width=12, command=update_item)
    update_btn.grid(row=6, column=4)

    clear_btn = Button(Frame, text='Clear input', width=12, command=clear_text)
    clear_btn.grid(row=6, column=5)

    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=580, y=500)


    fill_list()
    Frame.protocol('WM_DELETE_WINDOW',closure)    
    return


if __name__ == "__main__":
    app = Tk()
    app.title('Item control')
    app.geometry('700x550')

    OpenNewWindowItemD(app)
    app.mainloop()