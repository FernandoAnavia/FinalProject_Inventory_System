from tkinter import *
from tkinter import messagebox
from db import *
from sys import exit

def OpenNewWindowItemClassification(Frame):


    def fill_list():

        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM ItemClassification")
        rows = cursor.fetchall()

        part_list.delete(0,END)

        for row in rows:
            part_list.insert(END, row)



    def add_classification():
        
        if classification_text.get() == '':
            messagebox.showerror('Require Fields', 'Please fill up the method classification')
            return
        
        mycursor = mydb.cursor()

        sql = "INSERT INTO ItemClassification (Classification) VALUES (%s)"
        val = ((classification_text.get(),))
        
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        fill_list()

        print(mycursor.rowcount, "classification added")


    def select_classification(event):
        try:
            global selected_classification
            index = part_list.curselection()[0]
            selected_classification = part_list.get(index)

            ItemClassID_entry.delete(0, END)
            ItemClassID_entry.insert(END, selected_classification[0])
            classification_entry.delete(0, END)
            classification_entry.insert(END, selected_classification[1])


        except IndexError:
            pass

    def delete_classification():
        
        mycursor = mydb.cursor()

        sql = "DELETE FROM ItemClassification WHERE ItemClassID = %s"
        val = ItemClassID_text.get()
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to delete the classification?', icon = 'warning')
        if MsgBox == 'yes':
        
            try:
                mycursor.execute(sql, (val,))
                mydb.commit()
            
            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "classification(s) deleted"))

        else:
            messagebox.showinfo ('Message', 'The classification was not deleted')

    def update_classification():

        mycursor = mydb.cursor()

        sql = "UPDATE ItemClassification SET Classification = %s WHERE ItemClassID = %s"
        val = (classification_text.get(), ItemClassID_text.get())
        
        MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to update the classification details?', icon = 'warning')
        if MsgBox == 'yes':

            try:
        
                mycursor.execute(sql, val)
                mydb.commit()

            except mysql.connector.Error as e:
                messagebox.showerror('Error',e)

            fill_list()

            messagebox.showinfo('Message',(mycursor.rowcount, "classification(s) updated"))

        else:
            messagebox.showinfo ('Message', 'The classification was not updated')


    def clear_text():

        ItemClassID_entry.delete(0,END)
        classification_entry.delete(0,END)



    def find_classification():
        
        mycursor = mydb.cursor()

        sql = "SELECT * FROM ItemClassification WHERE ItemClassID = %s"
        val = ItemClassID_text.get()
        
        try:
        
            mycursor.execute(sql, (val,))
            
            record = mycursor.fetchone()

            classification_entry.delete(0, END)
            classification_entry.insert(0, record[1])



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
    ItemClassID_text = StringVar()
    ItemClassID_label = Label(Frame, text='Item Class ID (A_I)', font=('bold', 14), pady=20)
    ItemClassID_label.grid(row=0,column=0)
    ItemClassID_entry = Entry(Frame, textvariable = ItemClassID_text)
    ItemClassID_entry.grid(row=0, column=1)

    #Name
    classification_text = StringVar()
    classification_label = Label(Frame, text='Classification', font=('bold', 14), pady=20)
    classification_label.grid(row=0,column=3)
    classification_entry = Entry(Frame, textvariable = classification_text)
    classification_entry.grid(row=0, column=4)



    #List
    part_list = Listbox(Frame, height=10, width=100, border=0)
    part_list.grid(row=5, column=0, columnspan=6, rowspan=8, pady=20, padx=20)

    scrollbar = Scrollbar(Frame)
    scrollbar.place(x=605, y=113, height = 160)
    part_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=part_list.yview)

    part_list.bind('<<ListboxSelect>>', select_classification)

    #Buttons

    find_btn = Button(Frame, text='Find Class by ID', width=15, command=find_classification)
    find_btn.grid(row=3, column=0)

    add_btn = Button(Frame, text='Add Class', width=12, command=add_classification)
    add_btn.grid(row=3, column=1)

    delete_btn = Button(Frame, text='Delete Class', width=12, command=delete_classification)
    delete_btn.grid(row=3, column=2)

    update_btn = Button(Frame, text='Update Class', width=12, command=update_classification)
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
    app.title('classification control')
    app.geometry('650x350')

    OpenNewWindowItemClassification(app)
    app.mainloop()