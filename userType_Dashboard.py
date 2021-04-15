from tkinter import *
from tkinter import messagebox
from db import *


def OpenNewWindowUserTypeD(Frame):


    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM userType")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_userType():
        
        if userTypeId_text.get() == '' or typeOfUser_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up all fields')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO userType (uTypeId, typeOfUser) VALUES (%s, %s)"
        val = (userTypeId_text.get(), typeOfUser_text.get())
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        fill_list()

        print(mycursor.rowcount, "userType added")


    def select_userType(event):
        try:
            global selected_userType
            index = part_list.curselection()[0]
            selected_userType = part_list.get(index)

            userTypeId_entry.delete(0, END)
            userTypeId_entry.insert(END, selected_userType[0])
            typeOfUser_entry.delete(0, END)
            typeOfUser_entry.insert(END, selected_userType[1])


        except IndexError:
            pass

    def delete_userType():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM userType WHERE uTypeId = %s"
        val = userTypeId_text.get()
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to delete the userType?', icon = 'warning')
        if MsgBox == 'yes':
        
            try:
                mycursor.execute(sql, (val,))
                mydb.commit()
            
            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "userType(s) deleted"))

        else:
            messagebox.showinfo ('Message', 'The userType was not deleted')

    def update_userType():

        mycursor = mydb.cursor()

        sql = "UPDATE userType SET typeOfUser = %s WHERE uTypeId = %s"
        val = (typeOfUser_text.get(), userTypeId_text.get())
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to update the userType details?', icon = 'warning')
        if MsgBox == 'yes':

            try:
        
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "userType(s) updated"))

        else:
            messagebox.showinfo ('Message', 'The userType was not updated')


    def clear_text():

        userTypeId_entry.delete(0,END)
        typeOfUser_entry.delete(0,END)



    def find_userType():
        
        mycursor = mydb.cursor()

        sql = "SELECT * FROM userType WHERE uTypeId = %s"
        val = userTypeId_text.get()
        
        try:
        
            mycursor.execute(sql, (val,))
            
            record = mycursor.fetchone()

            typeOfUser_entry.delete(0, END)
            typeOfUser_entry.insert(0, record[1])



        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)


    #ID
    userTypeId_text = StringVar()
    userTypeId_label = Label(Frame, text='User Type Id', font=('bold', 14), pady=20)
    userTypeId_label.grid(row=0,column=0)
    userTypeId_entry = Entry(Frame, textvariable = userTypeId_text)
    userTypeId_entry.grid(row=0, column=1)

    #Name
    typeOfUser_text = StringVar()
    typeOfUser_label = Label(Frame, text='Type Of User', font=('bold', 14), pady=20)
    typeOfUser_label.grid(row=0,column=3)
    typeOfUser_entry = Entry(Frame, textvariable = typeOfUser_text)
    typeOfUser_entry.grid(row=0, column=4)



    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.grid(row=5, column=0, columnspan=6, rowspan=8, pady=20, padx=20)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=605, y=113, height = 160)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_userType)

    #Buttons

    find_btn = Button(Frame, text='Find userType by ID', width=15, command=find_userType)
    find_btn.grid(row=3, column=0)

    add_btn = Button(Frame, text='Add userType', width=12, command=add_userType)
    add_btn.grid(row=3, column=1)

    delete_btn = Button(Frame, text='Delete userType', width=12, command=delete_userType)
    delete_btn.grid(row=3, column=2)

    update_btn = Button(Frame, text='Update userType', width=12, command=update_userType)
    update_btn.grid(row=3, column=3)

    clear_btn = Button(Frame, text='Clear input', width=12, command=clear_text)
    clear_btn.grid(row=3, column=4)


    fill_list()
    return

if __name__ == "__main__":
    app = Tk()
    app.title('userType control')
    app.geometry('650x350')

    OpenNewWindowUserTypeD(app)
    app.mainloop()