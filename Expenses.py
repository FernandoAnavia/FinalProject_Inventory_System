
from db import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pandas import *
import numpy as np
from sys import exit
import matplotlib.pyplot as plt


def OpenNewWindowExpenses(Frame):

    def yearFunction():

        sqlQuery = "SELECT year(ODate) as year, round(sum(Total),2) as Total FROM Orders GROUP by year(ODate) order by year(ODate)"

        df = read_sql(sqlQuery, mydb)

        lb = [row for row in df['year']]
        plot = df.plot.bar(title="Yearly Outcome", x='year')

        for i in plot.patches:
            plot.text(i.get_x()-.03, i.get_height()+1,round(i.get_height(),0), fontsize= 9, color='black', weight='bold')

        plt.show()


    def monthFunction():

        if yearC_combo.get() == '':
            messagebox.showerror('Error','Please choose a year')
            return

        sqlQuery = "SELECT monthname(ODate) as month, round(sum(Total),2) as Total FROM Orders where year(ODate) = {c} GROUP by month(ODate) order by month(ODate)".format(c=yearC_combo.get())

        df = read_sql(sqlQuery, mydb)

        lb = [row for row in df['month']]
        plot = df.plot.bar(title="Monthly - " + yearC_combo.get(), x='month')

        for i in plot.patches:
            plot.text(i.get_x()-.03, i.get_height()+1,round(i.get_height(),0), fontsize= 9, color='black', weight='bold')

        plt.show()

    def month_YearFunction():

        sqlQuery = "SELECT month(ODate) as month, year(ODate) as year, round(sum(Total),2) as Total FROM Orders GROUP by year(ODate), month(ODate) order by year(ODate)"

        df = read_sql(sqlQuery, mydb)
        
        fig, ax = plt.subplots()

        for key, grp in df.groupby(['year']):
            ax = grp.plot(ax=ax, kind='line', x='month', y='Total', label=key, figsize=(8,6), grid=True)
                

        plt.legend(loc='best')

        plt.show()

    def Income_Outcome():

        cursor = mydb.cursor()

        cursor.execute("SELECT round(sum(Total),2) as Total FROM Orders GROUP by year(ODate) order by year(ODate)")
        rows = cursor.fetchall()

        TotalOut = []

        for row in rows:
            TotalOut.append(row[0])

        cursor.execute("SELECT round(sum(Total),2) as Total FROM ticket GROUP by year(TDate) order by year(TDate)")
        rows = cursor.fetchall()

        TotalIn = []

        for row in rows:
            TotalIn.append(row[0])


        cursor.execute("SELECT year(TDate) as year FROM ticket GROUP by year(TDate) order by year(TDate)")
        rows = cursor.fetchall()

        yearV = []
        Earn =[]
        n = -1

        for row in rows:
            n = n+1
            yearV.append(row[0])
            Earn.append(TotalIn[n]-TotalOut[n])

        barCol = ['g','r','b']

        plotData = DataFrame({
            "TotalEarned": TotalIn,
            "TotalExpended": TotalOut,
            "Final Profit/Loss": Earn},
            index=yearV
            )

        ax = plotData.plot.bar(title="Income", xlabel="year", ylabel="Total", stacked=False, color= barCol, grid=True, figsize=(9,7))
        

        for i in ax.patches:
            ax.text(i.get_x()-.03, i.get_height()+1,round(i.get_height(),0), fontsize= 9, color='black', weight='bold')

        plt.show()

    def combo_input():
        cursor = mydb.cursor()

        cursor.execute("select year(Odate) as year from Orders group by year(ODate) order by year(ODate)")
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
    yearly_btn.place(x=20, y=50)

    monthly_btn = Button(Frame, text='Monthly by Year', width=20, command=monthFunction)
    monthly_btn.place(x=185, y=50)

    month_Year_btn = Button(Frame, text='Monthly over all years', width=20, command=month_YearFunction)
    month_Year_btn.place(x=350, y=50)    

    month_Year_btn = Button(Frame, text='Income Vs Outcome', width=20, command=Income_Outcome)
    month_Year_btn.place(x=515, y=50)

    back_btn = Button(Frame, text='BACK', width=12, command=backCom)
    back_btn.place(x=580, y=150)

    # comboYear

    n = StringVar()
    yearC_combo = ttk.Combobox (Frame, state="readonly", width = 16, textvariable = n) 

    yearC_combo['values'] = combo_input()
    yearC_combo.place(x=200, y=100) 

    Frame.protocol('WM_DELETE_WINDOW',closure)
    return


if __name__ == "__main__":
    app = Tk()
    app.title('Expenses Report')
    app.geometry('700x200')

    OpenNewWindowExpenses(app)
    app.mainloop()