from tkinter import *
from tkinter import messagebox
from db import *
from sys import exit


def OpenNewWindowItemStatus(Frame):


    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM ItemStatus")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_Status():
        
        if Status_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up the method Status')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO ItemStatus (StatusItemO) VALUES (%s)"
        val = ((Status_text.get(),))
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        fill_list()

        print(mycursor.rowcount, "Status added")


    def select_Status(event):
        try:
            global selected_Status
            index = part_list.curselection()[0]
            selected_Status = part_list.get(index)

            statusID_entry.delete(0, END)
            statusID_entry.insert(END, selected_Status[0])
            Status_entry.delete(0, END)
            Status_entry.insert(END, selected_Status[1])


        except IndexError:
            pass

    def delete_Status():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM ItemStatus WHERE statusID = %s"
        val = statusID_text.get()
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to delete the Status?', icon = 'warning')
        if MsgBox == 'yes':
        
            try:
                mycursor.execute(sql, (val,))
                mydb.commit()
            
            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "Status(s) deleted"))

        else:
            messagebox.showinfo ('Message', 'The Status was not deleted')

    def update_Status():

        mycursor = mydb.cursor()

        sql = "UPDATE ItemStatus SET StatusItemO = %s WHERE statusID = %s"
        val = (Status_text.get(), statusID_text.get())
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to update the Status details?', icon = 'warning')
        if MsgBox == 'yes':

            try:
        
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "Status(s) updated"))

        else:
            messagebox.showinfo ('Message', 'The Status was not updated')


    def clear_text():

        statusID_entry.delete(0,END)
        Status_entry.delete(0,END)



    def find_Status():
        
        mycursor = mydb.cursor()

        sql = "SELECT * FROM ItemStatus WHERE statusID = %s"
        val = statusID_text.get()
        
        try:
        
            mycursor.execute(sql, (val,))
            
            record = mycursor.fetchone()

            Status_entry.delete(0, END)
            Status_entry.insert(0, record[1])



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
    statusID_text = StringVar()
    statusID_label = Label(Frame, text='Item Status ID (A_I)', font=('bold', 14), pady=20)
    statusID_label.grid(row=0,column=0)
    statusID_entry = Entry(Frame, textvariable = statusID_text)
    statusID_entry.grid(row=0, column=1)

    #Name
    Status_text = StringVar()
    Status_label = Label(Frame, text='Item Status', font=('bold', 14), pady=20)
    Status_label.grid(row=0,column=3)
    Status_entry = Entry(Frame, textvariable = Status_text)
    Status_entry.grid(row=0, column=4)



    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.grid(row=5, column=0, columnspan=6, rowspan=8, pady=20, padx=20)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=605, y=113, height = 160)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_Status)

    #Buttons

    find_btn = Button(Frame, text='Find Status by ID', width=15, command=find_Status)
    find_btn.grid(row=3, column=0)

    add_btn = Button(Frame, text='Add Status', width=12, command=add_Status)
    add_btn.grid(row=3, column=1)

    delete_btn = Button(Frame, text='Delete Status', width=12, command=delete_Status)
    delete_btn.grid(row=3, column=2)

    update_btn = Button(Frame, text='Update Status', width=12, command=update_Status)
    update_btn.grid(row=3, column=3)

    clear_btn = Button(Frame, text='Clear input', width=12, command=clear_text)
    clear_btn.grid(row=3, column=4)

    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=530, y=300)


    fill_list()
    Frame.protocol('WM_DELETE_WINDOW',closure)
    return

if __name__ == "__main__":
    app = Tk()
    app.title('Status control')
    app.geometry('650x350')

    OpenNewWindowItemStatus(app)
    app.mainloop()