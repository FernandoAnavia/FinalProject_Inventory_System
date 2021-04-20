from tkinter import *
from tkinter import messagebox
from db import *
from sys import exit

def OpenNewWindowPayment(Frame):


    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM payment")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_payment():
        
        if payment_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up the method payment')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO payment (Method) VALUES (%s)"
        val = ((payment_text.get(),))
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        fill_list()

        print(mycursor.rowcount, "payment added")


    def select_payment(event):
        try:
            global selected_payment
            index = part_list.curselection()[0]
            selected_payment = part_list.get(index)

            paymentID_entry.delete(0, END)
            paymentID_entry.insert(END, selected_payment[0])
            payment_entry.delete(0, END)
            payment_entry.insert(END, selected_payment[1])


        except IndexError:
            pass

    def delete_payment():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM payment WHERE paymentID = %s"
        val = paymentID_text.get()
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to delete the payment?', icon = 'warning')
        if MsgBox == 'yes':
        
            try:
                mycursor.execute(sql, (val,))
                mydb.commit()
            
            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "payment(s) deleted"))

        else:
            messagebox.showinfo ('Message', 'The payment was not deleted')

    def update_payment():

        mycursor = mydb.cursor()

        sql = "UPDATE payment SET Method = %s WHERE paymentTD = %s"
        val = (payment_text.get(), paymentID_text.get())
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to update the payment details?', icon = 'warning')
        if MsgBox == 'yes':

            try:
        
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "payment(s) updated"))

        else:
            messagebox.showinfo ('Message', 'The payment was not updated')


    def clear_text():

        paymentID_entry.delete(0,END)
        payment_entry.delete(0,END)



    def find_payment():
        
        mycursor = mydb.cursor()

        sql = "SELECT * FROM payment WHERE paymentID = %s"
        val = paymentID_text.get()
        
        try:
        
            mycursor.execute(sql, (val,))
            
            record = mycursor.fetchone()

            payment_entry.delete(0, END)
            payment_entry.insert(0, record[1])



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
    paymentID_text = StringVar()
    paymentID_label = Label(Frame, text='Payment ID (A_I)', font=('bold', 14), pady=20)
    paymentID_label.grid(row=0,column=0)
    paymentID_entry = Entry(Frame, textvariable = paymentID_text)
    paymentID_entry.grid(row=0, column=1)

    #Name
    payment_text = StringVar()
    payment_label = Label(Frame, text='Payment Method', font=('bold', 14), pady=20)
    payment_label.grid(row=0,column=3)
    payment_entry = Entry(Frame, textvariable = payment_text)
    payment_entry.grid(row=0, column=4)



    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.grid(row=5, column=0, columnspan=6, rowspan=8, pady=20, padx=20)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=605, y=113, height = 160)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_payment)

    #Buttons

    find_btn = Button(Frame, text='Find payment by ID', width=15, command=find_payment)
    find_btn.grid(row=3, column=0)

    add_btn = Button(Frame, text='Add payment', width=12, command=add_payment)
    add_btn.grid(row=3, column=1)

    delete_btn = Button(Frame, text='Delete payment', width=12, command=delete_payment)
    delete_btn.grid(row=3, column=2)

    update_btn = Button(Frame, text='Update payment', width=12, command=update_payment)
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
    app.title('payment control')
    app.geometry('650x350')

    OpenNewWindowPayment(app)
    app.mainloop()