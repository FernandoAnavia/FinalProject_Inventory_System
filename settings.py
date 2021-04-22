from tkinter import *
from tkinter import messagebox
from db import *
from tkinter import ttk
import re
from sys import exit


def OpenNewWindiwSettings(Frame):

    def combo_input():
    
        cursor = mydb.cursor()

        cursor.execute("SELECT IName FROM Item")
        rows = cursor.fetchall()

        result = ['**ALL PRODUCTS**']

        for row in rows:
            result.append(row[0])

        return result
        

    def combo_inputID(event):
        
        cursor = mydb.cursor()
        
        val =  Expiry_combo.get()

        sql = "SELECT ItemID FROM ITEM where IName = %s"
    
        cursor.execute(sql, (val,))
        BId = cursor.fetchone()
        print(BId)
        Expiry_entryID.delete(0,END)
        Expiry_entryID.insert(0,BId)



    def fill_list():

        cursor = mydb.cursor()

        sql = "Select ItemID, IName, ExpDateVal FROM Item order by ExpDateVal"

        cursor.execute(sql)

        tree.delete(*tree.get_children())

        for rec in cursor:
            tree.insert('','end',value=rec)

  



    def lowStockFunction():

        mycursor = mydb.cursor()

        sql = "UPDATE SingleVal set val = %s"
        val = lowStock_text.get()

        try:
    
            mycursor.execute(sql, (val,))
            mydb.commit()

        except mysql.connector.Error as e:
            messagebox.showerror('Error',e)

        messagebox.showinfo('Info','Low Stock Alert updated to: ' + lowStock_text.get())


    def ExpiryFunction():
        
        mycursor = mydb.cursor()

        if Expiry_combo.get() == '**ALL PRODUCTS**':
            MsgBox = messagebox.askquestion ('Confirmation message', 'Are you sure you want to modify the expiry value of ALL PRODUCTS?', icon = 'warning')
            if MsgBox == 'yes':
            
                sql = "UPDATE Item set ExpDateVal = %s"
                val = Expiry_text.get()
                print(val)

                try:
            
                    mycursor.execute(sql, (val,))
                    mydb.commit()

                except mysql.connector.Error as e:
                    messagebox.showerror('Error',e)

                fill_list()               

            else:
                messagebox.showinfo('Info','Modification aborted')
        else:
                sql = "UPDATE Item set ExpDateVal = %s where ItemID = %s"
                val = (Expiry_text.get(),Expiry_textID.get())
  
                try:
            
                    mycursor.execute(sql, val)
                    mydb.commit()

                except mysql.connector.Error as e:
                    messagebox.showerror('Error',e)

                fill_list()  



    def backCom():
        from admin_Dashboard import OpenNewWindowAdmnDash

        #Frame.iconify()
        win1 = Toplevel(Frame)
        win1.geometry('800x500')
        win1.title('Administrator')
        Frame.withdraw()
        OpenNewWindowAdmnDash(win1)
        #win1.deiconify()
        return

    def closure():
        exit(0)

    #Low Stock
    lowStock_text = StringVar()
    lowStock_label = Label(Frame, text='Low Stock Alert', font=('bold', 14))
    lowStock_label.place(x=50, y=50)
    lowStock_entry = Entry(Frame, textvariable = lowStock_text)
    lowStock_entry.place(x=200, y=55)

    #Expiry

    n = StringVar()
    Expiry_combo = ttk.Combobox (Frame, state="readonly", width = 16, textvariable = n) 
    
    # Adding combobox drop down list 
    Expiry_combo['values'] = combo_input()
    Expiry_combo.bind("<<ComboboxSelected>>",combo_inputID)
    Expiry_combo.place(x=200, y=140, width=130) 



    Expiry_text = StringVar()
    Expiry_textID = StringVar()
    Expiry_label = Label(Frame, text='Expiry Alert', font=('bold', 14), pady=14)
    Expiry_label.place(x=50, y=130)
    Expiry_entryID = Entry(Frame, textvariable = Expiry_textID)
    #Expiry_entryID.place(x=500, y=180)
    Expiry_entry = Entry(Frame, textvariable = Expiry_text)
    Expiry_entry.place(x=350, y=140)

    #treeView

    columns = ('Item ID', 'Product', 'Expiry Alert (Days)')
    tree = ttk.Treeview(Frame, height=10, columns=columns, show='headings')
    tree.place(x=50, y= 220, width = 600 , height = 200)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=CENTER)

    sb = Scrollbar(Frame, orient=VERTICAL, command=tree.yview)
    sb.place(x=631, y=221, height=198)
    tree.config(yscrollcommand=sb.set)

    #Buttons

    Expiry_btn = Button(Frame, text='Submit', width=15, command=ExpiryFunction)
    Expiry_btn.place(x=510, y=135)

    lowStock_btn = Button(Frame, text='Submit', width=15, command=lowStockFunction)
    lowStock_btn.place(x=510, y=55)


    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=580, y=500)


    fill_list()
    Frame.protocol('WM_DELETE_WINDOW',closure)
    return

if __name__ == "__main__":
    app = Tk()
    app.title('Settings')
    app.geometry('700x550')
    

    OpenNewWindiwSettings(app)
    app.mainloop()