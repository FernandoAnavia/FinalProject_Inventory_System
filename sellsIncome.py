
from db import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pandas import *
import matplotlib.pyplot as plt
from sys import exit


def OpenNewWindowSells(Frame):

    def yearFunction():

        sqlQuery = "SELECT year(TDate) as year, round(sum(Total),2) as Total FROM ticket GROUP by year(TDate) order by year(TDate)"

        df = read_sql(sqlQuery, mydb)

        lb = [row for row in df['year']]
        plot = df.plot.bar(title="Yearly Income", x='year')
        plt.show()


    def monthFunction():

        if yearC_combo.get() == '':
            messagebox.showerror('Error','Please choose a year')
            return

        sqlQuery = "SELECT monthname(TDate) as month, round(sum(Total),2) as Total FROM ticket where year(TDate) = {c} GROUP by month(TDate) order by month(TDate)".format(c=yearC_combo.get())

        df = read_sql(sqlQuery, mydb)

        lb = [row for row in df['month']]
        plot = df.plot.bar(title="Monthly - " + yearC_combo.get(), x='month')
        plt.show()




    def month_YearFunction():

        sqlQuery = "SELECT month(TDate) as month, year(TDate) as year, round(sum(Total),2) as Total FROM ticket GROUP by year(TDate), month(TDate) order by year(TDate)"

        df = read_sql(sqlQuery, mydb)
        
        fig, ax = plt.subplots()

        for key, grp in df.groupby(['year']):
            ax = grp.plot(ax=ax, kind='line', x='month', y='Total', label=key, figsize=(8,6), grid=True)

        plt.legend(loc='best')

        plt.show()

    def combo_input():
        cursor = mydb.cursor()

        cursor.execute("select year(Tdate) as year from Ticket group by year(TDate) order by year(TDate)")
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

    yearly_btn = Button(Frame, text='Yearly Comparation', width=20, command=yearFunction)
    yearly_btn.place(x=50, y=50)

    monthly_btn = Button(Frame, text='Monthly by Year', width=20, command=monthFunction)
    monthly_btn.place(x=250, y=50)

    month_Year_btn = Button(Frame, text='Monthly over all years', width=20, command=month_YearFunction)
    month_Year_btn.place(x=450, y=50)

    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=580, y=150)

    # comboYear

    n = StringVar()
    yearC_combo = ttk.Combobox (Frame, state="readonly", width = 16, textvariable = n) 

    yearC_combo['values'] = combo_input()
    yearC_combo.place(x=265, y=100) 

    Frame.protocol('WM_DELETE_WINDOW',closure)
    return


if __name__ == "__main__":
    app = Tk()
    app.title('Income Report')
    app.geometry('700x200')

    OpenNewWindowSells(app)
    app.mainloop()