from tkinter import *
from tkinter import messagebox
from db import *
from tkinter import ttk
import re

def OpenNewWindowUserD(Frame):

    def combo_input():
    
        cursor = mydb.cursor()

        cursor.execute("SELECT typeOfUser FROM UserType")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0])

        return result
        

    

    def combo_inputID(event):
        
        cursor = mydb.cursor()
        
        val =  userType_combo.get()

        sql = "SELECT uTypeId FROM UserType where typeOfUser = %s"
    
        cursor.execute(sql, (val,))
        BId = cursor.fetchone()
        print(BId)
        userType_entry.delete(0,END)
        userType_entry.insert(0,BId)


    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT U.UserId, U.firstName, U.lastName, U.loginPassword, U.uTypeId, T.typeOfUser, U.contactNumber, U.email FROM UserSystem U LEFT JOIN UserType T ON U.uTypeId = T.uTypeId ORDER BY U.UserId")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_User():
        
        if UserId_text.get() == '' or firstName_text.get() == '' or lastName_text.get() == '' or Password_text.get() == '' or userType_text.get() == '' or contactNumber_text.get() == '' or email_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up all fields')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO UserSystem (UserId, firstName, lastName, loginPassword, uTypeId, contactNumber, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (UserId_text.get(), firstName_text.get(), lastName_text.get(), Password_text.get(), userType_text.get(), contactNumber_text.get(), email_text.get())
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        fill_list()

        print(mycursor.rowcount, "User added")


    def select_User(event):
        try:
            global selected_User
            index = part_list.curselection()[0]
            selected_User = part_list.get(index)


            UserId_entry.delete(0, END)
            UserId_entry.insert(END, selected_User[0])
            firstName_entry.delete(0, END)
            firstName_entry.insert(END, selected_User[1])
            lastName_entry.delete(0, END)
            lastName_entry.insert(END, selected_User[2])
            Password_entry.delete(0, END)
            Password_entry.insert(END, selected_User[3])
            userType_entry.delete(0, END)
            userType_entry.insert(END, selected_User[4])
            userType_combo.set(selected_User[5])
            contactNumber_entry.delete(0, END)
            contactNumber_entry.insert(END, selected_User[6])
            email_entry.delete(0, END)
            email_entry.insert(END, selected_User[7])
        except IndexError:
            pass

    def delete_User():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM UserSystem WHERE UserId = %s"
        val = UserId_text.get()
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to delete the User?', icon = 'warning')
        if MsgBox == 'yes':
        
            try:
                mycursor.execute(sql, (val,))
                mydb.commit()
            
            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "User(s) deleted"))

        else:
            messagebox.showinfo ('Message', 'The User was not deleted')

    def update_User():

        mycursor = mydb.cursor()

        sql = "UPDATE UserSystem SET firstName = %s, lastName = %s, loginPassword = %s, uTypeId = %s, contactNumber = %s, email = %s WHERE UserId = %s"
        val = (firstName_text.get(), lastName_text.get(), Password_text.get(), userType_text.get(), contactNumber_text.get(), email_text.get(), UserId_text.get())
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to update the User?', icon = 'warning')
        if MsgBox == 'yes':

            try:
        
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "User(s) updated"))

        else:
            messagebox.showinfo ('Message', 'The User was not updated')


    def clear_text():
        
        UserId_entry.delete(0,END)
        firstName_entry.delete(0,END)
        lastName_entry.delete(0,END)
        Password_entry.delete(0,END)
        userType_entry.delete(0,END)
        contactNumber_entry.delete(0,END)
        email_entry.delete(0,END)
        userType_combo.set('')

    def find_User():
        
        mycursor = mydb.cursor()

        sql = "SELECT U.UserId, U.firstName, U.lastName, U.loginPassword, U.uTypeId, T.typeOfUser, U.contactNumber, U.email FROM UserSystem U INNER JOIN UserType T ON U.uTypeId = T.uTypeId WHERE UserId = %s"
        val = UserId_text.get()
        
        try:
        
            mycursor.execute(sql, (val,))
            
            record = mycursor.fetchone()

            #for X in record:
            #    print(X)


            firstName_entry.delete(0, END)
            firstName_entry.insert(0, record[1])
            lastName_entry.delete(0, END)
            lastName_entry.insert(END, record[2])
            Password_entry.delete(0, END)
            Password_entry.insert(END, record[3])
            userType_entry.delete(0, END)
            userType_entry.insert(END, record[4])
            userType_combo.set(record[5])
            contactNumber_entry.delete(0, END)
            contactNumber_entry.insert(END, record[6])
            email_entry.delete(0, END)
            email_entry.insert(END, record[7])

        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)




    #UserID
    UserId_text = StringVar()
    UserId_label = Label(Frame, text='UserId', font=('bold', 12), pady=20)
    UserId_label.grid(row=0,column=0, sticky=W)
    UserId_entry = Entry(Frame, textvariable = UserId_text)
    UserId_entry.grid(row=0, column=1)

    #firstName
    firstName_text = StringVar()
    firstName_label = Label(Frame, text='First Name', font=('bold', 12), pady=20)
    firstName_label.grid(row=0,column=2, sticky=W)
    firstName_entry = Entry(Frame, textvariable = firstName_text)
    firstName_entry.grid(row=0, column=3)

    #lastName
    lastName_text = StringVar()
    lastName_label = Label(Frame, text='Last Name', font=('bold', 12), pady=20)
    lastName_label.grid(row=0,column=4, sticky=W)
    lastName_entry = Entry(Frame, textvariable = lastName_text)
    lastName_entry.grid(row=0, column=5)

    #Password
    Password_text = StringVar()
    Password_label = Label(Frame, text='Password', font=('bold', 12), pady=20)
    Password_label.grid(row=0,column=6, sticky=W)
    Password_entry = Entry(Frame, textvariable = Password_text)
    Password_entry.grid(row=0, column=7)



    #userType

    n = StringVar()
    userType_combo = ttk.Combobox (Frame, state="readonly", width = 16, textvariable = n) 
    
    # Adding combobox drop down list 
    userType_combo['values'] = combo_input()
    userType_combo.bind("<<ComboboxSelected>>",combo_inputID)
    userType_combo.grid(row=2, column=1) 



    userType_text = StringVar()
    userType_label = Label(Frame, text='User Type', font=('bold', 12), pady=20)
    userType_label.grid(row=2,column=0, sticky=W)
    userType_entry = Entry(Frame, textvariable = userType_text)

    #userType_entry.grid(row=3, column=1)



    #Contact Number
    contactNumber_text = StringVar()
    contactNumber_label = Label(Frame, text='Contact Number', font=('bold', 12), pady=20)
    contactNumber_label.grid(row=2,column=2, sticky=W)
    contactNumber_entry = Entry(Frame, textvariable = contactNumber_text)
    contactNumber_entry.grid(row=2, column=3)

    #email
    email_text = StringVar()
    email_label = Label(Frame, text='email', font=('bold', 12), pady=20)
    email_label.grid(row=2,column=4, sticky=W)
    email_entry = Entry(Frame, textvariable = email_text)
    email_entry.grid(row=2, column=5)

    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.place(x=425, y=300, anchor = "center", width = 750, height = 220)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=790, y=190, height = 220)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_User)

    #Buttons

    find_btn = Button(Frame, text='Find User by ID', width=12, command=find_User)
    find_btn.place(x=50, y=130)

    add_btn = Button(Frame, text='Add User', width=12, command=add_User)
    add_btn.place(x=210, y=130)

    delete_btn = Button(Frame, text='Delete User', width=12, command=delete_User)
    delete_btn.place(x=370, y=130)

    update_btn = Button(Frame, text='Update User', width=12, command=update_User)
    update_btn.place(x=530, y=130)

    clear_btn = Button(Frame, text='Clear input', width=12, command=clear_text)
    clear_btn.place(x=690, y=130)


    fill_list()
    return

if __name__ == "__main__":
    app = Tk()
    app.title('User control')
    app.geometry('850x450')

    OpenNewWindowUserD(app)
    app.mainloop()
