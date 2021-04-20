
from db import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pandas import *
import matplotlib.pyplot as plt
from sys import exit



def OpenNewWindowIAnalysis(Frame):

    def yearFunction():

        if ItemName_combo.get() == '':
            messagebox.showerror('Error','Please choose an Item')
            return        

        sqlQuery = "SELECT I.IName as product, year(T.Tdate) as Year, month(T.Tdate) as Month, sum(O.Quantity) as Total FROM ItemOutput O left JOIN Item I ON I.ItemID = O.ItemID left join Ticket T ON O.TicketID = T.TicketID where I.ItemID = {c} group by I.IName, year(T.TDate), month(T.TDate) order by year(T.Tdate), month(T.TDate)".format(c=ItemName_text.get())

        df = read_sql(sqlQuery, mydb)

        fig, ax = plt.subplots()

        for key, grp in df.groupby(['Year']):
            ax = grp.plot(title = ItemName_combo.get(), ax=ax, kind='line', x='Month', y='Total', label=key, figsize=(8,6), grid=True)

        plt.legend(loc='best')

        plt.show()

        #lb = [row for row in df['month']]
        #plot = df.plot.bar(title="Yearly Income", x='year')
        #plt.show()


    def Stock():


        sqlQuery = "SELECT I.IName as Product, IFNULL(A.Quantity,0) - IFNULL(O.Quantity,0) AS Difference FROM Item I  LEFT JOIN ItemAcquired A ON I.ItemID = A.ItemID left JOIN ItemOutput O ON O.ItemID = I.ItemID group by I.ItemID"

        df = read_sql(sqlQuery, mydb)

        lb = [row for row in df['Product']]
        plot = df.plot.bar(title="Availability", x='Product', figsize=(13.5,8))
        plt.show()




    def month_YearFunction():

        if ItemName_combo.get() == '':
            messagebox.showerror('Error','Please choose an Item')
            return        

        if yearC_combo.get() == '':
            messagebox.showerror('Error','Please choose a Year')
            return

        sqlQuery = "SELECT I.IName as product, month(T.Tdate) as Month, sum(O.Quantity) as Total FROM ItemOutput O left JOIN Item I ON I.ItemID = O.ItemID left join Ticket T ON O.TicketID = T.TicketID where I.ItemID = {c} and year(TDate) = {d} group by I.IName, year(T.TDate), month(T.TDate) order by year(T.Tdate), month(T.TDate)".format(c=ItemName_text.get(),d=yearC_combo.get())

        df = read_sql(sqlQuery, mydb)

        lb = [row for row in df['Month']]
        plot = df.plot.bar(title="Yearly Income " + ItemName_combo.get() + " " + yearC_combo.get(), x='Month')
        plt.show()

    def combo_input():
        cursor = mydb.cursor()

        cursor.execute("select year(Tdate) as year from Ticket group by year(TDate) order by year(TDate)")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0])

        return result

    def combo_inputID(event):
        cursor = mydb.cursor()
        
        val =  ItemName_combo.get()

        sql = "SELECT ItemID FROM Item where IName = %s"
    
        cursor.execute(sql, (val,))
        BId = cursor.fetchone()
        print(BId)
        ItemName_entry.delete(0,END)
        ItemName_entry.insert(0,BId)

    def combo_input2():
        cursor = mydb.cursor()

        cursor.execute("SELECT IName FROM Item")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(row[0])

        return result

    def backCom():
        from reports import OpenNewWindowReports

        #Frame.iconify()
        win1 = Toplevel(Frame)
        win1.geometry('400x300')
        win1.title('Reports Window')
        Frame.withdraw()
        OpenNewWindowReports(win1)
        #win1.deiconify()
        return

    def closure():
        exit(0)

    #Buttons

    yearly_btn = Button(Frame, text='Yearly Sells by unit', width=20, command=month_YearFunction)
    yearly_btn.place(x=50, y=60)

    month_Year_btn = Button(Frame, text='Monthly Sells / years', width=20, command=yearFunction)
    month_Year_btn.place(x=250, y=60)

    monthly_btn = Button(Frame, text='Stock Available', width=20, command=Stock)
    monthly_btn.place(x=450, y=60)

    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=580, y=150)


    # comboYear

    n = StringVar()
    yearC_combo = ttk.Combobox (Frame, state="readonly", width = 16, textvariable = n) 

    yearC_combo['values'] = combo_input()
    yearC_combo.place(x=60, y=100) 

    #ComboItem

    m = StringVar()
    ItemName_combo = ttk.Combobox (Frame, state="readonly", width = 25, textvariable = m) 

    ItemName_combo['values'] = combo_input2()
    ItemName_combo.bind("<<ComboboxSelected>>",combo_inputID)
    ItemName_combo.grid(row=2, column=1) 

    ItemName_text = StringVar()
    ItemName_label = Label(Frame, text='Item', font=('bold', 12), pady=20)
    ItemName_label.grid(row=2,column=0, sticky=W)
    ItemName_entry = Entry(Frame, textvariable = ItemName_text)

    #ItemName_entry.grid(row=2, column=2)
    Frame.protocol('WM_DELETE_WINDOW',closure)
    return


if __name__ == "__main__":
    app = Tk()
    app.title('Item Analysis')
    app.geometry('700x200')

    OpenNewWindowIAnalysis(app)
    app.mainloop()