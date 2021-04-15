from tkinter import *
from tkinter import messagebox
from db import *

def OpenNewWindowBranchD(Frame):

    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM Branch")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_branch():
        
        if ID_text.get() == '' or Name_text.get() == '' or C_Number_text.get() == '' or email_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up all fields')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO Branch (BId, BName, contactNumber, email) VALUES (%s, %s, %s, %s)"
        val = (ID_text.get(), Name_text.get(), C_Number_text.get(), email_text.get())
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        fill_list()

        print(mycursor.rowcount, "Branch added")


    def select_branch(event):
        try:
            global selected_branch
            index = part_list.curselection()[0]
            selected_branch = part_list.get(index)

            ID_entry.delete(0, END)
            ID_entry.insert(END, selected_branch[0])
            Name_entry.delete(0, END)
            Name_entry.insert(END, selected_branch[1])
            C_Number_entry.delete(0, END)
            C_Number_entry.insert(END, selected_branch[2])
            email_entry.delete(0, END)
            email_entry.insert(END, selected_branch[3])

        except IndexError:
            pass

    def delete_branch():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM Branch WHERE BId = %s"
        val = ID_text.get()
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to delete the branch?', icon = 'warning')
        if MsgBox == 'yes':
        
            try:
                mycursor.execute(sql, (val,))
                mydb.commit()
            
            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "branch(s) deleted"))

        else:
            messagebox.showinfo ('Message', 'The Branch was not deleted')

    def update_branch():

        mycursor = mydb.cursor()

        sql = "UPDATE Branch SET BName = %s, contactNumber = %s, email = %s WHERE BId = %s"
        val = (Name_text.get(), C_Number_text.get(), email_text.get(), ID_text.get())
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to update the Branch details?', icon = 'warning')
        if MsgBox == 'yes':

            try:
        
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "Branch(s) updated"))

        else:
            messagebox.showinfo ('Message', 'The Branch was not updated')


    def clear_text():

        ID_entry.delete(0,END)
        Name_entry.delete(0,END)
        C_Number_entry.delete(0,END)
        email_entry.delete(0,END)


    def find_branch():
        
        mycursor = mydb.cursor()

        sql = "SELECT * FROM Branch WHERE BId = %s"
        val = ID_text.get()
        
        try:
        
            mycursor.execute(sql, (val,))
            
            record = mycursor.fetchone()

            Name_entry.delete(0, END)
            Name_entry.insert(0, record[1])
            C_Number_entry.delete(0, END)
            C_Number_entry.insert(END, record[2])
            email_entry.delete(0, END)
            email_entry.insert(END, record[3])


        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)



    #ID
    ID_text = StringVar()
    ID_label = Label(Frame, text='ID', font=('bold', 14), pady=20)
    ID_label.grid(row=0,column=0, sticky=W)
    ID_entry = Entry(Frame, textvariable = ID_text)
    ID_entry.grid(row=0, column=1)

    #Name
    Name_text = StringVar()
    Name_label = Label(Frame, text='Name', font=('bold', 14), pady=20)
    Name_label.grid(row=0,column=3, sticky=W)
    Name_entry = Entry(Frame, textvariable = Name_text)
    Name_entry.grid(row=0, column=4)

    #Description
    C_Number_text = StringVar()
    C_Number_label = Label(Frame, text='Contact Number', font=('bold', 14), pady=20)
    C_Number_label.grid(row=2,column=0, sticky=W)
    C_Number_entry = Entry(Frame, textvariable = C_Number_text)
    C_Number_entry.grid(row=2, column=1)

    #Branch
    email_text = StringVar()
    email_label = Label(Frame, text='email', font=('bold', 14), pady=20)
    email_label.grid(row=2,column=3, sticky=W)
    email_entry = Entry(Frame, textvariable = email_text)
    email_entry.grid(row=2, column=4)


    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.grid(row=5, column=0, columnspan=6, rowspan=8, pady=20, padx=20)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=605, y=180, height = 160)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_branch)

    #Buttons

    find_btn = Button(Frame, text='Find branch by ID', width=12, command=find_branch)
    find_btn.grid(row=3, column=0)

    add_btn = Button(Frame, text='Add branch', width=12, command=add_branch)
    add_btn.grid(row=3, column=1)

    delete_btn = Button(Frame, text='Delete branch', width=12, command=delete_branch)
    delete_btn.grid(row=3, column=2)

    update_btn = Button(Frame, text='Update branch', width=12, command=update_branch)
    update_btn.grid(row=3, column=3)

    clear_btn = Button(Frame, text='Clear input', width=12, command=clear_text)
    clear_btn.grid(row=3, column=4)

    fill_list()
    return


if __name__ == "__main__":
    app = Tk()
    app.title('Branch control')
    app.geometry('700x450')

    OpenNewWindowBranchD(app)
    app.mainloop()